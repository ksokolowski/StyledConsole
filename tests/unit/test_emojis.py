"""Tests for emoji constants module."""

from styledconsole.emojis import EMOJI, E, EmojiConstants


class TestEmojiConstants:
    """Test emoji constants are properly defined."""

    def test_emoji_class_exists(self):
        """Test EMOJI class is accessible."""
        assert EMOJI is not None
        assert isinstance(EMOJI, type)

    def test_shorthand_alias(self):
        """Test E is an alias for EMOJI."""
        assert E is EMOJI
        assert E is EmojiConstants

    def test_status_emojis(self):
        """Test status emoji constants."""
        assert EMOJI.CHECK == "✅"
        assert EMOJI.CROSS == "❌"
        assert EMOJI.WARNING == "⚠️"
        assert EMOJI.INFO == "ℹ️"

    def test_colored_circles(self):
        """Test colored circle emojis."""
        assert EMOJI.RED_CIRCLE == "🔴"
        assert EMOJI.YELLOW_CIRCLE == "🟡"
        assert EMOJI.GREEN_CIRCLE == "🟢"
        assert EMOJI.BLUE_CIRCLE == "🔵"

    def test_star_emojis(self):
        """Test star and sparkle emojis."""
        assert EMOJI.STAR == "⭐"
        assert EMOJI.SPARKLES == "✨"
        assert EMOJI.DIZZY == "💫"
        assert EMOJI.GLOWING_STAR == "🌟"

    def test_technology_emojis(self):
        """Test technology-related emojis."""
        assert EMOJI.COMPUTER == "💻"
        assert EMOJI.LAPTOP == "💻"  # Alias
        assert EMOJI.ROCKET == "🚀"
        assert EMOJI.GEAR == "⚙️"

    def test_chart_emojis(self):
        """Test chart and document emojis."""
        assert EMOJI.CHART_BAR == "📊"
        assert EMOJI.CHART_INCREASING == "📈"
        assert EMOJI.CHART_DECREASING == "📉"
        assert EMOJI.PACKAGE == "📦"

    def test_nature_emojis(self):
        """Test nature-related emojis."""
        assert EMOJI.RAINBOW == "🌈"
        assert EMOJI.FIRE == "🔥"
        assert EMOJI.LIGHTNING == "⚡"
        assert EMOJI.DROPLET == "💧"

    def test_celebration_emojis(self):
        """Test celebration emojis."""
        assert EMOJI.PARTY == "🎉"
        assert EMOJI.CONFETTI == "🎊"
        assert EMOJI.TROPHY == "🏆"

    def test_helper_methods(self):
        """Test helper methods for common patterns."""
        assert EMOJI.success("Done") == "✅ Done"
        assert EMOJI.error("Failed") == "❌ Failed"
        assert EMOJI.warning("Careful") == "⚠️ Careful"
        assert EMOJI.info("Note") == "ℹ️ Note"

    def test_helper_methods_no_text(self):
        """Test helper methods without text."""
        assert EMOJI.success() == "✅"
        assert EMOJI.error() == "❌"
        assert EMOJI.warning() == "⚠️"
        assert EMOJI.info() == "ℹ️"

    def test_emoji_aliases(self):
        """Test that aliases point to same emoji."""
        assert EMOJI.LAPTOP == EMOJI.COMPUTER
        assert EMOJI.PALETTE == EMOJI.ART
        assert EMOJI.DIAMOND == EMOJI.GEM

    def test_all_emojis_are_strings(self):
        """Test all emoji constants are strings."""
        for attr_name in dir(EMOJI):
            if attr_name.isupper():
                attr_value = getattr(EMOJI, attr_name)
                assert isinstance(attr_value, str), f"{attr_name} should be a string"
                assert len(attr_value) > 0, f"{attr_name} should not be empty"

    def test_no_zwj_sequences(self):
        """Test that no ZWJ sequences are included (unsupported)."""
        # ZWJ is U+200D
        zwj = "\u200d"
        for attr_name in dir(EMOJI):
            if attr_name.isupper():
                attr_value = getattr(EMOJI, attr_name)
                if isinstance(attr_value, str):
                    assert zwj not in attr_value, f"{attr_name} contains ZWJ sequence (unsupported)"

    def test_emojis_in_frames(self):
        """Test emojis work in frame titles."""
        from styledconsole import Console

        console = Console()
        # Should not raise any errors
        console.frame("Test content", title=f"{EMOJI.CHECK} Success", border="solid", width=40)

    def test_import_from_main_module(self):
        """Test emojis can be imported from main module."""
        from styledconsole import EMOJI, E

        assert EMOJI.CHECK == "✅"
        assert E.CROSS == "❌"


class TestEmojiUsagePatterns:
    """Test common emoji usage patterns."""

    def test_fstring_interpolation(self):
        """Test emojis work in f-strings."""
        title = f"{EMOJI.ROCKET} Deployment"
        assert "🚀" in title
        assert "Deployment" in title

    def test_concatenation(self):
        """Test emojis work with string concatenation."""
        message = EMOJI.CHECK + " Build successful"
        assert "✅" in message
        assert "Build successful" in message

    def test_multiple_emojis(self):
        """Test multiple emojis in one string."""
        status = f"{EMOJI.FIRE} {EMOJI.ROCKET} {EMOJI.SPARKLES}"
        assert "🔥" in status
        assert "🚀" in status
        assert "✨" in status

    def test_emoji_visual_width(self):
        """Test emojis have correct visual width."""
        from styledconsole.utils.text import visual_width

        # Most emojis should be 2 columns wide
        assert visual_width(EMOJI.CHECK) == 2
        assert visual_width(EMOJI.ROCKET) == 2
        assert visual_width(EMOJI.FIRE) == 2

    def test_shorthand_usage(self):
        """Test shorthand E alias works as expected."""
        assert f"{E.CHECK} Done" == f"{EMOJI.CHECK} Done"
        assert E.success("Test") == EMOJI.success("Test")
