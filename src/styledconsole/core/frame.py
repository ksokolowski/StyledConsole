"""Frame rendering with borders, padding, and titles.

This module provides high-level frame rendering that builds on BorderStyle primitives.
"""

from dataclasses import dataclass
from typing import Literal

from styledconsole.core.styles import BorderStyle, get_border_style
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
    """

    content: str | list[str]
    title: str | None = None
    border: str | BorderStyle = "solid"
    width: int | None = None
    padding: int = 1
    align: AlignType = "left"
    min_width: int = 20
    max_width: int = 100


class FrameRenderer:
    """Renders frames with borders, titles, and padding."""

    def __init__(self) -> None:
        """Initialize the frame renderer."""
        pass

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
        frame = Frame(
            content=content,
            title=title,
            border=border,
            width=width,
            padding=padding,
            align=align,
            min_width=min_width,
            max_width=max_width,
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
        lines.append(style.render_top_border(width, frame.title))

        # Content lines with padding
        for line in content_lines:
            lines.append(self._render_content_line(style, line, width, frame.padding, frame.align))

        # Bottom border
        lines.append(style.render_bottom_border(width))

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
