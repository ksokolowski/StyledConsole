"""Unit tests for Console class."""

import io
import logging
from unittest.mock import MagicMock, patch

import pytest

from styledconsole.console import Console
from styledconsole.utils.terminal import TerminalProfile


class TestConsoleInitialization:
    """Test Console initialization and configuration."""

    def test_basic_initialization(self):
        """Test Console can be initialized with defaults."""
        console = Console()

        assert console is not None
        assert console._rich_console is not None
        assert console._frame_renderer is not None
        assert console._banner_renderer is not None

    def test_terminal_detection_enabled(self):
        """Test terminal detection when enabled."""
        with patch("styledconsole.console.detect_terminal_capabilities") as mock_detect:
            mock_profile = TerminalProfile(
                ansi_support=True,
                color_depth=256,
                emoji_safe=True,
                width=120,
                height=30,
                term="xterm-256color",
                colorterm=None,
            )
            mock_detect.return_value = mock_profile

            console = Console(detect_terminal=True)

            assert console.terminal_profile == mock_profile
            mock_detect.assert_called_once()

    def test_terminal_detection_disabled(self):
        """Test terminal detection when disabled."""
        console = Console(detect_terminal=False)

        assert console.terminal_profile is None

    def test_recording_mode_enabled(self):
        """Test Console with recording mode enabled."""
        console = Console(record=True)

        assert console._rich_console.record is True

    def test_recording_mode_disabled(self):
        """Test Console with recording mode disabled."""
        console = Console(record=False)

        assert console._rich_console.record is False

    def test_custom_width(self):
        """Test Console with custom fixed width."""
        console = Console(width=100)

        assert console._rich_console.width == 100

    def test_custom_file_output(self):
        """Test Console with custom output stream."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Test")
        output = buffer.getvalue()

        assert "Test" in output

    def test_debug_mode_enabled(self):
        """Test Console with debug logging enabled."""
        with patch("styledconsole.console.Console._setup_logging") as mock_logging:
            mock_logger = MagicMock()
            mock_logging.return_value = mock_logger

            console = Console(debug=True, detect_terminal=False)

            assert console._debug is True
            mock_logging.assert_called_once()

    def test_debug_mode_disabled(self):
        """Test Console with debug logging disabled."""
        console = Console(debug=False, detect_terminal=False)

        assert console._debug is False
        assert console._logger is None


class TestConsoleTerminalProfile:
    """Test terminal_profile property."""

    def test_profile_property_when_detected(self):
        """Test terminal_profile property returns detected profile."""
        with patch("styledconsole.console.detect_terminal_capabilities") as mock_detect:
            mock_profile = TerminalProfile(
                ansi_support=True,
                color_depth=16777216,
                emoji_safe=True,
                width=80,
                height=24,
                term="xterm",
                colorterm="truecolor",
            )
            mock_detect.return_value = mock_profile

            console = Console(detect_terminal=True)
            profile = console.terminal_profile

            assert profile == mock_profile
            assert profile.ansi_support is True
            assert profile.color_depth == 16777216

    def test_profile_property_when_not_detected(self):
        """Test terminal_profile property when detection disabled."""
        console = Console(detect_terminal=False)

        assert console.terminal_profile is None


class TestConsoleFrameMethod:
    """Test frame() method."""

    def test_frame_simple_string(self):
        """Test rendering frame with simple string content."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame("Hello World")
        output = buffer.getvalue()

        assert "Hello World" in output
        assert "┌" in output or "+" in output  # Border character

    def test_frame_with_title(self):
        """Test rendering frame with title."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame("Content", title="Test Title")
        output = buffer.getvalue()

        assert "Content" in output
        assert "Test Title" in output

    def test_frame_with_border_style(self):
        """Test rendering frame with different border styles."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame("Test", border="double")
        output = buffer.getvalue()

        assert "Test" in output
        # Should have double border characters
        assert "═" in output or "=" in output

    def test_frame_with_list_content(self):
        """Test rendering frame with list of lines."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame(["Line 1", "Line 2", "Line 3"])
        output = buffer.getvalue()

        assert "Line 1" in output
        assert "Line 2" in output
        assert "Line 3" in output

    def test_frame_with_colors(self):
        """Test rendering frame with colors."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False, record=True)

        console.frame(
            "Test",
            content_color="#ff0000",
            border_color="blue",
            title_color="green",
        )
        output = buffer.getvalue()

        assert "Test" in output

    def test_frame_with_gradient(self):
        """Test rendering frame with gradient."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame(
            ["Line 1", "Line 2"],
            gradient_start="#ff0000",
            gradient_end="#0000ff",
        )
        output = buffer.getvalue()

        assert "Line 1" in output
        assert "Line 2" in output

    def test_frame_with_custom_width(self):
        """Test rendering frame with custom width."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame("Test", width=50)
        output = buffer.getvalue()

        assert "Test" in output

    def test_frame_with_alignment(self):
        """Test rendering frame with different alignments."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        for align in ["left", "center", "right"]:
            buffer.seek(0)
            buffer.truncate(0)
            console.frame("Test", align=align)
            output = buffer.getvalue()
            assert "Test" in output


class TestConsoleBannerMethod:
    """Test banner() method."""

    def test_banner_simple_text(self):
        """Test rendering banner with simple text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.banner("TEST")
        output = buffer.getvalue()

        # Banner should be multi-line ASCII art
        assert "TEST" in output or len(output.split("\n")) > 2

    def test_banner_with_font(self):
        """Test rendering banner with specific font."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.banner("HI", font="slant")
        output = buffer.getvalue()

        assert len(output) > 0

    def test_banner_with_gradient(self):
        """Test rendering banner with gradient colors."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.banner(
            "OK",
            gradient_start="red",
            gradient_end="blue",
        )
        output = buffer.getvalue()

        assert len(output) > 0

    def test_banner_with_border(self):
        """Test rendering banner with frame border."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.banner("TEST", border="solid")
        output = buffer.getvalue()

        # Should have border characters
        assert "┌" in output or "+" in output
        assert len(output) > 0

    def test_banner_with_alignment(self):
        """Test rendering banner with different alignments."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        for align in ["left", "center", "right"]:
            buffer.seek(0)
            buffer.truncate(0)
            console.banner("OK", align=align)
            output = buffer.getvalue()
            assert len(output) > 0


class TestConsoleTextMethod:
    """Test text() method."""

    def test_text_simple(self):
        """Test printing simple text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Hello World")
        output = buffer.getvalue()

        assert "Hello World" in output

    def test_text_with_color(self):
        """Test printing text with color."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False, record=True)

        console.text("Colored text", color="red")
        output = buffer.getvalue()

        assert "Colored text" in output

    def test_text_with_bold(self):
        """Test printing bold text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Bold text", bold=True)
        output = buffer.getvalue()

        assert "Bold text" in output

    def test_text_with_italic(self):
        """Test printing italic text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Italic text", italic=True)
        output = buffer.getvalue()

        assert "Italic text" in output

    def test_text_with_underline(self):
        """Test printing underlined text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Underlined text", underline=True)
        output = buffer.getvalue()

        assert "Underlined text" in output

    def test_text_with_dim(self):
        """Test printing dim text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Dim text", dim=True)
        output = buffer.getvalue()

        assert "Dim text" in output

    def test_text_with_multiple_styles(self):
        """Test printing text with multiple style attributes."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Styled text", color="blue", bold=True, italic=True)
        output = buffer.getvalue()

        assert "Styled text" in output

    def test_text_with_custom_end(self):
        """Test printing text with custom end character."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("No newline", end="")
        console.text(" continued")
        output = buffer.getvalue()

        assert "No newline continued" in output


class TestConsoleRuleMethod:
    """Test rule() method."""

    def test_rule_plain(self):
        """Test rendering plain horizontal rule."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False, width=80)

        console.rule()
        output = buffer.getvalue()

        # Should have horizontal line characters
        assert len(output.strip()) > 0

    def test_rule_with_title(self):
        """Test rendering rule with title."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False, width=80)

        console.rule("Section Title")
        output = buffer.getvalue()

        assert "Section Title" in output

    def test_rule_with_color(self):
        """Test rendering rule with color."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False, width=80)

        console.rule("Colored Rule", color="blue")
        output = buffer.getvalue()

        assert "Colored Rule" in output

    def test_rule_with_alignment(self):
        """Test rendering rule with different alignments."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False, width=80)

        for align in ["left", "center", "right"]:
            buffer.seek(0)
            buffer.truncate(0)
            console.rule("Title", align=align)
            output = buffer.getvalue()
            assert "Title" in output


class TestConsoleNewlineMethod:
    """Test newline() method."""

    def test_newline_single(self):
        """Test printing single newline."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Line 1")
        console.newline()
        console.text("Line 2")
        output = buffer.getvalue()

        lines = output.split("\n")
        assert len([line for line in lines if line.strip()]) >= 2

    def test_newline_multiple(self):
        """Test printing multiple newlines."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Line 1")
        console.newline(3)
        console.text("Line 2")
        output = buffer.getvalue()

        lines = output.split("\n")
        # Should have at least 3 blank lines between
        assert len(lines) >= 5

    def test_newline_zero(self):
        """Test newline with count=0."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Text")
        console.newline(0)
        output = buffer.getvalue()

        assert "Text" in output

    def test_newline_negative_raises(self):
        """Test newline with negative count raises ValueError."""
        console = Console(detect_terminal=False)

        with pytest.raises(ValueError, match="count must be >= 0"):
            console.newline(-1)


class TestConsoleClearMethod:
    """Test clear() method."""

    def test_clear_with_ansi_support(self):
        """Test clear() when ANSI is supported."""
        with patch("styledconsole.console.detect_terminal_capabilities") as mock_detect:
            mock_profile = TerminalProfile(
                ansi_support=True,
                color_depth=256,
                emoji_safe=True,
                width=80,
                height=24,
                term="xterm",
                colorterm=None,
            )
            mock_detect.return_value = mock_profile

            console = Console(detect_terminal=True)

            # Mock Rich console clear method
            console._rich_console.clear = MagicMock()

            console.clear()

            console._rich_console.clear.assert_called_once()

    def test_clear_without_ansi_support(self):
        """Test clear() when ANSI is not supported."""
        with patch("styledconsole.console.detect_terminal_capabilities") as mock_detect:
            mock_profile = TerminalProfile(
                ansi_support=False,
                color_depth=0,
                emoji_safe=False,
                width=80,
                height=24,
                term="dumb",
                colorterm=None,
            )
            mock_detect.return_value = mock_profile

            console = Console(detect_terminal=True)
            console._rich_console.clear = MagicMock()

            console.clear()

            # Should not call clear when no ANSI support
            console._rich_console.clear.assert_not_called()

    def test_clear_without_detection(self):
        """Test clear() when terminal detection is disabled."""
        console = Console(detect_terminal=False)
        console._rich_console.clear = MagicMock()

        console.clear()

        # Should not call clear when profile is None
        console._rich_console.clear.assert_not_called()


class TestConsoleExportHtml:
    """Test export_html() method."""

    def test_export_html_with_recording_enabled(self):
        """Test HTML export with recording mode enabled."""
        console = Console(record=True, detect_terminal=False)

        console.text("Test content", color="red")
        html = console.export_html()

        assert isinstance(html, str)
        assert len(html) > 0
        assert "Test content" in html

    def test_export_html_with_inline_styles(self):
        """Test HTML export with inline styles."""
        console = Console(record=True, detect_terminal=False)

        console.text("Styled", color="blue")
        html = console.export_html(inline_styles=True)

        assert isinstance(html, str)
        assert "Styled" in html

    def test_export_html_without_inline_styles(self):
        """Test HTML export without inline styles (CSS classes)."""
        console = Console(record=True, detect_terminal=False)

        console.text("Text")
        html = console.export_html(inline_styles=False)

        assert isinstance(html, str)
        assert "Text" in html

    def test_export_html_without_recording_raises(self):
        """Test export_html() raises when recording not enabled."""
        console = Console(record=False, detect_terminal=False)

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            console.export_html()

    def test_export_html_with_frame_content(self):
        """Test HTML export with frame content."""
        console = Console(record=True, detect_terminal=False)

        console.frame("Test", title="Frame Title")
        html = console.export_html()

        assert "Test" in html
        assert "Frame Title" in html


class TestConsoleExportText:
    """Test export_text() method."""

    def test_export_text_with_recording_enabled(self):
        """Test plain text export with recording mode enabled."""
        console = Console(record=True, detect_terminal=False)

        console.text("Plain text content")
        text = console.export_text()

        assert isinstance(text, str)
        assert "Plain text content" in text

    def test_export_text_strips_ansi(self):
        """Test plain text export strips ANSI codes."""
        console = Console(record=True, detect_terminal=False)

        console.text("Colored", color="red", bold=True)
        text = console.export_text()

        # Should contain text but no ANSI escape codes
        assert "Colored" in text
        assert "\033[" not in text  # No ANSI escape sequences

    def test_export_text_without_recording_raises(self):
        """Test export_text() raises when recording not enabled."""
        console = Console(record=False, detect_terminal=False)

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            console.export_text()

    def test_export_text_with_frame_content(self):
        """Test plain text export with frame content."""
        console = Console(record=True, detect_terminal=False)

        console.frame("Test content", title="Title")
        text = console.export_text()

        assert "Test content" in text
        assert "Title" in text


class TestConsolePrintMethod:
    """Test print() pass-through method."""

    def test_print_pass_through(self):
        """Test print() passes through to Rich console."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.print("Direct print")
        output = buffer.getvalue()

        assert "Direct print" in output

    def test_print_with_rich_markup(self):
        """Test print() with Rich markup."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.print("[bold red]Markup[/bold red]")
        output = buffer.getvalue()

        assert "Markup" in output

    def test_print_with_kwargs(self):
        """Test print() with keyword arguments."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.print("Test", end="", style="bold")
        output = buffer.getvalue()

        assert "Test" in output


class TestConsoleDebugLogging:
    """Test debug logging functionality."""

    def test_debug_logging_for_frame(self, caplog):
        """Test debug logging when rendering frame."""
        with caplog.at_level(logging.DEBUG, logger="styledconsole.console"):
            console = Console(debug=True, detect_terminal=False)
            console.frame("Test")

            # Check debug logs were created
            assert any("Rendering frame" in record.message for record in caplog.records)
            assert any("Frame rendered" in record.message for record in caplog.records)

    def test_debug_logging_for_banner(self, caplog):
        """Test debug logging when rendering banner."""
        with caplog.at_level(logging.DEBUG, logger="styledconsole.console"):
            console = Console(debug=True, detect_terminal=False)
            console.banner("TEST")

            assert any("Rendering banner" in record.message for record in caplog.records)
            assert any("Banner rendered" in record.message for record in caplog.records)

    def test_debug_logging_for_terminal_detection(self, caplog):
        """Test debug logging during terminal detection."""
        with caplog.at_level(logging.DEBUG, logger="styledconsole.console"):
            Console(debug=True, detect_terminal=True)

            assert any("Terminal detected" in record.message for record in caplog.records)
            assert any("Console initialized" in record.message for record in caplog.records)

    def test_no_debug_logging_when_disabled(self, caplog):
        """Test no debug logs when debug=False."""
        with caplog.at_level(logging.DEBUG, logger="styledconsole.console"):
            console = Console(debug=False, detect_terminal=False)
            console.frame("Test")

            # Should have no debug logs from console
            console_logs = [r for r in caplog.records if r.name == "styledconsole.console"]
            assert len(console_logs) == 0


class TestConsoleEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_frame_content(self):
        """Test rendering frame with empty content."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame("")
        output = buffer.getvalue()

        # Should still render border
        assert len(output) > 0

    def test_empty_banner_text(self):
        """Test rendering banner with empty text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.banner("")
        output = buffer.getvalue()

        # Should handle gracefully
        assert isinstance(output, str)

    def test_empty_text(self):
        """Test printing empty text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("")
        output = buffer.getvalue()

        # Should print newline
        assert output == "\n"

    def test_multiple_console_instances(self):
        """Test creating multiple Console instances."""
        console1 = Console(detect_terminal=False)
        console2 = Console(detect_terminal=False)

        assert console1 is not console2
        assert console1._rich_console is not console2._rich_console
