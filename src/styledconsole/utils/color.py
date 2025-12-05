"""Color parsing, conversion, and gradient utilities.

Supports multiple color formats:
- Hex: #FF0000, #f00 (shorthand)
- RGB: rgb(255, 0, 0), (255, 0, 0)
- Named: CSS4 color names (148 colors) + Rich color names (250+ colors)

The combined color system allows using human-readable names from both
CSS4 standard and Rich's extended palette throughout the library.

Policy-aware colorization:
- All colorization functions accept an optional `policy` parameter
- When `policy.color=False`, functions return plain text without ANSI codes
- This enables graceful degradation for NO_COLOR, CI environments, etc.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import TYPE_CHECKING

from styledconsole.utils.color_data import (
    CSS4_COLORS,
    RICH_TO_CSS4_MAPPING,
    get_color_names,
)

if TYPE_CHECKING:
    from styledconsole.policy import RenderPolicy

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


def _try_named_color(value_lower: str) -> RGBColor | None:
    """Try to parse as CSS4 or Rich named color."""
    if value_lower in CSS4_COLORS:
        return hex_to_rgb(CSS4_COLORS[value_lower])
    if value_lower in RICH_TO_CSS4_MAPPING:
        return hex_to_rgb(RICH_TO_CSS4_MAPPING[value_lower])
    return None


def _validate_rgb_range(r: int, g: int, b: int) -> None:
    """Validate RGB values are in 0-255 range."""
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError(f"RGB values must be 0-255, got ({r}, {g}, {b})")


def _try_rgb_pattern(value: str) -> RGBColor | None:
    """Try to parse as rgb(r, g, b) or (r, g, b) format."""
    rgb_match = RGB_PATTERN.match(value)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        _validate_rgb_range(r, g, b)
        return (r, g, b)

    tuple_match = TUPLE_PATTERN.match(value)
    if tuple_match:
        r, g, b = map(int, tuple_match.groups())
        _validate_rgb_range(r, g, b)
        return (r, g, b)

    return None


@lru_cache(maxsize=512)
def parse_color(value: str) -> RGBColor:
    """Parse color string in any supported format to RGB tuple.

    Cached with LRU cache (512 entries) for performance in loops.
    Input is normalized (lowercase, stripped) before caching for better hit ratio.

    Supported formats:
    - Hex: "#FF0000", "#f00", "FF0000"
    - RGB: "rgb(255, 0, 0)"
    - Tuple: "(255, 0, 0)"
    - Named CSS4: 148 colors (case-insensitive) - "red", "dodgerblue", "lime"
    - Named Rich: 250+ colors (case-insensitive) - "bright_green", "dodger_blue1"

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
        >>> parse_color("red")  # CSS4
        (255, 0, 0)
        >>> parse_color("lime")  # CSS4
        (0, 255, 0)
        >>> parse_color("bright_green")  # Rich
        (0, 255, 0)
        >>> parse_color("dodger_blue1")  # Rich numbered variant
        (30, 144, 255)
    """
    # Normalize for caching: strip whitespace and lowercase
    # This ensures "RED", "red", " red " all hit the same cache entry
    value_normalized = value.strip().lower()

    # Try named colors first (most common)
    named_result = _try_named_color(value_normalized)
    if named_result:
        return named_result

    # Try hex format (use original stripped value to preserve case for regex)
    value_stripped = value.strip()
    if HEX_PATTERN.match(value_stripped):
        return hex_to_rgb(value_stripped)

    # Try rgb/tuple formats
    pattern_result = _try_rgb_pattern(value_stripped)
    if pattern_result:
        return pattern_result

    # No match found
    raise ValueError(
        f"Invalid color format: '{value}'. "
        f"Supported: hex (#FF0000), rgb(r,g,b), CSS4 names (148), Rich names (250+)"
    )


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
    start_rgb = start if isinstance(start, tuple) else parse_color(start)

    end_rgb = end if isinstance(end, tuple) else parse_color(end)

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
    rgb1 = color1 if isinstance(color1, tuple) else parse_color(color1)

    rgb2 = color2 if isinstance(color2, tuple) else parse_color(color2)

    # Euclidean distance in RGB space
    return ((rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2) ** 0.5


@lru_cache(maxsize=256)
def normalize_color_for_rich(color: str | None) -> str | None:
    """Convert CSS4/Rich color name to hex for Rich compatibility.

    Rich's Panel and Text renderables prefer hex colors over named colors
    for consistent rendering across terminals. This function normalizes
    all color inputs to hex format.

    Args:
        color: Color in any supported format (CSS4 name, Rich name, hex, RGB tuple string)

    Returns:
        Hex color string (#RRGGBB) or None if color is None.
        Returns original string if parsing fails (let Rich handle it).

    Raises:
        No exceptions raised - returns original on parse failure.

    Example:
        >>> normalize_color_for_rich("lime")
        '#00FF00'
        >>> normalize_color_for_rich("#FF0000")
        '#FF0000'
        >>> normalize_color_for_rich("bright_green")  # Rich color
        '#00FF00'
        >>> normalize_color_for_rich(None)
        None
        >>> normalize_color_for_rich("invalid_color")
        'invalid_color'  # Returns original, let Rich handle

    Note:
        Cached with LRU cache (256 entries) for performance.
        Cache size covers all CSS4 (148) + common Rich colors (100+).
    """
    if not color:
        return None

    color = color.strip()

    # Empty after stripping - treat as None
    if not color:
        return None

    # Already hex - return as-is
    if color.startswith("#"):
        return color

    # Try parsing as CSS4/Rich color name
    try:
        r, g, b = parse_color(color)
        return rgb_to_hex(r, g, b)
    except (ValueError, KeyError):
        # Parsing failed - return original and let Rich try
        # This handles edge cases like Rich's special color names
        return color


def apply_line_gradient(
    lines: list[str],
    start_color: str,
    end_color: str,
    policy: RenderPolicy | None = None,
) -> list[str]:
    """Apply vertical gradient to lines (top to bottom).

    Optimized with cached color parsing and RGB interpolation.
    Policy-aware: returns uncolored lines when policy.color=False.

    Args:
        lines: Text lines to colorize
        start_color: Starting color (hex, RGB, or CSS4 name)
        end_color: Ending color (hex, RGB, or CSS4 name)
        policy: Optional RenderPolicy. If policy.color=False, returns lines unchanged.

    Returns:
        Lines with ANSI color codes applied (or unchanged if color disabled)

    Example:
        >>> lines = ["Line 1", "Line 2", "Line 3"]
        >>> colored = apply_line_gradient(lines, "red", "blue")
        >>> for line in colored:
        ...     print(line)  # Gradient from red to blue
    """
    if not lines:
        return lines

    # Check policy - skip colorization if color is disabled
    if policy is not None and not policy.color:
        return lines

    # Parse colors once (cached by lru_cache)
    start_rgb = parse_color(start_color)
    end_rgb = parse_color(end_color)

    colored_lines = []
    num_lines = len(lines)

    for i, line in enumerate(lines):
        # Calculate gradient position (0.0 to 1.0)
        t = i / (num_lines - 1) if num_lines > 1 else 0.0

        # Interpolate color using optimized RGB function
        r, g, b = interpolate_rgb(start_rgb, end_rgb, t)

        # Apply ANSI color code
        colored_line = f"\033[38;2;{r};{g};{b}m{line}\033[0m"
        colored_lines.append(colored_line)

    return colored_lines


def colorize_text(
    text: str,
    color: str,
    policy: RenderPolicy | None = None,
) -> str:
    """Apply color to text using ANSI codes.

    Policy-aware: returns plain text when policy.color=False.

    Args:
        text: Text to colorize
        color: Color specification (hex, RGB, or CSS4 name)
        policy: Optional RenderPolicy. If policy.color=False, returns text unchanged.

    Returns:
        ANSI colored text (or plain text if color disabled)

    Example:
        >>> colored = colorize_text("Hello", "red")
        >>> print(colored)  # Red text
    """
    # Check policy - skip colorization if color is disabled
    if policy is not None and not policy.color:
        return text

    r, g, b = parse_color(color)
    start_sequence = f"\033[38;2;{r};{g};{b}m"
    reset_sequence = "\033[0m"

    # Handle nested resets to preserve gradient
    if reset_sequence in text:
        text = text.replace(reset_sequence, reset_sequence + start_sequence)

    return f"{start_sequence}{text}{reset_sequence}"


def color_to_ansi(
    text: str,
    color: str,
    policy: RenderPolicy | None = None,
) -> str:
    """Apply color to text using ANSI codes (alias for colorize_text).

    Policy-aware: returns plain text when policy.color=False.

    Args:
        text: Text to colorize
        color: Color specification (hex, RGB, or CSS4 name)
        policy: Optional RenderPolicy. If policy.color=False, returns text unchanged.

    Returns:
        ANSI colored text (or plain text if color disabled)
    """
    return colorize_text(text, color, policy)


# Rainbow color spectrum (7 colors: ROYGBIV)
RAINBOW_COLORS = [
    "red",  # #FF0000
    "orange",  # #FFA500
    "yellow",  # #FFFF00
    "lime",  # #00FF00 (bright green for rainbow spectrum)
    "blue",  # #0000FF
    "indigo",  # #4B0082
    "darkviolet",  # #9400D3
]


def get_rainbow_color(position: float) -> str:
    """Get rainbow color at a specific position.

    Args:
        position: Position in rainbow (0.0 = red, 1.0 = violet)

    Returns:
        Hex color code at that position in rainbow spectrum
    """
    position = max(0.0, min(1.0, position))
    num_segments = len(RAINBOW_COLORS) - 1
    segment_size = 1.0 / num_segments
    segment_index = min(int(position / segment_size), num_segments - 1)
    local_position = (position - segment_index * segment_size) / segment_size

    return interpolate_color(
        RAINBOW_COLORS[segment_index], RAINBOW_COLORS[segment_index + 1], local_position
    )


# Alias for backward compatibility
colorize = colorize_text


__all__ = [
    "CSS4_COLORS",
    "RGBColor",
    "apply_line_gradient",
    "apply_line_gradient",
    "color_distance",
    "color_distance",
    "color_to_ansi",
    "colorize",
    "colorize_text",
    "get_color_names",
    "get_rainbow_color",
    "hex_to_rgb",
    "interpolate_color",
    "interpolate_rgb",
    "normalize_color_for_rich",
    "parse_color",
    "rgb_to_hex",
]
