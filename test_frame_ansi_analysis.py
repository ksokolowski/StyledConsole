"""Analyze ANSI codes in each frame line."""

from styledconsole import SOLID
from styledconsole.core.frame import FrameRenderer
from styledconsole.utils.text import strip_ansi, visual_width

renderer = FrameRenderer()
frame_lines = renderer.render(
    content="🚀 Test content",
    border=SOLID,
    width=60,
    border_color="cyan",
    content_color="yellow",
    title="Test",
)

print("Frame ANSI Analysis:")
print("=" * 80)

for i, line in enumerate(frame_lines):
    clean = strip_ansi(line)
    visual = visual_width(line)
    total_bytes = len(line)
    ansi_bytes = total_bytes - len(clean)

    print(f"\nLine {i}: {repr(clean[:40])}")
    print(f"  Visual width: {visual}")
    print(f"  Total bytes: {total_bytes}")
    print(f"  ANSI overhead: {ansi_bytes}")
    print(f"  Full line: {repr(line[:100])}")
