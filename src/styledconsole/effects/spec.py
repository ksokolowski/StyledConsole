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
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


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
    ) -> EffectSpec:
        """Create a two-color gradient effect.

        Args:
            start_color: Starting color (hex, RGB, or CSS4 name).
            end_color: Ending color (hex, RGB, or CSS4 name).
            direction: Gradient direction.
            target: What to apply effect to.
            layer: Color layer to use.
            reverse: Reverse the gradient direction.

        Returns:
            EffectSpec configured for a two-color gradient.

        Example:
            >>> fire = EffectSpec.gradient("red", "orange")
            >>> ocean = EffectSpec.gradient("#0077be", "#00d4ff", direction="horizontal")
        """
        return cls(
            name="gradient",
            colors=(start_color, end_color),
            direction=direction,
            target=target,
            layer=layer,
            reverse=reverse,
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
    ) -> EffectSpec:
        """Create a multi-color gradient effect with 3+ colors.

        Args:
            colors: List of colors (minimum 2, typically 3+).
            direction: Gradient direction.
            target: What to apply effect to.
            layer: Color layer to use.
            reverse: Reverse the gradient direction.

        Returns:
            EffectSpec configured for a multi-stop gradient.

        Example:
            >>> sunset = EffectSpec.multi_stop(["#ff6b6b", "#feca57", "#ff9ff3"])
            >>> fire = EffectSpec.multi_stop(["red", "orange", "yellow"])
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
    ) -> EffectSpec:
        """Create a rainbow spectrum effect (ROYGBIV).

        Args:
            direction: Rainbow direction.
            target: What to apply effect to.
            layer: Color layer to use.
            saturation: Color saturation (0.0-2.0, 1.0 = normal).
            brightness: Color brightness (0.0-2.0, 1.0 = normal).
            reverse: Reverse rainbow direction (violet to red).

        Returns:
            EffectSpec configured for a rainbow effect.

        Example:
            >>> rainbow = EffectSpec.rainbow()
            >>> pastel = EffectSpec.rainbow(saturation=0.5, brightness=1.2)
            >>> neon = EffectSpec.rainbow(saturation=1.2, brightness=1.1)
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
        )
