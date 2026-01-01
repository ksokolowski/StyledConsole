"""Rendering coordination engine for StyledConsole v0.3.0.

This module provides the RenderingEngine class that coordinates rendering
using Rich's native renderables (Panel, Align, etc.) with our gradient
enhancements.

v0.3.0: Architectural rework - uses Rich Panel/Align instead of custom renderers.

Policy-aware: Respects RenderPolicy for graceful degradation on limited terminals.
- When policy.unicode=False: Uses ASCII borders
- When policy.color=False: Skips gradient/color application
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from rich.align import Align
from rich.console import Console as RichConsole
from rich.text import Text as RichText

from styledconsole.core.banner import Banner
from styledconsole.core.box_mapping import get_box_style_for_policy
from styledconsole.core.context import StyleContext
from styledconsole.core.styles import get_border_chars, get_border_style
from styledconsole.effects.engine import apply_gradient
from styledconsole.effects.strategies import (
    BorderOnly,
    LinearGradient,
    VerticalPosition,
)
from styledconsole.types import AlignType, FrameGroupItem
from styledconsole.utils.color import colorize, normalize_color_for_rich
from styledconsole.utils.text import adjust_emoji_spacing_in_text

if TYPE_CHECKING:
    import pyfiglet

    from styledconsole.policy import RenderPolicy


class RenderingEngine:
    """Coordinates rendering operations for StyledConsole.

    Manages specialized renderers using lazy initialization and delegates
    text/rule/newline operations to Rich Console.

    Policy-aware: Respects RenderPolicy for graceful degradation.

    Attributes:
        _rich_console: Rich Console instance for low-level rendering.
        _debug: Enable debug logging for rendering operations.
        _logger: Logger for this rendering engine.
        _policy: Optional RenderPolicy for environment-aware rendering.
    """

    def __init__(
        self,
        rich_console: RichConsole,
        debug: bool = False,
        policy: RenderPolicy | None = None,
    ) -> None:
        """Initialize the rendering engine.

        Args:
            rich_console: Rich Console instance to use for rendering.
            debug: Enable debug logging. Defaults to False.
            policy: Optional RenderPolicy for environment-aware rendering.
        """
        self._rich_console = rich_console
        self._debug = debug
        self._policy = policy
        self._logger = self._setup_logging()

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

    def render_frame_to_string(
        self,
        content: str | list[str],
        *,
        context: StyleContext,
    ) -> str:
        """Render a frame to a string with all effects applied.

        Args:
            content: Frame content (string or list of strings).
            context: StyleContext object containing all styling parameters.

        Returns:
            Rendered frame as a string containing ANSI escape codes.
        """
        # Use custom renderer to ensure correct emoji width calculation
        output = self._render_custom_frame(content, context)

        # Apply border gradient if needed (skip if color disabled)
        if context.border_gradient_start and context.border_gradient_end:
            # Skip gradient if policy disables color
            if self._policy is not None and not self._policy.color:
                return output

            # Normalize border gradient colors
            border_gradient_start_norm = normalize_color_for_rich(context.border_gradient_start)
            border_gradient_end_norm = normalize_color_for_rich(context.border_gradient_end)

            # Guard for type checker - normalize returns str for non-None input
            if border_gradient_start_norm is None or border_gradient_end_norm is None:
                return output

            lines = output.splitlines()
            if context.border_gradient_direction == "vertical":
                colored_lines = apply_gradient(
                    lines,
                    position_strategy=VerticalPosition(),
                    color_source=LinearGradient(
                        border_gradient_start_norm, border_gradient_end_norm
                    ),
                    target_filter=BorderOnly(),
                    border_chars=get_border_chars(get_border_style(context.border_style)),
                )
                return "\n".join(colored_lines)
            else:
                return output

        return output

    def _render_custom_frame(
        self,
        content: str | list[str],
        context: StyleContext,
    ) -> str:
        """Render frame manually to bypass Rich's incorrect VS16 width calculation."""
        from styledconsole.utils.text import (
            adjust_emoji_spacing_in_text,
            normalize_content,
            render_markup_to_ansi,
            visual_width,
        )

        # Normalize colors
        content_color, border_color, title_color, start_color, end_color = self._normalize_colors(
            context.content_color,
            context.border_color,
            context.title_color,
            context.start_color,
            context.end_color,
        )

        # Prepare content lines
        lines = normalize_content(content)
        lines = [adjust_emoji_spacing_in_text(line) for line in lines]
        lines = [render_markup_to_ansi(line) for line in lines]
        content_widths = [visual_width(line) for line in lines]
        max_content_width = max(content_widths) if content_widths else 0

        # Prepare title
        adj_title, title_width = self._prepare_title(context.title)

        # Calculate dimensions
        _frame_width, inner_width, content_area_width = self._calculate_frame_dimensions(
            context.width, context.padding, max_content_width, title_width, context.title
        )

        # Get box style (policy-aware: falls back to ASCII when unicode disabled)
        box_style = get_box_style_for_policy(context.border_style, self._policy)

        # Build borders
        top_line = self._build_top_border(
            box_style, inner_width, adj_title, title_width, title_color, border_color
        )
        bottom_line = self._build_bottom_border(box_style, inner_width, border_color)

        # Build content lines
        rendered_lines = [top_line]
        rendered_lines.extend(
            self._build_content_lines(
                lines,
                box_style,
                content_area_width,
                context.padding,
                context.align,
                start_color,
                end_color,
                content_color,
                border_color,
                context.width,
            )
        )
        rendered_lines.append(bottom_line)

        # Apply margins if present
        # context.margin is normalized to tuple (top, right, bottom, left) in StyleContext
        if context.margin:
            # Ensure we have a tuple (it should be normalized by StyleContext)
            margins = context.margin if isinstance(context.margin, tuple) else (context.margin,) * 4
            top, _right, bottom, left = margins

            # Apply left margin
            if left > 0:
                pad = " " * left
                rendered_lines = [f"{pad}{line}" for line in rendered_lines]

            # Apply top margin
            if top > 0:
                rendered_lines = ([""] * top) + rendered_lines

            # Apply bottom margin
            if bottom > 0:
                rendered_lines = rendered_lines + ([""] * bottom)

        return "\n".join(rendered_lines)

    def _prepare_title(self, title: str | None) -> tuple[str | None, int]:
        """Prepare title with emoji spacing and markup conversion."""
        from styledconsole.utils.text import (
            adjust_emoji_spacing_in_text,
            render_markup_to_ansi,
            visual_width,
        )

        if not title:
            return None, 0

        adj_title = adjust_emoji_spacing_in_text(title)
        adj_title = render_markup_to_ansi(adj_title)
        return adj_title, visual_width(adj_title)

    def _calculate_frame_dimensions(
        self,
        width: int | None,
        padding: int,
        max_content_width: int,
        title_width: int,
        title: str | None,
    ) -> tuple[int, int, int]:
        """Calculate frame, inner, and content area widths."""
        if width:
            frame_width = width
            inner_width = frame_width - 2
            content_area_width = max(inner_width - (padding * 2), 0)
        else:
            content_area_width = max_content_width
            min_inner_for_title = title_width + 4 if title else 0
            inner_width = max(content_area_width + (padding * 2), min_inner_for_title)
            content_area_width = inner_width - (padding * 2)
            frame_width = inner_width + 2
        return frame_width, inner_width, content_area_width

    def _build_top_border(
        self,
        box_style,
        inner_width: int,
        adj_title: str | None,
        title_width: int,
        title_color: str | None,
        border_color: str | None,
    ) -> str:
        """Build the top border line with optional title."""
        top_bar = box_style.top * inner_width

        if adj_title and title_width <= inner_width - 2:
            left_pad = (inner_width - title_width - 2) // 2
            right_pad = inner_width - title_width - 2 - left_pad

            styled_title = adj_title
            if title_color:
                styled_title = colorize(styled_title, title_color, self._policy)
            elif border_color:
                styled_title = colorize(styled_title, border_color, self._policy)

            top_bar = (
                box_style.top * left_pad + " " + styled_title + " " + box_style.top * right_pad
            )

        top_line = f"{box_style.top_left}{top_bar}{box_style.top_right}"
        if border_color:
            top_line = colorize(top_line, border_color, self._policy)
        return top_line

    def _build_bottom_border(self, box_style, inner_width: int, border_color: str | None) -> str:
        """Build the bottom border line."""
        bottom_line = (
            f"{box_style.bottom_left}{box_style.bottom * inner_width}{box_style.bottom_right}"
        )
        if border_color:
            bottom_line = colorize(bottom_line, border_color, self._policy)
        return bottom_line

    def _build_content_lines(
        self,
        lines: list[str],
        box_style,
        content_area_width: int,
        padding: int,
        align: AlignType,
        start_color: str | None,
        end_color: str | None,
        content_color: str | None,
        border_color: str | None,
        width: int | None,
    ) -> list[str]:
        """Build all content lines with borders and colors."""
        from styledconsole.utils.text import pad_to_width, truncate_to_width, visual_width

        # 1. Prepare raw padded lines
        padded_lines = []
        for line in lines:
            if width and visual_width(line) > content_area_width:
                line = truncate_to_width(line, content_area_width)

            padded_line = pad_to_width(line, content_area_width, align=align)
            full_line = (" " * padding) + padded_line + (" " * padding)
            padded_lines.append(full_line)

        # 2. Apply coloring (Gradient or Solid)
        if start_color and end_color:
            from styledconsole.effects.engine import apply_gradient
            from styledconsole.effects.strategies import Both, LinearGradient, VerticalPosition

            # Use Unified Engine for gradient
            padded_lines = apply_gradient(
                padded_lines,
                position_strategy=VerticalPosition(),
                color_source=LinearGradient(start_color, end_color),
                target_filter=Both(),
                border_chars=set(),
            )
        elif content_color:
            # Apply solid color
            padded_lines = [colorize(line, content_color, self._policy) for line in padded_lines]

        # 3. Add borders
        rendered = []
        left_border = box_style.mid_left
        right_border = box_style.mid_right

        if border_color:
            left_border = colorize(left_border, border_color, self._policy)
            right_border = colorize(right_border, border_color, self._policy)

        for line in padded_lines:
            rendered.append(f"{left_border}{line}{right_border}")

        return rendered

    def print_frame(
        self,
        content: str | list[str],
        *,
        context: StyleContext,
    ) -> None:
        """Render and print a frame using Rich Panel.

        Args:
            content: Frame content (string or list of strings).
            context: StyleContext object containing all styling parameters.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering frame: title='{context.title}', border='{context.border_style}', "
                f"width={context.width}, padding={context.padding}"
            )

        output = self.render_frame_to_string(content, context=context)

        # Print the output, handling alignment of the frame itself
        # We align the entire block to avoid per-line centering issues with emojis
        if "\x1b" in output:
            text_obj = RichText.from_ansi(output, no_wrap=True)
        else:
            text_obj = RichText.from_markup(output)
            text_obj.no_wrap = True

        # Use frame_align if specified, otherwise fallback to align (for backward compat)
        effective_align = context.frame_align if context.frame_align is not None else context.align

        if effective_align == "center":
            self._rich_console.print(Align.center(text_obj), highlight=False, soft_wrap=True)
        elif effective_align == "right":
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
    ) -> RichText:
        """Return a Rich Text renderable for frame content.

        Applies ANSI-aware handling and gradient/color styling. Separated from
        print_frame to keep responsibilities focused:

        - Detect ANSI → convert to Text early (skip further styling)
        - Multi-line gradients → per-line interpolation
        - Single-line gradient → start_color only
        - Solid color → wrap entire content in Rich markup

        Returns:
            RichText instance with no_wrap=True to prevent wrapping.
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
            lines = content_str.split("\n")
            lines = content_str.split("\n")
            if len(lines) > 1:
                from styledconsole.effects.engine import apply_gradient
                from styledconsole.effects.strategies import Both, LinearGradient, VerticalPosition

                # Apply gradient to all content (ignoring borders since this is just a text block)
                styled_lines = apply_gradient(
                    lines,
                    position_strategy=VerticalPosition(),
                    color_source=LinearGradient(start_color, end_color),
                    target_filter=Both(),
                    border_chars=set(),  # No borders in content block
                )

                # Create Text with markup then set no_wrap
                text_obj = Text.from_ansi("\n".join(styled_lines))
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

    def _get_figlet(self, font: str) -> pyfiglet.Figlet:
        """Get cached Figlet instance for a font.

        Args:
            font: Font name

        Returns:
            Cached Figlet instance for the font
        """
        # Simple caching to avoid repeated font loading
        if not hasattr(self, "_figlet_cache"):
            self._figlet_cache: dict[str, pyfiglet.Figlet] = {}

        if font not in self._figlet_cache:
            import pyfiglet

            self._figlet_cache[font] = pyfiglet.Figlet(font=font, width=1000)

        return self._figlet_cache[font]

    def _render_banner_lines(self, banner: Banner) -> list[str]:
        """Render a Banner configuration object to lines.

        Args:
            banner: Banner configuration object

        Returns:
            List of rendered lines ready for printing
        """
        from styledconsole.utils.color import apply_line_gradient
        from styledconsole.utils.text import strip_ansi, visual_width

        # Check if text contains emoji (visual_width > len indicates emoji)
        text_clean = strip_ansi(banner.text)
        has_emoji = visual_width(text_clean) > len(text_clean)

        if has_emoji:
            # Fallback to plain text for emoji
            ascii_lines = [banner.text]
        else:
            # Generate ASCII art using cached Figlet instance
            try:
                figlet = self._get_figlet(banner.font)
                ascii_art = figlet.renderText(banner.text)
                # Split into lines and remove trailing empty lines
                ascii_lines = ascii_art.rstrip("\n").split("\n")
            except Exception as e:
                # Fallback on font error
                if self._debug:
                    self._logger.warning(f"Font error: {e}")
                ascii_lines = [banner.text]

        # Apply gradient coloring if specified
        if banner.rainbow:
            from styledconsole.utils.color import apply_rainbow_gradient

            ascii_lines = apply_rainbow_gradient(ascii_lines)
        elif banner.start_color and banner.end_color:
            ascii_lines = apply_line_gradient(ascii_lines, banner.start_color, banner.end_color)

        # If no border, return ASCII art lines directly
        if banner.border is None:
            return ascii_lines

        # Wrap in frame border using self.render_frame_to_string
        # (no need for temp console - use the existing method)

        # Handle border style object
        border_style = banner.border
        if hasattr(border_style, "name"):
            border_name = border_style.name
        else:
            border_name = str(border_style) if border_style else "solid"

        # If width is None (auto), force left alignment to prevent expansion
        # The banner alignment on screen is handled by print_banner
        align = banner.align if banner.width else "left"

        frame_ctx = StyleContext(
            border_style=border_name,
            width=banner.width,
            align=align,
            padding=banner.padding,
        )
        frame_str = self.render_frame_to_string(
            content=ascii_lines,
            context=frame_ctx,
        )

        return frame_str.splitlines()

    def print_banner(
        self,
        text: str,
        *,
        font: str = "standard",
        start_color: str | None = None,
        end_color: str | None = None,
        rainbow: bool = False,
        border: str | None = None,
        width: int | None = None,
        align: AlignType = "center",
        padding: int = 1,
    ) -> None:
        """Render and print a banner.

        Args:
            text: Text to display as ASCII art.
            font: FIGlet font name. Defaults to "standard".
            start_color: Gradient start color. Defaults to None.
            end_color: Gradient end color. Defaults to None.
            rainbow: Use full ROYGBIV rainbow spectrum. Defaults to False.
            border: Optional border style. Defaults to None.
            width: Fixed width or None for auto. Defaults to None.
            align: Text alignment. Defaults to "center".
            padding: Padding around banner. Defaults to 1.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering banner: text='{text}', font='{font}', "
                f"gradient={start_color}→{end_color}, rainbow={rainbow}, border={border}"
            )

        banner_obj = Banner(
            text=text,
            font=font,
            start_color=start_color,
            end_color=end_color,
            rainbow=rainbow,
            border=border,
            width=width,
            align=align,
            padding=padding,
        )

        lines = self._render_banner_lines(banner_obj)

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
        style = " ".join(style_parts) if style_parts else ""
        rich_text = RichText(adj_text, style=style)
        self._rich_console.print(rich_text, end=end, highlight=False)

    def print_rule(
        self,
        title: str | None = None,
        *,
        color: str = "white",
        style: str = "solid",
        align: AlignType = "center",
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
        rule_title = adjust_emoji_spacing_in_text(title) if title else ""

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

    # ----------------------------- Frame Group Methods -----------------------------

    def render_frame_group_to_string(
        self,
        items: list[FrameGroupItem],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: AlignType = "left",
        border_color: str | None = None,
        title_color: str | None = None,
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        layout: str = "vertical",
        gap: int = 1,
        inherit_style: bool = False,
        margin: int | tuple[int, int, int, int] = 0,
        frame_align: AlignType | None = None,
    ) -> str:
        """Render a group of frames to a string.

        Creates multiple frames arranged within an outer container frame.
        Currently supports vertical layout (frames stacked top to bottom).

        Args:
            items: List of frame item dictionaries. Each dict must have 'content'
                key and may have: title, border, border_color, content_color, title_color.
            title: Optional title for the outer container frame.
            border: Border style for outer frame. Defaults to "rounded".
            width: Fixed width for outer frame. None for auto. Defaults to None.
            padding: Padding inside outer frame. Defaults to 1.
            align: Content alignment within outer frame. Defaults to "left".
            border_color: Color for outer frame border.
            title_color: Color for outer frame title.
            border_gradient_start: Gradient start for outer border.
            border_gradient_end: Gradient end for outer border.
            layout: Layout mode. Currently only "vertical" supported.
            gap: Number of blank lines between inner frames. Defaults to 1.
            inherit_style: If True, inner frames inherit outer border style
                when not explicitly specified. Defaults to False.
            margin: Margin around the outer frame.
            frame_align: Alignment of the outer frame on screen.

        Returns:
            Rendered frame group as a string with ANSI codes.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering frame_group: {len(items)} items, layout={layout}, gap={gap}"
            )

        # Build inner frames content
        inner_content_lines: list[str] = []

        for i, item in enumerate(items):
            content = item.get("content", "")
            item_title = item.get("title")
            item_border = item.get("border", border if inherit_style else "rounded")
            item_border_color = item.get("border_color")
            item_content_color = item.get("content_color")
            item_title_color = item.get("title_color")

            # Render inner frame to string
            inner_ctx = StyleContext(
                title=item_title,
                border_style=item_border,
                border_color=item_border_color,
                title_color=item_title_color,
                content_color=item_content_color,
            )
            inner_frame = self.render_frame_to_string(
                content,
                context=inner_ctx,
            )

            # Add to content
            inner_content_lines.append(inner_frame)

            # Add gap between items (not after last)
            if i < len(items) - 1 and gap > 0:
                inner_content_lines.extend([""] * gap)

        # Join all inner content
        combined_content = "\n".join(inner_content_lines) if inner_content_lines else ""

        # Wrap in outer frame
        outer_ctx = StyleContext(
            title=title,
            border_style=border,
            width=width,
            padding=padding,
            align=align,
            border_color=border_color,
            title_color=title_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            margin=margin,
            frame_align=frame_align,
        )
        return self.render_frame_to_string(
            combined_content,
            context=outer_ctx,
        )

    def print_frame_group(
        self,
        items: list[FrameGroupItem],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: AlignType = "left",
        border_color: str | None = None,
        title_color: str | None = None,
        border_gradient_start: str | None = None,
        border_gradient_end: str | None = None,
        layout: str = "vertical",
        gap: int = 1,
        inherit_style: bool = False,
        margin: int | tuple[int, int, int, int] = 0,
        frame_align: AlignType | None = None,
    ) -> None:
        """Render and print a group of frames.

        See render_frame_group_to_string for argument details.
        """
        output = self.render_frame_group_to_string(
            items,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            border_color=border_color,
            title_color=title_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            layout=layout,
            gap=gap,
            inherit_style=inherit_style,
            margin=margin,
            frame_align=frame_align,
        )

        # Print with proper ANSI handling
        if "\x1b" in output:
            text_obj = RichText.from_ansi(output, no_wrap=True)
        else:
            text_obj = RichText.from_markup(output)
            text_obj.no_wrap = True

        # Resolve alignment: frame_align takes precedence over frame content alignment (align)
        # BUT print_frame_group creates an OUTER frame. The frame_align on RenderFrameToString
        # applies to THAT outer frame relative to the screen.
        effective_align = frame_align if frame_align is not None else align

        if effective_align == "center":
            self._rich_console.print(Align.center(text_obj), highlight=False, soft_wrap=True)
        elif effective_align == "right":
            self._rich_console.print(Align.right(text_obj), highlight=False, soft_wrap=True)
        else:
            self._rich_console.print(text_obj, highlight=False, soft_wrap=True)

        if self._debug:
            self._logger.debug(f"Frame group rendered: {len(items)} frames")
