"""Special visual effects for StyledConsole.

This module provides advanced visual effects like gradients and rainbow colors
for frames and other console output.

Available Effects:
- gradient_frame(): Vertical gradients (top to bottom)
- diagonal_gradient_frame(): Diagonal gradients (top-left to bottom-right)
- rainbow_frame(): 7-color rainbow spectrum (vertical or diagonal)

All functions support:
- target/mode: "content", "border", or "both"
- Auto-width calculation (when width=None)
- Custom border styles
- Safe emoji handling
"""

from __future__ import annotations

from io import StringIO
from typing import Literal

from styledconsole import Console
from styledconsole.core.gradient_utils import (
    colorize,
    get_rainbow_color,
)
from styledconsole.core.styles import get_border_style
from styledconsole.effects.engine import apply_gradient
from styledconsole.effects.strategies import (
    BorderOnly,
    Both,
    ContentOnly,
    DiagonalPosition,
    HorizontalPosition,
    LinearGradient,
    PositionStrategy,
    RainbowSpectrum,
    TargetFilter,
    VerticalPosition,
)
from styledconsole.utils.color import interpolate_color
from styledconsole.utils.text import strip_ansi

__all__ = [
    "diagonal_gradient_frame",
    "gradient_frame",
    "rainbow_cycling_frame",
    "rainbow_frame",
]


def _get_target_filter(target: str) -> TargetFilter:
    """Get target filter strategy from string."""
    if target == "content":
        return ContentOnly()
    elif target == "border":
        return BorderOnly()
    else:
        return Both()


def _get_border_chars(border_style: str) -> set[str]:
    """Get set of border characters for a style."""
    style = get_border_style(border_style)
    return {
        style.top_left,
        style.top_right,
        style.bottom_left,
        style.bottom_right,
        style.horizontal,
        style.vertical,
        style.left_joint,
        style.right_joint,
        style.top_joint,
        style.bottom_joint,
        style.cross,
    }


def gradient_frame(
    content: str | list[str],
    *,
    start_color: str = "cyan",
    end_color: str = "magenta",
    direction: Literal["vertical", "horizontal"] = "vertical",
    target: Literal["content", "border", "both"] = "content",
    title: str | None = None,
    border: str = "rounded",
    width: int | None = None,
    padding: int = 1,
    align: Literal["left", "center", "right"] = "left",
) -> list[str]:
    """Create a frame with gradient color effect.

    Args:
        content: Content to display in frame
        start_color: Starting color (CSS4 name or hex)
        end_color: Ending color (CSS4 name or hex)
        direction: Gradient direction ("vertical" or "horizontal")
        target: Apply gradient to "content", "border", or "both"
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines with gradient effect
    """
    # Normalize content
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

    # Render base frame
    buffer = StringIO()
    console = Console(file=buffer, detect_terminal=False, record=False)
    console.frame(
        content_lines,
        title=title,
        border=border,
        width=width,
        padding=padding,
        align=align,
    )
    lines = buffer.getvalue().splitlines()

    # Configure strategies
    pos_strategy: PositionStrategy = (
        VerticalPosition() if direction == "vertical" else HorizontalPosition()
    )
    color_source = LinearGradient(start_color, end_color)
    target_filter = _get_target_filter(target)
    border_chars = _get_border_chars(border)

    # Apply gradient
    return apply_gradient(lines, pos_strategy, color_source, target_filter, border_chars)


def diagonal_gradient_frame(
    content: str | list[str],
    *,
    start_color: str = "red",
    end_color: str = "blue",
    target: Literal["content", "border", "both"] = "both",
    title: str | None = None,
    border: str = "rounded",
    width: int | None = None,
    padding: int = 1,
    align: Literal["left", "center", "right"] = "left",
) -> list[str]:
    """Create a frame with diagonal gradient (top-left to bottom-right).

    Args:
        content: Content to display in frame
        start_color: Starting color at top-left
        end_color: Ending color at bottom-right
        target: Apply gradient to "content", "border", or "both"
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines with diagonal gradient effect
    """
    # Normalize content
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

    # Calculate width if needed (preserved from original logic for consistency)
    if width is None:
        from styledconsole.utils.text import visual_width as vw

        max_content_width = 0
        for line in content_lines:
            content_width = vw(line)
            if content_width > max_content_width:
                max_content_width = content_width

        needed_width = max_content_width + 2 + (padding * 2)
        if title:
            title_width = vw(title) + 4
            needed_width = max(needed_width, title_width)

        width = max(20, min(needed_width, 100))

    # Render base frame
    buffer = StringIO()
    console = Console(file=buffer, detect_terminal=False, record=False)
    console.frame(
        content_lines,
        title=title,
        border=border,
        width=width,
        padding=padding,
        align=align,
    )
    lines = buffer.getvalue().splitlines()

    # Configure strategies
    pos_strategy = DiagonalPosition()
    color_source = LinearGradient(start_color, end_color)
    target_filter = _get_target_filter(target)
    border_chars = _get_border_chars(border)

    # Apply gradient
    return apply_gradient(lines, pos_strategy, color_source, target_filter, border_chars)


def rainbow_frame(
    content: str | list[str],
    *,
    direction: Literal["vertical", "diagonal"] = "vertical",
    mode: Literal["content", "border", "both"] = "content",
    title: str | None = None,
    border: str = "rounded",
    width: int | None = None,
    padding: int = 1,
    align: Literal["left", "center", "right"] = "left",
) -> list[str]:
    """Create a frame with rainbow gradient effect.

    Args:
        content: Content to display in frame
        direction: Rainbow direction ("vertical" or "diagonal")
        mode: Apply rainbow to "content", "border", or "both"
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines with rainbow effect
    """
    # Normalize content
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

    # Render base frame
    buffer = StringIO()
    console = Console(file=buffer, detect_terminal=False, record=False)
    console.frame(
        content_lines,
        title=title,
        border=border,
        width=width,
        padding=padding,
        align=align,
    )
    lines = buffer.getvalue().splitlines()

    # Configure strategies
    pos_strategy: PositionStrategy = (
        VerticalPosition() if direction == "vertical" else DiagonalPosition()
    )
    color_source = RainbowSpectrum()
    target_filter = _get_target_filter(mode)
    border_chars = _get_border_chars(border)

    # Apply gradient
    return apply_gradient(lines, pos_strategy, color_source, target_filter, border_chars)


def rainbow_cycling_frame(
    content: str | list[str],
    *,
    border_gradient_start: str = "gold",
    border_gradient_end: str = "purple",
    title: str | None = None,
    border: str = "rounded",
    width: int | None = None,
    padding: int = 1,
    align: Literal["left", "center", "right"] = "left",
) -> list[str]:
    """Create a frame with cycling rainbow content and gradient borders.

    Args:
        content: Content to display in frame
        border_gradient_start: Start color for border gradient
        border_gradient_end: End color for border gradient
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines
    """
    # Normalize content
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

    # Render base frame
    buffer = StringIO()
    console = Console(file=buffer, detect_terminal=False, record=False)
    console.frame(
        content_lines,
        title=title,
        border=border,
        width=width,
        padding=padding,
        align=align,
    )
    lines = buffer.getvalue().splitlines()

    # We'll keep the original logic for this specific effect for now
    # as it has unique per-line cycling requirements that differ from
    # the standard gradient engine strategies.

    style = get_border_style(border)
    colored_lines = []
    content_line_count = 0

    for idx, line in enumerate(lines):
        clean = strip_ansi(line)

        # Calculate gradient position for borders (vertical gradient)
        position = idx / max(len(lines) - 1, 1)
        border_color = interpolate_color(border_gradient_start, border_gradient_end, position)

        # Check line type
        is_top_bottom_border = clean and clean[0] in {
            style.top_left,
            style.bottom_left,
            style.horizontal,
        }
        is_content_line = clean and clean[0] == style.vertical

        if is_top_bottom_border:
            # Top or bottom border - apply gradient
            colored_lines.append(colorize(clean, border_color))
        elif is_content_line:
            # Content line - rainbow cycling for content, gradient for borders
            left_border = clean[0]
            right_border = clean[-1]
            content_text = clean[len(left_border) : -len(right_border)]

            # Get cycling rainbow color (0-6 maps to ROYGBIV)
            rainbow_position = (content_line_count % 7) / 6.0
            content_color = get_rainbow_color(rainbow_position)
            content_line_count += 1

            # Combine: gradient borders + rainbow content
            colored_line = (
                colorize(left_border, border_color)
                + colorize(content_text, content_color)
                + colorize(right_border, border_color)
            )
            colored_lines.append(colored_line)
        else:
            colored_lines.append(line)

    return colored_lines
