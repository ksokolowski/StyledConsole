"""Effect registry for named effect presets.

This module provides EffectRegistry and the global EFFECTS instance with
30+ pre-configured effect presets organized by category.

Example:
    >>> from styledconsole.effects import EFFECTS
    >>>
    >>> # Access presets by name
    >>> fire = EFFECTS.fire
    >>> ocean = EFFECTS["ocean"]
    >>>
    >>> # List available effects
    >>> print(EFFECTS.list_all())
    >>>
    >>> # Filter by category
    >>> gradients = EFFECTS.gradients()
    >>> rainbows = EFFECTS.rainbows()
"""

from __future__ import annotations

from styledconsole.core.registry import Registry
from styledconsole.effects.spec import EffectSpec


class EffectRegistry(Registry[EffectSpec]):
    """Registry for named effect presets.

    Extends the base Registry with effect-specific filtering methods.
    Provides attribute-style access (EFFECTS.fire) and dict-style access
    (EFFECTS["fire"]).

    Example:
        >>> from styledconsole.effects import EFFECTS
        >>> fire = EFFECTS.fire
        >>> fire.colors
        ('#ff0000', '#ff6600', '#ffcc00')
    """

    def __init__(self) -> None:
        super().__init__("effect")

    def gradients(self) -> list[EffectSpec]:
        """Return all gradient effects (two-color and multi-stop)."""
        return [e for e in self.values() if e.is_gradient()]

    def rainbows(self) -> list[EffectSpec]:
        """Return all rainbow effects."""
        return [e for e in self.values() if e.is_rainbow()]

    def by_direction(self, direction: str) -> list[EffectSpec]:
        """Return effects with a specific direction."""
        return [e for e in self.values() if e.direction == direction]


# =============================================================================
# Global Registry Instance
# =============================================================================

EFFECTS = EffectRegistry()

# =============================================================================
# Gradient Presets (10)
# =============================================================================

EFFECTS.register(
    "fire",
    EffectSpec.multi_stop(["#ff0000", "#ff6600", "#ffcc00"]),
)

EFFECTS.register(
    "ocean",
    EffectSpec.multi_stop(["#0077be", "#00a8cc", "#00d4ff"]),
)

EFFECTS.register(
    "sunset",
    EffectSpec.multi_stop(
        ["#ff6b6b", "#feca57", "#ff9ff3"],
        direction="horizontal",
    ),
)

EFFECTS.register(
    "forest",
    EffectSpec.gradient("#134e5e", "#71b280"),
)

EFFECTS.register(
    "aurora",
    EffectSpec.gradient("#00c9ff", "#92fe9d", direction="diagonal"),
)

EFFECTS.register(
    "lavender",
    EffectSpec.gradient("#667eea", "#764ba2"),
)

EFFECTS.register(
    "peach",
    EffectSpec.gradient("#ed6ea0", "#ec8c69", direction="horizontal"),
)

EFFECTS.register(
    "mint",
    EffectSpec.gradient("#00b09b", "#96c93d"),
)

EFFECTS.register(
    "steel",
    EffectSpec.gradient("#485563", "#29323c"),
)

EFFECTS.register(
    "gold",
    EffectSpec.gradient("#f7971e", "#ffd200"),
)

# =============================================================================
# Rainbow Presets (7)
# =============================================================================

EFFECTS.register(
    "rainbow",
    EffectSpec.rainbow(),
)

EFFECTS.register(
    "rainbow_pastel",
    EffectSpec.rainbow(saturation=0.5, brightness=1.2),
)

EFFECTS.register(
    "rainbow_neon",
    EffectSpec.rainbow(saturation=1.2, brightness=1.1),
)

EFFECTS.register(
    "rainbow_muted",
    EffectSpec.rainbow(saturation=0.3, brightness=0.9),
)

EFFECTS.register(
    "rainbow_reverse",
    EffectSpec.rainbow(reverse=True),
)

EFFECTS.register(
    "rainbow_horizontal",
    EffectSpec.rainbow(direction="horizontal"),
)

EFFECTS.register(
    "rainbow_diagonal",
    EffectSpec.rainbow(direction="diagonal"),
)

# =============================================================================
# Themed Presets (6)
# =============================================================================

EFFECTS.register(
    "matrix",
    EffectSpec.gradient("#003300", "#00ff00"),
)

EFFECTS.register(
    "cyberpunk",
    EffectSpec.gradient("#ff00ff", "#00ffff"),
)

EFFECTS.register(
    "retro",
    EffectSpec.gradient("#ff6b6b", "#feca57"),
)

EFFECTS.register(
    "vaporwave",
    EffectSpec.multi_stop(["#ff71ce", "#01cdfe", "#05ffa1"]),
)

EFFECTS.register(
    "dracula",
    EffectSpec.gradient("#bd93f9", "#ff79c6"),
)

EFFECTS.register(
    "nord_aurora",
    EffectSpec.multi_stop(
        [
            "#bf616a",  # Red
            "#d08770",  # Orange
            "#ebcb8b",  # Yellow
            "#a3be8c",  # Green
            "#b48ead",  # Purple
        ]
    ),
)

# =============================================================================
# Semantic Presets (5)
# =============================================================================

EFFECTS.register(
    "success",
    EffectSpec.gradient("#00b894", "#00cec9"),
)

EFFECTS.register(
    "warning",
    EffectSpec.gradient("#fdcb6e", "#e17055"),
)

EFFECTS.register(
    "error",
    EffectSpec.gradient("#d63031", "#e84393"),
)

EFFECTS.register(
    "info",
    EffectSpec.gradient("#0984e3", "#74b9ff"),
)

EFFECTS.register(
    "neutral",
    EffectSpec.gradient("#636e72", "#b2bec3"),
)

# =============================================================================
# Border-Only Presets (4)
# =============================================================================

EFFECTS.register(
    "border_fire",
    EffectSpec.multi_stop(
        ["#ff0000", "#ff6600", "#ffcc00"],
        target="border",
    ),
)

EFFECTS.register(
    "border_ocean",
    EffectSpec.multi_stop(
        ["#0077be", "#00a8cc", "#00d4ff"],
        target="border",
    ),
)

EFFECTS.register(
    "border_rainbow",
    EffectSpec.rainbow(target="border"),
)

EFFECTS.register(
    "border_gold",
    EffectSpec.gradient("#f7971e", "#ffd200", target="border"),
)
