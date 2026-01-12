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
from functools import lru_cache
from typing import TYPE_CHECKING

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
from styledconsole.types import AlignType, ColumnsType, FrameGroupItem
from styledconsole.utils.color import colorize, normalize_color_for_rich
from styledconsole.utils.text import adjust_emoji_spacing_in_text, create_rich_text

if TYPE_CHECKING:
    import pyfiglet

    from styledconsole.policy import RenderPolicy


@lru_cache(maxsize=32)
def _get_cached_figlet(font: str) -> pyfiglet.Figlet:
    """Get a cached Figlet instance for a font.

    Module-level cached function to avoid repeated font loading.
    Figlet fonts are loaded from disk, so caching improves performance
    significantly when rendering multiple banners with the same font.

    Args:
        font: Font name (e.g., "standard", "slant", "banner")

    Returns:
        Cached Figlet instance for the font

    Note:
        Cache size of 32 is sufficient for typical usage where
        applications use a small set of fonts repeatedly.
    """
    import pyfiglet

    return pyfiglet.Figlet(font=font, width=1000)


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

        # Apply effect if provided (new v0.9.9.3+ system)
        if context.effect is not None:
            # Skip if policy disables color
            if self._policy is not None and not self._policy.color:
                return output

            from styledconsole.effects.resolver import resolve_effect

            position, color_source, target_filter = resolve_effect(context.effect)

            lines = output.splitlines()
            colored_lines = apply_gradient(
                lines,
                position_strategy=position,
                color_source=color_source,
                target_filter=target_filter,
                border_chars=get_border_chars(get_border_style(context.border_style)),
            )
            return "\n".join(colored_lines)

        # Legacy: Apply border gradient if needed (skip if color disabled)
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

        # Print with alignment (frame_align takes precedence for backward compat)
        effective_align = context.frame_align if context.frame_align is not None else context.align
        self._print_aligned(create_rich_text(output), effective_align)

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

    def _print_aligned(self, text_obj: RichText, align: str = "left") -> None:
        """Print RichText with alignment handling.

        Args:
            text_obj: RichText object to print.
            align: Alignment ("left", "center", "right").

        Note:
            Uses manual padding instead of Rich's native Align class for center/right
            alignment. This ensures consistency with StyledConsole's terminal-aware
            visual_width() calculation and avoids discrepancies with Rich's internal
            cell_len() that could cause line wraps in environments like VS Code.
        """
        if align == "left" or not align:
            self._rich_console.print(text_obj, highlight=False, soft_wrap=False)
            return

        # Manual alignment to avoid Rich width discrepancies
        from styledconsole.utils.text import visual_width

        # For multi-line text (like frames), align each line individually
        content = text_obj.plain
        if "\n" in content:
            # Re-render to ANSI to preserve styles while padding
            from io import StringIO

            buffer = StringIO()
            temp_console = RichConsole(file=buffer, force_terminal=True, width=10000)
            temp_console.print(text_obj, highlight=False, soft_wrap=False)
            lines = buffer.getvalue().splitlines()

            term_width = self._rich_console.width
            aligned_lines = []
            for line in lines:
                v_width = visual_width(line)
                if align == "center":
                    indent = max(0, (term_width - v_width) // 2)
                else:  # right
                    indent = max(0, term_width - v_width)
                aligned_lines.append(" " * indent + line)

            # Wrap in Text.from_ansi so Rich understands the content has escape codes
            # and applies the correct visual width (avoiding wrapping of ANSI sequences)
            from rich.text import Text

            self._rich_console.print(
                Text.from_ansi("\n".join(aligned_lines)), highlight=False, soft_wrap=False
            )
        else:
            # Single line alignment
            v_width = visual_width(content)
            term_width = self._rich_console.width
            if align == "center":
                indent = max(0, (term_width - v_width) // 2)
            else:  # right
                indent = max(0, term_width - v_width)

            if indent > 0:
                self._rich_console.print(" " * indent, end="")
            self._rich_console.print(text_obj, highlight=False, soft_wrap=False)

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
        return _get_cached_figlet(font)

    def _render_banner_lines(self, banner: Banner, width: int | None = None) -> list[str]:
        """Render a Banner configuration object to lines.

        Args:
            banner: Banner configuration object
            width: Optional maximum width for truncation

        Returns:
            List of rendered lines ready for printing
        """
        from styledconsole.utils.color import apply_line_gradient
        from styledconsole.utils.text import strip_ansi, truncate_to_width, visual_width

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

        # Truncate lines if width is specified and exceeded
        if width:
            truncated_lines = []
            for line in ascii_lines:
                if visual_width(line) > width:
                    # Clean cut for ASCII art looks better than ellipses on every line
                    truncated_lines.append(truncate_to_width(line, width, suffix=""))
                else:
                    truncated_lines.append(line)
            ascii_lines = truncated_lines

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

        from styledconsole.core.banner import Banner
        from styledconsole.utils.text import create_rich_text

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

        # Calculate available width to prevent wrapping
        # We use the actual terminal width (self._rich_console.size.width)
        # instead of the preferred width (self._rich_console.width) to allow
        # banners to expand if the terminal is large enough, even if a fixed
        # console width was set (though usually they are the same).
        term_width = self._rich_console.size.width
        # Banners with borders take up 4 chars of width (2 corners + 2 padding)
        available_width = term_width - 4 if border else term_width

        lines = self._render_banner_lines(banner_obj, width=available_width)
        text_obj = create_rich_text("\n".join(lines))
        self._print_aligned(text_obj, align=align)

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

        # Use create_rich_text to handle markup and ANSI codes
        rich_text = create_rich_text(adj_text)
        if style:
            rich_text.stylize(style)

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

        # Adjust emoji spacing and parse markup in rule title if provided
        rule_title = adjust_emoji_spacing_in_text(title) if title else ""
        rich_title = create_rich_text(rule_title)

        self._rich_console.rule(
            title=rich_title,
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
        columns: ColumnsType = "auto",
        min_columns: int = 2,
        item_width: int | None = None,
    ) -> str:
        """Render a group of frames to a string.

        Creates multiple frames arranged within an outer container frame.
        Supports vertical, horizontal, and grid layouts.

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
            layout: Layout mode. One of "vertical", "horizontal", or "grid".
            gap: Space between frames (lines for vertical, chars for horizontal).
            inherit_style: If True, inner frames inherit outer border style.
            margin: Margin around the outer frame.
            frame_align: Alignment of the outer frame on screen.
            columns: Number of columns for horizontal/grid layout.
                Use "auto" to calculate from terminal width. Defaults to "auto".
            min_columns: Minimum columns when columns="auto". Defaults to 2.
            item_width: Width of each item frame. Required for horizontal/grid
                layout when columns="auto". If None, uses 35.

        Returns:
            Rendered frame group as a string with ANSI codes.
        """
        if self._debug:
            self._logger.debug(
                f"Rendering frame_group: {len(items)} items, layout={layout}, gap={gap}"
            )

        # Handle horizontal and grid layouts
        if layout in ("horizontal", "grid"):
            return self._render_horizontal_frame_group(
                items=items,
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
                columns=columns,
                min_columns=min_columns,
                item_width=item_width,
            )

        # Vertical layout (original behavior)
        return self._render_vertical_frame_group(
            items=items,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            border_color=border_color,
            title_color=title_color,
            border_gradient_start=border_gradient_start,
            border_gradient_end=border_gradient_end,
            gap=gap,
            inherit_style=inherit_style,
            margin=margin,
            frame_align=frame_align,
        )

    def _render_vertical_frame_group(
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
        gap: int = 1,
        inherit_style: bool = False,
        margin: int | tuple[int, int, int, int] = 0,
        frame_align: AlignType | None = None,
    ) -> str:
        """Render frames in vertical layout (stacked top to bottom)."""
        inner_content_lines: list[str] = []

        for i, item in enumerate(items):
            content = item.get("content", "")
            item_title = item.get("title")
            item_border = item.get("border", border if inherit_style else "rounded")
            item_border_color = item.get("border_color")
            item_content_color = item.get("content_color")
            item_title_color = item.get("title_color")

            inner_ctx = StyleContext(
                title=item_title,
                border_style=item_border,
                border_color=item_border_color,
                title_color=item_title_color,
                content_color=item_content_color,
            )
            inner_frame = self.render_frame_to_string(content, context=inner_ctx)
            inner_content_lines.append(inner_frame)

            if i < len(items) - 1 and gap > 0:
                inner_content_lines.extend([""] * gap)

        combined_content = "\n".join(inner_content_lines) if inner_content_lines else ""

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
        return self.render_frame_to_string(combined_content, context=outer_ctx)

    def _render_horizontal_frame_group(
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
        layout: str = "horizontal",
        gap: int = 2,
        inherit_style: bool = False,
        margin: int | tuple[int, int, int, int] = 0,
        frame_align: AlignType | None = None,
        columns: ColumnsType = "auto",
        min_columns: int = 2,
        item_width: int | None = None,
    ) -> str:
        """Render frames in horizontal or grid layout (side by side).

        For horizontal layout: all items in one row.
        For grid layout: items arranged in rows based on columns setting.
        """
        from styledconsole.utils.text import visual_width

        # Default item width
        effective_item_width = item_width if item_width is not None else 35

        # Calculate number of columns
        if columns == "auto":
            terminal_width = self._rich_console.width
            # Formula: max(min_columns, (terminal_width + gap) // (item_width + gap))
            calculated_cols = (terminal_width + gap) // (effective_item_width + gap)
            num_columns = max(min_columns, calculated_cols)
        else:
            num_columns = columns

        # For horizontal layout, put all items in one row
        if layout == "horizontal":
            num_columns = len(items)

        # Render all item frames
        rendered_frames: list[list[str]] = []
        for item in items:
            content = item.get("content", "")
            item_title = item.get("title")
            item_border = item.get("border", border if inherit_style else "rounded")
            item_border_color = item.get("border_color")
            item_content_color = item.get("content_color")
            item_title_color = item.get("title_color")

            inner_ctx = StyleContext(
                title=item_title,
                border_style=item_border,
                border_color=item_border_color,
                title_color=item_title_color,
                content_color=item_content_color,
                width=effective_item_width,
            )
            inner_frame = self.render_frame_to_string(content, context=inner_ctx)

            # Split and clean trailing empty lines
            lines = inner_frame.split("\n")
            if lines and lines[-1].strip() == "":
                lines = lines[:-1]
            rendered_frames.append(lines)

        # Build rows of frames
        all_row_outputs: list[str] = []

        for row_start in range(0, len(rendered_frames), num_columns):
            row_frames = rendered_frames[row_start : row_start + num_columns]

            # Get max lines in this row
            max_lines = max(len(f) for f in row_frames) if row_frames else 0

            # Pad all frames to have the same number of lines
            for frame_lines in row_frames:
                while len(frame_lines) < max_lines:
                    frame_lines.append("")

            # Combine frames line by line
            row_lines: list[str] = []
            for line_idx in range(max_lines):
                line_parts: list[str] = []
                for frame_lines in row_frames:
                    line = frame_lines[line_idx]
                    if line:
                        # Calculate visual width and pad
                        vwidth = visual_width(line)
                        if vwidth < effective_item_width:
                            line += " " * (effective_item_width - vwidth)
                    else:
                        line = " " * effective_item_width
                    line_parts.append(line)

                # Join with gap
                row_lines.append((" " * gap).join(line_parts))

            all_row_outputs.append("\n".join(row_lines))

        # Join rows with vertical gap
        combined_content = ("\n" + "\n" * gap).join(all_row_outputs)

        # If no outer frame requested (title is None and no border styling),
        # return just the combined content
        if title is None and border_color is None and border_gradient_start is None:
            return combined_content

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
        return self.render_frame_to_string(combined_content, context=outer_ctx)

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
        columns: ColumnsType = "auto",
        min_columns: int = 2,
        item_width: int | None = None,
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
            columns=columns,
            min_columns=min_columns,
            item_width=item_width,
        )

        # Print with alignment (frame_align takes precedence for outer frame positioning)
        effective_align = frame_align if frame_align is not None else align
        self._print_aligned(create_rich_text(output), effective_align)

        if self._debug:
            self._logger.debug(f"Frame group rendered: {len(items)} frames")
