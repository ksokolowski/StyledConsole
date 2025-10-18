#!/usr/bin/env python3
"""
Border Styles Example

Demonstrates all 8 predefined border styles available in StyledConsole.
"""

from styledconsole import FrameRenderer, list_border_styles

renderer = FrameRenderer()

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
    ("solid", "SOLID", "Classic Unicode box-drawing characters"),
    ("double", "DOUBLE", "Double-line borders for emphasis"),
    ("rounded", "ROUNDED", "Smooth rounded corners for modern look"),
    ("heavy", "HEAVY", "Bold heavy lines for strong emphasis"),
    ("thick", "THICK", "Thick lines with rounded corners"),
    ("ascii", "ASCII", "Universal ASCII compatibility"),
    ("minimal", "MINIMAL", "Clean minimal horizontal lines"),
    ("dots", "DOTS", "Dotted lines for subtle separation"),
]

width = 60

for style_name, display_name, description in styles:
    content = [
        description,
        "",
        "Sample content line",
    ]
    for line in renderer.render(
        content,
        title=f"✨ {display_name} Style",
        border=style_name,
        width=width,
        align="center",
    ):
        print(line)
    print()

# Example: Dynamic style selection
print("=" * 70)
print("DYNAMIC STYLE SELECTION")
print("=" * 70)
print()

# Styles can be selected dynamically by name (case-insensitive)
style_name = "rounded"
print(f"Selected style: '{style_name}' (case-insensitive)")
for line in renderer.render(
    "Styles can be selected dynamically by name",
    title=f"Using border='{style_name}'",
    border=style_name,
    width=60,
    align="center",
):
    print(line)
print()

# Show it works with different cases
for case_variant in ["SOLID", "solid", "SoLiD"]:
    for line in renderer.render(
        "Case doesn't matter!",
        title=f"'{case_variant}'",
        border=case_variant,
        width=40,
        align="center",
    ):
        print(line)
    print()
