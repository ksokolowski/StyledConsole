"""Integration tests for FrameRenderer.

Tests real-world usage patterns and visual output correctness.
"""

from styledconsole import Frame, FrameRenderer


def test_basic_workflow():
    """Test typical user workflow with FrameRenderer."""
    renderer = FrameRenderer()

    # Single line frame
    lines = renderer.render("Hello, World!", border="solid")
    assert len(lines) == 3
    assert "Hello, World!" in lines[1]

    # Multi-line frame
    content = ["Line 1", "Line 2", "Line 3"]
    lines = renderer.render(content, title="Test", border="rounded")
    assert len(lines) == 5  # top + 3 content + bottom
    assert "Test" in lines[0]


def test_emoji_alignment_integration():
    """Test that emoji frames align correctly in practice."""
    renderer = FrameRenderer()

    test_cases = [
        "Plain text",
        "With emoji 🚀",
        "Multiple 🎉 emojis ✨",
        "Start 🎨",
        "End 🎯",
    ]

    for content in test_cases:
        lines = renderer.render(content, border="solid", width=40)

        # All lines must have same visual width
        from styledconsole import visual_width

        widths = [visual_width(line) for line in lines]
        assert len(set(widths)) == 1, f"Inconsistent widths for '{content}': {widths}"
        assert widths[0] == 40


def test_all_border_styles():
    """Test that all border styles work correctly."""
    renderer = FrameRenderer()
    styles = ["solid", "double", "rounded", "heavy", "thick", "ascii", "minimal", "dots"]

    for style in styles:
        lines = renderer.render("Test", title="Style Test", border=style, width=30)
        assert len(lines) == 3
        assert "Test" in lines[1]


def test_frame_object_workflow():
    """Test using Frame dataclass directly."""
    renderer = FrameRenderer()

    frame = Frame(
        content=["Line 1", "Line 2"],
        title="My Frame",
        border="double",
        width=40,
        padding=2,
        align="center",
    )

    lines = renderer.render_frame(frame)
    assert len(lines) == 4  # top + 2 content + bottom
    assert "My Frame" in lines[0]


def test_auto_width_calculation():
    """Test automatic width calculation in practice."""
    renderer = FrameRenderer()

    # Short content with min_width
    lines = renderer.render("X", min_width=30)
    from styledconsole import visual_width

    assert visual_width(lines[0]) == 30

    # Long content should expand
    long_content = "This is a much longer piece of content"
    lines = renderer.render(long_content, padding=1)
    width = visual_width(lines[0])
    assert width >= 20  # At least min_width


def test_mixed_content_types():
    """Test different content types work together."""
    renderer = FrameRenderer()

    # String with newlines
    lines1 = renderer.render("Line 1\nLine 2\nLine 3", width=30)
    assert len(lines1) == 5  # top + 3 content + bottom

    # List of strings
    lines2 = renderer.render(["Line 1", "Line 2", "Line 3"], width=30)
    assert len(lines2) == 5

    # Empty string
    lines3 = renderer.render("", width=30)
    assert len(lines3) == 3

    # Empty list
    lines4 = renderer.render([], width=30)
    assert len(lines4) == 3


def test_padding_and_alignment_combinations():
    """Test various padding and alignment combinations."""
    renderer = FrameRenderer()

    combinations = [
        (1, "left"),
        (1, "center"),
        (1, "right"),
        (2, "left"),
        (2, "center"),
        (2, "right"),
        (3, "center"),
    ]

    for padding, align in combinations:
        lines = renderer.render("Test", width=40, padding=padding, align=align, border="solid")
        from styledconsole import visual_width

        # All lines should have consistent width
        widths = [visual_width(line) for line in lines]
        assert len(set(widths)) == 1
        assert widths[0] == 40


def test_emoji_in_title_and_content():
    """Test emoji handling in both title and content."""
    renderer = FrameRenderer()

    lines = renderer.render(
        ["🚀 Rocket", "🎉 Party", "✨ Sparkle"],
        title="🎨 Emoji Test",
        border="rounded",
        width=40,
    )

    from styledconsole import visual_width

    # Check all lines have consistent width
    widths = [visual_width(line) for line in lines]
    assert len(set(widths)) == 1
    assert widths[0] == 40

    # Verify emoji are in output
    full_output = "\n".join(lines)
    assert "🎨" in full_output
    assert "🚀" in full_output
    assert "🎉" in full_output
    assert "✨" in full_output


def test_truncation_with_long_content():
    """Test that very long content is handled gracefully."""
    renderer = FrameRenderer()

    long_content = "A" * 200
    lines = renderer.render(long_content, width=30, border="solid")

    from styledconsole import visual_width

    # Should not exceed width
    for line in lines:
        assert visual_width(line) == 30


def test_realistic_use_case():
    """Test a realistic use case: status message."""
    renderer = FrameRenderer()

    status_lines = [
        "Service: API Server",
        "Status: ✅ Running",
        "Uptime: 99.9%",
        "Last Check: 2 minutes ago",
    ]

    lines = renderer.render(
        status_lines,
        title="🔍 System Status",
        border="double",
        width=50,
        padding=2,
    )

    # Verify structure
    assert len(lines) == 6  # top + 4 content + bottom
    assert "System Status" in lines[0]
    assert "API Server" in lines[1]
    assert "✅" in lines[2]
    assert "99.9%" in lines[3]

    # Verify visual consistency
    from styledconsole import visual_width

    widths = [visual_width(line) for line in lines]
    assert len(set(widths)) == 1
    assert widths[0] == 50
