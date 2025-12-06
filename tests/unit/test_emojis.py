"""Tests for emoji registry module (DRY architecture).

The emoji registry uses the emoji package as the single source of truth.
All emoji names follow the CLDR standard (canonical names).
"""

from styledconsole.emojis import EMOJI, E, EmojiConstants


class TestEmojiRegistry:
    """Test emoji registry provides emoji access."""

    def test_emoji_singleton_exists(self):
        """Test EMOJI singleton is accessible."""
        assert EMOJI is not None
        # It's an instance, not a type (singleton pattern)
        assert not isinstance(EMOJI, type)

    def test_shorthand_alias(self):
        """Test E is an alias for EMOJI."""
        assert E is EMOJI

    def test_emoji_constants_is_type_alias(self):
        """Test EmojiConstants is the type of EMOJI."""
        assert isinstance(EMOJI, EmojiConstants)

    def test_status_emojis(self):
        """Test status emoji constants."""
        assert EMOJI.CHECK_MARK_BUTTON == "✅"
        assert EMOJI.CROSS_MARK == "❌"
        assert EMOJI.WARNING == "⚠️"
        assert EMOJI.INFORMATION == "ℹ️"

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
        assert EMOJI.LAPTOP == "💻"
        assert EMOJI.ROCKET == "🚀"
        # Gear has variation selector in emoji package
        assert "⚙" in EMOJI.GEAR

    def test_chart_emojis(self):
        """Test chart and document emojis."""
        assert EMOJI.BAR_CHART == "📊"
        assert EMOJI.CHART_INCREASING == "📈"
        assert EMOJI.CHART_DECREASING == "📉"
        assert EMOJI.PACKAGE == "📦"

    def test_nature_emojis(self):
        """Test nature-related emojis."""
        assert EMOJI.RAINBOW == "🌈"
        assert EMOJI.FIRE == "🔥"
        assert EMOJI.HIGH_VOLTAGE == "⚡"
        assert EMOJI.DROPLET == "💧"

    def test_celebration_emojis(self):
        """Test celebration emojis."""
        assert EMOJI.PARTY_POPPER == "🎉"
        assert EMOJI.CONFETTI_BALL == "🎊"
        assert EMOJI.TROPHY == "🏆"

    def test_communication_emojis(self):
        """Test communication-related emojis."""
        assert EMOJI.GLOBE_WITH_MERIDIANS == "🌐"
        assert EMOJI.MOBILE_PHONE == "📱"
        assert EMOJI.E_MAIL == "📧"

    def test_symbols_emojis(self):
        """Test symbol emojis."""
        assert EMOJI.POLICE_CAR_LIGHT == "🚨"
        assert EMOJI.TRIANGULAR_RULER == "📐"
        assert EMOJI.LIGHT_BULB == "💡"
        assert EMOJI.BELL == "🔔"

    def test_file_and_folder_emojis(self):
        """Test file, folder, and storage emojis."""
        # Folders & Storage (may have variation selectors)
        assert EMOJI.FILE_FOLDER == "📁"
        assert EMOJI.OPEN_FILE_FOLDER == "📂"
        assert "🗄" in EMOJI.FILE_CABINET  # Allow variation selector
        assert "🗃" in EMOJI.CARD_FILE_BOX
        assert "🗑" in EMOJI.WASTEBASKET

        # Files & Documents
        assert EMOJI.PAGE_FACING_UP == "📄"
        assert EMOJI.PAGE_WITH_CURL == "📃"
        assert EMOJI.SCROLL == "📜"
        assert EMOJI.MEMO == "📝"
        assert EMOJI.CLIPBOARD == "📋"

        # File organization
        assert EMOJI.PUSHPIN == "📌"
        assert EMOJI.PAPERCLIP == "📎"
        assert EMOJI.BOOKMARK == "🔖"
        assert "🏷" in EMOJI.LABEL
        assert EMOJI.CARD_INDEX == "📇"

    def test_book_emojis(self):
        """Test book and reading-related emojis."""
        assert EMOJI.OPEN_BOOK == "📖"
        assert EMOJI.BOOKS == "📚"
        assert EMOJI.NOTEBOOK == "📓"
        assert EMOJI.LEDGER == "📒"
        assert EMOJI.CLOSED_BOOK == "📕"
        assert EMOJI.GREEN_BOOK == "📗"
        assert EMOJI.BLUE_BOOK == "📘"
        assert EMOJI.ORANGE_BOOK == "📙"

    def test_news_media_emojis(self):
        """Test news and media emojis."""
        assert EMOJI.NEWSPAPER == "📰"
        assert "🗞" in EMOJI.ROLLED_UP_NEWSPAPER

    def test_all_emojis_are_strings(self):
        """Test all emoji constants are strings."""
        for attr_name in dir(EMOJI):
            if attr_name.isupper() and not attr_name.startswith("_"):
                attr_value = getattr(EMOJI, attr_name)
                assert isinstance(attr_value, str), f"{attr_name} should be a string"
                assert len(attr_value) > 0, f"{attr_name} should not be empty"

    def test_emojis_in_frames(self):
        """Test emojis work in frame titles."""
        from styledconsole import Console

        console = Console()
        # Should not raise any errors
        console.frame(
            "Test content",
            title=f"{EMOJI.CHECK_MARK_BUTTON} Success",
            border="solid",
            width=40,
        )

    def test_import_from_main_module(self):
        """Test emojis can be imported from main module."""
        from styledconsole import EMOJI, E

        assert EMOJI.CHECK_MARK_BUTTON == "✅"
        assert E.CROSS_MARK == "❌"


class TestEmojiRegistryMethods:
    """Test emoji registry special methods."""

    def test_search_method(self):
        """Test search method finds emojis by partial name."""
        results = EMOJI.search("check")
        assert len(results) > 0
        # Should find CHECK_MARK_BUTTON
        names = [name for name, _ in results]
        assert "CHECK_MARK_BUTTON" in names

    def test_search_method_limit(self):
        """Test search method respects limit."""
        results = EMOJI.search("circle", limit=3)
        assert len(results) <= 3

    def test_get_method_found(self):
        """Test get method returns emoji when found."""
        result = EMOJI.get("ROCKET")
        assert result == "🚀"

    def test_get_method_not_found(self):
        """Test get method returns default when not found."""
        result = EMOJI.get("NOT_A_REAL_EMOJI", "fallback")
        assert result == "fallback"

    def test_contains_method(self):
        """Test __contains__ method."""
        assert "ROCKET" in EMOJI
        assert "NOT_A_REAL_EMOJI" not in EMOJI

    def test_len_method(self):
        """Test __len__ returns count of emojis."""
        # Should have thousands of emojis from emoji package
        assert len(EMOJI) > 1000

    def test_all_names_method(self):
        """Test all_names returns list of emoji names."""
        names = EMOJI.all_names()
        assert isinstance(names, list)
        assert "ROCKET" in names
        assert "FIRE" in names

    def test_dir_method(self):
        """Test __dir__ returns emoji names for autocomplete."""
        attrs = dir(EMOJI)
        assert "ROCKET" in attrs
        assert "FIRE" in attrs


class TestUnicodeArrows:
    """Test Unicode arrows are supported (not in emoji package)."""

    def test_arrow_directions(self):
        """Test basic arrow directions."""
        assert EMOJI.ARROW_UP == "↑"
        assert EMOJI.ARROW_DOWN == "↓"
        assert EMOJI.ARROW_LEFT == "←"
        assert EMOJI.ARROW_RIGHT == "→"


class TestEmojiUsagePatterns:
    """Test common emoji usage patterns."""

    def test_fstring_interpolation(self):
        """Test emojis work in f-strings."""
        title = f"{EMOJI.ROCKET} Deployment"
        assert "🚀" in title
        assert "Deployment" in title

    def test_concatenation(self):
        """Test emojis work with string concatenation."""
        message = EMOJI.CHECK_MARK_BUTTON + " Build successful"
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
        assert visual_width(EMOJI.CHECK_MARK_BUTTON) == 2
        assert visual_width(EMOJI.ROCKET) == 2
        assert visual_width(EMOJI.FIRE) == 2

    def test_shorthand_usage(self):
        """Test shorthand E alias works identically to EMOJI."""
        assert E.CHECK_MARK_BUTTON == EMOJI.CHECK_MARK_BUTTON
        assert E.ROCKET == EMOJI.ROCKET
        assert f"{E.FIRE} hot" == f"{EMOJI.FIRE} hot"


class TestEmojiPackageIntegration:
    """Test integration with emoji package."""

    def test_emoji_package_available(self):
        """Test emoji package is importable."""
        import emoji

        assert hasattr(emoji, "EMOJI_DATA")
        assert len(emoji.EMOJI_DATA) > 1000

    def test_registry_uses_emoji_package(self):
        """Test registry data comes from emoji package."""
        import emoji

        # ROCKET should match emoji package
        rocket_char = EMOJI.ROCKET
        assert emoji.is_emoji(rocket_char)

    def test_cldr_names(self):
        """Test registry uses CLDR canonical names."""
        # These names come from emoji package (CLDR standard)
        assert EMOJI.CHECK_MARK_BUTTON == "✅"  # Not "CHECK"
        assert EMOJI.CROSS_MARK == "❌"  # Not "CROSS" or "X"
        assert EMOJI.PARTY_POPPER == "🎉"  # Not "PARTY"
