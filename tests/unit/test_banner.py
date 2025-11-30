"""Unit tests for Banner and BannerRenderer."""

from io import StringIO

import pytest
from rich.console import Console as RichConsole

from styledconsole import Banner
from styledconsole.core.rendering_engine import RenderingEngine
from styledconsole.core.styles import DOUBLE, SOLID
from styledconsole.utils.text import strip_ansi, visual_width


class TestBanner:
    """Test Banner dataclass configuration."""

    def test_banner_defaults(self):
        """Test Banner with default values."""
        banner = Banner(text="Test")
        assert banner.text == "Test"
        assert banner.font == "standard"
        assert banner.start_color is None
        assert banner.end_color is None
        assert banner.border is None
        assert banner.width is None
        assert banner.align == "center"
        assert banner.padding == 1

    def test_banner_custom_values(self):
        """Test Banner with custom values."""
        banner = Banner(
            text="Custom",
            font="slant",
            start_color="#ff0000",
            end_color="#0000ff",
            border="solid",
            width=60,
            align="left",
            padding=2,
        )
        assert banner.text == "Custom"
        assert banner.font == "slant"
        assert banner.start_color == "#ff0000"
        assert banner.end_color == "#0000ff"
        assert banner.border == "solid"
        assert banner.width == 60
        assert banner.align == "left"
        assert banner.padding == 2

    def test_banner_with_border_style_object(self):
        """Test Banner with BorderStyle object."""
        banner = Banner(text="Test", border=SOLID)
        assert banner.border == SOLID

    def test_banner_immutable(self):
        """Test that Banner is immutable (frozen)."""
        banner = Banner(text="Test")
        with pytest.raises(AttributeError):
            banner.text = "Changed"  # type: ignore


class TestRenderingEngineBanner:
    """Test banner rendering via RenderingEngine."""

    def setup_method(self):
        """Setup rendering engine with captured output."""
        self.buffer = StringIO()
        self.console = RichConsole(file=self.buffer, width=100)
        self.engine = RenderingEngine(self.console)

    def test_render_banner_lines(self):
        """Test rendering banner to lines."""
        banner = Banner(text="Hi")
        lines = self.engine._render_banner_lines(banner)

        assert isinstance(lines, list)
        assert len(lines) > 0
        assert all(isinstance(line, str) for line in lines)

    def test_render_with_font(self):
        """Test rendering with different fonts."""
        # Standard font
        banner_standard = Banner(text="A", font="standard")
        lines_standard = self.engine._render_banner_lines(banner_standard)
        assert len(lines_standard) > 0

        # Slant font
        banner_slant = Banner(text="A", font="slant")
        lines_slant = self.engine._render_banner_lines(banner_slant)
        assert len(lines_slant) > 0

        # Different fonts should produce different output
        assert lines_standard != lines_slant

    def test_render_with_invalid_font(self):
        """Test rendering with invalid font falls back gracefully."""
        # Note: RenderingEngine now catches the error and falls back to plain text
        banner = Banner(text="Test", font="nonexistent")
        lines = self.engine._render_banner_lines(banner)

        # Should fallback to plain text
        assert len(lines) == 1
        assert "Test" in lines[0]

    def test_render_with_gradient(self):
        """Test rendering with gradient coloring."""
        banner = Banner(text="Hi", start_color="#ff0000", end_color="#0000ff")
        lines = self.engine._render_banner_lines(banner)

        assert len(lines) > 0
        # Should contain ANSI color codes
        assert any("\033[38;2;" in line for line in lines)
        # Should contain reset codes
        assert any("\033[0m" in line for line in lines)

    def test_render_with_border(self):
        """Test rendering with border."""
        banner = Banner(text="Hi", border="solid")
        lines = self.engine._render_banner_lines(banner)

        assert len(lines) >= 3  # At least top, content, bottom
        # First and last lines should be borders
        assert "─" in lines[0] or "+" in lines[0]
        assert "─" in lines[-1] or "+" in lines[-1]

    def test_render_with_border_and_gradient(self):
        """Test rendering with both border and gradient."""
        banner = Banner(
            text="Hi",
            start_color="#00ff00",
            end_color="#0000ff",
            border="double",
        )
        lines = self.engine._render_banner_lines(banner)

        assert len(lines) >= 3
        # Should have border characters
        assert "═" in lines[0]
        # Content should have ANSI codes
        content_lines = lines[1:-1]
        assert any("\033[38;2;" in line for line in content_lines)

    def test_render_with_emoji_fallback(self):
        """Test that emoji text falls back to plain rendering."""
        banner = Banner(text="🚀")
        lines = self.engine._render_banner_lines(banner)

        # Should fallback to plain text (single line)
        assert len(lines) == 1
        assert "🚀" in lines[0]

    def test_render_emoji_with_gradient(self):
        """Test emoji with gradient applies color to plain text."""
        banner = Banner(text="🎉", start_color="#ff0000", end_color="#00ff00")
        lines = self.engine._render_banner_lines(banner)

        assert len(lines) == 1
        assert "🎉" in lines[0]
        # Should still have color codes
        assert "\033[38;2;" in lines[0]

    def test_render_with_width(self):
        """Test rendering with specified width."""
        banner = Banner(text="Hi", border="solid", width=60)
        lines = self.engine._render_banner_lines(banner)

        # All lines should have same visual width (60)
        for line in lines:
            width = visual_width(line)
            assert width == 60

    def test_render_with_alignment(self):
        """Test rendering with different alignments."""
        # Test with border to make alignment visible
        for align in ["left", "center", "right"]:
            banner = Banner(text="X", border="solid", width=40, align=align)
            lines = self.engine._render_banner_lines(banner)
            assert len(lines) >= 3

    def test_render_with_padding(self):
        """Test rendering with custom padding."""
        banner1 = Banner(text="X", border="solid", width=40, padding=1)
        lines_padding1 = self.engine._render_banner_lines(banner1)

        banner3 = Banner(text="X", border="solid", width=40, padding=3)
        lines_padding3 = self.engine._render_banner_lines(banner3)

        # With same width but different padding, ASCII art inside should differ
        # More padding means ASCII content gets less space
        assert len(lines_padding1) >= 3
        assert len(lines_padding3) >= 3
        # Both should have same overall width
        assert visual_width(lines_padding1[0]) == 40
        assert visual_width(lines_padding3[0]) == 40

    def test_gradient_single_line(self):
        """Test gradient with single line (edge case)."""
        # Emoji fallback creates single line
        banner = Banner(text="X", start_color="#ff0000", end_color="#0000ff")
        lines = self.engine._render_banner_lines(banner)

        # Should handle single line gradient
        assert len(lines) >= 1

    def test_render_multiline_ascii(self):
        """Test that ASCII art produces multiple lines."""
        banner = Banner(text="ABC", font="banner")
        lines = self.engine._render_banner_lines(banner)

        # Banner font should produce multiple lines
        assert len(lines) > 1

    def test_gradient_colors_interpolate(self):
        """Test that gradient actually interpolates colors."""
        banner = Banner(text="TEST", font="banner", start_color="#ff0000", end_color="#0000ff")
        lines = self.engine._render_banner_lines(banner)

        # Extract RGB values from ANSI codes
        rgb_values = []
        for line in lines:
            if "\033[38;2;" in line:
                # Extract RGB from ANSI code
                parts = line.split("\033[38;2;")[1].split("m")[0].split(";")
                if len(parts) == 3:
                    rgb_values.append(tuple(map(int, parts)))

        # Should have multiple different colors
        if len(rgb_values) > 1:
            assert len(set(rgb_values)) > 1  # Not all same color

    def test_render_with_named_colors(self):
        """Test gradient with named colors."""
        banner = Banner(text="Hi", start_color="red", end_color="blue", font="standard")
        lines = self.engine._render_banner_lines(banner)

        assert len(lines) > 0
        assert any("\033[38;2;" in line for line in lines)

    def test_border_style_object(self):
        """Test rendering with BorderStyle object instead of string."""
        banner = Banner(text="X", border=DOUBLE)
        lines = self.engine._render_banner_lines(banner)
        assert len(lines) >= 3
        assert "═" in lines[0]

    def test_no_border_returns_ascii_only(self):
        """Test that no border returns ASCII art without frame."""
        banner = Banner(text="X", font="standard")
        lines = self.engine._render_banner_lines(banner)

        # Should not have border characters
        assert not any("─" in line or "│" in line for line in lines)
        # Should not have box corners
        assert not any("┌" in line or "└" in line for line in lines)

    def test_empty_text(self):
        """Test rendering empty text."""
        banner = Banner(text="")
        lines = self.engine._render_banner_lines(banner)
        assert isinstance(lines, list)

    def test_long_text(self):
        """Test rendering longer text."""
        banner = Banner(text="Hello World", font="standard")
        lines = self.engine._render_banner_lines(banner)
        assert len(lines) > 0
        # ASCII art should be wider for longer text
        max_width = max(visual_width(strip_ansi(line)) for line in lines)
        assert max_width > 10

    def test_special_characters(self):
        """Test rendering text with special characters."""
        # Numbers
        banner1 = Banner(text="123", font="standard")
        lines1 = self.engine._render_banner_lines(banner1)
        assert len(lines1) > 0

        # Symbols (that aren't emoji)
        banner2 = Banner(text="@#$", font="standard")
        lines2 = self.engine._render_banner_lines(banner2)
        assert len(lines2) > 0
