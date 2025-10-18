#!/usr/bin/env python3
"""
Border Styles Example

Demonstrates all 8 predefined border styles available in StyledConsole.
Shows Console API usage with different border styles.
"""

from styledconsole import Console, list_border_styles

console = Console()

print("=" * 70)
print("BORDER STYLES GALLERY")
print("=" * 70)
print()

# Display all available styles
console.text("Available border styles:", bold=True)
console.text(", ".join(list_border_styles()), color="cyan")
print()
console.rule(style="solid")
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
    console.frame(
        content,
        title=f"✨ {display_name} Style",
        border=style_name,
        width=width,
        align="center",
    )
    print()

# Example: Dynamic style selection
console.rule("DYNAMIC STYLE SELECTION", color="cyan")
print()

# Styles can be selected dynamically by name (case-insensitive)
style_name = "rounded"
console.text(f"Selected style: '{style_name}' (case-insensitive)", bold=True)
console.frame(
    "Styles can be selected dynamically by name",
    title=f"Using border='{style_name}'",
    border=style_name,
    width=60,
    align="center",
)
print()

# Show it works with different cases
for case_variant in ["SOLID", "solid", "SoLiD"]:
    console.frame(
        "Case doesn't matter!",
        title=f"'{case_variant}'",
        border=case_variant,
        width=40,
        align="center",
    )
    print()
