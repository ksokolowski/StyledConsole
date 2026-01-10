"""Styled extension of Rich Columns.

This module provides `StyledColumns`, which inherits from `rich.columns.Columns`
and adds policy awareness for emoji sanitization and VS16 emoji width fix.

VS16 Emoji Width Fix:
Rich's cell_len() miscalculates VS16 emojis (☁️, ⚙️, etc.) as width 1,
but modern terminals render them at width 2. This causes column layout
misalignment. We fix this by temporarily patching Rich's cell_len to use
our visual_width during columns rendering (via shared utils/rich_compat.py).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, Literal

from rich.columns import Columns

from styledconsole.policy import RenderPolicy, get_default_policy
from styledconsole.utils.rich_compat import patched_cell_len
from styledconsole.utils.sanitize import sanitize_emoji_content

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult


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
        with patched_cell_len():
            yield from super().__rich_console__(console, options)

    def _sanitize(self, content: Any) -> Any:
        """Sanitize content based on policy (e.g. converting emojis).

        Uses shared sanitize_emoji_content for consistent behavior.
        """
        return sanitize_emoji_content(content, with_color=True)
