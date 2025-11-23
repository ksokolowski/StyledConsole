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
from styledconsole.core.gradient_utils import apply_vertical_border_gradient
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

    def render_frame_to_string(
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
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        border_gradient_direction: str = "vertical",
    ) -> str:
        """Render a frame to a string with all effects applied.

        Args:
            content: Frame content.
            title: Optional title.
            border: Border style.
            width: Frame width.
            padding: Content padding.
            align: Content alignment.
            content_color: Content color.
            border_color: Border color.
            title_color: Title color.
            start_color: Content gradient start.
            end_color: Content gradient end.
            border_gradient_start: Border gradient start.
            border_gradient_end: Border gradient end.
            border_gradient_direction: Border gradient direction.

        Returns:
            Rendered frame as a string containing ANSI escape codes.
        """
        # Normalize colors
        content_color, border_color, title_color, start_color, end_color = self._normalize_colors(
            content_color, border_color, title_color, start_color, end_color
        )

        # Normalize border gradient colors
        border_gradient_start = normalize_color_for_rich(border_gradient_start)
        border_gradient_end = normalize_color_for_rich(border_gradient_end)

        # Normalize content to string
        if isinstance(content, list):
            content_str = "\n".join(str(line) for line in content)
        else:
            content_str = str(content)

        # Default: adjust emoji spacing in content
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

        # Get Rich box style
        box_style = get_box_style(border)

        # Build Panel kwargs
        panel_kwargs = {
            "box": box_style,
            "padding": (0, padding),
            "expand": False,
        }

        # Add width if provided
        if width:
            panel_kwargs["width"] = width
            panel_kwargs["expand"] = True

        # Add title if provided
        if title:
            adj_title = adjust_emoji_spacing_in_text(str(title))
            panel_kwargs["title"] = adj_title
            panel_kwargs["title_align"] = "center"
            if title_color:
                panel_kwargs["title"] = f"[{title_color}]{adj_title}[/]"
            elif border_color:
                panel_kwargs["title"] = f"[{border_color}]{adj_title}[/]"

        # Add border color if provided
        if border_color:
            panel_kwargs["border_style"] = border_color

        # Create Panel
        panel = Panel(content_renderable, **panel_kwargs)

        # Render to string using a temporary console to ensure ANSI codes are generated
        # independent of the main console's state (e.g. if main console is writing to a file)
        import io

        from rich.console import Console as RichConsole

        capture_file = io.StringIO()
        # Use a temporary console with forced terminal and truecolor to get full ANSI output
        temp_console = RichConsole(
            file=capture_file,
            force_terminal=True,
            color_system="truecolor",
            width=width or self._rich_console.width,
        )

        temp_console.print(panel, highlight=False, soft_wrap=False)
        output = capture_file.getvalue()

        # Apply border gradient if needed
        if border_gradient_start and border_gradient_end:
            lines = output.splitlines()
            if border_gradient_direction == "vertical":
                colored_lines = apply_vertical_border_gradient(
                    lines, border_gradient_start, border_gradient_end, border, title
                )
                return "\n".join(colored_lines)
            else:
                return output

        return output

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
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        border_gradient_direction: str = "vertical",
    ) -> None:
        """Render and print a frame using Rich Panel.

        See render_frame_to_string for argument details.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering frame: title='{title}', border='{border}', "
                f"width={width}, padding={padding}"
            )

        output = self.render_frame_to_string(
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
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            border_gradient_direction=border_gradient_direction,
        )

        # Print the output, handling alignment of the frame itself
        lines = output.splitlines()
        for line in lines:
            # Convert to Text to preserve ANSI and handle alignment
            if "\x1b" in line:
                text_obj = RichText.from_ansi(line, no_wrap=True)
            else:
                text_obj = RichText(line, no_wrap=True)

            if align == "center":
                self._rich_console.print(Align.center(text_obj), highlight=False, soft_wrap=True)
            elif align == "right":
                self._rich_console.print(Align.right(text_obj), highlight=False, soft_wrap=True)
            else:
                self._rich_console.print(text_obj, highlight=False, soft_wrap=True)

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
            Renderable object (Text instance with no_wrap=True to prevent wrapping).
        """
        from rich.text import Text

        # If ANSI already present (e.g., prior gradient/banner), wrap via Text.from_ansi
        if "\x1b" in content_str:
            text_obj = Text.from_ansi(content_str)
            text_obj.no_wrap = True
            text_obj.overflow = "ignore"
            return text_obj

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
                # Create Text with markup then set no_wrap
                text_obj = Text.from_markup("\n".join(styled_lines))
                text_obj.no_wrap = True
                text_obj.overflow = "ignore"
                return text_obj
            else:
                text_obj = Text.from_markup(f"[{start_color}]{content_str}[/]")
                text_obj.no_wrap = True
                text_obj.overflow = "ignore"
                return text_obj

        # Solid color
        if content_color:
            text_obj = Text.from_markup(f"[{content_color}]{content_str}[/]")
            text_obj.no_wrap = True
            text_obj.overflow = "ignore"
            return text_obj

        # No styling needed - wrap in Text to control wrapping behavior
        return Text(content_str, no_wrap=True, overflow="ignore")

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

        # Convert to Rich Text to preserve ANSI and handle alignment as a block
        content_str = "\n".join(lines)
        if "\x1b" in content_str:
            content = RichText.from_ansi(content_str, no_wrap=True)
        else:
            content = RichText(content_str, no_wrap=True)

        # Apply alignment
        if align == "center":
            self._rich_console.print(Align.center(content), highlight=False, soft_wrap=True)
        elif align == "right":
            self._rich_console.print(Align.right(content), highlight=False, soft_wrap=True)
        else:
            self._rich_console.print(content, highlight=False, soft_wrap=True)

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
