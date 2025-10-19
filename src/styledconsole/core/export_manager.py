"""Export management for Console output.

This module provides export functionality for recorded console output,
supporting both HTML and plain text formats.
"""

import logging
import sys

from rich.console import Console as RichConsole

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

    def export_html(self, *, inline_styles: bool = True) -> str:
        """Export recorded console output as HTML.

        Converts all recorded ANSI-styled output to HTML with proper formatting,
        colors, and styles. Supports both inline styles (embedded in HTML) and
        external stylesheet references.

        Args:
            inline_styles: If True (default), includes CSS styles inline in the HTML.
                If False, generates HTML that expects external Rich CSS stylesheet.

        Returns:
            Complete HTML document as a string, ready to save or display.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.

        Example:
            >>> manager = ExportManager(rich_console, debug=False)
            >>> html = manager.export_html(inline_styles=True)
            >>> with open("output.html", "w") as f:
            ...     f.write(html)

            >>> # External stylesheet
            >>> html = manager.export_html(inline_styles=False)
            >>> # Requires rich.css file in same directory
        """
        self._validate_recording_enabled()

        if self._debug and self._logger:
            self._logger.debug(f"Exporting HTML (inline_styles={inline_styles})")

        html = self._console.export_html(inline_styles=inline_styles)

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
