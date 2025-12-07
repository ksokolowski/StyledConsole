#!/usr/bin/env python3
"""Theme System Showcase - Demonstrates all predefined themes.

Shows how to use the theme system to create consistent color schemes
across your console output, including colored text inside frames
and gradient themes with automatic gradient application.
"""

from styledconsole import THEMES, Console, GradientSpec, Theme, icons
from styledconsole.utils.color import normalize_color_for_rich


def show_solid_themes(console: Console) -> None:
    """Show solid (non-gradient) themes."""
    console.text(f"\n{icons.ARTIST_PALETTE} Solid Themes:", bold=True, color="cyan")
    console.text("")

    for theme in THEMES.solid_themes():
        # Get hex colors for Rich markup inside frame content
        primary_hex = normalize_color_for_rich(theme.primary)
        success_hex = normalize_color_for_rich(theme.success)
        warning_hex = normalize_color_for_rich(theme.warning)
        error_hex = normalize_color_for_rich(theme.error)
        info_hex = normalize_color_for_rich(theme.info)
        secondary_hex = normalize_color_for_rich(theme.secondary)
        muted_hex = normalize_color_for_rich(theme.muted)

        # Build content with Rich markup for colors INSIDE the frame
        content = f"""[bold]{icons.ARTIST_PALETTE} {theme.name.upper()} Theme[/bold]

[{primary_hex}]{icons.STAR} Primary: {theme.primary}[/]
[{success_hex}]{icons.CHECK_MARK_BUTTON} Success: {theme.success}[/]
[{warning_hex}]{icons.WARNING} Warning: {theme.warning}[/]
[{error_hex}]{icons.CROSS_MARK} Error: {theme.error}[/]
[{info_hex}]{icons.INFORMATION} Info: {theme.info}[/]
[{secondary_hex}]{icons.SPARKLES} Secondary: {theme.secondary}[/]
[{muted_hex}]{icons.WHITE_CIRCLE} Muted: {theme.muted}[/]"""

        console.frame(content, border="rounded", border_color=primary_hex)
        console.text("")


def show_gradient_themes(console: Console) -> None:
    """Show gradient themes with automatic gradient application."""
    console.text(f"\n{icons.RAINBOW} Gradient Themes:", bold=True, color="magenta")
    console.text("(All gradients auto-applied: border, banner, AND text!)", color="gray")
    console.text("")

    for theme in THEMES.gradient_themes():
        # Create themed console - gradients auto-apply!
        themed_console = Console(theme=theme)

        # Show banner with theme's banner_gradient
        themed_console.banner(theme.name.upper(), font="slant")

        # Show frame with theme's border_gradient AND text_gradient
        bg = theme.banner_gradient
        border_g = theme.border_gradient
        text_g = theme.text_gradient

        # Multi-line content shows per-line text gradient
        content = [
            f"{icons.SPARKLES} Auto-applied gradients:",
            f"  Banner: {bg.start} → {bg.end}",
            f"  Border: {border_g.start} → {border_g.end}",
            f"  Text: {text_g.start} → {text_g.end}",
            "Each line gets interpolated color!",
        ]

        themed_console.frame(content, border="rounded")
        console.text("")


def show_custom_gradient_theme(console: Console) -> None:
    """Show how to create custom gradient themes."""
    console.text(f"\n{icons.SPARKLES} Custom Gradient Theme:", bold=True, color="gold")
    console.text("")

    # Create custom theme with gradients
    custom_theme = Theme(
        name="forest",
        primary="green",
        secondary="lime",
        success="lime",
        warning="yellow",
        error="orange",
        info="cyan",
        border="green",
        border_gradient=GradientSpec("darkgreen", "lime"),
        banner_gradient=GradientSpec("green", "yellow"),
        text_gradient=GradientSpec("darkgreen", "lime"),
    )

    custom_console = Console(theme=custom_theme)
    custom_console.banner("FOREST", font="slant")
    custom_console.frame(
        f"{icons.SEEDLING} Custom forest theme with leafy gradients!",
        border="rounded",
    )
    console.text("")


def show_semantic_colors(console: Console) -> None:
    """Show semantic color frames."""
    console.text(f"\n{icons.LIGHT_BULB} Semantic Frame Colors:", bold=True)

    dark_console = Console(theme="dark")

    dark_console.frame(
        f"{icons.CHECK_MARK_BUTTON} Success message!",
        border="rounded",
        border_color="success",
    )
    dark_console.frame(
        f"{icons.WARNING} Warning message!",
        border="rounded",
        border_color="warning",
    )
    dark_console.frame(
        f"{icons.CROSS_MARK} Error message!",
        border="rounded",
        border_color="error",
    )
    dark_console.frame(
        f"{icons.INFORMATION} Info message!",
        border="rounded",
        border_color="info",
    )


def main() -> None:
    """Demonstrate the theme system."""
    console = Console()
    console.banner("THEMES", font="slant", start_color="magenta", end_color="cyan")

    # Summary
    console.text(f"\nAvailable themes: {len(THEMES.all())}", bold=True)
    console.text(f"  Solid themes: {len(THEMES.solid_themes())}")
    console.text(f"  Gradient themes: {len(THEMES.gradient_themes())}")
    console.text("")

    # Show each category
    show_solid_themes(console)
    show_gradient_themes(console)
    show_custom_gradient_theme(console)
    show_semantic_colors(console)


if __name__ == "__main__":
    main()
