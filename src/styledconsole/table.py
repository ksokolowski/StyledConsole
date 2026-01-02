"""Styled extension of Rich Table.

This module provides `StyledTable`, which inherits from `rich.table.Table`
and adds policy awareness for border styles and emoji sanitization.

VS16 Emoji Width Fix:
Rich's cell_len() miscalculates VS16 emojis (☁️, ⚙️, etc.) as width 1,
but modern terminals render them at width 2. This causes table border
misalignment. We fix this by temporarily patching Rich's cell_len to use
our visual_width during table rendering.
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from rich.markup import escape
from rich.table import Table

from styledconsole.core.box_mapping import get_box_style_for_policy
from styledconsole.policy import RenderPolicy, get_default_policy
from styledconsole.utils.icon_data import EMOJI_TO_ICON
from styledconsole.utils.terminal import is_modern_terminal

if TYPE_CHECKING:
    from rich.box import Box
    from rich.console import Console, ConsoleOptions, RenderResult


@contextmanager
def _patched_cell_len() -> Generator[None, None, None]:
    """Context manager to temporarily patch Rich's cell_len with visual_width.

    This fixes VS16 emoji width miscalculation in modern terminals.
    Rich's cell_len returns 1 for VS16 emojis, but modern terminals render
    them at width 2, causing table border misalignment.

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


class StyledTable(Table):
    """A Rich Table with policy awareness.

    Features:
    - Auto-downgrades border styles to ASCII if policy.unicode=False
    - Auto-converts emojis to ASCII[OK] if policy.emoji=False
    """

    def __init__(
        self,
        *args: Any,
        policy: RenderPolicy | None = None,
        box: Box | None = None,
        border_style: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize StyledTable.

        Args:
            *args: Arguments passed to rich.table.Table
            policy: RenderPolicy to use. Defaults to global default policy.
            box: Rich Box instance (overrides policy if provided directly).
            border_style: StyledConsole border name (e.g. "rounded") used if box is None.
            **kwargs: Keyword arguments passed to rich.table.Table
        """
        self._policy = policy or get_default_policy()

        # Handle box style selection based on policy
        if box is None:
            # If border_style name is provided, use it with policy fallback
            # Otherwise use default "rounded" (or whatever Rich uses) with policy fallback
            target_style = border_style or "rounded"
            box = get_box_style_for_policy(target_style, self._policy)

        super().__init__(*args, box=box, **kwargs)

    def add_row(self, *renderables: Any, **kwargs: Any) -> None:
        """Add a row of renderables, sanitizing content if needed."""
        if not self._policy.emoji:
            renderables = tuple(self._sanitize(r) for r in renderables)
        super().add_row(*renderables, **kwargs)

    def add_column(self, header: Any = "", footer: Any = "", **kwargs: Any) -> None:
        """Add a column, sanitizing header/footer if needed."""
        if not self._policy.emoji:
            header = self._sanitize(header)
            footer = self._sanitize(footer)
        super().add_column(header, footer, **kwargs)

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render table with patched cell_len for VS16 emoji fix."""
        with _patched_cell_len():
            yield from super().__rich_console__(console, options)

    def _sanitize(self, content: Any) -> Any:
        """Sanitize content based on policy (e.g. converting emojis).

        Uses Rich markup for replacements to ensure correct width calculation.
        """
        if isinstance(content, str):
            result = content
            # Iterate through known emojis and replace with markup-safe ASCII
            for emoji, mapping in EMOJI_TO_ICON.items():
                if emoji in result:
                    if mapping.color:
                        # Use Rich markup for color
                        replacement = f"[{mapping.color}]{escape(mapping.ascii)}[/]"
                    else:
                        replacement = escape(mapping.ascii)
                    result = result.replace(emoji, replacement)
            return result
        return content
