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

        # Normalize all colors to hex for Rich compatibility
        content_color = normalize_color_for_rich(content_color)
        border_color = normalize_color_for_rich(border_color)
        title_color = normalize_color_for_rich(title_color)
        start_color = normalize_color_for_rich(start_color)
        end_color = normalize_color_for_rich(end_color)

        # Normalize content to string
        if isinstance(content, list):
            content_str = "\n".join(str(line) for line in content)
        else:
            content_str = str(content)

        # Check if content contains ANSI codes (from banner gradients, etc.)
        has_ansi_codes = "\x1b" in content_str

        # If content has ANSI codes, convert to Rich Text object for proper handling
        # This prevents Rich from mis-parsing ANSI sequences and breaking line wrapping
        if has_ansi_codes:
            from rich.text import Text

            # Convert ANSI string to Rich Text object (preserves colors)
            content_renderable = Text.from_ansi(content_str)

            # Note: We skip gradient/color application since content already has ANSI formatting
            # This typically happens when banner renderer has applied gradients
        else:
            # Apply gradient if requested (our unique feature!)
            if start_color and end_color:
                from styledconsole.utils.color import interpolate_color

                lines = content_str.split("\n")
                if len(lines) > 1:
                    styled_lines = []
                    for i, line in enumerate(lines):
                        ratio = i / (len(lines) - 1) if len(lines) > 1 else 0
                        color = interpolate_color(start_color, end_color, ratio)
                        styled_lines.append(f"[{color}]{line}[/]")
                    content_str = "\n".join(styled_lines)
                else:
                    # Single line: use start_color
                    content_str = f"[{start_color}]{content_str}[/]"
            elif content_color:
                # Apply solid color
                content_str = f"[{content_color}]{content_str}[/]"

            content_renderable = content_str

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
            # When explicit width is provided with matching console width, expand to fill
            if self._rich_console.width == width:
                panel_kwargs["expand"] = True

        # Add title if provided
        if title:
            panel_kwargs["title"] = title
            panel_kwargs["title_align"] = align
            # Title color: use title_color if set, else border_color, else default
            if title_color:
                panel_kwargs["title"] = f"[{title_color}]{title}[/]"
            elif border_color:
                panel_kwargs["title"] = f"[{border_color}]{title}[/]"

        # Add border color if provided
        if border_color:
            panel_kwargs["border_style"] = border_color

        # Create Panel with aligned content
        panel = Panel(content_renderable, **panel_kwargs)

        self._rich_console.print(panel, highlight=False, soft_wrap=False)

        if self._debug:
            self._logger.debug("Frame rendered using Rich Panel")

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
