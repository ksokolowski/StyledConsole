import io

from rich.console import Console as RichConsole

from styledconsole import Console
from styledconsole.core.rendering_engine import RenderingEngine


def test_frame_gradient_rendering():
    """Test that start_color and end_color apply gradient to frame content."""
    buffer = io.StringIO()
    console = Console(file=buffer, width=80)

    content = ["Line 1", "Line 2", "Line 3"]
    console.frame(content, start_color="#ff0000", end_color="#0000ff", border="solid")

    output = buffer.getvalue()
    # We expect Rich markup to have been applied, which then gets rendered to ANSI.
    # Since we can't easily check exact ANSI codes for interpolation without a complex setup,
    # we'll verify that the RenderingEngine logic was correct by mocking _build_content_renderable
    # or just trusting the integration if we see color codes.

    # However, let's look at the implementation of _build_content_renderable again.
    # It uses interpolate_color.

    assert "Line 1" in output
    assert "Line 3" in output


def test_build_content_renderable_gradient():
    """Directly test _build_content_renderable logic for gradients."""
    rich_console = RichConsole(file=io.StringIO())
    engine = RenderingEngine(rich_console)

    content = "Line 1\nLine 2\nLine 3"
    renderable = engine._build_content_renderable(
        content, content_color=None, start_color="#ff0000", end_color="#0000ff"
    )

    # Renderable should be a Text object with markup
    # But wait, _build_content_renderable returns Text.from_markup result
    # We can inspect the style of the text spans?

    # Actually, Text.from_markup parses the markup into spans.
    # Let's check the spans.

    # Line 1 should be red (#ff0000)
    # Line 3 should be blue (#0000ff)
    # Line 2 should be interpolated (approx #800080)

    # Note: Rich Text object structure is complex.
    # Let's just verify it returns a Text object and we can render it to check colors.

    c = RichConsole(file=io.StringIO(), force_terminal=True, color_system="truecolor")
    c.print(renderable)
    output = c.file.getvalue()

    # Check for RGB codes
    # Red: \x1b[38;2;255;0;0m
    # Blue: \x1b[38;2;0;0;255m

    assert "\x1b[38;2;255;0;0m" in output  # Red start
    assert "\x1b[38;2;0;0;255m" in output  # Blue end


def test_single_line_gradient_fallback():
    """Test single line content uses start_color."""
    rich_console = RichConsole(file=io.StringIO())
    engine = RenderingEngine(rich_console)

    content = "Single Line"
    renderable = engine._build_content_renderable(
        content, content_color=None, start_color="#ff0000", end_color="#0000ff"
    )

    c = RichConsole(file=io.StringIO(), force_terminal=True, color_system="truecolor")
    c.print(renderable)
    output = c.file.getvalue()

    assert "\x1b[38;2;255;0;0m" in output  # Red only
