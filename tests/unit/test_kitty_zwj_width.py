"""Tests for Kitty terminal ZWJ emoji width calculation."""

import os
from unittest import mock

import pytest

from styledconsole.utils.text import visual_width


class TestKittyTerminalZwjWidth:
    """Test ZWJ emoji width calculation in Kitty terminal."""

    @pytest.fixture
    def kitty_env(self):
        """Mock Kitty terminal environment."""
        with mock.patch.dict(os.environ, {"KITTY_WINDOW_ID": "1"}):
            # Clear any caches that might affect terminal detection
            from styledconsole.utils.text import _visual_width_cached
            _visual_width_cached.cache_clear()
            yield
            _visual_width_cached.cache_clear()

    @pytest.fixture
    def non_kitty_env(self):
        """Mock non-Kitty terminal environment."""
        env_without_kitty = {k: v for k, v in os.environ.items()
                             if not k.startswith("KITTY")}
        with mock.patch.dict(os.environ, env_without_kitty, clear=True):
            from styledconsole.utils.text import _visual_width_cached
            _visual_width_cached.cache_clear()
            yield
            _visual_width_cached.cache_clear()

    def test_zwj_developer_kitty(self, kitty_env):
        """Test developer emoji (Man + ZWJ + Laptop) in Kitty = 4 cells."""
        emoji = "👨‍💻"
        assert visual_width(emoji) == 4

    def test_zwj_artist_kitty(self, kitty_env):
        """Test artist emoji (Woman + ZWJ + Palette) in Kitty = 4 cells."""
        emoji = "👩‍🎨"
        assert visual_width(emoji) == 4

    def test_zwj_scientist_kitty(self, kitty_env):
        """Test scientist emoji (Person + ZWJ + Microscope) in Kitty = 4 cells."""
        emoji = "🧑‍🔬"
        assert visual_width(emoji) == 4

    def test_zwj_astronaut_kitty(self, kitty_env):
        """Test astronaut emoji (Man + ZWJ + Rocket) in Kitty = 4 cells."""
        emoji = "👨‍🚀"
        assert visual_width(emoji) == 4

    def test_zwj_rainbow_flag_kitty(self, kitty_env):
        """Test rainbow flag (Flag + VS16 + ZWJ + Rainbow) in Kitty = 4 cells."""
        emoji = "🏳️‍🌈"
        assert visual_width(emoji) == 4

    def test_zwj_family_kitty(self, kitty_env):
        """Test family emoji (Man + ZWJ + Woman + ZWJ + Girl) in Kitty = 6 cells."""
        emoji = "👨‍👩‍👧"
        assert visual_width(emoji) == 6

    def test_zwj_developer_non_kitty(self, non_kitty_env):
        """Test developer emoji in non-Kitty terminal = 2 cells."""
        emoji = "👨‍💻"
        # In standard mode (non-modern terminal), ZWJ sequences are width 2
        assert visual_width(emoji) == 2

    def test_zwj_family_non_kitty(self, non_kitty_env):
        """Test family emoji in non-Kitty terminal = 2 cells."""
        emoji = "👨‍👩‍👧"
        assert visual_width(emoji) == 2

    def test_regular_emoji_kitty(self, kitty_env):
        """Test regular (non-ZWJ) emoji still renders as width 2 in Kitty."""
        emoji = "🚀"
        assert visual_width(emoji) == 2

    def test_zwj_in_text_kitty(self, kitty_env):
        """Test ZWJ emoji embedded in text in Kitty."""
        text = "👨‍💻 Developer"
        # ZWJ emoji (4) + space (1) + "Developer" (9) = 14
        assert visual_width(text) == 14

    def test_zwj_in_text_non_kitty(self, non_kitty_env):
        """Test ZWJ emoji embedded in text in non-Kitty terminal."""
        text = "👨‍💻 Developer"
        # ZWJ emoji (2) + space (1) + "Developer" (9) = 12
        assert visual_width(text) == 12

    def test_wide_symbols_kitty(self, kitty_env):
        """Test wide Unicode symbols like trigram in Kitty."""
        # Trigram symbol ☰ (U+2630) should be width 2
        trigram = "☰"
        assert visual_width(trigram) == 2

    def test_wide_symbols_non_kitty(self, non_kitty_env):
        """Test wide Unicode symbols in non-Kitty terminal."""
        trigram = "☰"
        assert visual_width(trigram) == 2

    def test_trigram_in_context_kitty(self, kitty_env):
        """Test trigram symbol in full text context in Kitty."""
        text = "  ☰  Trigram (symbol): ❌ Invalid"
        # 2 spaces (2) + trigram (2) + 2 spaces (2) + text (20) + cross mark (2) + text (6) = 34
        assert visual_width(text) == 34
