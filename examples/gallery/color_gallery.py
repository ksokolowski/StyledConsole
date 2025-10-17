#!/usr/bin/env python3
"""
Color Gallery

Showcase of CSS4 color support in StyledConsole.
Displays color parsing capabilities and the full palette of 148 named colors.
"""

from styledconsole import (
    SOLID,
    get_color_names,
    parse_color,
    rgb_to_hex,
)

print()
print("=" * 80)
print(" " * 28 + "🎨 COLOR GALLERY 🎨")
print("=" * 80)
print()

# Color parsing examples
print(SOLID.render_top_border(75, "🎯 Color Parsing Examples"))
print(SOLID.render_line(75, "", align="center"))

examples = [
    ("Hex format:", "#FF0000, #f00", "parse_color('#FF0000') → (255, 0, 0)"),
    ("RGB format:", "rgb(0, 255, 0)", "parse_color('rgb(0,255,0)') → (0, 255, 0)"),
    ("Tuple format:", "(0, 0, 255)", "parse_color((0,0,255)) → (0, 0, 255)"),
    ("Named colors:", "red, blue, coral", "parse_color('coral') → (255, 127, 80)"),
]

for label, formats, example in examples:
    print(SOLID.render_line(75, f"{label:15} {formats}", align="left"))
    print(SOLID.render_line(75, f"                {example}", align="left"))
    print(SOLID.render_line(75, "", align="center"))

print(SOLID.render_bottom_border(75))
print()

# CSS4 Named Colors Showcase
all_colors = sorted(get_color_names())
print(SOLID.render_top_border(75, f"🌈 CSS4 Named Colors ({len(all_colors)} colors)"))
print(SOLID.render_line(75, "", align="center"))

# Group colors by category (simplified)
categories = {
    "Reds": [
        "red",
        "darkred",
        "indianred",
        "lightcoral",
        "salmon",
        "darksalmon",
        "lightsalmon",
        "crimson",
        "firebrick",
        "coral",
        "tomato",
        "orangered",
    ],
    "Blues": [
        "blue",
        "darkblue",
        "mediumblue",
        "navy",
        "midnightblue",
        "royalblue",
        "cornflowerblue",
        "lightsteelblue",
        "lightblue",
        "powderblue",
        "skyblue",
        "lightskyblue",
        "deepskyblue",
        "dodgerblue",
        "steelblue",
    ],
    "Greens": [
        "green",
        "darkgreen",
        "lime",
        "limegreen",
        "springgreen",
        "mediumspringgreen",
        "lightgreen",
        "palegreen",
        "darkseagreen",
        "seagreen",
        "mediumseagreen",
        "forestgreen",
        "olive",
        "olivedrab",
        "darkolivegreen",
    ],
    "Purples": [
        "purple",
        "indigo",
        "darkviolet",
        "blueviolet",
        "mediumviolet",
        "violet",
        "plum",
        "thistle",
        "lavender",
        "orchid",
        "mediumorchid",
        "darkorchid",
    ],
    "Yellows/Oranges": [
        "yellow",
        "gold",
        "orange",
        "darkorange",
        "lightyellow",
        "lemonchiffon",
        "lightgoldenrodyellow",
        "papayawhip",
        "moccasin",
        "peachpuff",
        "palegoldenrod",
    ],
    "Pinks": ["pink", "lightpink", "hotpink", "deeppink", "palevioletred", "mediumvioletred"],
    "Grays": [
        "gray",
        "grey",
        "darkgray",
        "darkgrey",
        "dimgray",
        "dimgrey",
        "lightgray",
        "lightgrey",
        "silver",
        "gainsboro",
        "whitesmoke",
        "slategray",
        "slategrey",
    ],
    "Browns": [
        "brown",
        "maroon",
        "sienna",
        "saddlebrown",
        "chocolate",
        "peru",
        "tan",
        "rosybrown",
        "sandybrown",
        "burlywood",
        "wheat",
    ],
}

for category, color_list in categories.items():
    # Filter to only include colors that exist in our palette
    available = [c for c in color_list if c in all_colors]
    if available:
        print(SOLID.render_divider(75))
        print(SOLID.render_line(75, f"  {category}", align="left"))

        # Display colors in rows
        for i in range(0, len(available), 4):
            row_colors = available[i : i + 4]
            line = "  " + "  ".join(f"{c:18}" for c in row_colors)
            print(SOLID.render_line(75, line, align="left"))

print(SOLID.render_line(75, "", align="center"))
print(SOLID.render_bottom_border(75))
print()

# Special colors
print(SOLID.render_top_border(75, "✨ Special & Web-safe Colors"))
print(SOLID.render_line(75, "", align="center"))
print(SOLID.render_line(75, "rebeccapurple: Named in honor of Rebecca Meyer (CSS4)", align="left"))
print(SOLID.render_line(75, "Web-safe colors: 216 colors safe across all browsers", align="left"))
print(
    SOLID.render_line(75, "Gray/Grey: Both spellings supported for all gray variants", align="left")
)
print(SOLID.render_line(75, "", align="center"))
print(SOLID.render_bottom_border(75))
print()

# Color operations showcase
print(SOLID.render_top_border(75, "🎨 Color Operations"))
print(SOLID.render_line(75, "", align="center"))

# Gradient example
print(SOLID.render_line(75, "Gradient Interpolation:", align="left"))
print(SOLID.render_line(75, "  interpolate_color('red', 'blue', 0.0) → red", align="left"))
print(SOLID.render_line(75, "  interpolate_color('red', 'blue', 0.5) → purple", align="left"))
print(SOLID.render_line(75, "  interpolate_color('red', 'blue', 1.0) → blue", align="left"))
print(SOLID.render_line(75, "", align="center"))

# Conversion example
print(SOLID.render_line(75, "Color Conversions:", align="left"))
r, g, b = parse_color("coral")
hex_color = rgb_to_hex(r, g, b)
print(SOLID.render_line(75, f"  parse_color('coral') → ({r}, {g}, {b})", align="left"))
print(SOLID.render_line(75, f"  rgb_to_hex({r}, {g}, {b}) → '{hex_color}'", align="left"))
print(SOLID.render_line(75, "", align="center"))

print(SOLID.render_bottom_border(75))
print()

print("=" * 80)
print(f"Total CSS4 colors: {len(all_colors)}")
print("All colors are case-insensitive and support multiple formats!")
print("=" * 80)
print()
