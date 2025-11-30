#!/usr/bin/env python3
"""
🌟 Safe Emojis Showcase

A comprehensive gallery of all 1000+ safe-to-use emojis available in StyledConsole.
These emojis are verified to be single-codepoint and width-2, ensuring consistent
rendering across most terminals.
"""

from rich.columns import Columns
from rich.text import Text

from styledconsole import Console
from styledconsole.utils.text import SAFE_EMOJIS

console = Console()


def main():
    console.banner("SAFE EMOJIS", font="standard", start_color="cyan", end_color="blue")
    console.newline()

    from rich.align import Align

    console.print(
        Align.center(
            Text(
                "This gallery showcases all verified safe emojis available in "
                "StyledConsole.\nThese emojis are guaranteed to be width-2 and "
                "single-codepoint for maximum compatibility.",
                style="green italic",
            )
        )
    )
    console.newline(2)

    # Group emojis by category
    categories = {}
    for char, info in SAFE_EMOJIS.items():
        category = info.get("category", "uncategorized")
        if category not in categories:
            categories[category] = []
        categories[category].append((char, info["name"]))

    # Sort categories and display
    sorted_categories = sorted(categories.keys())

    for category in sorted_categories:
        items = categories[category]
        count = len(items)

        # Title for the category
        console.rule(f"{category.title()} ({count})", color="cyan", align="left")
        console.newline()

        # Create renderables for Columns
        # Format: "Emoji  name"
        renderables = []
        for char, name in items:
            # Truncate name if too long to keep columns tidy
            display_name = name[:20] + "..." if len(name) > 20 else name
            text = Text(f"{char}  {display_name}", style="white")
            renderables.append(text)

        # Print using Rich Columns via console.print
        # optimal_width calculation or just letting Rich handle it
        console.print(Columns(renderables, equal=True, expand=True, column_first=True))
        console.newline(2)

    console.rule("End of Gallery", color="blue")
    console.print(Align.center(Text(f"Total Safe Emojis: {len(SAFE_EMOJIS)}", style="cyan bold")))
    console.newline()


if __name__ == "__main__":
    main()
