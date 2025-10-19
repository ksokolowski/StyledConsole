"""Tests for effects module (gradients and rainbows)."""

import pytest

from styledconsole.effects import (
    RAINBOW_COLORS,
    diagonal_gradient_frame,
    get_rainbow_color,
    gradient_frame,
    rainbow_frame,
)
from styledconsole.utils.text import strip_ansi


class TestRainbowColor:
    """Tests for rainbow color generation."""

    def test_rainbow_color_at_start(self):
        """Rainbow color at position 0.0 should be red."""
        color = get_rainbow_color(0.0)
        assert color == "#FF0000"  # Red

    def test_rainbow_color_at_end(self):
        """Rainbow color at position 1.0 should be violet."""
        color = get_rainbow_color(1.0)
        assert color == "#9400D3"  # Darkviolet

    def test_rainbow_color_at_middle(self):
        """Rainbow color at position 0.5 should be between green and blue."""
        color = get_rainbow_color(0.5)
        # Should return a hex color
        assert color.startswith("#")
        assert len(color) == 7

    def test_rainbow_color_clamping(self):
        """Rainbow color should clamp negative and >1.0 values."""
        assert get_rainbow_color(-0.5) == "#FF0000"  # Red
        assert get_rainbow_color(1.5) == "#9400D3"  # Darkviolet


class TestGradientFrame:
    """Tests for basic gradient frame function."""

    def test_gradient_frame_basic(self):
        """Test basic gradient frame creation."""
        lines = gradient_frame(
            ["Line 1", "Line 2", "Line 3"],
            start_color="red",
            end_color="blue",
            target="content",
        )
        assert len(lines) == 5  # 3 content + 2 borders
        # Check that output contains ANSI codes
        assert any("\033[" in line for line in lines)

    def test_gradient_frame_single_line(self):
        """Test gradient with single line."""
        lines = gradient_frame(
            "Single line",
            start_color="cyan",
            end_color="magenta",
            target="content",
        )
        assert len(lines) == 3  # 1 content + 2 borders

    def test_gradient_frame_with_title(self):
        """Test gradient frame with title."""
        lines = gradient_frame(
            ["Content 1", "Content 2"],
            title="Test Title",
            start_color="lime",
            end_color="red",
            target="content",
        )
        # Top border should contain title
        assert "Test Title" in strip_ansi(lines[0])

    def test_gradient_frame_border_target(self):
        """Test gradient applied to border only."""
        lines = gradient_frame(
            ["Plain content"],
            start_color="yellow",
            end_color="purple",
            target="border",
        )
        # Border lines should have ANSI codes
        assert "\033[" in lines[0]  # Top border
        assert "\033[" in lines[-1]  # Bottom border

    def test_gradient_frame_both_target(self):
        """Test gradient applied to both border and content."""
        lines = gradient_frame(
            ["Content"],
            start_color="orange",
            end_color="green",
            target="both",
        )
        # All lines should have colors
        assert all("\033[" in line for line in lines)

    def test_gradient_frame_custom_border(self):
        """Test gradient frame with custom border style."""
        lines = gradient_frame(
            ["Test"],
            border="double",
            start_color="red",
            end_color="blue",
            target="content",
        )
        # Should use double border characters
        assert "═" in strip_ansi(lines[0]) or "╔" in strip_ansi(lines[0])

    def test_gradient_frame_alignment(self):
        """Test gradient frame with different alignments."""
        for align in ["left", "center", "right"]:
            lines = gradient_frame(
                ["Short"],
                width=30,
                align=align,
                start_color="red",
                end_color="blue",
                target="content",
            )
            assert len(lines) == 3

    def test_gradient_frame_horizontal_not_implemented(self):
        """Test that horizontal gradients raise NotImplementedError."""
        with pytest.raises(NotImplementedError):
            gradient_frame(
                ["Test"],
                start_color="red",
                end_color="blue",
                direction="horizontal",
            )

    def test_gradient_frame_hex_colors(self):
        """Test gradient with CSS4 color names."""
        lines = gradient_frame(
            ["Test"],
            start_color="red",
            end_color="blue",
            target="content",
        )
        assert len(lines) == 3
        assert "\033[" in lines[1]  # Content line colored

    def test_gradient_frame_empty_content(self):
        """Test gradient frame with empty content."""
        lines = gradient_frame(
            [],
            start_color="red",
            end_color="blue",
            target="content",
        )
        # Should still create a frame
        assert len(lines) >= 2


class TestDiagonalGradientFrame:
    """Tests for diagonal gradient frame function."""

    def test_diagonal_gradient_basic(self):
        """Test basic diagonal gradient."""
        lines = diagonal_gradient_frame(
            ["Line 1", "Line 2", "Line 3"],
            start_color="red",
            end_color="blue",
            target="both",
        )
        assert len(lines) == 5  # 3 content + 2 borders
        # All lines should have ANSI codes
        assert all("\033[" in line for line in lines)

    def test_diagonal_gradient_content_only(self):
        """Test diagonal gradient on content only."""
        lines = diagonal_gradient_frame(
            ["Content 1", "Content 2"],
            start_color="lime",
            end_color="magenta",
            target="content",
        )
        # Content lines should be colored
        assert "\033[" in lines[1]
        assert "\033[" in lines[2]

    def test_diagonal_gradient_border_only(self):
        """Test diagonal gradient on border only."""
        lines = diagonal_gradient_frame(
            ["Plain content"],
            start_color="cyan",
            end_color="yellow",
            target="border",
        )
        # Border lines should be colored
        assert "\033[" in lines[0]  # Top
        assert "\033[" in lines[-1]  # Bottom

    def test_diagonal_gradient_with_title(self):
        """Test diagonal gradient with title."""
        lines = diagonal_gradient_frame(
            ["Content 1", "Content 2"],
            title="Test Diagonal",
            start_color="red",
            end_color="blue",
            target="both",
        )
        # Title should be present
        assert "Test Diagonal" in strip_ansi(lines[0])
        # And colored (since target=both)
        assert "\033[" in lines[0]

    def test_diagonal_gradient_custom_border(self):
        """Test diagonal gradient with different border styles."""
        for border_style in ["rounded", "double", "heavy", "solid"]:
            lines = diagonal_gradient_frame(
                ["Test"],
                border=border_style,
                start_color="red",
                end_color="blue",
                target="both",
            )
            assert len(lines) == 3

    def test_diagonal_gradient_single_line(self):
        """Test diagonal gradient with single line content."""
        lines = diagonal_gradient_frame(
            "Single line",
            start_color="orange",
            end_color="purple",
            target="both",
        )
        assert len(lines) == 3

    def test_diagonal_gradient_alignment(self):
        """Test diagonal gradient preserves alignment."""
        lines = diagonal_gradient_frame(
            ["Short"],
            width=40,
            align="center",
            start_color="red",
            end_color="blue",
            target="content",
        )
        # Content should be centered (with padding on both sides)
        content = strip_ansi(lines[1])
        # Check that there's padding
        assert content.startswith("│") or content.startswith("┃")

    def test_diagonal_gradient_empty_content(self):
        """Test diagonal gradient with empty content."""
        lines = diagonal_gradient_frame(
            [],
            start_color="red",
            end_color="blue",
            target="both",
        )
        assert len(lines) >= 2  # At least borders

    def test_diagonal_gradient_multi_line(self):
        """Test diagonal gradient with many lines."""
        content = [f"Line {i}" for i in range(10)]
        lines = diagonal_gradient_frame(
            content,
            start_color="red",
            end_color="blue",
            target="both",
        )
        assert len(lines) == 12  # 10 content + 2 borders


class TestRainbowFrame:
    """Tests for rainbow frame function."""

    def test_rainbow_frame_basic(self):
        """Test basic rainbow frame."""
        lines = rainbow_frame(
            ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"],
            mode="content",
        )
        assert len(lines) == 7  # 5 content + 2 borders
        # Content should be colored
        assert any("\033[" in line for line in lines[1:-1])

    def test_rainbow_frame_border_mode(self):
        """Test rainbow on border only."""
        lines = rainbow_frame(
            ["Plain 1", "Plain 2", "Plain 3"],
            mode="border",
        )
        # Borders should be colored
        assert "\033[" in lines[0]
        assert "\033[" in lines[-1]

    def test_rainbow_frame_both_mode(self):
        """Test rainbow on both border and content."""
        lines = rainbow_frame(
            ["Content 1", "Content 2"],
            mode="both",
        )
        # All lines should have colors
        assert all("\033[" in line for line in lines)

    def test_rainbow_frame_with_title(self):
        """Test rainbow frame with title."""
        lines = rainbow_frame(
            ["Test"],
            title="Rainbow Title",
            mode="content",
        )
        assert "Rainbow Title" in strip_ansi(lines[0])

    def test_rainbow_frame_custom_border(self):
        """Test rainbow frame with custom border."""
        lines = rainbow_frame(
            ["Test"],
            border="heavy",
            mode="content",
        )
        # Should use heavy border
        assert "━" in strip_ansi(lines[0]) or "┏" in strip_ansi(lines[0])

    def test_rainbow_frame_single_line(self):
        """Test rainbow with single line."""
        lines = rainbow_frame("Single", mode="content")
        assert len(lines) == 3

    def test_rainbow_frame_many_lines(self):
        """Test rainbow with many lines to see full spectrum."""
        content = [f"Line {i}" for i in range(7)]
        lines = rainbow_frame(content, mode="content")
        # Should have gradient through all colors
        assert len(lines) == 9  # 7 content + 2 borders

    def test_rainbow_frame_alignment(self):
        """Test rainbow frame with alignment options."""
        for align in ["left", "center", "right"]:
            lines = rainbow_frame(
                ["Test"],
                align=align,
                width=30,
                mode="content",
            )
            assert len(lines) == 3


class TestGradientIntegration:
    """Integration tests for gradient effects."""

    def test_all_css4_colors_work(self):
        """Test that various CSS4 colors work in gradients."""
        color_pairs = [
            ("red", "blue"),
            ("lime", "magenta"),
            ("cyan", "yellow"),
            ("orange", "purple"),
            ("pink", "teal"),
        ]

        for start, end in color_pairs:
            lines = gradient_frame(
                ["Test"],
                start_color=start,
                end_color=end,
                target="content",
            )
            assert len(lines) == 3
            assert "\033[" in lines[1]

    def test_gradient_with_emojis(self):
        """Test gradient frames with emoji content."""
        lines = diagonal_gradient_frame(
            ["🌈 Rainbow", "🔥 Fire", "🌊 Ocean"],
            start_color="red",
            end_color="blue",
            target="both",
        )
        # Should handle emojis properly
        assert "🌈" in strip_ansi(lines[1])
        assert "🔥" in strip_ansi(lines[2])
        assert "🌊" in strip_ansi(lines[3])

    def test_gradient_preserves_width(self):
        """Test that gradients don't break visual width."""
        lines = gradient_frame(
            ["Test content"],
            width=30,
            start_color="red",
            end_color="blue",
            target="both",
        )
        # All lines should have same visual width (excluding ANSI)
        widths = [len(strip_ansi(line)) for line in lines]
        assert len(set(widths)) == 1  # All same width

    def test_mixed_gradient_types(self):
        """Test using different gradient types in sequence."""
        content = ["Line 1", "Line 2"]

        # Vertical gradient
        lines1 = gradient_frame(content, start_color="red", end_color="blue")

        # Diagonal gradient
        lines2 = diagonal_gradient_frame(content, start_color="red", end_color="blue")

        # Rainbow
        lines3 = rainbow_frame(content)

        # All should produce valid output
        assert all(len(l) == 4 for l in [lines1, lines2, lines3])

    def test_gradient_with_padding(self):
        """Test gradients with different padding values."""
        for padding in [0, 1, 2, 3]:
            lines = diagonal_gradient_frame(
                ["Test"],
                padding=padding,
                start_color="red",
                end_color="blue",
                target="both",
            )
            assert len(lines) == 3
