"""Export management for Console output.

This module provides export functionality for recorded console output,
supporting both HTML and plain text formats.
"""

import logging
import sys

from rich.console import Console as RichConsole
from rich.terminal_theme import TerminalTheme

from styledconsole.utils.text import strip_ansi


class ExportManager:
    """Manages export operations for recorded console output.

    This class encapsulates export-related functionality including:
    - HTML export with inline or external styles
    - Plain text export with ANSI codes stripped
    - Export validation and error handling
    - Debug logging for export operations

    Attributes:
        None (operates on provided Rich console instance)

    Example:
        >>> from rich.console import Console as RichConsole
        >>> rich_console = RichConsole(record=True)
        >>> manager = ExportManager(rich_console, debug=True)
        >>> rich_console.print("Hello")
        >>> html = manager.export_html()
        >>> text = manager.export_text()
    """

    def __init__(self, rich_console: RichConsole, debug: bool = False):
        """Initialize export manager with Rich console instance.

        Args:
            rich_console: Rich Console instance to export from.
                Must have recording enabled (record=True) for exports to work.
            debug: Enable debug logging for export operations.

        Example:
            >>> from rich.console import Console as RichConsole
            >>> console = RichConsole(record=True)
            >>> manager = ExportManager(console, debug=True)
        """
        self._console = rich_console
        self._debug = debug
        self._logger = self._setup_logging() if debug else None

    def _setup_logging(self) -> logging.Logger:
        """Set up debug logger for ExportManager.

        Returns:
            Configured logger instance that writes to stderr.

        Note:
            Logger is only created if debug=True in __init__.
            Uses format: [module.class] LEVEL: message
        """
        logger = logging.getLogger("styledconsole.export")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        return logger

    def _validate_recording_enabled(self) -> None:
        """Validate that recording mode is enabled.

        Raises:
            RuntimeError: If recording mode was not enabled during Console initialization.

        Note:
            Called internally by export_html() and export_text() before attempting export.
        """
        if not self._console.record:
            raise RuntimeError(
                "Recording mode not enabled. Initialize Console with record=True "
                "to use export methods."
            )

    def export_html(
        self,
        *,
        theme: "TerminalTheme | None" = None,
        clear_screen: bool = False,
        inline_styles: bool = True,
        page_title: str = "StyledConsole Export",
        theme_css: str | None = None,
    ) -> str:
        """Export recorded console output as HTML.

        Converts all recorded ANSI-styled output to HTML with proper formatting,
        colors, and styles. Supports both inline styles (embedded in HTML) and
        external stylesheet references.

        Args:
            theme: TerminalTheme object to use for export. Defaults to None (current theme).
            clear_screen: If True, clears the recording buffer after export. Defaults to False.
            inline_styles: If True (default), includes CSS styles inline in the HTML.
                If False, generates HTML that expects external Rich CSS stylesheet.
            page_title: Title for the HTML page. Defaults to "StyledConsole Export".
            theme_css: Custom CSS to inject into the <style> block. Defaults to None.

        Returns:
            Complete HTML document as a string, ready to save or display.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.
        """
        self._validate_recording_enabled()

        if self._debug and self._logger:
            self._logger.debug(
                f"Exporting HTML (inline_styles={inline_styles}, title='{page_title}')"
            )

        html = self._console.export_html(
            theme=theme,
            clear=clear_screen,
            inline_styles=inline_styles,
        )

        # Inject page title and custom CSS if provided
        if page_title != "StyledConsole Export":
            if "<title>Rich</title>" in html:
                html = html.replace("<title>Rich</title>", f"<title>{page_title}</title>")
            elif "<head>" in html:
                # If no title tag exists but head does, insert it
                html = html.replace("<head>", f"<head>\n<title>{page_title}</title>")

        # CSS to force VS16 emojis to width 1ch (mimicking terminal behavior)
        vs16_css = """
    /* VS16 Emoji Alignment Fix */
    .rich-emoji-vs16 {
        display: inline-block;
        width: 1ch;
        overflow: visible;
        white-space: nowrap;
        vertical-align: text-bottom;
        text-align: left;
    }
        """

        # Combine VS16 CSS with custom CSS
        combined_css = vs16_css
        if theme_css:
            combined_css += "\n" + theme_css

        # Inject combined CSS before the closing </style> tag
        if "</style>" in html:
            html = html.replace("</style>", f"{combined_css}\n</style>")
        elif "<head>" in html:
            # If no style tag exists (e.g. inline_styles=False), insert one
            html = html.replace("</head>", f"<style>\n{combined_css}\n</style>\n</head>")

        # Post-process HTML to wrap VS16 sequences
        # We look for any character followed by \uFE0F (VS16)
        # Note: Rich exports raw UTF-8. Be careful not to break HTML tags.
        # Rich might wrap text in spans like <span ...>X</span>.
        # If we have "⚠️" it might be "⚠\ufe0f".
        # Let's try a regex replacement on the HTML string.
        # We match any non-tag character followed by VS16.

        import re

        # Match a character that is NOT > (end of tag) followed by VS16
        # This is a heuristic but should work for Rich's output format
        # We capture the base char (group 1) and the VS16 (group 2)
        # Regex: ([^>])(\uFE0F)
        # IMPORTANT: We use a negative lookahead (?!\u200d) to ensure we don't break
        # ZWJ sequences (like 🏳️‍🌈) where the VS16 is followed by a joiner.
        html = re.sub(
            r"([^>])(\ufe0f)(?!\u200d)", r'<span class="rich-emoji-vs16">\1\2</span>', html
        )

        if self._debug and self._logger:
            self._logger.debug(f"HTML exported: {len(html)} characters")

        return html

    def export_text(self) -> str:
        """Export recorded console output as plain text.

        Returns all recorded output with ANSI escape codes stripped.
        Useful for logging, testing, or text-only output formats.

        Returns:
            Plain text string with all ANSI codes removed.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.

        Example:
            >>> manager = ExportManager(rich_console, debug=False)
            >>> text = manager.export_text()
            >>> print(repr(text))  # No ANSI codes
            >>> assert "\\033[" not in text  # Verify no escape codes
        """
        self._validate_recording_enabled()

        if self._debug and self._logger:
            self._logger.debug("Exporting plain text")

        # Get Rich's text export and strip any remaining ANSI codes
        text = self._console.export_text()
        clean_text = strip_ansi(text)

        if self._debug and self._logger:
            self._logger.debug(f"Text exported: {len(clean_text)} characters")

        return clean_text


__all__ = ["ExportManager"]
