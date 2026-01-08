"""Palette utilities for creating effects from color lists.

This module provides utilities for:
- Creating effects from color lists
- Converting palette data to EffectSpec objects

Example:
    >>> from styledconsole.utils.palette import create_palette_effect
    >>> from styledconsole import Console
    >>>
    >>> # Create effect from hex colors
    >>> colors = ["#96ceb4", "#ffeaa7", "#dfe6e9", "#74b9ff"]
    >>> effect = create_palette_effect(colors)
    >>> console = Console()
    >>> console.frame("Hello", effect=effect)
"""

from __future__ import annotations

from typing import Literal

from styledconsole.effects.spec import EffectSpec


def create_palette_effect(
    colors: list[str],
    *,
    direction: Literal["vertical", "horizontal", "diagonal"] = "vertical",
    target: Literal["content", "border", "both"] = "both",
    name: str | None = None,
) -> EffectSpec:
    """Create an effect from a list of colors.

    This is useful for importing palettes from color-hex.com or other sources.

    Args:
        colors: List of color values (hex codes, RGB tuples, or CSS4 names).
        direction: Gradient direction.
        target: What to apply effect to.
        name: Optional name for the palette (for reference).

    Returns:
        EffectSpec that can be used with console.frame(effect=...).

    Example:
        >>> # Create palette effect
        >>> beach = create_palette_effect(
        ...     ["#96ceb4", "#ffeaa7", "#dfe6e9", "#74b9ff"],
        ...     name="beach"
        ... )
        >>> console.frame("Vacation", effect=beach)
        >>>
        >>> # Horizontal gradient
        >>> sunset = create_palette_effect(
        ...     ["#ff6b6b", "#feca57", "#ff9ff3"],
        ...     direction="horizontal"
        ... )
    """
    if len(colors) < 2:
        raise ValueError(f"Need at least 2 colors for a gradient, got {len(colors)}")

    if len(colors) == 2:
        # Two-color gradient
        return EffectSpec.gradient(
            colors[0],
            colors[1],
            direction=direction,
            target=target,
        )
    else:
        # Multi-stop gradient
        return EffectSpec.multi_stop(
            tuple(colors),
            direction=direction,
            target=target,
        )


def palette_from_dict(data: dict) -> EffectSpec:
    """Create an effect from a palette dictionary.

    Args:
        data: Dictionary with 'colors' key and optional 'direction', 'target', 'name'.

    Returns:
        EffectSpec instance.

    Example:
        >>> palette_data = {
        ...     "name": "sunset",
        ...     "colors": ["#ff6b6b", "#feca57", "#ff9ff3"],
        ...     "direction": "horizontal"
        ... }
        >>> effect = palette_from_dict(palette_data)
    """
    colors = data["colors"]
    direction = data.get("direction", "vertical")
    target = data.get("target", "both")
    name = data.get("name")

    return create_palette_effect(
        colors,
        direction=direction,  # type: ignore[arg-type]
        target=target,  # type: ignore[arg-type]
        name=name,
    )


__all__ = [
    "create_palette_effect",
    "palette_from_dict",
]
