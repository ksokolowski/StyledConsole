"""Styled extension of Rich Table.

This module provides `StyledTable`, which inherits from `rich.table.Table`
and adds policy awareness for border styles and emoji sanitization.

VS16 Emoji Width Fix:
Rich's cell_len() miscalculates VS16 emojis (☁️, ⚙️, etc.) as width 1,
but modern terminals render them at width 2. This causes table border
misalignment. We fix this by temporarily patching Rich's cell_len to use
our visual_width during table rendering (via shared utils/rich_compat.py).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.table import Table

from styledconsole.core.box_mapping import get_box_style_for_policy
from styledconsole.policy import RenderPolicy, get_default_policy
from styledconsole.utils.rich_compat import patched_cell_len
from styledconsole.utils.sanitize import sanitize_emoji_content

if TYPE_CHECKING:
    from rich.box import Box
    from rich.console import Console, ConsoleOptions, RenderResult


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
        with patched_cell_len():
            yield from super().__rich_console__(console, options)

    def _sanitize(self, content: Any) -> Any:
        """Sanitize content based on policy (e.g. converting emojis).

        Uses shared sanitize_emoji_content for consistent behavior.
        """
        return sanitize_emoji_content(content, with_color=True)
