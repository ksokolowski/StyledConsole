"""Unit tests for Frame color and gradient features."""

from styledconsole import Frame, FrameRenderer


class TestFrameColors:
    """Test Frame with color parameters."""

    def test_frame_with_content_color(self):
        """Test frame with content color parameter."""
        frame = Frame(content=["Test"], content_color="lime")
        assert frame.content_color == "lime"

    def test_frame_with_border_color(self):
        """Test frame with border color parameter."""
        frame = Frame(content=["Test"], border_color="red")
        assert frame.border_color == "red"

    def test_frame_with_title_color(self):
        """Test frame with title color parameter."""
        frame = Frame(content=["Test"], title="Title", title_color="blue")
        assert frame.title_color == "blue"

    def test_frame_with_gradient(self):
        """Test frame with gradient parameters."""
        frame = Frame(content=["Test"], start_color="red", end_color="blue")
        assert frame.start_color == "red"
        assert frame.end_color == "blue"

    def test_frame_with_all_colors(self):
        """Test frame with all color parameters."""
        frame = Frame(
            content=["Test"],
            content_color="magenta",
            border_color="cyan",
            title_color="yellow",
            title="Title",
        )
        assert frame.content_color == "magenta"
        assert frame.border_color == "cyan"
        assert frame.title_color == "yellow"


class TestFrameRendererColors:
    """Test FrameRenderer color rendering."""

    def test_render_with_content_color(self):
        """Test rendering with content color."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test content"], content_color="lime")

        # Check that ANSI color codes are present
        assert any("\033[" in line for line in lines)
        # Content line should have color codes
        assert "\033[38;2;0;255;0m" in lines[1]

    def test_render_with_border_color(self):
        """Test rendering with border color."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test"], border_color="red")

        # All lines should have border color codes
        for line in lines:
            assert "\033[38;2;255;0;0m" in line

    def test_render_with_title_color(self):
        """Test rendering with title color."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test"], title="Title", title_color="blue")

        # Title line should have title color
        assert "\033[38;2;0;0;255m" in lines[0]

    def test_render_with_gradient(self):
        """Test rendering with gradient."""
        renderer = FrameRenderer()
        lines = renderer.render(["Line 1", "Line 2", "Line 3"], start_color="red", end_color="blue")

        # Each content line should have different colors
        # First line: red (255, 0, 0)
        assert "\033[38;2;255;0;0m" in lines[1]
        # Last line: blue (0, 0, 255)
        assert "\033[38;2;0;0;255m" in lines[3]

    def test_render_with_all_colors(self):
        """Test rendering with all color options."""
        renderer = FrameRenderer()
        lines = renderer.render(
            ["Content"],
            title="Title",
            content_color="magenta",
            border_color="cyan",
            title_color="yellow",
        )

        # Check that multiple color codes are present
        assert "\033[38;2;255;255;0m" in lines[0]  # Title (yellow)
        assert "\033[38;2;0;255;255m" in lines[0]  # Border (cyan)
        assert "\033[38;2;255;0;255m" in lines[1]  # Content (magenta)

    def test_render_named_colors(self):
        """Test rendering with CSS4 named colors."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test"], content_color="green", border_color="blue")

        # Green = (0, 128, 0)
        assert "\033[38;2;0;128;0m" in lines[1]
        # Blue = (0, 0, 255)
        assert "\033[38;2;0;0;255m" in lines[0]

    def test_render_gradient_single_line(self):
        """Test gradient with single line (edge case)."""
        renderer = FrameRenderer()
        lines = renderer.render(["Single line"], start_color="red", end_color="blue")

        # Single line should get the start color
        assert "\033[38;2;255;0;0m" in lines[1]

    def test_gradient_overrides_content_color(self):
        """Test that gradient takes precedence over content_color."""
        renderer = FrameRenderer()
        lines = renderer.render(
            ["Line 1", "Line 2"],
            content_color="white",
            start_color="red",
            end_color="blue",
        )

        # Should use gradient, not white
        assert "\033[38;2;255;0;0m" in lines[1]
        assert "\033[38;2;255;255;255m" not in lines[1]

    def test_color_with_different_borders(self):
        """Test colors with different border styles."""
        renderer = FrameRenderer()

        for border_style in ["solid", "double", "rounded", "heavy"]:
            lines = renderer.render(["Test"], border=border_style, content_color="lime")
            assert "\033[38;2;0;255;0m" in lines[1]

    def test_color_with_emoji_content(self):
        """Test colors with emoji content."""
        renderer = FrameRenderer()
        lines = renderer.render(["🚀 Test", "💎 Content"], start_color="red", end_color="lime")

        # Should have color codes despite emoji
        assert "\033[38;2;255;0;0m" in lines[1]
        assert "\033[38;2;0;255;0m" in lines[2]

    def test_no_color_by_default(self):
        """Test that no color codes are added when colors not specified."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test content"])

        # Should not have ANSI color codes
        has_ansi = any("\033[" in line for line in lines)
        assert not has_ansi

    def test_ansi_reset_codes(self):
        """Test that ANSI reset codes are properly added."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test"], content_color="red")

        # Should have reset code after color
        assert "\033[0m" in lines[1]

    def test_color_with_multiline_content(self):
        """Test colors with multi-line content."""
        renderer = FrameRenderer()
        lines = renderer.render(
            ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"],
            start_color="red",
            end_color="blue",
        )

        # All content lines should have color codes
        for i in range(1, 6):
            assert "\033[38;2;" in lines[i]
            assert "\033[0m" in lines[i]

    def test_color_with_padding(self):
        """Test colors with different padding values."""
        renderer = FrameRenderer()

        for padding in [0, 1, 2, 3]:
            lines = renderer.render(["Test"], padding=padding, content_color="lime")
            assert "\033[38;2;0;255;0m" in lines[1]

    def test_color_with_alignment(self):
        """Test colors with different alignments."""
        renderer = FrameRenderer()

        for align in ["left", "center", "right"]:
            lines = renderer.render(["Test"], align=align, content_color="red")
            assert "\033[38;2;255;0;0m" in lines[1]
