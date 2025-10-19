#!/usr/bin/env python3
"""
Banner Rendering Example

Demonstrates ASCII art banner rendering with pyfiglet fonts, gradient coloring,
and optional frame borders using the Console API.

Pro Tip: For advanced banner customization, you can use BannerRenderer directly.
"""

from styledconsole import Banner, BannerRenderer, Console

console = Console()

console.rule("BANNER RENDERING EXAMPLES", style="bold cyan")
console.newline()

# Example 1: Simple banner with default font
console.text("1. Simple Banner (default 'standard' font):", bold=True)
console.newline()

console.banner("Hello")
console.newline()

# Example 2: Different fonts
console.text("2. Different Fonts:", bold=True)
console.newline()

fonts_to_show = ["slant", "banner", "big", "digital"]
for font in fonts_to_show:
    console.text(f"Font: {font}", color="cyan")
    console.banner("DEMO", font=font)
    console.newline()

# Example 3: Gradient coloring
console.text("3. Gradient Coloring:", bold=True)
console.newline()

console.text("Red to Blue gradient:", color="magenta")
console.banner(
    "GRADIENT",
    font="slant",
    gradient_start="red",
    gradient_end="blue",
)
console.newline()

console.text("Green to Yellow gradient:", color="magenta")
console.banner(
    "COLORS",
    font="banner",
    gradient_start="green",
    gradient_end="yellow",
)
console.newline()

# Example 4: Banner with border
console.text("4. Banner with Border:", bold=True)
console.newline()

console.banner(
    "FRAMED",
    font="slant",
    border="double",
)
console.newline()

# Example 5: Gradient + Border
console.text("5. Gradient with Border:", bold=True)
console.newline()

console.banner(
    "SUCCESS",
    font="banner",
    gradient_start="lime",
    gradient_end="cyan",
    border="heavy",
)
console.newline()

# Example 6: Custom width and alignment
console.text("6. Custom Width and Alignment:", bold=True)
console.newline()

console.banner(
    "LEFT",
    font="slant",
    border="rounded",
    width=60,
    align="left",
)
console.newline()

console.banner(
    "CENTER",
    font="slant",
    border="rounded",
    width=60,
    align="center",
)
console.newline()

console.banner(
    "RIGHT",
    font="slant",
    border="rounded",
    width=60,
    align="right",
)
console.newline()

# Example 7: Custom padding
console.text("7. Custom Padding:", bold=True)
console.newline()

console.banner(
    "PADDED",
    font="banner",
    border="solid",
    padding=3,
    gradient_start="red",
    gradient_end="orange",
)
console.newline()

# Example 8: Direct Banner dataclass with Console
console.text("8. Using Banner with Console:", bold=True)
console.newline()

banner = Banner(
    text="BANNER",
    font="digital",
    gradient_start="magenta",
    gradient_end="cyan",
    border="thick",
    width=70,
    align="center",
    padding=2,
)

console.banner(
    banner.text,
    font=banner.font,
    gradient_start=banner.gradient_start,
    gradient_end=banner.gradient_end,
    border=banner.border,
    width=banner.width,
    align=banner.align,
    padding=banner.padding,
)
console.newline()

# Example 9: Emoji fallback (plain text rendering)
console.text("9. Emoji Fallback (renders as plain text):", bold=True)
console.newline()

console.banner(
    "🚀 Launch",
    gradient_start="red",
    gradient_end="blue",
    border="rounded",
)
console.newline()

# Example 10: Font preview utility (using BannerRenderer for utility methods)
console.text("10. Font Preview Utility:", bold=True)
console.newline()

renderer = BannerRenderer()

console.text("Available fonts (first 20):", color="yellow")
fonts = renderer.list_fonts(limit=20)
console.text(", ".join(fonts))
console.newline()

console.text("Preview 'small' font:", color="yellow")
preview = renderer.preview_font("small", "Sample")
console.print(preview)

# Example 11: Application titles
console.text("11. Application Title Banner:", bold=True)
console.newline()

console.banner(
    "StyledConsole",
    font="slant",
    gradient_start="dodgerblue",
    gradient_end="purple",
    border="double",
    width=80,
)
console.newline()

# Example 12: Status messages
console.text("12. Status Message Banners:", bold=True)
console.newline()

# Success
console.banner(
    "SUCCESS",
    font="banner",
    gradient_start="lime",
    gradient_end="darkgreen",
    border="heavy",
)
console.newline()

# Error
console.banner(
    "ERROR",
    font="banner",
    gradient_start="red",
    gradient_end="darkred",
    border="heavy",
)
console.newline()

# Warning
console.banner(
    "WARNING",
    font="banner",
    gradient_start="orange",
    gradient_end="orangered",
    border="heavy",
)
console.newline()

console.rule("All banner examples complete!", style="bold green")
