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
from styledconsole.utils.text import (
    pad_to_width,
    split_graphemes,
    strip_ansi,
    truncate_to_width,
    visual_width,
)

__all__ = [
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
]
