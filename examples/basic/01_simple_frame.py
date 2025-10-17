#!/usr/bin/env python3
"""
Simple Frame Example

Demonstrates basic frame rendering with different border styles.
This is the simplest way to use StyledConsole border rendering.
"""

from styledconsole import ASCII, DOUBLE, ROUNDED, SOLID

print("=" * 60)
print("SIMPLE FRAME EXAMPLES")
print("=" * 60)
print()

# Example 1: SOLID border
print("1. SOLID Border:")
print(SOLID.render_top_border(50, "Welcome"))
print(SOLID.render_line(50, "Hello, StyledConsole!", align="center"))
print(SOLID.render_bottom_border(50))
print()

# Example 2: ROUNDED border
print("2. ROUNDED Border:")
print(ROUNDED.render_top_border(50, "Rounded Corners"))
print(ROUNDED.render_line(50, "Smooth and modern", align="center"))
print(ROUNDED.render_bottom_border(50))
print()

# Example 3: DOUBLE border
print("3. DOUBLE Border:")
print(DOUBLE.render_top_border(50, "Double Lines"))
print(DOUBLE.render_line(50, "For emphasis", align="center"))
print(DOUBLE.render_bottom_border(50))
print()

# Example 4: ASCII border (universal compatibility)
print("4. ASCII Border (Universal):")
print(ASCII.render_top_border(50, "ASCII Compatible"))
print(ASCII.render_line(50, "Works everywhere", align="center"))
print(ASCII.render_bottom_border(50))
print()

# Example 5: Multiple content lines
print("5. Multiple Lines:")
print(SOLID.render_top_border(50, "Multi-line Content"))
print(SOLID.render_line(50, "First line", align="left"))
print(SOLID.render_line(50, "Second line", align="center"))
print(SOLID.render_line(50, "Third line", align="right"))
print(SOLID.render_bottom_border(50))
