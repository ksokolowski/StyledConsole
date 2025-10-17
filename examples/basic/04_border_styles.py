#!/usr/bin/env python3
"""
Border Styles Example

Demonstrates all 8 predefined border styles available in StyledConsole.
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
    get_border_style,
    list_border_styles,
)

print("=" * 70)
print("BORDER STYLES GALLERY")
print("=" * 70)
print()

# Display all available styles
print("Available border styles:")
print(", ".join(list_border_styles()))
print()
print("=" * 70)
print()

# Showcase each style
styles = [
    (SOLID, "SOLID", "Classic Unicode box-drawing characters"),
    (DOUBLE, "DOUBLE", "Double-line borders for emphasis"),
    (ROUNDED, "ROUNDED", "Smooth rounded corners for modern look"),
    (HEAVY, "HEAVY", "Bold heavy lines for strong emphasis"),
    (THICK, "THICK", "Thick lines with rounded corners"),
    (ASCII, "ASCII", "Universal ASCII compatibility"),
    (MINIMAL, "MINIMAL", "Clean minimal horizontal lines"),
    (DOTS, "DOTS", "Dotted lines for subtle separation"),
]

width = 60

for style, name, description in styles:
    print(style.render_top_border(width, f"✨ {name} Style"))
    print(style.render_line(width, description, align="center"))
    print(style.render_line(width, "", align="center"))
    print(style.render_line(width, "Sample content line", align="left"))
    print(style.render_divider(width))
    print(style.render_line(width, "With divider support", align="right"))
    print(style.render_bottom_border(width))
    print()

# Example: Dynamic style selection
print("=" * 70)
print("DYNAMIC STYLE SELECTION")
print("=" * 70)
print()

# Get style by name (case-insensitive)
style_name = "rounded"
style = get_border_style(style_name)

print(f"Selected style: '{style_name}' (case-insensitive)")
print(style.render_top_border(60, f"Using get_border_style('{style_name}')"))
print(style.render_line(60, "Styles can be selected dynamically by name", align="center"))
print(style.render_bottom_border(60))
print()

# Show it works with different cases
for case_variant in ["SOLID", "solid", "SoLiD"]:
    style = get_border_style(case_variant)
    print(style.render_top_border(40, f"'{case_variant}'"))
    print(style.render_line(40, "Case doesn't matter!", align="center"))
    print(style.render_bottom_border(40))
    print()
