"""Tests for Kitty terminal compatibility.

These tests verify that frames render correctly in Kitty terminal,
specifically testing the soft_wrap=False fix that prevents Rich from
re-wrapping pre-formatted content.
"""

from __future__ import annotations

import io

from rich.console import Console as RichConsole

from styledconsole.core.context import StyleContext
from styledconsole.core.rendering_engine import RenderingEngine
from styledconsole.utils.text import visual_width


class TestKittyTerminalDetection:
    """Tests for Kitty terminal detection."""

    def test_kitty_detected_via_window_id(self, monkeypatch):
        """Verify Kitty is detected via KITTY_WINDOW_ID."""
        monkeypatch.setenv("KITTY_WINDOW_ID", "1")
        monkeypatch.setenv("TERM", "xterm-kitty")

        from styledconsole.utils.terminal import is_modern_terminal

        assert is_modern_terminal() is True

    def test_kitty_detected_via_term(self, monkeypatch):
        """Verify Kitty is detected via TERM=xterm-kitty."""
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        monkeypatch.setenv("TERM", "xterm-kitty")
        monkeypatch.setenv("TERM_PROGRAM", "kitty")

        from styledconsole.utils.terminal import is_modern_terminal

        assert is_modern_terminal() is True

    def test_kitty_detected_via_term_program(self, monkeypatch):
        """Verify Kitty is detected via TERM_PROGRAM."""
        monkeypatch.delenv("KITTY_WINDOW_ID", raising=False)
        monkeypatch.setenv("TERM", "xterm-256color")
        monkeypatch.setenv("TERM_PROGRAM", "kitty")

        from styledconsole.utils.terminal import is_modern_terminal

        assert is_modern_terminal() is True


class TestFrameLineCount:
    """Tests to verify frame output has correct number of lines."""

    def test_simple_frame_line_count(self):
        """Verify simple frame has exactly expected lines."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        content = ["Line 1", "Line 2", "Line 3"]
        ctx = StyleContext(border_style="rounded")

        output = engine.render_frame_to_string(content, context=ctx)
        lines = [line for line in output.split("\n") if line.strip()]

        # 3 content lines + 2 border lines = 5 total
        assert len(lines) == 5, f"Expected 5 lines, got {len(lines)}: {lines}"

    def test_single_content_frame_line_count(self):
        """Verify single content frame has exactly 3 lines."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        ctx = StyleContext(border_style="solid")

        output = engine.render_frame_to_string("Single line content", context=ctx)
        lines = [line for line in output.split("\n") if line.strip()]

        # 1 content line + 2 border lines = 3 total
        assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}: {lines}"

    def test_frame_with_title_line_count(self):
        """Verify frame with title has correct line count."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        ctx = StyleContext(title="Test Title", border_style="rounded")

        output = engine.render_frame_to_string("Content", context=ctx)
        lines = [line for line in output.split("\n") if line.strip()]

        # 1 content line + 2 border lines = 3 total (title is in top border)
        assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}: {lines}"


class TestSoftWrapDisabled:
    """Tests to verify soft_wrap=False is working correctly."""

    def test_print_aligned_does_not_wrap_content(self):
        """Verify _print_aligned doesn't add extra lines."""
        buffer = io.StringIO()
        # Use narrow console that might trigger wrapping
        rich_console = RichConsole(file=buffer, width=40, force_terminal=True)
        engine = RenderingEngine(rich_console)

        ctx = StyleContext(title="Test", border_style="solid", width=35)
        engine.print_frame("Short content", context=ctx)

        output = buffer.getvalue()
        lines = [line for line in output.strip().split("\n") if line.strip()]

        # Should be exactly 3 lines: top border, content, bottom border
        assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}: {output}"

    def test_long_content_not_wrapped(self):
        """Verify long content is not re-wrapped by Rich."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        long_content = "A" * 60  # 60 chars of content
        ctx = StyleContext(border_style="solid", width=70)

        engine.print_frame(long_content, context=ctx)

        output = buffer.getvalue()
        lines = [line for line in output.strip().split("\n") if line.strip()]

        # Should still be 3 lines, not wrapped
        assert len(lines) == 3, f"Content wrapped unexpectedly: {output}"


class TestEmojiAlignment:
    """Tests for emoji content alignment in frames."""

    def test_emoji_content_preserved(self):
        """Verify emoji content is not corrupted."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        content = ["Status: Ready", "Warning: Low"]
        ctx = StyleContext(border_style="rounded", width=30)

        output = engine.render_frame_to_string(content, context=ctx)

        # Content should be preserved
        assert "Ready" in output
        assert "Warning" in output

    def test_frame_line_widths_consistent(self):
        """Verify all frame lines have same visual width."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        content = ["Task complete", "Low memory", "Failed"]
        ctx = StyleContext(border_style="rounded", width=35)

        output = engine.render_frame_to_string(content, context=ctx)
        lines = [line for line in output.split("\n") if line.strip()]

        # All lines should have same visual width
        widths = [visual_width(line) for line in lines]

        assert len(set(widths)) == 1, (
            f"Inconsistent widths: {dict(zip(lines, widths, strict=False))}"
        )


class TestGradientFrames:
    """Tests for gradient frame rendering."""

    def test_gradient_frame_line_count(self):
        """Verify gradient frame has correct line count."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        ctx = StyleContext(
            title="Gradient",
            border_style="rounded",
            border_gradient_start="cyan",
            border_gradient_end="magenta",
        )

        output = engine.render_frame_to_string("Gradient content", context=ctx)
        lines = [line for line in output.split("\n") if line.strip()]

        # Should be 3 lines: top border, content, bottom border
        assert len(lines) == 3, f"Expected 3 lines, got {len(lines)}: {lines}"

    def test_gradient_does_not_add_lines(self):
        """Verify gradient application doesn't add extra lines."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        # Render without gradient
        ctx_plain = StyleContext(title="Plain", border_style="rounded")
        output_plain = engine.render_frame_to_string("Content", context=ctx_plain)
        lines_plain = [line for line in output_plain.split("\n") if line.strip()]

        # Render with gradient
        ctx_gradient = StyleContext(
            title="Gradient",
            border_style="rounded",
            border_gradient_start="red",
            border_gradient_end="blue",
        )
        output_gradient = engine.render_frame_to_string("Content", context=ctx_gradient)
        lines_gradient = [line for line in output_gradient.split("\n") if line.strip()]

        # Both should have same number of lines
        assert len(lines_plain) == len(lines_gradient), (
            f"Gradient added lines: plain={len(lines_plain)}, gradient={len(lines_gradient)}"
        )


class TestMultipleFrames:
    """Tests for multiple frames in sequence."""

    def test_multiple_frames_no_extra_lines(self):
        """Verify multiple frames don't accumulate extra lines."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, force_terminal=True)
        engine = RenderingEngine(rich_console)

        # Print multiple frames
        for i in range(3):
            ctx = StyleContext(title=f"Frame {i + 1}", border_style="solid")
            engine.print_frame(f"Content {i + 1}", context=ctx)

        output = buffer.getvalue()
        lines = [line for line in output.strip().split("\n") if line.strip()]

        # 3 frames x 3 lines each = 9 lines
        assert len(lines) == 9, f"Expected 9 lines, got {len(lines)}"
