"""
StyledConsole - A modern Python library for elegant terminal output.

Provides rich formatting, colors, emoji support, and export capabilities
for creating beautiful command-line interfaces.

Example:
    >>> from styledconsole import Console
    >>> console = Console()
    >>> console.frame("Hello, World!", title="Greeting", border="solid")
    >>> console.text("Status: OK", color="green", bold=True)
"""

from styledconsole.console import Console
from styledconsole.core.banner import Banner
from styledconsole.core.progress import StyledProgress
from styledconsole.core.styles import (
    ASCII,
    BORDERS,
    DOTS,
    DOUBLE,
    HEAVY,
    MINIMAL,
    ROUNDED,
    ROUNDED_THICK,
    SOLID,
    THICK,
    BorderStyle,
    get_border_style,
    list_border_styles,
)
from styledconsole.core.theme import DEFAULT_THEME, THEMES, GradientSpec, Theme

# Import effects
from styledconsole.effects import (
    diagonal_gradient_frame,
    gradient_frame,
    rainbow_cycling_frame,
    rainbow_frame,
)

# Import emoji constants
from styledconsole.emojis import EMOJI, E, EmojiConstants

# Import icon system (v0.9.0+)
from styledconsole.icons import (
    Icon,
    IconMode,
    IconProvider,
    convert_emoji_to_ascii,
    get_icon_mode,
    icons,
    reset_icon_mode,
    set_icon_mode,
)

# Import type aliases
from styledconsole.types import AlignType, ColorType, Renderer
from styledconsole.utils.color import (
    CSS4_COLORS,
    RGBColor,
    color_distance,
    hex_to_rgb,
    interpolate_color,
    interpolate_rgb,
    normalize_color_for_rich,
    parse_color,
    rgb_to_hex,
)
from styledconsole.utils.color_data import (
    RICH_TO_CSS4_MAPPING,
    get_all_color_names,
    get_color_names,
    get_rich_color_names,
)
from styledconsole.utils.terminal import (
    TerminalProfile,
    detect_terminal_capabilities,
)
from styledconsole.utils.text import (
    SAFE_EMOJIS,
    format_emoji_with_spacing,
    get_safe_emojis,
    pad_to_width,
    split_graphemes,
    strip_ansi,
    truncate_to_width,
    validate_emoji,
    visual_width,
)
from styledconsole.utils.wrap import (
    auto_size_content,
    prepare_frame_content,
    truncate_lines,
    wrap_multiline,
    wrap_text,
)

__version__ = "0.8.0"
__author__ = "Krzysztof Sokołowski"
__license__ = "Apache-2.0"


# Custom exceptions
class StyledConsoleError(Exception):
    """Base exception for all StyledConsole errors."""

    pass


class RenderError(StyledConsoleError):
    """Raised when rendering fails."""

    pass


class ExportError(StyledConsoleError):
    """Raised when export operation fails."""

    pass


class TerminalError(StyledConsoleError):
    """Raised when terminal detection or interaction fails."""

    pass


# Public API
__all__ = [
    # Main Console API
    "Console",
    # Banner rendering
    "Banner",
    # Theme system
    "Theme",
    "THEMES",
    "DEFAULT_THEME",
    "GradientSpec",
    # Progress tracking
    "StyledProgress",
    # Emoji constants
    "EMOJI",
    "E",
    "EmojiConstants",
    # Icon system (terminal-adaptive)
    "icons",
    "Icon",
    "IconProvider",
    "IconMode",
    "set_icon_mode",
    "get_icon_mode",
    "reset_icon_mode",
    "convert_emoji_to_ascii",
    # Special effects
    "gradient_frame",
    "diagonal_gradient_frame",
    "rainbow_frame",
    "rainbow_cycling_frame",
    # Text utilities
    "visual_width",
    "strip_ansi",
    "split_graphemes",
    "pad_to_width",
    "truncate_to_width",
    "SAFE_EMOJIS",
    "get_safe_emojis",
    "validate_emoji",
    "format_emoji_with_spacing",
    # Text wrapping utilities
    "wrap_text",
    "wrap_multiline",
    "truncate_lines",
    "prepare_frame_content",
    "auto_size_content",
    # Type aliases
    "AlignType",
    "ColorType",
    "Renderer",
    # Color utilities
    "parse_color",
    "hex_to_rgb",
    "rgb_to_hex",
    "interpolate_color",
    "interpolate_rgb",
    "color_distance",
    "normalize_color_for_rich",
    "get_color_names",
    "get_rich_color_names",
    "get_all_color_names",
    "CSS4_COLORS",
    "RICH_TO_CSS4_MAPPING",
    "RGBColor",
    # Terminal utilities
    "TerminalProfile",
    "detect_terminal_capabilities",
    # Border styles
    "BorderStyle",
    "SOLID",
    "DOUBLE",
    "ROUNDED",
    "HEAVY",
    "THICK",
    "ROUNDED_THICK",
    "ASCII",
    "MINIMAL",
    "DOTS",
    "BORDERS",
    "get_border_style",
    "list_border_styles",
    # Core types and exceptions
    "StyledConsoleError",
    "RenderError",
    "ExportError",
    "TerminalError",
    # Metadata
    "__version__",
    "__author__",
    "__license__",
]
