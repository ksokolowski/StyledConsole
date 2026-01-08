"""Effect specification for declarative effect definitions.

This module provides EffectSpec, a frozen dataclass that describes visual effects
(gradients, rainbows, etc.) in a declarative, serializable way.

Example:
    >>> from styledconsole.effects import EffectSpec
    >>>
    >>> # Two-color gradient
    >>> fire = EffectSpec.gradient("red", "yellow")
    >>>
    >>> # Multi-stop gradient
    >>> ocean = EffectSpec.multi_stop(["#0077be", "#00a8cc", "#00d4ff"])
    >>>
    >>> # Rainbow with options
    >>> neon = EffectSpec.rainbow(saturation=1.2, brightness=1.1)
    >>>
    >>> # Animated rainbow with phase
    >>> from styledconsole import cycle_phase
    >>> phase = 0.0
    >>> for _ in range(30):
    ...     animated = EffectSpec.rainbow(phase=phase)
    ...     phase = cycle_phase(phase)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

# Phase animation constants
PHASE_FULL_CYCLE = 1.0
"""Full phase cycle (0.0 to 1.0) for gradient animations."""

PHASE_INCREMENT_DEFAULT = 0.033
"""Default phase increment per frame (~30 frames for full cycle).

This provides smooth animation at typical frame rates:
- 10 FPS: 3.0 seconds for full cycle
- 15 FPS: 2.0 seconds for full cycle
- 30 FPS: 1.0 second for full cycle
"""


def cycle_phase(current_phase: float, increment: float = PHASE_INCREMENT_DEFAULT) -> float:
    """Advance phase for gradient animation with wrapping.

    Increments the phase value and wraps around at 1.0 to create
    seamless looping animations. Supports both forward (positive increment)
    and reverse (negative increment) animations.

    Args:
        current_phase: Current phase value (any float, will be normalized).
        increment: Amount to add to phase. Default is ~30 frames per cycle.
            Use negative values for reverse animations.

    Returns:
        New phase value in range [0.0, 1.0).

    Example:
        >>> # Forward animation
        >>> phase = 0.0
        >>> phase = cycle_phase(phase)  # 0.033
        >>> phase = cycle_phase(phase)  # 0.066

        >>> # Reverse animation
        >>> phase = cycle_phase(0.1, increment=-0.2)  # 0.9 (wraps backward)

        >>> # Custom speed (60 frames per cycle)
        >>> phase = cycle_phase(phase, increment=1.0/60)  # 0.0167

        >>> # Frame calculation for desired duration:
        >>> # For 30 FPS over 2 seconds (60 frames):
        >>> increment = PHASE_FULL_CYCLE / 60  # 0.0167 per frame
    """
    return (current_phase + increment) % PHASE_FULL_CYCLE


@dataclass(frozen=True)
class EffectSpec:
    """Specification for a visual effect.

    EffectSpec is a frozen (immutable) dataclass that describes how to apply
    visual effects like gradients or rainbows. It follows the same pattern as
    GradientSpec and Theme in the codebase.

    Attributes:
        name: Effect type identifier ("gradient", "rainbow", "multi_stop").
        colors: Tuple of color values (hex, RGB, or CSS4 names).
        direction: Gradient direction ("vertical", "horizontal", "diagonal").
        target: What to apply effect to ("content", "border", "both").
        layer: Color layer ("foreground", "background", "both").
        background_colors: Separate background colors when layer="both".
        saturation: Color saturation multiplier (1.0 = normal).
        brightness: Color brightness multiplier (1.0 = normal).
        reverse: Reverse the gradient/rainbow direction.

    Example:
        >>> # Direct construction
        >>> spec = EffectSpec(
        ...     name="gradient",
        ...     colors=("cyan", "magenta"),
        ...     direction="horizontal",
        ... )
        >>>
        >>> # Factory methods (preferred)
        >>> spec = EffectSpec.gradient("cyan", "magenta", direction="horizontal")
    """

    name: str
    colors: tuple[str, ...] = field(default_factory=tuple)
    direction: Literal["vertical", "horizontal", "diagonal"] = "vertical"
    target: Literal["content", "border", "both"] = "both"
    layer: Literal["foreground", "background"] = "foreground"
    background_colors: tuple[str, ...] | None = None
    saturation: float = 1.0
    brightness: float = 1.0
    reverse: bool = False
    neon: bool = False  # Use neon/cyberpunk color palette for rainbows
    phase: float = 0.0  # Animation phase offset (0.0-1.0, normalized via modulo)

    def __post_init__(self) -> None:
        """Normalize phase to [0.0, 1.0) range."""
        # Frozen dataclass requires object.__setattr__
        object.__setattr__(self, "phase", self.phase % PHASE_FULL_CYCLE)

    # =========================================================================
    # Factory Methods
    # =========================================================================

    @classmethod
    def gradient(
        cls,
        start_color: str,
        end_color: str,
        *,
        direction: Literal["vertical", "horizontal", "diagonal"] = "vertical",
        target: Literal["content", "border", "both"] = "both",
        layer: Literal["foreground", "background"] = "foreground",
        reverse: bool = False,
        phase: float = 0.0,
    ) -> EffectSpec:
        """Create a two-color gradient effect.

        Args:
            start_color: Starting color (hex, RGB, or CSS4 name).
            end_color: Ending color (hex, RGB, or CSS4 name).
            direction: Gradient direction.
            target: What to apply effect to.
            layer: Color layer to use.
            reverse: Reverse the gradient direction.
            phase: Animation phase offset (0.0-1.0, values normalized via modulo).
                Use cycle_phase() to increment smoothly. See animation example:
                StyledConsole-Examples/04_effects/animation.py

        Returns:
            EffectSpec configured for a two-color gradient.

        Example:
            >>> fire = EffectSpec.gradient("red", "orange")
            >>> ocean = EffectSpec.gradient("#0077be", "#00d4ff", direction="horizontal")
            >>> animated = EffectSpec.gradient("cyan", "magenta", phase=0.25)
        """
        return cls(
            name="gradient",
            colors=(start_color, end_color),
            direction=direction,
            target=target,
            layer=layer,
            reverse=reverse,
            phase=phase,
        )

    @classmethod
    def multi_stop(
        cls,
        colors: list[str] | tuple[str, ...],
        *,
        direction: Literal["vertical", "horizontal", "diagonal"] = "vertical",
        target: Literal["content", "border", "both"] = "both",
        layer: Literal["foreground", "background"] = "foreground",
        reverse: bool = False,
        phase: float = 0.0,
    ) -> EffectSpec:
        """Create a multi-color gradient effect with 3+ colors.

        Args:
            colors: List of colors (minimum 2, typically 3+).
            direction: Gradient direction.
            target: What to apply effect to.
            layer: Color layer to use.
            reverse: Reverse the gradient direction.
            phase: Animation phase offset (0.0-1.0, values normalized via modulo).
                Use cycle_phase() to increment smoothly. See animation example:
                StyledConsole-Examples/04_effects/animation.py

        Returns:
            EffectSpec configured for a multi-stop gradient.

        Example:
            >>> sunset = EffectSpec.multi_stop(["#ff6b6b", "#feca57", "#ff9ff3"])
            >>> fire = EffectSpec.multi_stop(["red", "orange", "yellow"])
            >>> animated = EffectSpec.multi_stop(["red", "orange", "yellow"], phase=0.5)
        """
        color_tuple = tuple(colors) if isinstance(colors, list) else colors
        if len(color_tuple) < 2:
            raise ValueError("multi_stop requires at least 2 colors")
        return cls(
            name="multi_stop",
            colors=color_tuple,
            direction=direction,
            target=target,
            layer=layer,
            reverse=reverse,
            phase=phase,
        )

    @classmethod
    def rainbow(
        cls,
        *,
        direction: Literal["vertical", "horizontal", "diagonal"] = "vertical",
        target: Literal["content", "border", "both"] = "both",
        layer: Literal["foreground", "background"] = "foreground",
        saturation: float = 1.0,
        brightness: float = 1.0,
        reverse: bool = False,
        neon: bool = False,
        phase: float = 0.0,
    ) -> EffectSpec:
        """Create a rainbow spectrum effect (ROYGBIV).

        Args:
            direction: Rainbow direction.
            target: What to apply effect to.
            layer: Color layer to use.
            saturation: Color saturation (0.0-2.0, 1.0 = normal).
            brightness: Color brightness (0.0-2.0, 1.0 = normal).
            reverse: Reverse rainbow direction (violet to red).
            neon: Use neon/cyberpunk color palette for electric, vivid colors.
            phase: Animation phase offset (0.0-1.0, values normalized via modulo).
                Use cycle_phase() to increment smoothly. See animation example:
                StyledConsole-Examples/04_effects/animation.py

        Returns:
            EffectSpec configured for a rainbow effect.

        Example:
            >>> rainbow = EffectSpec.rainbow()
            >>> pastel = EffectSpec.rainbow(saturation=0.5, brightness=1.2)
            >>> neon = EffectSpec.rainbow(neon=True)
            >>> animated = EffectSpec.rainbow(phase=0.33, direction="diagonal")
        """
        return cls(
            name="rainbow",
            colors=(),  # Rainbow generates colors dynamically
            direction=direction,
            target=target,
            layer=layer,
            saturation=saturation,
            brightness=brightness,
            reverse=reverse,
            neon=neon,
            phase=phase,
        )

    @classmethod
    def from_palette(
        cls,
        name: str,
        *,
        direction: Literal["vertical", "horizontal", "diagonal"] = "vertical",
        target: Literal["content", "border", "both"] = "both",
        layer: Literal["foreground", "background"] = "foreground",
        reverse: bool = False,
        phase: float = 0.0,
    ) -> EffectSpec:
        """Create a multi-stop gradient from a named palette.

        Loads colors from the unified palette system (90 curated palettes)
        and creates a multi-stop gradient effect.

        Args:
            name: Palette name (e.g., 'ocean_depths', 'fire', 'pastel_candy').
            direction: Gradient direction.
            target: What to apply effect to.
            layer: Color layer to use.
            reverse: Reverse the gradient direction.
            phase: Animation phase offset (0.0-1.0, values normalized via modulo).
                Use cycle_phase() to increment smoothly. See animation example:
                StyledConsole-Examples/04_effects/animation.py

        Returns:
            EffectSpec configured with palette colors.

        Raises:
            ValueError: If palette name not found.

        Example:
            >>> ocean = EffectSpec.from_palette("ocean_depths")
            >>> sunset = EffectSpec.from_palette("aesthetic", direction="horizontal")
            >>> bedroom = EffectSpec.from_palette("bedroom_muted", reverse=True)
            >>> animated = EffectSpec.from_palette("fire", phase=0.66)
        """
        from styledconsole.data.palettes import get_palette

        palette_data = get_palette(name)
        if not palette_data:
            raise ValueError(
                f"Palette '{name}' not found. Use list_palettes() to see available palettes."
            )

        colors = palette_data["colors"]
        return cls.multi_stop(
            colors=colors,
            direction=direction,
            target=target,
            layer=layer,
            reverse=reverse,
            phase=phase,
        )

    # =========================================================================
    # Utility Methods
    # =========================================================================

    def is_gradient(self) -> bool:
        """Check if this is a gradient effect (not rainbow)."""
        return self.name in ("gradient", "multi_stop")

    def is_rainbow(self) -> bool:
        """Check if this is a rainbow effect."""
        return self.name == "rainbow"

    def is_multi_stop(self) -> bool:
        """Check if this is a multi-stop gradient."""
        return self.name == "multi_stop"

    def with_direction(
        self, direction: Literal["vertical", "horizontal", "diagonal"]
    ) -> EffectSpec:
        """Return a copy with a different direction.

        Args:
            direction: New direction.

        Returns:
            New EffectSpec with updated direction.
        """
        return EffectSpec(
            name=self.name,
            colors=self.colors,
            direction=direction,
            target=self.target,
            layer=self.layer,
            background_colors=self.background_colors,
            saturation=self.saturation,
            brightness=self.brightness,
            reverse=self.reverse,
            neon=self.neon,
            phase=self.phase,
        )

    def with_target(self, target: Literal["content", "border", "both"]) -> EffectSpec:
        """Return a copy with a different target.

        Args:
            target: New target.

        Returns:
            New EffectSpec with updated target.
        """
        return EffectSpec(
            name=self.name,
            colors=self.colors,
            direction=self.direction,
            target=target,
            layer=self.layer,
            background_colors=self.background_colors,
            saturation=self.saturation,
            brightness=self.brightness,
            reverse=self.reverse,
            neon=self.neon,
            phase=self.phase,
        )

    def reversed(self) -> EffectSpec:
        """Return a copy with reversed direction.

        Returns:
            New EffectSpec with reverse=True.
        """
        return EffectSpec(
            name=self.name,
            colors=self.colors,
            direction=self.direction,
            target=self.target,
            layer=self.layer,
            background_colors=self.background_colors,
            saturation=self.saturation,
            brightness=self.brightness,
            reverse=not self.reverse,
            neon=self.neon,
            phase=self.phase,
        )

    def with_phase(self, phase: float) -> EffectSpec:
        """Return a copy with a different phase.

        Useful for functional-style phase updates in animation loops.

        Args:
            phase: New phase value (0.0-1.0, normalized via modulo).

        Returns:
            New EffectSpec with updated phase.

        Example:
            >>> spec = EffectSpec.rainbow()
            >>> frame1 = spec.with_phase(0.0)
            >>> frame2 = spec.with_phase(0.1)
            >>> frame3 = spec.with_phase(0.2)
        """
        return EffectSpec(
            name=self.name,
            colors=self.colors,
            direction=self.direction,
            target=self.target,
            layer=self.layer,
            background_colors=self.background_colors,
            saturation=self.saturation,
            brightness=self.brightness,
            reverse=self.reverse,
            neon=self.neon,
            phase=phase,
        )
