"""Configuration constants for image export.

This module centralizes configuration values and magic numbers used for
image generation, font loading, and styling.
"""

from __future__ import annotations

# =============================================================================
# Theme Defaults
# =============================================================================

# Catppuccin Mocha Palette
# Reference: https://catppuccin.com/palette
THEME_MOCHA_BACKGROUND = "#11111b"  # Crust
THEME_MOCHA_FOREGROUND = "#cdd6f4"  # Text

DEFAULT_FONT_SIZE_PX = 16
"""Default font size in pixels.
16px matches common terminal defaults and scales cleanly to 2x (32px).
"""

DEFAULT_LINE_HEIGHT = 1.4
"""Line height multiplier.
1.4 provides comfortable reading and space for emojis.
"""

DEFAULT_PADDING_PX = 20
"""Padding around terminal content in pixels."""

# =============================================================================
# Font Configuration
# =============================================================================

FONT_MEASURE_CHAR = "M"
"""Character used for measuring monospace font dimensions."""

TEMP_IMAGE_SIZE = (100, 100)
"""Temporary image size for font measurement."""

# Font Search Paths (Standard Locations)
FONT_DIRS: dict[str, list[str]] = {
    "linux": [
        "~/.local/share/fonts",
        "~/.fonts",
        "/usr/share/fonts",
        "/usr/local/share/fonts",
    ],
    "darwin": [
        "~/Library/Fonts",
        "/Library/Fonts",
        "/System/Library/Fonts",
    ],
    "win32": [
        "%WINDIR%\\Fonts",
        "%LOCALAPPDATA%\\Microsoft\\Windows\\Fonts",
    ],
}

# Preferred Fonts (in order of preference)
FONT_NAMES_MONOSPACE = [
    "DejaVu Sans Mono",
    "Bitstream Vera Sans Mono",
    "Liberation Mono",
    "Noto Sans Mono",
    "Consolas",
    "Menlo",
    "Monaco",
    "Courier New",
    "Courier",
]

FONT_NAMES_EMOJI = [
    "Noto Color Emoji",
    "Apple Color Emoji",
    "Segoe UI Emoji",
]

# =============================================================================
# Emoji Rendering
# =============================================================================

EMOJI_SCALE_FACTOR = 1.0
"""Default scale factor for emoji size relative to font size."""

EMOJI_MIN_SIZE_PX = 12
"""Minimum size in pixels for rendered emojis."""

EMOJI_LINE_HEIGHT_FACTOR = 0.75
"""Fraction of line height to use for emoji sizing when line_height is set."""

EMOJI_POSITION_OFFSET = (0, -2)
"""Default pixel offset (x, y) for emoji positioning."""

# =============================================================================
# Text Decoration Rendering
# =============================================================================

TEXT_DECORATION_THICKNESS_DIVISOR = 12
"""Divisor for calculating text decoration line thickness.

Line thickness = max(1, char_height // TEXT_DECORATION_THICKNESS_DIVISOR)

Value of 12 produces visually balanced underlines and strikethroughs
that scale proportionally with font size:
- 16px font → ~1px line (16 // 12 = 1)
- 24px font → 2px line (24 // 12 = 2)
- 36px font → 3px line (36 // 12 = 3)
"""

TEXT_DECORATION_UNDERLINE_OFFSET = 3
"""Pixels from bottom of character cell for underline position."""

TEXT_DECORATION_OVERLINE_OFFSET = 2
"""Pixels from top of character cell for overline position."""
