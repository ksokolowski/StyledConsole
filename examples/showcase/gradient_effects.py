"""Gradient Effects Showcase - Beautiful gradients and rainbow effects.

This example demonstrates the gradient effects available in StyledConsole:
- Vertical gradients (content and borders)
- Diagonal gradients (top-left to bottom-right)
- Rainbow effects (7-color spectrum)
"""

from styledconsole import Console, diagonal_gradient_frame, gradient_frame, rainbow_frame


def main():
    """Run gradient effects showcase."""
    console = Console()

    # Header - showcasing rainbow effect
    print()
    header_lines = rainbow_frame(
        [
            "✨ GRADIENT EFFECTS SHOWCASE ✨",
            "Beautiful gradients for StyledConsole",
        ],
        mode="both",
        border="double",
        width=57,
    )
    for line in header_lines:
        print(line)
    print()

    # Section 1: Basic Vertical Gradients
    console.text("1️⃣  VERTICAL GRADIENTS", color="cyan", bold=True)
    print("-" * 80)

    # Content gradient
    lines = gradient_frame(
        ["Gradient flows from top to bottom", "Start color: Red", "End color: Blue"],
        title="🌈 Content Gradient",
        start_color="red",
        end_color="blue",
        target="content",
        border="rounded",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Border gradient
    lines = gradient_frame(
        ["Plain content here", "But borders have gradient!", "From cyan to magenta"],
        title="🎨 Border Gradient",
        start_color="cyan",
        end_color="magenta",
        target="border",
        border="double",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Both gradient
    lines = gradient_frame(
        ["Everything gradients!", "Content AND borders", "Full color experience"],
        title="💎 Content + Border",
        start_color="lime",
        end_color="purple",
        target="both",
        border="heavy",
        width=50,
    )
    for line in lines:
        print(line)
    print()
    print()

    # Section 2: Diagonal Gradients
    console.text("2️⃣  DIAGONAL GRADIENTS (Top-Left → Bottom-Right)", color="magenta", bold=True)
    print("-" * 80)

    # Diagonal content
    lines = diagonal_gradient_frame(
        [
            "Top-left: RED 🔴",
            "Center: PURPLE 🟣",
            "Bottom-right: BLUE 🔵",
            "Diagonal flow!",
        ],
        title="↘ Diagonal Flow",
        start_color="red",
        end_color="blue",
        target="content",
        border="rounded",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Diagonal border
    lines = diagonal_gradient_frame(
        ["Plain content", "Check the borders!", "Diagonal gradient on borders"],
        title="↘ Diagonal Borders",
        start_color="orange",
        end_color="teal",
        target="border",
        border="solid",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Diagonal both
    lines = diagonal_gradient_frame(
        [
            "Everything flows diagonally",
            "From top-left corner",
            "To bottom-right corner",
            "Stunning effect! ✨",
        ],
        title="↘ Full Diagonal",
        start_color="lime",
        end_color="magenta",
        target="both",
        border="heavy",
        width=50,
    )
    for line in lines:
        print(line)
    print()
    print()

    # Section 3: Rainbow Effects
    console.text("3️⃣  RAINBOW EFFECTS (7-Color Spectrum)", color="yellow", bold=True)
    print("-" * 80)

    # Rainbow content
    lines = rainbow_frame(
        [
            "🔴 Red",
            "🟠 Orange",
            "🟡 Yellow",
            "🟢 Green",
            "🔵 Blue",
            "🟣 Indigo",
            "🟣 Violet",
        ],
        title="🌈 Rainbow Content",
        mode="content",
        border="rounded",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Rainbow border
    lines = rainbow_frame(
        ["Plain content", "But look at the borders!", "Full rainbow spectrum 🌈"],
        title="🎨 Rainbow Borders",
        mode="border",
        border="double",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Rainbow both
    lines = rainbow_frame(
        [
            "Ultimate rainbow!",
            "Content: Rainbow gradient",
            "Borders: Rainbow gradient",
            "Double rainbow effect! 🌈🌈",
        ],
        title="🌈 DOUBLE RAINBOW 🌈",
        direction="vertical",
        mode="both",
        border="heavy",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Diagonal rainbow
    lines = rainbow_frame(
        [
            "🌈 Top-left: RED corner",
            "🌈 Center: GREEN middle",
            "🌈 Bottom-right: VIOLET",
            "🌈 Diagonal rainbow flow!",
        ],
        title="↘ Diagonal Rainbow",
        direction="diagonal",
        mode="both",
        border="heavy",
        width=50,
    )
    for line in lines:
        print(line)
    print()
    print()

    # Section 4: Creative Examples
    console.text("4️⃣  CREATIVE EFFECTS", color="lime", bold=True)
    print("-" * 80)

    # Fire effect
    lines = diagonal_gradient_frame(
        [
            "🔥 Flames at top",
            "🔥 Heat spreads diagonally",
            "🔥 Cooler at bottom",
            "🔥 Fire gradient!",
        ],
        title="🔥 FIRE EFFECT",
        start_color="yellow",
        end_color="red",
        target="both",
        border="heavy",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Ocean effect
    lines = gradient_frame(
        [
            "🌊 Surface water",
            "🌊 Getting deeper",
            "🌊 Deep ocean",
            "🌊 Ocean depths",
        ],
        title="🌊 Ocean Depths",
        start_color="cyan",
        end_color="blue",
        target="both",
        border="rounded",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Sunset effect
    lines = gradient_frame(
        [
            "🌅 Sky high",
            "🌅 Horizon",
            "🌅 Sunset colors",
            "🌅 Ground level",
        ],
        title="🌅 Sunset",
        start_color="orange",
        end_color="purple",
        target="both",
        border="rounded",
        width=50,
    )
    for line in lines:
        print(line)
    print()

    # Matrix effect
    lines = diagonal_gradient_frame(
        [
            "▓▒░ Digital rain",
            "▓▒░ Code flowing",
            "▓▒░ Matrix style",
            "▓▒░ Green cascade",
        ],
        title="🖥 Matrix Effect",  # Base emoji without variation selector
        start_color="lime",
        end_color="green",
        target="both",
        border="solid",
        width=50,
    )
    for line in lines:
        print(line)
    print()
    print()

    # Footer - showcasing gradient effect
    footer_lines = gradient_frame(
        [
            "✨ Gradient effects showcase complete! ✨",
            "Try different color combinations!",
        ],
        start_color="purple",
        end_color="cyan",
        target="both",
        border="double",
        width=57,
    )
    for line in footer_lines:
        print(line)
    print()

    # Section 5: Digital Poetry
    console.text("5️⃣  DIGITAL POETRY", color="gold", bold=True)
    print("-" * 80)

    # Poetry banner header with gradient - will be inside the frame
    from styledconsole.core.banner import BannerRenderer

    banner_renderer = BannerRenderer()
    banner_lines = banner_renderer.render(
        "POETRY", font="slant", start_color="magenta", end_color="cyan"
    )

    # Digital poetry content with banner at the top
    poetry_lines = banner_lines + [
        "",
        "⭐ In the realm where colors dance and play,",
        "Where gradients flow in bold display,",
        "A library born from code and art,",
        "StyledConsole, a beating heart.",
        "",
        "🌈 From red to blue, the spectrum bends,",
        "Through purple hues, the rainbow blends,",
        "Diagonal paths from corner bright,",
        "Top-left to bottom-right in flight.",
        "",
        "✨ Three modes of beauty we provide:",
        "Content glows with colored pride,",
        "Borders shine with gradient flow,",
        "Or both together steal the show.",
        "",
        "💎 Characters measured, width precise,",
        "Emojis handled, calculated twice,",
        "Visual width and codepoints clean,",
        "The finest frames you've ever seen.",
        "",
        "🎨 From fire's glow to ocean deep,",
        "From sunset's fade to secrets keep,",
        "Matrix rain in cascading green,",
        "Every effect a vivid dream.",
        "",
        "🚀 So render bold, let colors sing,",
        "Let gradients dance, let rainbows ring,",
        "In terminal windows, dark and wide,",
        "Let StyledConsole be your guide!",
    ]

    # Apply full rainbow spectrum to content (cycling through ROYGBIV)
    # Create frame first (without gradient)
    from styledconsole.core.frame import FrameRenderer
    from styledconsole.effects import _colorize, get_rainbow_color
    from styledconsole.utils.color import interpolate_color
    from styledconsole.utils.text import strip_ansi

    frame_renderer = FrameRenderer()
    poetry_frame = frame_renderer.render(
        poetry_lines,
        border="heavy",
        # No width specified - auto-width calculation!
    )

    # Apply rainbow to content lines (skip borders)
    from styledconsole.core.styles import get_border_style

    style = get_border_style("heavy")
    colored_poetry = []

    content_line_count = 0
    for idx, line in enumerate(poetry_frame):
        clean = strip_ansi(line)

        if clean and clean[0] in {style.top_left, style.bottom_left}:
            # Top or bottom border - apply gradient
            position = idx / max(len(poetry_frame) - 1, 1)
            color = interpolate_color("gold", "purple", position)
            colored_poetry.append(_colorize(clean, color))
        elif clean and clean[0] == style.vertical:
            # Content line - apply rainbow to content, gradient to borders
            position = idx / max(len(poetry_frame) - 1, 1)
            border_color = interpolate_color("gold", "purple", position)

            # Get rainbow color for this content line (cycling through 7 colors)
            rainbow_position = (content_line_count % 7) / 6.0  # Convert to 0.0-1.0 range
            rainbow_color = get_rainbow_color(rainbow_position)
            content_line_count += 1

            left_border = clean[0]
            right_border = clean[-1]
            content = clean[len(left_border) : -len(right_border)]

            colored_line = (
                _colorize(left_border, border_color)
                + _colorize(content, rainbow_color)
                + _colorize(right_border, border_color)
            )
            colored_poetry.append(colored_line)
        else:
            colored_poetry.append(line)

    for line in colored_poetry:
        print(line)
    print()
    print()

    # Tips
    console.text("💡 Tips:", color="yellow", bold=True)
    console.text("  • Use gradient_frame() for vertical gradients")
    console.text("  • Use diagonal_gradient_frame() for diagonal effects")
    console.text("  • Use rainbow_frame() with direction='vertical' or 'diagonal'")
    console.text("  • Set target='content', 'border', or 'both'")
    console.text("  • All CSS4 color names and hex codes supported!")
    console.text("  • Width auto-calculated when not specified!")
    print()


if __name__ == "__main__":
    main()
