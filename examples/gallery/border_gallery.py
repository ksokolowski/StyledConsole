#!/usr/bin/env python3
"""
Border Gallery

A visual catalog of all StyledConsole border styles with detailed character sets.
Perfect for choosing the right style for your application.
"""

from styledconsole import (
    ASCII,
    DOTS,
    DOUBLE,
    HEAVY,
    MINIMAL,
    ROUNDED,
    SOLID,
    THICK,
    list_border_styles,
)

print()
print("=" * 90)
print(" " * 30 + "🎨 BORDER GALLERY 🎨")
print("=" * 90)
print()

# Gallery entry for each style
styles = [
    (SOLID, "SOLID", "Classic Unicode box-drawing", "Professional, universal"),
    (DOUBLE, "DOUBLE", "Double-line borders", "Emphasis, importance"),
    (ROUNDED, "ROUNDED", "Smooth rounded corners", "Modern, friendly"),
    (HEAVY, "HEAVY", "Bold heavy weight", "Strong emphasis, alerts"),
    (THICK, "THICK", "Thick with curves", "Bold yet friendly"),
    (ASCII, "ASCII", "Pure ASCII characters", "Maximum compatibility"),
    (MINIMAL, "MINIMAL", "Minimal horizontal lines", "Clean, subtle"),
    (DOTS, "DOTS", "Dotted separators", "Delicate, unobtrusive"),
]

width = 80

for style, name, description, use_case in styles:
    # Header
    print(style.render_top_border(width, f"✨ {name}"))
    print(style.render_line(width, "", align="center"))

    # Description
    print(style.render_line(width, description, align="center"))
    print(style.render_line(width, f"Use case: {use_case}", align="center"))
    print(style.render_line(width, "", align="center"))

    # Character set display
    print(style.render_divider(width))
    print(style.render_line(width, "", align="center"))

    chars = f"Corners: '{style.top_left}{style.top_right}{style.bottom_left}{style.bottom_right}'  "
    chars += f"Lines: '{style.horizontal}{style.vertical}'  "
    chars += f"Joints: '{style.left_joint}{style.right_joint}{style.top_joint}{style.bottom_joint}'"

    print(style.render_line(width, chars, align="center"))
    print(style.render_line(width, "", align="center"))

    # Sample content
    print(style.render_divider(width))
    print(style.render_line(width, "Sample left-aligned content", align="left"))
    print(style.render_line(width, "Sample centered content", align="center"))
    print(style.render_line(width, "Sample right-aligned content", align="right"))

    # Footer
    print(style.render_bottom_border(width))
    print()

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
