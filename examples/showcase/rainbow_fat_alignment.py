#!/usr/bin/env python
"""Rainbow Fat Alignment Showcase (v0.3.0 - Rich Native).

Advanced example demonstrating:
- Large, colorful banners with rainbow gradients
- Emoji integration throughout layout
- All three alignment types: left, center, right
- Mixed alignment layouts (sections aligned differently on same row)
- Emoji-rich dashboard with multiple cards
- Border style gallery with all 8 border types
- Nested layouts with panels within panels
- Complex grid layouts with mixed content types
- Dynamic dashboard simulation with status indicators
- Advanced typography with mixed styles and colors
- Data visualization mockups with charts and metrics
- Rich Panel and Align for perfect ANSI handling
- Complex layout composition with Groups and Columns

v0.3.0: Rich-native with comprehensive showcase features.
No more manual string manipulation - all ANSI-safe!
"""

from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from styledconsole import Console
from styledconsole.core.banner import BannerRenderer
from styledconsole.core.box_mapping import get_box_style


def create_panel(
    content: str,
    title: str = "",
    emoji: str = "✨",
    border: str = "rounded",
    border_color: str = "cyan",
    content_color: str | None = None,
    width: int = 60,
) -> Panel:
    """Create a Rich Panel with optional color and emoji.

    Args:
        content: Panel content (can include newlines)
        title: Panel title
        emoji: Emoji for title decoration
        border: Border style name
        border_color: Border color
        content_color: Content color (optional)
        width: Panel width

    Returns:
        Rich Panel renderable
    """
    # Format title with emoji
    if title and emoji:
        full_title = f"{emoji}  {title}"
    else:
        full_title = title

    # Apply content color if specified
    if content_color:
        styled_content = f"[{content_color}]{content}[/]"
    else:
        styled_content = content

    # Get Rich box style
    box_style = get_box_style(border)

    return Panel(
        styled_content,
        title=full_title,
        box=box_style,
        border_style=border_color,
        width=width,
        padding=(0, 2),
        expand=False,
    )


# -------------------------
# Formatting helpers
# -------------------------
def expand_emoji_shortcodes(text: str) -> str:
    """Replace simple emoji shortcodes like :rocket: with actual emoji.

    This is intentionally lightweight (no external dependency). Add mappings
    as needed for the example. Returns the transformed string.
    """
    mapping = {
        ":rocket:": "🚀",
        ":sparkles:": "✨",
        ":fire:": "🔥",
        ":bulb:": "💡",
        ":chart_with_upwards_trend:": "📈",
        ":gear:": "⚙️",
        ":package:": "📦",
        ":star:": "⭐",
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


def gradient_markup(text: str, start_color: str, end_color: str, per: str = "line") -> str:
    """Return Rich markup wrapping the input text with an interpolated gradient.

    Args:
        text: Input (may contain multiple lines).
        start_color: CSS4 color name or hex for gradient start.
        end_color: CSS4 color name or hex for gradient end.
        per: "line" to color each line in a gradient, "char" to color each grapheme.

    Returns:
        A string containing Rich color markup (e.g. [#rrggbb]...[/]).
    """
    # Lazy import to reuse existing color utils
    try:
        from styledconsole.utils.color import interpolate_color
    except Exception:
        # Fallback: return text wrapped with start_color
        return f"[{start_color}]{text}[/]"

    lines = text.split("\n")
    if per == "line":
        out_lines = []
        for i, line in enumerate(lines):
            ratio = i / (len(lines) - 1) if len(lines) > 1 else 0
            col = interpolate_color(start_color, end_color, ratio)
            out_lines.append(f"[{col}]{line}[/]")
        return "\n".join(out_lines)
    else:
        # per-char gradient (safe fallback using characters)
        try:
            from styledconsole.utils.text import split_graphemes

            graphemes = split_graphemes(text)
        except Exception:
            graphemes = list(text)

        out = []
        n = len(graphemes)
        for i, g in enumerate(graphemes):
            ratio = i / (n - 1) if n > 1 else 0
            col = interpolate_color(start_color, end_color, ratio)
            out.append(f"[{col}]{g}[/]")
        return "".join(out)


def print_banner_from_lines(console: Console, lines: list[str], align: str = "left") -> None:
    """Print banner lines with proper alignment.

    Args:
        console: Console instance
        lines: Banner lines (from BannerRenderer)
        align: Alignment (left, center, right)
    """
    banner_text = "\n".join(lines)
    text = Text.from_ansi(banner_text)
    aligned = Align(text, align=align)
    console._rich_console.print(aligned)


def create_rainbow_banner(text: str, font: str = "slant", max_width: int = 100) -> list[str]:
    """Create a rainbow gradient banner.

    Args:
        text: Text to display in banner
        font: Pyfiglet font to use
        max_width: Maximum banner width (actual may be less)

    Returns:
        List of lines representing the banner
    """
    renderer = BannerRenderer()
    return renderer.render(
        text,
        font=font,
        start_color="red",
        end_color="magenta",
        width=max_width,
    )


def main() -> None:
    """Main showcase function."""
    console = Console()
    terminal_width = console._rich_console.width

    # Frame width for panels
    panel_width = min(70, terminal_width // 2)

    console.newline()

    # ==============================================================================
    # SECTION 1: Rainbow Banner Header
    # ==============================================================================
    console.frame(
        "Welcome to the comprehensive alignment showcase! UNIQUE_IDENTIFIER_12345",
        title="🚀 Rainbow Fat Alignment (v0.3.0)",
        border="double",
        border_color="magenta",
        content_color="bright_yellow",
        padding=2,
    )

    console.newline()

    # Large rainbow banner
    banner = create_rainbow_banner("ALIGNMENT", font="banner", max_width=panel_width)
    print_banner_from_lines(console, banner, align="center")
    console.newline(2)

    # ==============================================================================
    # NESTED PANELS EXAMPLE (side-by-side and stacked)
    # ==============================================================================
    # Demonstrate encapsulating Panels inside a larger Panel. Use gradient_markup
    # and emoji shortcodes to create colorful inner content, then embed two inner
    # Panels into an outer Panel both side-by-side and stacked.

    raw_a = ":sparkles: Inner A — Compact metrics\nCPU: 42%\nMem: 3.2GB"
    raw_b = ":fire: Inner B — Alerts\nErrors: 2\nWarnings: 7"

    a_exp = expand_emoji_shortcodes(raw_a)
    b_exp = expand_emoji_shortcodes(raw_b)

    a_grad = gradient_markup(a_exp, "red", "magenta", per="line")
    b_grad = gradient_markup(b_exp, "yellow", "red", per="line")

    # Calculate a slightly smaller outer width so the nested panels fit comfortably
    outer_width = max(48, panel_width - 10)
    # Inner width computed to fit two panels side-by-side inside the outer width
    inner_width = max(16, (outer_width - 6) // 2)

    inner1 = Panel(
        Text.from_markup(a_grad),
        title="🔹 Inner A",
        box=get_box_style("rounded"),
        border_style="bright_magenta",
        width=inner_width,
    )
    inner2 = Panel(
        Text.from_markup(b_grad),
        title="🔸 Inner B",
        box=get_box_style("rounded"),
        border_style="bright_yellow",
        width=inner_width,
    )

    # Outer: side-by-side using a Table grid to force single-row layout
    side_table = Table.grid(padding=(0, 1))
    side_table.add_column(ratio=1)
    side_table.add_column(ratio=1)
    side_table.add_row(inner1, inner2)

    outer_side = Panel(
        side_table,
        title="🌈 Nested Panels (side-by-side)",
        box=get_box_style("double"),
        border_style="bright_cyan",
        width=outer_width,
    )

    # Outer: stacked (use the same inner panels but stacked)
    # For stacked layout we use a smaller outer width and center each inner panel
    outer_stack_width = max(inner_width + 8, 36)
    stacked_group = Group(Align(inner1, align="center"), Align(inner2, align="center"))
    outer_stack = Panel(
        stacked_group,
        title="🌈 Nested Panels (stacked)",
        box=get_box_style("double"),
        border_style="bright_green",
        width=outer_stack_width,
    )

    # Wrap both nested examples into one outermost frame with a heavy, rainbow-styled title.
    title_markup = gradient_markup("🌈 Rainbow Frame", "red", "magenta", per="char")
    title_text = Text.from_markup(title_markup)

    outermost_width = min(panel_width + 8, terminal_width - 4)
    outermost = Panel(
        Group(Align(outer_side, align="center"), Align(outer_stack, align="center")),
        title=title_text,
        box=get_box_style("heavy"),
        border_style="bright_magenta",
        width=outermost_width,
        padding=(0, 1),
    )

    # Build a mirrored outermost frame to place next to the first one
    # Reuse gradients/content but change title colors for visual distinction
    title2_markup = gradient_markup("🌈 Rainbow Frame 2", "cyan", "blue", per="char")
    title2_text = Text.from_markup(title2_markup)

    # Create second set of inner panels (copies) so we can display two independent frames
    inner1_b = Panel(
        Text.from_markup(a_grad),
        title="🔹 Inner A",
        box=get_box_style("rounded"),
        border_style="bright_magenta",
        width=inner_width,
    )
    inner2_b = Panel(
        Text.from_markup(b_grad),
        title="🔸 Inner B",
        box=get_box_style("rounded"),
        border_style="bright_yellow",
        width=inner_width,
    )

    # Side-by-side and stacked variants for the second frame
    side_table_b = Table.grid(padding=(0, 1))
    side_table_b.add_column(ratio=1)
    side_table_b.add_column(ratio=1)
    side_table_b.add_row(inner1_b, inner2_b)

    outer_side_b = Panel(
        side_table_b,
        title="🌈 Nested Panels (side-by-side)",
        box=get_box_style("double"),
        border_style="bright_cyan",
        width=outer_width,
    )
    stacked_group_b = Group(Align(inner1_b, align="center"), Align(inner2_b, align="center"))
    outer_stack_b = Panel(
        stacked_group_b,
        title="🌈 Nested Panels (stacked)",
        box=get_box_style("double"),
        border_style="bright_green",
        width=outer_stack_width,
    )

    outermost_b = Panel(
        Group(Align(outer_side_b, align="center"), Align(outer_stack_b, align="center")),
        title=title2_text,
        box=get_box_style("heavy"),
        border_style="bright_blue",
        width=outermost_width,
        padding=(0, 1),
    )

    # Print both outermost frames side-by-side
    both = Columns([outermost, outermost_b], equal=True, expand=False)
    console._rich_console.print(Align(both, align="center"))
    console.newline(2)

    # ==============================================================================
    # SECTION 2: Three Alignment Demonstration
    # ==============================================================================
    console.frame(
        "Demonstrating Left, Center, and Right alignment with Rich Panel",
        title="🎨 Basic Alignment Showcase",
        border="double",
        border_color="magenta",
        content_color="bright_yellow",
        padding=2,
    )

    console.newline(2)

    # ==============================================================================
    # LEFT ALIGNMENT
    # ==============================================================================
    console.print("[bold cyan]LEFT-ALIGNED (Default)[/]")
    console.newline()

    # Banner
    left_banner = BannerRenderer().render(
        "LEFT",
        font="small",
        start_color="red",
        end_color="orange",
        width=panel_width,
    )
    print_banner_from_lines(console, left_banner, align="left")
    console.newline()

    # Panels
    panel1 = create_panel(
        "⚡ Lightning speed\n🚀 Rapid deployment\n📈 Quick response",
        title="Fast & Quick",
        emoji="⚡",
        border="rounded",
        border_color="bright_yellow",
        content_color="yellow",
        width=panel_width,
    )

    panel2 = create_panel(
        "✨ Strong performance\n💎 Hot features\n⚙️ Robust engine",
        title="Powerful",
        emoji="✨",
        border="solid",
        border_color="red",
        content_color="bright_yellow",
        width=panel_width,
    )

    # Print with left alignment
    console._rich_console.print(Align(panel1, align="left"))
    console.newline()
    console._rich_console.print(Align(panel2, align="left"))
    console.newline(2)

    # ==============================================================================
    # CENTER ALIGNMENT
    # ==============================================================================
    console.print("[bold green]CENTER-ALIGNED[/]", justify="center")
    console.newline()

    # Banner
    center_banner = BannerRenderer().render(
        "CENTER",
        font="small",
        start_color="green",
        end_color="cyan",
        width=panel_width,
    )
    print_banner_from_lines(console, center_banner, align="center")
    console.newline()

    # Panels
    panel3 = create_panel(
        "✅ Perfect equilibrium\n🎯 Focused approach\n🌟 Best practices",
        title="Balanced",
        emoji="✅",
        border="double",
        border_color="green",
        content_color="bright_green",
        width=panel_width,
    )

    panel4 = create_panel(
        "🎨 Beautiful design\n🌈 Rich gradients\n✨ Premium quality",
        title="Harmonious",
        emoji="🎨",
        border="rounded",
        border_color="cyan",
        content_color="bright_cyan",
        width=panel_width,
    )

    # Print with center alignment
    console._rich_console.print(Align(panel3, align="center"))
    console.newline()
    console._rich_console.print(Align(panel4, align="center"))
    console.newline(2)

    # ==============================================================================
    # RIGHT ALIGNMENT
    # ==============================================================================
    console.print("[bold magenta]RIGHT-ALIGNED[/]", justify="right")
    console.newline()

    # Banner
    right_banner = BannerRenderer().render(
        "RIGHT",
        font="small",
        start_color="blue",
        end_color="magenta",
        width=panel_width,
    )
    print_banner_from_lines(console, right_banner, align="right")
    console.newline()

    # Panels
    panel5 = create_panel(
        "🚀 Next generation\n✨ Cutting edge\n🌟 Innovation",
        title="Advanced",
        emoji="🚀",
        border="heavy",
        border_color="blue",
        content_color="bright_blue",
        width=panel_width,
    )

    panel6 = create_panel(
        "⭐ Premium features\n🏆 Luxury experience\n🎉 Award winning",
        title="Exclusive",
        emoji="⭐",
        border="double",
        border_color="magenta",
        content_color="bright_magenta",
        width=panel_width,
    )

    # Print with right alignment
    console._rich_console.print(Align(panel5, align="right"))
    console.newline()
    console._rich_console.print(Align(panel6, align="right"))
    console.newline(2)

    # ==============================================================================
    # SECTION 3: Mixed Alignment Layout
    # ==============================================================================
    console.frame(
        "Creating dynamic visual hierarchy with mixed alignments on the same row",
        title="🎭 Mixed Alignment Display",
        border="double",
        border_color="yellow",
        content_color="bright_yellow",
        padding=2,
    )

    console.newline(2)

    # Create three independent sections with different alignments
    section_a = create_panel(
        "🎯 Left aligned\n📊 Data display\n💻 Technical info",
        title="Section A",
        emoji="🎯",
        border="solid",
        border_color="bright_green",
        content_color="green",
        width=panel_width,
    )

    section_b = create_panel(
        "⭐ Center stage\n✨ Main focus\n🌟 Spotlight",
        title="Section B",
        emoji="⭐",
        border="rounded",
        border_color="bright_yellow",
        content_color="yellow",
        width=panel_width,
    )

    section_c = create_panel(
        "📈 Right side\n📋 Notifications\n⚠️ Important",
        title="Section C",
        emoji="📈",
        border="double",
        border_color="bright_magenta",
        content_color="magenta",
        width=panel_width,
    )

    # Use Rich Columns for side-by-side mixed alignment
    mixed_row = Columns(
        [
            Align(section_a, align="left"),
            Align(section_b, align="center"),
            Align(section_c, align="right"),
        ],
        equal=False,
        expand=True,
    )

    console._rich_console.print(mixed_row)
    console.newline(2)

    # ==============================================================================
    # SECTION 4: Emoji-Rich Dashboard
    # ==============================================================================
    console.frame(
        "Dashboard with multiple cards and centered layout",
        title="📊 Emoji Dashboard",
        border="double",
        border_color="cyan",
        content_color="bright_cyan",
        padding=2,
    )

    console.newline(2)

    # Dashboard banner
    dash_banner = BannerRenderer().render(
        "DASHBOARD",
        font="small",
        start_color="magenta",
        end_color="cyan",
        width=panel_width,
    )
    print_banner_from_lines(console, dash_banner, align="center")
    console.newline()

    # Create dashboard cards
    card_1 = create_panel(
        "🚀 Performance\n\n95% uptime",
        title="",
        emoji="",
        border="rounded",
        border_color="bright_green",
        content_color="green",
        width=panel_width // 2 - 2,
    )

    card_2 = create_panel(
        "💾 Storage\n\n512 GB free",
        title="",
        emoji="",
        border="rounded",
        border_color="bright_cyan",
        content_color="cyan",
        width=panel_width // 2 - 2,
    )

    card_3 = create_panel(
        "📊 Users\n\n1,234 online",
        title="",
        emoji="",
        border="rounded",
        border_color="bright_yellow",
        content_color="yellow",
        width=panel_width // 2 - 2,
    )

    card_4 = create_panel(
        "⚡ Speed\n\n2.1 GHz",
        title="",
        emoji="",
        border="rounded",
        border_color="bright_red",
        content_color="red",
        width=panel_width // 2 - 2,
    )

    # Use Rich Columns for dashboard grid
    dashboard_row1 = Columns([card_1, card_2], equal=True)
    dashboard_row2 = Columns([card_3, card_4], equal=True)
    dashboard = Group(dashboard_row1, dashboard_row2)

    console._rich_console.print(Align(dashboard, align="center"))
    console.newline(2)

    # ==============================================================================
    # SECTION 5: Border Style Gallery
    # ==============================================================================
    console.frame(
        "All border styles with different alignments and colors",
        title="🌈 Border Style Gallery",
        border="double",
        border_color="magenta",
        content_color="bright_magenta",
        padding=2,
    )

    console.newline(2)

    styles_to_show = ["solid", "rounded", "double", "heavy", "thick", "ascii", "minimal", "dots"]
    colors = [
        "bright_green",
        "bright_cyan",
        "bright_yellow",
        "bright_red",
        "bright_blue",
        "bright_magenta",
        "bright_white",
        "gray",
    ]

    for i, (style_name, color) in enumerate(zip(styles_to_show, colors)):
        style_panel = create_panel(
            f"✨ {style_name.upper()}\nBorder style demo",
            title="",
            emoji="",
            border=style_name,
            border_color=color,
            content_color="bright_white",
            width=panel_width,
        )

        # Rotate alignments
        alignments = ["left", "center", "right"]
        align_choice = alignments[i % 3]

    # ==============================================================================
    # SECTION 6: Nested Layouts & Hierarchies
    # ==============================================================================
    console.frame(
        "Complex nested layouts with panels within panels and multi-level hierarchies",
        title="🏗️ Nested Layouts & Hierarchies",
        border="double",
        border_color="bright_blue",
        content_color="bright_white",
        padding=2,
    )

    console.newline(2)

    # Simple nested layout
    inner_panel = create_panel(
        "🔧 Core Engine\n⚙️ Processing Unit",
        title="System Core",
        emoji="🔧",
        border="minimal",
        border_color="bright_green",
        content_color="green",
        width=30,
    )

    outer_panel = create_panel(
        "Outer container with inner content",
        title="Infrastructure Stack",
        emoji="🏗️",
        border="double",
        border_color="bright_yellow",
        content_color="yellow",
        width=panel_width,
    )

    # Display panels
    console._rich_console.print(Align(inner_panel, align="center"))
    console.newline()
    console._rich_console.print(Align(outer_panel, align="center"))
    console.newline(2)

    # ==============================================================================
    # SECTION 7: Complex Grid Layouts
    # ==============================================================================
    console.frame(
        "Advanced grid layouts with mixed content types and responsive design",
        title="📐 Complex Grid Layouts",
        border="thick",
        border_color="bright_magenta",
        content_color="bright_white",
        padding=2,
    )

    console.newline(2)

    # Create a complex grid with different content types
    grid_panels = []

    # Status cards with different states
    status_cards = [
        create_panel(
            "🟢 ONLINE\nAll systems operational",
            title="Web Server",
            emoji="🌐",
            border="rounded",
            border_color="bright_green",
            width=20,
        ),
        create_panel(
            "🟡 MAINTENANCE\nScheduled updates",
            title="Database",
            emoji="🗄️",
            border="rounded",
            border_color="bright_yellow",
            width=20,
        ),
        create_panel(
            "🔴 OFFLINE\nConnection lost",
            title="Cache",
            emoji="💾",
            border="rounded",
            border_color="bright_red",
            width=20,
        ),
        create_panel(
            "🔵 STANDBY\nReady for deployment",
            title="Worker",
            emoji="⚙️",
            border="rounded",
            border_color="bright_blue",
            width=20,
        ),
    ]

    # Metrics cards
    metrics_cards = [
        create_panel(
            "📈 2.4M\nRequests/min",
            title="Throughput",
            emoji="📈",
            border="solid",
            border_color="bright_cyan",
            width=18,
        ),
        create_panel(
            "⚡ 45ms\nResponse time",
            title="Latency",
            emoji="⚡",
            border="solid",
            border_color="bright_green",
            width=18,
        ),
        create_panel(
            "💾 78%\nStorage used",
            title="Capacity",
            emoji="💾",
            border="solid",
            border_color="bright_yellow",
            width=18,
        ),
        create_panel(
            "👥 12.5K\nActive users",
            title="Users",
            emoji="👥",
            border="solid",
            border_color="bright_magenta",
            width=18,
        ),
    ]

    # Create rows of the grid
    status_row = Columns(status_cards[:2], equal=True)
    status_row2 = Columns(status_cards[2:], equal=True)
    metrics_row = Columns(metrics_cards[:2], equal=True)
    metrics_row2 = Columns(metrics_cards[2:], equal=True)

    # Combine into final grid
    complex_grid = Group(
        Align(Text("System Status", style="bold bright_white"), align="center"),
        status_row,
        status_row2,
        Text(""),  # Spacer
        Align(Text("Key Metrics", style="bold bright_white"), align="center"),
        metrics_row,
        metrics_row2,
    )

    console._rich_console.print(Align(complex_grid, align="center"))
    console.newline(2)

    # ==============================================================================
    # SECTION 8: Dynamic Dashboard Simulation
    # ==============================================================================
    console.frame(
        "Simulated real-time dashboard with status indicators and progress bars",
        title="📊 Dynamic Dashboard Simulation",
        border="double",
        border_color="bright_cyan",
        content_color="bright_white",
        padding=2,
    )

    console.newline(2)

    # Simulate a deployment dashboard
    deployment_status = create_panel(
        "🚀 Deployment in Progress\n\n"
        "Stage 1: ✅ Build Complete\n"
        "Stage 2: 🔄 Testing (78%)\n"
        "Stage 3: ⏳ Deployment (Pending)\n"
        "Stage 4: ⏳ Rollback (Ready)",
        title="Deployment Pipeline",
        emoji="🚀",
        border="double",
        border_color="bright_blue",
        content_color="bright_white",
        width=panel_width,
    )

    # Progress visualization
    progress_bars = create_panel(
        "Build:     ██████████░░░░░░░ 65%\n"
        "Test:      ████████░░░░░░░░░ 50%\n"
        "Deploy:    ███████████████░░ 85%\n"
        "Monitor:   █████████████████ 100%",
        title="Progress Tracking",
        emoji="📊",
        border="rounded",
        border_color="bright_green",
        content_color="bright_white",
        width=panel_width // 2 - 2,
    )

    # Error/success indicators
    alerts_panel = create_panel(
        "✅ All checks passed\n"
        "✅ Security scan: OK\n"
        "⚠️  Performance warning\n"
        "❌ 1 test failure (minor)",
        title="Quality Gates",
        emoji="🛡️",
        border="solid",
        border_color="bright_yellow",
        content_color="bright_white",
        width=panel_width // 2 - 2,
    )

    # Combine dashboard elements
    dashboard_row = Columns([progress_bars, alerts_panel], equal=True)
    full_dashboard = Group(deployment_status, dashboard_row)

    console._rich_console.print(Align(full_dashboard, align="center"))
    console.newline(2)

    # ==============================================================================
    # SECTION 9: Advanced Typography & Forms
    # ==============================================================================
    console.frame(
        "Advanced typography showcase with mixed styles, forms, and interactive elements",
        title="🎨 Advanced Typography & Forms",
        border="dots",
        border_color="bright_white",
        content_color="bright_white",
        padding=2,
    )

    console.newline(2)

    # Typography showcase
    typography_panel = create_panel(
        "[bold bright_white]BOLD TEXT[/bold bright_white] | [italic bright_cyan]Italic Text[/italic bright_cyan]\n"
        "[underline bright_green]Underlined[/underline bright_green] | [strike bright_red]Strikethrough[/strike bright_red]\n"
        "[bright_yellow]Colors:[/bright_yellow] [red]Red[/red] [green]Green[/green] [blue]Blue[/blue] [magenta]Magenta[/magenta]\n"
        "[dim]Dim text[/dim] | [blink]Blinking text[/blink] | [reverse]Reversed[/reverse]",
        title="Typography Showcase",
        emoji="🎨",
        border="rounded",
        border_color="bright_white",
        width=panel_width,
    )

    # Form-like layout (use Rich Table inside a Panel instead of ASCII art)
    form_table = Table.grid(padding=(0, 1))
    form_table.add_column(justify="right", ratio=1)
    form_table.add_column(justify="left", ratio=3)
    form_table.add_row("Name:", "[bright_cyan]John Doe[/bright_cyan]")
    form_table.add_row("Email:", "[bright_cyan]john@example.com[/bright_cyan]")
    form_table.add_row("Role:", "[bright_yellow]Administrator[/bright_yellow]")
    form_table.add_row("Status:", "[bright_green]✓ Active[/bright_green]")
    form_table.add_row("", "")
    form_table.add_row("", "[bright_blue][Submit][/bright_blue] [bright_red][Cancel][/bright_red]")

    form_panel = Panel(
        form_table,
        title="📝 Interactive Form",
        box=get_box_style("double"),
        border_style="bright_blue",
        width=panel_width,
        padding=(0, 1),
    )

    # Code snippet showcase
    code_panel = create_panel(
        "[bright_green]# Python code example[/bright_green]\n"
        "[bright_white]def[/bright_white] [bright_cyan]calculate_total[/bright_cyan](items):\n"
        "    [bright_white]return[/bright_white] [bright_yellow]sum[/bright_yellow](item.price * item.qty\n"
        "                                   [bright_white]for[/bright_white] item [bright_white]in[/bright_white] items)\n\n"
        "[bright_green]# Result: $1,247.50[/bright_green]",
        title="Code Snippet",
        emoji="💻",
        border="solid",
        border_color="bright_green",
        width=panel_width,
    )

    # Display typography elements
    console._rich_console.print(Align(typography_panel, align="center"))
    console.newline()
    console._rich_console.print(Align(form_panel, align="center"))
    console.newline()
    console._rich_console.print(Align(code_panel, align="center"))
    console.newline(2)

    # ==============================================================================
    # SECTION 10: Data Visualization Mockups
    # ==============================================================================
    console.frame(
        "Data visualization mockups with charts, graphs, and analytics displays",
        title="📈 Data Visualization Mockups",
        border="double",
        border_color="bright_yellow",
        content_color="bright_white",
        padding=2,
    )

    console.newline(2)

    # Bar chart mockup
    bar_chart = create_panel(
        "Monthly Revenue (2025)\n\n"
        "Jan: ████████████████░░ 85K\n"
        "Feb: ███████████████░░░ 78K\n"
        "Mar: ███████████████████ 95K\n"
        "Apr: ████████████████░░ 82K\n"
        "May: ██████████████████░ 92K\n\n"
        "[bright_green]↑ 12% growth YTD[/bright_green]",
        title="Revenue Chart",
        emoji="📊",
        border="rounded",
        border_color="bright_green",
        width=panel_width // 2 - 2,
    )

    # Pie chart mockup (text-based)
    pie_chart = create_panel(
        "Traffic Sources\n\n"
        "█ [bright_blue]Direct (45%)[/bright_blue]\n"
        "█ [bright_green]Search (30%)[/bright_green]\n"
        "█ [bright_yellow]Social (15%)[/bright_yellow]\n"
        "█ [bright_red]Email (10%)[/bright_red]\n\n"
        "[bright_cyan]Total: 2.4M visits[/bright_cyan]",
        title="Traffic Sources",
        emoji="🥧",
        border="rounded",
        border_color="bright_cyan",
        width=panel_width // 2 - 2,
    )

    # Metrics dashboard
    # Use a Rich Table inside a Panel for KPI display instead of manual ASCII box art.
    # Manual box-drawing characters inside a Panel cause nested-border rendering issues
    # (right-side clipping) when the outer Panel draws its own border. Use structured
    # Rich renderables to ensure correct ANSI-safe nesting.
    metrics_table = Table.grid(padding=(0, 1))
    metrics_table.add_column(justify="left", ratio=1)
    metrics_table.add_column(justify="right", ratio=1)

    metrics_table.add_row(
        "💰 Revenue:", "[bright_green]$1.2M[/bright_green] [bright_green]+15%[/bright_green]"
    )
    metrics_table.add_row(
        "👥 Users:", "[bright_green]45K[/bright_green] [bright_green]+8%[/bright_green]"
    )
    metrics_table.add_row(
        "🎯 Conversion:", "[bright_red]3.2%[/bright_red] [bright_red]-0.3%[/bright_red]"
    )
    metrics_table.add_row(
        "⭐ Rating:", "[bright_green]4.8[/bright_green] [bright_green]+0.1[/bright_green]"
    )

    metrics_dashboard = Panel(
        metrics_table,
        title="KPI Dashboard",
        box=get_box_style("double"),
        border_style="bright_magenta",
        width=panel_width,
        padding=(0, 1),
    )

    # Display data visualizations
    viz_row = Columns([bar_chart, pie_chart], equal=True)
    viz_layout = Group(viz_row, metrics_dashboard)
    console._rich_console.print(Align(viz_layout, align="center"))
    console.newline(2)

    # ==============================================================================
    # PRE-FORMATTED CONTENT DEMO
    # ==============================================================================
    # Demonstrate passing a pre-formatted Rich Text into console.frame so the
    # rendering engine does not apply additional internal formatting. This
    # enables complex formats (gradients per-char/line, JSON-like blocks, etc.)
    raw = ":rocket: Release v0.3.0\n:chart_with_upwards_trend: Q4 Targets achieved"
    expanded = expand_emoji_shortcodes(raw)
    grad = gradient_markup(expanded, "magenta", "bright_yellow", per="line")
    rich_content = Text.from_markup(grad)

    console.frame(
        rich_content,
        title="🧩 Preformatted Content",
        border="double",
        border_color="bright_magenta",
        padding=1,
    )
    console.newline(2)

    # ==============================================================================
    # FINAL SUMMARY
    # ==============================================================================
    console.frame(
        "v0.3.0: Comprehensive Rich-Native Showcase\n"
        "10 sections demonstrating advanced terminal UI capabilities!\n"
        "🎨 Perfect alignment | 🏗️ Nested layouts | 📊 Complex grids\n"
        "📈 Data visualization | 🎭 Advanced typography | 🚀 Dynamic dashboards\n"
        "No ANSI wrapping bugs! All Rich-powered! 🎉",
        title="🎊 Showcase Complete - 10 Advanced Sections!",
        border="double",
        border_color="bright_green",
        content_color="bright_white",
        align="center",
        padding=2,
    )
    console.newline()


if __name__ == "__main__":
    main()
