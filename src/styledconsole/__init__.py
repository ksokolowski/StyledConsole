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

# Import emoji constants (DRY: from emoji package)
from styledconsole.emoji_registry import EMOJI, CuratedEmojis, E

# Legacy import for backward compatibility (deprecated)
from styledconsole.emojis import EmojiConstants

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

# Import policy system (v0.9.0+)
from styledconsole.policy import (
    RenderPolicy,
    get_default_policy,
    reset_default_policy,
    set_default_policy,
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
from styledconsole.utils.emoji_support import (
    EMOJI_PACKAGE_AVAILABLE,
    EmojiInfo,
    analyze_emoji_safety,
    demojize,
    emoji_list,
    emojize,
    filter_by_version,
    get_all_emojis,
    get_emoji_info,
    get_emoji_version,
    is_valid_emoji,
    is_zwj_sequence,
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

__version__ = "0.9.0"
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
    "ASCII",
    "BORDERS",
    "CSS4_COLORS",
    "DEFAULT_THEME",
    "DOTS",
    "DOUBLE",
    # Emoji constants
    "EMOJI",
    "EMOJI_PACKAGE_AVAILABLE",
    "HEAVY",
    "MINIMAL",
    "RICH_TO_CSS4_MAPPING",
    "ROUNDED",
    "ROUNDED_THICK",
    "SAFE_EMOJIS",
    "SOLID",
    "THEMES",
    "THICK",
    # Type aliases
    "AlignType",
    # Banner rendering
    "Banner",
    # Border styles
    "BorderStyle",
    "ColorType",
    # Main Console API
    "Console",
    "CuratedEmojis",
    "E",
    "EmojiConstants",
    "EmojiInfo",
    "ExportError",
    "GradientSpec",
    "Icon",
    "IconMode",
    "IconProvider",
    "RGBColor",
    "RenderError",
    # Policy system (environment-aware rendering)
    "RenderPolicy",
    "Renderer",
    # Core types and exceptions
    "StyledConsoleError",
    # Progress tracking
    "StyledProgress",
    "TerminalError",
    # Terminal utilities
    "TerminalProfile",
    # Theme system
    "Theme",
    "__author__",
    "__license__",
    # Metadata
    "__version__",
    "analyze_emoji_safety",
    "auto_size_content",
    "color_distance",
    "convert_emoji_to_ascii",
    "demojize",
    "detect_terminal_capabilities",
    "diagonal_gradient_frame",
    "emoji_list",
    "emojize",
    "filter_by_version",
    "format_emoji_with_spacing",
    "get_all_color_names",
    "get_all_emojis",
    "get_border_style",
    "get_color_names",
    "get_default_policy",
    "get_emoji_info",
    "get_emoji_version",
    "get_icon_mode",
    "get_rich_color_names",
    "get_safe_emojis",
    # Special effects
    "gradient_frame",
    "hex_to_rgb",
    # Icon system (terminal-adaptive)
    "icons",
    "interpolate_color",
    "interpolate_rgb",
    "is_valid_emoji",
    "is_zwj_sequence",
    "list_border_styles",
    "normalize_color_for_rich",
    "pad_to_width",
    # Color utilities
    "parse_color",
    "prepare_frame_content",
    "rainbow_cycling_frame",
    "rainbow_frame",
    "reset_default_policy",
    "reset_icon_mode",
    "rgb_to_hex",
    "set_default_policy",
    "set_icon_mode",
    "split_graphemes",
    "strip_ansi",
    "truncate_lines",
    "truncate_to_width",
    "validate_emoji",
    # Text utilities
    "visual_width",
    "wrap_multiline",
    # Text wrapping utilities
    "wrap_text",
]
