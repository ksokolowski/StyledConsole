"""Styled extension of Rich Table.

This module provides `StyledTable`, which inherits from `rich.table.Table`
and adds policy awareness for border styles and emoji sanitization.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.table import Table

from styledconsole.core.box_mapping import get_box_style_for_policy
from styledconsole.policy import RenderPolicy, get_default_policy
from styledconsole.utils.icon_data import EMOJI_TO_ICON
from rich.markup import escape

if TYPE_CHECKING:
    from rich.box import Box
    from rich.console import ConsoleOptions, ConsoleRenderable, RenderResult
    from rich.console import Console as RichConsole


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

    # Note: We don't need to override __rich_console__ usually, 
    # as inheritance handles the rendering. 
    # But if we wanted to enforce policy dynamically at render time
    # (in case policy changes between init and print), we might need hooks.
    # For now, we assume policy is static per table instance.
