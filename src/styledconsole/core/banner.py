"""Banner rendering with ASCII art text using pyfiglet.

This module provides high-level banner rendering with:
- ASCII art text using pyfiglet fonts
- Gradient color support per line
- Optional frame borders around banners
- Emoji-aware fallback (renders plain text if emoji detected)
- Alignment and width control
"""

from dataclasses import dataclass

from styledconsole.core.styles import BorderStyle
from styledconsole.types import AlignType


@dataclass(frozen=True)
class Banner:
    """Configuration for ASCII art banner rendering.

    Attributes:
        text: Text to render as ASCII art (plain text only, emojis fallback to plain)
        font: Pyfiglet font name (default: "standard")
        start_color: Starting color for gradient (hex, rgb, or named color)
        end_color: Ending color for gradient (hex, rgb, or named color)
        rainbow: Use full ROYGBIV rainbow spectrum instead of linear gradient
        border: Border style name or BorderStyle object (None for no border)
        width: Fixed width for banner (None for auto-width)
        align: AlignType = "center"
        padding: Padding spaces inside border (only used if border is set)
    """

    text: str
    font: str = "standard"
    start_color: str | None = None
    end_color: str | None = None
    rainbow: bool = False
    border: str | BorderStyle | None = None
    width: int | None = None
    align: AlignType = "center"
    padding: int = 1


__all__ = [
    "Banner",
]
