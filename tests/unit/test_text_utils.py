"""Unit tests for text width utilities."""

import pytest

from styledconsole.utils.text import (
    format_emoji_with_spacing,
    get_emoji_spacing_adjustment,
    get_safe_emojis,
    normalize_content,
    pad_to_width,
    split_graphemes,
    strip_ansi,
    truncate_to_width,
    visual_width,
)


class TestStripAnsi:
    """Test ANSI escape sequence removal."""

    def test_strip_simple_color(self):
        """Strip simple color codes."""
        assert strip_ansi("\033[31mRed\033[0m") == "Red"
        assert strip_ansi("\033[32mGreen\033[0m") == "Green"

    def test_strip_multiple_codes(self):
        """Strip multiple ANSI codes."""
        text = "\033[1m\033[31mBold Red\033[0m"
        assert strip_ansi(text) == "Bold Red"

    def test_strip_no_ansi(self):
        """Text without ANSI codes remains unchanged."""
        assert strip_ansi("Plain text") == "Plain text"
        assert strip_ansi("Hello 🚀") == "Hello 🚀"

    def test_strip_empty(self):
        """Empty string remains empty."""
        assert strip_ansi("") == ""


class TestVisualWidth:
    """Test visual width calculation."""

    def test_ascii_text(self):
        """ASCII text has width equal to length."""
        assert visual_width("Hello") == 5
        assert visual_width("Test") == 4
        assert visual_width("") == 0

    def test_tier1_basic_icons(self):
        """Tier 1: Basic single-codepoint emojis have width=2.

        Note: Emojis with variation selector (U+FE0F) are NOT safe for
        consistent rendering and are excluded from SAFE_EMOJIS.
        """
        assert visual_width("🚀") == 2  # Rocket (no VS16)
        assert visual_width("✅") == 2  # Check mark
        assert visual_width("❌") == 2  # Cross mark
        assert visual_width("⭐") == 2  # Star (no VS16)
        assert visual_width("🎉") == 2  # Party popper (no VS16)
        # VS16 emojis have terminal-dependent width behavior (excluded from SAFE_EMOJIS)

    def test_mixed_text_and_icons(self):
        """Mixed ASCII and emojis."""
        assert visual_width("Test 🚀") == 7  # 4 + 1 space + 2
        assert visual_width("Test 🚀 🎉") == 10  # 4 + 1 + 2 + 1 + 2 = 10
        assert visual_width("✅ Done") == 7  # 2 + 1 + 4

    def test_ansi_codes_stripped(self):
        """ANSI codes don't contribute to width."""
        assert visual_width("\033[31mRed\033[0m") == 3
        assert visual_width("\033[1m\033[32mBold Green\033[0m") == 10
        assert visual_width("\033[31m🚀\033[0m") == 2

    def test_whitespace(self):
        """Whitespace has width=1."""
        assert visual_width(" ") == 1
        assert visual_width("   ") == 3
        assert visual_width("\t") == 1  # Tab counts as 1

    def test_wide_characters(self):
        """Wide characters (CJK) have width=2."""
        assert visual_width("你好") == 4  # 2 Chinese characters
        assert visual_width("こんにちは") == 10  # 5 Japanese characters

    def test_zero_width_characters(self):
        """Zero-width characters are handled correctly."""
        # Combining characters, zero-width joiners, etc.
        # wcwidth should handle these
        assert visual_width("a\u0301") == 1  # a with combining acute accent


class TestSplitGraphemes:
    """Test grapheme splitting."""

    def test_ascii_text(self):
        """Split ASCII text into characters."""
        assert split_graphemes("Hello") == ["H", "e", "l", "l", "o"]
        assert split_graphemes("Hi") == ["H", "i"]

    def test_with_emojis(self):
        """Split text with emojis."""
        assert split_graphemes("Hi 🚀") == ["H", "i", " ", "🚀"]
        assert split_graphemes("✅❌") == ["✅", "❌"]

    def test_with_ansi_codes(self):
        """ANSI codes are preserved with adjacent characters."""
        result = split_graphemes("\033[31mR\033[0me\033[0md")
        # ANSI code attaches to previous grapheme if exists, else standalone
        # First ANSI has no previous char, so it's standalone
        assert len(result) == 4  # [ansi, R+ansi, e+ansi, d]
        assert "\033[31m" in result[0]  # First ANSI standalone
        assert "R" in result[1]

    def test_empty_string(self):
        """Empty string returns empty list."""
        assert split_graphemes("") == []


class TestPadToWidth:
    """Test text padding."""

    def test_pad_left(self):
        """Pad text on the right (left-aligned)."""
        assert pad_to_width("Hi", 5, "left") == "Hi   "
        assert pad_to_width("Test", 10, "left") == "Test      "

    def test_pad_right(self):
        """Pad text on the left (right-aligned)."""
        assert pad_to_width("Hi", 5, "right") == "   Hi"
        assert pad_to_width("Test", 10, "right") == "      Test"

    def test_pad_center(self):
        """Center text with padding."""
        assert pad_to_width("X", 5, "center") == "  X  "
        assert pad_to_width("Hi", 6, "center") == "  Hi  "
        assert pad_to_width("Test", 10, "center") == "   Test   "

    def test_pad_with_emojis_left(self):
        """Pad emoji text (left-aligned)."""
        assert pad_to_width("🚀", 4, "left") == "🚀  "  # 2 + 2 spaces
        assert pad_to_width("✅", 5, "left") == "✅   "  # 2 + 3 spaces

    def test_pad_with_emojis_center(self):
        """Center emoji text."""
        assert pad_to_width("✅", 6, "center") == "  ✅  "  # 2 + 2 + 2
        assert pad_to_width("🚀", 8, "center") == "   🚀   "  # 3 + 2 + 3

    def test_pad_exact_width(self):
        """No padding needed when width matches."""
        assert pad_to_width("Hello", 5, "left") == "Hello"
        assert pad_to_width("🚀", 2, "left") == "🚀"

    def test_pad_too_wide_raises(self):
        """Raise error if text exceeds target width."""
        with pytest.raises(ValueError, match="exceeds target width"):
            pad_to_width("Hello World", 5, "left")

    def test_pad_invalid_align_raises(self):
        """Raise error for invalid alignment."""
        with pytest.raises(ValueError, match="Invalid align value"):
            pad_to_width("Hi", 5, "invalid")  # type: ignore

    def test_pad_custom_fill_char(self):
        """Use custom fill character."""
        assert pad_to_width("Hi", 5, "left", "-") == "Hi---"
        assert pad_to_width("X", 5, "center", "*") == "**X**"


class TestTruncateToWidth:
    """Test text truncation."""

    def test_truncate_longer_text(self):
        """Truncate text that exceeds width."""
        assert truncate_to_width("Hello World", 8) == "Hello..."
        assert truncate_to_width("Testing", 5) == "Te..."

    def test_truncate_fits(self):
        """Text that fits is not truncated."""
        assert truncate_to_width("Hi", 10) == "Hi"
        assert truncate_to_width("Hello", 5) == "Hello"

    def test_truncate_with_emoji(self):
        """Truncate text with emojis."""
        assert truncate_to_width("🚀 Rocket", 5) == "🚀..."
        assert truncate_to_width("Test 🚀 🎉", 8) == "Test ..."

    def test_truncate_custom_suffix(self):
        """Use custom truncation suffix."""
        assert truncate_to_width("Hello World", 8, "…") == "Hello W…"
        assert truncate_to_width("Testing", 6, "->") == "Test->"

    def test_truncate_no_space_for_suffix(self):
        """Handle case where width is too small for suffix."""
        assert truncate_to_width("Hello", 2, "...") == ".."
        assert truncate_to_width("Test", 1, "...") == "."

    def test_truncate_emoji_respects_width(self):
        """Ensure emoji boundaries are respected."""
        # "🚀🎉" = 4 width, truncate to 3 should keep only first emoji
        result = truncate_to_width("🚀🎉", 5, "...")
        assert visual_width(result) <= 5


class TestTier1EmojiSupport:
    """Test Tier 1 emoji support explicitly."""

    def test_common_tier1_emojis(self):
        """Common Tier 1 emojis from specification.

        Only emojis WITHOUT Variation Selector-16 (U+FE0F) are considered safe.
        VS16 emojis are excluded from SAFE_EMOJIS due to terminal inconsistencies.
        """
        tier1_emojis = [
            ("✅", "check mark", 2),  # No VS16
            ("❌", "cross mark", 2),  # No VS16
            ("⭐", "star", 2),  # No VS16
            ("🚀", "rocket", 2),  # No VS16
            ("🎉", "party popper", 2),  # No VS16
            ("💡", "light bulb", 2),  # No VS16
            ("📝", "memo", 2),  # No VS16
            ("🔥", "fire", 2),  # No VS16
            ("👍", "thumbs up", 2),  # No VS16
            ("😀", "grinning face", 2),  # No VS16
            ("🌟", "glowing star", 2),  # No VS16
            ("📊", "bar chart", 2),  # No VS16
        ]

        for emoji, name, expected_width in tier1_emojis:
            width = visual_width(emoji)
            assert width == expected_width, (
                f"{name} ({emoji}) has width {width}, expected {expected_width}"
            )


class TestVariationSelector:
    """Test emoji variation selector (U+FE0F) handling."""

    def test_variation_selector_detected_dynamically(self):
        """VS16 emojis are detected dynamically and marked as not terminal-safe.

        VS16 emojis have has_vs16=True, width=2, but terminal_safe=False
        because many terminals render them inconsistently (as width 1).
        """
        # Get all safe emojis dynamically
        all_emojis = get_safe_emojis()

        # Check some known VS16 emojis
        vs16_emojis = ["⚠️", "ℹ️", "❤️", "⚙️", "☀️"]
        for e in vs16_emojis:
            if e in all_emojis:
                info = all_emojis[e]
                assert info.get("has_vs16") is True, f"{e} should have has_vs16=True"
                assert info.get("terminal_safe") is False, f"{e} should have terminal_safe=False"


class TestModernTerminalZwjSupport:
    """Test ZWJ sequence handling in modern terminals (v0.9.6+)."""

    def test_zwj_sequence_width_modern(self, monkeypatch):
        """ALL ZWJ sequences should have width 2 in modern terminal mode.

        Modern terminals (Kitty, WezTerm, iTerm2, Ghostty, Alacritty) render
        ALL ZWJ sequences as a single glyph with width 2, regardless of how
        many component emojis are joined.
        """
        # Force modern terminal mode
        monkeypatch.setenv("STYLEDCONSOLE_MODERN_TERMINAL", "1")
        visual_width.cache_clear()

        # Family: Man + ZWJ + Woman + ZWJ + Girl (3 components) = width 2
        assert visual_width("👨‍👩‍👧") == 2

        # Larger family (4 components) = still width 2
        assert visual_width("👨‍👩‍👧‍👦") == 2

        # Technologist: Man + ZWJ + Laptop (2 components) = width 2
        assert visual_width("👨‍💻") == 2

        # Scientist: Woman + ZWJ + Microscope (2 components) = width 2
        assert visual_width("👩‍🔬") == 2

        # Rainbow Flag: Flag + VS16 + ZWJ + Rainbow = width 2
        assert visual_width("🏳️‍🌈") == 2

    def test_vs16_sequence_width_modern(self, monkeypatch):
        """VS16 sequences should have width 2 in modern terminal mode.

        VS16 (Emoji Presentation) forces emojis to display as wide glyphs
        in modern terminals (Kitty).
        """
        monkeypatch.setenv("STYLEDCONSOLE_MODERN_TERMINAL", "1")
        visual_width.cache_clear()

        # Warning (U+26A0 + VS16)
        # wcwidth report: 2
        # Actual render: 2 (in Kitty)
        assert visual_width("⚠️\ufe0f") == 2

        # Information (U+2139 + VS16)
        assert visual_width("ℹ️\ufe0f") == 2

    def test_vs16_sequence_width_standard(self, monkeypatch):
        """VS16 sequences should have width 1 in standard terminal mode (legacy behavior)."""
        monkeypatch.setenv("STYLEDCONSOLE_MODERN_TERMINAL", "0")
        monkeypatch.setenv("STYLEDCONSOLE_LEGACY_EMOJI", "0")
        visual_width.cache_clear()

        # Warning (U+26A0 + VS16)
        # Standard mode forces width 1 for compatibility with older terminals
        assert visual_width("⚠️\ufe0f") == 1

        # Information (U+2139 + VS16)
        assert visual_width("ℹ️\ufe0f") == 1


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_string(self):
        """Handle empty strings."""
        assert visual_width("") == 0
        assert split_graphemes("") == []
        assert pad_to_width("", 5) == "     "
        assert truncate_to_width("", 5) == ""

    def test_only_ansi_codes(self):
        """Handle strings with only ANSI codes."""
        assert visual_width("\033[31m\033[0m") == 0
        assert strip_ansi("\033[31m\033[0m") == ""

    def test_only_whitespace(self):
        """Handle whitespace-only strings."""
        assert visual_width("   ") == 3
        assert pad_to_width("   ", 5) == "     "

    def test_unicode_edge_cases(self):
        """Handle various Unicode edge cases."""
        # Combining diacritics
        assert visual_width("café") == 4  # é is 1 character

        # Zero-width space
        assert visual_width("a\u200bb") == 2  # zero-width space


class TestNormalizeContent:
    """Tests for normalize_content()."""

    def test_string_with_newlines(self):
        """Test string with newlines splits into lines."""
        result = normalize_content("Line 1\nLine 2\nLine 3")
        assert result == ["Line 1", "Line 2", "Line 3"]

    def test_string_without_newlines(self):
        """Test single-line string."""
        result = normalize_content("Single line")
        assert result == ["Single line"]

    def test_empty_string(self):
        """Test empty string returns list with empty string."""
        result = normalize_content("")
        assert result == [""]

    def test_list_of_strings(self):
        """Test list of strings is returned as-is."""
        input_list = ["Line 1", "Line 2"]
        result = normalize_content(input_list)
        assert result == ["Line 1", "Line 2"]

    def test_empty_list(self):
        """Test empty list returns list with empty string."""
        result = normalize_content([])
        assert result == [""]

    def test_list_with_empty_strings(self):
        """Test list with empty strings preserved."""
        result = normalize_content(["", "text", ""])
        assert result == ["", "text", ""]

    def test_string_with_only_newlines(self):
        """Test string with only newlines."""
        result = normalize_content("\n\n")
        # splitlines() returns ["", ""] for "\n\n" (2 newlines = 2 empty strings)
        assert result == ["", ""]

    def test_string_with_trailing_newline(self):
        """Test string with trailing newline."""
        result = normalize_content("Line 1\nLine 2\n")
        # splitlines() removes trailing newline
        assert result == ["Line 1", "Line 2"]

    def test_preserves_whitespace(self):
        """Test whitespace in lines is preserved."""
        result = normalize_content("  Line 1  \n\tLine 2\t")
        assert result == ["  Line 1  ", "\tLine 2\t"]

    def test_with_unicode_content(self):
        """Test normalization with unicode content."""
        result = normalize_content("Hello 🚀\nWorld 🎉")
        assert result == ["Hello 🚀", "World 🎉"]

    def test_does_not_modify_original_list(self):
        """Test that original list is not modified if non-empty."""
        original = ["Line 1", "Line 2"]
        result = normalize_content(original)
        assert result == original
        # For non-empty lists, we return the same list (optimization)
        # This is fine since we're not modifying it


class TestEmojiSpacingAdjustment:
    """Test emoji spacing adjustment detection."""

    def test_standard_emoji_no_adjustment(self):
        """Standard emojis with correct width don't need adjustment."""
        assert get_emoji_spacing_adjustment("✅") == 0  # Check mark
        assert get_emoji_spacing_adjustment("🚀") == 0  # Rocket
        assert get_emoji_spacing_adjustment("🎉") == 0  # Party popper
        assert get_emoji_spacing_adjustment("❌") == 0  # Cross mark
        assert get_emoji_spacing_adjustment("🔥") == 0  # Fire

    def test_non_safe_emoji_raises_error(self):
        """Non-safe emojis raise ValueError."""
        # ZWJ sequences are valid emojis but may not be in the dynamic safe list
        # The function now validates using emoji.is_emoji, so these won't raise
        # Instead, test with an invalid non-emoji character
        with pytest.raises(ValueError, match="Invalid emoji"):
            get_emoji_spacing_adjustment("X")  # Not an emoji

        with pytest.raises(ValueError, match="Invalid emoji"):
            get_emoji_spacing_adjustment("")  # Empty string

    def test_adjustment_range(self):
        """Adjustment is always 0, 1, or 2."""
        all_emojis = get_safe_emojis()
        for emoji in all_emojis:
            adjustment = get_emoji_spacing_adjustment(emoji)
            assert adjustment in (0, 1, 2), (
                f"Emoji {emoji} returned invalid adjustment: {adjustment}"
            )


class TestFormatEmojiWithSpacing:
    """Test emoji formatting with automatic spacing."""

    def test_standard_emoji_single_space(self):
        """Standard emojis use single space separator."""
        assert format_emoji_with_spacing("✅", "Success") == "✅ Success"
        assert format_emoji_with_spacing("🚀", "Launch") == "🚀 Launch"
        assert format_emoji_with_spacing("❌", "Failed") == "❌ Failed"

    def test_emoji_without_text(self):
        """Emoji without text returns just emoji."""
        assert format_emoji_with_spacing("✅") == "✅"
        assert format_emoji_with_spacing("") == ""

    def test_custom_separator(self):
        """Custom separator is used as base."""
        # Standard emoji with custom sep
        assert format_emoji_with_spacing("✅", "Success", sep="") == "✅Success"
        assert format_emoji_with_spacing("✅", "Success", sep="  ") == "✅  Success"

    def test_all_safe_emojis_format_without_error(self):
        """All safe emojis can be formatted without error."""
        all_emojis = get_safe_emojis()
        for emoji in all_emojis:
            # Should not raise any error
            result = format_emoji_with_spacing(emoji, "Test")
            assert isinstance(result, str)
            assert emoji in result
            assert "Test" in result

    def test_formatting_consistency(self):
        """Formatted output is consistent for safe emojis."""
        # Safe emojis without VS16 should have consistent spacing
        for emoji in ["✅", "🚀", "❌", "🎉"]:
            adjustment = get_emoji_spacing_adjustment(emoji)
            formatted = format_emoji_with_spacing(emoji, "Text")
            expected_spaces = 1 + adjustment  # 1 for base sep, + adjustment

            # Extract spaces between emoji and text
            spaces_in_result = formatted.split("Text")[0].replace(emoji, "")
            assert len(spaces_in_result) == expected_spaces
