"""Color Palettes - 90 curated color palettes with auto-categorization.

Palettes are curated from popular color combinations and organized by
HSL color space analysis for easy discovery.

Categories:
- Hue-based: warm, cool, red, orange, yellow, green, blue, purple, pink
- Saturation: vibrant, muted, pastel
- Lightness: dark, bright
- Special: monochrome, rainbow, neutral
"""

import json
from pathlib import Path
from typing import TypedDict


class PaletteInfo(TypedDict):
    """Palette metadata."""

    colors: list[str]
    categories: list[str]


# Load palettes at import time (simple, no lazy loading needed for small JSON)
_data_file = Path(__file__).parent / "palettes.json"
if not _data_file.exists():
    raise FileNotFoundError(f"Palette data file not found: {_data_file}")

_PALETTES_DATA: dict[str, PaletteInfo] = json.loads(_data_file.read_text())

# Public dict-like interface
PALETTES = _PALETTES_DATA


def get_palette(name: str) -> PaletteInfo | None:
    """Get a palette by name.

    Args:
        name: Palette name (snake_case).

    Returns:
        Palette info or None if not found.

    Example:
        >>> palette = get_palette("beach")
        >>> palette["colors"]
        ['#96ceb4', '#ffeead', '#ff6f69', '#ffcc5c', '#88d8b0']
    """
    return _PALETTES_DATA.get(name)


def list_palettes(category: str | None = None) -> list[str]:
    """List available palette names, optionally filtered by category.

    Args:
        category: Category to filter by (e.g., "vibrant", "pastel").

    Returns:
        List of palette names.

    Example:
        >>> pastel = list_palettes("pastel")
        >>> len(pastel)  # Number of pastel palettes
    """
    if category is None:
        return sorted(_PALETTES_DATA.keys())

    return sorted([name for name, info in _PALETTES_DATA.items() if category in info["categories"]])


def get_palette_categories() -> dict[str, int]:
    """Get all categories with palette counts.

    Returns:
        Dictionary of category names to counts.

    Example:
        >>> categories = get_palette_categories()
        >>> categories["vibrant"]
        45
    """
    categories: dict[str, int] = {}

    for info in _PALETTES_DATA.values():
        for cat in info["categories"]:
            categories[cat] = categories.get(cat, 0) + 1

    return dict(sorted(categories.items()))


__all__ = [
    "PALETTES",
    "PaletteInfo",
    "get_palette",
    "get_palette_categories",
    "list_palettes",
]
