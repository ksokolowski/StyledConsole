"""Unit tests for TerminalManager class."""

import logging
import os
from unittest.mock import patch

from styledconsole.core.terminal_manager import TerminalManager
from styledconsole.utils.terminal import TerminalProfile


def make_profile(
    ansi=True, colors=16777216, emoji=True, w=80, h=24, term="xterm-256color", colorterm="truecolor"
):
    """Helper to create TerminalProfile for testing."""
    return TerminalProfile(
        ansi_support=ansi,
        color_depth=colors,
        emoji_safe=emoji,
        width=w,
        height=h,
        term=term,
        colorterm=colorterm,
    )


class TestTerminalManagerBasics:
    """Basic tests for Terminal Manager."""

    def test_init_with_detection_disabled(self):
        """Test initialization with terminal detection disabled."""
        manager = TerminalManager(detect=False, debug=False)
        assert manager.profile is None
        assert manager._debug is False
        assert manager._logger is None

    def test_init_with_debug_enabled(self):
        """Test initialization with debug logging enabled."""
        manager = TerminalManager(detect=False, debug=True)
        assert manager._debug is True
        assert manager._logger is not None
        assert isinstance(manager._logger, logging.Logger)

    def test_color_system_auto_without_profile(self):
        """Test fallback to auto when no profile available."""
        manager = TerminalManager(detect=False)
        assert manager.profile is None
        assert manager.get_color_system() == "auto"

    def test_should_force_terminal_without_profile(self):
        """Test should_force_terminal returns False when no profile."""
        manager = TerminalManager(detect=False)
        assert manager.profile is None
        assert manager.should_force_terminal() is False


class TestTerminalManagerColorSystem:
    """Tests for color system determination."""

    def test_color_system_with_env_override_truecolor(self):
        """Test color system with environment variable override (truecolor)."""
        with patch.dict(os.environ, {"SC_FORCE_COLOR_SYSTEM": "truecolor"}):
            manager = TerminalManager(detect=False)
            assert manager.get_color_system() == "truecolor"

    def test_color_system_with_env_override_256(self):
        """Test color system with environment variable override (256)."""
        with patch.dict(os.environ, {"SC_FORCE_COLOR_SYSTEM": "256"}):
            manager = TerminalManager(detect=False)
            assert manager.get_color_system() == "256"

    def test_color_system_ignores_invalid_env_override(self):
        """Test that invalid environment variable values are ignored."""
        with patch.dict(os.environ, {"SC_FORCE_COLOR_SYSTEM": "invalid"}):
            manager = TerminalManager(detect=False)
            assert manager.get_color_system() == "auto"  # Falls back to auto

    def test_color_system_truecolor_from_profile(self):
        """Test truecolor detection from terminal profile."""
        manager = TerminalManager(detect=False)
        manager.profile = make_profile(colors=16777216)
        assert manager.get_color_system() == "truecolor"

    def test_color_system_256_from_profile(self):
        """Test 256-color detection from terminal profile."""
        manager = TerminalManager(detect=False)
        manager.profile = make_profile(colors=256)
        assert manager.get_color_system() == "256"

    def test_color_system_standard_from_profile(self):
        """Test standard (8-color) detection from terminal profile."""
        manager = TerminalManager(detect=False)
        manager.profile = make_profile(colors=8)
        assert manager.get_color_system() == "standard"

    def test_color_system_env_override_takes_precedence(self):
        """Test that environment override takes precedence over profile."""
        with patch.dict(os.environ, {"SC_FORCE_COLOR_SYSTEM": "standard"}):
            manager = TerminalManager(detect=False)
            manager.profile = make_profile(colors=16777216)  # truecolor profile
            # Should use env override, not profile's truecolor
            assert manager.get_color_system() == "standard"


class TestTerminalManagerForceTerminal:
    """Tests for force_terminal determination."""

    def test_should_force_terminal_with_ansi_support(self):
        """Test should_force_terminal returns True when ANSI supported."""
        manager = TerminalManager(detect=False)
        manager.profile = make_profile(ansi=True)
        assert manager.should_force_terminal() is True

    def test_should_force_terminal_without_ansi_support(self):
        """Test should_force_terminal returns False when ANSI not supported."""
        manager = TerminalManager(detect=False)
        manager.profile = make_profile(ansi=False)
        assert manager.should_force_terminal() is False
