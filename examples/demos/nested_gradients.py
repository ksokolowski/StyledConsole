#!/usr/bin/env python3
"""
🏛️ Nested Gradient Architecture Showcase

Demonstrates the power of StyledConsole's rendering engine by nesting
multiple frames with independent gradient borders.

Structure:
1. Fire Layer (Outer)
2. Growth Layer
3. Depth Layer
4. Soul Layer (Inner)
"""

from styledconsole import Console

console = Console()


def main():
    console.clear()
    console.newline(2)

    # 4. Soul Layer (Innermost)
    # Meaning: The core essence
    soul_content = "This is gradient architecture at its finest."
    soul_frame = console.render_frame(
        soul_content,
        border="double",
        align="center",
        width=50,
        padding=1,
        border_gradient_start="#E6E6FA",  # Lavender
        border_gradient_end="#9370DB",  # Medium Purple
        border_gradient_direction="vertical",
    )

    # 3. Depth Layer
    # Meaning: Complexity and understanding
    depth_frame = console.render_frame(
        [
            "Four gradient layers, each with meaning:",
            "Fire → Growth → Depth → Soul",
            "",
            soul_frame,
        ],
        border="rounded",
        align="center",
        width=58,
        padding=1,
        border_gradient_start="#4169E1",  # Royal Blue
        border_gradient_end="#000080",  # Navy
        border_gradient_direction="vertical",
    )

    # 2. Growth Layer
    # Meaning: Expansion and development
    growth_frame = console.render_frame(
        [
            "Native Implementation",
            "Rendering Engine v0.5.0",
            "",
            depth_frame,
        ],
        border="thick",
        align="center",
        width=66,
        padding=1,
        border_gradient_start="#90EE90",  # Light Green
        border_gradient_end="#006400",  # Dark Green
        border_gradient_direction="vertical",
    )

    # 1. Fire Layer (Outermost)
    # Meaning: Passion and energy
    # Render and print the final result
    console.frame(
        [
            "🌈 NESTED GRADIENT ARCHITECTURE",
            "",
            growth_frame,
        ],
        title="🏛️  Gradient Architecture",
        border="heavy",
        align="center",
        width=76,
        padding=2,
        border_gradient_start="#FF4500",  # Orange Red
        border_gradient_end="#8B0000",  # Dark Red
        border_gradient_direction="vertical",
    )

    console.newline(2)


if __name__ == "__main__":
    main()
