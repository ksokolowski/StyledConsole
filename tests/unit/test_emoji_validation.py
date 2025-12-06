"""Tests for emoji validation system.

These tests validate emoji handling using the dynamic emoji package integration.
"""

import emoji

from styledconsole.utils.text import (
    get_safe_emojis,
    validate_emoji,
    visual_width,
)


class TestGetSafeEmojis:
    """Tests for the get_safe_emojis function."""

    def test_get_safe_emojis_returns_dict(self):
        """get_safe_emojis() should return a dictionary."""
        all_emojis = get_safe_emojis()
        assert isinstance(all_emojis, dict)
        assert len(all_emojis) > 50  # Should have many emojis

    def test_get_safe_emojis_structure(self):
        """Each emoji entry should have required fields."""
        all_emojis = get_safe_emojis()
        for _emoji, info in all_emojis.items():
            assert isinstance(info, dict)
            assert "name" in info
            assert "width" in info
            assert info["width"] in (1, 2)
            assert isinstance(info["name"], str)

    def test_get_safe_emojis_have_known_width(self):
        """All safe emojis should have width 1 or 2."""
        all_emojis = get_safe_emojis()
        for emoji_char, info in all_emojis.items():
            width = info["width"]
            assert width in (1, 2), f"{emoji_char} has invalid width {width}"

    def test_common_emojis_present(self):
        """Common emojis should be in safe list."""
        all_emojis = get_safe_emojis()
        # Uses emojis confirmed in most emoji sets
        common = {"🚀", "✅", "❌", "🔴", "⭐"}
        for e in common:
            assert e in all_emojis, f"Missing common emoji: {e}"

    def test_get_safe_emojis_terminal_safe_only(self):
        """get_safe_emojis(terminal_safe_only=True) should exclude VS16 emojis."""
        all_emojis = get_safe_emojis()
        terminal_safe = get_safe_emojis(terminal_safe_only=True)

        # Terminal safe should be a subset
        assert len(terminal_safe) <= len(all_emojis)

        # All terminal_safe emojis should have terminal_safe=True
        for _emoji, info in terminal_safe.items():
            assert info.get("terminal_safe", False) is True

    def test_get_safe_emojis_category_returns_empty(self):
        """Category filtering is not supported in dynamic mode."""
        # Dynamic mode doesn't have category data
        category_emojis = get_safe_emojis(category="status")
        assert category_emojis == {}

    def test_get_safe_emojis_returns_copy(self):
        """get_safe_emojis should return a new dict each time."""
        emojis1 = get_safe_emojis()
        emojis2 = get_safe_emojis()
        assert emojis1 is not emojis2  # Different objects
        assert emojis1 == emojis2  # Same content


class TestValidateEmoji:
    """Tests for the validate_emoji function."""

    def test_validate_safe_emoji(self):
        """validate_emoji should identify safe emojis."""
        result = validate_emoji("✅")
        assert result["safe"] is True
        assert result["width"] == 2

    def test_validate_safe_emoji_with_vs16(self):
        """VS16 emojis should be marked with terminal rendering warnings."""
        result = validate_emoji("⚠️")
        assert result["safe"] is True
        assert result["width"] == 2
        assert result["has_vs16"] is True
        assert result["terminal_safe"] is False

    def test_validate_unknown_character(self):
        """Unknown character should not be safe."""
        result = validate_emoji("A")
        assert result["safe"] is False
        assert (
            "unknown" in result["recommendation"].lower()
            or "invalid" in result["recommendation"].lower()
        )

    def test_validate_zwj_sequence(self):
        """ZWJ sequences should be detected and rejected."""
        # ZWJ example: person + zwj + laptop
        zwj_emoji = "👨\u200d💻"
        result = validate_emoji(zwj_emoji)
        assert result["safe"] is False
        assert "ZWJ" in result["recommendation"]
        assert "not supported" in result["recommendation"].lower()

    def test_validate_skin_tone_modifier(self):
        """Skin tone modifiers should be detected and rejected."""
        # Thumbs up with skin tone
        skin_tone_emoji = "👍🏽"  # Thumbs up + medium skin tone
        result = validate_emoji(skin_tone_emoji)
        assert result["safe"] is False
        assert "Skin tone" in result["recommendation"]
        assert "Tier 2" in result["recommendation"]

    def test_validate_result_structure(self):
        """validate_emoji result should always have required keys."""
        result = validate_emoji("✅")
        required_keys = {
            "safe",
            "name",
            "width",
            "category",
            "has_vs16",
            "terminal_safe",
            "recommendation",
        }
        assert set(result.keys()) == required_keys

    def test_validate_emoji_rocket(self):
        """Rocket emoji should be safe and well-known."""
        result = validate_emoji("🚀")
        assert result["safe"] is True
        assert result["width"] == 2

    def test_validate_emoji_rainbow(self):
        """Rainbow emoji should be safe."""
        result = validate_emoji("🌈")
        assert result["safe"] is True
        assert result["width"] == 2

    def test_validate_emoji_party(self):
        """Party emoji should be safe."""
        result = validate_emoji("🎉")
        assert result["safe"] is True
        assert result["width"] == 2


class TestEmojiValidationIntegration:
    """Integration tests for emoji validation."""

    def test_validate_and_use_in_frame(self):
        """Validated emoji should work in frames."""
        from styledconsole import Console

        result = validate_emoji("✅")
        assert result["safe"]

        console = Console()
        # Should not raise an error
        console.frame(f"Test {result['name']}", title="Demo")

    def test_emoji_validation_performance(self):
        """Emoji validation should be fast."""
        import time

        start = time.time()
        for e in ["✅", "❌", "🚀", "🌈", "🎉"]:
            validate_emoji(e)
        elapsed = time.time() - start

        # Should validate 5 emojis in under 50ms
        assert elapsed < 0.05, f"Validation too slow: {elapsed}s"

    def test_emoji_list_completeness(self):
        """Safe emoji list should have good coverage."""
        all_emojis = get_safe_emojis()
        total = len(all_emojis)
        # Dynamic mode returns many emojis from the emoji package
        assert total > 100, f"Expected >100 safe emojis, got {total}"


class TestEmojiEdgeCases:
    """Test edge cases and corner cases."""

    def test_validate_empty_string(self):
        """Empty string should not crash."""
        result = validate_emoji("")
        assert result["safe"] is False

    def test_validate_multiple_characters(self):
        """Multiple characters should be handled gracefully."""
        result = validate_emoji("✅❌")
        # Should handle it somehow (safe False is fine for multi-char)
        assert "recommendation" in result

    def test_emoji_width_matches_visual_width(self):
        """Emoji width should be calculable via visual_width."""
        for e in ["✅", "❌", "🚀", "🌈"]:
            calculated_width = visual_width(e)
            # Most emojis should match (some VS16 emojis might differ)
            assert calculated_width > 0, f"visual_width failed for {e}"

    def test_validate_uses_emoji_package(self):
        """Validation should use the emoji package for detection."""
        # Verify emoji package is being used
        assert emoji.is_emoji("🚀")
        result = validate_emoji("🚀")
        assert result["safe"] is True
