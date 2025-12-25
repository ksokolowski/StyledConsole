"""Nested frames and frame grouping demonstration.

This example showcases three approaches for creating grouped frames:
1. frame_group() - Dictionary-based API (v0.7.0)
2. console.group() - Context manager API (v0.7.0)
3. render_frame() - Manual nesting for complex layouts

The context manager is recommended for most use cases as it:
- Is more Pythonic and readable
- Supports arbitrary nesting
- Automatically handles frame capture and rendering
"""

from styledconsole import Console, StyleContext, icons


def demo_context_manager_basic():
    """Basic context manager usage - the recommended approach."""
    console = Console()

    console.banner("CONTEXT MANAGER", font="slant", start_color="cyan", end_color="magenta")
    console.newline()

    # Simple group with context manager
    with console.group(title=f"{icons.BAR_CHART} Dashboard", border="double", border_color="cyan"):
        console.frame("System status: Online", style=StyleContext(title="Status"))
        console.frame("CPU: 45%\nMemory: 2.1GB\nDisk: 120GB", style=StyleContext(title="Resources"))
        console.frame("Last backup: 2 hours ago", style=StyleContext(title="Backup"))

    console.newline(2)


def demo_context_manager_nested():
    """Nested context managers for complex layouts."""
    console = Console()

    console.text("Nested Context Managers:", bold=True, color="yellow")
    console.newline()

    with console.group(title=f"{icons.FILE_FOLDER} Project Overview", border="heavy"):
        console.frame("Main application ready", title="App Status")

        with console.group(title="Services", border="rounded", border_color="cyan"):
            console.frame(
                f"{icons.CHECK_MARK_BUTTON} Database connected",
                style=StyleContext(border_color="green"),
            )
            console.frame(
                f"{icons.CHECK_MARK_BUTTON} Cache active", style=StyleContext(border_color="green")
            )
            console.frame(f"{icons.WARNING} Queue slow", style=StyleContext(border_color="yellow"))

        console.frame("All tests passing", style=StyleContext(title="CI/CD"))

    console.newline(2)


def demo_context_manager_align_widths():
    """Context manager with width alignment for status displays."""
    console = Console()

    console.text("Aligned Widths (Status Style):", bold=True, color="magenta")
    console.newline()

    # align_widths=True makes all inner frames the same width
    with console.group(title=f"{icons.CLIPBOARD} System Report", align_widths=True):
        console.frame(
            f"{icons.CHECK_MARK_BUTTON} All systems operational",
            style=StyleContext(title="Success", border_color="green"),
        )
        console.frame(
            f"{icons.WARNING} High memory usage detected",
            style=StyleContext(title="Warning", border_color="yellow"),
        )
        console.frame(
            f"{icons.CROSS_MARK} Database connection failed",
            style=StyleContext(title="Error", border_color="red"),
        )

    console.newline(2)


def demo_frame_group_basic():
    """Dictionary-based frame_group() for simple cases."""
    console = Console()

    console.text("Dictionary-based frame_group():", bold=True, color="cyan")
    console.newline()

    # Simple frame group with multiple sections
    console.frame_group(
        [
            {"content": "System status: Online", "title": "Status"},
            {"content": "CPU: 45%\nMemory: 2.1GB", "title": "Resources"},
        ],
        title=f"{icons.BAR_CHART} Quick Stats",
        border="rounded",
        border_color="cyan",
        gap=1,
    )
    console.newline(2)


def demo_nested_render_frame():
    """Manual nesting using render_frame() - for complex layouts."""
    console = Console()

    console.text("Manual Nesting (render_frame):", bold=True, color="cyan")
    console.newline()

    # Create nested gradient frames manually
    soul_frame = console.render_frame(
        "Purple → Magenta (Soul)",
        border="ascii",
        border_color="magenta",
        width=26,
    )

    depth_frame = console.render_frame(
        ["Cyan → Blue (Depth)", "", soul_frame],
        border="thick",
        border_gradient_start="cyan",
        border_gradient_end="blue",
        width=34,
    )

    growth_frame = console.render_frame(
        ["Yellow → Green (Growth)", "", depth_frame],
        border="rounded",
        border_gradient_start="yellow",
        border_gradient_end="green",
        width=44,
    )

    console.frame(
        [
            f"{icons.RAINBOW} GRADIENT ARCHITECTURE",
            "",
            growth_frame,
            "",
            "Three gradient layers: Growth → Depth → Soul",
        ],
        style=StyleContext(
            title=f"{icons.CLASSICAL_BUILDING} Nested Gradients",
            border_style="heavy",
            border_gradient_start="red",
            border_gradient_end="magenta",
            align="center",
            width=60,
        ),
    )
    console.newline(2)


def demo_comparison():
    """Show when to use each approach."""
    console = Console()

    console.text("When to Use Each Approach:", bold=True, color="white")
    console.newline()

    with console.group(title=f"{icons.LIGHT_BULB} Choosing the Right API", border="rounded"):
        console.frame(
            [
                f"{icons.CHECK_MARK_BUTTON} console.group() context manager:",
                "  • Most Pythonic approach",
                "  • Arbitrary nesting depth",
                "  • Dynamic content during context",
                "  • Automatic width alignment option",
            ],
            style=StyleContext(title="Recommended", border_color="green"),
        )
        console.frame(
            [
                f"{icons.WRENCH} frame_group() dictionary API:",
                "  • Simple, known structure",
                "  • Good for data-driven layouts",
                "  • Compact one-liner possible",
            ],
            style=StyleContext(title="Alternative", border_color="cyan"),
        )
        console.frame(
            [
                f"{icons.GEAR} render_frame() manual nesting:",
                "  • Complex gradient compositions",
                "  • Per-frame width control",
                "  • Maximum flexibility",
            ],
            style=StyleContext(title="Advanced", border_color="yellow"),
        )

    console.newline()


if __name__ == "__main__":
    console = Console()
    console.clear()

    demo_context_manager_basic()
    demo_context_manager_nested()
    demo_context_manager_align_widths()
    demo_frame_group_basic()
    demo_nested_render_frame()
    demo_comparison()

    console.text(
        "console.group() context manager is the recommended approach!",
        color="cyan",
        bold=True,
    )
