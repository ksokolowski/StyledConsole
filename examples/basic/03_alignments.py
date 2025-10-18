#!/usr/bin/env python3
"""
Text Alignment Example

Demonstrates left, center, and right alignment options for content lines.
"""

from styledconsole import FrameRenderer

renderer = FrameRenderer()

print("=" * 60)
print("TEXT ALIGNMENT EXAMPLES")
print("=" * 60)
print()

# Example 1: Basic alignments (demonstrating different alignments per line)
print("1. Basic Alignment Options:")
print()

for line in renderer.render(
    "This is LEFT aligned",
    title="Alignment Demo",
    border="solid",
    width=60,
    align="left",
):
    print(line)
print()

for line in renderer.render(
    "This is CENTER aligned",
    border="solid",
    width=60,
    align="center",
):
    print(line)
print()

for line in renderer.render(
    "This is RIGHT aligned",
    border="solid",
    width=60,
    align="right",
):
    print(line)
print()

# Example 2: Multi-line with consistent alignment
print("2. Multi-line Content:")
print()

content = [
    "Header: Left Aligned",
    "Main Content: Centered",
    "More centered text here",
    "Footer: Right Aligned",
]

for line in renderer.render(
    content,
    title="🎨 Creative Layout",
    border="rounded",
    width=60,
    align="center",
):
    print(line)
print()

# Example 3: Practical use case - status display
print("3. Status Display:")
print()

status_content = [
    "Service: API Server",
    "Status: ✅ Running",
    "Uptime: 99.9%",
    "",
    "Service: Database",
    "Status: ✅ Connected",
    "Queries/sec: 1,234",
]

for line in renderer.render(
    status_content,
    title="⚡ System Status",
    border="heavy",
    width=60,
    align="left",
):
    print(line)
print()

# Example 4: Different widths
print("4. Different Frame Widths:")
print()

widths = [30, 45, 60]
for w in widths:
    for line in renderer.render(
        ["Left", "Center", "Right"],
        title=f"Width: {w}",
        border="solid",
        width=w,
        align="center",
    ):
        print(line)
    print()
