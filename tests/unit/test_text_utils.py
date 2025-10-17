"""Unit tests for text width utilities."""

import pytest

from styledconsole.utils.text import (
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

        Note: Emojis with variation selector (U+FE0F) are rendered as width=1
        due to terminal-specific behavior. See visual_width() documentation.
        """
        assert visual_width("🚀") == 2  # Rocket (no VS16)
        assert visual_width("✅") == 2  # Check mark
        assert visual_width("❌") == 2  # Cross mark
        assert visual_width("⚠️") == 1  # Warning + VS16 → width=1 (terminal fix)
        assert visual_width("⚠") == 1  # Warning without VS16 → width=1
        assert visual_width("ℹ️") == 1  # Info + VS16 → width=1 (terminal fix)
        assert visual_width("ℹ") == 1  # Info without VS16 → width=1
        assert visual_width("⭐") == 2  # Star (no VS16)
        assert visual_width("🎉") == 2  # Party popper (no VS16)
        assert visual_width("❤️") == 1  # Heart + VS16 → width=1 (terminal fix)
        assert visual_width("❤") == 1  # Heart without VS16 → width=1

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

        Note: Emojis with Variation Selector-16 (U+FE0F) are rendered as
        width=1 to match actual terminal behavior, not wcwidth's theoretical width=2.
        """
        tier1_emojis = [
            ("✅", "check mark", 2),  # No VS16
            ("❌", "cross mark", 2),  # No VS16
            ("⚠️", "warning", 1),  # Has VS16 → width=1 (terminal fix)
            ("ℹ️", "info", 1),  # Has VS16 → width=1 (terminal fix)
            ("⭐", "star", 2),  # No VS16
            ("🚀", "rocket", 2),  # No VS16
            ("❤️", "heart", 1),  # Has VS16 → width=1 (terminal fix)
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

    def test_variation_selector_terminal_fix(self):
        """Variation selectors are handled according to terminal behavior.

        Many terminals display emoji+VS16 with the width of the base character,
        not the width=2 that wcwidth reports. Our fix matches terminal behavior.
        """
        # These emojis have VS16, terminal renders them as width=1
        assert visual_width("⚠️") == 1  # Warning + VS16
        assert visual_width("ℹ️") == 1  # Info + VS16
        assert visual_width("❤️") == 1  # Heart + VS16
        assert visual_width("🏗️") == 1  # Building + VS16

        # Without VS16, base characters are width=1
        assert visual_width("⚠") == 1  # Warning alone
        assert visual_width("ℹ") == 1  # Info alone
        assert visual_width("❤") == 1  # Heart alone

    def test_variation_selector_in_text(self):
        """VS16 emojis in text are calculated correctly."""
        # Each emoji with VS16 counts as width=1 (terminal behavior)
        assert visual_width("⚠️  Warning") == 10  # 1 + 2 spaces + 7 chars
        assert visual_width("ℹ️  Info") == 7  # 1 + 2 spaces + 4 chars
        assert visual_width("Test 🏗️ emoji") == 12  # 4 + 1 + 1 + 1 + 5

    def test_variation_selector_vs_no_selector(self):
        """Text should have same width with or without VS16."""
        # Since terminal renders both as width=1, they should match
        assert visual_width("⚠️  Warning") == visual_width("⚠  Warning")
        assert visual_width("ℹ️  Info") == visual_width("ℹ  Info")

    def test_multiple_variation_selectors(self):
        """Multiple VS16 emojis in one string."""
        text = "⚠️ ℹ️ ❤️"  # Three emojis with VS16, two spaces
        # 1 + 1 + 1 + 1 + 1 = 5
        assert visual_width(text) == 5


class TestTier2Tier3FutureWork:
    """Document limitations for Tier 2/3 (future work)."""

    def test_tier2_skin_tones_known_limitation(self):
        """Tier 2: Modified emojis with skin tones - future work.

        These may have alignment issues in v0.1 as they use
        multiple codepoints (emoji + modifier).
        """
        # Example: 👍🏽 (thumbs up + medium skin tone)
        # This is composed of 2 codepoints
        # Current implementation may not handle perfectly
        pass

    def test_tier3_zwj_sequences_known_limitation(self):
        """Tier 3: ZWJ sequences - future work.

        Complex multi-codepoint emojis like 👨‍👩‍👧‍👦 (family)
        or 👨‍💻 (man technologist) will be addressed in v0.3+.
        """
        # These use Zero-Width Joiners to combine multiple emojis
        # Example: 👨‍💻 = 👨 (man) + ZWJ + 💻 (laptop)
        pass


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
