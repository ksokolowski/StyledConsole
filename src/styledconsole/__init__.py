"""
StyledConsole - A modern Python library for elegant terminal output.

Provides rich formatting, colors, emoji support, and export capabilities
for creating beautiful command-line interfaces.

Example:
    >>> from styledconsole import Console
    >>> console = Console()
    >>> console.print("Hello, World!", color="blue", bold=True)
"""

from styledconsole.core.banner import Banner, BannerRenderer
from styledconsole.core.frame import Frame, FrameRenderer
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
from styledconsole.utils.color import (
    CSS4_COLORS,
    color_distance,
    get_color_names,
    hex_to_rgb,
    interpolate_color,
    parse_color,
    rgb_to_hex,
)
from styledconsole.utils.terminal import (
    TerminalProfile,
    detect_terminal_capabilities,
)
from styledconsole.utils.text import (
    pad_to_width,
    split_graphemes,
    strip_ansi,
    truncate_to_width,
    visual_width,
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


# Public API will be added as components are implemented
__all__ = [
    # Banner rendering
    "Banner",
    "BannerRenderer",
    # Frame rendering
    "Frame",
    "FrameRenderer",
    # Text utilities
    "visual_width",
    "strip_ansi",
    "split_graphemes",
    "pad_to_width",
    "truncate_to_width",
    # Color utilities
    "parse_color",
    "hex_to_rgb",
    "rgb_to_hex",
    "interpolate_color",
    "color_distance",
    "get_color_names",
    "CSS4_COLORS",
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
