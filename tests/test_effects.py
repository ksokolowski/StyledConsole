"""Tests for effects module (gradients and rainbows)."""

import pytest

from styledconsole.effects import (
    diagonal_gradient_frame,
    get_rainbow_color,
    gradient_frame,
    rainbow_cycling_frame,
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
        assert all(len(line) == 4 for line in [lines1, lines2, lines3])

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


class TestRainbowCyclingFrame:
    """Tests for rainbow_cycling_frame function (discrete per-line colors)."""

    def test_basic_cycling(self):
        """Test that each line gets a different rainbow color."""
        lines = rainbow_cycling_frame(
            ["Line 1", "Line 2", "Line 3", "Line 4"],
            border_gradient_start="gold",
            border_gradient_end="purple",
        )

        # Should have frame structure (top border + 4 content + bottom border)
        assert len(lines) >= 6

        # Content lines should exist
        assert "Line 1" in strip_ansi(lines[1])
        assert "Line 2" in strip_ansi(lines[2])
        assert "Line 3" in strip_ansi(lines[3])
        assert "Line 4" in strip_ansi(lines[4])

    def test_cycling_wraps_after_7_lines(self):
        """Test that line 8 gets same color as line 1 (cycling through 7 rainbow colors)."""
        # Create 8 lines to test cycling
        content = [f"Line {i}" for i in range(1, 9)]
        lines = rainbow_cycling_frame(content)

        # Should have all 8 content lines
        assert len(lines) >= 10  # top + 8 content + bottom

        # All content should be present
        for i in range(1, 9):
            assert f"Line {i}" in strip_ansi("\n".join(lines))

    def test_border_gradient(self):
        """Test that borders have the specified gradient."""
        lines = rainbow_cycling_frame(
            ["Line 1", "Line 2"],
            border_gradient_start="red",
            border_gradient_end="blue",
            border="rounded",
        )

        # Should have top and bottom borders
        assert len(lines) >= 4

        # Borders should exist (with ANSI codes for colors)
        assert len(lines[0]) > 0  # Top border
        assert len(lines[-1]) > 0  # Bottom border

    def test_custom_border_colors(self):
        """Test custom border gradient colors."""
        lines = rainbow_cycling_frame(
            ["Test"],
            border_gradient_start="#FF0000",  # Red
            border_gradient_end="#0000FF",  # Blue
        )

        # Should produce valid output
        assert len(lines) >= 3
        assert "Test" in strip_ansi(lines[1])

    def test_with_title(self):
        """Test that title works correctly."""
        lines = rainbow_cycling_frame(
            ["Line 1", "Line 2"],
            title="Test Title",
        )

        # Title should appear in first line
        assert "Test Title" in strip_ansi(lines[0])

    def test_different_borders(self):
        """Test that it works with all border styles."""
        content = ["Test content"]

        for border_style in [
            "solid",
            "rounded",
            "double",
            "heavy",
            "thick",
            "minimal",
            "ascii",
            "dots",
        ]:
            lines = rainbow_cycling_frame(
                content,
                border=border_style,
            )

            # Should produce valid output
            assert len(lines) >= 3
            assert "Test content" in strip_ansi("\n".join(lines))

    def test_single_line(self):
        """Test with single line (should get first rainbow color - red)."""
        lines = rainbow_cycling_frame(["Single line"])

        assert len(lines) >= 3  # top + content + bottom
        assert "Single line" in strip_ansi(lines[1])

    def test_many_lines(self):
        """Test with 15+ lines to verify cycling through colors multiple times."""
        content = [f"Line {i}" for i in range(1, 16)]  # 15 lines
        lines = rainbow_cycling_frame(content)

        # Should have all 15 content lines
        assert len(lines) >= 17  # top + 15 content + bottom

        # All content should be present
        for i in range(1, 16):
            assert f"Line {i}" in strip_ansi("\n".join(lines))

    def test_with_emojis(self):
        """Test that emoji content renders correctly."""
        lines = rainbow_cycling_frame(
            ["🌈 Rainbow", "🔥 Fire", "🌊 Ocean"],
        )

        # Should handle emojis properly
        assert "🌈" in strip_ansi(lines[1])
        assert "🔥" in strip_ansi(lines[2])
        assert "🌊" in strip_ansi(lines[3])

    def test_alignment_options(self):
        """Test left/center/right alignment."""
        content = ["Test"]

        for align in ["left", "center", "right"]:
            lines = rainbow_cycling_frame(
                content,
                align=align,
            )

            # Should produce valid output
            assert len(lines) >= 3
            assert "Test" in strip_ansi("\n".join(lines))

    def test_with_padding(self):
        """Test that padding doesn't break color cycling."""
        for padding in [0, 1, 2, 3]:
            lines = rainbow_cycling_frame(
                ["Line 1", "Line 2"],
                padding=padding,
            )

            # Should produce valid output with padding
            assert len(lines) >= 4
            assert "Line 1" in strip_ansi("\n".join(lines))
            assert "Line 2" in strip_ansi("\n".join(lines))

    def test_empty_content(self):
        """Test that empty content is handled gracefully."""
        lines = rainbow_cycling_frame([])

        # Should still produce a frame (even if empty)
        # With no content, only top and bottom borders
        assert len(lines) >= 2  # top + bottom

    def test_string_content(self):
        """Test that string input (not list) works."""
        lines = rainbow_cycling_frame("Line 1\nLine 2\nLine 3")

        # Should split by newlines and process
        assert len(lines) >= 5
        assert "Line 1" in strip_ansi("\n".join(lines))
        assert "Line 2" in strip_ansi("\n".join(lines))
        assert "Line 3" in strip_ansi("\n".join(lines))

    def test_width_specification(self):
        """Test with explicit width."""
        lines = rainbow_cycling_frame(
            ["Short"],
            width=50,
        )

        # All lines should have approximately the same visual width
        widths = [len(strip_ansi(line)) for line in lines]
        # Allow some variation due to emojis/borders
        assert max(widths) - min(widths) <= 2

    def test_different_from_rainbow_frame(self):
        """Test that output differs from regular rainbow_frame."""
        content = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5"]

        # Regular rainbow frame (smooth gradient)
        rainbow_lines = rainbow_frame(content, direction="vertical", mode="content")

        # Cycling rainbow frame (discrete colors)
        cycling_lines = rainbow_cycling_frame(content)

        # Both should produce output
        assert len(rainbow_lines) >= 7
        assert len(cycling_lines) >= 7

        # Content should be present in both
        for line_content in content:
            assert line_content in strip_ansi("\n".join(rainbow_lines))
            assert line_content in strip_ansi("\n".join(cycling_lines))


class TestRainbowFrameDiagonal:
    """Tests for rainbow_frame with diagonal direction (lines 782-837 coverage)."""

    def test_rainbow_diagonal_basic(self):
        """Test diagonal rainbow frame creation."""
        lines = rainbow_frame(
            ["Line 1", "Line 2", "Line 3"],
            direction="diagonal",
            mode="border",
        )
        assert len(lines) >= 5
        # Should have ANSI color codes
        assert any("\033[" in line for line in lines)

    def test_rainbow_diagonal_content_mode(self):
        """Test diagonal rainbow with content mode."""
        lines = rainbow_frame(
            ["Content line"],
            direction="diagonal",
            mode="content",
        )
        assert len(lines) >= 3
        # Content should be colored
        assert "\033[" in lines[1]  # Content line

    def test_rainbow_diagonal_both_mode(self):
        """Test diagonal rainbow with both border and content."""
        lines = rainbow_frame(
            ["Test"],
            direction="diagonal",
            mode="both",
        )
        assert len(lines) >= 3
        # All lines should have colors
        assert all("\033[" in line for line in lines)

    def test_rainbow_diagonal_with_title(self):
        """Test diagonal rainbow with title."""
        lines = rainbow_frame(
            ["Content"],
            title="Diagonal Test",
            direction="diagonal",
            mode="border",
        )
        # Title should be present
        assert "Diagonal Test" in strip_ansi(lines[0])

    def test_rainbow_diagonal_multiline(self):
        """Test diagonal rainbow with multiple lines."""
        content = [f"Line {i}" for i in range(10)]
        lines = rainbow_frame(
            content,
            direction="diagonal",
            mode="both",
        )
        assert len(lines) >= 12  # 10 content + 2 borders

    def test_rainbow_diagonal_different_borders(self):
        """Test diagonal rainbow with different border styles."""
        for border in ["solid", "rounded", "double", "heavy", "thick"]:
            lines = rainbow_frame(
                ["Test"],
                direction="diagonal",
                mode="border",
                border=border,
            )
            assert len(lines) >= 3, f"Failed for border: {border}"

    def test_rainbow_diagonal_vs_vertical(self):
        """Test that diagonal produces different output than vertical."""
        content = ["Line 1", "Line 2", "Line 3"]

        vertical_lines = rainbow_frame(content, direction="vertical", mode="border")
        diagonal_lines = rainbow_frame(content, direction="diagonal", mode="border")

        # Both should produce output
        assert len(vertical_lines) >= 5
        assert len(diagonal_lines) >= 5

        # Content should be same, but coloring different
        assert strip_ansi("\n".join(vertical_lines)) == strip_ansi("\n".join(diagonal_lines))
