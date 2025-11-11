#!/usr/bin/env python3
"""
Digital Poetry - StyledConsole Showcase

A creative multi-line poem celebrating the beauty of terminal styling,
demonstrating StyledConsole's emoji-safe rendering and visual appeal.
"""

from styledconsole import DOUBLE, HEAVY, ROUNDED, SOLID

print()
print("=" * 80)
print(" " * 20 + "✨ DIGITAL POETRY ✨")
print("=" * 80)
print()

# Poem 1: The Art of Terminal
poem1_width = 70
poem1 = [
    "In terminals of monospaced grace,",
    "Where characters find their perfect place,",
    "🎨 Colors dance and borders shine,",
    "Each glyph aligned in perfect line.",
    "",
    "From ASCII old to Unicode new,",
    "We render text in vibrant hue,",
    "✨ Emojis wide, yet counted true,",
    "Visual width guides all we do.",
]

print(ROUNDED.render_top_border(poem1_width, "🎭 The Art of Terminal"))
for line in poem1:
    if line:
        print(ROUNDED.render_line(poem1_width, line, align="center"))
    else:
        print(ROUNDED.render_line(poem1_width, "", align="center"))
print(ROUNDED.render_bottom_border(poem1_width))
print()

# Poem 2: Ode to StyledConsole
poem2_width = 75
poem2 = [
    "🚀 Born from pixels, shaped by care,",
    "StyledConsole breathes terminal air,",
    "SOLID borders, ROUNDED grace,",
    "DOUBLE lines find their place.",
    "",
    "HEAVY weight and THICK design,",
    "ASCII simple, MINIMAL fine,",
    "DOTS that whisper, frames that shout,",
    "Eight pure styles we can't live without.",
    "",
    "💎 From text utilities foundation strong,",
    "To color palettes rich and long,",
    "CSS4 names, one-four-eight,",
    "Terminal detection, capability state.",
    "",
    "⚡ With visual_width() we measure right,",
    "pad_to_width() makes spacing tight,",
    "truncate_to_width() cuts with care,",
    "Emoji-safe rendering everywhere!",
]

print(DOUBLE.render_top_border(poem2_width, "📜 Ode to StyledConsole"))
for line in poem2:
    if line:
        align = "center" if line.startswith(("🚀", "💎", "⚡")) else "center"
        print(DOUBLE.render_line(poem2_width, line, align=align))
    else:
        print(DOUBLE.render_divider(poem2_width))
print(DOUBLE.render_bottom_border(poem2_width))
print()

# Poem 3: The Developer's Haiku
haiku_width = 55
haikus = [
    ("Terminal awaits", "Borders render, pixels dance", "Code becomes beauty"),
    ("Emojis align 🎯", "Visual width guides the way", "Perfect frames emerge"),
    ("Eight styles to choose ✨", "SOLID, ROUNDED, pure and clean", "StyledConsole shines"),
]

print(HEAVY.render_top_border(haiku_width, "🌸 Developer's Haiku"))
print(HEAVY.render_line(haiku_width, "", align="center"))

for i, (line1, line2, line3) in enumerate(haikus):
    if i > 0:
        print(HEAVY.render_divider(haiku_width))
    print(HEAVY.render_line(haiku_width, line1, align="center"))
    print(HEAVY.render_line(haiku_width, line2, align="center"))
    print(HEAVY.render_line(haiku_width, line3, align="center"))
    print(HEAVY.render_line(haiku_width, "", align="center"))

print(HEAVY.render_bottom_border(haiku_width))
print()

# Finale: Multi-style celebration
finale_width = 78

print(SOLID.render_top_border(finale_width, "🎪 The Grand Finale"))
print(SOLID.render_line(finale_width, "", align="center"))
print(SOLID.render_line(finale_width, "✨ Where code meets art ✨", align="center"))
print(SOLID.render_line(finale_width, "", align="center"))
print(SOLID.render_line(finale_width, "From simple frames to complex scenes,", align="center"))
print(SOLID.render_line(finale_width, "StyledConsole powers developer dreams,", align="center"))
print(SOLID.render_line(finale_width, "With 189 tests all passing green,", align="center"))
print(SOLID.render_line(finale_width, "The finest terminal toolkit ever seen! 🎉", align="center"))
print(SOLID.render_line(finale_width, "", align="center"))
print(SOLID.render_divider(finale_width))
print(SOLID.render_line(finale_width, "", align="center"))
print(SOLID.render_line(finale_width, "98.62% coverage strong 💪", align="center"))
print(SOLID.render_line(finale_width, "Emoji-safe rendering all day long 🚀", align="center"))
print(SOLID.render_line(finale_width, "Foundation complete, M2 next in line 🏗️", align="center"))
print(SOLID.render_line(finale_width, "The rendering engine will be sublime! ⚡", align="center"))
print(SOLID.render_line(finale_width, "", align="center"))
print(SOLID.render_bottom_border(finale_width))
print()

print("=" * 80)
print(" " * 25 + "🎨 StyledConsole 🎨")
print(" " * 18 + "Terminal Beauty, Terminal Power")
print("=" * 80)
print()
