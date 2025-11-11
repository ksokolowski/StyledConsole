#!/usr/bin/env python3
"""
Console Frame Examples (v0.3.0 - Rich Native)

Demonstrates Console.frame() usage - the main API for creating styled frames.

Console.frame() internally uses Rich Panel for perfect ANSI-safe rendering.
All alignment and color handling is automatic.

For advanced composition, you can also use Rich Panel directly.
"""

from rich.align import Align
from rich.panel import Panel

from styledconsole import Console
from styledconsole.core.box_mapping import get_box_style

print("=" * 70)
print("CONSOLE FRAME EXAMPLES (v0.3.0)")
print("=" * 70)
print()

console = Console()

# Example 1: Simple frame
print("1. Simple Frame:")
console.frame("Hello, StyledConsole!")
print()

# Example 2: Frame with title and border style
print("2. Frame with Title and Double Border:")
console.frame(
    "This is the content",
    title="My Frame",
    border="double",
)
print()

# Example 3: Multi-line content
print("3. Multi-line Content:")
content = "\n".join(
    [
        "Line 1: Introduction",
        "Line 2: Main content",
        "Line 3: Conclusion",
    ]
)
console.frame(content, title="Document", border="rounded")
print()

# Example 4: Custom width and padding
print("4. Custom Width and Padding:")
console.frame(
    "Padded content",
    width=50,
    padding=3,
    border="heavy",
)
print()

# Example 5: Different alignments
print("5. Content Alignment:")
for align in ["left", "center", "right"]:
    console.frame(
        f"Aligned: {align}",
        title=f"{align.upper()} align",
        width=40,
        align=align,
        border="solid",
    )
    print()

# Example 6: Emoji support
print("6. Emoji Support:")
console.frame(
    "🚀 Rocket Launch\n🎉 Celebration\n✨ Magic",
    title="🎨 Emoji Frame",
    border="rounded",
    align="center",
)
print()

# Example 7: Colors
print("7. Colored Borders and Content:")
console.frame(
    "Colorful frame with blue content",
    title="🌈 Colors",
    border="double",
    border_color="cyan",
    content_color="blue",
    width=50,
)
print()

# Example 8: All border styles
print("8. All Border Styles:")
for border in ["solid", "double", "rounded", "heavy", "thick", "ascii", "minimal", "dots"]:
    console.frame(
        f"This uses the '{border}' border style",
        title=border.upper(),
        border=border,
        width=50,
    )
    print()

# Example 9: Advanced - Using Rich Panel directly
print("9. Advanced: Direct Rich Panel Usage:")

# Create a Panel manually for advanced composition
panel = Panel(
    "[bold cyan]Direct Rich Panel[/bold cyan]\nWith Rich markup support!",
    title="⚡ Advanced",
    box=get_box_style("double"),
    border_style="magenta",
    padding=(0, 2),
)

# Print with center alignment
aligned = Align(panel, align="center")
console._rich_console.print(aligned)
print()

# Summary
console.frame(
    "✅ Console.frame() is the recommended API\n"
    "✅ Uses Rich Panel internally (no ANSI bugs)\n"
    "✅ Supports all border styles, colors, alignment\n"
    "✅ Can compose with Rich Group/Align for layouts",
    title="💡 Summary",
    border="double",
    border_color="green",
    width=70,
)
