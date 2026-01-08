"""Unified color registry with priority-based resolution.

This module provides a centralized color lookup system that respects source priority:
1. CSS4 Standard Colors (148 colors) - highest priority
2. Rich Extended Colors (251 colors) - medium priority
3. Extended Colors (949 colors) - lowest priority

Example:
    >>> from styledconsole.utils.color_registry import get_color, get_all_colors
    >>>
    >>> # Simple lookup (CSS4 takes precedence)
    >>> get_color("red")  # Returns CSS4 red: #ff0000
    >>>
    >>> # Get all available colors
    >>> colors = get_all_colors()
    >>> len(colors)  # ~1348 unique color names
    >>>
    >>> # Access extended filtered set
    >>> extended_colors = get_extended_colors(filtered=True)
"""

from typing import Literal

from styledconsole.data.colors import (
    COLORS,
)
from styledconsole.data.colors import (
    get_colors as _get_extended_all,
)
from styledconsole.data.colors import (
    get_filtered as _get_extended_filtered,
)
from styledconsole.utils.color_data import CSS4_COLORS, get_rich_color_names

# Cache for unified color registry
_COLOR_REGISTRY: dict[str, str] | None = None
_COLOR_REGISTRY_WITH_EXTENDED: dict[str, str] | None = None


def _build_color_registry(include_extended: bool = False) -> dict[str, str]:
    """Build unified color registry with priority ordering.

    Priority order (later entries override earlier ones):
    3. Extended colors (if included) - lowest priority
    2. Rich Extended - medium priority
    1. CSS4 - highest priority (final override)

    Args:
        include_extended: Whether to include extended colors.

    Returns:
        Unified color dictionary.
    """
    registry = {}

    # Layer 3: Extended colors (if included) - lowest priority
    if include_extended:
        registry.update(COLORS)

    # Layer 2: Rich Extended colors - override extended
    rich_colors = get_rich_color_names()
    for name in rich_colors:
        # Rich colors are already validated, just add them
        color = parse_color_simple(name)
        if color:
            registry[name] = color

    # Layer 1: CSS4 colors - highest priority, override everything
    registry.update(CSS4_COLORS)

    return registry


def get_color_registry(include_extended: bool = True) -> dict[str, str]:
    """Get the unified color registry.

    Args:
        include_extended: Whether to include extended colors (default: True).

    Returns:
        Dictionary mapping color names to hex codes.

    Example:
        >>> registry = get_color_registry()
        >>> registry["red"]  # CSS4 color
        '#ff0000'
        >>> registry["puke_green"]  # Extended color (if include_extended=True)
        '#9aae07'
    """
    global _COLOR_REGISTRY, _COLOR_REGISTRY_WITH_EXTENDED

    if include_extended:
        if _COLOR_REGISTRY_WITH_EXTENDED is None:
            _COLOR_REGISTRY_WITH_EXTENDED = _build_color_registry(include_extended=True)
        return _COLOR_REGISTRY_WITH_EXTENDED
    else:
        if _COLOR_REGISTRY is None:
            _COLOR_REGISTRY = _build_color_registry(include_extended=False)
        return _COLOR_REGISTRY


def get_color(name: str, include_extended: bool = True) -> str | None:
    """Get color hex code by name with priority resolution.

    Args:
        name: Color name (case-insensitive, spaces/dashes normalized to underscores).
        include_extended: Whether to include extended colors in lookup.

    Returns:
        Hex color code or None if not found.

    Example:
        >>> get_color("red")  # CSS4
        '#ff0000'
        >>> get_color("bright_red")  # Rich
        '#ff5555'
        >>> get_color("puke_green")  # Extended
        '#9aae07'
        >>> get_color("baby blue")  # Normalized to baby_blue (Extended)
        '#89cff0'
    """
    # Normalize name
    normalized = name.lower().replace(" ", "_").replace("-", "_")

    # Look up in registry
    registry = get_color_registry(include_extended=include_extended)
    return registry.get(normalized)


def get_all_colors(include_extended: bool = True) -> dict[str, str]:
    """Get all available colors.

    Args:
        include_extended: Whether to include extended colors.

    Returns:
        Dictionary of all color names to hex codes.

    Example:
        >>> colors = get_all_colors()
        >>> len(colors)  # ~1348 colors
        >>> "red" in colors
        True
        >>> "puke_green" in colors  # Extended
        True
    """
    return get_color_registry(include_extended=include_extended).copy()


def get_extended_colors(filtered: bool = False) -> dict[str, str]:
    """Get extended color names.

    Args:
        filtered: If True, return filtered set (excluding crude names).

    Returns:
        Dictionary of extended color names to hex codes.

    Example:
        >>> extended_all = get_extended_colors(filtered=False)
        >>> len(extended_all)  # 949 colors
        >>>
        >>> extended_filtered = get_extended_colors(filtered=True)
        >>> len(extended_filtered)  # 944 colors (excludes crude names)
        >>> "puke_green" in extended_filtered
        False
    """
    if filtered:
        return _get_extended_filtered()
    return _get_extended_all()


def get_color_source(name: str) -> Literal["css4", "rich", "extended", "unknown"]:
    """Determine the source of a color name.

    Args:
        name: Color name.

    Returns:
        Source identifier: "css4", "rich", "extended", or "unknown".

    Example:
        >>> get_color_source("red")
        'css4'
        >>> get_color_source("bright_red")
        'rich'
        >>> get_color_source("puke_green")
        'extended'
        >>> get_color_source("not_a_color")
        'unknown'
    """
    normalized = name.lower().replace(" ", "_").replace("-", "_")

    # Check CSS4 first (highest priority)
    if normalized in CSS4_COLORS:
        return "css4"

    # Check Rich
    rich_colors = get_rich_color_names()
    if normalized in rich_colors:
        return "rich"

    # Check extended colors
    if normalized in COLORS:
        return "extended"

    return "unknown"


def list_colors_by_source(
    source: Literal["css4", "rich", "extended"] | None = None,
) -> dict[str, str]:
    """List colors from a specific source.

    Args:
        source: Color source to filter by, or None for all.

    Returns:
        Dictionary of colors from the specified source.

    Example:
        >>> css4_colors = list_colors_by_source("css4")
        >>> len(css4_colors)  # 148
        >>>
        >>> rich_colors = list_colors_by_source("rich")
        >>> len(rich_colors)  # 251
    """
    if source == "css4":
        return CSS4_COLORS.copy()
    elif source == "rich":
        rich_names = get_rich_color_names()
        return {name: hex_val for name in rich_names if (hex_val := parse_color_simple(name))}
    elif source == "extended":
        return COLORS.copy()
    else:
        return get_all_colors(include_extended=True)


def parse_color_simple(color: str) -> str | None:
    """Simple color parser for Rich color names.

    This is a lightweight parser for existing Rich color resolution.
    For full color parsing (hex codes, RGB tuples, etc.), use Console.parse_color().

    Args:
        color: Color name or hex code.

    Returns:
        Hex code or None.
    """
    # Import here to avoid circular dependency
    from styledconsole.utils.color import parse_color

    try:
        result = parse_color(color)
        if result:
            r, g, b = result
            return f"#{r:02x}{g:02x}{b:02x}"
        return None
    except Exception:
        return None


# Public API
__all__ = [
    "get_all_colors",
    "get_color",
    "get_color_registry",
    "get_color_source",
    "get_extended_colors",
    "list_colors_by_source",
]
