"""Color parsing, conversion, and gradient utilities.

Supports multiple color formats:
- Hex: #FF0000, #f00 (shorthand)
- RGB: rgb(255, 0, 0), (255, 0, 0)
- Named: CSS4 color names (148 colors)
"""

import re
from functools import lru_cache

from styledconsole.utils.color_data import CSS4_COLORS, get_color_names

# Regex patterns for color parsing
HEX_PATTERN = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
RGB_PATTERN = re.compile(r"^rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$")
TUPLE_PATTERN = re.compile(r"^\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)$")

# Type alias for RGB color
RGBColor = tuple[int, int, int]


def hex_to_rgb(hex_str: str) -> RGBColor:
    """Convert hex color string to RGB tuple.

    Args:
        hex_str: Hex color string (#FF0000 or #f00)

    Returns:
        RGB tuple (r, g, b) with values 0-255

    Raises:
        ValueError: If hex string is invalid

    Example:
        >>> hex_to_rgb("#FF0000")
        (255, 0, 0)
        >>> hex_to_rgb("#f00")
        (255, 0, 0)
        >>> hex_to_rgb("FF0000")
        (255, 0, 0)
    """
    # Remove # if present
    hex_str = hex_str.lstrip("#")

    # Validate format
    if not HEX_PATTERN.match("#" + hex_str):
        raise ValueError(f"Invalid hex color: #{hex_str}")

    # Expand shorthand (e.g., "f00" -> "ff0000")
    if len(hex_str) == 3:
        hex_str = "".join([c * 2 for c in hex_str])

    # Convert to RGB
    r = int(hex_str[0:2], 16)
    g = int(hex_str[2:4], 16)
    b = int(hex_str[4:6], 16)

    return (r, g, b)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB values to hex color string.

    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)

    Returns:
        Hex color string with # prefix (e.g., "#FF0000")

    Raises:
        ValueError: If any value is outside 0-255 range

    Example:
        >>> rgb_to_hex(255, 0, 0)
        '#FF0000'
        >>> rgb_to_hex(30, 144, 255)
        '#1E90FF'
    """
    # Validate ranges
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"RGB values must be 0-255, got ({r}, {g}, {b})")

    return f"#{r:02X}{g:02X}{b:02X}"


@lru_cache(maxsize=512)
def parse_color(value: str) -> RGBColor:
    """Parse color string in any supported format to RGB tuple.

    Cached with LRU cache (512 entries) for performance in loops.

    Supported formats:
    - Hex: "#FF0000", "#f00", "FF0000"
    - RGB: "rgb(255, 0, 0)"
    - Tuple: "(255, 0, 0)"
    - Named: CSS4 color names (case-insensitive)

    Args:
        value: Color string in any supported format

    Returns:
        RGB tuple (r, g, b) with values 0-255

    Raises:
        ValueError: If color format is not recognized

    Example:
        >>> parse_color("#FF0000")
        (255, 0, 0)
        >>> parse_color("rgb(0, 255, 0)")
        (0, 255, 0)
        >>> parse_color("red")
        (255, 0, 0)
        >>> parse_color("dodgerblue")
        (30, 144, 255)
    """
    value = value.strip()

    # Try CSS4 named color first (case-insensitive)
    value_lower = value.lower()
    if value_lower in CSS4_COLORS:
        return hex_to_rgb(CSS4_COLORS[value_lower])

    # Try hex format
    if HEX_PATTERN.match(value):
        return hex_to_rgb(value)

    # Try rgb(r, g, b) format
    rgb_match = RGB_PATTERN.match(value)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError(f"RGB values must be 0-255, got ({r}, {g}, {b})")
        return (r, g, b)

    # Try tuple format (r, g, b)
    tuple_match = TUPLE_PATTERN.match(value)
    if tuple_match:
        r, g, b = map(int, tuple_match.groups())
        if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
            raise ValueError(f"RGB values must be 0-255, got ({r}, {g}, {b})")
        return (r, g, b)

    # No match found
    raise ValueError(f"Invalid color format: '{value}'")


def interpolate_rgb(
    start_rgb: RGBColor,
    end_rgb: RGBColor,
    t: float,
) -> RGBColor:
    """Interpolate between two RGB colors (optimized for loops).

    Use this when you've already parsed colors to RGB tuples to avoid
    repeated hex conversions in tight loops.

    Args:
        start_rgb: Start color as RGB tuple
        end_rgb: End color as RGB tuple
        t: Interpolation factor (0.0 = start, 1.0 = end)

    Returns:
        Interpolated RGB tuple

    Example:
        >>> interpolate_rgb((255, 0, 0), (0, 0, 255), 0.5)
        (128, 0, 128)
    """
    # Clamp t to [0, 1]
    t = max(0.0, min(1.0, t))

    # Linear interpolation for each channel
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)

    return (r, g, b)


def interpolate_color(
    start: str | RGBColor,
    end: str | RGBColor,
    t: float,
) -> str:
    """Interpolate between two colors for gradient effects.

    Args:
        start: Start color (hex, RGB, named, or RGB tuple)
        end: End color (hex, RGB, named, or RGB tuple)
        t: Interpolation factor (0.0 = start, 1.0 = end)

    Returns:
        Hex color string for interpolated color

    Example:
        >>> interpolate_color("#000000", "#FFFFFF", 0.5)
        '#808080'
        >>> interpolate_color("red", "blue", 0.5)
        '#800080'
        >>> interpolate_color((255, 0, 0), (0, 0, 255), 0.5)
        '#800080'
    """
    # Parse colors to RGB
    if isinstance(start, tuple):
        start_rgb = start
    else:
        start_rgb = parse_color(start)

    if isinstance(end, tuple):
        end_rgb = end
    else:
        end_rgb = parse_color(end)

    # Use optimized RGB interpolation
    result_rgb = interpolate_rgb(start_rgb, end_rgb, t)
    return rgb_to_hex(*result_rgb)


def color_distance(color1: str | RGBColor, color2: str | RGBColor) -> float:
    """Calculate Euclidean distance between two colors in RGB space.

    Useful for finding similar colors or color matching.

    Args:
        color1: First color
        color2: Second color

    Returns:
        Distance value (0 = identical, ~442 = max distance black<->white)

    Example:
        >>> color_distance("red", "red")
        0.0
        >>> color_distance("#000000", "#FFFFFF")
        441.67...
        >>> color_distance("red", "darkred") < color_distance("red", "blue")
        True
    """
    # Parse colors
    if isinstance(color1, tuple):
        rgb1 = color1
    else:
        rgb1 = parse_color(color1)

    if isinstance(color2, tuple):
        rgb2 = color2
    else:
        rgb2 = parse_color(color2)

    # Euclidean distance in RGB space
    return ((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2) ** 0.5


__all__ = [
    "hex_to_rgb",
    "rgb_to_hex",
    "parse_color",
    "interpolate_color",
    "interpolate_rgb",
    "color_distance",
    "get_color_names",
    "CSS4_COLORS",
    "RGBColor",
]
