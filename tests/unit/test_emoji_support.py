"""Tests for emoji_support module - PyPI emoji package integration."""

from styledconsole.utils.emoji_support import (
    EMOJI_PACKAGE_AVAILABLE,
    EmojiInfo,
    analyze_emoji_safety,
    demojize,
    emoji_list,
    emojize,
    filter_by_version,
    get_all_emojis,
    get_emoji_info,
    get_emoji_version,
    is_valid_emoji,
    is_zwj_sequence,
)


class TestEmojiPackageAvailability:
    """Test that emoji package is available in dev environment."""

    def test_emoji_package_available(self):
        """emoji package should be available in dev environment."""
        assert EMOJI_PACKAGE_AVAILABLE is True


class TestIsValidEmoji:
    """Tests for is_valid_emoji function."""

    def test_single_emoji_valid(self):
        """Single emojis should be valid."""
        assert is_valid_emoji("🚀") is True
        assert is_valid_emoji("✅") is True
        assert is_valid_emoji("❌") is True

    def test_zwj_sequence_valid(self):
        """ZWJ sequences should be valid emojis."""
        # Family emoji (ZWJ sequence)
        assert is_valid_emoji("👨‍👩‍👧") is True
        # Technologist
        assert is_valid_emoji("👨‍💻") is True

    def test_non_emoji_invalid(self):
        """Non-emoji characters should not be valid."""
        assert is_valid_emoji("A") is False
        assert is_valid_emoji("1") is False
        assert is_valid_emoji(" ") is False
        assert is_valid_emoji("hello") is False


class TestIsZwjSequence:
    """Tests for is_zwj_sequence function."""

    def test_zwj_sequence_detected(self):
        """ZWJ sequences should be detected."""
        assert is_zwj_sequence("👨‍👩‍👧") is True
        assert is_zwj_sequence("👨‍💻") is True
        assert is_zwj_sequence("👩‍🔬") is True

    def test_simple_emoji_not_zwj(self):
        """Simple emojis should not be ZWJ sequences."""
        assert is_zwj_sequence("🚀") is False
        assert is_zwj_sequence("✅") is False

    def test_text_with_zwj(self):
        """Text containing ZWJ sequences should be detected."""
        assert is_zwj_sequence("Hello 👨‍👩‍👧 family") is True

    def test_text_without_zwj(self):
        """Text without ZWJ should return False."""
        assert is_zwj_sequence("Hello 🚀 World") is False
        assert is_zwj_sequence("No emojis here") is False


class TestAnalyzeEmojiSafety:
    """Tests for analyze_emoji_safety function."""

    def test_safe_emojis(self):
        """Safe emojis should be categorized correctly."""
        result = analyze_emoji_safety("Hello 🚀 World")
        assert result["emoji_count"] >= 1
        assert "🚀" in result["safe_emojis"]
        assert result["all_safe"] is True

    def test_zwj_unsafe(self):
        """ZWJ sequences should mark text as unsafe."""
        result = analyze_emoji_safety("Family: 👨‍👩‍👧")
        assert result["all_safe"] is False
        assert len(result["zwj_sequences"]) > 0 or len(result["non_rgi"]) > 0

    def test_empty_text(self):
        """Empty text should have zero counts."""
        result = analyze_emoji_safety("")
        assert result["emoji_count"] == 0
        assert result["all_safe"] is True

    def test_text_only(self):
        """Text without emojis should be safe."""
        result = analyze_emoji_safety("Just plain text")
        assert result["emoji_count"] == 0
        assert result["all_safe"] is True


class TestGetEmojiInfo:
    """Tests for get_emoji_info function."""

    def test_valid_emoji_info(self):
        """Valid emoji should return complete info."""
        info = get_emoji_info("🚀")
        assert isinstance(info, EmojiInfo)
        assert info.emoji == "🚀"
        assert info.is_valid is True
        assert "rocket" in info.name.lower()
        assert info.is_zwj is False

    def test_zwj_emoji_info(self):
        """ZWJ sequence should be marked correctly."""
        info = get_emoji_info("👨‍💻")
        assert info.is_valid is True
        assert info.is_zwj is True
        assert info.terminal_safe is False

    def test_invalid_char_info(self):
        """Non-emoji should return invalid info."""
        info = get_emoji_info("A")
        assert info.is_valid is False
        assert info.terminal_safe is False


class TestGetEmojiVersion:
    """Tests for get_emoji_version function."""

    def test_emoji_version(self):
        """Should return version for known emojis."""
        version = get_emoji_version("🚀")
        assert version is not None
        assert isinstance(version, (int, float))

    def test_non_emoji_version(self):
        """Non-emoji should return None."""
        version = get_emoji_version("A")
        assert version is None


class TestFilterByVersion:
    """Tests for filter_by_version function."""

    def test_filter_keeps_old_emojis(self):
        """Old emojis should be kept."""
        text = "Hello 🚀"  # Rocket is Emoji 0.6
        result = filter_by_version(text, max_version=5.0)
        assert "🚀" in result

    def test_filter_replaces_new_emojis(self):
        """New emojis beyond max_version should be replaced."""
        # Most emojis from version > 12 should be filtered with low version
        text = "Hello 🚀 World"
        result = filter_by_version(text, max_version=0.5, replacement="X")
        # Rocket is 0.6, so it should be replaced
        assert "X" in result or "🚀" not in result


class TestEmojize:
    """Tests for emojize function."""

    def test_emojize_rocket(self):
        """Should convert :rocket: to 🚀."""
        result = emojize(":rocket:")
        assert "🚀" in result

    def test_emojize_preserves_text(self):
        """Should preserve non-shortcode text."""
        result = emojize("Hello :rocket: World")
        assert "Hello" in result
        assert "World" in result
        assert "🚀" in result


class TestDemojize:
    """Tests for demojize function."""

    def test_demojize_rocket(self):
        """Should convert 🚀 to shortcode."""
        result = demojize("🚀")
        assert "rocket" in result.lower()

    def test_demojize_preserves_text(self):
        """Should preserve non-emoji text."""
        result = demojize("Hello 🚀 World")
        assert "Hello" in result
        assert "World" in result


class TestGetAllEmojis:
    """Tests for get_all_emojis function."""

    def test_returns_set(self):
        """Should return a set of emojis."""
        emojis = get_all_emojis()
        assert isinstance(emojis, set)
        assert len(emojis) > 100

    def test_common_emojis_included(self):
        """Common emojis should be in the set."""
        emojis = get_all_emojis()
        assert "🚀" in emojis
        assert "✅" in emojis
        assert "❌" in emojis


class TestEmojiList:
    """Tests for emoji_list function."""

    def test_finds_emojis(self):
        """Should find all emojis with positions."""
        result = emoji_list("Hello 👋 World 🌍")
        assert len(result) == 2
        assert result[0]["emoji"] == "👋"
        assert result[1]["emoji"] == "🌍"

    def test_positions_correct(self):
        """Positions should be correct."""
        result = emoji_list("A🚀B")
        assert len(result) == 1
        assert result[0]["match_start"] == 1

    def test_empty_for_no_emojis(self):
        """Should return empty list for no emojis."""
        result = emoji_list("Hello World")
        assert len(result) == 0


class TestEmojiInfoDataclass:
    """Tests for EmojiInfo dataclass."""

    def test_create_emoji_info(self):
        """Should create EmojiInfo correctly."""
        info = EmojiInfo(
            emoji="🚀",
            name="rocket",
            is_valid=True,
            is_zwj=False,
            version=0.6,
            terminal_safe=True,
        )
        assert info.emoji == "🚀"
        assert info.name == "rocket"
        assert info.is_valid is True
        assert info.is_zwj is False
        assert info.version == 0.6
        assert info.terminal_safe is True

    def test_default_values(self):
        """Default values should be correct."""
        info = EmojiInfo(emoji="X", name="", is_valid=False)
        assert info.is_zwj is False
        assert info.is_zwj_non_rgi is False
        assert info.version is None
        assert info.terminal_safe is True


class TestIntegrationWithExistingCode:
    """Test integration with existing StyledConsole code."""

    def test_safe_emojis_generated_dynamically(self):
        """get_safe_emojis should generate emoji data dynamically from emoji package."""
        from styledconsole.utils.text import get_safe_emojis

        safe_emojis = get_safe_emojis()

        # Should have many emojis from the emoji package
        assert len(safe_emojis) > 100

        # Common emojis should be present
        assert "🚀" in safe_emojis
        assert "✅" in safe_emojis

    def test_validation_uses_emoji_package(self):
        """Emoji validation should use the emoji package."""
        from styledconsole.utils.text import validate_emoji

        # Valid emoji
        result = validate_emoji("🚀")
        assert result["safe"] is True

        # Invalid character
        result = validate_emoji("X")
        assert result["safe"] is False
