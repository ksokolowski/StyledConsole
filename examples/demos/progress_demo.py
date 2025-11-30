#!/usr/bin/env python3
"""Progress Bar Demo - Demonstrates styled progress bars.

Shows how to use the StyledProgress wrapper for rich progress bars
with theme integration.
"""

import time

from styledconsole import EMOJI, THEMES, Console


def main() -> None:
    """Demonstrate progress bar functionality."""
    console = Console()
    console.banner("PROGRESS", font="slant", start_color="cyan", end_color="blue")
    console.text("")

    # Basic progress bar
    console.text(f"{EMOJI.ROCKET} Basic Progress Bar:", bold=True)
    with console.progress() as progress:
        task = progress.add_task("Downloading files", total=100)
        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)
    console.text(f"  {EMOJI.CHECK} Complete!\n")

    # Multiple tasks
    console.text(f"{EMOJI.SPARKLES} Multiple Tasks:", bold=True)
    with console.progress() as progress:
        task1 = progress.add_task("Task 1: Fetching data", total=50)
        task2 = progress.add_task("Task 2: Processing", total=75)
        task3 = progress.add_task("Task 3: Saving", total=100)

        for _ in range(100):
            time.sleep(0.01)
            if not progress.finished:
                progress.update(task1, advance=0.5)
                progress.update(task2, advance=0.75)
                progress.update(task3, advance=1)
    console.text(f"  {EMOJI.CHECK} All tasks complete!\n")

    # Indeterminate progress (spinner)
    console.text(f"{EMOJI.WHITE_CIRCLE} Indeterminate Progress:", bold=True)
    with console.progress() as progress:
        task = progress.add_task("Connecting...", total=None)
        for i in range(30):
            time.sleep(0.05)
            if i == 15:
                progress.update(task, description="Authenticating...")
            if i == 25:
                progress.update(task, description="Almost done...")
    console.text(f"  {EMOJI.CHECK} Connected!\n")

    # Theme-aware progress
    console.text(f"{EMOJI.PALETTE} Themed Progress Bars:", bold=True)
    for theme_name in ["DARK", "MONOKAI", "NORD"]:
        theme = THEMES.get_theme(theme_name)
        themed_console = Console(theme=theme)
        themed_console.text(f"  Theme: {theme_name}")

        with console.progress() as progress:
            task = progress.add_task(f"Processing with {theme_name}", total=50)
            for _ in range(50):
                time.sleep(0.01)
                progress.update(task, advance=1)

    console.text(f"\n{EMOJI.PARTY} All progress demos complete!")


if __name__ == "__main__":
    main()
