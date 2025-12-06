"""Utility modules for text, color, and terminal handling."""

from styledconsole.utils.color import (
    CSS4_COLORS,
    color_distance,
    get_color_names,
    hex_to_rgb,
    interpolate_color,
    parse_color,
    rgb_to_hex,
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
    pad_to_width,
    split_graphemes,
    strip_ansi,
    truncate_to_width,
    visual_width,
)

__all__ = [
    "CSS4_COLORS",
    "EMOJI_PACKAGE_AVAILABLE",
    "EmojiInfo",
    # Terminal utilities
    "TerminalProfile",
    "analyze_emoji_safety",
    "color_distance",
    "demojize",
    "detect_terminal_capabilities",
    "emoji_list",
    "emojize",
    "filter_by_version",
    "get_all_emojis",
    "get_color_names",
    "get_emoji_info",
    "get_emoji_version",
    "hex_to_rgb",
    "interpolate_color",
    "is_valid_emoji",
    "is_zwj_sequence",
    "pad_to_width",
    # Color utilities
    "parse_color",
    "rgb_to_hex",
    "split_graphemes",
    "strip_ansi",
    "truncate_to_width",
    # Text utilities
    "visual_width",
]
