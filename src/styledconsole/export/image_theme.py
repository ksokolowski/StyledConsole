"""Theme and style configuration for image export.

This module provides dataclasses for configuring the visual appearance
of exported images, including colors, fonts, and text styling.

Design Decisions:
    - Default colors use Catppuccin Mocha palette for modern dark theme
    - Font size 16px chosen for optimal readability at 1x and 2x scale
    - Line height 1.4 provides comfortable reading with emoji support
    - Padding 20px gives clean margins around terminal content
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import ImageFont as PILImageFont

from .config import (
    DEFAULT_FONT_SIZE_PX,
    DEFAULT_LINE_HEIGHT,
    DEFAULT_PADDING_PX,
    THEME_MOCHA_BACKGROUND,
    THEME_MOCHA_FOREGROUND,
)

__all__ = [
    "DEFAULT_FONT_SIZE_PX",
    "DEFAULT_LINE_HEIGHT",
    "DEFAULT_PADDING_PX",
    "DEFAULT_THEME",
    "THEME_MOCHA_BACKGROUND",
    "THEME_MOCHA_FOREGROUND",
    "FontFamily",
    "ImageTheme",
    "TextStyle",
]


# =============================================================================
# Theme and Style Dataclasses
# =============================================================================


@dataclass
class ImageTheme:
    """Color theme for image export.

    Controls the visual appearance of exported terminal images
    including background, foreground colors, font size, and spacing.

    Attributes:
        background: Background color (hex string).
        foreground: Default text color (hex string).
        font_size: Base font size in pixels.
        padding: Padding around content in pixels.
        line_height: Line height multiplier (1.0 = single spacing).
        terminal_size: Fixed (cols, rows) size, or None for auto-sizing.

    Example:
        >>> # Create theme with Catppuccin Mocha defaults
        >>> theme = ImageTheme()
        >>>
        >>> # Create custom theme with larger font
        >>> theme = ImageTheme(font_size=20, padding=30)
        >>>
        >>> # Fixed terminal size (80x24 standard)
        >>> theme = ImageTheme(terminal_size=(80, 24))
    """

    background: str = THEME_MOCHA_BACKGROUND
    foreground: str = THEME_MOCHA_FOREGROUND
    font_size: int = DEFAULT_FONT_SIZE_PX
    padding: int = DEFAULT_PADDING_PX
    line_height: float = DEFAULT_LINE_HEIGHT
    terminal_size: tuple[int, int] | None = None

    # Debugging: overlay a grid showing terminal cell boundaries.
    # Useful when diagnosing alignment issues in exported images.
    debug_grid: bool = False
    debug_grid_every: int = 1


@dataclass
class FontFamily:
    """Collection of font variants for styled text rendering.

    Manages Regular, Bold, Italic, and Bold+Italic font variants
    for proper text styling in image export.

    Attributes:
        regular: Regular weight font (required).
        bold: Bold variant (optional, falls back to regular).
        italic: Italic variant (optional, falls back to regular).
        bold_italic: Bold+Italic variant (optional, falls back to regular).

    Example:
        >>> from PIL import ImageFont
        >>> family = FontFamily(
        ...     regular=ImageFont.truetype("DejaVuSansMono.ttf", 16),
        ...     bold=ImageFont.truetype("DejaVuSansMono-Bold.ttf", 16),
        ... )
        >>> font = family.get_font(bold=True)  # Returns bold variant
    """

    regular: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None
    bold: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
    italic: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
    bold_italic: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None

    def get_font(
        self, bold: bool = False, italic: bool = False
    ) -> PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None:
        """Get appropriate font variant for requested style.

        Tries to match the requested style exactly, falling back to
        regular font if the requested variant is not available.

        Args:
            bold: Whether bold style is requested.
            italic: Whether italic style is requested.

        Returns:
            The most appropriate font variant available.
        """
        if bold and italic and self.bold_italic:
            return self.bold_italic
        if bold and self.bold:
            return self.bold
        if italic and self.italic:
            return self.italic
        return self.regular


@dataclass
class TextStyle:
    """Text style properties extracted from Rich markup.

    Captures text styling attributes for rendering text decorations
    and effects in image export.

    Attributes:
        bold: Bold text weight.
        italic: Italic text style.
        underline: Underline decoration.
        strike: Strikethrough decoration.
        overline: Overline decoration.
        dim: Reduced brightness effect (50% opacity).

    Example:
        >>> style = TextStyle(bold=True, underline=True)
        >>> style.bold
        True
    """

    bold: bool = False
    italic: bool = False
    underline: bool = False
    strike: bool = False
    overline: bool = False
    dim: bool = False

    @classmethod
    def from_rich_style(cls, style) -> TextStyle:
        """Create TextStyle from Rich Style object.

        Args:
            style: Rich Style object or None.

        Returns:
            TextStyle with properties extracted from Rich style.
        """
        if style is None:
            return cls()
        return cls(
            bold=bool(style.bold),
            italic=bool(style.italic),
            underline=bool(style.underline),
            strike=bool(style.strike),
            overline=bool(getattr(style, "overline", False)),
            dim=bool(style.dim),
        )


# =============================================================================
# Default Theme Instance
# =============================================================================

DEFAULT_THEME = ImageTheme()
"""Pre-configured theme using Catppuccin Mocha dark palette.

This theme provides a modern, readable dark theme suitable for
terminal screenshots and documentation images.
"""
