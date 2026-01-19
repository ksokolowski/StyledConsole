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

# v0.10.0 API - Builder Layer
from styledconsole.builders import (
    BannerBuilder,
    FrameBuilder,
    LayoutBuilder,
    TableBuilder,
)
from styledconsole.columns import StyledColumns
from styledconsole.console import Console
from styledconsole.core.banner import Banner
from styledconsole.core.context import StyleContext
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
from styledconsole.data.palettes import (
    PALETTES,
    get_palette,
    get_palette_categories,
    list_palettes,
)

# v0.10.0 API - Declarative Layer
from styledconsole.declarative import (
    BUILTIN_TEMPLATES,
    Declarative,
    Template,
    TemplateRegistry,
    add_jinja_filter,
    from_template,
    load_dict,
    load_file,
    load_jinja_file,
    load_json,
    load_yaml,
    normalize,
    render_jinja,
    render_jinja_string,
)
from styledconsole.declarative import (
    create as create_object,
)

# Import effects
from styledconsole.effects import (
    diagonal_gradient_frame,
    gradient_frame,
    rainbow_cycling_frame,
    rainbow_frame,
)

# Effect system (v0.9.9.3+)
from styledconsole.effects.registry import EFFECTS
from styledconsole.effects.spec import (
    PHASE_FULL_CYCLE,
    PHASE_INCREMENT_DEFAULT,
    EffectSpec,
    cycle_phase,
)

# Import emoji data layer (4000+ emojis from emoji package)
# NOTE: For terminal output, prefer `icons` module which provides ASCII fallback
from styledconsole.emoji_registry import EMOJI, CuratedEmojis, E

# Import enums for IDE autocomplete (v0.10.2+)
from styledconsole.enums import (
    Align,
    Border,
    Direction,
    Effect,
    ExportFormat,
    LayoutMode,
    Target,
)

# Note: EmojiConstants is deprecated and available via __getattr__ below
# Icon system - PRIMARY FACADE for terminal symbol output (v0.9.5+)
# Provides 204 icons with automatic ASCII fallback for non-emoji terminals
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

# v0.10.0 API - Model Layer
from styledconsole.model import (
    Banner as BannerModel,
)
from styledconsole.model import (
    Column,
    ConsoleObject,
    Group,
    Layout,
    Spacer,
    Style,
    Text,
)
from styledconsole.model import (
    Frame as FrameModel,
)
from styledconsole.model import (
    Rule as RuleModel,
)
from styledconsole.model import (
    Table as TableModel,
)

# Import policy system (v0.9.0+)
from styledconsole.policy import (
    RenderPolicy,
    get_default_policy,
    reset_default_policy,
    set_default_policy,
)
from styledconsole.presets.styles import (
    ERROR_STYLE,
    INFO_STYLE,
    MINIMAL_STYLE,
    PANEL_STYLE,
    SUCCESS_STYLE,
    WARNING_STYLE,
)

# v0.10.0 API - Renderer Layer
from styledconsole.rendering import (
    HTMLRenderer,
    RenderContext,
    TerminalRenderer,
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
from styledconsole.utils.palette import (
    create_palette_effect,
    palette_from_dict,
)
from styledconsole.utils.terminal import (
    TerminalProfile,
    detect_terminal_capabilities,
)
from styledconsole.utils.text import (
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

__version__ = "0.10.2"
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


# Public API (sorted alphabetically per RUF022)
__all__ = [
    "ASCII",
    "BORDERS",
    "BUILTIN_TEMPLATES",
    "CSS4_COLORS",
    "DEFAULT_THEME",
    "DOTS",
    "DOUBLE",
    "EFFECTS",
    "EMOJI",
    "EMOJI_PACKAGE_AVAILABLE",
    "ERROR_STYLE",
    "HEAVY",
    "INFO_STYLE",
    "MINIMAL",
    "MINIMAL_STYLE",
    "PALETTES",
    "PANEL_STYLE",
    "PHASE_FULL_CYCLE",
    "PHASE_INCREMENT_DEFAULT",
    "RICH_TO_CSS4_MAPPING",
    "ROUNDED",
    "ROUNDED_THICK",
    "SOLID",
    "SUCCESS_STYLE",
    "THEMES",
    "THICK",
    "WARNING_STYLE",
    "Align",
    "AlignType",
    "Banner",
    "BannerBuilder",
    "BannerModel",
    "Border",
    "BorderStyle",
    "ColorType",
    "Column",
    "Console",
    "ConsoleObject",
    "CuratedEmojis",
    "Declarative",
    "Direction",
    "E",
    "Effect",
    "EffectSpec",
    "EmojiConstants",
    "EmojiInfo",
    "ExportError",
    "ExportFormat",
    "FrameBuilder",
    "FrameModel",
    "GradientSpec",
    "Group",
    "HTMLRenderer",
    "Icon",
    "IconMode",
    "IconProvider",
    "Layout",
    "LayoutBuilder",
    "LayoutMode",
    "RGBColor",
    "RenderContext",
    "RenderError",
    "RenderPolicy",
    "Renderer",
    "RuleModel",
    "Spacer",
    "Style",
    "StyleContext",
    "StyledColumns",
    "StyledConsoleError",
    "StyledProgress",
    "TableBuilder",
    "TableModel",
    "Target",
    "Template",
    "TemplateRegistry",
    "TerminalError",
    "TerminalProfile",
    "TerminalRenderer",
    "Text",
    "Theme",
    "__author__",
    "__license__",
    "__version__",
    "add_jinja_filter",
    "analyze_emoji_safety",
    "auto_size_content",
    "color_distance",
    "convert_emoji_to_ascii",
    "create_object",
    "create_palette_effect",
    "cycle_phase",
    "demojize",
    "detect_terminal_capabilities",
    "diagonal_gradient_frame",
    "emoji_list",
    "emojize",
    "filter_by_version",
    "format_emoji_with_spacing",
    "from_template",
    "get_all_color_names",
    "get_all_emojis",
    "get_border_style",
    "get_color_names",
    "get_default_policy",
    "get_emoji_info",
    "get_emoji_version",
    "get_icon_mode",
    "get_palette",
    "get_palette_categories",
    "get_rich_color_names",
    "get_safe_emojis",
    "gradient_frame",
    "hex_to_rgb",
    "icons",
    "interpolate_color",
    "interpolate_rgb",
    "is_valid_emoji",
    "is_zwj_sequence",
    "list_border_styles",
    "list_palettes",
    "load_dict",
    "load_file",
    "load_jinja_file",
    "load_json",
    "load_yaml",
    "normalize",
    "normalize_color_for_rich",
    "pad_to_width",
    "palette_from_dict",
    "parse_color",
    "prepare_frame_content",
    "rainbow_cycling_frame",
    "rainbow_frame",
    "render_jinja",
    "render_jinja_string",
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
    "visual_width",
    "wrap_multiline",
    "wrap_text",
]


def __getattr__(name: str):
    """Module-level __getattr__ for lazy/deprecated imports."""
    if name == "EmojiConstants":
        import warnings

        warnings.warn(
            "EmojiConstants is deprecated. Use 'EMOJI' directly or "
            "'type(EMOJI)' for type hints. Will be removed in v1.0.0.",
            DeprecationWarning,
            stacklevel=2,
        )
        return type(EMOJI)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
