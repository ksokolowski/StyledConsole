#!/usr/bin/env python3
"""
Banner Renderer Example

Demonstrates ASCII art banner rendering with pyfiglet fonts, gradient coloring,
and optional frame borders.
"""

from styledconsole import Banner, BannerRenderer

renderer = BannerRenderer()

print("=" * 80)
print("BANNER RENDERER EXAMPLES")
print("=" * 80)
print()

# Example 1: Simple banner with default font
print("1. Simple Banner (default 'standard' font):")
print()

for line in renderer.render("Hello"):
    print(line)
print()

# Example 2: Different fonts
print("2. Different Fonts:")
print()

fonts_to_show = ["slant", "banner", "big", "digital"]
for font in fonts_to_show:
    print(f"Font: {font}")
    for line in renderer.render("DEMO", font=font):
        print(line)
    print()

# Example 3: Gradient coloring
print("3. Gradient Coloring:")
print()

print("Red to Blue gradient:")
for line in renderer.render(
    "GRADIENT",
    font="slant",
    gradient_start="#ff0000",
    gradient_end="#0000ff",
):
    print(line)
print()

print("Green to Yellow gradient:")
for line in renderer.render(
    "COLORS",
    font="banner",
    gradient_start="green",
    gradient_end="yellow",
):
    print(line)
print()

# Example 4: Banner with border
print("4. Banner with Border:")
print()

for line in renderer.render(
    "FRAMED",
    font="slant",
    border="double",
):
    print(line)
print()

# Example 5: Gradient + Border
print("5. Gradient with Border:")
print()

for line in renderer.render(
    "SUCCESS",
    font="banner",
    gradient_start="#00ff00",
    gradient_end="#00ffff",
    border="heavy",
):
    print(line)
print()

# Example 6: Custom width and alignment
print("6. Custom Width and Alignment:")
print()

for line in renderer.render(
    "LEFT",
    font="slant",
    border="rounded",
    width=60,
    align="left",
):
    print(line)
print()

for line in renderer.render(
    "CENTER",
    font="slant",
    border="rounded",
    width=60,
    align="center",
):
    print(line)
print()

for line in renderer.render(
    "RIGHT",
    font="slant",
    border="rounded",
    width=60,
    align="right",
):
    print(line)
print()

# Example 7: Custom padding
print("7. Custom Padding:")
print()

for line in renderer.render(
    "PADDED",
    font="banner",
    border="solid",
    padding=3,
    gradient_start="red",
    gradient_end="orange",
):
    print(line)
print()

# Example 8: Using Banner dataclass
print("8. Using Banner Dataclass:")
print()

banner = Banner(
    text="BANNER",
    font="digital",
    gradient_start="#ff00ff",
    gradient_end="#00ffff",
    border="thick",
    width=70,
    align="center",
    padding=2,
)

for line in renderer.render_banner(banner):
    print(line)
print()

# Example 9: Emoji fallback (plain text rendering)
print("9. Emoji Fallback (renders as plain text):")
print()

for line in renderer.render(
    "🚀 Launch",
    gradient_start="red",
    gradient_end="blue",
    border="rounded",
):
    print(line)
print()

# Example 10: Font preview utility
print("10. Font Preview Utility:")
print()

print("Available fonts (first 20):")
fonts = renderer.list_fonts(limit=20)
print(", ".join(fonts))
print()

print("Preview 'small' font:")
preview = renderer.preview_font("small", "Sample")
print(preview)

# Example 11: Application titles
print("11. Application Title Banner:")
print()

for line in renderer.render(
    "StyledConsole",
    font="slant",
    gradient_start="dodgerblue",
    gradient_end="purple",
    border="double",
    width=80,
):
    print(line)
print()

# Example 12: Status messages
print("12. Status Message Banners:")
print()

# Success
for line in renderer.render(
    "SUCCESS",
    font="banner",
    gradient_start="#00ff00",
    gradient_end="#00aa00",
    border="heavy",
):
    print(line)
print()

# Error
for line in renderer.render(
    "ERROR",
    font="banner",
    gradient_start="#ff0000",
    gradient_end="#aa0000",
    border="heavy",
):
    print(line)
print()

# Warning
for line in renderer.render(
    "WARNING",
    font="banner",
    gradient_start="#ffaa00",
    gradient_end="#ff6600",
    border="heavy",
):
    print(line)
print()

print("=" * 80)
print("All banner examples complete!")
print("=" * 80)
