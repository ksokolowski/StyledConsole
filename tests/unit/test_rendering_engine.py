"""Tests for RenderingEngine class."""

import io
from unittest.mock import patch

import pytest
from rich.console import Console as RichConsole

from styledconsole.core.rendering_engine import RenderingEngine


class TestRenderingEngineInit:
    """Tests for RenderingEngine initialization."""

    def test_init_basic(self):
        """Test basic initialization without debug."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console)

        assert engine._rich_console is rich_console
        assert engine._debug is False
        assert engine._logger is not None

    def test_init_with_debug(self):
        """Test initialization with debug enabled."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console, debug=True)

        assert engine._rich_console is rich_console
        assert engine._debug is True
        assert engine._logger is not None

    def test_init_creates_logger(self):
        """Test that logger is created with correct name."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console)

        assert engine._logger.name == "styledconsole.core.rendering_engine"


class TestRenderingEngineFrame:
    """Tests for frame rendering."""

    def test_print_frame_simple(self):
        """Test printing a simple frame."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=40, legacy_windows=False)
        engine = RenderingEngine(rich_console)

        engine.print_frame("Test content")

        output = buffer.getvalue()
        assert "Test content" in output
        assert "─" in output or "-" in output  # Border characters

    def test_print_frame_with_title(self):
        """Test printing frame with title."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=40, legacy_windows=False)
        engine = RenderingEngine(rich_console)

        engine.print_frame("Content", title="My Title")

        output = buffer.getvalue()
        assert "My Title" in output
        assert "Content" in output

    def test_print_frame_multiple_lines(self):
        """Test printing frame with list of lines."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=40, legacy_windows=False)
        engine = RenderingEngine(rich_console)

        engine.print_frame(["Line 1", "Line 2", "Line 3"])

        output = buffer.getvalue()
        assert "Line 1" in output
        assert "Line 2" in output
        assert "Line 3" in output

    def test_print_frame_debug_logging(self):
        """Test that frame rendering logs debug messages (v0.3.0: Rich Panel)."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console, debug=True)

        with patch.object(engine._logger, "debug") as mock_debug:
            engine.print_frame("Test", title="Title", border="solid")

            # Check debug calls
            calls = [str(call) for call in mock_debug.call_args_list]
            assert any("Rendering frame" in str(call) for call in calls)
            assert any("Frame rendered" in str(call) for call in calls)


class TestRenderingEngineBanner:
    """Tests for banner rendering."""

    def test_print_banner_simple(self):
        """Test printing a simple banner."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, legacy_windows=False)
        engine = RenderingEngine(rich_console)

        engine.print_banner("Hi")

        output = buffer.getvalue()
        assert len(output) > 0  # Banner produces ASCII art

    def test_print_banner_with_font(self):
        """Test printing banner with specific font."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=80, legacy_windows=False)
        engine = RenderingEngine(rich_console)

        engine.print_banner("X", font="standard")

        output = buffer.getvalue()
        assert len(output) > 0

    def test_print_banner_debug_logging(self):
        """Test that banner rendering logs debug messages."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console, debug=True)

        with (
            patch.object(engine._logger, "debug") as mock_debug,
            # We mock _render_banner_lines to avoid actual rendering logic
            patch.object(engine, "_render_banner_lines", return_value=["line"]),
        ):
            engine.print_banner("Test", font="standard", start_color="blue", end_color="cyan")

            # Check debug calls
            calls = [str(call) for call in mock_debug.call_args_list]
            assert any("Rendering banner" in str(call) for call in calls)
            assert any("Banner rendered" in str(call) for call in calls)


class TestRenderingEngineText:
    """Tests for text rendering."""

    def test_print_text_plain(self):
        """Test printing plain text."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_text("Hello, World!")

        output = buffer.getvalue()
        assert "Hello, World!" in output

    def test_print_text_with_color(self):
        """Test printing colored text."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_text("Colored", color="blue")

        output = buffer.getvalue()
        assert "Colored" in output

    def test_print_text_with_bold(self):
        """Test printing bold text."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_text("Bold text", bold=True)

        output = buffer.getvalue()
        assert "Bold text" in output

    def test_print_text_with_multiple_styles(self):
        """Test printing text with multiple styles."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_text(
            "Styled text",
            color="red",
            bold=True,
            italic=True,
            underline=True,
        )

        output = buffer.getvalue()
        assert "Styled text" in output

    def test_print_text_custom_end(self):
        """Test printing text with custom line ending."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_text("No newline", end="")

        output = buffer.getvalue()
        assert output == "No newline"

    def test_print_text_debug_logging(self):
        """Test that text printing logs debug messages."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console, debug=True)

        with patch.object(engine._logger, "debug") as mock_debug:
            engine.print_text("Test", color="green", bold=True)

            mock_debug.assert_called()
            call_str = str(mock_debug.call_args)
            assert "Printing text" in call_str


class TestRenderingEngineRule:
    """Tests for rule rendering."""

    def test_print_rule_plain(self):
        """Test printing plain rule."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=40, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_rule()

        output = buffer.getvalue()
        assert "─" in output or "-" in output

    def test_print_rule_with_title(self):
        """Test printing rule with title."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=40, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_rule("Section Title")

        output = buffer.getvalue()
        assert "Section Title" in output

    def test_print_rule_with_color(self):
        """Test printing colored rule."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=40, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_rule(title="Blue Rule", color="blue")

        output = buffer.getvalue()
        assert "Blue Rule" in output

    def test_print_rule_debug_logging(self):
        """Test that rule rendering logs debug messages."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console, debug=True)

        with patch.object(engine._logger, "debug") as mock_debug:
            engine.print_rule("Test Rule", color="cyan")

            mock_debug.assert_called()
            call_str = str(mock_debug.call_args)
            assert "Rendering rule" in call_str


class TestRenderingEngineNewline:
    """Tests for newline rendering."""

    def test_print_newline_single(self):
        """Test printing single newline."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_newline()

        output = buffer.getvalue()
        assert output == "\n"

    def test_print_newline_multiple(self):
        """Test printing multiple newlines."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_newline(3)

        output = buffer.getvalue()
        assert output == "\n\n\n"

    def test_print_newline_zero(self):
        """Test printing zero newlines."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, force_terminal=False)
        engine = RenderingEngine(rich_console)

        engine.print_newline(0)

        output = buffer.getvalue()
        assert output == ""

    def test_print_newline_negative_raises(self):
        """Test that negative count raises ValueError."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console)

        with pytest.raises(ValueError, match="count must be >= 0"):
            engine.print_newline(-1)

    def test_print_newline_debug_logging(self):
        """Test that newline printing logs debug messages."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console, debug=True)

        with patch.object(engine._logger, "debug") as mock_debug:
            engine.print_newline(2)

            mock_debug.assert_called()
            call_str = str(mock_debug.call_args)
            assert "Printing 2 blank line(s)" in call_str


class TestRenderingEngineIntegration:
    """Integration tests for RenderingEngine."""

    def test_realistic_document_workflow(self):
        """Test realistic workflow with multiple rendering operations."""
        buffer = io.StringIO()
        rich_console = RichConsole(file=buffer, width=60, force_terminal=False)
        engine = RenderingEngine(rich_console)

        # Title banner
        engine.print_banner("REPORT")

        # Section separator
        engine.print_rule("Introduction")

        # Content frame
        engine.print_frame(
            ["This is line 1", "This is line 2"],
            title="Important Info",
        )

        # Text paragraph
        engine.print_text("Additional details here", color="blue")

        # Spacing
        engine.print_newline(2)

        output = buffer.getvalue()
        # Banner produces ASCII art, so check for ASCII art patterns (underscores, pipes, etc.)
        assert "____" in output or "|||" in output or "|__" in output  # ASCII art patterns
        assert "Introduction" in output
        assert "Important Info" in output
        assert "This is line 1" in output
        assert "Additional details" in output

    def test_debug_mode_comprehensive(self):
        """Test that debug mode logs all operations (v0.3.0: no frame_renderer)."""
        rich_console = RichConsole()
        engine = RenderingEngine(rich_console, debug=True)

        debug_calls = []

        def capture_debug(msg):
            debug_calls.append(msg)

        with patch.object(engine._logger, "debug", side_effect=capture_debug):
            engine.print_frame("Frame test")

            with patch.object(engine, "_render_banner_lines", return_value=["line"]):
                engine.print_banner("Banner test")

            engine.print_text("Text test")
            engine.print_rule("Rule test")
            engine.print_newline(1)

        # Verify debug messages for all operations
        debug_str = " ".join(debug_calls)
        assert "Rendering frame" in debug_str
        assert "Frame rendered" in debug_str
        assert "Rendering banner" in debug_str
        assert "Banner rendered" in debug_str
        assert "Printing text" in debug_str
        assert "Rendering rule" in debug_str
        assert "Printing" in debug_str and "blank line" in debug_str
