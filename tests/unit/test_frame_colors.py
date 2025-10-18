"""Unit tests for Frame color and gradient features."""

from styledconsole import Frame, FrameRenderer


class TestFrameColors:
    """Test Frame with color parameters."""

    def test_frame_with_content_color(self):
        """Test frame with content color parameter."""
        frame = Frame(content=["Test"], content_color="#00ff00")
        assert frame.content_color == "#00ff00"

    def test_frame_with_border_color(self):
        """Test frame with border color parameter."""
        frame = Frame(content=["Test"], border_color="#ff0000")
        assert frame.border_color == "#ff0000"

    def test_frame_with_title_color(self):
        """Test frame with title color parameter."""
        frame = Frame(content=["Test"], title="Title", title_color="#0000ff")
        assert frame.title_color == "#0000ff"

    def test_frame_with_gradient(self):
        """Test frame with gradient parameters."""
        frame = Frame(content=["Test"], gradient_start="#ff0000", gradient_end="#0000ff")
        assert frame.gradient_start == "#ff0000"
        assert frame.gradient_end == "#0000ff"

    def test_frame_with_all_colors(self):
        """Test frame with all color parameters."""
        frame = Frame(
            content=["Test"],
            content_color="#ff00ff",
            border_color="#00ffff",
            title_color="#ffff00",
            title="Title",
        )
        assert frame.content_color == "#ff00ff"
        assert frame.border_color == "#00ffff"
        assert frame.title_color == "#ffff00"


class TestFrameRendererColors:
    """Test FrameRenderer color rendering."""

    def test_render_with_content_color(self):
        """Test rendering with content color."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test content"], content_color="#00ff00")

        # Check that ANSI color codes are present
        assert any("\033[" in line for line in lines)
        # Content line should have color codes
        assert "\033[38;2;0;255;0m" in lines[1]

    def test_render_with_border_color(self):
        """Test rendering with border color."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test"], border_color="#ff0000")

        # All lines should have border color codes
        for line in lines:
            assert "\033[38;2;255;0;0m" in line

    def test_render_with_title_color(self):
        """Test rendering with title color."""
        renderer = FrameRenderer()
        lines = renderer.render(["Test"], title="Title", title_color="#0000ff")

        # Title line should have title color
        assert "\033[38;2;0;0;255m" in lines[0]

    def test_render_with_gradient(self):
        """Test rendering with gradient."""
        renderer = FrameRenderer()
        lines = renderer.render(
            ["Line 1", "Line 2", "Line 3"], gradient_start="#ff0000", gradient_end="#0000ff"
        )

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
            content_color="#ff00ff",
            border_color="#00ffff",
            title_color="#ffff00",
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
        lines = renderer.render(["Single line"], gradient_start="#ff0000", gradient_end="#0000ff")

        # Single line should get the start color
        assert "\033[38;2;255;0;0m" in lines[1]

    def test_gradient_overrides_content_color(self):
        """Test that gradient takes precedence over content_color."""
        renderer = FrameRenderer()
        lines = renderer.render(
            ["Line 1", "Line 2"],
            content_color="#ffffff",
            gradient_start="#ff0000",
            gradient_end="#0000ff",
        )

        # Should use gradient, not white
        assert "\033[38;2;255;0;0m" in lines[1]
        assert "\033[38;2;255;255;255m" not in lines[1]

    def test_color_with_different_borders(self):
        """Test colors with different border styles."""
        renderer = FrameRenderer()

        for border_style in ["solid", "double", "rounded", "heavy"]:
            lines = renderer.render(["Test"], border=border_style, content_color="#00ff00")
            assert "\033[38;2;0;255;0m" in lines[1]

    def test_color_with_emoji_content(self):
        """Test colors with emoji content."""
        renderer = FrameRenderer()
        lines = renderer.render(
            ["🚀 Test", "💎 Content"], gradient_start="#ff0000", gradient_end="#00ff00"
        )

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
        lines = renderer.render(["Test"], content_color="#ff0000")

        # Should have reset code after color
        assert "\033[0m" in lines[1]

    def test_color_with_multiline_content(self):
        """Test colors with multi-line content."""
        renderer = FrameRenderer()
        lines = renderer.render(
            ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"],
            gradient_start="#ff0000",
            gradient_end="#0000ff",
        )

        # All content lines should have color codes
        for i in range(1, 6):
            assert "\033[38;2;" in lines[i]
            assert "\033[0m" in lines[i]

    def test_color_with_padding(self):
        """Test colors with different padding values."""
        renderer = FrameRenderer()

        for padding in [0, 1, 2, 3]:
            lines = renderer.render(["Test"], padding=padding, content_color="#00ff00")
            assert "\033[38;2;0;255;0m" in lines[1]

    def test_color_with_alignment(self):
        """Test colors with different alignments."""
        renderer = FrameRenderer()

        for align in ["left", "center", "right"]:
            lines = renderer.render(["Test"], align=align, content_color="#ff0000")
            assert "\033[38;2;255;0;0m" in lines[1]


class TestFrameRendererColorHelpers:
    """Test internal color helper methods."""

    def test_colorize_method(self):
        """Test _colorize helper method."""
        renderer = FrameRenderer()
        colored = renderer._colorize("Test", "#ff0000")

        assert "\033[38;2;255;0;0m" in colored
        assert "Test" in colored
        assert "\033[0m" in colored

    def test_colorize_with_named_color(self):
        """Test _colorize with named color."""
        renderer = FrameRenderer()
        colored = renderer._colorize("Test", "red")

        assert "\033[38;2;255;0;0m" in colored

    def test_colorize_content_in_line(self):
        """Test _colorize_content_in_line method."""
        renderer = FrameRenderer()
        from styledconsole.core.styles import get_border_style

        style = get_border_style("solid")
        line = "│ Test content │"

        colored = renderer._colorize_content_in_line(line, style, "#00ff00", None)

        # Content should be colored
        assert "\033[38;2;0;255;0m" in colored
        # Borders should not be colored
        assert colored.startswith("│")

    def test_colorize_borders_in_line(self):
        """Test _colorize_borders_in_line method."""
        renderer = FrameRenderer()
        from styledconsole.core.styles import get_border_style

        style = get_border_style("solid")
        line = "│ Test content │"

        colored = renderer._colorize_borders_in_line(line, style, "#0000ff")

        # Borders should be colored
        assert "\033[38;2;0;0;255m" in colored
        # Should have content unchanged in middle
        assert "Test content" in colored
