"""Tests for text wrapping utilities."""

import pytest

from styledconsole.utils.wrap import (
    auto_size_content,
    prepare_frame_content,
    truncate_lines,
    wrap_multiline,
    wrap_text,
)


class TestWrapText:
    """Tests for wrap_text function."""

    def test_wrap_simple_text(self):
        """Test basic text wrapping."""
        text = "This is a long line that needs to be wrapped"
        result = wrap_text(text, width=20)

        assert len(result) > 1
        assert all(len(line) <= 20 for line in result)
        assert " ".join(result) == text

    def test_wrap_already_fits(self):
        """Test text that already fits."""
        text = "Short text"
        result = wrap_text(text, width=20)

        assert result == ["Short text"]

    def test_wrap_empty_text(self):
        """Test wrapping empty text."""
        result = wrap_text("", width=20)
        assert result == [""]

    def test_wrap_with_paragraphs(self):
        """Test paragraph preservation."""
        text = "First paragraph.\n\nSecond paragraph."
        result = wrap_text(text, width=20, preserve_paragraphs=True)

        # Should have blank line between paragraphs
        assert "" in result

    def test_break_long_words(self):
        """Test breaking long words."""
        text = "supercalifragilisticexpialidocious"
        result = wrap_text(text, width=10, break_long_words=True)

        assert len(result) > 1
        assert all(len(line) <= 10 for line in result)

    def test_no_break_long_words(self):
        """Test not breaking long words."""
        text = "supercalifragilisticexpialidocious"
        result = wrap_text(text, width=10, break_long_words=False)

        # Should have one long line
        assert len(result) == 1


class TestWrapMultiline:
    """Tests for wrap_multiline function."""

    def test_wrap_multiple_lines(self):
        """Test wrapping multiple lines."""
        lines = [
            "Short line",
            "This is a much longer line that needs to be wrapped",
            "Another line",
        ]
        result = wrap_multiline(lines, width=20)

        assert len(result) > len(lines)  # Some lines got wrapped

    def test_preserve_empty_lines(self):
        """Test empty line preservation."""
        lines = ["Line 1", "", "Line 2"]
        result = wrap_multiline(lines, width=20)

        assert "" in result

    def test_preserve_indentation(self):
        """Test indentation preservation."""
        lines = ["  Indented line that is very long"]
        result = wrap_multiline(lines, width=15, preserve_indentation=True)

        assert all(line.startswith("  ") or not line for line in result)


class TestTruncateLines:
    """Tests for truncate_lines function."""

    def test_truncate_when_needed(self):
        """Test truncation when exceeding max lines."""
        lines = [f"Line {i}" for i in range(10)]
        result = truncate_lines(lines, max_lines=5)

        assert len(result) == 6  # 5 lines + truncation indicator
        assert "more lines" in result[-1]

    def test_no_truncate_when_fits(self):
        """Test no truncation when within limit."""
        lines = [f"Line {i}" for i in range(3)]
        result = truncate_lines(lines, max_lines=5)

        assert result == lines

    def test_custom_truncation_indicator(self):
        """Test custom truncation message."""
        lines = [f"Line {i}" for i in range(10)]
        result = truncate_lines(lines, max_lines=5, truncation_indicator="[{count} omitted]")

        assert "[5 omitted]" in result[-1]


class TestPrepareFrameContent:
    """Tests for prepare_frame_content function."""

    def test_prepare_string_content(self):
        """Test preparing string content."""
        text = "This is a very long line that needs to be wrapped for display"
        result = prepare_frame_content(text, max_width=20)

        assert len(result) > 1
        assert all(len(line) <= 20 for line in result)

    def test_prepare_list_content(self):
        """Test preparing list content."""
        lines = ["Short", "This is much longer"]
        result = prepare_frame_content(lines, max_width=10, wrap=True)

        assert len(result) > len(lines)

    def test_no_wrap_option(self):
        """Test disabling wrapping."""
        text = "Very long line"
        result = prepare_frame_content(text, max_width=5, wrap=False)

        assert result == ["Very long line"]

    def test_max_lines_truncation(self):
        """Test line count truncation."""
        text = "Line\n" * 20
        result = prepare_frame_content(text, max_lines=5)

        assert len(result) <= 6  # 5 lines + possible truncation indicator


class TestAutoSizeContent:
    """Tests for auto_size_content function."""

    def test_short_content(self):
        """Test auto-sizing short content."""
        text = "Short"
        lines, width = auto_size_content(text, max_width=80, min_width=20)

        assert lines == ["Short"]
        assert 20 <= width <= 80

    def test_long_content_wrapped(self):
        """Test auto-sizing long content (should wrap)."""
        text = "This is an extremely long line that exceeds the maximum width"
        lines, width = auto_size_content(text, max_width=30, min_width=20)

        assert len(lines) > 1
        assert width == 30  # Should use max_width since content was wrapped

    def test_medium_content_natural_width(self):
        """Test content that fits naturally."""
        text = "Medium length text"
        lines, width = auto_size_content(text, max_width=80, min_width=20)

        assert lines == ["Medium length text"]
        assert width >= len(text)

    def test_multiline_content(self):
        """Test multiline content."""
        lines_in = ["Short", "Medium length", "Very very long line"]
        lines_out, _width = auto_size_content(lines_in, max_width=50)

        assert len(lines_out) >= len(lines_in)


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_zero_width(self):
        """Test handling zero width."""
        # Should handle gracefully or raise meaningful error
        with pytest.raises(ValueError):
            wrap_text("text", width=0)

    def test_negative_max_lines(self):
        """Test negative max_lines."""
        lines = ["Line 1", "Line 2"]
        # Should return all lines (no truncation)
        result = truncate_lines(lines, max_lines=-1)
        assert result == lines

    def test_very_long_word(self):
        """Test handling very long unbreakable word."""
        word = "x" * 100
        result = prepare_frame_content(word, max_width=20, break_long_words=True)

        assert len(result) > 1

    def test_unicode_content(self):
        """Test handling Unicode characters."""
        text = "Hello 世界 🌍"
        result = wrap_text(text, width=20)

        assert result  # Should not crash

    def test_empty_list(self):
        """Test empty list input."""
        result = prepare_frame_content([], max_width=20)

        assert result == [""]
