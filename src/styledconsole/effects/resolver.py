"""Effect resolver - bridges EffectSpec to strategy objects.

This module provides functions to convert declarative EffectSpec objects
into the concrete strategy objects used by the gradient engine.

Example:
    >>> from styledconsole.effects import EffectSpec, EFFECTS
    >>> from styledconsole.effects.resolver import resolve_effect
    >>>
    >>> # Resolve a preset by name
    >>> position, color, target = resolve_effect("fire")
    >>>
    >>> # Resolve an EffectSpec
    >>> spec = EffectSpec.rainbow(saturation=0.5)
    >>> position, color, target = resolve_effect(spec)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from styledconsole.effects.strategies import (
    BorderOnly,
    Both,
    ColorSource,
    ContentOnly,
    DiagonalPosition,
    EnhancedRainbow,
    HorizontalPosition,
    LinearGradient,
    MultiStopGradient,
    OffsetPositionStrategy,
    PositionStrategy,
    RainbowSpectrum,
    ReversedColorSource,
    TargetFilter,
    VerticalPosition,
)

if TYPE_CHECKING:
    from styledconsole.effects.spec import EffectSpec


def resolve_effect(
    effect: EffectSpec | str,
) -> tuple[PositionStrategy, ColorSource, TargetFilter]:
    """Convert an EffectSpec or preset name to strategy objects.

    This function bridges the declarative EffectSpec with the imperative
    strategy objects used by apply_gradient().

    Args:
        effect: An EffectSpec instance or a preset name (e.g., "fire", "rainbow").

    Returns:
        Tuple of (PositionStrategy, ColorSource, TargetFilter) for use
        with the gradient engine.

    Raises:
        KeyError: If effect is a string and not found in EFFECTS registry.
        TypeError: If effect is neither an EffectSpec nor a string.

    Example:
        >>> from styledconsole.effects.resolver import resolve_effect
        >>>
        >>> # From preset name
        >>> pos, color, target = resolve_effect("fire")
        >>>
        >>> # From EffectSpec
        >>> spec = EffectSpec.gradient("red", "blue")
        >>> pos, color, target = resolve_effect(spec)
    """
    from styledconsole.effects.registry import EFFECTS
    from styledconsole.effects.spec import EffectSpec

    # Handle string lookup
    if isinstance(effect, str):
        spec = EFFECTS.get(effect)
    elif isinstance(effect, EffectSpec):
        spec = effect
    else:
        raise TypeError(f"effect must be an EffectSpec or string, got {type(effect).__name__}")

    # Resolve position strategy
    position = _resolve_position(spec.direction)

    # Apply phase offset if non-zero (for animation)
    if spec.phase != 0.0:
        position = OffsetPositionStrategy(position, offset=spec.phase)

    # Resolve color source
    color = _resolve_color_source(spec)

    # Apply reverse if needed
    if spec.reverse and not spec.is_rainbow():
        # Rainbow handles reverse internally via EnhancedRainbow
        color = ReversedColorSource(color)

    # Resolve target filter
    target = _resolve_target(spec.target)

    return position, color, target


def _resolve_position(direction: str) -> PositionStrategy:
    """Convert direction string to PositionStrategy.

    Args:
        direction: One of "vertical", "horizontal", "diagonal".

    Returns:
        Appropriate PositionStrategy instance.
    """
    if direction == "horizontal":
        return HorizontalPosition()
    elif direction == "diagonal":
        return DiagonalPosition()
    else:
        return VerticalPosition()


def _resolve_color_source(spec: EffectSpec) -> ColorSource:
    """Convert EffectSpec to ColorSource.

    Args:
        spec: The effect specification.

    Returns:
        Appropriate ColorSource instance.
    """

    if spec.is_rainbow():
        # Use EnhancedRainbow if any adjustments or neon mode are needed
        if spec.saturation != 1.0 or spec.brightness != 1.0 or spec.reverse or spec.neon:
            return EnhancedRainbow(
                saturation=spec.saturation,
                brightness=spec.brightness,
                reverse=spec.reverse,
                neon=spec.neon,
            )
        # Use simple RainbowSpectrum for default rainbow
        return RainbowSpectrum()

    elif spec.is_multi_stop():
        return MultiStopGradient(spec.colors)

    else:  # gradient (two-color)
        if len(spec.colors) >= 2:
            return LinearGradient(spec.colors[0], spec.colors[1])
        # Fallback for edge cases
        return LinearGradient("white", "white")


def _resolve_target(target: str) -> TargetFilter:
    """Convert target string to TargetFilter.

    Args:
        target: One of "content", "border", "both".

    Returns:
        Appropriate TargetFilter instance.
    """
    if target == "content":
        return ContentOnly()
    elif target == "border":
        return BorderOnly()
    else:
        return Both()


def get_position_strategy(
    direction: str,
) -> PositionStrategy:
    """Get a position strategy by direction name.

    Convenience function for direct strategy access.

    Args:
        direction: One of "vertical", "horizontal", "diagonal".

    Returns:
        PositionStrategy instance.
    """
    return _resolve_position(direction)


def get_target_filter(
    target: str,
) -> TargetFilter:
    """Get a target filter by target name.

    Convenience function for direct filter access.

    Args:
        target: One of "content", "border", "both".

    Returns:
        TargetFilter instance.
    """
    return _resolve_target(target)
