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
    # Terminal utilities
    "TerminalProfile",
    "color_distance",
    "detect_terminal_capabilities",
    "get_color_names",
    "hex_to_rgb",
    "interpolate_color",
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
