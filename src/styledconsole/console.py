"""Main Console class - high-level facade for terminal rendering.

This module provides the primary API for StyledConsole, wrapping Rich console
functionality with additional features like terminal detection, frame/banner
rendering, and HTML export capabilities.

Phase 4.4: Refactored to use specialized manager classes (TerminalManager,
ExportManager, RenderingEngine) following the Facade pattern.
"""

import sys
from typing import Any, TextIO

from rich.console import Console as RichConsole

from styledconsole.core.export_manager import ExportManager
from styledconsole.core.rendering_engine import RenderingEngine
from styledconsole.core.terminal_manager import TerminalManager
from styledconsole.types import AlignType
from styledconsole.utils.terminal import TerminalProfile


class Console:
    """High-level console rendering facade with Rich backend.

    The Console class is the main entry point for StyledConsole, providing
    a unified API for rendering frames, banners, styled text, and more.
    It integrates with Rich for ANSI rendering and supports HTML export
    via recording mode.

    Phase 4.4: Refactored to delegate to specialized managers:
        - TerminalManager: Terminal detection and capabilities
        - RenderingEngine: Frame, banner, text, rule, newline rendering
        - ExportManager: HTML and text export functionality

    Features:
        - Terminal capability detection
        - Frame and banner rendering
        - Styled text output with colors and formatting
        - Recording mode for HTML export
        - Debug logging support
        - Custom output streams

    Example:
        >>> console = Console()
        >>> console.frame("Hello World", title="Greeting", border="solid")
        >>> console.banner("SUCCESS", font="slant", start_color="green")
        >>> console.text("Status: OK", color="green", bold=True)

    Attributes:
        terminal_profile: Detected terminal capabilities (if detection enabled)
    """

    def __init__(
        self,
        *,
        detect_terminal: bool = True,
        record: bool = False,
        width: int | None = None,
        file: TextIO | None = None,
        debug: bool = False,
    ):
        """Initialize Console with optional terminal detection and recording.

        Args:
            detect_terminal: Automatically detect terminal capabilities (color depth,
                emoji support, dimensions). Defaults to True.
            record: Enable recording mode for HTML export. When True, all output is
                captured for later export via export_html(). Defaults to False.
            width: Fixed console width in characters. If None, auto-detected from
                terminal or uses Rich default (80). Defaults to None.
            file: Output stream for console output. Defaults to sys.stdout.
            debug: Enable debug logging for library internals. Useful for
                troubleshooting rendering issues. Defaults to False.

        Example:
            >>> # Basic usage
            >>> console = Console()

            >>> # Recording mode for HTML export
            >>> console = Console(record=True)
            >>> console.text("Test")
            >>> html = console.export_html()

            >>> # Custom width and output stream
            >>> import io
            >>> buffer = io.StringIO()
            >>> console = Console(width=100, file=buffer)

            >>> # Debug mode
            >>> console = Console(debug=True)
        """
        # Initialize terminal manager (handles detection and color system)
        self._terminal = TerminalManager(detect=detect_terminal, debug=debug)

        # Initialize Rich console with terminal settings
        self._rich_console = RichConsole(
            record=record,
            width=width,
            file=file or sys.stdout,
            force_terminal=self._terminal.should_force_terminal(),
            color_system=self._terminal.get_color_system(),
        )

        # Initialize rendering engine (handles frame, banner, text, rule, newline)
        self._renderer = RenderingEngine(self._rich_console, debug=debug)

        # Initialize export manager (handles HTML and text export)
        self._exporter = ExportManager(self._rich_console, debug=debug)

        # Store debug flag for backward compatibility
        self._debug = debug

    @property
    def terminal_profile(self) -> TerminalProfile | None:
        """Get detected terminal capabilities.

        Returns:
            TerminalProfile with capabilities (ANSI support, color depth, emoji safety,
            dimensions) if terminal detection was enabled, None otherwise.

        Example:
            >>> console = Console(detect_terminal=True)
            >>> if console.terminal_profile and console.terminal_profile.emoji_safe:
            ...     print("Emoji supported: 🚀")
        """
        return self._terminal.profile

    def frame(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "solid",
        width: int | None = None,
        padding: int = 1,
        align: AlignType = "left",
        content_color: str | None = None,
        border_color: str | None = None,
        title_color: str | None = None,
        start_color: str | None = None,
        end_color: str | None = None,
    ) -> None:
        """Render and print a framed content box.

        Creates a bordered frame around text content with optional title,
        colors, and gradients. Supports all border styles and extensive
        customization.

        Args:
            content: Text content to frame. Can be a single string or list of strings
                (one per line).
            title: Optional title displayed in the top border. Defaults to None.
            border: Border style name. One of: "solid", "double", "rounded", "heavy",
                "thick", "ascii", "minimal", "dots". Defaults to "solid".
            width: Frame width in characters. If None, auto-calculated from content.
                Defaults to None.
            padding: Horizontal padding (spaces) on each side of content. Defaults to 1.
            align: Content alignment within frame. One of: "left", "center", "right".
                Defaults to "left".
            content_color: Color for frame content. Accepts hex codes (#ff0000),
                RGB tuples (255, 0, 0), or CSS4 color names ("red"). Defaults to None.
            border_color: Color for frame border characters. Defaults to None.
            title_color: Color for frame title. If None and border_color is set,
                title uses border_color. Defaults to None.
            start_color: Starting color for per-line gradient effect. Overrides
                content_color when set. Defaults to None.
            end_color: Ending color for per-line gradient effect. Required when
                start_color is set. Defaults to None.

        Example:
            >>> console = Console()
            >>> console.frame("Hello World", title="Greeting", border="double")

            >>> # With colors
            >>> console.frame(
            ...     ["Line 1", "Line 2"],
            ...     title="Status",
            ...     border="solid",
            ...     content_color="lime",
            ...     border_color="cyan"
            ... )

            >>> # With gradient
            >>> console.frame(
            ...     "Test",
            ...     start_color="red",
            ...     end_color="blue"
            ... )
        """
        self._renderer.print_frame(
            content,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            content_color=content_color,
            border_color=border_color,
            title_color=title_color,
            start_color=start_color,
            end_color=end_color,
        )

    def banner(
        self,
        text: str,
        *,
        font: str = "standard",
        start_color: str | None = None,
        end_color: str | None = None,
        border: str | None = None,
        width: int | None = None,
        align: AlignType = "center",
        padding: int = 1,
    ) -> None:
        """Render and print an ASCII art banner.

        Creates large ASCII art text using pyfiglet with optional gradient
        coloring and frame borders. Perfect for headers, titles, and status
        messages.

        Args:
            text: Text to render as ASCII art banner. Emoji characters will
                fallback to plain text rendering.
            font: Pyfiglet font name. Common options: "slant", "banner", "big",
                "digital", "standard". Use BannerRenderer.list_fonts() to see
                all available fonts. Defaults to "standard".
            start_color: Starting color for per-line gradient effect. Accepts
                hex codes, RGB tuples, or CSS4 names. Defaults to None.
            end_color: Ending color for per-line gradient effect. Required
                when start_color is set. Defaults to None.
            border: Optional border style to frame the banner. One of: "solid",
                "double", "rounded", etc. Defaults to None (no border).
            width: Banner width in characters. If None, auto-calculated.
                Defaults to None.
            align: Banner alignment. One of: "left", "center", "right".
                Defaults to "center".
            padding: Horizontal padding when border is used. Defaults to 1.

        Example:
            >>> console = Console()
            >>> console.banner("SUCCESS", font="slant")

            >>> # With gradient and border
            >>> console.banner(
            ...     "DEMO",
            ...     font="banner",
            ...     start_color="red",
            ...     end_color="blue",
            ...     border="double"
            ... )
        """
        self._renderer.print_banner(
            text,
            font=font,
            start_color=start_color,
            end_color=end_color,
            border=border,
            width=width,
            align=align,
            padding=padding,
        )

    def text(
        self,
        text: str,
        *,
        color: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        dim: bool = False,
        end: str = "\n",
    ) -> None:
        """Print styled text with colors and formatting.

        Simple wrapper around Rich's print functionality for styled text output
        with optional color and text formatting attributes.

        Args:
            text: Text content to print.
            color: Text color. Accepts Rich color names ("red", "blue", "green",
                "bright_yellow", etc.) or hex codes. Defaults to None (terminal default).
            bold: Apply bold formatting. Defaults to False.
            italic: Apply italic formatting. Defaults to False.
            underline: Apply underline formatting. Defaults to False.
            dim: Apply dim/faint formatting. Defaults to False.
            end: String appended after text. Defaults to "\\n" (newline).

        Example:
            >>> console = Console()
            >>> console.text("Success!", color="green", bold=True)
            >>> console.text("Warning", color="yellow", italic=True)
            >>> console.text("Error: File not found", color="red", bold=True)

            >>> # No newline
            >>> console.text("Loading", end="")
            >>> console.text("... done!", color="green")
        """
        # Note: RenderingEngine.print_text doesn't support dim, so we need to handle it here
        # Build style string
        styles = []
        if bold:
            styles.append("bold")
        if italic:
            styles.append("italic")
        if underline:
            styles.append("underline")
        if dim:
            styles.append("dim")
        if color:
            styles.append(color)

        # Use Rich console directly for dim support
        if styles:
            from rich.text import Text as RichText

            style_str = " ".join(styles)
            rich_text = RichText(text, style=style_str)
            self._rich_console.print(rich_text, end=end, highlight=False)
        else:
            self._renderer.print_text(
                text,
                color=color,
                bold=bold,
                italic=italic,
                underline=underline,
                end=end,
            )

    def rule(
        self,
        title: str | None = None,
        *,
        color: str = "white",
        style: str = "solid",
        align: str = "center",
    ) -> None:
        """Print a horizontal rule line with optional title.

        Renders a full-width horizontal line (separator) with an optional
        centered title. Useful for section dividers.

        Args:
            title: Optional title text displayed in the center of the rule.
                Defaults to None (plain line).
            color: Rule color. Accepts Rich color names or hex codes.
                Defaults to "white".
            style: Rule line style. Currently only "solid" is supported
                (Rich limitation). Defaults to "solid".
            align: Title alignment within rule. One of: "left", "center", "right".
                Defaults to "center".

        Example:
            >>> console = Console()
            >>> console.rule()  # Plain line
            >>> console.rule("Section 1", color="blue")
            >>> console.rule("Configuration", color="cyan", align="left")
        """
        self._renderer.print_rule(title=title, color=color, style=style, align=align)

    def newline(self, count: int = 1) -> None:
        """Print one or more blank lines.

        Simple utility for adding vertical spacing in console output.

        Args:
            count: Number of blank lines to print. Must be >= 0. Defaults to 1.

        Example:
            >>> console = Console()
            >>> console.text("Line 1")
            >>> console.newline()
            >>> console.text("Line 2")
            >>> console.newline(3)  # Three blank lines
            >>> console.text("Line 3")
        """
        self._renderer.print_newline(count=count)

    def clear(self) -> None:
        """Clear the console screen.

        Clears the terminal screen if ANSI support is available. Does nothing
        if terminal doesn't support ANSI escape codes.

        Example:
            >>> console = Console()
            >>> console.text("Some content")
            >>> console.clear()  # Screen is cleared
        """
        profile = self.terminal_profile
        if profile and profile.ansi_support:
            self._rich_console.clear()

    def export_html(self, *, inline_styles: bool = True) -> str:
        """Export recorded console output as HTML.

        Converts all recorded ANSI output to HTML with preserved formatting,
        colors, and styles. Requires recording mode to be enabled during
        Console initialization (record=True).

        Args:
            inline_styles: Use inline CSS styles (True) or CSS classes (False).
                Inline styles are recommended for standalone HTML files or
                email embedding. Defaults to True.

        Returns:
            HTML string with ANSI formatting converted to styled spans.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.

        Example:
            >>> console = Console(record=True)
            >>> console.frame("Test", title="Demo")
            >>> console.text("Hello", color="green")
            >>> html = console.export_html()
            >>> with open("output.html", "w") as f:
            ...     f.write(html)
        """
        return self._exporter.export_html(inline_styles=inline_styles)

    def export_text(self) -> str:
        """Export recorded console output as plain text.

        Returns all recorded output with ANSI escape codes stripped.
        Useful for logging, testing, or text-only output formats.
        Requires recording mode to be enabled (record=True).

        Returns:
            Plain text string with all ANSI codes removed.

        Raises:
            RuntimeError: If recording mode was not enabled during initialization.

        Example:
            >>> console = Console(record=True)
            >>> console.frame("Test", title="Demo")
            >>> text = console.export_text()
            >>> print(repr(text))  # No ANSI codes
        """
        return self._exporter.export_text()

    def print(self, *args: Any, **kwargs: Any) -> None:
        """Direct pass-through to Rich console print.

        Provides direct access to Rich's print method for advanced use cases
        not covered by Console's high-level methods.

        Args:
            *args: Positional arguments passed to Rich console.print()
            **kwargs: Keyword arguments passed to Rich console.print()

        Example:
            >>> console = Console()
            >>> # Use Rich markup directly
            >>> console.print("[bold red]Error:[/bold red] Something failed")
            >>> # Rich Table, Panel, etc.
            >>> from rich.table import Table
            >>> table = Table()
            >>> console.print(table)
        """
        self._rich_console.print(*args, **kwargs)
