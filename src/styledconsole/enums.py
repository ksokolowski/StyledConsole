"""Enumeration types for StyledConsole.

Provides StrEnum types for all string constants, enabling IDE autocomplete
and type safety while maintaining backward compatibility with string values.

Example:
    >>> from styledconsole import Console, Border, Effect, Align
    >>> console = Console()
    >>> console.frame("Hello", border=Border.ROUNDED, effect=Effect.OCEAN)
    >>> console.frame("Centered", align=Align.CENTER)

    # String values still work for backward compatibility
    >>> console.frame("Hello", border="rounded", effect="ocean")
"""

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        """Backport of StrEnum for Python < 3.11."""

        def __new__(cls, value: str) -> "StrEnum":
            member = str.__new__(cls, value)
            member._value_ = value
            return member

        def __str__(self) -> str:
            return self.value


__all__ = [
    "Align",
    "Border",
    "Direction",
    "Effect",
    "ExportFormat",
    "LayoutMode",
    "Target",
]


class Align(StrEnum):
    """Text alignment options.

    Example:
        >>> from styledconsole import Console, Align
        >>> console = Console()
        >>> console.frame("Centered", align=Align.CENTER)
    """

    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


class Border(StrEnum):
    """Border style options for frames.

    Example:
        >>> from styledconsole import Console, Border
        >>> console = Console()
        >>> console.frame("Hello", border=Border.ROUNDED)
        >>> console.frame("Important", border=Border.DOUBLE)
    """

    SOLID = "solid"
    DOUBLE = "double"
    ROUNDED = "rounded"
    HEAVY = "heavy"
    THICK = "thick"
    ROUNDED_THICK = "rounded_thick"
    ASCII = "ascii"
    MINIMAL = "minimal"
    DOTS = "dots"


class Direction(StrEnum):
    """Gradient direction options.

    Example:
        >>> from styledconsole import EffectSpec, Direction
        >>> effect = EffectSpec.gradient("red", "blue", direction=Direction.HORIZONTAL)
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    DIAGONAL = "diagonal"


class Target(StrEnum):
    """Effect target options (what to apply effects to).

    Example:
        >>> from styledconsole import EffectSpec, Target
        >>> effect = EffectSpec.gradient("red", "blue", target=Target.BORDER)
    """

    CONTENT = "content"
    BORDER = "border"
    BOTH = "both"


class LayoutMode(StrEnum):
    """Layout mode options for frame groups and layouts.

    Example:
        >>> from styledconsole import Console, LayoutMode
        >>> console = Console()
        >>> console.frame_group(items, layout=LayoutMode.HORIZONTAL)
    """

    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    GRID = "grid"


class ExportFormat(StrEnum):
    """Export format options.

    Example:
        >>> from styledconsole import Console, ExportFormat
        >>> console = Console(record=True)
        >>> console.frame("Hello")
        >>> html = console.export_html()  # or use ExportFormat.HTML
    """

    HTML = "html"
    TEXT = "text"
    PNG = "png"
    WEBP = "webp"
    GIF = "gif"


class Effect(StrEnum):
    """Named effect presets for gradients and rainbows.

    32+ pre-configured effects organized by category:
    - Gradients: FIRE, OCEAN, SUNSET, FOREST, AURORA, LAVENDER, PEACH, MINT, STEEL, GOLD
    - Rainbows: RAINBOW, RAINBOW_PASTEL, RAINBOW_NEON, RAINBOW_MUTED, etc.
    - Themed: MATRIX, CYBERPUNK, RETRO, VAPORWAVE, DRACULA, NORD_AURORA
    - Semantic: SUCCESS, WARNING, ERROR, INFO, NEUTRAL
    - Border-only: BORDER_FIRE, BORDER_OCEAN, BORDER_RAINBOW, BORDER_GOLD
    - Nature: BEACH, AUTUMN, SPRING_BLOSSOM, WINTER_FROST
    - Food: CAPPUCCINO, TROPICAL_JUICE, BERRY_SMOOTHIE
    - Tech: TERMINAL_GREEN, ELECTRIC_BLUE, CYBER_MAGENTA
    - Pastels: PASTEL_CANDY, SOFT_RAINBOW
    - Dark: DARK_PURPLE, MIDNIGHT, CARBON

    Example:
        >>> from styledconsole import Console, Effect
        >>> console = Console()
        >>> console.frame("Fire!", effect=Effect.FIRE)
        >>> console.frame("Ocean", effect=Effect.OCEAN)
        >>> console.banner("CYBER", effect=Effect.CYBERPUNK)
    """

    # Gradient presets (10)
    FIRE = "fire"
    OCEAN = "ocean"
    SUNSET = "sunset"
    FOREST = "forest"
    AURORA = "aurora"
    LAVENDER = "lavender"
    PEACH = "peach"
    MINT = "mint"
    STEEL = "steel"
    GOLD = "gold"

    # Rainbow presets (7)
    RAINBOW = "rainbow"
    RAINBOW_PASTEL = "rainbow_pastel"
    RAINBOW_NEON = "rainbow_neon"
    RAINBOW_MUTED = "rainbow_muted"
    RAINBOW_REVERSE = "rainbow_reverse"
    RAINBOW_HORIZONTAL = "rainbow_horizontal"
    RAINBOW_DIAGONAL = "rainbow_diagonal"

    # Themed presets (6)
    MATRIX = "matrix"
    CYBERPUNK = "cyberpunk"
    RETRO = "retro"
    VAPORWAVE = "vaporwave"
    DRACULA = "dracula"
    NORD_AURORA = "nord_aurora"

    # Semantic presets (5)
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"
    NEUTRAL = "neutral"

    # Border-only presets (4)
    BORDER_FIRE = "border_fire"
    BORDER_OCEAN = "border_ocean"
    BORDER_RAINBOW = "border_rainbow"
    BORDER_GOLD = "border_gold"

    # Nature & Seasons (4)
    BEACH = "beach"
    AUTUMN = "autumn"
    SPRING_BLOSSOM = "spring_blossom"
    WINTER_FROST = "winter_frost"

    # Food & Drink (3)
    CAPPUCCINO = "cappuccino"
    TROPICAL_JUICE = "tropical_juice"
    BERRY_SMOOTHIE = "berry_smoothie"

    # Tech & Cyber (3)
    TERMINAL_GREEN = "terminal_green"
    ELECTRIC_BLUE = "electric_blue"
    CYBER_MAGENTA = "cyber_magenta"

    # Pastels (2)
    PASTEL_CANDY = "pastel_candy"
    SOFT_RAINBOW = "soft_rainbow"

    # Dark Themes (3)
    DARK_PURPLE = "dark_purple"
    MIDNIGHT = "midnight"
    CARBON = "carbon"
