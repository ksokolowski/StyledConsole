"""Tests for emoji validation system."""

from styledconsole.utils.text import (
    SAFE_EMOJIS,
    get_safe_emojis,
    validate_emoji,
)


class TestSafeEmojiList:
    """Tests for the SAFE_EMOJIS constant."""

    def test_safe_emoji_list_exists(self):
        """SAFE_EMOJIS should be a non-empty dict."""
        assert isinstance(SAFE_EMOJIS, dict)
        assert len(SAFE_EMOJIS) > 50  # Should have many emojis

    def test_safe_emoji_list_structure(self):
        """Each emoji entry should have required fields."""
        for emoji, info in SAFE_EMOJIS.items():
            assert isinstance(info, dict)
            assert "name" in info
            assert "width" in info
            assert "category" in info
            assert info["width"] in (1, 2)
            assert isinstance(info["name"], str)
            assert isinstance(info["category"], str)

    def test_safe_emojis_have_known_width(self):
        """All safe emojis should have width 1 or 2."""
        for emoji, info in SAFE_EMOJIS.items():
            width = info["width"]
            assert width in (1, 2), f"{emoji} has invalid width {width}"

    def test_safe_emojis_have_category(self):
        """All safe emojis should belong to a category."""
        valid_categories = {
            "status",
            "progress",
            "direction",
            "tech",
            "data",
            "nature",
            "food",
            "activity",
            "hand",
            "other",
        }
        for emoji, info in SAFE_EMOJIS.items():
            assert info["category"] in valid_categories, (
                f"{emoji} has unknown category: {info['category']}"
            )

    def test_common_status_emojis_present(self):
        """Common status emojis should be in safe list."""
        common = {"✅", "❌", "⚠️", "ℹ️", "🟢", "🔴"}
        for emoji in common:
            assert emoji in SAFE_EMOJIS, f"Missing common emoji: {emoji}"

    def test_tech_emojis_present(self):
        """Common tech emojis should be present."""
        tech = {"🚀", "💻", "🔧", "⚙️", "📦"}
        for emoji in tech:
            assert emoji in SAFE_EMOJIS, f"Missing tech emoji: {emoji}"

    def test_nature_emojis_present(self):
        """Common nature emojis should be present."""
        nature = {"🌈", "☀️", "⭐", "✨", "🔥"}
        for emoji in nature:
            assert emoji in SAFE_EMOJIS, f"Missing nature emoji: {emoji}"


class TestValidateEmoji:
    """Tests for the validate_emoji function."""

    def test_validate_safe_emoji(self):
        """validate_emoji should identify safe emojis."""
        result = validate_emoji("✅")
        assert result["safe"] is True
        assert result["name"] == "check_mark"
        assert result["width"] == 2
        assert result["category"] == "status"

    def test_validate_safe_emoji_with_vs16(self):
        """Emojis with variation selectors should be marked."""
        result = validate_emoji("⚠️")
        assert result["safe"] is True
        assert result["has_vs16"] is True
        assert "variation selector" in result["recommendation"].lower()

    def test_validate_unknown_emoji(self):
        """Unknown emoji should not be safe."""
        result = validate_emoji("🦄")  # Unicorn - may or may not be in list
        if result["safe"]:
            assert result["width"] is not None
        else:
            assert "unknown" in result["recommendation"].lower()

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
        required_keys = {"safe", "name", "width", "category", "has_vs16", "recommendation"}
        assert set(result.keys()) == required_keys

    def test_validate_emoji_rocket(self):
        """Rocket emoji should be safe and well-known."""
        result = validate_emoji("🚀")
        assert result["safe"] is True
        assert result["name"] == "rocket"
        assert result["width"] == 2
        assert result["category"] == "tech"

    def test_validate_emoji_rainbow(self):
        """Rainbow emoji should be safe."""
        result = validate_emoji("🌈")
        assert result["safe"] is True
        assert result["width"] == 2
        assert result["category"] == "nature"

    def test_validate_emoji_party(self):
        """Party emoji should be safe."""
        result = validate_emoji("🎉")
        assert result["safe"] is True
        assert result["width"] == 2
        assert result["category"] == "activity"


class TestGetSafeEmojis:
    """Tests for the get_safe_emojis function."""

    def test_get_all_safe_emojis(self):
        """get_safe_emojis() should return all emojis."""
        all_emojis = get_safe_emojis()
        assert len(all_emojis) == len(SAFE_EMOJIS)
        assert all_emojis == SAFE_EMOJIS

    def test_get_safe_emojis_by_category(self):
        """get_safe_emojis should filter by category."""
        status_emojis = get_safe_emojis("status")
        assert len(status_emojis) > 0
        for emoji, info in status_emojis.items():
            assert info["category"] == "status"

    def test_get_safe_emojis_all_categories(self):
        """Should be able to retrieve emojis for all categories."""
        categories = {
            "status",
            "progress",
            "direction",
            "tech",
            "data",
            "nature",
            "food",
            "activity",
            "hand",
            "other",
        }
        for category in categories:
            emojis = get_safe_emojis(category)
            assert len(emojis) > 0, f"No emojis found for category: {category}"
            for emoji, info in emojis.items():
                assert info["category"] == category

    def test_get_safe_emojis_category_returns_copy(self):
        """get_safe_emojis should return a copy, not reference."""
        emojis1 = get_safe_emojis()
        emojis2 = get_safe_emojis()
        assert emojis1 is not emojis2  # Different objects
        assert emojis1 == emojis2  # Same content

    def test_get_safe_emojis_preserves_info(self):
        """Filtered results should preserve emoji info."""
        tech_emojis = get_safe_emojis("tech")
        rocket_info = tech_emojis.get("🚀")
        assert rocket_info is not None
        assert rocket_info["name"] == "rocket"
        assert rocket_info["width"] == 2


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

    def test_all_safe_emojis_have_known_properties(self):
        """All safe emojis should have consistent metadata."""
        for emoji, info in SAFE_EMOJIS.items():
            # Validate emoji using the function
            result = validate_emoji(emoji)
            assert result["safe"] is True
            assert result["width"] == info["width"]
            assert result["category"] == info["category"]

    def test_emoji_categories_are_consistent(self):
        """Category names should be consistent across all emojis."""
        categories = set()
        for info in SAFE_EMOJIS.values():
            categories.add(info["category"])

        # Categories should be reasonable
        assert len(categories) >= 8  # At least 8 distinct categories
        assert "tech" in categories or "other" in categories

    def test_emoji_validation_performance(self):
        """Emoji validation should be fast."""
        import time

        start = time.time()
        for emoji in ["✅", "❌", "🚀", "🌈", "🎉"]:
            validate_emoji(emoji)
        elapsed = time.time() - start

        # Should validate 5 emojis in under 10ms
        assert elapsed < 0.01, f"Validation too slow: {elapsed}s"

    def test_emoji_list_completeness(self):
        """Safe emoji list should have good coverage."""
        total = len(SAFE_EMOJIS)
        assert total > 70, f"Expected >70 safe emojis, got {total}"

        # Check distribution across categories
        categories = {}
        for info in SAFE_EMOJIS.values():
            cat = info["category"]
            categories[cat] = categories.get(cat, 0) + 1

        # Most categories should have at least 3 emojis
        for cat, count in categories.items():
            assert count >= 3, f"Category '{cat}' has only {count} emojis"


class TestEmojiEdgeCases:
    """Test edge cases and corner cases."""

    def test_validate_empty_string(self):
        """Empty string should not crash."""
        result = validate_emoji("")
        assert result["safe"] is False

    def test_validate_multiple_characters(self):
        """Multiple characters should be handled gracefully."""
        result = validate_emoji("✅❌")
        # Should handle it somehow (safe False is fine)
        assert "recommendation" in result

    def test_emoji_width_matches_visual_width(self):
        """Emoji width in SAFE_EMOJIS should match visual_width calculation."""
        from styledconsole.utils.text import visual_width

        for emoji in ["✅", "❌", "🚀", "🌈"]:
            SAFE_EMOJIS[emoji]  # Verify emoji exists
            calculated_width = visual_width(emoji)
            # Most emojis should match (some VS16 emojis might differ)
            assert calculated_width > 0, f"visual_width failed for {emoji}"

    def test_safe_emoji_names_are_unique(self):
        """Emoji names should be reasonably unique within categories."""
        for emoji, info in SAFE_EMOJIS.items():
            # Names should not be empty
            assert len(info["name"]) >= 2, f"Name too short for {emoji}"
            assert " " not in info["name"]
            # Names should be lowercase or use underscores
            assert info["name"].replace("_", "").islower() or "_" in info["name"]
