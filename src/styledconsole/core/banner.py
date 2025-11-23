"""Banner rendering with ASCII art text using pyfiglet.

This module provides high-level banner rendering with:
- ASCII art text using pyfiglet fonts
- Gradient color support per line
- Optional frame borders around banners
- Emoji-aware fallback (renders plain text if emoji detected)
- Alignment and width control
"""

from dataclasses import dataclass
from functools import lru_cache
from io import StringIO

import pyfiglet
from rich.console import Console as RichConsole

from styledconsole.core.styles import BorderStyle, get_border_style
from styledconsole.types import AlignType
from styledconsole.utils.color import apply_line_gradient
from styledconsole.utils.text import strip_ansi, visual_width


@dataclass(frozen=True)
class Banner:
    """Configuration for ASCII art banner rendering.

    Attributes:
        text: Text to render as ASCII art (plain text only, emojis fallback to plain)
        font: Pyfiglet font name (default: "standard")
        start_color: Starting color for gradient (hex, rgb, or named color)
        end_color: Ending color for gradient (hex, rgb, or named color)
        border: Border style name or BorderStyle object (None for no border)
        width: Fixed width for banner (None for auto-width)
        align: Text alignment within banner ("left", "center", "right")
        padding: Padding spaces inside border (only used if border is set)
    """

    text: str
    font: str = "standard"
    start_color: str | None = None
    end_color: str | None = None
    border: str | BorderStyle | None = None
    width: int | None = None
    align: AlignType = "center"
    padding: int = 1


class BannerRenderer:
    """High-level renderer for ASCII art banners with gradients and borders.

    Features:
    - Renders text as ASCII art using pyfiglet fonts
    - Supports gradient coloring per line (top to bottom)
    - Optional frame borders around banners
    - Emoji-aware: Falls back to plain text if emoji detected
    - Alignment control (left, center, right)
    - Auto-width calculation or fixed width

    Example:
        >>> renderer = BannerRenderer()
        >>> lines = renderer.render("HELLO", font="slant")
        >>> for line in lines:
        ...     print(line)

        >>> # With gradient and border
        >>> lines = renderer.render(
        ...     "SUCCESS",
        ...     font="banner",
        ...     start_color="lime",
        ...     end_color="blue",
        ...     border="double",
        ... )
    """

    def __init__(self):
        """Initialize banner renderer with Rich rendering engine."""
        # Lazy import to avoid circular dependency
        from styledconsole.core.rendering_engine import RenderingEngine

        # Create buffer for capturing frame output
        self._buffer = StringIO()
        self._rich_console = RichConsole(
            file=self._buffer,
            record=False,
            force_terminal=True,
            force_jupyter=False,
            force_interactive=False,
            width=999,
            height=999,
        )
        self._rendering_engine = RenderingEngine(self._rich_console, debug=False)
        self._available_fonts = set(pyfiglet.FigletFont.getFonts())

    @staticmethod
    @lru_cache(maxsize=32)
    def _get_figlet(font: str) -> pyfiglet.Figlet:
        """Get cached Figlet instance for a font.

        Cached to avoid repeated font file loading.

        Args:
            font: Font name

        Returns:
            Figlet instance for the font
        """
        return pyfiglet.Figlet(font=font, width=1000)

    def render(
        self,
        text: str,
        font: str = "standard",
        start_color: str | None = None,
        end_color: str | None = None,
        border: str | BorderStyle | None = None,
        width: int | None = None,
        align: AlignType = "center",
        padding: int = 1,
    ) -> list[str]:
        """Render text as ASCII art banner with optional gradient and border.

        Args:
            text: Text to render (plain text only, emoji triggers fallback)
            font: Pyfiglet font name (default: "standard")
            start_color: Starting color for gradient (hex, rgb, or named)
            end_color: Ending color for gradient (hex, rgb, or named)
            border: Border style name or BorderStyle object (None for no border)
            width: Fixed width for banner (None for auto-width)
            align: Text alignment ("left", "center", "right")
            padding: Padding spaces inside border (only if border is set)

        Returns:
            List of rendered lines ready for printing

        Example:
            >>> renderer = BannerRenderer()
            >>> lines = renderer.render("HELLO", font="slant")
            >>> for line in lines:
            ...     print(line)
        """
        banner = Banner(
            text=text,
            font=font,
            start_color=start_color,
            end_color=end_color,
            border=border,
            width=width,
            align=align,
            padding=padding,
        )
        return self.render_banner(banner)

    def render_banner(self, banner: Banner) -> list[str]:
        """Render a Banner configuration object.

        Args:
            banner: Banner configuration object

        Returns:
            List of rendered lines ready for printing
        """
        # Check if text contains emoji (visual_width > len indicates emoji)
        text_clean = strip_ansi(banner.text)
        has_emoji = visual_width(text_clean) > len(text_clean)

        if has_emoji:
            # Fallback to plain text for emoji
            ascii_lines = [banner.text]
        else:
            # Validate font
            if banner.font not in self._available_fonts:
                available = sorted(self._available_fonts)[:10]
                raise ValueError(
                    f"Font '{banner.font}' not found. "
                    f"Available fonts include: {', '.join(available)}... "
                    f"Use pyfiglet.FigletFont.getFonts() for full list."
                )

            # Generate ASCII art using cached Figlet instance
            figlet = self._get_figlet(banner.font)
            ascii_art = figlet.renderText(banner.text)

            # Split into lines and remove trailing empty lines
            ascii_lines = ascii_art.rstrip("\n").split("\n")

        # Apply gradient coloring if specified
        if banner.start_color and banner.end_color:
            ascii_lines = apply_line_gradient(ascii_lines, banner.start_color, banner.end_color)

        # If no border, return ASCII art lines directly
        if banner.border is None:
            return ascii_lines

        # Wrap in frame border using RenderingEngine
        border_style = (
            get_border_style(banner.border) if isinstance(banner.border, str) else banner.border
        )

        # Reset buffer
        self._buffer.seek(0)
        self._buffer.truncate(0)

        # If width is specified, we need to recreate console with proper width
        # Otherwise Rich Panel won't expand to the requested width
        if banner.width:
            # Create temporary console with desired width
            temp_console = RichConsole(
                file=self._buffer,
                record=False,
                force_terminal=True,
                force_jupyter=False,
                force_interactive=False,
                width=banner.width,
                height=999,
            )
            # Import lazily
            from styledconsole.core.rendering_engine import RenderingEngine

            temp_engine = RenderingEngine(temp_console, debug=False)

            # Use temporary engine
            temp_engine.print_frame(
                content=ascii_lines,
                border=border_style.name if hasattr(border_style, "name") else str(border_style),
                width=banner.width,
                align=banner.align,
                padding=banner.padding,
            )
        else:
            # Use default engine
            self._rendering_engine.print_frame(
                content=ascii_lines,
                border=border_style.name if hasattr(border_style, "name") else str(border_style),
                width=banner.width,
                align=banner.align,
                padding=banner.padding,
            )

        # Get output and return as list of lines
        output = self._buffer.getvalue()
        return output.splitlines()

    def list_fonts(self, limit: int | None = None) -> list[str]:
        """Get list of available pyfiglet fonts.

        Args:
            limit: Maximum number of fonts to return (None for all)

        Returns:
            Sorted list of available font names
        """
        fonts = sorted(self._available_fonts)
        return fonts[:limit] if limit else fonts

    def preview_font(self, font: str, text: str = "Preview") -> str:
        """Preview a font with sample text.

        Args:
            font: Font name to preview
            text: Text to render (default: "Preview")

        Returns:
            Rendered ASCII art as single string

        Raises:
            ValueError: If font is not available
        """
        if font not in self._available_fonts:
            raise ValueError(f"Font '{font}' not found")

        figlet = pyfiglet.Figlet(font=font)
        return figlet.renderText(text)


__all__ = [
    "Banner",
    "BannerRenderer",
    "AlignType",
]
