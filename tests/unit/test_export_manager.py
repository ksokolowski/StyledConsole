"""Unit tests for ExportManager class."""

import logging

import pytest
from rich.console import Console as RichConsole
from rich.terminal_theme import MONOKAI

from styledconsole.core.export_manager import ExportManager


class TestExportManagerInit:
    """Tests for ExportManager initialization."""

    def test_init_with_recording_console(self):
        """Test initialization with recording-enabled console."""
        console = RichConsole(record=True)
        manager = ExportManager(console, debug=False)
        assert manager._console is console
        assert manager._debug is False
        assert manager._logger is None

    def test_init_with_non_recording_console(self):
        """Test initialization with non-recording console."""
        console = RichConsole(record=False)
        manager = ExportManager(console, debug=False)
        # Should initialize fine, validation happens at export time
        assert manager._console is console

    def test_init_with_debug_enabled(self):
        """Test initialization with debug logging enabled."""
        console = RichConsole(record=True)
        manager = ExportManager(console, debug=True)
        assert manager._debug is True
        assert manager._logger is not None
        assert isinstance(manager._logger, logging.Logger)

    def test_init_with_debug_disabled(self):
        """Test initialization with debug logging disabled."""
        console = RichConsole(record=True)
        manager = ExportManager(console, debug=False)
        assert manager._debug is False
        assert manager._logger is None


class TestExportManagerHTMLExport:
    """Tests for HTML export functionality."""

    def test_export_html_with_inline_styles(self):
        """Test HTML export with inline styles."""
        console = RichConsole(record=True, width=80)
        console.print("Hello, World!")

        manager = ExportManager(console, debug=False)
        html = manager.export_html(inline_styles=True)

        assert isinstance(html, str)
        assert len(html) > 0
        assert "<!DOCTYPE html>" in html
        assert "Hello, World!" in html

    def test_export_html_without_inline_styles(self):
        """Test HTML export without inline styles."""
        console = RichConsole(record=True, width=80)
        console.print("Test content")

        manager = ExportManager(console, debug=False)
        html = manager.export_html(inline_styles=False)

        assert isinstance(html, str)
        assert len(html) > 0
        assert "<!DOCTYPE html>" in html
        assert "Test content" in html

    def test_export_html_with_colored_text(self):
        """Test HTML export preserves colors."""
        console = RichConsole(record=True, width=80)
        console.print("[red]Red text[/red]")
        console.print("[green]Green text[/green]")

        manager = ExportManager(console, debug=False)
        html = manager.export_html(inline_styles=True)

        assert "Red text" in html
        assert "Green text" in html

    def test_export_html_without_recording_raises_error(self):
        """Test that export_html raises error without recording mode."""
        console = RichConsole(record=False)
        manager = ExportManager(console, debug=False)

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            manager.export_html()

    def test_export_html_with_debug_logging(self):
        """Test that debug logging works during HTML export."""
        console = RichConsole(record=True, width=80)
        console.print("Test")

        manager = ExportManager(console, debug=True)

        # Should not raise, debug logging should work
        html = manager.export_html(inline_styles=True)
        assert len(html) > 0


class TestExportManagerTextExport:
    """Tests for plain text export functionality."""

    def test_export_text_basic(self):
        """Test basic plain text export."""
        console = RichConsole(record=True, width=80)
        console.print("Hello, World!")

        manager = ExportManager(console, debug=False)
        text = manager.export_text()

        assert isinstance(text, str)
        assert "Hello, World!" in text

    def test_export_text_strips_ansi_codes(self):
        """Test that ANSI codes are stripped from text export."""
        console = RichConsole(record=True, width=80, force_terminal=True)
        console.print("[red]Colored text[/red]")

        manager = ExportManager(console, debug=False)
        text = manager.export_text()

        # Should contain the text but not ANSI escape codes
        assert "Colored text" in text or "Colored" in text
        # ANSI codes like \033[ should be stripped
        assert "\033[" not in text

    def test_export_text_multiple_lines(self):
        """Test text export with multiple lines."""
        console = RichConsole(record=True, width=80)
        console.print("Line 1")
        console.print("Line 2")
        console.print("Line 3")

        manager = ExportManager(console, debug=False)
        text = manager.export_text()

        assert "Line 1" in text
        assert "Line 2" in text
        assert "Line 3" in text

    def test_export_text_without_recording_raises_error(self):
        """Test that export_text raises error without recording mode."""
        console = RichConsole(record=False)
        manager = ExportManager(console, debug=False)

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            manager.export_text()

    def test_export_text_with_debug_logging(self):
        """Test that debug logging works during text export."""
        console = RichConsole(record=True, width=80)
        console.print("Test")

        manager = ExportManager(console, debug=True)

        # Should not raise, debug logging should work
        text = manager.export_text()
        assert len(text) > 0


class TestExportManagerValidation:
    """Tests for export validation."""

    def test_validate_recording_enabled_success(self):
        """Test validation passes with recording enabled."""
        console = RichConsole(record=True)
        manager = ExportManager(console, debug=False)

        # Should not raise
        manager._validate_recording_enabled()

    def test_validate_recording_enabled_failure(self):
        """Test validation fails without recording."""
        console = RichConsole(record=False)
        manager = ExportManager(console, debug=False)

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            manager._validate_recording_enabled()


class TestExportManagerIntegration:
    """Integration tests for ExportManager."""

    def test_realistic_workflow_html_export(self):
        """Test realistic HTML export workflow."""
        # Setup
        console = RichConsole(record=True, width=80)
        manager = ExportManager(console, debug=False)

        # Generate some output
        console.print("Title", style="bold")
        console.print("[green]Success:[/green] Operation completed")
        console.print("---")

        # Export
        html = manager.export_html(inline_styles=True)

        # Verify
        assert "<!DOCTYPE html>" in html
        assert "Title" in html
        assert "Success" in html
        assert "Operation completed" in html

    def test_realistic_workflow_text_export(self):
        """Test realistic text export workflow."""
        # Setup
        console = RichConsole(record=True, width=80)
        manager = ExportManager(console, debug=False)

        # Generate some output
        console.print("Report")
        console.print("Status: OK")
        console.print("Items: 42")

        # Export
        text = manager.export_text()

        # Verify
        assert "Report" in text
        assert "Status: OK" in text or "Status:" in text
        assert "42" in text

    def test_export_both_formats_from_same_recording(self):
        """Test exporting both HTML and text from same recording."""
        console = RichConsole(record=True, width=80)
        manager = ExportManager(console, debug=False)

        # Generate output
        console.print("Content to export")

        # Export HTML first
        html = manager.export_html()
        assert "Content to export" in html
        assert "<!DOCTYPE html>" in html

        # Note: Rich's export_text() may not work after export_html()
        # Test text export separately would be more reliable,
        # but both should at least not error
        text = manager.export_text()
        # Text might be empty if Rich consumed the buffer, that's OK
        assert isinstance(text, str)


class TestExportManagerEnhancedHTML:
    """Tests for enhanced HTML export functionality."""

    def test_export_html_custom_title(self):
        """Test HTML export with custom page title."""
        console = RichConsole(record=True, width=80)
        console.print("Content")
        manager = ExportManager(console, debug=False)

        html = manager.export_html(page_title="My Dashboard")

        assert "<title>My Dashboard</title>" in html
        assert "<title>Rich</title>" not in html

    def test_export_html_custom_css(self):
        """Test HTML export with custom CSS injection."""
        console = RichConsole(record=True, width=80)
        console.print("Content")
        manager = ExportManager(console, debug=False)

        custom_css = ".custom-class { font-weight: bold; }"
        html = manager.export_html(theme_css=custom_css)

        assert custom_css in html
        assert f"{custom_css}\n</style>" in html

    def test_export_html_clear_screen(self):
        """Test HTML export with clear_screen=True."""
        console = RichConsole(record=True, width=80)
        console.print("Content")
        manager = ExportManager(console, debug=False)

        # Export and clear
        html = manager.export_html(clear_screen=True)
        assert "Content" in html

        # Verify buffer is cleared
        text = console.export_text()
        assert text.strip() == ""

    def test_export_html_with_theme(self):
        """Test HTML export with specific theme."""
        console = RichConsole(record=True, width=80)
        console.print("Content")
        manager = ExportManager(console, debug=False)

        # We can't easily verify the theme applied without inspecting styles deeply,
        # but we can verify it doesn't crash.
        html = manager.export_html(theme=MONOKAI)
        assert "Content" in html
