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
from styledconsole.core.styles import get_border_style
from styledconsole.utils.color import interpolate_color, parse_color
from styledconsole.utils.text import strip_ansi, visual_width

__all__ = [
    "gradient_frame",
    "diagonal_gradient_frame",
    "rainbow_frame",
    "rainbow_cycling_frame",
]

# Rainbow color spectrum (7 colors: ROYGBIV)
# Using CSS4 color names for readability and consistency
RAINBOW_COLORS = [
    "red",  # #FF0000
    "orange",  # #FFA500
    "yellow",  # #FFFF00
    "lime",  # #00FF00 (bright green for rainbow spectrum)
    "blue",  # #0000FF
    "indigo",  # #4B0082
    "darkviolet",  # #9400D3
]


def _colorize(text: str, color: str) -> str:
    """Apply color to text using ANSI codes.

    Args:
        text: Text to colorize
        color: Color specification (hex, rgb, or CSS4 name)

    Returns:
        ANSI colored text
    """
    r, g, b = parse_color(color)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"


def get_rainbow_color(position: float) -> str:
    """Get rainbow color at a specific position.

    Args:
        position: Position in rainbow (0.0 = red, 1.0 = violet)

    Returns:
        Hex color code at that position in rainbow spectrum
    """
    position = max(0.0, min(1.0, position))
    num_segments = len(RAINBOW_COLORS) - 1
    segment_size = 1.0 / num_segments
    segment_index = min(int(position / segment_size), num_segments - 1)
    local_position = (position - segment_index * segment_size) / segment_size

    return interpolate_color(
        RAINBOW_COLORS[segment_index], RAINBOW_COLORS[segment_index + 1], local_position
    )


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
        direction: Gradient direction ("vertical" only for now)
        target: Apply gradient to "content", "border", or "both"
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines with gradient effect

    Example:
        >>> from styledconsole.effects import gradient_frame
        >>> lines = gradient_frame(
        ...     ["Line 1", "Line 2", "Line 3"],
        ...     start_color="red",
        ...     end_color="blue",
        ...     target="content"
        ... )
    """
    if direction == "horizontal":
        raise NotImplementedError("Horizontal gradients not yet implemented")

    # Normalize content to list
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

    # Get border style
    style = get_border_style(border)

    # Build frame using Console.frame()
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

    # Get rendered lines
    lines = buffer.getvalue().splitlines()

    # Apply vertical gradient
    if target in ("content", "both"):
        # For "both", also color the vertical borders
        color_vertical_borders = target == "both"
        lines = _apply_vertical_content_gradient(
            lines, start_color, end_color, style, color_vertical_borders
        )

    if target in ("border", "both"):
        lines = _apply_vertical_border_gradient(lines, start_color, end_color, border, title)

    return lines


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
        start_color: Starting color at top-left (CSS4 name or hex)
        end_color: Ending color at bottom-right (CSS4 name or hex)
        target: Apply gradient to "content", "border", or "both"
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines with diagonal gradient effect

    Example:
        >>> from styledconsole.effects import diagonal_gradient_frame
        >>> lines = diagonal_gradient_frame(
        ...     ["Top-left", "Center", "Bottom-right"],
        ...     start_color="lime",
        ...     end_color="magenta",
        ...     target="both"
        ... )

    Note:
        Diagonal gradients work best with simple emojis. Avoid emojis with
        variation selectors (like ↘️) as they may cause alignment issues.
        Use base emojis instead (like ↘).
    """
    # Normalize content to list
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

    # Get border style
    style = get_border_style(border)

    # Calculate width if not provided
    if width is None:
        from styledconsole.utils.text import visual_width as vw

        # Find longest content line
        max_content_width = 0
        for line in content_lines:
            content_width = vw(line)
            if content_width > max_content_width:
                max_content_width = content_width

        # Account for borders (2 chars) + padding (both sides)
        needed_width = max_content_width + 2 + (padding * 2)

        # Check title width if present
        if title:
            # Title needs space for " title " + borders
            title_width = vw(title) + 2 + 2  # spaces + borders
            needed_width = max(needed_width, title_width)

        # Clamp to min/max (20 to 100)
        width = max(20, min(needed_width, 100))

    # Build frame without colors using Console.frame()
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

    # Get rendered lines
    lines = buffer.getvalue().splitlines()

    # Apply diagonal gradient character-by-character
    apply_to_border = target in ("border", "both")
    apply_to_content = target in ("content", "both")

    colored_lines = _apply_diagonal_gradient(
        lines, start_color, end_color, style, title, apply_to_border, apply_to_content
    )

    return colored_lines


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

    Uses a 7-color rainbow spectrum (red → orange → yellow → green →
    blue → indigo → violet), interpolating through ALL colors instead
    of just red to violet.

    Args:
        content: Content to display in frame
        direction: Rainbow direction - "vertical" (top to bottom) or
                   "diagonal" (top-left to bottom-right)
        mode: Apply rainbow to "content", "border", or "both"
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines with rainbow effect

    Example:
        >>> from styledconsole.effects import rainbow_frame
        >>> # Vertical rainbow
        >>> lines = rainbow_frame(
        ...     ["Red", "Orange", "Yellow", "Green", "Blue"],
        ...     direction="vertical",
        ...     mode="both"
        ... )
        >>> # Diagonal rainbow
        >>> lines = rainbow_frame(
        ...     ["Content line 1", "Content line 2"],
        ...     direction="diagonal",
        ...     mode="both"
        ... )
    """
    # Build base frame using Console.frame()
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

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

    # Get rendered lines
    lines = buffer.getvalue().splitlines()

    # Apply rainbow using get_rainbow_color for proper ROYGBIV spectrum
    if direction == "vertical":
        lines = _apply_vertical_rainbow(lines, mode, border, title)
    else:  # diagonal
        style = get_border_style(border)
        apply_to_border = mode in ("border", "both")
        apply_to_content = mode in ("content", "both")
        lines = _apply_diagonal_rainbow(lines, style, title, apply_to_border, apply_to_content)

    return lines


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

    Each content line cycles through the 7-color ROYGBIV spectrum:
    - Line 1: Red, Line 2: Orange, Line 3: Yellow, etc.
    - After violet (line 7), cycles back to red (line 8)

    Borders use a vertical gradient (top to bottom) with custom colors.

    This creates a unique effect where:
    - Content: Rainbow colors cycling per line (discrete colors)
    - Borders: Smooth gradient from start to end color

    Args:
        content: Content to display in frame
        border_gradient_start: Start color for border gradient (default: gold)
        border_gradient_end: End color for border gradient (default: purple)
        title: Optional frame title
        border: Border style name
        width: Frame width (auto-calculated if None)
        padding: Padding around content
        align: Text alignment

    Returns:
        List of rendered lines with cycling rainbow content and gradient borders

    Example:
        >>> from styledconsole.effects import rainbow_cycling_frame
        >>> lines = rainbow_cycling_frame(
        ...     ["Line 1 (Red)", "Line 2 (Orange)", "Line 3 (Yellow)",
        ...      "Line 4 (Green)", "Line 5 (Blue)", "Line 6 (Indigo)",
        ...      "Line 7 (Violet)", "Line 8 (Red again)"],
        ...     border_gradient_start="gold",
        ...     border_gradient_end="purple",
        ...     border="heavy"
        ... )
    """
    from io import StringIO

    from styledconsole.console import Console
    from styledconsole.core.styles import get_border_style
    from styledconsole.utils.color import interpolate_color
    from styledconsole.utils.text import strip_ansi

    # Build base frame
    if isinstance(content, str):
        content_lines = content.splitlines() if content else [""]
    else:
        content_lines = content if content else [""]

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

    # Get rendered lines
    lines = buffer.getvalue().splitlines()
    style = get_border_style(border)
    colored_lines = []
    content_line_count = 0  # Track content lines for cycling

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
            colored_lines.append(_colorize(clean, border_color))
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
                _colorize(left_border, border_color)
                + _colorize(content_text, content_color)
                + _colorize(right_border, border_color)
            )
            colored_lines.append(colored_line)
        else:
            # Other lines (shouldn't happen, but preserve as-is)
            colored_lines.append(line)

    return colored_lines


# Internal helper functions


def _apply_vertical_content_gradient(
    lines: list[str],
    start_color: str,
    end_color: str,
    border_style,
    color_vertical_borders: bool = False,
) -> list[str]:
    """Apply vertical gradient to content lines.

    Args:
        lines: Frame lines including borders
        start_color: Starting color
        end_color: Ending color
        border_style: BorderStyle object for border character detection
        color_vertical_borders: If True, also color left/right vertical borders (for target="both")

    Returns:
        Lines with gradient applied to content (and optionally vertical borders)
    """
    if len(lines) <= 2:  # Only borders, no content
        return lines

    colored_lines = [lines[0]]  # Keep top border as-is

    # Color content lines (skip first and last which are borders)
    content_lines = lines[1:-1]
    for idx, line in enumerate(content_lines):
        position = idx / max(len(content_lines) - 1, 1)
        color = interpolate_color(start_color, end_color, position)

        # Extract and color the content part (not the border characters)
        left_border = border_style.vertical
        right_border = border_style.vertical

        # Split: left border | content | right border
        if len(line) > len(left_border) + len(right_border):
            content = line[len(left_border) : -len(right_border)]
            content_colored = _colorize(content, color)

            # Color vertical borders if requested (for target="both")
            if color_vertical_borders:
                left_border_colored = _colorize(left_border, color)
                right_border_colored = _colorize(right_border, color)
                colored_line = left_border_colored + content_colored + right_border_colored
            else:
                colored_line = left_border + content_colored + right_border
        else:
            # Safety: if line is too short, just keep it as-is
            colored_line = line

        colored_lines.append(colored_line)

    colored_lines.append(lines[-1])  # Keep bottom border as-is

    return colored_lines


def _apply_vertical_border_gradient(
    lines: list[str], start_color: str, end_color: str, border: str, title: str | None
) -> list[str]:
    """Apply vertical gradient to border lines."""
    style = get_border_style(border)
    colored_lines = []

    for idx, line in enumerate(lines):
        position = idx / max(len(lines) - 1, 1)
        color = interpolate_color(start_color, end_color, position)

        # For borders, we need to detect and color only border characters
        # For now, simple approach: check if line starts with border character
        if line.strip() and line.lstrip()[0] in {
            style.top_left,
            style.top_right,
            style.bottom_left,
            style.bottom_right,
            style.vertical,
        }:
            # This is a border line - color it
            colored_lines.append(_colorize(line, color))
        else:
            # Content line - keep as is (already colored if content gradient applied)
            colored_lines.append(line)

    return colored_lines


def _apply_diagonal_gradient(
    lines: list[str],
    start_color: str,
    end_color: str,
    style,
    title: str | None,
    apply_to_border: bool,
    apply_to_content: bool,
) -> list[str]:
    """Apply diagonal gradient (top-left to bottom-right) character-by-character."""
    total_rows = len(lines)
    max_col = max(visual_width(strip_ansi(line)) for line in lines)

    # Define border characters for detection
    border_chars = {
        style.top_left,
        style.top_right,
        style.bottom_left,
        style.bottom_right,
        style.horizontal,
        style.vertical,
        style.top_joint,
        style.bottom_joint,
        style.left_joint,
        style.right_joint,
        style.cross,
    }

    colored_lines = []
    for row_idx, line in enumerate(lines):
        # Strip ANSI codes to work with clean text
        clean_line = strip_ansi(line)

        # Special handling for title line (first line with title)
        if row_idx == 0 and title:
            colored_line = ""
            visual_col = 0
            i = 0

            while i < len(clean_line):
                char = clean_line[i]

                # Calculate position
                row_progress = row_idx / max(total_rows - 1, 1)
                col_progress = visual_col / max(max_col - 1, 1)
                diagonal_position = (row_progress + col_progress) / 2.0
                char_color = interpolate_color(start_color, end_color, diagonal_position)

                # Check if we're at the title position
                if title in clean_line[i : i + len(title) + 2]:  # +2 for spaces
                    # We're at the title - color title if content coloring is on
                    if apply_to_content:
                        # Color the title portion
                        title_part = clean_line[i : i + len(title) + 2]
                        for tc in title_part:
                            tc_progress = visual_col / max(max_col - 1, 1)
                            tc_position = (row_progress + tc_progress) / 2.0
                            tc_color = interpolate_color(start_color, end_color, tc_position)
                            colored_line += _colorize(tc, tc_color)
                            visual_col += 1
                        i += len(title_part)
                    else:
                        # Keep title as-is
                        colored_line += clean_line[i : i + len(title) + 2]
                        visual_col += len(title) + 2
                        i += len(title) + 2
                    continue

                # Regular border character
                if apply_to_border and char in border_chars:
                    colored_line += _colorize(char, char_color)
                else:
                    colored_line += char

                visual_col += 1
                i += 1

            colored_lines.append(colored_line)
        else:
            # Regular line without title
            colored_chars = []
            visual_col = 0

            for char in clean_line:
                # Calculate diagonal position (0.0 to 1.0)
                row_progress = row_idx / max(total_rows - 1, 1)
                col_progress = visual_col / max(max_col - 1, 1)
                diagonal_position = (row_progress + col_progress) / 2.0

                # Get color for this position
                char_color = interpolate_color(start_color, end_color, diagonal_position)

                # Determine if this is border or content character
                is_border_char = row_idx == 0 or row_idx == total_rows - 1 or char in border_chars

                # Apply color based on settings
                if (is_border_char and apply_to_border) or (
                    not is_border_char and apply_to_content
                ):
                    colored_chars.append(_colorize(char, char_color))
                else:
                    colored_chars.append(char)

                # Update visual column position
                visual_col += 1

            colored_lines.append("".join(colored_chars))

    return colored_lines


def _apply_vertical_rainbow(
    lines: list[str], mode: str, border: str, title: str | None
) -> list[str]:
    """Apply vertical rainbow effect (proper ROYGBIV spectrum)."""
    colored_lines = []
    num_lines = len(lines)

    style = get_border_style(border)

    for idx, line in enumerate(lines):
        # Calculate position in rainbow (0.0 to 1.0)
        position = idx / max(num_lines - 1, 1)
        color = get_rainbow_color(position)

        # Check if this is a border line
        clean = strip_ansi(line)
        is_top_bottom_border = clean and clean[0] in {
            style.top_left,
            style.bottom_left,
            style.horizontal,
        }
        is_content_line = clean and clean[0] == style.vertical

        if is_top_bottom_border:
            # Top or bottom border
            if mode in ("border", "both"):
                colored_lines.append(_colorize(clean, color))
            else:
                colored_lines.append(line)
        elif is_content_line:
            # Content line with vertical borders
            left_border = clean[0]
            right_border = clean[-1]
            content = clean[len(left_border) : -len(right_border)]

            if mode == "content":
                # Color content only
                colored_line = left_border + _colorize(content, color) + right_border
            elif mode == "border":
                # Color borders only
                colored_line = (
                    _colorize(left_border, color) + content + _colorize(right_border, color)
                )
            else:  # both
                # Color everything
                colored_line = (
                    _colorize(left_border, color)
                    + _colorize(content, color)
                    + _colorize(right_border, color)
                )

            colored_lines.append(colored_line)
        else:
            colored_lines.append(line)

    return colored_lines


def _apply_diagonal_rainbow(
    lines: list[str],
    style,
    title: str | None,
    apply_to_border: bool,
    apply_to_content: bool,
) -> list[str]:
    """Apply diagonal rainbow effect (proper ROYGBIV spectrum)."""
    total_rows = len(lines)
    max_col = max(visual_width(strip_ansi(line)) for line in lines)

    # Define border characters for detection
    border_chars = {
        style.top_left,
        style.top_right,
        style.bottom_left,
        style.bottom_right,
        style.horizontal,
        style.vertical,
        style.top_joint,
        style.bottom_joint,
        style.left_joint,
        style.right_joint,
        style.cross,
    }

    colored_lines = []
    for row_idx, line in enumerate(lines):
        # Strip ANSI codes to work with clean text
        clean_line = strip_ansi(line)

        # Calculate row progress for diagonal
        row_progress = row_idx / max(total_rows - 1, 1)

        colored_chars = []
        visual_col = 0
        i = 0

        while i < len(clean_line):
            char = clean_line[i]
            i += 1

            # Calculate diagonal position (0.0 at top-left, 1.0 at bottom-right)
            col_progress = visual_col / max(max_col - 1, 1)
            diagonal_position = (row_progress + col_progress) / 2.0

            # Get rainbow color for this position
            char_color = get_rainbow_color(diagonal_position)

            # Check if this is a border character
            is_border_char = char in border_chars

            # Apply color based on settings
            if (is_border_char and apply_to_border) or (not is_border_char and apply_to_content):
                colored_chars.append(_colorize(char, char_color))
            else:
                colored_chars.append(char)

            # Update visual column position
            visual_col += 1

        colored_lines.append("".join(colored_chars))

    return colored_lines
