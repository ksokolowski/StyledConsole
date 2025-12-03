"""Tests for animation module."""

from __future__ import annotations

import io
import sys
from unittest.mock import patch

from styledconsole.animation import Animation, _supports_cursor_control
from styledconsole.policy import RenderPolicy


class TestSupportsCursorControl:
    """Tests for _supports_cursor_control function."""

    def test_returns_false_when_not_tty(self) -> None:
        """Non-TTY should not support cursor control."""
        with patch.object(sys.stdout, "isatty", return_value=False):
            assert _supports_cursor_control() is False

    def test_returns_false_for_dumb_terminal(self) -> None:
        """TERM=dumb should not support cursor control."""
        with (
            patch.object(sys.stdout, "isatty", return_value=True),
            patch.dict("os.environ", {"TERM": "dumb"}),
        ):
            assert _supports_cursor_control() is False

    def test_returns_true_for_normal_terminal(self) -> None:
        """Normal terminal with TTY should support cursor control."""
        with (
            patch.object(sys.stdout, "isatty", return_value=True),
            patch.dict("os.environ", {"TERM": "xterm-256color"}),
        ):
            assert _supports_cursor_control() is True

    def test_respects_policy_unicode_true(self) -> None:
        """Policy with unicode=True should enable cursor control."""
        policy = RenderPolicy(unicode=True)
        with patch.object(sys.stdout, "isatty", return_value=True):
            assert _supports_cursor_control(policy) is True

    def test_respects_policy_unicode_false(self) -> None:
        """Policy with unicode=False should disable cursor control."""
        policy = RenderPolicy.minimal()  # unicode=False, color=False, emoji=False
        with patch.object(sys.stdout, "isatty", return_value=True):
            assert _supports_cursor_control(policy) is False

    def test_no_tty_overrides_policy(self) -> None:
        """Non-TTY should disable cursor control regardless of policy."""
        policy = RenderPolicy.full()
        with patch.object(sys.stdout, "isatty", return_value=False):
            assert _supports_cursor_control(policy) is False


class TestAnimationRun:
    """Tests for Animation.run method."""

    def test_run_with_frames(self) -> None:
        """Animation runs through all frames."""
        frames_shown = []

        def frame_gen():
            for i in range(3):
                frames_shown.append(i)
                yield f"Frame {i}\n"

        # Run in fallback mode (no TTY)
        with patch.object(sys.stdout, "isatty", return_value=False):
            with patch.object(sys, "stdout", new=io.StringIO()):
                Animation.run(frame_gen(), fps=100, duration=1)

        assert frames_shown == [0, 1, 2]

    def test_run_respects_duration(self) -> None:
        """Animation stops after duration."""
        import time

        frame_count = 0

        def infinite_frames():
            nonlocal frame_count
            while True:
                frame_count += 1
                yield f"Frame {frame_count}\n"

        with patch.object(sys.stdout, "isatty", return_value=False):
            with patch.object(sys, "stdout", new=io.StringIO()):
                start = time.time()
                Animation.run(infinite_frames(), fps=100, duration=0.2)
                elapsed = time.time() - start

        # Should stop around 0.2 seconds
        assert 0.1 < elapsed < 0.5
        assert frame_count > 0

    def test_run_uses_policy(self) -> None:
        """Animation respects provided policy."""
        output = io.StringIO()

        def frame_gen():
            yield "Test\n"

        # With minimal policy (no cursor control)
        policy = RenderPolicy.minimal()
        with (
            patch.object(sys.stdout, "isatty", return_value=True),
            patch.object(sys, "stdout", new=output),
        ):
            Animation.run(frame_gen(), policy=policy)

        # Should not contain cursor control codes
        result = output.getvalue()
        assert "\033[?25l" not in result  # hide cursor
        assert "\033[?25h" not in result  # show cursor


class TestAnimationFallback:
    """Tests for fallback animation mode."""

    def test_fallback_single_line_uses_carriage_return(self) -> None:
        """Single-line frames use carriage return."""
        output = io.StringIO()

        def frame_gen():
            yield "Frame 1\n"
            yield "Frame 2\n"

        with (
            patch.object(sys.stdout, "isatty", return_value=False),
            patch.object(sys, "stdout", new=output),
        ):
            Animation.run(frame_gen(), fps=100)

        result = output.getvalue()
        assert "\r" in result
        assert "Frame 1" in result
        assert "Frame 2" in result

    def test_fallback_multiline_uses_separator(self) -> None:
        """Multi-line frames use separator."""
        output = io.StringIO()

        def frame_gen():
            yield "Line 1\nLine 2\n"
            yield "Line 3\nLine 4\n"

        with (
            patch.object(sys.stdout, "isatty", return_value=False),
            patch.object(sys, "stdout", new=output),
        ):
            Animation.run(frame_gen(), fps=100)

        result = output.getvalue()
        assert "---" in result  # default separator

    def test_fallback_custom_separator(self) -> None:
        """Custom separator is used."""
        output = io.StringIO()

        def frame_gen():
            yield "A\nB\n"
            yield "C\nD\n"

        with (
            patch.object(sys.stdout, "isatty", return_value=False),
            patch.object(sys, "stdout", new=output),
        ):
            Animation.run(frame_gen(), fps=100, fallback_separator="***")

        result = output.getvalue()
        assert "***" in result

    def test_fallback_no_separator(self) -> None:
        """Empty separator disables separators."""
        output = io.StringIO()

        def frame_gen():
            yield "A\nB\n"
            yield "C\nD\n"

        with (
            patch.object(sys.stdout, "isatty", return_value=False),
            patch.object(sys, "stdout", new=output),
        ):
            Animation.run(frame_gen(), fps=100, fallback_separator="")

        result = output.getvalue()
        assert "---" not in result


class TestAnimationAnimated:
    """Tests for animated mode (with cursor control)."""

    def test_animated_uses_cursor_codes(self) -> None:
        """Animated mode uses ANSI cursor codes."""
        output = io.StringIO()
        # Make output look like a TTY
        output.isatty = lambda: True  # type: ignore[method-assign]

        def frame_gen():
            yield "Frame 1\n"
            yield "Frame 2\n"

        # Use full policy to force cursor control
        policy = RenderPolicy.full()
        with (
            patch.dict("os.environ", {"TERM": "xterm"}),
            patch.object(sys, "stdout", new=output),
        ):
            Animation.run(frame_gen(), fps=100, policy=policy)

        result = output.getvalue()
        assert "\033[?25l" in result  # hide cursor
        assert "\033[?25h" in result  # show cursor

    def test_animated_moves_cursor_up(self) -> None:
        """Animated mode moves cursor up between frames."""
        output = io.StringIO()
        # Make output look like a TTY
        output.isatty = lambda: True  # type: ignore[method-assign]

        def frame_gen():
            yield "Line\n"
            yield "Line\n"

        # Use full policy to force cursor control
        policy = RenderPolicy.full()
        with (
            patch.dict("os.environ", {"TERM": "xterm"}),
            patch.object(sys, "stdout", new=output),
        ):
            Animation.run(frame_gen(), fps=100, policy=policy)

        result = output.getvalue()
        assert "\033[1A" in result  # cursor up 1 line
