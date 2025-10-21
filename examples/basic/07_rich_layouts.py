"""Rich Layout Examples (v0.3.0 - Rich Native)

Demonstrates layout composition using Rich's native renderables:
- Group for vertical stacking
- Columns for side-by-side placement
- Table.grid for grid layouts
- Align for positioning

v0.3.0: Updated to use Rich Panel/Group/Columns instead of LayoutComposer.
"""

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from styledconsole import Console
from styledconsole.core.box_mapping import get_box_style

console = Console()


def example_1_basic_stacking():
    """Example 1: Basic vertical stacking with Group."""
    console.newline()
    console.rule("Example 1: Vertical Stacking with Group", style="bold cyan")
    console.newline()

    # Create panels
    header = Panel("Application Dashboard", title="Header", box=get_box_style("solid"))
    content = Panel(
        "This is the main content area\nMultiple lines supported",
        title="Content",
        box=get_box_style("solid"),
    )
    footer = Panel("Status: Active", title="Footer", box=get_box_style("solid"))

    # Stack with Group (use Text("") for spacing)
    group = Group(
        header,
        Text(""),  # Spacing
        content,
        Text(""),  # Spacing
        footer,
    )

    console._rich_console.print(group)


def example_2_side_by_side():
    """Example 2: Side-by-side placement with Columns."""
    console.newline()
    console.rule("Example 2: Side-by-Side with Columns", style="bold cyan")
    console.newline()

    # Create panels
    left_panel = Panel("Option 1\nOption 2\nOption 3", title="Menu", box=get_box_style("rounded"))
    right_panel = Panel(
        "Details about\nthe selected\noption", title="Details", box=get_box_style("rounded")
    )

    # Use Columns for side-by-side
    columns = Columns([left_panel, right_panel], padding=(0, 2))

    console._rich_console.print(columns)


def example_3_grid_layout():
    """Example 3: Grid layout using Table.grid."""
    console.newline()
    console.rule("Example 3: Grid Layout with Table.grid", style="bold cyan")
    console.newline()

    # Create 2x2 grid of status cards
    panel1 = Panel("Count: 42", title="Users", box=get_box_style("double"))
    panel2 = Panel("Count: 128", title="Posts", box=get_box_style("double"))
    panel3 = Panel("Count: 5", title="Admins", box=get_box_style("double"))
    panel4 = Panel("Count: 3", title="Alerts", box=get_box_style("double"))

    # Create grid using Table
    grid = Table.grid(padding=(0, 2))
    grid.add_column()
    grid.add_column()

    grid.add_row(panel1, panel2)
    grid.add_row(Text(""))  # Spacing row
    grid.add_row(panel3, panel4)

    console._rich_console.print(grid)


def example_4_alignment_options():
    """Example 4: Different alignment options using Align."""
    console.newline()
    console.rule("Example 4: Alignment with Align", style="bold cyan")
    console.newline()

    # Create panels with different widths
    short = Panel("Short", expand=False)
    long = Panel("Much longer text line", expand=False)
    mid = Panel("Mid", expand=False)

    # Left alignment
    console.text("Left Aligned:", color="yellow")
    group_left = Group(short, long, mid)
    console._rich_console.print(Align(group_left, align="left"))

    console.newline()
    console.text("Center Aligned:", color="yellow")
    group_center = Group(short, long, mid)
    console._rich_console.print(Align(group_center, align="center"))

    console.newline()
    console.text("Right Aligned:", color="yellow")
    group_right = Group(short, long, mid)
    console._rich_console.print(Align(group_right, align="right"))


def example_5_complex_dashboard():
    """Example 5: Complex dashboard combining techniques."""
    console.newline()
    console.rule("Example 5: Complex Dashboard", style="bold cyan")
    console.newline()

    # Header
    header = Panel(
        "[bold cyan]System Dashboard[/bold cyan]",
        box=get_box_style("double"),
    )

    # Metrics row (3 panels side by side)
    metric1 = Panel("✅ 98.5%", title="Uptime", box=get_box_style("rounded"))
    metric2 = Panel("🚀 1.2ms", title="Latency", box=get_box_style("rounded"))
    metric3 = Panel("👥 1,234", title="Users", box=get_box_style("rounded"))

    metrics = Columns([metric1, metric2, metric3], equal=True, expand=True)

    # Status panels (2 panels side by side)
    status_left = Panel(
        "✅ API Server: Running\n✅ Database: Connected\n✅ Cache: Active",
        title="Services",
        box=get_box_style("solid"),
    )

    status_right = Panel(
        "📊 CPU: 23%\n💾 Memory: 45%\n💽 Disk: 67%",
        title="Resources",
        box=get_box_style("solid"),
    )

    status = Columns([status_left, status_right], equal=True, expand=True)

    # Footer
    footer = Panel(
        "Last updated: Just now | Next refresh: 30s",
        box=get_box_style("minimal"),
    )

    # Combine everything
    dashboard = Group(
        header,
        Text(""),
        metrics,
        Text(""),
        status,
        Text(""),
        footer,
    )

    console._rich_console.print(dashboard)


def example_6_mixed_renderables():
    """Example 6: Mixing different Rich renderables."""
    console.newline()
    console.rule("Example 6: Mixed Renderables", style="bold cyan")
    console.newline()

    # Mix text, panels, and styled text
    title = Text("System Status Report", style="bold magenta")

    panel1 = Panel(
        "All systems operational ✅",
        title="Status",
        border_style="green",
    )

    divider = Text("─" * 50, style="dim")

    panel2 = Panel(
        "Total: 1,234\nActive: 1,100\nIdle: 134",
        title="User Statistics",
        border_style="cyan",
    )

    group = Group(
        Align(title, align="center"),
        Text(""),
        panel1,
        divider,
        panel2,
    )

    console._rich_console.print(group)


if __name__ == "__main__":
    console.frame(
        "Demonstrates Rich's native layout capabilities:\n"
        "• Group for vertical stacking\n"
        "• Columns for horizontal placement\n"
        "• Table.grid for grid layouts\n"
        "• Align for positioning",
        title="🎨 Rich Layout Examples (v0.3.0)",
        border="double",
        border_color="magenta",
        width=70,
    )

    example_1_basic_stacking()
    example_2_side_by_side()
    example_3_grid_layout()
    example_4_alignment_options()
    example_5_complex_dashboard()
    example_6_mixed_renderables()

    console.newline()
    console.frame(
        "✅ Rich provides powerful layout primitives\n"
        "✅ All rendering is ANSI-safe\n"
        "✅ Compose complex UIs with simple building blocks\n"
        "✅ Use Console.frame() for quick frames",
        title="💡 Summary",
        border="double",
        border_color="green",
        width=70,
    )
    console.newline()
