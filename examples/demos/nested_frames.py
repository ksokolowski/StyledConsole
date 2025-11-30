"""Nested frames and frame_group() demonstration.

This example showcases:
1. frame_group() - The v0.7.0 approach for grouped frames (recommended)
2. render_frame() nesting - Manual nesting using render_frame() strings

frame_group() is the recommended approach for most use cases as it:
- Handles layout and spacing automatically
- Supports style inheritance
- Provides cleaner, more readable code
"""

from styledconsole import EMOJI, Console


def demo_frame_group_basic():
    """Basic frame_group usage - the recommended approach."""
    console = Console()

    console.banner("FRAME GROUP", font="slant", start_color="cyan", end_color="blue")
    console.newline()

    # Simple frame group with multiple sections
    console.frame_group(
        [
            {"content": "System status: Online", "title": "Status"},
            {"content": "CPU: 45%\nMemory: 2.1GB\nDisk: 120GB", "title": "Resources"},
            {"content": "Last backup: 2 hours ago", "title": "Backup"},
        ],
        title=f"{EMOJI.CHART_BAR} Dashboard",
        border="double",
        border_color="cyan",
        gap=1,
    )
    console.newline(2)


def demo_frame_group_styled():
    """Frame group with individual styling per section."""
    console = Console()

    console.text("Styled Frame Group:", bold=True, color="yellow")
    console.newline()

    # Each section can have its own colors
    console.frame_group(
        [
            {
                "content": f"{EMOJI.CHECK} All systems operational",
                "title": "Success",
                "border_color": "green",
                "border": "rounded",
            },
            {
                "content": f"{EMOJI.WARNING} High memory usage",
                "title": "Warning",
                "border_color": "yellow",
                "border": "rounded",
            },
            {
                "content": f"{EMOJI.CROSS} Database connection failed",
                "title": "Error",
                "border_color": "red",
                "border": "rounded",
            },
        ],
        title=f"{EMOJI.CLIPBOARD} System Report",
        border="heavy",
        border_gradient_start="green",
        border_gradient_end="red",
        gap=1,
    )
    console.newline(2)


def demo_frame_group_inherit():
    """Frame group with style inheritance."""
    console = Console()

    console.text("Style Inheritance:", bold=True, color="magenta")
    console.newline()

    # Inner frames inherit outer border style
    console.frame_group(
        [
            {"content": "Section A - inherits heavy border"},
            {"content": "Section B - inherits heavy border"},
            {"content": "Section C - inherits heavy border"},
        ],
        title="Inherited Styling",
        border="heavy",
        border_color="magenta",
        inherit_style=True,  # Inner frames also use "heavy"
        gap=0,
    )
    console.newline(2)


def demo_nested_render_frame():
    """Manual nesting using render_frame() - for complex layouts."""
    console = Console()

    console.text("Manual Nesting (render_frame):", bold=True, color="cyan")
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
            f"{EMOJI.RAINBOW} NESTED GRADIENT ARCHITECTURE",
            "   (Manual Nesting with render_frame)",
            "",
            fire_frame,
            "",
            "Four gradient layers, each with meaning:",
            "Fire → Growth → Depth → Soul",
        ],
        title=f"{EMOJI.CLASSICAL_BUILDING} Gradient Architecture",
        border="heavy",
        border_gradient_start="red",
        border_gradient_end="magenta",
        content_color="white",
        align="center",
        width=80,
    )
    console.newline(2)


def demo_nested_frame_groups():
    """Nesting frame_groups using render_frame_group()."""
    console = Console()

    console.text("Nested Frame Groups:", bold=True, color="green")
    console.newline()

    # Create an inner group
    inner_group = console.render_frame_group(
        [
            {"content": "Sub-item 1"},
            {"content": "Sub-item 2"},
        ],
        title="Inner Group",
        border="rounded",
        border_color="cyan",
        gap=0,
    )

    # Embed inner group in outer frame
    console.frame(
        [
            "This demonstrates nesting frame_groups",
            "",
            inner_group,
            "",
            "The inner group is rendered to string first,",
            "then embedded in the outer frame.",
        ],
        title=f"{EMOJI.FOLDER} Nested Groups",
        border="double",
        border_color="green",
        width=60,
    )
    console.newline(2)


def demo_comparison():
    """Show when to use frame_group vs render_frame."""
    console = Console()

    console.text("When to Use Each Approach:", bold=True, color="white")
    console.newline()

    console.frame_group(
        [
            {
                "content": [
                    "• Dashboards with multiple sections",
                    "• Status panels",
                    "• Uniform layouts",
                    "• Style inheritance needed",
                ],
                "title": f"{EMOJI.CHECK} Use frame_group()",
                "border_color": "green",
            },
            {
                "content": [
                    "• Complex gradient nesting",
                    "• Arbitrary depth levels",
                    "• Per-frame width control",
                    "• Custom compositions",
                ],
                "title": f"{EMOJI.WRENCH} Use render_frame()",
                "border_color": "cyan",
            },
        ],
        title=f"{EMOJI.LIGHTBULB} Choosing the Right Approach",
        border="rounded",
        gap=1,
    )
    console.newline()


if __name__ == "__main__":
    console = Console()
    console.clear()

    demo_frame_group_basic()
    demo_frame_group_styled()
    demo_frame_group_inherit()
    demo_nested_render_frame()
    demo_nested_frame_groups()
    demo_comparison()

    console.text(
        "frame_group() is v0.7.0's recommended approach for grouped frames!",
        color="cyan",
        bold=True,
    )
