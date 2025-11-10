"""Rendering coordination engine for StyledConsole v0.3.0.

This module provides the RenderingEngine class that coordinates rendering
using Rich's native renderables (Panel, Align, etc.) with our gradient
enhancements.

v0.3.0: Architectural rework - uses Rich Panel/Align instead of custom renderers.
"""

import logging

from rich.align import Align
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.text import Text as RichText

from styledconsole.core.banner import Banner, BannerRenderer
from styledconsole.core.box_mapping import get_box_style
from styledconsole.utils.color import normalize_color_for_rich
from styledconsole.utils.text import adjust_emoji_spacing_in_text


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

        # Lazy-initialized banner renderer (banners still use custom pyfiglet integration)
        self.__banner_renderer: BannerRenderer | None = None

        if self._debug:
            self._logger.debug("RenderingEngine initialized (v0.3.0 - Rich native)")

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
        """Render and print a frame using Rich Panel.

        v0.3.0: Uses Rich Panel instead of custom FrameRenderer.
        Automatically converts CSS4/Rich color names to hex for Rich compatibility.

        Args:
            content: Frame content (string or list of lines).
            title: Optional frame title.
            border: Border style name. Defaults to "rounded".
            width: Fixed width or None for auto. Defaults to None.
            padding: Padding around content. Defaults to 1.
            align: Content alignment ("left", "center", "right"). Defaults to "left".
            content_color: Content text color (CSS4/Rich name or hex). Defaults to None.
            border_color: Border color (CSS4/Rich name or hex). Defaults to None.
            title_color: Title text color (CSS4/Rich name or hex). Defaults to None.
            start_color: Gradient start color (CSS4/Rich name or hex). Defaults to None.
            end_color: Gradient end color (CSS4/Rich name or hex). Defaults to None.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering frame: title='{title}', border='{border}', "
                f"width={width}, padding={padding}"
            )

        # Normalize colors (kept separate for testability and lower cyclomatic complexity)
        content_color, border_color, title_color, start_color, end_color = self._normalize_colors(
            content_color, border_color, title_color, start_color, end_color
        )

        # Normalize content to string
        if isinstance(content, list):
            content_str = "\n".join(str(line) for line in content)
        else:
            content_str = str(content)

        # Default: adjust emoji spacing in content (VS16 assumption on by default)
        if content_str:
            content_str = adjust_emoji_spacing_in_text(content_str)

        content_renderable = self._build_content_renderable(
            content_str,
            content_color=content_color,
            start_color=start_color,
            end_color=end_color,
        )

        # Apply content alignment using Rich's Align
        if align == "center":
            content_renderable = Align.center(content_renderable)
        elif align == "right":
            content_renderable = Align.right(content_renderable)
        # else: left alignment (default, no Align wrapper needed)

        # Get Rich box style
        box_style = get_box_style(border)

        # Build Panel kwargs
        panel_kwargs = {
            "box": box_style,
            "padding": (0, padding),  # Rich padding is (vertical, horizontal)
            "expand": False,  # Don't auto-expand by default
        }

        # Add width if provided
        if width:
            panel_kwargs["width"] = width
            # Always expand to fill the specified width for proper title centering
            panel_kwargs["expand"] = True

        # Add title if provided
        if title:
            # Adjust emoji spacing in title before styling
            adj_title = adjust_emoji_spacing_in_text(str(title))
            panel_kwargs["title"] = adj_title
            panel_kwargs["title_align"] = "center"  # Titles always centered for balanced borders
            # Title color: use title_color if set, else border_color, else default
            if title_color:
                panel_kwargs["title"] = f"[{title_color}]{adj_title}[/]"
            elif border_color:
                panel_kwargs["title"] = f"[{border_color}]{adj_title}[/]"

        # Add border color if provided
        if border_color:
            panel_kwargs["border_style"] = border_color

        # Create Panel with aligned content
        panel = Panel(content_renderable, **panel_kwargs)

        self._rich_console.print(panel, highlight=False, soft_wrap=False)

        if self._debug:
            self._logger.debug("Frame rendered using Rich Panel")

    # ----------------------------- Helper Methods -----------------------------
    def _normalize_colors(
        self,
        content_color: str | None,
        border_color: str | None,
        title_color: str | None,
        start_color: str | None,
        end_color: str | None,
    ) -> tuple[str | None, str | None, str | None, str | None, str | None]:
        """Normalize optional color inputs to Rich-compatible hex codes.

        Keeping this logic isolated reduces branching inside print_frame and
        allows future caching/validation (e.g., ensuring start/end pairs).
        """
        return (
            normalize_color_for_rich(content_color),
            normalize_color_for_rich(border_color),
            normalize_color_for_rich(title_color),
            normalize_color_for_rich(start_color),
            normalize_color_for_rich(end_color),
        )

    def _build_content_renderable(
        self,
        content_str: str,
        *,
        content_color: str | None,
        start_color: str | None,
        end_color: str | None,
    ):
        """Return a Rich-compatible renderable for frame content.

        Applies ANSI-aware handling and gradient/color styling. Separated from
        print_frame to keep responsibilities focused:

        - Detect ANSI → convert to Text early (skip further styling)
        - Multi-line gradients → per-line interpolation
        - Single-line gradient → start_color only
        - Solid color → wrap entire content in Rich markup

        Returns:
            Renderable object (string with markup or Rich Text instance).
        """
        # If ANSI already present (e.g., prior gradient/banner), wrap via Text.from_ansi
        if "\x1b" in content_str:
            from rich.text import Text

            return Text.from_ansi(content_str)

        # Gradient application
        if start_color and end_color:
            from styledconsole.utils.color import interpolate_color

            lines = content_str.split("\n")
            if len(lines) > 1:
                styled_lines = []
                for i, line in enumerate(lines):
                    ratio = i / (len(lines) - 1) if len(lines) > 1 else 0
                    color = interpolate_color(start_color, end_color, ratio)
                    styled_lines.append(f"[{color}]{line}[/]")
                return "\n".join(styled_lines)
            else:
                return f"[{start_color}]{content_str}[/]"

        # Solid color
        if content_color:
            return f"[{content_color}]{content_str}[/]"

        # No styling needed
        return content_str

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

        # Log completion
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
        # Adjust emoji spacing by default for plain text printing
        adj_text = adjust_emoji_spacing_in_text(text)
        style = " ".join(style_parts) if style_parts else None
        rich_text = RichText(adj_text, style=style)
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

        # Adjust emoji spacing in rule title if provided
        rule_title = adjust_emoji_spacing_in_text(title) if title else None

        self._rich_console.rule(
            title=rule_title,
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
