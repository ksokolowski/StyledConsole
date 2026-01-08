"""Styled extension of Rich Columns.

This module provides `StyledColumns`, which inherits from `rich.columns.Columns`
and adds policy awareness for emoji sanitization and VS16 emoji width fix.

VS16 Emoji Width Fix:
Rich's cell_len() miscalculates VS16 emojis (☁️, ⚙️, etc.) as width 1,
but modern terminals render them at width 2. This causes column layout
misalignment. We fix this by temporarily patching Rich's cell_len to use
our visual_width during columns rendering.
"""

from __future__ import annotations

from collections.abc import Generator, Iterable
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Literal

from rich.columns import Columns

from styledconsole.policy import RenderPolicy, get_default_policy
from styledconsole.utils.icon_data import EMOJI_TO_ICON
from styledconsole.utils.terminal import is_modern_terminal

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult


@contextmanager
def _patched_cell_len() -> Generator[None, None, None]:
    """Context manager to temporarily patch Rich's cell_len with visual_width.

    This fixes VS16 emoji width miscalculation in modern terminals.
    Rich's cell_len returns 1 for VS16 emojis, but modern terminals render
    them at width 2, causing column layout misalignment.

    We must patch cell_len in ALL Rich modules that import it directly,
    not just in rich.cells, because Python's import system creates separate
    references. This includes:
    - rich.cells (source)
    - rich.segment (CRITICAL - used for all segment width calculations)
    - rich.text
    - rich.containers
    - rich.panel
    - rich._wrap

    We also patch cached_cell_len (LRU-cached version) used by rich.segment.
    """
    if not is_modern_terminal():
        # No patch needed for non-modern terminals
        yield
        return

    import rich._wrap
    import rich.cells
    import rich.containers
    import rich.panel
    import rich.segment
    import rich.text

    from styledconsole.utils.text import visual_width

    def patched_cell_len(text: str) -> int:
        """Use visual_width for accurate emoji width in modern terminals."""
        return visual_width(text)

    # Clear LRU cache FIRST to prevent stale cached width values
    if hasattr(rich.cells.cached_cell_len, "cache_clear"):
        rich.cells.cached_cell_len.cache_clear()

    # Save original functions from ALL modules that use cell_len
    originals = {
        "cells.cell_len": rich.cells.cell_len,
        "cells.cached_cell_len": rich.cells.cached_cell_len,
        "segment.cell_len": rich.segment.cell_len,
        "segment.cached_cell_len": rich.segment.cached_cell_len,
        "text": rich.text.cell_len,
        "containers": rich.containers.cell_len,
        "panel": rich.panel.cell_len,
        "_wrap": rich._wrap.cell_len,
    }

    # Patch ALL modules including segment and cached_cell_len
    rich.cells.cell_len = patched_cell_len  # type: ignore[assignment]
    rich.cells.cached_cell_len = patched_cell_len  # type: ignore[assignment]
    rich.segment.cell_len = patched_cell_len  # type: ignore[assignment]
    rich.segment.cached_cell_len = patched_cell_len  # type: ignore[assignment]
    rich.text.cell_len = patched_cell_len  # type: ignore[assignment]
    rich.containers.cell_len = patched_cell_len  # type: ignore[assignment]
    rich.panel.cell_len = patched_cell_len  # type: ignore[assignment]
    rich._wrap.cell_len = patched_cell_len  # type: ignore[assignment]

    try:
        yield
    finally:
        # Restore ALL originals
        rich.cells.cell_len = originals["cells.cell_len"]  # type: ignore[assignment]
        rich.cells.cached_cell_len = originals["cells.cached_cell_len"]  # type: ignore[assignment]
        rich.segment.cell_len = originals["segment.cell_len"]  # type: ignore[assignment]
        rich.segment.cached_cell_len = originals["segment.cached_cell_len"]  # type: ignore[assignment]
        rich.text.cell_len = originals["text"]  # type: ignore[assignment]
        rich.containers.cell_len = originals["containers"]  # type: ignore[assignment]
        rich.panel.cell_len = originals["panel"]  # type: ignore[assignment]
        rich._wrap.cell_len = originals["_wrap"]  # type: ignore[assignment]


class StyledColumns(Columns):
    """A Rich Columns with policy awareness.

    Features:
    - Auto-converts emojis to ASCII[OK] if policy.emoji=False
    - VS16 emoji width fix for proper alignment in modern terminals

    Example:
        >>> from styledconsole import Console, StyledColumns
        >>> console = Console()
        >>> items = ["Item 1", "Item 2", "Item 3"]
        >>> columns = StyledColumns(items, padding=(0, 2))
        >>> console.print(columns)
    """

    def __init__(
        self,
        renderables: Iterable[Any] | None = None,
        padding: int | tuple[int] | tuple[int, int] | tuple[int, int, int, int] = (0, 1),
        *,
        policy: RenderPolicy | None = None,
        width: int | None = None,
        expand: bool = False,
        equal: bool = False,
        column_first: bool = False,
        right_to_left: bool = False,
        align: Literal["left", "center", "right"] | None = None,
        title: str | None = None,
    ) -> None:
        """Initialize StyledColumns.

        Args:
            renderables: Iterable of renderable items to display in columns.
            padding: Padding around each column. Can be int or tuple (top, right, bottom, left).
            policy: RenderPolicy to use. Defaults to global default policy.
            width: Width constraint for columns.
            expand: Expand columns to fill available width.
            equal: Make all columns equal width.
            column_first: Fill columns vertically instead of horizontally.
            right_to_left: Render columns from right to left.
            align: Alignment of content within columns.
            title: Optional title for the columns layout.
        """
        self._policy = policy or get_default_policy()

        # Sanitize renderables if emoji is disabled
        if renderables is not None and not self._policy.emoji:
            renderables = [self._sanitize(r) for r in renderables]

        super().__init__(
            renderables,
            padding=padding,
            width=width,
            expand=expand,
            equal=equal,
            column_first=column_first,
            right_to_left=right_to_left,
            align=align,
            title=title,
        )

    def add_renderable(self, renderable: Any) -> None:
        """Add a renderable to the columns, sanitizing if needed."""
        if not self._policy.emoji:
            renderable = self._sanitize(renderable)
        super().add_renderable(renderable)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render columns with patched cell_len for VS16 emoji fix."""
        with _patched_cell_len():
            yield from super().__rich_console__(console, options)

    def _sanitize(self, content: Any) -> Any:
        """Sanitize content based on policy (e.g. converting emojis).

        Uses plain text replacements for simple strings.
        """
        if isinstance(content, str):
            result = content
            # Iterate through known emojis and replace with ASCII
            for emoji, mapping in EMOJI_TO_ICON.items():
                if emoji in result:
                    result = result.replace(emoji, mapping.ascii)
            return result
        return content
