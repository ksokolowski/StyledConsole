"""Unit tests for terminal capability detection."""

from unittest.mock import MagicMock, patch

from styledconsole.utils.terminal import (
    MODERN_TERMINALS,
    TerminalProfile,
    _detect_color_depth,
    _detect_emoji_safety,
    _get_terminal_size,
    detect_terminal_capabilities,
    is_modern_terminal,
)


class TestTerminalProfile:
    """Test TerminalProfile dataclass."""

    def test_create_profile(self):
        """Test creating a TerminalProfile."""
        profile = TerminalProfile(
            ansi_support=True,
            color_depth=256,
            emoji_safe=True,
            width=120,
            height=40,
            term="xterm-256color",
            colorterm="truecolor",
        )

        assert profile.ansi_support is True
        assert profile.color_depth == 256
        assert profile.emoji_safe is True
        assert profile.width == 120
        assert profile.height == 40
        assert profile.term == "xterm-256color"
        assert profile.colorterm == "truecolor"
        # Default values for new fields
        assert profile.terminal_name is None
        assert profile.modern_emoji is False

    def test_profile_with_modern_terminal(self):
        """Test profile with modern terminal fields."""
        profile = TerminalProfile(
            ansi_support=True,
            color_depth=16777216,
            emoji_safe=True,
            width=120,
            height=40,
            term="xterm-kitty",
            colorterm="truecolor",
            terminal_name="kitty",
            modern_emoji=True,
        )

        assert profile.terminal_name == "kitty"
        assert profile.modern_emoji is True

    def test_profile_with_none_values(self):
        """Test profile with None values for env vars."""
        profile = TerminalProfile(
            ansi_support=False,
            color_depth=0,
            emoji_safe=False,
            width=80,
            height=24,
            term=None,
            colorterm=None,
        )

        assert profile.term is None
        assert profile.colorterm is None
        assert profile.terminal_name is None
        assert profile.modern_emoji is False


class TestDetectColorDepth:
    """Test color depth detection logic."""

    def test_truecolor_via_colorterm(self):
        """Test truecolor detection via COLORTERM=truecolor."""
        depth = _detect_color_depth("xterm", "truecolor", ansi_support=True)
        assert depth == 16777216

    def test_truecolor_via_24bit(self):
        """Test truecolor detection via COLORTERM=24bit."""
        depth = _detect_color_depth("xterm", "24bit", ansi_support=True)
        assert depth == 16777216

    def test_256_color_via_term(self):
        """Test 256 color detection via TERM=xterm-256color."""
        depth = _detect_color_depth("xterm-256color", "", ansi_support=True)
        assert depth == 256

    def test_256_color_via_term_variant(self):
        """Test 256 color detection with various TERM values."""
        assert _detect_color_depth("screen-256color", "", True) == 256
        assert _detect_color_depth("tmux-256", "", True) == 256

    def test_basic_color_xterm(self):
        """Test basic color detection for xterm."""
        depth = _detect_color_depth("xterm", "", ansi_support=True)
        assert depth == 8

    def test_basic_color_screen(self):
        """Test basic color detection for screen/tmux."""
        assert _detect_color_depth("screen", "", True) == 8
        assert _detect_color_depth("tmux", "", True) == 8

    def test_basic_color_linux(self):
        """Test basic color detection for linux console."""
        depth = _detect_color_depth("linux", "", ansi_support=True)
        assert depth == 8

    def test_no_ansi_support(self):
        """Test color depth when ANSI is not supported."""
        depth = _detect_color_depth("xterm-256color", "truecolor", ansi_support=False)
        assert depth == 0

    def test_dumb_terminal(self):
        """Test dumb terminal has no color."""
        depth = _detect_color_depth("dumb", "", ansi_support=False)
        assert depth == 0

    def test_unknown_term(self):
        """Test unknown TERM defaults to basic colors if ANSI supported."""
        depth = _detect_color_depth("unknown", "", ansi_support=True)
        assert depth == 8


class TestDetectEmojiSafety:
    """Test emoji safety detection logic."""

    def test_emoji_safe_with_utf8_lang(self, monkeypatch):
        """Test emoji safe when LANG has UTF-8."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is True

    def test_emoji_safe_with_utf8_lc_all(self, monkeypatch):
        """Test emoji safe when LC_ALL has UTF-8."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        monkeypatch.setenv("LC_ALL", "en_GB.UTF-8")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is True

    def test_emoji_safe_with_utf8_lc_ctype(self, monkeypatch):
        """Test emoji safe when LC_CTYPE has UTF-8."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        monkeypatch.delenv("LANG", raising=False)
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.setenv("LC_CTYPE", "C.UTF-8")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is True

    def test_emoji_unsafe_no_tty(self, monkeypatch):
        """Test emoji unsafe when not a TTY."""
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        safe = _detect_emoji_safety(is_tty=False, color_depth=256)
        assert safe is False

    def test_emoji_unsafe_no_color(self, monkeypatch):
        """Test emoji unsafe when no color support."""
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        safe = _detect_emoji_safety(is_tty=True, color_depth=0)
        assert safe is False

    def test_emoji_unsafe_in_ci_github(self, monkeypatch):
        """Test emoji unsafe in GitHub Actions."""
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is False

    def test_emoji_unsafe_in_ci_jenkins(self, monkeypatch):
        """Test emoji unsafe in Jenkins."""
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        monkeypatch.setenv("JENKINS_URL", "http://jenkins")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is False

    def test_emoji_unsafe_in_ci_gitlab(self, monkeypatch):
        """Test emoji unsafe in GitLab CI."""
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        monkeypatch.setenv("GITLAB_CI", "true")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is False

    def test_emoji_unsafe_no_utf8(self, monkeypatch):
        """Test emoji unsafe when no UTF-8 locale."""
        monkeypatch.setenv("LANG", "C")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is False


class TestGetTerminalSize:
    """Test terminal size detection."""

    def test_get_size_success(self):
        """Test getting terminal size successfully."""
        with patch("os.get_terminal_size") as mock_size:
            mock_size.return_value = MagicMock(columns=120, lines=40)
            width, height = _get_terminal_size()
            assert width == 120
            assert height == 40

    def test_get_size_fallback_on_error(self):
        """Test fallback size when get_terminal_size fails."""
        with patch("os.get_terminal_size", side_effect=OSError):
            width, height = _get_terminal_size()
            assert width == 80
            assert height == 24

    def test_get_size_fallback_on_value_error(self):
        """Test fallback size on ValueError."""
        with patch("os.get_terminal_size", side_effect=ValueError):
            width, height = _get_terminal_size()
            assert width == 80
            assert height == 24


class TestDetectTerminalCapabilities:
    """Test full terminal capability detection."""

    def test_detect_truecolor_terminal(self, monkeypatch):
        """Test detection of truecolor terminal."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.setenv("COLORTERM", "truecolor")
        monkeypatch.setenv("LANG", "en_US.UTF-8")

        with (
            patch("sys.stdout.isatty", return_value=True),
            patch("os.get_terminal_size") as mock_size,
        ):
            mock_size.return_value = MagicMock(columns=120, lines=40)

            profile = detect_terminal_capabilities()

            assert profile.ansi_support is True
            assert profile.color_depth == 16777216
            assert profile.emoji_safe is True
            assert profile.width == 120
            assert profile.height == 40
            assert profile.term == "xterm-256color"
            assert profile.colorterm == "truecolor"

    def test_detect_256_color_terminal(self, monkeypatch):
        """Test detection of 256 color terminal."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.delenv("COLORTERM", raising=False)
        monkeypatch.setenv("LANG", "en_US.UTF-8")

        with (
            patch("sys.stdout.isatty", return_value=True),
            patch("os.get_terminal_size") as mock_size,
        ):
            mock_size.return_value = MagicMock(columns=100, lines=30)

            profile = detect_terminal_capabilities()

            assert profile.ansi_support is True
            assert profile.color_depth == 256
            assert profile.emoji_safe is True
            assert profile.term == "xterm-256color"
            assert profile.colorterm is None

    def test_detect_basic_terminal(self, monkeypatch):
        """Test detection of basic ANSI terminal."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        monkeypatch.setenv("TERM", "xterm")
        monkeypatch.delenv("COLORTERM", raising=False)
        monkeypatch.setenv("LANG", "en_US.UTF-8")

        with (
            patch("sys.stdout.isatty", return_value=True),
            patch("os.get_terminal_size") as mock_size,
        ):
            mock_size.return_value = MagicMock(columns=80, lines=24)

            profile = detect_terminal_capabilities()

            assert profile.ansi_support is True
            assert profile.color_depth == 8
            assert profile.emoji_safe is True

    def test_detect_dumb_terminal(self, monkeypatch):
        """Test detection of dumb terminal."""
        monkeypatch.setenv("TERM", "dumb")
        # Clear modern terminal indicators
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        monkeypatch.delenv("WEZTERM_PANE", raising=False)
        monkeypatch.delenv("ITERM_SESSION_ID", raising=False)
        monkeypatch.delenv("WT_SESSION", raising=False)
        monkeypatch.delenv("VSCODE_PID", raising=False)

        with (
            patch("sys.stdout.isatty", return_value=True),
            patch("os.get_terminal_size") as mock_size,
        ):
            mock_size.return_value = MagicMock(columns=80, lines=24)

            profile = detect_terminal_capabilities()

            assert profile.ansi_support is False
            assert profile.color_depth == 0
            assert profile.emoji_safe is False
            assert profile.term == "dumb"
            assert profile.modern_emoji is False

    def test_detect_no_tty(self, monkeypatch):
        """Test detection when output is not a TTY (pipe/redirect)."""
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.setenv("COLORTERM", "truecolor")
        # Clear modern terminal indicators
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        monkeypatch.delenv("WEZTERM_PANE", raising=False)
        monkeypatch.delenv("ITERM_SESSION_ID", raising=False)
        monkeypatch.delenv("WT_SESSION", raising=False)
        monkeypatch.delenv("VSCODE_PID", raising=False)

        with (
            patch("sys.stdout.isatty", return_value=False),
            patch("os.get_terminal_size") as mock_size,
        ):
            mock_size.return_value = MagicMock(columns=80, lines=24)

            profile = detect_terminal_capabilities()

            assert profile.ansi_support is False
            assert profile.color_depth == 0
            assert profile.emoji_safe is False
            assert profile.modern_emoji is False

    def test_detect_with_no_color(self, monkeypatch):
        """Test detection when NO_COLOR is set."""
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.setenv("NO_COLOR", "1")

        with patch("sys.stdout.isatty", return_value=True):
            profile = detect_terminal_capabilities()

            assert profile.ansi_support is False
            assert profile.color_depth == 0

    def test_detect_with_ansi_colors_disabled(self, monkeypatch):
        """Test detection when ANSI_COLORS_DISABLED is set."""
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.setenv("ANSI_COLORS_DISABLED", "1")

        with patch("sys.stdout.isatty", return_value=True):
            profile = detect_terminal_capabilities()

            assert profile.ansi_support is False
            assert profile.color_depth == 0

    def test_detect_empty_term(self, monkeypatch):
        """Test detection when TERM is empty."""
        monkeypatch.delenv("TERM", raising=False)

        with patch("sys.stdout.isatty", return_value=True):
            profile = detect_terminal_capabilities()

            assert profile.ansi_support is False
            assert profile.term is None

    def test_detect_in_ci_environment(self, monkeypatch):
        """Test detection in CI environment."""
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.setenv("COLORTERM", "truecolor")
        monkeypatch.setenv("LANG", "en_US.UTF-8")
        monkeypatch.setenv("CI", "true")
        # Clear modern terminal indicators
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        monkeypatch.delenv("WEZTERM_PANE", raising=False)
        monkeypatch.delenv("ITERM_SESSION_ID", raising=False)
        monkeypatch.delenv("WT_SESSION", raising=False)
        monkeypatch.delenv("VSCODE_PID", raising=False)

        with patch("sys.stdout.isatty", return_value=True):
            profile = detect_terminal_capabilities()

            assert profile.ansi_support is True
            assert profile.color_depth == 16777216
            # Emoji should be unsafe in CI even with UTF-8 (no modern terminal)
            assert profile.emoji_safe is False
            assert profile.modern_emoji is False


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_case_insensitive_utf8(self, monkeypatch):
        """Test UTF-8 detection is case-insensitive."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        monkeypatch.setenv("LANG", "en_US.utf-8")  # lowercase
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is True

    def test_multiple_locale_vars_priority(self, monkeypatch):
        """Test that any UTF-8 locale var enables emoji."""
        # Clear CI environment variables that disable emoji
        monkeypatch.delenv("CI", raising=False)
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITLAB_CI", raising=False)
        monkeypatch.delenv("JENKINS_URL", raising=False)
        # LANG without UTF-8, but LC_ALL with UTF-8
        monkeypatch.setenv("LANG", "C")
        monkeypatch.setenv("LC_ALL", "en_US.UTF-8")
        safe = _detect_emoji_safety(is_tty=True, color_depth=256)
        assert safe is True

    def test_terminal_size_with_small_dimensions(self):
        """Test handling of small terminal dimensions."""
        with patch("os.get_terminal_size") as mock_size:
            mock_size.return_value = MagicMock(columns=20, lines=5)
            width, height = _get_terminal_size()
            assert width == 20
            assert height == 5

    def test_terminal_size_with_large_dimensions(self):
        """Test handling of large terminal dimensions."""
        with patch("os.get_terminal_size") as mock_size:
            mock_size.return_value = MagicMock(columns=300, lines=100)
            width, height = _get_terminal_size()
            assert width == 300
            assert height == 100


class TestModernTerminalDetection:
    """Test modern terminal detection (v0.9.6+)."""

    def test_modern_terminals_constant(self):
        """Test MODERN_TERMINALS constant is defined."""
        assert isinstance(MODERN_TERMINALS, dict)
        assert "kitty" in MODERN_TERMINALS
        assert "wezterm" in MODERN_TERMINALS
        assert "iterm" in MODERN_TERMINALS
        assert "ghostty" in MODERN_TERMINALS
        assert "alacritty" in MODERN_TERMINALS

    def test_detect_kitty_via_env(self, monkeypatch):
        """Test Kitty detection via KITTY_WINDOW_ID."""
        monkeypatch.setenv("KITTY_WINDOW_ID", "1")
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        assert is_modern_terminal() is True

    def test_detect_kitty_via_term(self, monkeypatch):
        """Test Kitty detection via TERM=xterm-kitty."""
        monkeypatch.setenv("TERM", "xterm-kitty")
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        assert is_modern_terminal() is True

    def test_detect_kitty_via_term_program(self, monkeypatch):
        """Test Kitty detection via TERM_PROGRAM=kitty."""
        monkeypatch.setenv("TERM_PROGRAM", "kitty")
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        assert is_modern_terminal() is True

    def test_detect_wezterm_via_env(self, monkeypatch):
        """Test WezTerm detection via WEZTERM_PANE."""
        monkeypatch.setenv("WEZTERM_PANE", "0")
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        assert is_modern_terminal() is True

    def test_detect_wezterm_via_term_program(self, monkeypatch):
        """Test WezTerm detection via TERM_PROGRAM."""
        monkeypatch.setenv("TERM_PROGRAM", "WezTerm")
        monkeypatch.setenv("TERM", "wezterm")
        assert is_modern_terminal() is True

    def test_detect_iterm_via_env(self, monkeypatch):
        """Test iTerm2 detection via ITERM_SESSION_ID."""
        monkeypatch.setenv("ITERM_SESSION_ID", "session123")
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        assert is_modern_terminal() is True

    def test_detect_iterm_via_term_program(self, monkeypatch):
        """Test iTerm2 detection via TERM_PROGRAM."""
        monkeypatch.setenv("TERM_PROGRAM", "iTerm.app")
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.delenv("ITERM_SESSION_ID", raising=False)
        assert is_modern_terminal() is True

    def test_detect_ghostty(self, monkeypatch):
        """Test Ghostty detection via TERM_PROGRAM."""
        monkeypatch.setenv("TERM_PROGRAM", "ghostty")
        monkeypatch.setenv("TERM", "xterm-256color")
        assert is_modern_terminal() is True

    def test_detect_alacritty(self, monkeypatch):
        """Test Alacritty detection via TERM_PROGRAM."""
        monkeypatch.setenv("TERM_PROGRAM", "Alacritty")
        monkeypatch.setenv("TERM", "alacritty")
        assert is_modern_terminal() is True

    def test_vscode_not_modern(self, monkeypatch):
        """Test VS Code terminal is NOT detected as modern.

        VS Code's integrated terminal doesn't properly render ZWJ sequences
        at the expected width, so it's excluded from modern terminal detection.
        """
        monkeypatch.setenv("TERM_PROGRAM", "vscode")
        monkeypatch.setenv("TERM", "xterm-256color")
        assert is_modern_terminal() is False

    def test_detect_windows_terminal(self, monkeypatch):
        """Test Windows Terminal detection via WT_SESSION."""
        monkeypatch.setenv("WT_SESSION", "abc123")
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        assert is_modern_terminal() is True

    def test_no_modern_terminal(self, monkeypatch):
        """Test basic xterm is not detected as modern."""
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.delenv("TERM_PROGRAM", raising=False)
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        monkeypatch.delenv("WEZTERM_PANE", raising=False)
        monkeypatch.delenv("WEZTERM_EXECUTABLE", raising=False)
        monkeypatch.delenv("ITERM_SESSION_ID", raising=False)
        monkeypatch.delenv("WT_SESSION", raising=False)
        monkeypatch.delenv("VSCODE_PID", raising=False)
        assert is_modern_terminal() is False

    def test_detect_capabilities_includes_modern_fields(self, monkeypatch):
        """Test detect_terminal_capabilities includes modern terminal fields."""
        monkeypatch.setenv("KITTY_WINDOW_ID", "1")
        monkeypatch.setenv("TERM", "xterm-kitty")
        monkeypatch.setenv("COLORTERM", "truecolor")
        monkeypatch.setenv("LANG", "en_US.UTF-8")

        with (
            patch("sys.stdout.isatty", return_value=True),
            patch("os.get_terminal_size") as mock_size,
        ):
            mock_size.return_value = MagicMock(columns=120, lines=40)
            profile = detect_terminal_capabilities()

            assert profile.terminal_name == "kitty"
            assert profile.modern_emoji is True
            assert profile.emoji_safe is True  # Modern terminals are always emoji-safe

    def test_modern_terminal_forces_emoji_safe(self, monkeypatch):
        """Test that modern terminal detection forces emoji_safe=True."""
        monkeypatch.setenv("KITTY_WINDOW_ID", "1")
        monkeypatch.setenv("TERM", "xterm-kitty")
        monkeypatch.setenv("COLORTERM", "truecolor")
        # Even without UTF-8 locale, modern terminal should be emoji-safe
        monkeypatch.delenv("LANG", raising=False)
        monkeypatch.delenv("LC_ALL", raising=False)
        monkeypatch.delenv("LC_CTYPE", raising=False)

        with (
            patch("sys.stdout.isatty", return_value=True),
            patch("os.get_terminal_size") as mock_size,
        ):
            mock_size.return_value = MagicMock(columns=80, lines=24)
            profile = detect_terminal_capabilities()

            assert profile.modern_emoji is True
            assert profile.emoji_safe is True  # Forced by modern terminal
