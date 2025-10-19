"""Main Console class - high-level facade for terminal rendering.

This module provides the primary API for StyledConsole, wrapping Rich console
functionality with additional features like terminal detection, frame/banner
rendering, and HTML export capabilities.
"""

import logging
import sys
from typing import Any, TextIO

from rich.console import Console as RichConsole
from rich.text import Text as RichText

from styledconsole.core.banner import Banner, BannerRenderer
from styledconsole.core.frame import Frame, FrameRenderer
from styledconsole.types import AlignType
from styledconsole.utils.terminal import TerminalProfile, detect_terminal_capabilities
from styledconsole.utils.text import strip_ansi

# Valid alignment options
VALID_ALIGNMENTS = {"left", "center", "right"}


class Console:
    """High-level console rendering facade with Rich backend.

    The Console class is the main entry point for StyledConsole, providing
    a unified API for rendering frames, banners, styled text, and more.
    It integrates with Rich for ANSI rendering and supports HTML export
    via recording mode.

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
        >>> console.banner("SUCCESS", font="slant", gradient_start="green")
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
        self._debug = debug
        self._logger = self._setup_logging() if debug else None

        # Detect terminal capabilities if requested
        self._profile: TerminalProfile | None = None
        if detect_terminal:
            self._profile = detect_terminal_capabilities()
            if self._debug:
                self._logger.debug(
                    f"Terminal detected: ANSI={self._profile.ansi_support}, "
                    f"colors={self._profile.color_depth}, "
                    f"emoji={self._profile.emoji_safe}, "
                    f"size={self._profile.width}x{self._profile.height}"
                )

        # Determine color system based on detected terminal capabilities
        color_system = self._determine_color_system()

        # Initialize Rich console
        self._rich_console = RichConsole(
            record=record,
            width=width,
            file=file or sys.stdout,
            force_terminal=True
            if detect_terminal and self._profile and self._profile.ansi_support
            else None,
            color_system=color_system,
        )

        # Lazy-initialized renderers (created on first use)
        self.__frame_renderer: FrameRenderer | None = None
        self.__banner_renderer: BannerRenderer | None = None

        if self._debug:
            self._logger.debug(
                f"Console initialized: record={record}, width={width}, file={file or 'stdout'}"
            )

    def _setup_logging(self) -> logging.Logger:
        """Set up debug logger for Console class.

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger("styledconsole.console")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(logging.Formatter("[%(name)s] %(levelname)s: %(message)s"))
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        return logger

    def _determine_color_system(self) -> str:
        """Determine appropriate color system based on terminal capabilities.

        Returns:
            Color system string: "standard", "256", "truecolor", or "auto"
        """
        import os

        # Check for environment variable override
        env_override = os.environ.get("SC_FORCE_COLOR_SYSTEM")
        if env_override in {"standard", "256", "truecolor", "auto"}:
            if self._debug:
                self._logger.debug(f"Color system overridden by env: {env_override}")
            return env_override

        # Use detected terminal profile if available
        if self._profile:
            if self._profile.color_depth >= 16777216:  # 24-bit truecolor
                return "truecolor"
            elif self._profile.color_depth >= 256:
                return "256"
            elif self._profile.color_depth >= 8:
                return "standard"

        # Fallback to auto-detection
        return "auto"

    @property
    def _frame_renderer(self) -> FrameRenderer:
        """Lazy-initialized frame renderer."""
        if self.__frame_renderer is None:
            self.__frame_renderer = FrameRenderer()
            if self._debug:
                self._logger.debug("FrameRenderer initialized (lazy)")
        return self.__frame_renderer

    @property
    def _banner_renderer(self) -> BannerRenderer:
        """Lazy-initialized banner renderer."""
        if self.__banner_renderer is None:
            self.__banner_renderer = BannerRenderer()
            if self._debug:
                self._logger.debug("BannerRenderer initialized (lazy)")
        return self.__banner_renderer

    @staticmethod
    def _validate_align(align: str) -> None:
        """Validate alignment parameter.

        Args:
            align: Alignment value to validate

        Raises:
            ValueError: If align is not one of: left, center, right
        """
        if align not in VALID_ALIGNMENTS:
            raise ValueError(f"align must be one of {VALID_ALIGNMENTS}, got: {align!r}")

    @staticmethod
    def _validate_gradient_pair(gradient_start: str | None, gradient_end: str | None) -> None:
        """Validate gradient color pair.

        Args:
            gradient_start: Starting gradient color
            gradient_end: Ending gradient color

        Raises:
            ValueError: If only one gradient color is provided
        """
        if (gradient_start is None) != (gradient_end is None):
            raise ValueError(
                "gradient_start and gradient_end must both be provided or both be None. "
                f"Got gradient_start={gradient_start!r}, gradient_end={gradient_end!r}"
            )

    @staticmethod
    def _validate_dimensions(
        width: int | None = None,
        padding: int | None = None,
        min_width: int | None = None,
        max_width: int | None = None,
    ) -> None:
        """Validate dimensional parameters.

        Args:
            width: Frame width
            padding: Padding value
            min_width: Minimum width
            max_width: Maximum width

        Raises:
            ValueError: If dimensions are invalid
        """
        if padding is not None and padding < 0:
            raise ValueError(f"padding must be >= 0, got: {padding}")

        if width is not None and width < 1:
            raise ValueError(f"width must be >= 1, got: {width}")

        if min_width is not None and min_width < 1:
            raise ValueError(f"min_width must be >= 1, got: {min_width}")

        if max_width is not None and max_width < 1:
            raise ValueError(f"max_width must be >= 1, got: {max_width}")

        if min_width is not None and max_width is not None and min_width > max_width:
            raise ValueError(f"min_width ({min_width}) must be <= max_width ({max_width})")

        if width is not None and min_width is not None and width < min_width:
            raise ValueError(f"width ({width}) must be >= min_width ({min_width})")

    @property
    def terminal_profile(self) -> TerminalProfile | None:
        """Get detected terminal capabilities.

        Returns:
            TerminalProfile with capabilities (ANSI support, color depth, emoji safety,
            dimensions) if terminal detection was enabled, None otherwise.

        Example:
            >>> console = Console(detect_terminal=True)
            >>> if console.terminal_profile.emoji_safe:
            ...     print("Emoji supported: 🚀")
        """
        return self._profile

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
        gradient_start: str | None = None,
        gradient_end: str | None = None,
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
            gradient_start: Starting color for per-line gradient effect. Overrides
                content_color when set. Defaults to None.
            gradient_end: Ending color for per-line gradient effect. Required when
                gradient_start is set. Defaults to None.

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
            ...     gradient_start="red",
            ...     gradient_end="blue"
            ... )
        """
        # Validate inputs
        self._validate_align(align)
        self._validate_gradient_pair(gradient_start, gradient_end)
        self._validate_dimensions(width=width, padding=padding)

        if self._debug:
            self._logger.debug(
                f"Rendering frame: title='{title}', border='{border}', "
                f"width={width}, padding={padding}"
            )

        frame = Frame(
            content=content if isinstance(content, list) else [content],
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            content_color=content_color,
            border_color=border_color,
            title_color=title_color,
            gradient_start=gradient_start,
            gradient_end=gradient_end,
        )

        lines = self._frame_renderer.render_frame(frame)
        for line in lines:
            self._rich_console.print(line, highlight=False, soft_wrap=False)

        if self._debug:
            self._logger.debug(f"Frame rendered: {len(lines)} lines")

    def banner(
        self,
        text: str,
        *,
        font: str = "standard",
        gradient_start: str | None = None,
        gradient_end: str | None = None,
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
                all available fonts. Defaults to "slant".
            gradient_start: Starting color for per-line gradient effect. Accepts
                hex codes, RGB tuples, or CSS4 names. Defaults to None.
            gradient_end: Ending color for per-line gradient effect. Required
                when gradient_start is set. Defaults to None.
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
            ...     gradient_start="red",
            ...     gradient_end="blue",
            ...     border="double"
            ... )
        """
        # Validate inputs
        self._validate_align(align)
        self._validate_gradient_pair(gradient_start, gradient_end)
        self._validate_dimensions(width=width, padding=padding)

        if self._debug:
            self._logger.debug(
                f"Rendering banner: text='{text}', font='{font}', "
                f"gradient={gradient_start}→{gradient_end}, border='{border}'"
            )

        banner_obj = Banner(
            text=text,
            font=font,
            gradient_start=gradient_start,
            gradient_end=gradient_end,
            border=border,
            width=width,
            align=align,
            padding=padding,
        )

        lines = self._banner_renderer.render_banner(banner_obj)
        for line in lines:
            self._rich_console.print(line, highlight=False, soft_wrap=False)

        if self._debug:
            self._logger.debug(f"Banner rendered: {len(lines)} lines")

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
            end: String appended after text. Defaults to "\n" (newline).

        Example:
            >>> console = Console()
            >>> console.text("Success!", color="green", bold=True)
            >>> console.text("Warning", color="yellow", italic=True)
            >>> console.text("Error: File not found", color="red", bold=True)

            >>> # No newline
            >>> console.text("Loading", end="")
            >>> console.text("... done!", color="green")
        """
        if self._debug:
            self._logger.debug(
                f"Printing text: '{text[:50]}...' (color={color}, bold={bold}, italic={italic})"
            )

        # Build Rich Text object with styles
        rich_text = RichText(text)
        if color:
            rich_text.stylize(f"bold {color}" if bold else color)
        elif bold:
            rich_text.stylize("bold")

        if italic:
            rich_text.stylize("italic")
        if underline:
            rich_text.stylize("underline")
        if dim:
            rich_text.stylize("dim")

        self._rich_console.print(rich_text, end=end, highlight=False)

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
        if self._debug:
            self._logger.debug(f"Rendering rule: title='{title}', color={color}")

        self._rich_console.rule(
            title=title,
            style=color,
            align=align,
        )

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
        if count < 0:
            raise ValueError("count must be >= 0")

        for _ in range(count):
            self._rich_console.print()

    def clear(self) -> None:
        """Clear the console screen.

        Clears the terminal screen if ANSI support is available. Does nothing
        if terminal doesn't support ANSI escape codes.

        Example:
            >>> console = Console()
            >>> console.text("Some content")
            >>> console.clear()  # Screen is cleared
        """
        if self._profile and self._profile.ansi_support:
            self._rich_console.clear()
            if self._debug:
                self._logger.debug("Console cleared")
        elif self._debug:
            self._logger.debug("Console clear skipped: no ANSI support")

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
        if not self._rich_console.record:
            raise RuntimeError(
                "Recording mode not enabled. Initialize Console with record=True "
                "to use export_html()."
            )

        if self._debug:
            self._logger.debug(f"Exporting HTML (inline_styles={inline_styles})")

        html = self._rich_console.export_html(inline_styles=inline_styles)

        if self._debug:
            self._logger.debug(f"HTML exported: {len(html)} characters")

        return html

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
        if not self._rich_console.record:
            raise RuntimeError(
                "Recording mode not enabled. Initialize Console with record=True "
                "to use export_text()."
            )

        if self._debug:
            self._logger.debug("Exporting plain text")

        # Get Rich's text export and strip any remaining ANSI codes
        text = self._rich_console.export_text()
        clean_text = strip_ansi(text)

        if self._debug:
            self._logger.debug(f"Text exported: {len(clean_text)} characters")

        return clean_text

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
