#!/usr/bin/env python3
"""
HTML Export Demo
===============

Demonstrates exporting a rich dashboard to HTML with custom styling and gradients.
"""

import os

from rich.terminal_theme import MONOKAI

from styledconsole import Console


def create_dashboard(console: Console) -> None:
    """Render a complex dashboard to the console."""

    # 1. Gradient Banner
    console.banner(
        "SYSTEM STATUS", start_color="dodgerblue", end_color="cyan", border="double", align="center"
    )

    # 2. Status Grid
    # Note: ⚠️ renders as width-1 in terminals but width-2 in browsers (with VS16)
    # This causes unavoidable differences between terminal and HTML output
    metrics_lines = [
        "CPU Load      42%        🟢",
        "Memory        1.2GB      🟢",
        "Disk          85%        ⚠️",  # Best compromise for both terminal and browser
        "Network       120ms      🔴",
    ]

    # 3. Framed Content with Metrics
    console.frame(
        metrics_lines, title="Metrics", border="rounded", border_color="blue", title_color="cyan"
    )

    # 4. Gradient Text
    console.text("System analysis complete. No critical errors found.", color="green")


def main():
    # Initialize console with recording enabled
    console = Console(record=True, width=100)

    print("Rendering dashboard...")
    create_dashboard(console)

    # Custom CSS to enhance the HTML output
    custom_css = """
    body {
        font-family: 'Fira Code', monospace;
        background-color: #1a1a1a;
        margin: 2rem;
    }
    .rich-terminal {
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border-radius: 8px;
        padding: 2rem;
        background-color: #222;
    }
    """

    output_file = "dashboard_export.html"

    print(f"Exporting to {output_file}...")

    # Export using the enhanced ExportManager (accessed via console.export_html)
    # Note: Console.export_html delegates to RichConsole.export_html,
    # but we want to use our ExportManager logic.
    # Wait, Console doesn't expose ExportManager directly.
    # We should use ExportManager explicitly for this demo to show its features.

    from styledconsole.core.export_manager import ExportManager

    manager = ExportManager(console._rich_console)

    html = manager.export_html(
        page_title="System Status Dashboard",
        theme=MONOKAI,
        theme_css=custom_css,
        inline_styles=True,
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Export complete! Open {output_file} in your browser.")
    print(f"File path: {os.path.abspath(output_file)}")


if __name__ == "__main__":
    main()
