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

    def load_palette(
        self,
        name: str,
        *,
        direction: str = "vertical",
        target: str = "both",
        layer: str = "foreground",
        reverse: bool = False,
    ) -> EffectSpec:
        """Dynamically load a palette as an effect.

        Creates a multi-stop gradient from any of the 90 curated palettes.
        This provides runtime palette loading without pre-registering all palettes.

        Args:
            name: Palette name (e.g., 'ocean_depths', 'pastel_candy').
            direction: Gradient direction ('vertical', 'horizontal', 'diagonal').
            target: What to apply effect to ('content', 'border', 'both').
            layer: Color layer ('foreground', 'background').
            reverse: Reverse the gradient direction.

        Returns:
            EffectSpec configured with palette colors.

        Raises:
            ValueError: If palette name not found.

        Example:
            >>> from styledconsole.effects import EFFECTS
            >>> ocean = EFFECTS.load_palette("ocean_depths", direction="horizontal")
            >>> bedroom = EFFECTS.load_palette("bedroom_muted", reverse=True)
        """
        return EffectSpec.from_palette(
            name,
            direction=direction,  # type: ignore[arg-type]
            target=target,  # type: ignore[arg-type]
            layer=layer,  # type: ignore[arg-type]
            reverse=reverse,
        )


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
    EffectSpec.rainbow(neon=True),
)

EFFECTS.register(
    "rainbow_muted",
    EffectSpec.rainbow(saturation=0.3, brightness=0.8),
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

# =============================================================================
# Curated Palette Presets
# Optimized preset effects with pre-configured direction and target settings
# =============================================================================

# Nature & Seasons
EFFECTS.register(
    "beach",
    EffectSpec.multi_stop(["#96ceb4", "#ffeaa7", "#dfe6e9", "#74b9ff"]),
)

EFFECTS.register(
    "autumn",
    EffectSpec.multi_stop(["#d63031", "#e17055", "#fdcb6e", "#6c5ce7"]),
)

EFFECTS.register(
    "spring_blossom",
    EffectSpec.multi_stop(["#fd79a8", "#fdcb6e", "#55efc4", "#74b9ff"]),
)

EFFECTS.register(
    "winter_frost",
    EffectSpec.multi_stop(["#dfe6e9", "#74b9ff", "#a29bfe", "#b2bec3"]),
)

# Food & Drink
EFFECTS.register(
    "cappuccino",
    EffectSpec.multi_stop(["#6c5b7b", "#c06c84", "#f67280", "#f8b195"]),
)

EFFECTS.register(
    "tropical_juice",
    EffectSpec.multi_stop(["#fc5c65", "#fd9644", "#fed330", "#26de81"]),
)

EFFECTS.register(
    "berry_smoothie",
    EffectSpec.multi_stop(["#a29bfe", "#fd79a8", "#e84393", "#6c5ce7"]),
)

# Tech & Cyber
EFFECTS.register(
    "terminal_green",
    EffectSpec.gradient("#052e16", "#00ff41"),
)

EFFECTS.register(
    "electric_blue",
    EffectSpec.multi_stop(["#0a3d62", "#0652dd", "#00a8ff", "#0abde3"]),
)

EFFECTS.register(
    "cyber_magenta",
    EffectSpec.multi_stop(["#ea00d9", "#c44569", "#5f27cd", "#341f97"]),
)

# Pastels
EFFECTS.register(
    "pastel_candy",
    EffectSpec.multi_stop(["#ffeaa7", "#fab1a0", "#fd79a8", "#a29bfe"]),
)

EFFECTS.register(
    "soft_rainbow",
    EffectSpec.multi_stop(["#ffcccc", "#ffd9b3", "#ffffcc", "#ccffcc", "#ccccff"]),
)

# Dark Themes
EFFECTS.register(
    "dark_purple",
    EffectSpec.gradient("#2c003e", "#512b58"),
)

EFFECTS.register(
    "midnight",
    EffectSpec.multi_stop(["#191970", "#0f0e23", "#1e3a8a", "#312e81"]),
)

EFFECTS.register(
    "carbon",
    EffectSpec.gradient("#2c3e50", "#34495e"),
)
