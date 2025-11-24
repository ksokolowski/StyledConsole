#!/usr/bin/env python3
"""
🌈 Gradient Effects Masterclass

A comprehensive showcase of gradient capabilities in StyledConsole,
from simple two-color gradients to complex rainbow effects.

Design Philosophy:
- Gradients add depth and visual interest
- Color transitions tell emotional stories
- Diagonal gradients create dynamic energy
- Rainbows celebrate the full spectrum

Run: python examples/gallery/gradients_showcase.py
"""

from styledconsole import EMOJI, Console
from styledconsole.effects import diagonal_gradient_frame, rainbow_frame

console = Console(record=True)


def demo_horizontal_gradients():
    """Horizontal gradients - smooth left-to-right transitions."""
    console.banner("HORIZONTAL", font="standard", start_color="cyan", end_color="blue")
    console.newline()

    console.text(
        "Horizontal gradients flow like rivers across the frame.", color="cyan", italic=True
    )
    console.newline()

    # Simple two-color gradients
    gradients = [
        (("red", "orange"), f"{EMOJI.FIRE} Fire", "From ember to flame"),
        (("blue", "cyan"), f"{EMOJI.OCEAN} Ocean", "From deep sea to shallow waters"),
        (("purple", "magenta"), f"{EMOJI.CROWN} Royalty", "From twilight to dawn"),
        (("green", "lime"), f"{EMOJI.HERB} Forest", "From shadow to sunlight"),
        (("yellow", "orange"), f"{EMOJI.SUNRISE} Sunset", "From noon to dusk"),
    ]

    for colors, title, desc in gradients:
        console.frame(
            f"{desc}\n\n"
            f"{'═' * 50}\n\n"
            f"Color journey: {colors[0]} → {colors[1]}\n"
            "Smooth interpolation across horizontal space",
            title=title,
            border="rounded",
            border_gradient_start=colors[0],
            border_gradient_end=colors[1],
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def demo_vertical_gradients():
    """Vertical gradients - top-to-bottom color flows."""
    console.banner("VERTICAL", font="standard", start_color="purple", end_color="blue")
    console.newline()

    console.text(
        "Vertical gradients rise and fall like the sun's journey.",
        italic=True,
        color="magenta",
    )
    console.newline()

    # Note: Current implementation uses horizontal gradients
    # This demonstrates the visual concept with border colors
    console.frame(
        f"{EMOJI.DIZZY} DAWN TO DUSK\n\n"
        "Imagine colors flowing vertically:\n\n"
        "Top: Dark purple (midnight)\n"
        "↓\n"
        "Middle: Blue (morning)\n"
        "↓\n"
        "Bottom: Cyan (noon)\n\n"
        "Vertical gradients create\n"
        "The illusion of depth and elevation",
        title=f"{EMOJI.MILKY_WAY} Vertical Flow",
        border="thick",
        border_gradient_start="purple",
        border_gradient_end="cyan",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline(2)


def demo_diagonal_gradients():
    """Diagonal gradient frames."""
    console.banner("DIAGONAL", font="standard", start_color="red", end_color="blue")
    console.newline()

    console.text(
        "Diagonal gradients add motion and energy, slicing across frames with purpose.",
        color="yellow",
        italic=True,
    )
    console.newline()

    # Create diagonal gradient frames with effects module
    lines = diagonal_gradient_frame(
        f"{EMOJI.LIGHTNING} ELECTRIC ENERGY\n\n"
        "From top-left cyan to bottom-right magenta,\n"
        "The gradient cuts across the frame\n"
        "Like lightning through a storm.\n\n"
        "Dynamic. Energetic. Unstoppable.",
        title=f"{EMOJI.LIGHTNING} Power Flow",
        start_color="cyan",
        end_color="magenta",
        border="thick",
        width=70,
        align="center",
    )
    for line in lines:
        print(line)
    console.newline()

    lines = diagonal_gradient_frame(
        f"{EMOJI.WATER_WAVE} OCEAN WAVES\n\n"
        "Blue depths in the corner\n"
        "Rising to cyan shallows\n"
        "Across the diagonal tide.\n\n"
        "Watch the waves flow\n"
        "From deep to light.",
        title=f"{EMOJI.WATER_WAVE} Tidal Flow",
        start_color="darkblue",
        end_color="cyan",
        border="rounded",
        width=70,
        align="center",
    )
    for line in lines:
        print(line)
    console.newline()

    lines = diagonal_gradient_frame(
        f"{EMOJI.FIRE} SUNSET DIAGONAL\n\n"
        "Red in the upper corner,\n"
        "Flowing through orange and yellow,\n"
        "To golden amber below.\n\n"
        "The sun sets diagonally\n"
        "Across the terminal sky.",
        title=f"{EMOJI.SUNRISE} Diagonal Sunset",
        start_color="red",
        end_color="orange",
        border="double",
        width=70,
        align="center",
    )
    for line in lines:
        print(line)
    console.newline(2)


def demo_rainbow_effects():
    """Rainbow gradients - full spectrum glory."""
    console.banner("RAINBOW", font="banner", start_color="red", end_color="violet")
    console.newline()

    console.text(
        "Rainbow gradients celebrate the complete color spectrum,\n"
        "Painting terminals with all the colors of light itself.",
        color="magenta",
        italic=True,
    )
    console.newline()

    # Simple rainbow frame
    lines = rainbow_frame(
        f"{EMOJI.RAINBOW} FULL SPECTRUM BEAUTY\n\n"
        "Red → Orange → Yellow → Green → Blue → Indigo → Violet\n\n"
        "Seven colors, infinite variations.\n"
        "The rainbow is nature's gradient,\n"
        "Now available in your terminal!",
        title=f"{EMOJI.SPARKLES} Rainbow Classic",
        border="rounded",
        width=70,
        align="center",
    )
    for line in lines:
        print(line)
    console.newline()

    # Rainbow with different content
    lines = rainbow_frame(
        f"{EMOJI.PALETTE} CHROMATIC CELEBRATION\n\n"
        "Every wavelength of visible light\n"
        "Compressed into terminal art.\n\n"
        "From 650nm (red) to 450nm (blue),\n"
        "Science and beauty unite\n"
        "In prismatic perfection.",
        title=f"{EMOJI.MICROSCOPE} Physics of Color",
        border="thick",
        width=70,
        align="center",
    )
    for line in lines:
        print(line)
    console.newline()

    # Rainbow poetry
    lines = rainbow_frame(
        "When sunlight hits the rain,\n"
        "When terminal meets art,\n"
        "When code displays emotion—\n\n"
        "Rainbows are born.\n\n"
        "Not just color transitions,\n"
        "But visual poetry,\n"
        "Dancing across the screen\n"
        "In perfect chromatic harmony.",
        title=f"{EMOJI.GLOWING_STAR} Rainbow Poetry",
        border="double",
        width=70,
        align="center",
    )
    for line in lines:
        print(line)
    console.newline(2)


def demo_multicolor_gradients():
    """Multi-stop gradients - complex color journeys."""
    console.banner("MULTI-COLOR", font="standard", start_color="red", end_color="yellow")
    console.newline()

    console.text(
        "Multi-color gradients flow through multiple hues,\nCreating rich, complex transitions.",
        color="cyan",
        italic=True,
    )
    console.newline()

    # Three-color gradients (Simplified to 2-color for v0.3.0 API)
    three_color = [
        ("red", "green", f"{EMOJI.RAINBOW} Warm to Cool", "Fire → Forest"),
        ("purple", "red", f"{EMOJI.PURPLE_HEART} Royal Passion", "Twilight → Flame"),
        ("cyan", "purple", f"{EMOJI.MILKY_WAY} Deep Space", "Sky → Cosmos"),
        ("lime", "blue", f"{EMOJI.WATER_WAVE} Tropical Waters", "Shallows → Abyss"),
    ]

    for start, end, title, desc in three_color:
        console.frame(
            f"{desc}\n\n"
            f"{'═' * 50}\n\n"
            f"Gradient journey:\n"
            f"{start} → {end}\n\n"
            "Each transition smooth and intentional,\n"
            "Building a complete visual narrative",
            title=title,
            border="rounded",
            border_gradient_start=start,
            border_gradient_end=end,
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def demo_gradient_poetry():
    """Gradients as emotional expression."""
    console.banner("GRADIENT POETRY", font="standard", start_color="purple", end_color="cyan")
    console.newline()

    poems = [
        {
            "title": f"{EMOJI.SUNRISE} Dawn",
            "start": "darkblue",
            "end": "yellow",
            "text": "In the darkest blue of night,\n"
            "Orange whispers of coming light.\n"
            "Then yellow bursts with joyful might—\n"
            "Dawn breaks, and shadows take their flight.",
        },
        {
            "title": f"{EMOJI.WATER_WAVE} Ocean Deep",
            "start": "cyan",
            "end": "darkblue",
            "text": "Surface sparkles, cyan bright,\n"
            "Deeper down, the blue takes flight.\n"
            "Darkest depths, beyond the light—\n"
            "Ocean's secrets, hidden from sight.",
        },
        {
            "title": f"{EMOJI.FIRE} Fire's Dance",
            "start": "red",
            "end": "yellow",
            "text": "Red coals glow with ancient heat,\n"
            "Orange flames leap, light and fleet.\n"
            "Yellow tips where fire and air meet—\n"
            "Dancing light, wild and sweet.",
        },
        {
            "title": f"{EMOJI.BLOSSOM} Spring Bloom",
            "start": "green",
            "end": "yellow",
            "text": "Green shoots push through winter's hold,\n"
            "Lime leaves unfurl, bright and bold.\n"
            "Yellow blooms, stories untold—\n"
            "Spring's gradient of life unfolds.",
        },
    ]

    for poem in poems:
        console.frame(
            poem["text"],
            title=poem["title"],
            border="double",
            border_gradient_start=poem["start"],
            border_gradient_end=poem["end"],
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def demo_gradient_applications():
    """Practical applications of gradients in UIs."""
    console.banner("APPLICATIONS", font="standard", start_color="cyan", end_color="purple")
    console.newline()

    console.text(
        "Gradients aren't just beautiful—they're functional.\n"
        "Here's how to use them effectively in your terminal UIs:",
        color="magenta",
        italic=True,
    )
    console.newline()

    applications = [
        {
            "title": f"{EMOJI.CHECK} Success Indicators",
            "start": "lime",
            "end": "green",
            "text": "Use green gradients for success messages.\n"
            "Light to dark suggests completion and stability.\n\n"
            "Perfect for: Deployments, tests passed, operations complete",
        },
        {
            "title": f"{EMOJI.WARNING}  Warning States",
            "start": "yellow",
            "end": "orange",
            "text": "Yellow-to-orange gradients grab attention\n"
            "Without the alarm of pure red.\n\n"
            "Perfect for: Deprecation notices, resource warnings, caution states",
        },
        {
            "title": f"{EMOJI.CROSS} Error Messages",
            "start": "orange",
            "end": "red",
            "text": "Red gradients signal critical issues.\n"
            "Dark red adds severity and urgency.\n\n"
            "Perfect for: Build failures, critical errors, system alerts",
        },
        {
            "title": f"{EMOJI.INFO}  Information",
            "start": "cyan",
            "end": "blue",
            "text": "Blue gradients convey trust and calm.\n"
            "Cyan to blue suggests depth of information.\n\n"
            "Perfect for: Documentation, help text, status updates",
        },
        {
            "title": f"{EMOJI.LIGHTNING} Progress Indicators",
            "start": "yellow",
            "end": "green",
            "text": "Multi-color gradients show progression.\n"
            "Watch the color shift as completion nears.\n\n"
            "Perfect for: Build pipelines, downloads, processing steps",
        },
    ]

    for app in applications:
        console.frame(
            app["text"],
            title=app["title"],
            border="rounded",
            border_gradient_start=app["start"],
            border_gradient_end=app["end"],
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def demo_gradient_best_practices():
    """Design guidelines for using gradients effectively."""
    console.banner("BEST PRACTICES", font="standard", start_color="magenta", end_color="cyan")
    console.newline()

    practices = [
        {
            "title": f"{EMOJI.SPARKLES} Rule 1: Keep It Smooth",
            "start": "blue",
            "end": "cyan",
            "text": f"{EMOJI.CHECK} DO: Use adjacent colors on the spectrum.\n"
            "Blue → Cyan creates smooth transitions.\n\n"
            f"{EMOJI.CROSS} DON'T: Jump across the spectrum randomly.\n"
            "Red → Cyan can look muddy in the middle.",
        },
        {
            "title": f"{EMOJI.PALETTE} Rule 2: Match the Mood",
            "start": "darkblue",
            "end": "purple",
            "text": f"{EMOJI.CHECK} DO: Choose colors that support your message.\n"
            "Dark blue → Purple for serious, professional content.\n\n"
            f"{EMOJI.CROSS} DON'T: Use cheerful colors for errors.\n"
            "Rainbow gradients on error messages confuse users.",
        },
        {
            "title": f"{EMOJI.TRIANGULAR_RULER} Rule 3: Mind the Length",
            "start": "green",
            "end": "lime",
            "text": f"{EMOJI.CHECK} DO: Use longer gradients for wide frames.\n"
            "Gives colors room to transition smoothly.\n\n"
            f"{EMOJI.CROSS} DON'T: Cram many colors into tiny frames.\n"
            "You'll lose the gradient effect entirely.",
        },
        {
            "title": "⚖️  Rule 4: Balance Saturation",
            "start": "cyan",
            "end": "blue",
            "text": f"{EMOJI.CHECK} DO: Keep saturation levels similar.\n"
            "Cyan and blue have similar intensity.\n\n"
            f"{EMOJI.CROSS} DON'T: Mix pale and vivid colors randomly.\n"
            "Lavender → Hot Pink creates jarring transitions.",
        },
        {
            "title": f"{EMOJI.TARGET} Rule 5: Purpose Over Pretty",
            "start": "lime",
            "end": "green",
            "text": f"{EMOJI.CHECK} DO: Use gradients to enhance meaning.\n"
            "Green gradient reinforces success message.\n\n"
            f"{EMOJI.CROSS} DON'T: Add gradients just because.\n"
            "Every visual choice should serve a purpose.",
        },
    ]

    for practice in practices:
        console.frame(
            practice["text"],
            title=practice["title"],
            border="thick",
            border_gradient_start=practice["start"],
            border_gradient_end=practice["end"],
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def demo_gradient_masterpiece():
    """A complex gradient composition - the grand finale."""
    console.banner("MASTERPIECE", font="banner", start_color="red", end_color="violet")
    console.newline()

    # Diagonal rainbow gradient frame
    diagonal_gradient_frame(
        f"{EMOJI.PALETTE} THE ART OF GRADIENTS\n\n"
        "You've journeyed through the spectrum:\n\n"
        "• Horizontal flows like rivers\n"
        "• Vertical rises like dawn\n"
        "• Diagonals slice like lightning\n"
        "• Rainbows celebrate completeness\n"
        "• Multi-colors tell stories\n\n"
        "Gradients are more than color transitions—\n"
        "They're emotional journeys,\n"
        "Visual narratives,\n"
        "Terminal poetry.\n\n"
        "Now you hold the spectrum's power.\n"
        f"Paint your terminals with light! {EMOJI.SPARKLES}",
        title=f"{EMOJI.RAINBOW} Gradient Mastery",
        start_color="purple",
        end_color="cyan",
        border="double",
        width=70,
        align="center",
    )
    console.newline()

    # Nested gradient composition
    # 1. Create the innermost frame (Soul)
    soul_frame = console.render_frame(
        "Purple → Magenta (Soul)\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔",
        border="ascii",
        content_color="magenta",
        border_color="magenta",
        align="center",
        width=30,
    )

    # 2. Create the next layer (Depth)
    depth_frame = console.render_frame(
        ["Cyan → Blue (Depth frame)", "", soul_frame],
        border="thick",
        border_gradient_start="cyan",
        border_gradient_end="blue",
        align="center",
        width=40,
    )

    # 3. Create the next layer (Growth)
    growth_frame = console.render_frame(
        ["Yellow → Green (Growth frame)", "", depth_frame],
        border="rounded",
        border_gradient_start="yellow",
        border_gradient_end="green",
        align="center",
        width=50,
    )

    # 4. Create the outer layer (Fire)
    fire_frame = console.render_frame(
        ["Red → Orange (Fire frame)", "", growth_frame],
        border="solid",
        border_gradient_start="red",
        border_gradient_end="orange1",
        align="center",
        width=60,
    )

    # 5. Create the header frame
    header_frame = console.render_frame(
        f"{EMOJI.RAINBOW} NESTED GRADIENT ARCHITECTURE\n(Native Implementation)",
        border="double",
        border_gradient_start="purple",
        border_gradient_end="blue",
        align="center",
        width=60,
    )

    # 6. Final assembly
    console.frame(
        [
            header_frame,
            "",
            fire_frame,
            "",
            "Four gradient layers, each with meaning:",
            "Fire → Growth → Depth → Soul",
            "",
            "This is gradient architecture at its finest.",
        ],
        title=f"{EMOJI.CLASSICAL_BUILDING}  Gradient Architecture",
        border="heavy",
        border_gradient_start="red",
        border_gradient_end="magenta",
        content_color="white",
        align="center",
        width=80,
    )
    console.newline(2)


def main():
    """Run the complete gradients showcase."""
    console.rule(f"{EMOJI.RAINBOW} GRADIENT EFFECTS MASTERCLASS", color="magenta")
    console.newline()

    console.text(
        "A comprehensive exploration of gradient capabilities.\n"
        "From simple two-color transitions to complex rainbow effects.\n"
        "Master the art of color flow in terminal interfaces.",
        color="cyan",
        italic=True,
    )
    console.newline(2)

    # Core gradient demonstrations
    demo_horizontal_gradients()
    demo_vertical_gradients()
    demo_diagonal_gradients()
    demo_rainbow_effects()
    demo_multicolor_gradients()

    # Artistic and practical applications
    demo_gradient_poetry()
    demo_gradient_applications()
    demo_gradient_best_practices()
    demo_gradient_masterpiece()

    # Finale
    console.rule(f"{EMOJI.SPARKLES}", color="magenta")
    console.newline()
    console.frame(
        f"{EMOJI.PALETTE} GRADIENT MASTERY ACHIEVED\n\n"
        "You've explored:\n\n"
        f"{EMOJI.CHECK} Horizontal, vertical, and diagonal gradients\n"
        f"{EMOJI.CHECK} Rainbow and multi-color effects\n"
        f"{EMOJI.CHECK} Gradient poetry and emotional expression\n"
        f"{EMOJI.CHECK} Practical UI applications\n"
        f"{EMOJI.CHECK} Design best practices\n\n"
        "Gradients transform flat interfaces\n"
        "Into dimensional experiences.\n\n"
        f"Now go paint your terminal with light! {EMOJI.RAINBOW}{EMOJI.SPARKLES}",
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
