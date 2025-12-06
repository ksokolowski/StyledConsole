#!/usr/bin/env python3
"""
🌟 Safe Emojis Showcase

A comprehensive gallery of safe-to-use emojis available in StyledConsole.
These emojis are dynamically generated from the emoji package and filtered
for single-codepoint, width-2 characters for consistent terminal rendering.
"""

from rich.columns import Columns
from rich.text import Text

from styledconsole import Console
from styledconsole.utils.text import get_safe_emojis

console = Console()


def main():
    console.banner("SAFE EMOJIS", font="standard", start_color="cyan", end_color="blue")
    console.newline()

    from rich.align import Align

    console.print(
        Align.center(
            Text(
                "This gallery showcases safe emojis available in "
                "StyledConsole.\nThese emojis are width-2 and "
                "single-codepoint for maximum compatibility.",
                style="green italic",
            )
        )
    )
    console.newline(2)

    # Get safe emojis dynamically
    safe_emojis = get_safe_emojis()

    # Create a simple list of emojis (no category in dynamic mode)
    console.rule(f"All Safe Emojis ({len(safe_emojis)})", color="cyan", align="left")
    console.newline()

    # Create renderables for Columns
    # Format: "Emoji  name"
    renderables = []
    for char, info in list(safe_emojis.items())[:200]:  # Limit to first 200 for display
        name = info.get("name", "")
        # Truncate name if too long to keep columns tidy
        display_name = name[:20] + "..." if len(name) > 20 else name
        text = Text(f"{char}  {display_name}", style="white")
        renderables.append(text)

    # Print using Rich Columns via console.print
    console.print(Columns(renderables, equal=True, expand=True, column_first=True))
    console.newline(2)

    console.rule("End of Gallery", color="blue")
    console.print(Align.center(Text(f"Total Safe Emojis: {len(safe_emojis)}", style="cyan bold")))
    console.newline()


if __name__ == "__main__":
    main()
