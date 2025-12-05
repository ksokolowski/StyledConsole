"""Theme system for consistent color schemes.

This module provides a Theme dataclass for defining color schemes
and predefined themes for common use cases, including gradient support.

Example:
    >>> from styledconsole import Console, THEMES
    >>> console = Console(theme=THEMES.DARK)
    >>> console.frame("Success!", border_color="success")  # Uses theme's success color

    >>> # Gradient theme
    >>> console = Console(theme=THEMES.RAINBOW)
    >>> console.banner("HELLO")  # Uses rainbow gradient from theme
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GradientSpec:
    """Specification for a gradient effect.

    Attributes:
        start: Starting color of the gradient.
        end: Ending color of the gradient.
        direction: Direction for border gradients ('vertical' or 'horizontal').
    """

    start: str
    end: str
    direction: str = "vertical"


@dataclass(frozen=True)
class Theme:
    """A color theme for consistent styling across Console output.

    Themes define semantic colors that can be referenced by name
    instead of specifying exact color values. This enables:
    - Consistent color schemes across an application
    - Easy switching between light/dark modes
    - Professional, coordinated color palettes
    - Gradient effects for borders, text, and banners

    Attributes:
        name: Human-readable theme name.
        primary: Primary accent color for highlights and emphasis.
        secondary: Secondary accent color for less prominent elements.
        success: Color for success states (green family).
        warning: Color for warning states (yellow/orange family).
        error: Color for error states (red family).
        info: Color for informational states (blue family).
        border: Default border color for frames.
        text: Default text color.
        muted: Color for de-emphasized text.
        background: Background color hint (for HTML export).
        border_gradient: Optional gradient for frame borders.
        text_gradient: Optional gradient for text content.
        banner_gradient: Optional gradient for banner text.

    Example:
        >>> # Simple theme
        >>> theme = Theme(
        ...     name="Custom",
        ...     primary="dodgerblue",
        ...     success="lime",
        ... )

        >>> # Theme with gradients
        >>> theme = Theme(
        ...     name="Vibrant",
        ...     primary="magenta",
        ...     border_gradient=GradientSpec("magenta", "cyan"),
        ...     banner_gradient=GradientSpec("red", "yellow"),
        ... )
        >>> console = Console(theme=theme)
    """

    name: str = "default"
    primary: str = "cyan"
    secondary: str = "magenta"
    success: str = "green"
    warning: str = "yellow"
    error: str = "red"
    info: str = "blue"
    border: str = "white"
    text: str = "white"
    muted: str = "gray"
    background: str = "black"

    # Gradient specifications (optional)
    border_gradient: GradientSpec | None = None
    text_gradient: GradientSpec | None = None
    banner_gradient: GradientSpec | None = None

    def get_color(self, name: str) -> str | None:
        """Get a color by semantic name.

        Args:
            name: Color name (primary, success, warning, error, info, border, etc.)

        Returns:
            The color value, or None if not a semantic color name.
        """
        return getattr(self, name, None)

    def resolve_color(self, color: str | None) -> str | None:
        """Resolve a color that may be a semantic name or literal value.

        If the color is a semantic name (like 'success', 'error'), returns
        the theme's color for that semantic. Otherwise returns the color
        unchanged (assumed to be a literal like 'red' or '#ff0000').

        Args:
            color: A semantic color name or literal color value.

        Returns:
            The resolved color value, or None if input was None.
        """
        if color is None:
            return None

        # Check if it's a semantic color name
        semantic = self.get_color(color)
        if semantic is not None and semantic != color:
            return semantic

        # Return as-is (literal color)
        return color

    def has_gradients(self) -> bool:
        """Check if this theme has any gradient definitions."""
        return any([self.border_gradient, self.text_gradient, self.banner_gradient])


class THEMES:
    """Predefined theme collection.

    Available themes:
        - THEMES.DARK: Dark theme with cyan/lime accents
        - THEMES.LIGHT: Light theme with blue/green accents
        - THEMES.SOLARIZED: Solarized dark color scheme
        - THEMES.MONOKAI: Monokai editor color scheme
        - THEMES.NORD: Nord color scheme
        - THEMES.DRACULA: Dracula color scheme
        - THEMES.RAINBOW: Vibrant rainbow gradient theme
        - THEMES.OCEAN: Ocean-inspired blue gradient theme
        - THEMES.SUNSET: Warm sunset gradient theme
        - THEMES.NEON: Cyberpunk neon gradient theme

    Example:
        >>> from styledconsole import Console, THEMES
        >>> console = Console(theme=THEMES.MONOKAI)

        >>> # Gradient theme for eye-catching output
        >>> console = Console(theme=THEMES.RAINBOW)
        >>> console.banner("WELCOME")  # Rainbow gradient banner
    """

    DARK = Theme(
        name="dark",
        primary="cyan",
        secondary="magenta",
        success="bright_green",
        warning="yellow",
        error="red",
        info="blue",
        border="white",
        text="white",
        muted="bright_black",
        background="black",
    )

    LIGHT = Theme(
        name="light",
        primary="blue",
        secondary="magenta",
        success="green",
        warning="yellow",
        error="red",
        info="blue",
        border="bright_black",
        text="black",
        muted="bright_black",
        background="white",
    )

    SOLARIZED = Theme(
        name="solarized",
        primary="cyan",
        secondary="green",
        success="green",
        warning="yellow",
        error="red",
        info="blue",
        border="bright_black",
        text="bright_cyan",
        muted="blue",
        background="black",  # simplified
    )

    MONOKAI = Theme(
        name="monokai",
        primary="magenta",
        secondary="bright_blue",
        success="green",
        warning="yellow",
        error="magenta",
        info="cyan",
        border="white",
        text="white",
        muted="bright_black",
        background="black",
    )

    NORD = Theme(
        name="nord",
        primary="bright_blue",
        secondary="magenta",
        success="green",
        warning="yellow",
        error="red",
        info="blue",
        border="white",
        text="white",
        muted="bright_black",
        background="black",
    )

    DRACULA = Theme(
        name="dracula",
        primary="bright_magenta",
        secondary="purple",
        success="green",
        warning="yellow",
        error="bright_red",
        info="cyan",
        border="white",
        text="white",
        muted="blue",
        background="black",
    )

    # Gradient-enabled themes
    RAINBOW = Theme(
        name="rainbow",
        primary="magenta",
        secondary="cyan",
        success="bright_green",
        warning="yellow",
        error="red",
        info="blue",
        border="magenta",
        text="white",
        muted="bright_black",
        background="black",
        border_gradient=GradientSpec("red", "magenta"),
        text_gradient=GradientSpec("red", "magenta"),
        banner_gradient=GradientSpec("red", "magenta"),
    )

    OCEAN = Theme(
        name="ocean",
        primary="blue",
        secondary="cyan",
        success="green",
        warning="yellow",
        error="red",
        info="cyan",
        border="blue",
        text="white",
        muted="bright_black",
        background="black",
        border_gradient=GradientSpec("blue", "cyan"),
        text_gradient=GradientSpec("blue", "cyan"),
        banner_gradient=GradientSpec("blue", "cyan"),
    )

    SUNSET = Theme(
        name="sunset",
        primary="red",
        secondary="magenta",
        success="bright_green",
        warning="yellow",
        error="red",
        info="cyan",
        border="red",
        text="white",
        muted="purple",
        background="black",
        border_gradient=GradientSpec("red", "magenta"),
        text_gradient=GradientSpec("red", "magenta"),
        banner_gradient=GradientSpec("red", "magenta"),
    )

    NEON = Theme(
        name="neon",
        primary="bright_green",
        secondary="bright_magenta",
        success="bright_green",
        warning="yellow",
        error="red",
        info="blue",
        border="bright_green",
        text="white",
        muted="bright_black",
        background="black",
        border_gradient=GradientSpec("bright_green", "magenta"),
        text_gradient=GradientSpec("bright_green", "magenta"),
        banner_gradient=GradientSpec("bright_green", "magenta"),
    )

    FIRE = Theme(
        name="fire",
        primary="red",
        secondary="orange3",
        success="yellow",
        warning="orange1",
        error="bright_red",
        info="gold3",
        border="red",
        text="white",
        muted="dark_red",
        background="black",
        border_gradient=GradientSpec("red", "yellow"),
        text_gradient=GradientSpec("red", "yellow"),
        banner_gradient=GradientSpec("red", "yellow"),
    )

    SUNNY = Theme(
        name="sunny",
        primary="gold3",
        secondary="orange1",
        success="bright_green",
        warning="red",
        error="red",
        info="cyan",
        border="gold3",
        text="black",
        muted="grey30",
        background="white",
        border_gradient=GradientSpec("yellow", "orange1"),
        text_gradient=GradientSpec("yellow", "orange1"),
        banner_gradient=GradientSpec("yellow", "orange1"),
    )

    @classmethod
    def all(cls) -> list[Theme]:
        """Return all predefined themes."""
        return [
            cls.DARK,
            cls.LIGHT,
            cls.SOLARIZED,
            cls.MONOKAI,
            cls.NORD,
            cls.DRACULA,
            cls.RAINBOW,
            cls.OCEAN,
            cls.SUNSET,
            cls.NEON,
        ]

    @classmethod
    def solid_themes(cls) -> list[Theme]:
        """Return only themes without gradients."""
        return [t for t in cls.all() if not t.has_gradients()]

    @classmethod
    def gradient_themes(cls) -> list[Theme]:
        """Return only themes with gradients."""
        return [t for t in cls.all() if t.has_gradients()]

    @classmethod
    def get(cls, name: str) -> Theme | None:
        """Get a theme by name (case-insensitive).

        Args:
            name: Theme name (dark, light, solarized, monokai, nord, dracula,
                  rainbow, ocean, sunset, neon).

        Returns:
            The Theme instance, or None if not found.
        """
        name_upper = name.upper()
        return getattr(cls, name_upper, None)

    @classmethod
    def get_theme(cls, name: str) -> Theme | None:
        """Alias for get() - get a theme by name (case-insensitive).

        Args:
            name: Theme name (dark, light, solarized, monokai, nord, dracula,
                  rainbow, ocean, sunset, neon).

        Returns:
            The Theme instance, or None if not found.
        """
        return cls.get(name)


# Default theme (no theme = current behavior)
DEFAULT_THEME = Theme(name="default")
