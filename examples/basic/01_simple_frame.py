#!/usr/bin/env python3
"""
Simple Frame Example

Demonstrates basic frame rendering with different border styles.
Uses the high-level FrameRenderer API for easy frame creation.
"""

from styledconsole import FrameRenderer

print("=" * 60)
print("SIMPLE FRAME EXAMPLES")
print("=" * 60)
print()

renderer = FrameRenderer()

# Example 1: SOLID border
print("1. SOLID Border:")
for line in renderer.render(
    "Hello, StyledConsole!",
    title="Welcome",
    border="solid",
    width=50,
    align="center",
):
    print(line)
print()

# Example 2: ROUNDED border
print("2. ROUNDED Border:")
for line in renderer.render(
    "Smooth and modern",
    title="Rounded Corners",
    border="rounded",
    width=50,
    align="center",
):
    print(line)
print()

# Example 3: DOUBLE border
print("3. DOUBLE Border:")
for line in renderer.render(
    "For emphasis",
    title="Double Lines",
    border="double",
    width=50,
    align="center",
):
    print(line)
print()

# Example 4: ASCII border (universal compatibility)
print("4. ASCII Border (Universal):")
for line in renderer.render(
    "Works everywhere",
    title="ASCII Compatible",
    border="ascii",
    width=50,
    align="center",
):
    print(line)
print()

# Example 5: Multiple content lines
print("5. Multiple Lines:")
for line in renderer.render(
    ["First line", "Second line", "Third line"],
    title="Multi-line Content",
    border="solid",
    width=50,
):
    print(line)
