#!/usr/bin/env python
"""Rainbow Fat Alignment Showcase (v0.3.0 - Rich Native).

Advanced example demonstrating:
- Large, colorful banners with rainbow gradients
- Emoji integration throughout layout
- All three alignment types: left, center, right
- Rich Panel and Align for perfect ANSI handling
- Border gradients and color combinations

v0.3.0: Completely refactored to use Rich's native renderables.
No more manual string manipulation - all ANSI-safe!
"""

from rich.align import Align
from rich.panel import Panel
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


def main() -> None:
    """Main showcase function."""
    console = Console()
    terminal_width = console._rich_console.width

    # Frame width for panels
    panel_width = min(70, terminal_width // 2)

    console.newline()

    # ==============================================================================
    # HEADER
    # ==============================================================================
    console.frame(
        "Demonstrating Left, Center, and Right alignment with Rich Panel",
        title="🎨 Alignment Showcase (v0.3.0)",
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
    # FOOTER
    # ==============================================================================
    console.frame(
        "v0.3.0: Powered by Rich Panel + Align\nNo ANSI wrapping bugs! 🎉",
        title="✅ Perfect Alignment Achieved",
        border="double",
        border_color="green",
        content_color="bright_green",
        align="center",
        padding=2,
    )
    console.newline()


if __name__ == "__main__":
    main()
