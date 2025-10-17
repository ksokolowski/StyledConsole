#!/usr/bin/env python3
"""
Text Alignment Example

Demonstrates left, center, and right alignment options for content lines.
"""

from styledconsole import HEAVY, ROUNDED, SOLID

print("=" * 60)
print("TEXT ALIGNMENT EXAMPLES")
print("=" * 60)
print()

# Example 1: Basic alignments
print("1. Basic Alignment Options:")
print()

print(SOLID.render_top_border(60, "Alignment Demo"))
print(SOLID.render_line(60, "This is LEFT aligned", align="left"))
print(SOLID.render_line(60, "This is CENTER aligned", align="center"))
print(SOLID.render_line(60, "This is RIGHT aligned", align="right"))
print(SOLID.render_bottom_border(60))
print()

# Example 2: Mixed alignments for visual effect
print("2. Mixed Alignments:")
print()

print(ROUNDED.render_top_border(60, "🎨 Creative Layout"))
print(ROUNDED.render_line(60, "Header: Left Aligned", align="left"))
print(ROUNDED.render_divider(60))
print(ROUNDED.render_line(60, "Main Content: Centered", align="center"))
print(ROUNDED.render_line(60, "More centered text here", align="center"))
print(ROUNDED.render_divider(60))
print(ROUNDED.render_line(60, "Footer: Right Aligned", align="right"))
print(ROUNDED.render_bottom_border(60))
print()

# Example 3: Practical use case - status display
print("3. Status Display:")
print()

print(HEAVY.render_top_border(60, "⚡ System Status"))
print(HEAVY.render_line(60, "Service: API Server", align="left"))
print(HEAVY.render_line(60, "Status: ✅ Running", align="center"))
print(HEAVY.render_line(60, "Uptime: 99.9%", align="right"))
print(HEAVY.render_divider(60))
print(HEAVY.render_line(60, "Service: Database", align="left"))
print(HEAVY.render_line(60, "Status: ✅ Connected", align="center"))
print(HEAVY.render_line(60, "Queries/sec: 1,234", align="right"))
print(HEAVY.render_bottom_border(60))
print()

# Example 4: Different widths
print("4. Different Frame Widths:")
print()

widths = [30, 45, 60]
for w in widths:
    print(SOLID.render_top_border(w, f"Width: {w}"))
    print(SOLID.render_line(w, "Left", align="left"))
    print(SOLID.render_line(w, "Center", align="center"))
    print(SOLID.render_line(w, "Right", align="right"))
    print(SOLID.render_bottom_border(w))
    print()
