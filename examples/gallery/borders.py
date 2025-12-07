#!/usr/bin/env python3
"""
🎨 Border Styles Visual Showcase

A creative demonstration of all 8 border styles with artistic layouts,
gradients, rainbow effects, and nested compositions.

Design Philosophy:
- Each border style tells a visual story
- Gradients enhance the perception of depth
- Nested frames create architectural beauty
- Color harmony guides the eye

Run: python examples/gallery/borders_showcase.py
"""

from styledconsole import Console, icons

# Initialize console with recording for potential HTML export
console = Console(record=True)


def demo_solid_borders():
    """SOLID: The Foundation - Clean, professional, timeless."""
    console.banner("SOLID", font="standard", start_color="blue", end_color="cyan")
    console.newline()

    console.frame(
        "The foundation of terminal aesthetics.\n"
        "Clean lines. Professional presence.\n"
        "Perfect for business applications.",
        title=f"{icons.TRIANGULAR_RULER} The Classic",
        border="solid",
        border_color="cyan",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Gradient variation
    console.frame(
        "With gradient borders, even simplicity\ntransforms into visual poetry.",
        title=f"{icons.WATER_WAVE} Gradient Flow",
        border="solid",
        border_color="cyan",
        content_color="cyan",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_rounded_borders():
    """ROUNDED: The Modern - Soft, friendly, approachable."""
    console.banner("ROUNDED", font="standard", start_color="green", end_color="lime")
    console.newline()

    console.frame(
        "Smooth curves welcome the eye,\n"
        "Like stones polished by gentle streams.\n"
        "Modern interfaces speak softly.",
        title=f"{icons.HERB} Gentle Curves",
        border="rounded",
        border_color="lime",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Rainbow rounded frame
    console.frame(
        "When rainbows dance on rounded edges,\n"
        "The terminal becomes a canvas\n"
        "Where technology meets art.",
        title=f"{icons.RAINBOW} Rainbow Dreams",
        border="rounded",
        border_color="red",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_double_borders():
    """DOUBLE: The Emphasis - Strong, authoritative, important."""
    console.banner("DOUBLE", font="standard", start_color="yellow", end_color="orange")
    console.newline()

    console.frame(
        "⚠️  ATTENTION\n\n"
        "Double lines command respect.\n"
        "They frame what matters most,\n"
        "Drawing focus with geometric precision.",
        title=f"{icons.HIGH_VOLTAGE} The Emphasis",
        border="double",
        border_color="orange",
        content_color="yellow",
        align="center",
        width=60,
    )
    console.newline()

    # Gradient double frame
    console.frame(
        "Critical systems demand clarity.\n"
        "Important messages deserve distinction.\n"
        "Double borders deliver both.",
        title=f"{icons.FIRE} High Priority",
        border="double",
        border_color="orange",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_thick_borders():
    """THICK: The Bold - Strong, impactful, unmissable."""
    console.banner("THICK", font="standard", start_color="magenta", end_color="purple")
    console.newline()

    console.frame(
        f"{icons.FIREWORKS} BOLD STATEMENTS\n\n"
        "Thick borders make bold statements.\n"
        "They don't whisper—they proclaim.\n"
        "Perfect for headlines that demand attention.",
        title=f"{icons.MUSCLE} The Bold",
        border="thick",
        border_color="magenta",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Vibrant gradient
    console.frame(
        "Energy radiates from these borders,\n"
        "Pulsing with digital vitality.\n"
        "Your message becomes unmissable.",
        title=f"{icons.HIGH_VOLTAGE} Electric Energy",
        border="thick",
        border_color="magenta",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_heavy_borders():
    """HEAVY: The Fortress - Solid, protected, secure."""
    console.banner("HEAVY", font="standard", start_color="blue", end_color="purple")
    console.newline()

    console.frame(
        f"{icons.SHIELD} FORTIFIED\n\n"
        "Heavy borders build fortresses.\n"
        "They protect and contain,\n"
        "Creating sanctuaries of information.",
        title=f"{icons.CASTLE} The Fortress",
        border="heavy",
        border_color="blue",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Nested heavy frames - demonstrating content with security theme
    protected_content = f"""Security through layers:

{icons.LOCKED} Protected Zone
Data encrypted
Access controlled"""

    console.frame(
        protected_content,
        title=f"{icons.LOCKED} Secure Container",
        border="heavy",
        border_color="blue",
        content_color="cyan",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_minimal_borders():
    """MINIMAL: The Subtle - Light, airy, spacious."""
    console.banner("MINIMAL", font="standard", start_color="white", end_color="cyan")
    console.newline()

    console.frame(
        "Whispers on the terminal canvas,\n"
        "Light touches that organize without overwhelming.\n"
        "Minimalism is the ultimate sophistication.",
        title=f"{icons.CHERRY_BLOSSOM} Light Touch",
        border="minimal",
        border_color="cyan",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Delicate gradient
    console.frame(
        "Like morning mist on a meadow,\n"
        "These borders suggest rather than insist,\n"
        "Guiding the eye with gentle grace.",
        title=f"{icons.BUTTERFLY} Delicate Beauty",
        border="minimal",
        border_color="cyan",
        content_color="cyan",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_ascii_borders():
    """ASCII: The Universal - Compatible, classic, reliable."""
    console.banner("ASCII", font="standard", start_color="green", end_color="yellow")
    console.newline()

    console.frame(
        "Where Unicode cannot tread,\n"
        "ASCII borders carry the torch.\n"
        "Universal compatibility, timeless simplicity.",
        title=f"{icons.GLOBE_SHOWING_EUROPE_AFRICA} Universal",
        border="ascii",
        border_color="green",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    console.frame(
        "From the earliest terminals to modern shells,\n"
        "These characters bridge generations.\n"
        "The lingua franca of text interfaces.",
        title=f"{icons.KEYBOARD} Retro Charm",
        border="ascii",
        border_color="green",
        content_color="lime",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_dashed_borders():
    """DOTS: The Dynamic - Energetic, modern, flowing."""
    console.banner("DOTS", font="standard", start_color="yellow", end_color="orange")
    console.newline()

    console.frame(
        "Motion frozen in ASCII art,\n"
        "Dashed lines pulse with energy.\n"
        "Perfect for temporary states and transitions.",
        title=f"{icons.HIGH_VOLTAGE} Dynamic Flow",
        border="dots",
        border_color="yellow",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Rainbow dashed
    console.frame(
        "Imagine electricity flowing through these lines,\n"
        "Each dash a spark in the digital void.\n"
        "Energy visualized, motion suggested.",
        title=f"{icons.GLOWING_STAR} Electric Dreams",
        border="dots",
        border_color="yellow",
        content_color="orange",
        align="center",
        width=60,
    )
    console.newline(2)


def demo_nested_composition():
    """The Art of Nesting - Real-world dashboard example."""
    console.banner("NESTED FRAMES", font="banner", start_color="cyan", end_color="purple")
    console.newline()

    console.text(
        f"{icons.CLASSICAL_BUILDING} Simulating a system monitoring dashboard "
        "with nested information panels",
        color="cyan",
        bold=True,
    )
    console.newline()

    # CPU Metrics - Inner frame 1 (rounded border, green)
    cpu_content = f"""{icons.CHART_INCREASING} CPU METRICS

Usage: 67% (Normal)
Temperature: 58°C
Cores: 8 active
Threads: 16 running"""

    console.frame(
        cpu_content,
        title=f"{icons.DESKTOP_COMPUTER} CPU Status",
        border="rounded",
        border_color="green",
        content_color="bright_green",
        width=35,
    )
    console.newline()

    # Memory Metrics - Inner frame 2 (rounded border, yellow)
    memory_content = f"""{icons.FLOPPY_DISK} MEMORY STATUS

RAM: 12.4 GB / 16 GB
Swap: 2.1 GB / 8 GB
Cache: 3.2 GB
Available: 3.6 GB"""

    console.frame(
        memory_content,
        title=f"{icons.FLOPPY_DISK} Memory Status",
        border="rounded",
        border_color="yellow",
        content_color="bright_yellow",
        width=35,
    )
    console.newline()

    # Network Activity - Inner frame 3 (rounded border, cyan)
    network_content = f"""{icons.SATELLITE_ANTENNA} NETWORK ACTIVITY

Download: 5.2 MB/s
Upload: 1.8 MB/s
Latency: 12ms
Packets: 45,231 sent"""

    console.frame(
        network_content,
        title=f"{icons.GLOBE_WITH_MERIDIANS} Network Status",
        border="rounded",
        border_color="cyan",
        content_color="bright_cyan",
        width=35,
    )

    console.newline(2)
    console.text(
        f"{icons.LIGHT_BULB} Note: True nested frames (frames within frames) "
        "require rich.Panel composition.\n"
        "This example shows multiple independent frames that could logically "
        "be grouped.\n"
        f"{icons.CONSTRUCTION} Future Console API improvement: console.group() "
        "to visually nest frames.",
        color="yellow",
        italic=True,
    )
    console.newline(2)


def demo_rainbow_gallery():
    """The Rainbow Collection - All borders in spectral glory."""
    console.banner("RAINBOW GALLERY", font="banner", start_color="red", end_color="purple")
    console.newline()

    borders = ["solid", "rounded", "double", "thick", "heavy", "minimal", "ascii", "dots"]
    colors = [
        ("red", "orange"),
        ("orange", "yellow"),
        ("yellow", "lime"),
        ("lime", "cyan"),
        ("cyan", "blue"),
        ("blue", "purple"),
        ("purple", "magenta"),
        ("magenta", "red"),
    ]

    for border, color_pair in zip(borders, colors, strict=False):
        console.frame(
            f"{icons.RAINBOW} {border.upper()} in rainbow gradients\n"
            f"Where color meets structure,\n"
            f"Art emerges from code.",
            title=f"{icons.SPARKLES} {border.title()}",
            border=border,
            border_color=color_pair[0],  # Use first color from tuple
            content_color="white",
            align="center",
            width=50,
        )
        console.newline()

    console.newline()


def demo_comparison_grid():
    """Side-by-side comparison of all border styles."""
    console.banner("COMPARISON", font="standard", start_color="white", end_color="cyan")
    console.newline()

    console.text("All 8 border styles at a glance:", color="cyan", bold=True)
    console.newline()

    # Demonstrate each border style with actual frames
    border_styles = [
        ("solid", "cyan"),
        ("rounded", "lime"),
        ("double", "yellow"),
        ("thick", "magenta"),
        ("heavy", "blue"),
        ("minimal", "cyan"),
        ("ascii", "green"),
        ("dots", "orange"),
    ]

    for border_name, border_color in border_styles:
        console.frame(
            f"This is the {border_name.upper()} border style",
            title=f"{icons.SPARKLES} {border_name.title()}",
            border=border_name,
            border_color=border_color,
            content_color="white",
            width=45,
        )
        console.newline()

    console.newline()


def main():
    """Run the complete borders showcase."""
    console.rule(f"{icons.ARTIST_PALETTE} BORDER STYLES GALLERY", color="magenta")
    console.newline()

    console.text(
        "A visual journey through the 8 border styles of StyledConsole.\n"
        "Each border tells a story. Each gradient adds emotion.\n"
        "Together, they form the vocabulary of terminal aesthetics.",
        color="cyan",
        italic=True,
    )
    console.newline(2)

    # Individual style demonstrations
    demo_solid_borders()
    demo_rounded_borders()
    demo_double_borders()
    demo_thick_borders()
    demo_heavy_borders()
    demo_minimal_borders()
    demo_ascii_borders()
    demo_dashed_borders()

    # Artistic compositions
    demo_nested_composition()
    demo_rainbow_gallery()
    demo_comparison_grid()

    # Finale
    console.rule(f"{icons.SPARKLES}", color="magenta")
    console.newline()
    console.frame(
        f"{icons.ARTIST_PALETTE} BORDER MASTERY ACHIEVED\n\n"
        "You've witnessed the full spectrum of border aesthetics.\n"
        "From solid foundations to dashed energy,\n"
        "From minimal whispers to heavy fortresses.\n\n"
        "Now go forth and frame your terminal with beauty!",
        title=f"{icons.TROPHY} Gallery Complete",
        border="double",
        border_color="magenta",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()


if __name__ == "__main__":
    main()
