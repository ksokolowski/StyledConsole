"""Unit tests for frame rendering."""

from styledconsole.core.frame import Frame, FrameRenderer
from styledconsole.core.styles import SOLID
from styledconsole.utils.text import visual_width


class TestFrame:
    """Test Frame dataclass."""

    def test_frame_defaults(self):
        """Test Frame with default values."""
        frame = Frame(content="Hello")
        assert frame.content == "Hello"
        assert frame.title is None
        assert frame.border == "solid"
        assert frame.width is None
        assert frame.padding == 1
        assert frame.align == "left"
        assert frame.min_width == 20
        assert frame.max_width == 100

    def test_frame_custom_values(self):
        """Test Frame with custom values."""
        frame = Frame(
            content="Test",
            title="Title",
            border="double",
            width=50,
            padding=2,
            align="center",
            min_width=30,
            max_width=80,
        )
        assert frame.content == "Test"
        assert frame.title == "Title"
        assert frame.border == "double"
        assert frame.width == 50
        assert frame.padding == 2
        assert frame.align == "center"
        assert frame.min_width == 30
        assert frame.max_width == 80

    def test_frame_with_list_content(self):
        """Test Frame with list of lines."""
        lines = ["Line 1", "Line 2", "Line 3"]
        frame = Frame(content=lines)
        assert frame.content == lines


class TestFrameRenderer:
    """Test FrameRenderer class."""

    def test_renderer_initialization(self):
        """Test FrameRenderer can be created."""
        renderer = FrameRenderer()
        assert renderer is not None

    def test_simple_frame(self):
        """Test rendering a simple frame."""
        renderer = FrameRenderer()
        lines = renderer.render("Hello", border="solid", width=20)

        assert len(lines) == 3  # top, content, bottom
        assert lines[0].startswith("┌")
        assert lines[0].endswith("┐")
        assert "Hello" in lines[1]
        assert lines[1].startswith("│")
        assert lines[1].endswith("│")
        assert lines[2].startswith("└")
        assert lines[2].endswith("┘")

    def test_frame_with_title(self):
        """Test frame with title."""
        renderer = FrameRenderer()
        lines = renderer.render("Content", title="My Title", border="solid", width=30)

        assert len(lines) == 3
        assert "My Title" in lines[0]
        assert "Content" in lines[1]

    def test_frame_multiline_content(self):
        """Test frame with multiple content lines."""
        renderer = FrameRenderer()
        content = ["Line 1", "Line 2", "Line 3"]
        lines = renderer.render(content, border="solid", width=20)

        assert len(lines) == 5  # top + 3 content + bottom
        assert "Line 1" in lines[1]
        assert "Line 2" in lines[2]
        assert "Line 3" in lines[3]

    def test_frame_with_emoji(self):
        """Test frame with emoji content."""
        renderer = FrameRenderer()
        lines = renderer.render("Test 🚀", border="solid", width=30)

        # Verify alignment is correct
        for line in lines:
            assert visual_width(line) == 30

    def test_frame_auto_width(self):
        """Test automatic width calculation."""
        renderer = FrameRenderer()
        lines = renderer.render("Hello, World!", border="solid")

        # Should calculate appropriate width
        width = visual_width(lines[0])
        assert width >= 20  # min_width default
        assert width <= 100  # max_width default

        # All lines should have same width
        for line in lines:
            assert visual_width(line) == width

    def test_frame_with_padding(self):
        """Test frame with custom padding."""
        renderer = FrameRenderer()
        lines = renderer.render("X", border="solid", width=10, padding=2, min_width=5)

        # Content line should have padding on both sides
        content_line = lines[1]
        # Format: │ + space*2 + X + space*5 + │ = 10 chars
        assert content_line.startswith("│  ")

    def test_frame_alignment_left(self):
        """Test left alignment."""
        renderer = FrameRenderer()
        lines = renderer.render("Hi", border="solid", width=20, align="left")

        content_line = lines[1]
        assert "Hi" in content_line
        # Left-aligned should have content near the left side (after padding)

    def test_frame_alignment_center(self):
        """Test center alignment."""
        renderer = FrameRenderer()
        lines = renderer.render("Hi", border="solid", width=20, align="center")

        content_line = lines[1]
        assert "Hi" in content_line
        # Should be roughly centered

    def test_frame_alignment_right(self):
        """Test right alignment."""
        renderer = FrameRenderer()
        lines = renderer.render("Hi", border="solid", width=20, align="right")

        content_line = lines[1]
        assert "Hi" in content_line
        # Right-aligned should have content near the right side

    def test_frame_different_border_styles(self):
        """Test rendering with different border styles."""
        renderer = FrameRenderer()

        # Test with string names
        solid_lines = renderer.render("Test", border="solid", width=20)
        assert solid_lines[0].startswith("┌")

        double_lines = renderer.render("Test", border="double", width=20)
        assert double_lines[0].startswith("╔")

        rounded_lines = renderer.render("Test", border="rounded", width=20)
        assert rounded_lines[0].startswith("╭")

    def test_frame_with_border_style_object(self):
        """Test rendering with BorderStyle object."""
        renderer = FrameRenderer()
        lines = renderer.render("Test", border=SOLID, width=20)

        assert lines[0].startswith("┌")
        assert "Test" in lines[1]

    def test_frame_empty_content(self):
        """Test frame with empty content."""
        renderer = FrameRenderer()
        lines = renderer.render("", border="solid", width=20)

        assert len(lines) == 3  # Still renders frame structure
        assert lines[0].startswith("┌")
        assert lines[2].startswith("└")

    def test_frame_with_newlines(self):
        """Test frame with content containing newlines."""
        renderer = FrameRenderer()
        content = "Line 1\nLine 2\nLine 3"
        lines = renderer.render(content, border="solid", width=20)

        assert len(lines) == 5  # top + 3 content lines + bottom
        assert "Line 1" in lines[1]
        assert "Line 2" in lines[2]
        assert "Line 3" in lines[3]

    def test_frame_truncates_long_content(self):
        """Test that long content is truncated."""
        renderer = FrameRenderer()
        long_content = "This is a very long line that should be truncated"
        lines = renderer.render(long_content, border="solid", width=20)

        # All lines should be exactly width=20
        for line in lines:
            assert visual_width(line) == 20

    def test_frame_min_width(self):
        """Test minimum width enforcement."""
        renderer = FrameRenderer()
        lines = renderer.render("X", border="solid", min_width=30)

        width = visual_width(lines[0])
        assert width >= 30

    def test_frame_max_width(self):
        """Test maximum width enforcement."""
        renderer = FrameRenderer()
        long_content = "A" * 200
        lines = renderer.render(long_content, border="solid", max_width=50)

        width = visual_width(lines[0])
        assert width <= 50

    def test_render_frame_method(self):
        """Test render_frame method with Frame object."""
        renderer = FrameRenderer()
        frame = Frame(content="Test", border="solid", width=20)
        lines = renderer.render_frame(frame)

        assert len(lines) == 3
        assert "Test" in lines[1]

    def test_frame_with_emoji_title(self):
        """Test frame with emoji in title."""
        renderer = FrameRenderer()
        lines = renderer.render("Content", title="🚀 Launch", border="solid", width=30)

        # Title should be in top border
        assert "🚀" in lines[0]
        assert "Launch" in lines[0]

        # All lines should have consistent width
        for line in lines:
            assert visual_width(line) == 30

    def test_frame_visual_width_consistency(self):
        """Test that all frame lines have consistent visual width."""
        renderer = FrameRenderer()
        test_cases = [
            ("Plain text", None),
            ("With emoji 🎉", None),
            ("Content", "Title"),
            ("Content", "🚀 Emoji Title"),
        ]

        for content, title in test_cases:
            lines = renderer.render(content, title=title, border="solid", width=40)

            # All lines must have same visual width
            widths = [visual_width(line) for line in lines]
            assert len(set(widths)) == 1, f"Inconsistent widths for {content}/{title}: {widths}"
            assert widths[0] == 40

    def test_frame_multiline_with_different_lengths(self):
        """Test multiline content with varying line lengths."""
        renderer = FrameRenderer()
        content = ["Short", "A much longer line", "Mid"]
        lines = renderer.render(content, border="solid", width=30)

        assert len(lines) == 5  # top + 3 content + bottom

        # All lines should have same width
        for line in lines:
            assert visual_width(line) == 30


class TestFrameWidthCalculation:
    """Test automatic width calculation logic."""

    def test_calculate_width_simple(self):
        """Test width calculation for simple content."""
        renderer = FrameRenderer()
        lines = renderer.render("Hello", border="solid")

        # Should be wide enough for content + borders + padding
        width = visual_width(lines[0])
        # "Hello" = 5 chars + 2 borders + 2 padding = 9, but min_width=20
        assert width == 20

    def test_calculate_width_respects_content(self):
        """Test width calculation respects content length."""
        renderer = FrameRenderer()
        content = "This is a longer piece of content"
        lines = renderer.render(content, border="solid", padding=1)

        width = visual_width(lines[0])
        # Should be wide enough for content
        content_width = visual_width(content)
        assert width >= content_width + 2 + 2  # borders + padding

    def test_calculate_width_respects_title(self):
        """Test width calculation respects title length."""
        renderer = FrameRenderer()
        lines = renderer.render("X", title="This is a very long title", border="solid", padding=1)

        width = visual_width(lines[0])
        title_width = visual_width("This is a very long title")
        # Width should accommodate title + spacing
        assert width >= title_width + 2 + 2
