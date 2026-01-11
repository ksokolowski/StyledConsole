"""TerminalRenderer - renders ConsoleObjects to terminal using Rich.

This renderer converts ConsoleObjects to Rich renderables and outputs
them to the terminal with ANSI color codes.

Example:
    >>> from styledconsole.rendering import TerminalRenderer
    >>> from styledconsole.model import Frame, Text
    >>>
    >>> renderer = TerminalRenderer()
    >>> frame = Frame(content=Text(content="Hello"), title="Greeting")
    >>> renderer.render(frame)  # Prints to stdout
"""

from __future__ import annotations

from typing import IO, TYPE_CHECKING, Any

from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.rule import Rule as RichRule
from rich.style import Style as RichStyle
from rich.table import Table as RichTable
from rich.text import Text as RichText

from styledconsole.rendering.base import BaseRenderer

if TYPE_CHECKING:
    from styledconsole.model import (
        Banner,
        Frame,
        Group,
        Layout,
        Rule,
        Spacer,
        Style,
        Table,
        Text,
    )
    from styledconsole.rendering.context import RenderContext


class TerminalRenderer(BaseRenderer):
    """Renders ConsoleObjects to terminal using Rich.

    This renderer converts model objects to Rich renderables and prints
    them to stdout or a file-like object.

    Example:
        >>> renderer = TerminalRenderer()
        >>> renderer.render(frame)  # Print to stdout
        >>> renderer.render(frame, target=sys.stderr)  # Print to stderr
    """

    def __init__(self, console: RichConsole | None = None) -> None:
        """Initialize the terminal renderer.

        Args:
            console: Optional Rich Console to use. If None, creates one.
        """
        self._console = console or RichConsole()

    def render(
        self,
        obj: Any,
        target: IO[str] | None = None,
        context: RenderContext | None = None,
    ) -> None:
        """Render ConsoleObject to terminal.

        Args:
            obj: ConsoleObject to render.
            target: Output stream. None for stdout.
            context: Rendering context.
        """
        ctx = self._get_context(context)
        rich_obj = self._dispatch(obj, ctx)

        if target is not None:
            # Create console for specific target
            console = RichConsole(file=target, width=ctx.width)
            console.print(rich_obj)
        else:
            self._console.print(rich_obj)

    def render_to_string(
        self,
        obj: Any,
        context: RenderContext | None = None,
    ) -> str:
        """Render ConsoleObject to ANSI string.

        Args:
            obj: ConsoleObject to render.
            context: Rendering context.

        Returns:
            String with ANSI escape codes.
        """
        from io import StringIO

        ctx = self._get_context(context)
        rich_obj = self._dispatch(obj, ctx)

        console = RichConsole(file=StringIO(), width=ctx.width, force_terminal=True)
        console.print(rich_obj)
        file = console.file
        if hasattr(file, "getvalue"):
            return str(file.getvalue())
        return ""

    def _render_text(self, obj: Text, context: RenderContext) -> RichText:
        """Render Text to Rich Text."""
        if obj.style:
            style = self._convert_style(obj.style)
            if style is not None:
                return RichText(obj.content, style=style)
        return RichText(obj.content)

    def _render_frame(self, obj: Frame, context: RenderContext) -> Panel:
        """Render Frame to Rich Panel."""
        # Render content
        content = self._dispatch(obj.content, context) if obj.content else ""

        # Get border style based on effect
        border_style = self._resolve_border_style(obj, context)

        # Get box type
        box = self._get_box(obj.border)

        # Build panel kwargs
        panel_kwargs: dict[str, Any] = {
            "title": obj.title,
            "subtitle": obj.subtitle,
            "box": box,
            "width": obj.width,
            "padding": (0, obj.padding),
        }

        # Only add border_style if set
        if border_style:
            panel_kwargs["border_style"] = border_style

        # Only add style if set
        if obj.style:
            panel_kwargs["style"] = self._convert_style(obj.style)

        return Panel(content, **panel_kwargs)

    def _render_banner(self, obj: Banner, context: RenderContext) -> RichText:
        """Render Banner to Rich Text with figlet."""
        import pyfiglet

        # Generate ASCII art
        figlet = pyfiglet.Figlet(font=obj.font, width=context.width)
        ascii_art = figlet.renderText(obj.text)

        # Apply effect if specified
        if obj.effect:
            return self._apply_gradient(ascii_art, obj.effect, context)

        if obj.style:
            style = self._convert_style(obj.style)
            if style is not None:
                return RichText(ascii_art, style=style)
        return RichText(ascii_art)

    def _render_table(self, obj: Table, context: RenderContext) -> RichTable:
        """Render Table to Rich Table."""
        box = self._get_box(obj.border)
        border_style = self._resolve_effect_style(obj.effect, context)

        table = RichTable(
            title=obj.title,
            box=box,
            border_style=border_style,
        )

        # Add columns
        for col in obj.columns:
            col_kwargs: dict[str, Any] = {
                "header": col.header,
                "width": col.width,
            }
            if col.align:
                col_kwargs["justify"] = col.align
            if col.style:
                style = self._convert_style(col.style)
                if style is not None:
                    col_kwargs["style"] = style
            table.add_column(**col_kwargs)

        # Add rows
        for row in obj.rows:
            table.add_row(*[str(cell) for cell in row])

        return table

    def _render_layout(self, obj: Layout, context: RenderContext) -> Any:
        """Render Layout by arranging children."""
        if not obj.children:
            return RichText("")

        rendered = [self._dispatch(child, context) for child in obj.children]

        if obj.direction == "vertical":
            return self._vertical_layout(rendered, obj.gap)
        elif obj.direction == "horizontal":
            return self._horizontal_layout(rendered, obj.gap, context)
        else:  # grid
            return self._grid_layout(rendered, obj.columns or 2, obj.gap, context)

    def _render_group(self, obj: Group, context: RenderContext) -> Any:
        """Render Group as vertical stack."""
        if not obj.children:
            return RichText("")
        rendered = [self._dispatch(child, context) for child in obj.children]
        return self._vertical_layout(rendered, gap=0)

    def _render_spacer(self, obj: Spacer, context: RenderContext) -> RichText:
        """Render Spacer as blank lines."""
        return RichText("\n" * obj.lines)

    def _render_rule(self, obj: Rule, context: RenderContext) -> RichRule:
        """Render Rule to Rich Rule."""
        kwargs: dict[str, Any] = {}
        if obj.title:
            kwargs["title"] = obj.title
        if obj.style:
            kwargs["style"] = self._convert_style(obj.style)
        return RichRule(**kwargs)

    # Helper methods

    def _convert_style(self, style: Style | None) -> RichStyle | None:
        """Convert model Style to Rich Style."""
        if style is None:
            return None

        return RichStyle(
            color=style.color,
            bgcolor=style.background,
            bold=style.bold,
            italic=style.italic,
            underline=style.underline,
            dim=style.dim,
            strike=style.strikethrough,
        )

    def _get_box(self, border: str) -> Any:
        """Get Rich box style from border name."""
        from rich import box

        box_map = {
            "solid": box.ROUNDED,
            "rounded": box.ROUNDED,
            "heavy": box.HEAVY,
            "double": box.DOUBLE,
            "simple": box.SIMPLE,
            "minimal": box.MINIMAL,
            "none": None,
        }
        return box_map.get(border, box.ROUNDED)

    def _resolve_border_style(self, obj: Frame, context: RenderContext) -> str | None:
        """Resolve border style from effect."""
        if obj.effect:
            return self._resolve_effect_style(obj.effect, context)
        return None

    def _resolve_effect_style(self, effect: str | None, context: RenderContext) -> str | None:
        """Get color from effect preset."""
        if not effect:
            return None

        # Map effect names to colors
        effect_colors = {
            "ocean": "cyan",
            "fire": "red",
            "forest": "green",
            "sunset": "yellow",
            "steel": "bright_black",
            "rainbow": "magenta",
            "neon": "bright_magenta",
            "aurora": "bright_cyan",
        }
        return effect_colors.get(effect, effect)

    def _apply_gradient(self, text: str, effect: str, context: RenderContext) -> RichText:
        """Apply gradient effect to text."""
        # For now, just apply the effect color
        color = self._resolve_effect_style(effect, context)
        if color:
            return RichText(text, style=color)
        return RichText(text)

    def _vertical_layout(self, items: list[Any], gap: int) -> Any:
        """Arrange items vertically with gap."""
        from rich.console import Group as RichGroup

        if gap == 0:
            return RichGroup(*items)

        # Insert spacers between items
        result = []
        for i, item in enumerate(items):
            result.append(item)
            if i < len(items) - 1:
                result.append(RichText("\n" * gap))
        return RichGroup(*result)

    def _horizontal_layout(self, items: list[Any], gap: int, context: RenderContext) -> Any:
        """Arrange items horizontally with gap."""
        from rich.columns import Columns

        return Columns(items, padding=(0, gap), expand=True)

    def _grid_layout(self, items: list[Any], columns: int, gap: int, context: RenderContext) -> Any:
        """Arrange items in a grid."""
        from rich.columns import Columns
        from rich.console import Group as RichGroup

        # Split into rows
        rows = []
        for i in range(0, len(items), columns):
            row_items = items[i : i + columns]
            rows.append(Columns(row_items, padding=(0, gap), expand=True))

        return RichGroup(*rows)


__all__ = ["TerminalRenderer"]
