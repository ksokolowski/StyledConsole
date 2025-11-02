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
from styledconsole.core.banner import Banner, BannerRenderer
from styledconsole.core.frame import Frame, FrameRenderer
from styledconsole.core.layout import Layout, LayoutComposer
from styledconsole.core.styles import (
    ASCII,
    BORDERS,
    DOTS,
    DOUBLE,
    HEAVY,
    MINIMAL,
    ROUNDED,
    SOLID,
    THICK,
    BorderStyle,
    get_border_style,
    list_border_styles,
)

# Import effects
from styledconsole.effects import (
    diagonal_gradient_frame,
    gradient_frame,
    rainbow_cycling_frame,
    rainbow_frame,
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

__version__ = "0.1.0"
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
    "BannerRenderer",
    # Frame rendering
    "Frame",
    "FrameRenderer",
    # Layout composition
    "Layout",
    "LayoutComposer",
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
