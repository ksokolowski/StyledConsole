"""Frame rendering with borders, padding, and titles.

This module provides high-level frame rendering that builds on BorderStyle primitives.
"""

from dataclasses import dataclass
from typing import Literal

from styledconsole.core.styles import BorderStyle, get_border_style
from styledconsole.utils.color import interpolate_color, parse_color
from styledconsole.utils.text import pad_to_width, truncate_to_width, visual_width

AlignType = Literal["left", "center", "right"]


@dataclass
class Frame:
    """Configuration for a rendered frame.

    Attributes:
        content: Text content to display (single line or list of lines)
        title: Optional title for the frame
        border: Border style name or BorderStyle object
        width: Frame width (auto-calculated if None)
        padding: Internal padding (left/right spaces)
        align: Content alignment ("left", "center", "right")
        min_width: Minimum frame width (when auto-calculating)
        max_width: Maximum frame width (when auto-calculating)
        content_color: Color for content text (hex, rgb, or CSS4 name)
        border_color: Color for border (hex, rgb, or CSS4 name)
        title_color: Color for title (hex, rgb, or CSS4 name)
        gradient_start: Starting color for content gradient (overrides content_color)
        gradient_end: Ending color for content gradient
    """

    content: str | list[str]
    title: str | None = None
    border: str | BorderStyle = "solid"
    width: int | None = None
    padding: int = 1
    align: AlignType = "left"
    min_width: int = 20
    max_width: int = 100
    content_color: str | None = None
    border_color: str | None = None
    title_color: str | None = None
    gradient_start: str | None = None
    gradient_end: str | None = None


class FrameRenderer:
    """Renders frames with borders, titles, and padding."""

    # Valid alignment options
    VALID_ALIGNMENTS = {"left", "center", "right"}

    def __init__(self) -> None:
        """Initialize the frame renderer."""
        pass

    @staticmethod
    def _validate_align(align: AlignType) -> None:
        """Validate alignment parameter.

        Args:
            align: Alignment value to validate

        Raises:
            ValueError: If align is not one of: left, center, right
        """
        if align not in FrameRenderer.VALID_ALIGNMENTS:
            raise ValueError(
                f"align must be one of {FrameRenderer.VALID_ALIGNMENTS}, got: {align!r}"
            )

    @staticmethod
    def _validate_dimensions(
        width: int | None = None,
        padding: int = 1,
        min_width: int = 20,
        max_width: int = 100,
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
        if padding < 0:
            raise ValueError(f"padding must be >= 0, got: {padding}")

        if width is not None and width < 1:
            raise ValueError(f"width must be >= 1, got: {width}")

        if min_width < 1:
            raise ValueError(f"min_width must be >= 1, got: {min_width}")

        if max_width < 1:
            raise ValueError(f"max_width must be >= 1, got: {max_width}")

        if min_width > max_width:
            raise ValueError(f"min_width ({min_width}) must be <= max_width ({max_width})")

        if width is not None and width < min_width:
            raise ValueError(f"width ({width}) must be >= min_width ({min_width})")

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

    def render(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str | BorderStyle = "solid",
        width: int | None = None,
        padding: int = 1,
        align: AlignType = "left",
        min_width: int = 20,
        max_width: int = 100,
        content_color: str | None = None,
        border_color: str | None = None,
        title_color: str | None = None,
        gradient_start: str | None = None,
        gradient_end: str | None = None,
    ) -> list[str]:
        """Render a frame with the given content and configuration.

        Args:
            content: Text content (single line or list of lines)
            title: Optional title for the top border
            border: Border style name or BorderStyle object
            width: Frame width (auto-calculated if None)
            padding: Internal padding (left/right spaces)
            align: Content alignment ("left", "center", "right")
            min_width: Minimum frame width (when auto-calculating)
            max_width: Maximum frame width (when auto-calculating)
            content_color: Color for content text (hex, rgb, or CSS4 name)
            border_color: Color for border (hex, rgb, or CSS4 name)
            title_color: Color for title (hex, rgb, or CSS4 name)
            gradient_start: Starting color for content gradient (overrides content_color)
            gradient_end: Ending color for content gradient

        Returns:
            List of strings, one per line of the rendered frame

        Example:
            >>> renderer = FrameRenderer()
            >>> lines = renderer.render("Hello, World!", border="solid")
            >>> for line in lines:
            ...     print(line)
            ┌─────────────────┐
            │ Hello, World!   │
            └─────────────────┘
        """
        # Validate inputs
        self._validate_align(align)
        self._validate_dimensions(width, padding, min_width, max_width)
        self._validate_gradient_pair(gradient_start, gradient_end)

        frame = Frame(
            content=content,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            min_width=min_width,
            max_width=max_width,
            content_color=content_color,
            border_color=border_color,
            title_color=title_color,
            gradient_start=gradient_start,
            gradient_end=gradient_end,
        )
        return self.render_frame(frame)

    def render_frame(self, frame: Frame) -> list[str]:
        """Render a Frame dataclass into output lines.

        Args:
            frame: Frame configuration

        Returns:
            List of strings representing the rendered frame
        """
        # Get border style
        if isinstance(frame.border, str):
            style = get_border_style(frame.border)
        else:
            style = frame.border

        # Normalize content to list of lines
        if isinstance(frame.content, str):
            content_lines = frame.content.splitlines() if frame.content else [""]
        else:
            content_lines = frame.content if frame.content else [""]

        # Calculate frame width
        if frame.width is None:
            width = self._calculate_width(
                content_lines, frame.title, frame.padding, frame.min_width, frame.max_width
            )
        else:
            width = frame.width

        # Build frame output
        lines: list[str] = []

        # Top border with title
        top_border = style.render_top_border(width, frame.title)
        if frame.title_color and frame.title:
            # Color the title (and optionally the border)
            top_border = self._colorize_title_in_border(
                top_border, frame.title, frame.title_color, frame.border_color
            )
        elif frame.border_color:
            # Color only the border (no title color specified)
            top_border = self._colorize(top_border, frame.border_color)
        lines.append(top_border)

        # Content lines with padding
        for idx, line in enumerate(content_lines):
            content_line = self._render_content_line(style, line, width, frame.padding, frame.align)

            # Apply coloring
            if frame.gradient_start and frame.gradient_end:
                # Apply gradient
                t = idx / max(len(content_lines) - 1, 1)
                color = interpolate_color(frame.gradient_start, frame.gradient_end, t)
                # Color only the content part, not the borders
                content_line = self._colorize_content_in_line(
                    content_line, style, color, frame.border_color
                )
            elif frame.content_color:
                # Apply solid content color
                content_line = self._colorize_content_in_line(
                    content_line, style, frame.content_color, frame.border_color
                )
            elif frame.border_color:
                # Color only borders
                content_line = self._colorize_borders_in_line(
                    content_line, style, frame.border_color
                )

            lines.append(content_line)

        # Bottom border
        bottom_border = style.render_bottom_border(width)
        if frame.border_color:
            bottom_border = self._colorize(bottom_border, frame.border_color)
        lines.append(bottom_border)

        return lines

    def _calculate_width(
        self,
        content_lines: list[str],
        title: str | None,
        padding: int,
        min_width: int,
        max_width: int,
    ) -> int:
        """Calculate appropriate frame width based on content.

        Args:
            content_lines: List of content lines
            title: Optional title text
            padding: Padding amount
            min_width: Minimum allowed width
            max_width: Maximum allowed width

        Returns:
            Calculated width for the frame
        """
        # Find longest content line
        max_content_width = 0
        for line in content_lines:
            content_width = visual_width(line)
            if content_width > max_content_width:
                max_content_width = content_width

        # Account for borders (2 chars) + padding (both sides)
        needed_width = max_content_width + 2 + (padding * 2)

        # Check title width if present
        if title:
            # Title needs space for " title " + borders
            title_width = visual_width(title) + 2 + 2  # spaces + borders
            needed_width = max(needed_width, title_width)

        # Clamp to min/max
        return max(min_width, min(needed_width, max_width))

    def _render_content_line(
        self,
        style: BorderStyle,
        content: str,
        width: int,
        padding: int,
        align: AlignType,
    ) -> str:
        """Render a single content line with padding and alignment.

        Args:
            style: Border style to use
            content: Content text
            width: Total frame width
            padding: Padding amount
            align: Text alignment

        Returns:
            Rendered line with borders and padding
        """
        # Calculate available space for content
        # width = border(1) + content + border(1)
        inner_width = width - 2

        # Apply padding
        content_width = inner_width - (padding * 2)

        # Truncate if too long
        if visual_width(content) > content_width:
            content = truncate_to_width(content, content_width)

        # Apply alignment with padding
        if align == "left":
            padded = " " * padding + pad_to_width(content, content_width, "left") + " " * padding
        elif align == "right":
            padded = " " * padding + pad_to_width(content, content_width, "right") + " " * padding
        else:  # center
            # For center alignment, calculate padding and center the content
            content_vis_width = visual_width(content)
            remaining = content_width - content_vis_width
            left_pad = remaining // 2
            right_pad = remaining - left_pad
            padded = " " * padding + " " * left_pad + content + " " * right_pad + " " * padding

        # Render with borders
        return style.vertical + padded + style.vertical

    def _colorize(self, text: str, color: str) -> str:
        """Apply color to entire text.

        Args:
            text: Text to colorize
            color: Color specification (hex, rgb, or CSS4 name)

        Returns:
            ANSI colored text
        """
        r, g, b = parse_color(color)
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def _colorize_content_in_line(
        self, line: str, style: BorderStyle, content_color: str, border_color: str | None
    ) -> str:
        """Color content within a line, optionally coloring borders separately.

        Args:
            line: Full line with borders
            style: Border style
            content_color: Color for content
            border_color: Optional color for borders

        Returns:
            Colored line
        """
        # Split into: border | content | border
        left_border = style.vertical
        right_border = style.vertical
        content = line[len(left_border) : -len(right_border)]

        # Apply colors
        if border_color:
            left_colored = self._colorize(left_border, border_color)
            right_colored = self._colorize(right_border, border_color)
        else:
            left_colored = left_border
            right_colored = right_border

        content_colored = self._colorize(content, content_color)

        return left_colored + content_colored + right_colored

    def _colorize_borders_in_line(self, line: str, style: BorderStyle, border_color: str) -> str:
        """Color only the borders in a line.

        Args:
            line: Full line with borders
            style: Border style
            border_color: Color for borders

        Returns:
            Line with colored borders
        """
        left_border = style.vertical
        right_border = style.vertical
        content = line[len(left_border) : -len(right_border)]

        left_colored = self._colorize(left_border, border_color)
        right_colored = self._colorize(right_border, border_color)

        return left_colored + content + right_colored

    def _colorize_title_in_border(
        self, border_line: str, title: str, title_color: str, border_color: str | None
    ) -> str:
        """Color the title within a border line.

        Args:
            border_line: Full border line with title
            title: Title text
            title_color: Color for title
            border_color: Optional color for border

        Returns:
            Colored border line
        """
        # Find title in border line
        title_start = border_line.find(title)
        if title_start == -1:
            # Title not found, just color the whole border
            if border_color:
                return self._colorize(border_line, border_color)
            return border_line

        # Split into: border_before | title | border_after
        before = border_line[:title_start]
        after = border_line[title_start + len(title) :]

        # Apply colors
        if border_color:
            before_colored = self._colorize(before, border_color)
            after_colored = self._colorize(after, border_color)
        else:
            before_colored = before
            after_colored = after

        title_colored = self._colorize(title, title_color)

        return before_colored + title_colored + after_colored
