#!/usr/bin/env python3
"""
Emoji Support Example

Demonstrates emoji-safe rendering with perfect visual alignment.
StyledConsole uses visual_width() to ensure emojis (which display as 2 columns)
align correctly with ASCII text (which displays as 1 column per character).
"""

from styledconsole import ROUNDED, SOLID, visual_width

print("=" * 60)
print("EMOJI-SAFE RENDERING EXAMPLES")
print("=" * 60)
print()

# Example 1: Emojis in titles
print("1. Emoji Titles - All Perfectly Aligned:")
print()

width = 50
examples = [
    ("🚀 Rocket Launch", "Emoji at start of title"),
    ("Success 🎉", "Emoji at end of title"),
    ("🔥 Hot 🚀 Fast", "Multiple emojis in title"),
    ("Plain Text", "No emojis for comparison"),
]

for title, description in examples:
    top = SOLID.render_top_border(width, title)
    line = SOLID.render_line(width, description, align="center")
    bottom = SOLID.render_bottom_border(width)

    print(top)
    print(line)
    print(bottom)
    print(f"  Visual width: {visual_width(top)} (expected: {width})")
    print()

# Example 2: Emojis in content with different alignments
print("2. Emoji Content - Different Alignments:")
print()

print(ROUNDED.render_top_border(50, "🎨 Alignment Demo"))
print(ROUNDED.render_line(50, "🎯 Left aligned", align="left"))
print(ROUNDED.render_line(50, "🌟 Centered", align="center"))
print(ROUNDED.render_line(50, "🚀 Right aligned", align="right"))
print(ROUNDED.render_line(50, "🎪 Multiple 🎭 emojis 🎨 in line", align="center"))
print(ROUNDED.render_bottom_border(50))
print()

# Example 3: Common emoji icons
print("3. Common Emoji Icons:")
print()

icons = [
    "✅ Success",
    "❌ Error",
    "⚠️  Warning",
    "ℹ️  Info",
    "🔍 Search",
    "📁 Folder",
    "📝 Document",
    "💾 Save",
    "🎉 Celebrate",
    "🎯 Target",
    "⚡ Fast",
    "🔒 Secure",
]

print(SOLID.render_top_border(50, "🎨 Icon Library"))
for icon_text in icons:
    print(SOLID.render_line(50, icon_text, align="left"))
print(SOLID.render_bottom_border(50))
print()

print("✨ All frames have perfect visual alignment!")
print("✨ Visual width calculations handle emoji correctly!")
