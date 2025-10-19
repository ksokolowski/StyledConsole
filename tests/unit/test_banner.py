"""Unit tests for Banner and BannerRenderer."""

import pytest

from styledconsole import Banner, BannerRenderer
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


class TestBannerRenderer:
    """Test BannerRenderer class."""

    def test_renderer_initialization(self):
        """Test BannerRenderer initializes correctly."""
        renderer = BannerRenderer()
        assert renderer is not None
        assert len(renderer.list_fonts()) > 0

    def test_render_simple_text(self):
        """Test rendering simple text without options."""
        renderer = BannerRenderer()
        lines = renderer.render("Hi")

        assert isinstance(lines, list)
        assert len(lines) > 0
        assert all(isinstance(line, str) for line in lines)

    def test_render_with_font(self):
        """Test rendering with different fonts."""
        renderer = BannerRenderer()

        # Standard font
        lines_standard = renderer.render("A", font="standard")
        assert len(lines_standard) > 0

        # Slant font
        lines_slant = renderer.render("A", font="slant")
        assert len(lines_slant) > 0

        # Different fonts should produce different output
        assert lines_standard != lines_slant

    def test_render_with_invalid_font(self):
        """Test rendering with invalid font raises error."""
        renderer = BannerRenderer()

        with pytest.raises(ValueError, match="Font 'nonexistent' not found"):
            renderer.render("Test", font="nonexistent")

    def test_render_with_gradient(self):
        """Test rendering with gradient coloring."""
        renderer = BannerRenderer()
        lines = renderer.render("Hi", start_color="#ff0000", end_color="#0000ff")

        assert len(lines) > 0
        # Should contain ANSI color codes
        assert any("\033[38;2;" in line for line in lines)
        # Should contain reset codes
        assert any("\033[0m" in line for line in lines)

    def test_render_with_border(self):
        """Test rendering with border."""
        renderer = BannerRenderer()
        lines = renderer.render("Hi", border="solid")

        assert len(lines) >= 3  # At least top, content, bottom
        # First and last lines should be borders
        assert "─" in lines[0] or "+" in lines[0]
        assert "─" in lines[-1] or "+" in lines[-1]

    def test_render_with_border_and_gradient(self):
        """Test rendering with both border and gradient."""
        renderer = BannerRenderer()
        lines = renderer.render(
            "Hi",
            start_color="#00ff00",
            end_color="#0000ff",
            border="double",
        )

        assert len(lines) >= 3
        # Should have border characters
        assert "═" in lines[0]
        # Content should have ANSI codes
        content_lines = lines[1:-1]
        assert any("\033[38;2;" in line for line in content_lines)

    def test_render_with_emoji_fallback(self):
        """Test that emoji text falls back to plain rendering."""
        renderer = BannerRenderer()
        lines = renderer.render("🚀")

        # Should fallback to plain text (single line)
        assert len(lines) == 1
        assert "🚀" in lines[0]

    def test_render_emoji_with_gradient(self):
        """Test emoji with gradient applies color to plain text."""
        renderer = BannerRenderer()
        lines = renderer.render("🎉", start_color="#ff0000", end_color="#00ff00")

        assert len(lines) == 1
        assert "🎉" in lines[0]
        # Should still have color codes
        assert "\033[38;2;" in lines[0]

    def test_render_banner_method(self):
        """Test render_banner with Banner object."""
        renderer = BannerRenderer()
        banner = Banner(text="Test", font="standard", border="solid")

        lines = renderer.render_banner(banner)
        assert len(lines) >= 3
        assert isinstance(lines, list)

    def test_render_with_width(self):
        """Test rendering with specified width."""
        renderer = BannerRenderer()
        lines = renderer.render("Hi", border="solid", width=60)

        # All lines should have same visual width (60)
        for line in lines:
            width = visual_width(line)
            assert width == 60

    def test_render_with_alignment(self):
        """Test rendering with different alignments."""
        renderer = BannerRenderer()

        # Test with border to make alignment visible
        for align in ["left", "center", "right"]:
            lines = renderer.render("X", border="solid", width=40, align=align)
            assert len(lines) >= 3

    def test_render_with_padding(self):
        """Test rendering with custom padding."""
        renderer = BannerRenderer()

        lines_padding1 = renderer.render("X", border="solid", width=40, padding=1)
        lines_padding3 = renderer.render("X", border="solid", width=40, padding=3)

        # With same width but different padding, ASCII art inside should differ
        # More padding means ASCII content gets less space
        assert len(lines_padding1) >= 3
        assert len(lines_padding3) >= 3
        # Both should have same overall width
        assert visual_width(lines_padding1[0]) == 40
        assert visual_width(lines_padding3[0]) == 40

    def test_list_fonts(self):
        """Test listing available fonts."""
        renderer = BannerRenderer()

        # Get all fonts
        all_fonts = renderer.list_fonts()
        assert len(all_fonts) > 0
        assert "standard" in all_fonts
        assert all(isinstance(font, str) for font in all_fonts)

        # Get limited fonts
        limited = renderer.list_fonts(limit=5)
        assert len(limited) == 5

    def test_preview_font(self):
        """Test font preview."""
        renderer = BannerRenderer()

        # Valid font
        preview = renderer.preview_font("standard", "Hi")
        assert isinstance(preview, str)
        assert len(preview) > 0

        # Custom text - ASCII art contains the characters in some form
        preview2 = renderer.preview_font("standard", "ABC")
        # The characters are present but as ASCII art patterns, not literal
        assert len(preview2) > 10  # ASCII art is multi-line and wide
        assert preview2.count("\n") >= 3  # Multiple lines of ASCII art

    def test_preview_font_invalid(self):
        """Test preview with invalid font."""
        renderer = BannerRenderer()

        with pytest.raises(ValueError, match="Font 'invalid' not found"):
            renderer.preview_font("invalid")

    def test_gradient_single_line(self):
        """Test gradient with single line (edge case)."""
        renderer = BannerRenderer()

        # Emoji fallback creates single line
        lines = renderer.render("X", start_color="#ff0000", end_color="#0000ff")

        # Should handle single line gradient
        assert len(lines) >= 1

    def test_render_multiline_ascii(self):
        """Test that ASCII art produces multiple lines."""
        renderer = BannerRenderer()
        lines = renderer.render("ABC", font="banner")

        # Banner font should produce multiple lines
        assert len(lines) > 1

    def test_gradient_colors_interpolate(self):
        """Test that gradient actually interpolates colors."""
        renderer = BannerRenderer()

        lines = renderer.render("TEST", font="banner", start_color="#ff0000", end_color="#0000ff")

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
        renderer = BannerRenderer()

        lines = renderer.render("Hi", start_color="red", end_color="blue", font="standard")

        assert len(lines) > 0
        assert any("\033[38;2;" in line for line in lines)

    def test_border_style_object(self):
        """Test rendering with BorderStyle object instead of string."""
        renderer = BannerRenderer()

        lines = renderer.render("X", border=DOUBLE)
        assert len(lines) >= 3
        assert "═" in lines[0]

    def test_no_border_returns_ascii_only(self):
        """Test that no border returns ASCII art without frame."""
        renderer = BannerRenderer()

        lines = renderer.render("X", font="standard")

        # Should not have border characters
        assert not any("─" in line or "│" in line for line in lines)
        # Should not have box corners
        assert not any("┌" in line or "└" in line for line in lines)

    def test_empty_text(self):
        """Test rendering empty text."""
        renderer = BannerRenderer()

        lines = renderer.render("")
        assert isinstance(lines, list)
        # pyfiglet may still produce some output for empty string

    def test_long_text(self):
        """Test rendering longer text."""
        renderer = BannerRenderer()

        lines = renderer.render("Hello World", font="standard")
        assert len(lines) > 0
        # ASCII art should be wider for longer text
        max_width = max(visual_width(strip_ansi(line)) for line in lines)
        assert max_width > 10

    def test_special_characters(self):
        """Test rendering text with special characters."""
        renderer = BannerRenderer()

        # Numbers
        lines = renderer.render("123", font="standard")
        assert len(lines) > 0

        # Symbols (that aren't emoji)
        lines = renderer.render("@#$", font="standard")
        assert len(lines) > 0
