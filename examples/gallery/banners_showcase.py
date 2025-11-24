#!/usr/bin/env python3
"""
🎪 Banner Typography Showcase

A celebration of ASCII art typography through pyfiglet integration,
featuring various fonts, gradient effects, and creative compositions.

Design Philosophy:
- Typography as art form
- Fonts convey personality and mood
- Gradients amplify visual impact
- Banners command attention

Run: python examples/gallery/banners_showcase.py
"""

from styledconsole import EMOJI, Console

console = Console(record=True)


def demo_standard_fonts():
    """Classic banner fonts for everyday use."""
    console.rule(f"{EMOJI.PERFORMING_ARTS} STANDARD FONTS", color="cyan")
    console.newline()

    console.text(
        "The workhorses of terminal typography.\nClear, readable, professional.",
        color="cyan",
        italic=True,
    )
    console.newline()

    # Standard font
    console.banner("STANDARD", font="standard", start_color="cyan", end_color="cyan")
    console.text("The default choice - clean and reliable", color="white", dim=True)
    console.newline(2)

    # Banner font
    console.banner("BANNER", font="banner", start_color="blue", end_color="blue")
    console.text("Bold and commanding - makes statements", color="white", dim=True)
    console.newline(2)

    # Big font
    console.banner("BIG", font="big", start_color="purple", end_color="purple")
    console.text("Extra large - for maximum impact", color="white", dim=True)
    console.newline(2)

    # Block font
    console.banner("BLOCK", font="block", start_color="magenta", end_color="magenta")
    console.text("Solid and substantial - hard to miss", color="white", dim=True)
    console.newline(2)


def demo_decorative_fonts():
    """Artistic and decorative banner fonts."""
    console.rule(f"{EMOJI.SPARKLES} DECORATIVE FONTS", color="magenta")
    console.newline()

    console.text(
        "Typography with personality.\nEach font tells a different story.",
        color="magenta",
        italic=True,
    )
    console.newline()

    # Slant font
    console.banner("SLANT", font="slant", start_color="cyan", end_color="cyan")
    console.text("Dynamic and modern - suggests motion", color="white", dim=True)
    console.newline(2)

    # Digital font
    console.banner("DIGITAL", font="digital", start_color="green", end_color="green")
    console.text("Retro tech aesthetic - LCD display vibes", color="white", dim=True)
    console.newline(2)

    # Mini font
    console.banner("MINI FONT", font="mini", start_color="yellow", end_color="yellow")
    console.text("Compact and efficient - maximum info density", color="white", dim=True)
    console.newline(2)

    # Script font (if available)
    console.banner("ELEGANT", font="script", start_color="magenta", end_color="magenta")
    console.text("Graceful and flowing - adds sophistication", color="white", dim=True)
    console.newline(2)


def demo_gradient_banners():
    """Banners with color gradients."""
    console.rule(f"{EMOJI.RAINBOW} GRADIENT BANNERS", color="yellow")
    console.newline()

    console.text(
        "Where typography meets color theory.\nGradients add depth and visual interest.",
        color="yellow",
        italic=True,
    )
    console.newline()

    # Fire gradient
    console.banner("FIRE", font="banner", start_color="red", end_color="yellow")
    console.text(f"{EMOJI.FIRE} From ember to flame - burning bright", color="white", dim=True)
    console.newline(2)

    # Ocean gradient
    console.banner("OCEAN", font="slant", start_color="cyan", end_color="blue")
    console.text(f"{EMOJI.OCEAN} Deep sea to shallow waters", color="white", dim=True)
    console.newline(2)

    # Forest gradient
    console.banner("FOREST", font="standard", start_color="green", end_color="lime")
    console.text(f"{EMOJI.EVERGREEN} From shadow to sunlight", color="white", dim=True)
    console.newline(2)

    # Sunset gradient
    console.banner("SUNSET", font="big", start_color="orange", end_color="purple")
    console.text(f"{EMOJI.SUNRISE} Day fading into night", color="white", dim=True)
    console.newline(2)

    # Galaxy gradient
    console.banner("GALAXY", font="banner", start_color="purple", end_color="cyan")
    console.text(f"{EMOJI.MILKY_WAY} Cosmic color journey", color="white", dim=True)
    console.newline(2)


def demo_rainbow_banners():
    """Full spectrum rainbow banners."""
    console.rule(f"{EMOJI.RAINBOW} RAINBOW SPECTRUM", color="magenta")
    console.newline()

    console.text(
        "The complete visible spectrum in typography.\nSeven colors celebrating chromatic unity.",
        color="magenta",
        italic=True,
    )
    console.newline()

    # Classic rainbow
    console.banner("RAINBOW", font="banner", start_color="red", end_color="violet")
    console.text(f"{EMOJI.SPARKLES} All colors in perfect harmony", color="white", dim=True)
    console.newline(2)

    # Rainbow with different fonts
    console.banner("SPECTRUM", font="slant", start_color="orange", end_color="blue")
    console.text(f"{EMOJI.PALETTE} Full chromatic range", color="white", dim=True)
    console.newline(2)

    console.banner("COLORS", font="block", start_color="yellow", end_color="green")
    console.text(f"{EMOJI.GLOWING_STAR} Visual celebration", color="white", dim=True)
    console.newline(2)

    console.banner("PRISM", font="standard", start_color="cyan", end_color="magenta")
    console.text(f"{EMOJI.GEM_STONE} Light refracted into beauty", color="white", dim=True)
    console.newline(2)


def demo_diagonal_banners():
    """Diagonal gradient banners for dynamic energy."""
    console.rule(f"{EMOJI.LIGHTNING} DIAGONAL GRADIENTS", color="yellow")
    console.newline()

    console.text(
        "Diagonal color flows add motion and energy.\nTypography in dynamic transition.",
        color="yellow",
        italic=True,
    )
    console.newline()

    # Note: Diagonal gradients on banners would require special handling
    # For now, we demonstrate the concept with horizontal gradients
    console.banner("ENERGY", font="banner", start_color="yellow", end_color="red")
    console.text(f"{EMOJI.LIGHTNING} Power flowing through letters", color="white", dim=True)
    console.newline(2)

    console.banner("DYNAMIC", font="slant", start_color="cyan", end_color="magenta")
    console.text(f"{EMOJI.DIZZY} Cutting across the frame", color="white", dim=True)
    console.newline(2)

    console.banner("MOTION", font="big", start_color="blue", end_color="red")
    console.text(f"{EMOJI.ROCKET} Typography in flux", color="white", dim=True)
    console.newline(2)


def demo_themed_banners():
    """Banners designed for specific themes."""
    console.rule(f"{EMOJI.PALETTE} THEMED BANNERS", color="cyan")
    console.newline()

    # Success theme
    console.banner("SUCCESS", font="banner", start_color="lime", end_color="green")
    console.text(f"{EMOJI.CHECK} Celebrate achievements", color="green", bold=True)
    console.newline(2)

    # Warning theme
    console.banner("WARNING", font="standard", start_color="yellow", end_color="orange")
    console.text(f"{EMOJI.WARNING}  Proceed with caution", color="orange", bold=True)
    console.newline(2)

    # Error theme
    console.banner("ERROR", font="banner", start_color="orange", end_color="red")
    console.text(f"{EMOJI.CROSS} Critical attention required", color="red", bold=True)
    console.newline(2)

    # Info theme
    console.banner("INFO", font="standard", start_color="cyan", end_color="blue")
    console.text(f"{EMOJI.INFO}  Information available", color="cyan", bold=True)
    console.newline(2)

    # Tech theme
    console.banner("TECH", font="digital", start_color="cyan", end_color="purple")
    console.text(f"{EMOJI.COMPUTER} Digital excellence", color="magenta", bold=True)
    console.newline(2)


def demo_welcome_banners():
    """Application welcome screens."""
    console.rule(f"{EMOJI.WAVE} WELCOME SCREENS", color="magenta")
    console.newline()

    # Simple welcome
    console.banner("WELCOME", font="banner", start_color="red", end_color="violet")
    console.newline()
    console.text("StyledConsole v0.3.0", color="cyan", bold=True)
    console.text("Beautiful Terminal Output Made Easy", color="white", italic=True)
    console.newline(2)

    # Application launch
    console.banner("APP NAME", font="slant", start_color="cyan", end_color="purple")
    console.newline()
    console.frame(
        "Version: 1.0.0\n"
        "Environment: Production\n"
        "Started: 2025-11-12 10:30:45\n\n"
        f"{EMOJI.CHECK} All systems operational",
        title=f"{EMOJI.ROCKET} Launch Status",
        border="rounded",
        border_color="cyan",
        content_color="white",
        align="center",
        width=50,
    )
    console.newline(2)

    # Startup banner
    console.banner("SYSTEM", font="standard", start_color="green", end_color="cyan")
    console.text(f"{EMOJI.COMPUTER}  Initializing...", color="cyan", bold=True)
    console.newline(2)


def demo_creative_compositions():
    """Creative banner arrangements."""
    console.rule(f"{EMOJI.CIRCUS_TENT} CREATIVE COMPOSITIONS", color="yellow")
    console.newline()

    # Stacked banners
    console.banner("STYLED", font="banner", start_color="red", end_color="orange")
    console.banner("CONSOLE", font="banner", start_color="orange", end_color="yellow")
    console.text(f"{EMOJI.PALETTE} Stacked for visual impact", color="white", dim=True)
    console.newline(2)

    # Contrasting styles
    console.banner("BIG", font="big", start_color="cyan", end_color="cyan")
    console.banner("small", font="mini", start_color="magenta", end_color="magenta")
    console.text(
        f"{EMOJI.TRIANGULAR_RULER} Size contrast creates hierarchy", color="white", dim=True
    )
    console.newline(2)

    # Color progression
    console.banner("RED", font="standard", start_color="red", end_color="red")
    console.banner("ORANGE", font="standard", start_color="orange", end_color="orange")
    console.banner("YELLOW", font="standard", start_color="yellow", end_color="yellow")
    console.banner("GREEN", font="standard", start_color="green", end_color="green")
    console.text(f"{EMOJI.RAINBOW} Color progression tells a story", color="white", dim=True)
    console.newline(2)


def demo_banner_typography_art():
    """Banners as pure visual art."""
    console.rule(f"{EMOJI.ART}  TYPOGRAPHY AS ART", color="magenta")
    console.newline()

    # Art piece 1: The Elements
    console.text("═══════════ THE ELEMENTS ═══════════", color="cyan", bold=True)
    console.newline()
    console.banner("FIRE", font="banner", start_color="red", end_color="yellow")
    console.banner("WATER", font="slant", start_color="cyan", end_color="blue")
    console.banner("EARTH", font="standard", start_color="brown", end_color="green")
    console.banner("AIR", font="mini", start_color="white", end_color="cyan")
    console.newline(2)

    # Art piece 2: Day and Night
    console.text("═══════════ DAY & NIGHT ═══════════", color="yellow", bold=True)
    console.newline()
    console.banner("SUNRISE", font="slant", start_color="orange", end_color="yellow")
    console.banner("NOON", font="big", start_color="yellow", end_color="yellow")
    console.banner("SUNSET", font="slant", start_color="orange", end_color="purple")
    console.banner("MIDNIGHT", font="standard", start_color="darkblue", end_color="black")
    console.newline(2)

    # Art piece 3: Seasons
    console.text("═══════════ THE SEASONS ═══════════", color="green", bold=True)
    console.newline()
    console.banner("SPRING", font="standard", start_color="lime", end_color="green")
    console.banner("SUMMER", font="slant", start_color="yellow", end_color="orange")
    console.banner("AUTUMN", font="standard", start_color="orange", end_color="red")
    console.banner("WINTER", font="slant", start_color="cyan", end_color="blue")
    console.newline(2)


def demo_banner_best_practices():
    """Guidelines for effective banner usage."""
    console.rule(f"{EMOJI.BOOKS} BEST PRACTICES", color="cyan")
    console.newline()

    practices = [
        {
            "do": f"{EMOJI.CHECK} DO: Match Font to Context",
            "text": "• Standard/Banner for professional apps\n"
            "• Slant/Big for dynamic, modern apps\n"
            "• Digital for retro/tech themes\n"
            "• Block for bold statements",
        },
        {
            "do": f"{EMOJI.CHECK} DO: Use Color Purposefully",
            "text": "• Green gradients for success\n"
            "• Red gradients for errors\n"
            "• Blue gradients for information\n"
            "• Rainbow for celebrations",
        },
        {
            "do": f"{EMOJI.CHECK} DO: Consider Scale",
            "text": "• Big fonts for splash screens\n"
            "• Standard fonts for section headers\n"
            "• Mini fonts for subtle dividers\n"
            "• Match font size to importance",
        },
        {
            "do": f"{EMOJI.CROSS} DON'T: Overuse Banners",
            "text": "• One banner per section maximum\n"
            "• Too many banners = visual noise\n"
            "• Use for emphasis, not decoration\n"
            "• Reserve for important moments",
        },
        {
            "do": f"{EMOJI.CHECK} DO: Test Readability",
            "text": "• Some fonts work better than others\n"
            "• Test on different terminal sizes\n"
            "• Ensure sufficient contrast\n"
            "• Prioritize clarity over creativity",
        },
    ]

    for practice in practices:
        console.frame(
            practice["text"],
            title=practice["do"],
            border="rounded",
            border_color="cyan",
            content_color="white",
            align="left",
            width=70,
        )
        console.newline()

    console.newline()


def main():
    """Run the complete banners showcase."""
    console.banner("BANNERS", font="banner", start_color="red", end_color="violet")
    console.rule(f"{EMOJI.CIRCUS_TENT} TYPOGRAPHY SHOWCASE", color="magenta")
    console.newline()

    console.text(
        "A comprehensive exploration of ASCII art typography.\n"
        "From standard fonts to rainbow gradients,\n"
        "Discover the art of terminal typography.",
        color="cyan",
        italic=True,
    )
    console.newline(2)

    # Core demonstrations
    demo_standard_fonts()
    demo_decorative_fonts()
    demo_gradient_banners()
    demo_rainbow_banners()
    demo_diagonal_banners()

    # Practical applications
    demo_themed_banners()
    demo_welcome_banners()

    # Artistic explorations
    demo_creative_compositions()
    demo_banner_typography_art()
    demo_banner_best_practices()

    # Grand finale
    console.rule(f"{EMOJI.SPARKLES}", color="magenta")
    console.newline()
    console.banner("MASTERY", font="banner", start_color="red", end_color="violet")
    console.newline()
    console.frame(
        f"{EMOJI.PERFORMING_ARTS} TYPOGRAPHY MASTERY ACHIEVED\n\n"
        "You've explored:\n\n"
        f"{EMOJI.CHECK} 8+ font styles\n"
        f"{EMOJI.CHECK} Solid, gradient, and rainbow effects\n"
        f"{EMOJI.CHECK} Themed applications\n"
        f"{EMOJI.CHECK} Creative compositions\n"
        f"{EMOJI.CHECK} Typography as art form\n\n"
        "Banners are more than large text—\n"
        "They're the headlines of terminal interfaces,\n"
        "The first impressions that set the tone.\n\n"
        f"Now go forth and craft beautiful headers! {EMOJI.ROCKET}{EMOJI.SPARKLES}",
        title=f"{EMOJI.TROPHY} Gallery Complete",
        border="double",
        border_gradient_start="red",
        border_gradient_end="purple",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()


if __name__ == "__main__":
    main()
