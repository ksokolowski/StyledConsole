#!/usr/bin/env python3
"""
Quick Start Example
===================

A simple demonstration of StyledConsole's core features.
For more extensive examples, visit:
https://github.com/ksokolowski/StyledConsole-Examples
"""

from styledconsole import Console, EffectSpec, icons


def main():
    console = Console()

    # 1. High-impact Banner
    console.banner(
        "StyledConsole", effect=EffectSpec.gradient("dodgerblue", "cyan"), border="double"
    )

    # 2. Styled Frame with Features
    console.frame(
        [
            f"{icons.CHECK_MARK_BUTTON}  Easy to use",
            f"{icons.ROCKET}  High performance",
            f"{icons.SPARKLES}  Beautiful output",
            f"{icons.GEAR}  Policy-aware rendering",
        ],
        title=f"{icons.STAR} Core Features",
        border="double",
        effect=EffectSpec.gradient("cyan", "blue"),
        border_gradient_end="blue",
        padding=1,
    )

    # 3. Invitation and Link
    console.text("\nExplore more elaborate examples at:", color="yellow", bold=True)
    console.text(
        "👉 https://github.com/ksokolowski/StyledConsole-Examples",
        color="cyan",
        italic=True,
    )


if __name__ == "__main__":
    main()
