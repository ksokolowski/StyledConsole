#!/usr/bin/env python3
"""
Frame Renderer Example - Advanced Direct API Usage

This is an ADVANCED example demonstrating direct FrameRenderer API usage.
For most use cases, the Console API is recommended (see 01_simple_frame.py).

Use FrameRenderer directly when you need:
- To generate frames as list[str] for composition with LayoutComposer
- Fine-grained control over rendering without immediate output
- Integration with custom rendering pipelines

For standard usage, prefer: Console().frame(content, title="...", border="...")
"""

from styledconsole import SOLID, Frame, FrameRenderer

print("=" * 70)
print("FRAME RENDERER EXAMPLES")
print("=" * 70)
print()

renderer = FrameRenderer()

# Example 1: Simple frame with auto-width
print("1. Simple Frame (auto-width):")
lines = renderer.render("Hello, FrameRenderer!")
for line in lines:
    print(line)
print()

# Example 2: Frame with title
print("2. Frame with Title:")
lines = renderer.render(
    "This is the content",
    title="My Frame",
    border="double",
)
for line in lines:
    print(line)
print()

# Example 3: Multi-line content
print("3. Multi-line Content:")
content = [
    "Line 1: Introduction",
    "Line 2: Main content",
    "Line 3: Conclusion",
]
lines = renderer.render(content, title="Document", border="rounded")
for line in lines:
    print(line)
print()

# Example 4: Custom width and padding
print("4. Custom Width and Padding:")
lines = renderer.render(
    "Padded content",
    width=50,
    padding=3,
    border="heavy",
)
for line in lines:
    print(line)
print()

# Example 5: Different alignments
print("5. Content Alignment:")
for align in ["left", "center", "right"]:
    lines = renderer.render(
        f"Aligned: {align}",
        title=f"{align.upper()} align",
        width=40,
        align=align,
        border="solid",
    )
    for line in lines:
        print(line)
    print()

# Example 6: Emoji support
print("6. Emoji Support:")
lines = renderer.render(
    ["🚀 Rocket Launch", "🎉 Celebration", "✨ Magic"],
    title="🎨 Emoji Frame",
    border="rounded",
    align="center",
)
for line in lines:
    print(line)
print()

# Example 7: Using Frame dataclass
print("7. Using Frame Dataclass:")
frame = Frame(
    content="Using Frame object",
    title="Frame Config",
    border="thick",
    width=45,
    padding=2,
    align="center",
)
lines = renderer.render_frame(frame)
for line in lines:
    print(line)
print()

# Example 8: Min/Max width constraints
print("8. Width Constraints:")
short_content = "Short"
long_content = "This is a very long line of text that would normally make a wide frame"

lines = renderer.render(short_content, min_width=40, border="minimal")
print("Min width (40):")
for line in lines:
    print(line)
print()

lines = renderer.render(long_content, max_width=50, border="dots")
print("Max width (50) - content truncated:")
for line in lines:
    print(line)
print()

# Example 9: Comparison with low-level API
print("9. Comparison: FrameRenderer vs BorderStyle API:")
print()

# Old way (low-level)
print("Low-level BorderStyle API (manual):")
width = 40
print(SOLID.render_top_border(width, "Old Way"))
print(SOLID.render_line(width, "Requires manual width calculation"))
print(SOLID.render_line(width, "Manual line rendering"))
print(SOLID.render_bottom_border(width))
print()

# New way (high-level)
print("High-level FrameRenderer API (automatic):")
lines = renderer.render(
    ["Automatic width calculation", "Simpler API"],
    title="New Way",
    border="solid",
)
for line in lines:
    print(line)
print()

print("=" * 70)
print("✨ FrameRenderer provides a convenient high-level API!")
print("✨ Use BorderStyle methods for fine-grained control")
print("✨ Use FrameRenderer for quick and easy frames")
print("=" * 70)
