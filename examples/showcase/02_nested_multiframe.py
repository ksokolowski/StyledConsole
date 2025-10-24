#!/usr/bin/env python
"""Multinested frames showcase.

This standalone example demonstrates several nesting patterns using Rich
renderables via the StyledConsole facade: side-by-side outer frames, stacked
frames, deep nesting (panel -> panel -> panel), banners and multiline
gradient titles, emoji expansion and per-line/per-char gradients.

Run with: PYTHONPATH=src python examples/showcase/02_nested_multiframe.py
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


def expand_emoji_shortcodes(text: str) -> str:
    mapping = {
        ":rocket:": "🚀",
        ":sparkles:": "✨",
        ":fire:": "🔥",
        ":chart_with_upwards_trend:": "📈",
        ":gear:": "⚙️",
        ":star:": "⭐",
        ":bulb:": "💡",
    }
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


def gradient_markup(text: str, start_color: str, end_color: str, per: str = "line") -> str:
    """Simple gradient markup helper that uses styledconsole color utils when available."""
    try:
        from styledconsole.utils.color import interpolate_color
    except Exception:
        # fallback - single color
        return f"[{start_color}]" + text + "[/]"

    if per == "line":
        lines = text.split("\n")
        out = []
        for i, line in enumerate(lines):
            ratio = i / (len(lines) - 1) if len(lines) > 1 else 0
            c = interpolate_color(start_color, end_color, ratio)
            out.append(f"[{c}]{line}[/]")
        return "\n".join(out)
    else:
        # per-char
        chars = list(text)
        out = []
        n = len(chars)
        for i, ch in enumerate(chars):
            ratio = i / (n - 1) if n > 1 else 0
            c = interpolate_color(start_color, end_color, ratio)
            out.append(f"[{c}]{ch}[/]")
        return "".join(out)


def make_inner_panel(content: str, title: str, start: str, end: str, width: int):
    expanded = expand_emoji_shortcodes(content)
    grad = gradient_markup(expanded, start, end, per="line")
    return Panel(
        Text.from_markup(grad),
        title=title,
        box=get_box_style("rounded"),
        border_style=start,
        width=width,
    )


def banner_lines(text: str, width: int = 60):
    b = BannerRenderer()
    return b.render(text, font="small", start_color="magenta", end_color="cyan", width=width)


def main() -> None:
    console = Console()
    w = console._rich_console.width

    outer_width = min(72, max(48, w - 10))
    inner_w = max(16, (outer_width - 6) // 2)

    # Simple banner (multiline gradient title) — avoid complex pyfiglet banner
    title_plain = "MULTINEST\nSHOWCASE\n2025"
    title_markup = gradient_markup(title_plain, "magenta", "cyan", per="line")
    banner_text = Text.from_markup(title_markup)

    # Build first set (side-by-side + stacked)
    # Make inner panels have more lines to showcase gradient effects
    a_content = (
        ":sparkles: A\n"
        "CPU: 12%\n"
        "Mem: 1.1GB\n"
        "Uptime: 99.99%\n"
        "Threads: 8\n"
        "Load: 0.24\n"
        "Cache: 75%\n"
        "Req/s: 1234\n"
        "Errors: 0\n"
        "Warnings: 0"
    )

    b_content = (
        ":fire: B\n"
        "Errors: 0\n"
        "Warnings: 1\n"
        "Alerts: 2\n"
        "Retries: 5\n"
        "Latency: 45ms\n"
        "Throughput: 1.2k/s\n"
        "Active: 64\n"
        "Queue: 3\n"
        "Notes: nominal"
    )

    a = make_inner_panel(a_content, "A", "red", "magenta", inner_w)
    b = make_inner_panel(b_content, "B", "yellow", "red", inner_w)

    side_table = Table.grid(padding=(0, 1))
    side_table.add_column()
    side_table.add_column()
    side_table.add_row(a, b)

    side_panel = Panel(
        side_table,
        title="Side-by-side",
        box=get_box_style("double"),
        border_style="bright_cyan",
        width=outer_width,
    )

    stacked_group = Group(Align(a, align="center"), Align(b, align="center"))
    stacked_panel = Panel(
        stacked_group,
        title="Stacked",
        box=get_box_style("double"),
        border_style="bright_green",
        width=max(inner_w + 8, 36),
    )

    outer1 = Panel(
        Group(Align(side_panel, align="center"), Align(stacked_panel, align="center")),
        title=banner_text,
        box=get_box_style("heavy"),
        border_style="bright_magenta",
        width=outer_width,
    )

    # Deeply nested example (panel inside panel inside panel)
    deep_content = (
        ":bulb: Idea\n"
        "Status: draft\n"
        "Owner: team-x\n"
        "Priority: medium\n"
        "ETA: Q4\n"
        "Notes: prototype\n"
        "Tests: pending\n"
        "Review: needed\n"
        "Score: 7/10\n"
        "Tags: feature,ui"
    )
    deep_inner = make_inner_panel(deep_content, "Inner", "bright_yellow", "yellow", inner_w)
    deep_mid = Panel(
        Align(deep_inner, align="center"),
        title="Mid",
        box=get_box_style("thick"),
        border_style="bright_blue",
        width=inner_w + 6,
    )
    deep_outer = Panel(
        Align(deep_mid, align="center"),
        title="Deeply Nested",
        box=get_box_style("double"),
        border_style="bright_green",
        width=deep_mid.width + 6,
    )

    # Another outer frame with different color scheme
    title2 = Text.from_markup(
        gradient_markup(expand_emoji_shortcodes(":rocket: MULTINEST 2"), "cyan", "blue", per="char")
    )
    metrics_text = gradient_markup(
        expand_emoji_shortcodes(":chart_with_upwards_trend: Metrics coming soon\nDetails incoming"),
        "bright_green",
        "bright_cyan",
        per="line",
    )
    outer2 = Panel(
        Group(Align(deep_outer, align="center"), Text.from_markup(metrics_text)),
        title=title2,
        box=get_box_style("heavy"),
        border_style="bright_blue",
        width=outer_width,
    )

    # Print two outer frames next to each other
    page = Columns([outer1, outer2], equal=True, expand=False)
    console._rich_console.print(Align(page, align="center"))


if __name__ == "__main__":
    main()
