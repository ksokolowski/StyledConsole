#!/usr/bin/env python3
"""
🌈 CSS4 Color Palette Showcase

A comprehensive visual demonstration of all 148 CSS4 named colors,
organized by color families with gradients and artistic presentations.

Design Philosophy:
- Colors are organized by hue families for visual harmony
- Gradients demonstrate smooth color transitions
- Each section tells a chromatic story
- Color theory meets practical application

Run: python examples/gallery/colors_showcase.py
"""

from styledconsole import Console

console = Console(record=True)


def demo_red_family():
    """RED FAMILY: Fire, passion, energy."""
    console.banner("REDS", font="standard", start_color="red", end_color="darkred")
    console.newline()

    reds = [
        "indianred",
        "lightcoral",
        "salmon",
        "darksalmon",
        "lightsalmon",
        "crimson",
        "red",
        "firebrick",
        "darkred",
    ]

    console.frame(
        "🔥 The color of fire and passion\n"
        "From delicate coral to deep crimson\n"
        "Red commands attention and stirs emotion",
        title="❤️  Red Spectrum",
        border="rounded",
        border_color="red",
        content_color="lightcoral",
        align="center",
        width=70,
    )
    console.newline()

    # Display reds in gradient frames
    for i, color in enumerate(reds):
        if i < len(reds) - 1:
            next_color = reds[i + 1]
            console.frame(
                f"Color: {color}\nRGB gradient to {next_color}",
                border="solid",
                border_gradient_start=color,
                border_gradient_end=next_color,
                content_color="white",
                align="center",
                width=60,
            )
        else:
            console.frame(
                f"Color: {color}\nThe deepest red",
                border="solid",
                border_color=color,
                content_color="white",
                align="center",
                width=60,
            )

    console.newline(2)


def demo_orange_family():
    """ORANGE FAMILY: Warmth, energy, creativity."""
    console.banner("ORANGES", font="standard", start_color="orange", end_color="darkorange")
    console.newline()

    console.frame(
        "🍊 The color of sunset and creativity\n"
        "Warm, inviting, and energetic\n"
        "Orange bridges red passion and yellow joy",
        title="🌅 Orange Spectrum",
        border="rounded",
        border_color="orange",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()

    # Create a gradient showcase
    console.frame(
        "Coral → Tomato → Orange Red → Dark Orange → Orange\n\n"
        "Watch the spectrum flow from soft coral\n"
        "Through vibrant tomato red\n"
        "To rich, saturated orange",
        border="thick",
        border_gradient_start="coral",
        border_gradient_end="orange",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_yellow_family():
    """YELLOW FAMILY: Joy, optimism, sunlight."""
    console.banner("YELLOWS", font="standard", start_color="yellow", end_color="gold")
    console.newline()

    yellows = [
        "gold",
        "yellow",
        "lightyellow",
        "lemonchiffon",
        "lightgoldenrodyellow",
        "papayawhip",
        "moccasin",
        "peachpuff",
        "palegoldenrod",
        "khaki",
        "darkkhaki",
    ]

    console.frame(
        "☀️  The color of sunlight and joy\n"
        "From pale lemon to deep gold\n"
        "Yellow illuminates and uplifts",
        title="🌟 Yellow Spectrum",
        border="rounded",
        border_color="gold",
        content_color="yellow",
        align="center",
        width=70,
    )
    console.newline()

    console.frame(
        "Gold ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Khaki\n\n"
        "11 shades of sunshine:\n"
        f"{' • '.join(yellows[:6])}\n"
        f"{' • '.join(yellows[6:])}\n\n"
        "Each shade tells a story of light",
        border="double",
        border_gradient_start="gold",
        border_gradient_end="khaki",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_green_family():
    """GREEN FAMILY: Nature, growth, harmony."""
    console.banner("GREENS", font="standard", start_color="lime", end_color="green")
    console.newline()

    console.frame(
        "🌿 The color of nature and renewal\n"
        "From electric lime to deep forest\n"
        "Green soothes, balances, and revitalizes",
        title="🍃 Green Spectrum",
        border="rounded",
        border_color="lime",
        content_color="lightgreen",
        align="center",
        width=70,
    )
    console.newline()

    # Gradient journey through greens
    console.frame(
        "A Walk Through the Forest:\n\n"
        "🌱 Lime ────→ Spring Green ────→ Forest Green ────→ Dark Green 🌲\n\n"
        "From new growth to ancient trees,\n"
        "The green spectrum encompasses\n"
        "The full cycle of natural life",
        border="heavy",
        border_gradient_start="lime",
        border_gradient_end="darkgreen",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_cyan_family():
    """CYAN FAMILY: Water, clarity, technology."""
    console.banner("CYANS", font="standard", start_color="cyan", end_color="darkcyan")
    console.newline()

    console.frame(
        "💧 The color of water and sky\nFrom pale aqua to deep ocean\nCyan refreshes and clarifies",
        title="🌊 Cyan Spectrum",
        border="rounded",
        border_color="cyan",
        content_color="lightcyan",
        align="center",
        width=70,
    )
    console.newline()

    console.frame(
        "Ocean Depths Gradient:\n\n"
        "Surface ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Deep\n\n"
        "Light Cyan → Turquoise → Steel Blue → Deep Sky Blue\n\n"
        "17 shades of aquatic beauty,\n"
        "Each capturing a different depth\n"
        "Of the digital ocean",
        border="thick",
        border_gradient_start="lightcyan",
        border_gradient_end="deepskyblue",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_blue_family():
    """BLUE FAMILY: Depth, trust, infinity."""
    console.banner("BLUES", font="standard", start_color="blue", end_color="darkblue")
    console.newline()

    blues = [
        "cornflowerblue",
        "royalblue",
        "blue",
        "mediumblue",
        "darkblue",
        "navy",
        "midnightblue",
    ]

    console.frame(
        "🌌 The color of depth and infinity\n"
        "From bright royal blue to midnight navy\n"
        "Blue inspires trust and contemplation",
        title="💙 Blue Spectrum",
        border="rounded",
        border_color="blue",
        content_color="cornflowerblue",
        align="center",
        width=70,
    )
    console.newline()

    # Show each blue with its character
    descriptions = [
        "Bright and regal, like a summer sky",
        "The king of blues, commanding yet elegant",
        "Pure blue, the standard bearer",
        "Deep and rich, ocean depths",
        "Dark mysteries, twilight blue",
        "Naval tradition, professional depth",
        "The darkest hour, before dawn breaks",
    ]

    for color, desc in zip(blues, descriptions):
        console.frame(
            f"{desc}",
            title=f"💎 {color.title()}",
            border="solid",
            border_color=color,
            content_color="white",
            align="center",
            width=60,
        )

    console.newline(2)


def demo_purple_family():
    """PURPLE FAMILY: Royalty, mystery, creativity."""
    console.banner("PURPLES", font="standard", start_color="purple", end_color="indigo")
    console.newline()

    console.frame(
        "👑 The color of royalty and mystery\n"
        "From delicate lavender to deep indigo\n"
        "Purple bridges earthly red and celestial blue",
        title="💜 Purple Spectrum",
        border="rounded",
        border_color="magenta",
        content_color="lavender",
        align="center",
        width=70,
    )
    console.newline()

    console.frame(
        "The Royal Gradient:\n\n"
        "Lavender ═══════════════════════════════════ Indigo\n\n"
        "16 shades of majesty:\n\n"
        "Light: Lavender, Thistle, Plum, Violet\n"
        "Vibrant: Orchid, Fuchsia, Magenta\n"
        "Deep: Purple, Dark Magenta, Indigo\n\n"
        "Each shade carries the weight\n"
        "Of artistic tradition and digital innovation",
        border="double",
        border_gradient_start="lavender",
        border_gradient_end="indigo",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_pink_family():
    """PINK FAMILY: Tenderness, romance, playfulness."""
    console.banner("PINKS", font="standard", start_color="pink", end_color="deeppink")
    console.newline()

    pinks = [
        "pink",
        "lightpink",
        "hotpink",
        "deeppink",
        "mediumvioletred",
        "palevioletred",
    ]

    console.frame(
        "🌸 The color of tenderness and joy\n"
        "From soft blush to vibrant hot pink\n"
        "Pink brings warmth and playfulness",
        title="💗 Pink Spectrum",
        border="rounded",
        border_color="hotpink",
        content_color="lightpink",
        align="center",
        width=70,
    )
    console.newline()

    console.frame(
        "Light Pink ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Deep Pink\n\n"
        "Six shades of affection:\n\n"
        f"{' • '.join(pinks)}\n\n"
        "From whispered sweet nothings\n"
        "To declarations of vibrant love",
        border="thick",
        border_gradient_start="lightpink",
        border_gradient_end="deeppink",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_brown_family():
    """BROWN FAMILY: Earth, stability, warmth."""
    console.banner("BROWNS", font="standard", start_color="tan", end_color="brown")
    console.newline()

    console.frame(
        "🏜️  The color of earth and stability\n"
        "From pale cornsilk to deep brown\n"
        "Browns ground us in natural warmth",
        title="🌰 Brown Spectrum",
        border="rounded",
        border_color="tan",
        content_color="wheat",
        align="center",
        width=70,
    )
    console.newline()

    console.frame(
        "Earth Tones Journey:\n\n"
        "Wheat → Sandy Brown → Peru → Chocolate → Brown\n\n"
        "17 shades of terrestrial beauty,\n"
        "Each carrying the essence\n"
        "Of wood, earth, and natural materials.\n\n"
        "From coffee cream to rich mahogany,\n"
        "Browns provide the foundation\n"
        "For warm, welcoming interfaces.",
        border="heavy",
        border_gradient_start="wheat",
        border_gradient_end="brown",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_white_gray_black():
    """NEUTRALS: The foundation of design."""
    console.banner("NEUTRALS", font="standard", start_color="white", end_color="black")
    console.newline()

    console.frame(
        "⚪ The spectrum from light to dark\n"
        "From pure white to absolute black\n"
        "Neutrals provide structure and balance",
        title="🎨 Neutral Spectrum",
        border="rounded",
        border_color="white",
        content_color="lightgray",
        align="center",
        width=70,
    )
    console.newline()

    console.frame(
        "The Grayscale Gradient:\n\n"
        "White ═══════════════════════════════════════ Black\n\n"
        "27 shades of neutral elegance:\n\n"
        "Light Whites: Snow, Honeydew, Mint Cream, Ghost White\n"
        "Off-Whites: Seashell, Beige, Old Lace, Ivory\n"
        "Light Grays: Gainsboro, Light Gray, Silver\n"
        "Mid Grays: Dark Gray, Gray, Dim Gray\n"
        "Dark Grays: Slate Gray, Dark Slate Gray\n"
        "Pure: White, Black\n\n"
        "The foundation upon which\n"
        "All other colors dance",
        border="double",
        border_gradient_start="white",
        border_gradient_end="dimgray",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_rainbow_spectrum():
    """The complete rainbow - all hues in harmony."""
    console.banner("RAINBOW", font="banner", start_color="red", end_color="violet")
    console.newline()

    console.frame(
        "🌈 THE COMPLETE SPECTRUM\n\n"
        "Red → Orange → Yellow → Green → Cyan → Blue → Purple\n\n"
        "148 CSS4 colors organized into chromatic families.\n"
        "Each color a note in the visual symphony.\n"
        "Together, they form the palette\n"
        "Of infinite terminal possibilities.",
        title="✨ Color Theory in Action",
        border="double",
        border_gradient_start="red",
        border_gradient_end="magenta",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_color_gradients():
    """Smooth gradient transitions between color families."""
    console.banner("GRADIENTS", font="standard", start_color="magenta", end_color="cyan")
    console.newline()

    gradients = [
        ("red", "orange", "Fire Sunset"),
        ("yellow", "lime", "Spring Dawn"),
        ("cyan", "blue", "Ocean Depths"),
        ("blue", "purple", "Twilight Sky"),
        ("magenta", "red", "Royal Passion"),
    ]

    for start, end, name in gradients:
        console.frame(
            f"Smooth transition from {start} to {end}\n\n"
            f"{'═' * 50}\n\n"
            "Watch as one color melts into another,\n"
            "Creating infinite intermediate shades.",
            title=f"🎨 {name}",
            border="thick",
            border_gradient_start=start,
            border_gradient_end=end,
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def main():
    """Run the complete colors showcase."""
    console.rule("🌈 CSS4 COLOR PALETTE SHOWCASE", color="magenta")
    console.newline()

    console.text(
        "A visual journey through all 148 CSS4 named colors.\n"
        "Organized by hue families for chromatic harmony.\n"
        "Each color tells a story. Each gradient sings a song.",
        color="cyan",
        italic=True,
    )
    console.newline(2)

    # Color family demonstrations
    demo_red_family()
    demo_orange_family()
    demo_yellow_family()
    demo_green_family()
    demo_cyan_family()
    demo_blue_family()
    demo_purple_family()
    demo_pink_family()
    demo_brown_family()
    demo_white_gray_black()

    # Artistic compositions
    demo_rainbow_spectrum()
    demo_color_gradients()

    # Finale
    console.rule("✨", color="magenta")
    console.newline()
    console.frame(
        "🎨 COLOR MASTERY ACHIEVED\n\n"
        "You've explored the complete CSS4 color palette:\n\n"
        "• 148 named colors\n"
        "• 9 chromatic families\n"
        "• Infinite gradient possibilities\n\n"
        "Now you hold the full spectrum\n"
        "In the palm of your terminal!\n\n"
        "Go forth and paint with pixels! 🖌️",
        title="🏆 Gallery Complete",
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
