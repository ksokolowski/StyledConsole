from styledconsole import Console


def demo_nested_frames():
    console = Console()
    console.clear()
    console.banner("NESTED", font="slant", start_color="cyan", end_color="blue")
    console.newline()

    # 1. Create the innermost frame (Soul)
    soul_frame = console.render_frame(
        "Purple → Magenta (Soul)\n▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔",
        border="ascii",
        content_color="magenta",
        border_color="magenta",
        align="center",
        width=26,
    )

    # 2. Create the next layer (Depth)
    depth_frame = console.render_frame(
        ["Cyan → Blue (Depth frame)", "", soul_frame],
        border="thick",
        border_gradient_start="cyan",
        border_gradient_end="blue",
        align="center",
        width=34,
    )

    # 3. Create the next layer (Growth)
    growth_frame = console.render_frame(
        ["Yellow → Green (Growth frame)", "", depth_frame],
        border="rounded",
        border_gradient_start="yellow",
        border_gradient_end="green",
        align="center",
        width=44,
    )

    # 4. Create the outer layer (Fire)
    fire_frame = console.render_frame(
        ["Red → Orange (Fire frame)", "", growth_frame],
        border="solid",
        border_gradient_start="red",
        border_gradient_end="orange1",
        align="center",
        width=54,
    )

    # 5. Final assembly
    console.frame(
        [
            "🌈 NESTED GRADIENT ARCHITECTURE",
            "   (Native Implementation)",
            "",
            fire_frame,
            "",
            "Four gradient layers, each with meaning:",
            "Fire → Growth → Depth → Soul",
            "",
            "This is gradient architecture at its finest.",
        ],
        title="🏛️  Gradient Architecture",
        border="heavy",
        border_gradient_start="red",
        border_gradient_end="magenta",
        content_color="white",
        align="center",
        width=80,
    )
    console.newline(2)


if __name__ == "__main__":
    demo_nested_frames()
