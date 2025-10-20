"""Rendering coordination engine for StyledConsole.

This module provides the RenderingEngine class that coordinates all rendering
operations, managing specialized renderers and delegating to Rich Console.

Part of Phase 4.3 - Extract rendering coordination logic from Console class.
"""

import logging

from rich.console import Console as RichConsole
from rich.text import Text as RichText

from styledconsole.core.banner import Banner, BannerRenderer
from styledconsole.core.frame import Frame, FrameRenderer


class RenderingEngine:
    """Coordinates rendering operations for StyledConsole.

    Manages specialized renderers (FrameRenderer, BannerRenderer) using lazy
    initialization and delegates text/rule/newline operations to Rich Console.

    Attributes:
        _rich_console: Rich Console instance for low-level rendering.
        _debug: Enable debug logging for rendering operations.
        _logger: Logger for this rendering engine.
    """

    def __init__(self, rich_console: RichConsole, debug: bool = False) -> None:
        """Initialize the rendering engine.

        Args:
            rich_console: Rich Console instance to use for rendering.
            debug: Enable debug logging. Defaults to False.
        """
        self._rich_console = rich_console
        self._debug = debug
        self._logger = self._setup_logging()

        # Lazy-initialized renderers
        self.__frame_renderer: FrameRenderer | None = None
        self.__banner_renderer: BannerRenderer | None = None

        if self._debug:
            self._logger.debug("RenderingEngine initialized")

    def _setup_logging(self) -> logging.Logger:
        """Set up logging for the rendering engine.

        Returns:
            Configured logger instance.
        """
        logger = logging.getLogger("styledconsole.core.rendering_engine")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if self._debug else logging.WARNING)
        return logger

    @property
    def _frame_renderer(self) -> FrameRenderer:
        """Get the frame renderer, initializing it lazily if needed.

        Returns:
            FrameRenderer instance.
        """
        if self.__frame_renderer is None:
            self.__frame_renderer = FrameRenderer()
            if self._debug:
                self._logger.debug("FrameRenderer initialized (lazy)")
        return self.__frame_renderer

    @property
    def _banner_renderer(self) -> BannerRenderer:
        """Get the banner renderer, initializing it lazily if needed.

        Returns:
            BannerRenderer instance.
        """
        if self.__banner_renderer is None:
            self.__banner_renderer = BannerRenderer()
            if self._debug:
                self._logger.debug("BannerRenderer initialized (lazy)")
        return self.__banner_renderer

    def print_frame(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: str = "left",
        content_color: str | None = None,
        border_color: str | None = None,
        title_color: str | None = None,
        start_color: str | None = None,
        end_color: str | None = None,
    ) -> None:
        """Render and print a frame.

        Args:
            content: Frame content (string or list of lines).
            title: Optional frame title.
            border: Border style. Defaults to "rounded".
            width: Fixed width or None for auto. Defaults to None.
            padding: Padding around content. Defaults to 1.
            align: Content alignment. Defaults to "left".
            content_color: Content text color. Defaults to None.
            border_color: Border color. Defaults to None.
            title_color: Title text color. Defaults to None.
            start_color: Gradient start color. Defaults to None.
            end_color: Gradient end color. Defaults to None.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering frame: title='{title}', border='{border}', "
                f"width={width}, padding={padding}"
            )

        # Normalize content to list of lines
        if isinstance(content, str):
            # Split string by newlines to get individual lines
            content_lines = content.splitlines() if content else [""]
        else:
            # If already a list, process each element for embedded newlines
            content_lines = []
            for item in content:
                if isinstance(item, str) and "\n" in item:
                    # Split items that contain newlines
                    content_lines.extend(item.splitlines())
                else:
                    content_lines.append(item)

        frame = Frame(
            content=content_lines,
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

        lines = self._frame_renderer.render_frame(frame)
        for line in lines:
            self._rich_console.print(line, highlight=False, soft_wrap=False)

        if self._debug:
            self._logger.debug(f"Frame rendered: {len(lines)} lines")

    def print_banner(
        self,
        text: str,
        *,
        font: str = "standard",
        start_color: str | None = None,
        end_color: str | None = None,
        border: str | None = None,
        width: int | None = None,
        align: str = "center",
        padding: int = 1,
    ) -> None:
        """Render and print a banner.

        Args:
            text: Text to display as ASCII art.
            font: FIGlet font name. Defaults to "standard".
            start_color: Gradient start color. Defaults to None.
            end_color: Gradient end color. Defaults to None.
            border: Optional border style. Defaults to None.
            width: Fixed width or None for auto. Defaults to None.
            align: Text alignment. Defaults to "center".
            padding: Padding around banner. Defaults to 1.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering banner: text='{text}', font='{font}', "
                f"gradient={start_color}→{end_color}, border={border}"
            )

        banner_obj = Banner(
            text=text,
            font=font,
            start_color=start_color,
            end_color=end_color,
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

    def print_text(
        self,
        text: str,
        *,
        color: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        end: str = "\n",
    ) -> None:
        """Print styled text.

        Args:
            text: Text to print.
            color: Text color. Defaults to None.
            bold: Apply bold style. Defaults to False.
            italic: Apply italic style. Defaults to False.
            underline: Apply underline style. Defaults to False.
            end: Line ending. Defaults to "\\n".
        """
        if self._debug:
            self._logger.debug(
                f"Printing text: color={color}, bold={bold}, italic={italic}, underline={underline}"
            )

        style_parts = []
        if bold:
            style_parts.append("bold")
        if italic:
            style_parts.append("italic")
        if underline:
            style_parts.append("underline")
        if color:
            style_parts.append(color)

        style = " ".join(style_parts) if style_parts else None
        rich_text = RichText(text, style=style)
        self._rich_console.print(rich_text, end=end, highlight=False)

    def print_rule(
        self,
        title: str | None = None,
        *,
        color: str = "white",
        style: str = "solid",
        align: str = "center",
    ) -> None:
        """Print a horizontal rule line with optional title.

        Args:
            title: Optional title text. Defaults to None.
            color: Rule color. Defaults to "white".
            style: Rule line style. Defaults to "solid".
            align: Title alignment. Defaults to "center".
        """
        if self._debug:
            self._logger.debug(f"Rendering rule: title='{title}', color={color}")

        self._rich_console.rule(
            title=title,
            style=color,
            align=align,
        )

    def print_newline(self, count: int = 1) -> None:
        """Print one or more blank lines.

        Args:
            count: Number of blank lines. Defaults to 1.

        Raises:
            ValueError: If count is negative.
        """
        if count < 0:
            raise ValueError("count must be >= 0")

        if self._debug:
            self._logger.debug(f"Printing {count} blank line(s)")

        for _ in range(count):
            self._rich_console.print()
