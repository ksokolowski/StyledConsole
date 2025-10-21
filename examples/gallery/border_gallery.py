#!/usr/bin/env python3
"""
Border Gallery (v0.3.0 - Rich Native)

A visual catalog of all StyledConsole border styles with detailed character sets.
Perfect for choosing the right style for your application.

v0.3.0: Updated to use Console.frame() which internally uses Rich Panel.
"""

from styledconsole import Console, get_border_style, list_border_styles

console = Console()

print()
print("=" * 90)
print(" " * 30 + "🎨 BORDER GALLERY 🎨")
print("=" * 90)
print()

# Gallery entry for each style
styles = [
    ("solid", "SOLID", "Classic Unicode box-drawing", "Professional, universal"),
    ("double", "DOUBLE", "Double-line borders", "Emphasis, importance"),
    ("rounded", "ROUNDED", "Smooth rounded corners", "Modern, friendly"),
    ("heavy", "HEAVY", "Bold heavy weight", "Strong emphasis, alerts"),
    ("thick", "THICK", "Thick with curves", "Bold yet friendly"),
    ("ascii", "ASCII", "Pure ASCII characters", "Maximum compatibility"),
    ("minimal", "MINIMAL", "Minimal horizontal lines", "Clean, subtle"),
    ("dots", "DOTS", "Dotted separators", "Delicate, unobtrusive"),
]

width = 80

for style_name, display_name, description, use_case in styles:
    # Get the BorderStyle object to show character details
    style = get_border_style(style_name)

    # Build content with character information
    chars = f"Corners: '{style.top_left}{style.top_right}{style.bottom_left}{style.bottom_right}'  "
    chars += f"Lines: '{style.horizontal}{style.vertical}'  "
    chars += f"Joints: '{style.left_joint}{style.right_joint}{style.top_joint}{style.bottom_joint}'"

    content = "\n".join(
        [
            "",
            description,
            f"Use case: {use_case}",
            "",
            chars,
            "",
            "Sample left-aligned content",
            "Sample centered content",
            "Sample right-aligned content",
        ]
    )

    # Use Console.frame() which internally uses Rich Panel
    console.frame(
        content,
        title=f"✨ {display_name}",
        border=style_name,
        width=width,
        align="center",
    )
    console.newline()

# Summary
print("=" * 90)
print()
print(f"Total styles available: {len(list_border_styles())}")
print(f"Styles: {', '.join(list_border_styles())}")
print()
print("All styles support:")
print("  ✅ Emoji-safe rendering with visual_width() calculations")
print("  ✅ Left, center, and right alignment")
print("  ✅ Titles in top borders")
print("  ✅ Horizontal dividers")
print("  ✅ Perfect visual alignment regardless of content")
print()
print("=" * 90)
print()
