"""Tests for uncovered effects module functions.

This module targets specific coverage gaps identified in the code review:
- rainbow_cycling_frame function (lines 782-837)
- Edge cases in gradient functions
"""

from styledconsole.effects import rainbow_cycling_frame
from styledconsole.utils.text import strip_ansi


class TestRainbowCyclingFrame:
    """Tests for rainbow_cycling_frame function (87.55% → 95%+ coverage target)."""

    def test_rainbow_cycling_basic(self):
        """Test basic rainbow cycling frame creation."""
        lines = rainbow_cycling_frame(
            ["Line 1", "Line 2", "Line 3"],
            title="Test",
            border="solid",
            width=40,
        )
        # Should have content lines + top/bottom borders
        assert len(lines) >= 5
        # Check that output contains ANSI codes
        assert any("\033[" in line for line in lines)

    def test_rainbow_cycling_single_line(self):
        """Test rainbow cycling with single line."""
        lines = rainbow_cycling_frame(
            "Single line",
            border="rounded",
            width=30,
        )
        # Should have 1 content + 2 borders
        assert len(lines) >= 3
        # Should contain content
        assert "Single line" in strip_ansi("".join(lines))

    def test_rainbow_cycling_empty_content(self):
        """Test rainbow cycling with empty content."""
        lines = rainbow_cycling_frame([], width=40)
        # Should still have top and bottom borders
        assert len(lines) >= 2

    def test_rainbow_cycling_empty_string(self):
        """Test rainbow cycling with empty string."""
        lines = rainbow_cycling_frame("", width=40)
        # Should handle empty string gracefully
        assert len(lines) >= 2

    def test_rainbow_cycling_with_title(self):
        """Test rainbow cycling frame with title."""
        lines = rainbow_cycling_frame(
            ["Content 1", "Content 2"],
            title="Rainbow Title",
            border="solid",
            width=50,
        )
        # Top border should contain title
        assert "Rainbow Title" in strip_ansi(lines[0])

    def test_rainbow_cycling_multiline(self):
        """Test rainbow cycling with multiple lines."""
        content = [f"Line {i}" for i in range(10)]
        lines = rainbow_cycling_frame(
            content,
            border="double",
            width=40,
        )
        # Should have 10 content lines + 2 borders
        assert len(lines) >= 12

    def test_rainbow_cycling_different_borders(self):
        """Test rainbow cycling with different border styles."""
        content = ["Test content"]

        for border in ["solid", "rounded", "double", "heavy", "thick", "ascii"]:
            lines = rainbow_cycling_frame(content, border=border, width=40)
            assert len(lines) >= 3, f"Failed for border: {border}"
            assert any("\033[" in line for line in lines), f"No colors for border: {border}"

        # DOTS border is a special case - subtle characters
        lines = rainbow_cycling_frame(content, border="dots", width=40)
        assert len(lines) >= 3, "Failed for border: dots"

    def test_rainbow_cycling_list_input(self):
        """Test rainbow cycling with list input."""
        content_list = ["First line", "Second line", "Third line"]
        lines = rainbow_cycling_frame(content_list, width=50)
        assert len(lines) >= 5

    def test_rainbow_cycling_auto_width(self):
        """Test rainbow cycling with automatic width calculation."""
        # Don't specify width - should auto-calculate
        lines = rainbow_cycling_frame(
            ["Short", "A much longer line of content here"],
            border="solid",
        )
        assert len(lines) >= 4
        # Width should be auto-calculated based on content

    def test_rainbow_cycling_narrow_width(self):
        """Test rainbow cycling with very narrow width."""
        lines = rainbow_cycling_frame(
            ["Content that will be wrapped"],
            width=20,  # Very narrow
        )
        assert len(lines) >= 3

    def test_rainbow_cycling_wide_width(self):
        """Test rainbow cycling with very wide width."""
        lines = rainbow_cycling_frame(
            ["Short content"],
            width=100,  # Very wide
        )
        assert len(lines) >= 3

    def test_rainbow_cycling_with_padding(self):
        """Test rainbow cycling with different padding values."""
        for padding in [0, 1, 2, 5]:
            lines = rainbow_cycling_frame(
                ["Test"],
                padding=padding,
                width=40,
            )
            assert len(lines) >= 3, f"Failed for padding: {padding}"

    def test_rainbow_cycling_with_emoji(self):
        """Test rainbow cycling with emoji content."""
        lines = rainbow_cycling_frame(
            ["🚀 Rocket", "🎉 Party", "✨ Sparkles"],
            border="solid",
            width=40,
        )
        assert len(lines) >= 5
        # Emojis should be present in output
        assert any("🚀" in strip_ansi(line) for line in lines)

    def test_rainbow_cycling_alignment(self):
        """Test rainbow cycling with different alignments."""
        content = ["Short"]

        for align in ["left", "center", "right"]:
            lines = rainbow_cycling_frame(content, align=align, width=50)
            assert len(lines) >= 3, f"Failed for align: {align}"

    def test_rainbow_cycling_long_content(self):
        """Test rainbow cycling with very long content."""
        long_content = ["This is a very long line that contains a lot of text " * 5]
        lines = rainbow_cycling_frame(long_content, width=80)
        assert len(lines) >= 3

    def test_rainbow_cycling_special_characters(self):
        """Test rainbow cycling with special characters."""
        content = [
            "Special chars: @#$%^&*()",
            "Symbols: ←→↑↓",
            "Punctuation: !\"#$%&'()*+,-./:;<=>?@",
        ]
        lines = rainbow_cycling_frame(content, width=60)
        assert len(lines) >= 5
        # Special characters should be preserved
        assert any("@#$%^&*()" in strip_ansi(line) for line in lines)

    def test_rainbow_cycling_unicode(self):
        """Test rainbow cycling with Unicode characters."""
        content = [
            "Greek: αβγδε",
            "Math: ∑∫∂∇",
            "Arrows: ←→↑↓",
        ]
        lines = rainbow_cycling_frame(content, width=40)
        assert len(lines) >= 5

    def test_rainbow_cycling_ansi_in_content(self):
        """Test rainbow cycling with ANSI codes in content."""
        # Content with pre-existing ANSI codes
        content = ["\033[31mRed text\033[0m", "\033[32mGreen text\033[0m"]
        lines = rainbow_cycling_frame(content, width=40)
        assert len(lines) >= 4

    def test_rainbow_cycling_minimal_border(self):
        """Test rainbow cycling with minimal border (edge case)."""
        lines = rainbow_cycling_frame(
            ["Test"],
            border="minimal",  # Only horizontal lines
            width=30,
        )
        assert len(lines) >= 3

    def test_rainbow_cycling_rounded_thick_border(self):
        """Test rainbow cycling with rounded_thick border (new style)."""
        lines = rainbow_cycling_frame(
            ["Test content"],
            border="rounded_thick",
            width=40,
        )
        assert len(lines) >= 3
        # Should have ANSI color codes
        assert any("\033[" in line for line in lines)
