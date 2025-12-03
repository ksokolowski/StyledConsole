"""Tests for the Icon Provider system.

Tests cover:
- Icon class rendering in all modes (emoji, ascii, auto)
- IconProvider attribute access and methods
- Mode switching functions
- Emoji to ASCII conversion
- Terminal capability integration
"""

import pytest

from styledconsole.icons import (
    Icon,
    IconProvider,
    convert_emoji_to_ascii,
    get_icon_mode,
    icons,
    reset_icon_mode,
    set_icon_mode,
)
from styledconsole.utils.icon_data import ICON_REGISTRY


class TestIcon:
    """Tests for the Icon dataclass."""

    def setup_method(self):
        """Reset icon mode before each test."""
        reset_icon_mode()

    def teardown_method(self):
        """Reset icon mode after each test."""
        reset_icon_mode()

    def test_icon_creation(self):
        """Test Icon can be created with all attributes."""
        icon = Icon(name="TEST", emoji="✅", ascii="[OK]", color="green")
        assert icon.name == "TEST"
        assert icon.emoji == "✅"
        assert icon.ascii == "[OK]"
        assert icon.color == "green"

    def test_icon_creation_without_color(self):
        """Test Icon can be created without color."""
        icon = Icon(name="TEST", emoji="→", ascii="->")
        assert icon.name == "TEST"
        assert icon.emoji == "→"
        assert icon.ascii == "->"
        assert icon.color is None

    def test_icon_as_emoji(self):
        """Test as_emoji() always returns emoji."""
        icon = Icon(name="TEST", emoji="✅", ascii="[OK]", color="green")
        assert icon.as_emoji() == "✅"

        # Even in ASCII mode
        set_icon_mode("ascii")
        assert icon.as_emoji() == "✅"

    def test_icon_as_ascii_with_color(self):
        """Test as_ascii() returns colored ASCII when color is set."""
        icon = Icon(name="TEST", emoji="✅", ascii="[OK]", color="green")
        assert icon.as_ascii() == "[green][OK][/]"

    def test_icon_as_ascii_without_color(self):
        """Test as_ascii() returns plain ASCII when no color."""
        icon = Icon(name="TEST", emoji="→", ascii="->")
        assert icon.as_ascii() == "->"

    def test_icon_as_plain_ascii(self):
        """Test as_plain_ascii() returns ASCII without markup."""
        icon = Icon(name="TEST", emoji="✅", ascii="[OK]", color="green")
        assert icon.as_plain_ascii() == "[OK]"

    def test_icon_str_emoji_mode(self):
        """Test __str__ in emoji mode."""
        set_icon_mode("emoji")
        icon = Icon(name="TEST", emoji="✅", ascii="[OK]", color="green")
        assert str(icon) == "✅"

    def test_icon_str_ascii_mode(self):
        """Test __str__ in ascii mode."""
        set_icon_mode("ascii")
        icon = Icon(name="TEST", emoji="✅", ascii="[OK]", color="green")
        assert str(icon) == "[green][OK][/]"

    def test_icon_immutable(self):
        """Test Icon is immutable (frozen dataclass)."""
        icon = Icon(name="TEST", emoji="✅", ascii="[OK]", color="green")
        with pytest.raises(AttributeError):
            icon.name = "CHANGED"


class TestIconProvider:
    """Tests for the IconProvider class."""

    def setup_method(self):
        """Reset icon mode before each test."""
        reset_icon_mode()

    def teardown_method(self):
        """Reset icon mode after each test."""
        reset_icon_mode()

    def test_icons_singleton_exists(self):
        """Test module-level icons instance exists."""
        assert icons is not None
        assert isinstance(icons, IconProvider)

    def test_provider_has_all_registry_icons(self):
        """Test provider contains all icons from registry."""
        assert len(icons) == len(ICON_REGISTRY)

    def test_provider_attribute_access(self):
        """Test icons can be accessed as attributes."""
        icon = icons.CHECK
        assert isinstance(icon, Icon)
        assert icon.emoji == "✅"

    def test_provider_attribute_access_various_icons(self):
        """Test various icons can be accessed."""
        assert icons.CROSS.emoji == "❌"
        assert icons.WARNING.emoji == "⚠️"
        assert icons.ROCKET.emoji == "🚀"
        assert icons.STAR.emoji == "⭐"

    def test_provider_attribute_not_found(self):
        """Test accessing non-existent icon raises AttributeError."""
        with pytest.raises(AttributeError, match="Icon 'NONEXISTENT' not found"):
            _ = icons.NONEXISTENT

    def test_provider_private_attribute_raises(self):
        """Test accessing private attributes raises AttributeError."""
        with pytest.raises(AttributeError):
            _ = icons._private

    def test_provider_get_method(self):
        """Test get() method returns icon or None."""
        icon = icons.get("CHECK")
        assert icon is not None
        assert icon.emoji == "✅"

        assert icons.get("NONEXISTENT") is None

    def test_provider_get_by_emoji(self):
        """Test get_by_emoji() looks up icon by emoji character."""
        icon = icons.get_by_emoji("✅")
        assert icon is not None
        assert icon.name == "CHECK"

        assert icons.get_by_emoji("🤷") is None  # Unknown emoji

    def test_provider_list_icons(self):
        """Test list_icons() returns sorted list of names."""
        names = icons.list_icons()
        assert isinstance(names, list)
        assert "CHECK" in names
        assert "CROSS" in names
        assert names == sorted(names)  # Sorted

    def test_provider_list_by_category(self):
        """Test list_by_category() returns organized dictionary."""
        categories = icons.list_by_category()
        assert isinstance(categories, dict)
        assert "status" in categories
        assert "CHECK" in categories["status"]
        assert "transport" in categories
        assert "ROCKET" in categories["transport"]

    def test_provider_len(self):
        """Test len() returns icon count."""
        assert len(icons) > 100  # We have 100+ icons

    def test_provider_iter(self):
        """Test iteration over icon names."""
        names = list(icons)
        assert "CHECK" in names
        assert len(names) == len(icons)

    def test_provider_contains(self):
        """Test 'in' operator for icon names."""
        assert "CHECK" in icons
        assert "CROSS" in icons
        assert "NONEXISTENT" not in icons


class TestIconModeControl:
    """Tests for mode control functions."""

    def setup_method(self):
        """Reset icon mode before each test."""
        reset_icon_mode()

    def teardown_method(self):
        """Reset icon mode after each test."""
        reset_icon_mode()

    def test_default_mode_is_auto(self):
        """Test default mode is 'auto'."""
        assert get_icon_mode() == "auto"

    def test_set_mode_emoji(self):
        """Test setting mode to emoji."""
        set_icon_mode("emoji")
        assert get_icon_mode() == "emoji"

    def test_set_mode_ascii(self):
        """Test setting mode to ascii."""
        set_icon_mode("ascii")
        assert get_icon_mode() == "ascii"

    def test_set_mode_auto(self):
        """Test setting mode to auto."""
        set_icon_mode("ascii")
        set_icon_mode("auto")
        assert get_icon_mode() == "auto"

    def test_set_mode_invalid(self):
        """Test setting invalid mode raises ValueError."""
        with pytest.raises(ValueError, match="Invalid mode"):
            set_icon_mode("invalid")

    def test_reset_mode(self):
        """Test reset_icon_mode() restores auto mode."""
        set_icon_mode("ascii")
        reset_icon_mode()
        assert get_icon_mode() == "auto"

    def test_mode_affects_icon_str(self):
        """Test mode changes affect icon string output."""
        icon = icons.CHECK

        set_icon_mode("emoji")
        assert str(icon) == "✅"

        set_icon_mode("ascii")
        assert str(icon) == "[green][OK][/]"


class TestEmojiConversion:
    """Tests for emoji to ASCII conversion function."""

    def test_convert_single_emoji(self):
        """Test converting single emoji."""
        result = convert_emoji_to_ascii("✅")
        assert result == "[green][OK][/]"

    def test_convert_emoji_in_text(self):
        """Test converting emoji within text."""
        result = convert_emoji_to_ascii("Status: ✅ Done")
        assert result == "Status: [green][OK][/] Done"

    def test_convert_multiple_emojis(self):
        """Test converting multiple emojis."""
        result = convert_emoji_to_ascii("✅ Pass ❌ Fail")
        assert "[green][OK][/]" in result
        assert "[red][FAIL][/]" in result

    def test_convert_emoji_without_color(self):
        """Test converting emoji that has no color."""
        result = convert_emoji_to_ascii("→")
        assert result == "->"

    def test_convert_no_emoji(self):
        """Test text without emoji is unchanged."""
        text = "No emojis here"
        assert convert_emoji_to_ascii(text) == text

    def test_convert_unknown_emoji(self):
        """Test unknown emoji is left unchanged."""
        result = convert_emoji_to_ascii("Unknown: 🤷")
        assert "🤷" in result  # Not converted


class TestIconDataIntegrity:
    """Tests for icon data consistency."""

    def test_all_status_icons_have_colors(self):
        """Test status icons have semantic colors."""
        assert icons.CHECK.color == "green"
        assert icons.CROSS.color == "red"
        assert icons.WARNING.color == "yellow"
        assert icons.INFO.color == "cyan"

    def test_colored_circles_match_color(self):
        """Test colored circle icons have matching colors."""
        assert icons.RED_CIRCLE.color == "red"
        assert icons.GREEN_CIRCLE.color == "green"
        assert icons.YELLOW_CIRCLE.color == "yellow"
        assert icons.BLUE_CIRCLE.color == "blue"

    def test_arrows_have_no_color(self):
        """Test arrow icons have no color (use terminal default)."""
        assert icons.ARROW_RIGHT.color is None
        assert icons.ARROW_LEFT.color is None
        assert icons.ARROW_UP.color is None
        assert icons.ARROW_DOWN.color is None

    def test_ascii_representations_readable(self):
        """Test ASCII representations are recognizable."""
        # Status should be bracketed text
        assert icons.CHECK.ascii == "[OK]"
        assert icons.CROSS.ascii == "[FAIL]"
        assert icons.WARNING.ascii == "[WARN]"

        # Arrows should be simple
        assert icons.ARROW_RIGHT.ascii == "->"
        assert icons.ARROW_LEFT.ascii == "<-"

    def test_no_empty_ascii(self):
        """Test no icon has empty ASCII representation."""
        for name in icons:
            icon = icons.get(name)
            assert icon.ascii, f"Icon {name} has empty ASCII"
            assert len(icon.ascii) > 0, f"Icon {name} has zero-length ASCII"


class TestIconProviderIntegration:
    """Integration tests for icon provider with other components."""

    def setup_method(self):
        """Reset icon mode before each test."""
        reset_icon_mode()

    def teardown_method(self):
        """Reset icon mode after each test."""
        reset_icon_mode()

    def test_icon_in_fstring(self):
        """Test icons work in f-strings."""
        set_icon_mode("emoji")
        result = f"{icons.CHECK} Tests passed"
        assert result == "✅ Tests passed"

        set_icon_mode("ascii")
        result = f"{icons.CHECK} Tests passed"
        assert result == "[green][OK][/] Tests passed"

    def test_icon_concatenation(self):
        """Test icons can be concatenated."""
        set_icon_mode("emoji")
        result = str(icons.CHECK) + " " + str(icons.CROSS)
        assert result == "✅ ❌"

    def test_multiple_icons_in_string(self):
        """Test multiple icons in formatted string."""
        set_icon_mode("ascii")
        result = f"Pass: {icons.CHECK} | Fail: {icons.CROSS} | Warn: {icons.WARNING}"
        assert "[green][OK][/]" in result
        assert "[red][FAIL][/]" in result
        assert "[yellow][WARN][/]" in result
