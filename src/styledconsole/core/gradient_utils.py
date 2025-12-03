"""Gradient application utilities for StyledConsole.

This module provides helper functions for applying gradients to text lines,
extracted from effects.py to allow reuse in RenderingEngine.

Policy-aware: All colorization functions accept an optional `policy` parameter.
When policy.color=False, functions return plain text without ANSI codes.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import TYPE_CHECKING

from styledconsole.core.styles import BorderStyle, get_border_style
from styledconsole.utils.color import interpolate_color, parse_color
from styledconsole.utils.text import strip_ansi, visual_width

if TYPE_CHECKING:
    from styledconsole.policy import RenderPolicy

# Regex for ANSI escape codes
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_trailing_ansi(text: str) -> str:
    """Remove ANSI escape codes from the end of the string."""
    return re.sub(r"(\x1b\[[0-9;]*m)+$", "", text)


# Rainbow color spectrum (7 colors: ROYGBIV)
RAINBOW_COLORS = [
    "red",  # #FF0000
    "orange",  # #FFA500
    "yellow",  # #FFFF00
    "lime",  # #00FF00 (bright green for rainbow spectrum)
    "blue",  # #0000FF
    "indigo",  # #4B0082
    "darkviolet",  # #9400D3
]


def colorize(text: str, color: str, policy: RenderPolicy | None = None) -> str:
    """Apply color to text using ANSI codes.

    Handles nested ANSI resets by re-applying the outer color after any
    internal reset codes (\033[0m).

    Policy-aware: returns plain text when policy.color=False.

    Args:
        text: Text to colorize
        color: Color specification (hex, rgb, or CSS4 name)
        policy: Optional RenderPolicy. If policy.color=False, returns text unchanged.

    Returns:
        ANSI colored text (or plain text if color disabled)
    """
    # Check policy - skip colorization if color is disabled
    if policy is not None and not policy.color:
        return text

    r, g, b = parse_color(color)
    start_sequence = f"\033[38;2;{r};{g};{b}m"
    reset_sequence = "\033[0m"

    # If the text contains reset codes, we need to re-apply our color after them
    # so the gradient continues.
    # We look for standard ANSI reset codes.
    if reset_sequence in text:
        # Replace reset with reset + our color
        # This ensures we reset everything (including background/bold etc from inner)
        # but then immediately re-establish our foreground color.
        text = text.replace(reset_sequence, reset_sequence + start_sequence)

    return f"{start_sequence}{text}{reset_sequence}"


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


def apply_vertical_content_gradient(
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

        # Remove trailing ANSI codes to correctly find the end of the string
        # This prevents slicing into an ANSI code if the line ends with one
        clean_line_end = strip_trailing_ansi(line)

        # Split: left border | content | right border
        if len(clean_line_end) > len(left_border) + len(right_border):
            # Slice from the cleaned line end to ensure we don't cut ANSI codes
            # But we need to preserve the original line's content (which might have ANSI)
            # The issue is that line[-1] might be part of an ANSI code.
            # So we use clean_line_end to determine the length to slice.

            # Actually, we want to slice the *original* line, but using indices derived from
            # the visual structure.
            # If clean_line_end ends with the border char, we can slice it off.

            # Let's assume the border is at the very end of clean_line_end.
            # content = clean_line_end[len(left_border) : -len(right_border)]
            # But wait, clean_line_end has stripped ANSI from the END.
            # It might still have ANSI in the middle.

            content = clean_line_end[len(left_border) : -len(right_border)]
            content_colored = colorize(content, color)

            # Color vertical borders if requested (for target="both")
            if color_vertical_borders:
                left_border_colored = colorize(left_border, color)
                right_border_colored = colorize(right_border, color)
                colored_line = left_border_colored + content_colored + right_border_colored
            else:
                colored_line = left_border + content_colored + right_border
        else:
            # Safety: if line is too short, just keep it as-is
            colored_line = line

        colored_lines.append(colored_line)

    colored_lines.append(lines[-1])  # Keep bottom border as-is

    return colored_lines


def _colorize_line_with_ansi(
    line: str,
    color: str,
    should_color_func: Callable[[str, int, int], bool],
    policy: RenderPolicy | None = None,
) -> str:
    """Colorize a line while preserving ANSI codes, based on a predicate function.

    Policy-aware: returns line unchanged when policy.color=False.

    Args:
        line: The text line to colorize (may contain ANSI codes)
        color: The color to apply
        should_color_func: Predicate function(char, visible_index, total_visible_length)
                           that returns True if the character should be colored.
        policy: Optional RenderPolicy. If policy.color=False, returns line unchanged.

    Returns:
        Colorized line with ANSI codes preserved (or plain line if color disabled)
    """
    # Check policy - skip colorization if color is disabled
    if policy is not None and not policy.color:
        return line
    # Split into segments (text vs ansi)
    segments = []
    pos = 0
    for match in ANSI_RE.finditer(line):
        if match.start() > pos:
            segments.append(("text", line[pos : match.start()]))
        segments.append(("ansi", match.group()))
        pos = match.end()
    if pos < len(line):
        segments.append(("text", line[pos:]))

    result_parts = []
    visible_idx = 0
    clean_line = strip_ansi(line)
    total_visible = len(clean_line)

    for seg_type, seg_content in segments:
        if seg_type == "ansi":
            result_parts.append(seg_content)
        else:
            # Process text segment: group contiguous characters by color status
            current_group = []
            current_should_color = None

            for char in seg_content:
                should_color = should_color_func(char, visible_idx, total_visible)

                if current_should_color is None:
                    current_should_color = should_color
                    current_group.append(char)
                elif should_color == current_should_color:
                    current_group.append(char)
                else:
                    # Flush current group
                    text_chunk = "".join(current_group)
                    if current_should_color:
                        result_parts.append(colorize(text_chunk, color, policy))
                    else:
                        result_parts.append(text_chunk)
                    # Start new group
                    current_group = [char]
                    current_should_color = should_color

                visible_idx += 1

            # Flush remaining group
            if current_group:
                text_chunk = "".join(current_group)
                if current_should_color:
                    result_parts.append(colorize(text_chunk, color, policy))
                else:
                    result_parts.append(text_chunk)

    return "".join(result_parts)


def apply_vertical_border_gradient(
    lines: list[str],
    start_color: str,
    end_color: str,
    border: str,
    title: str | None,
    policy: RenderPolicy | None = None,
) -> list[str]:
    """Apply vertical gradient to border characters only.

    This function colors only the actual border characters (top/bottom borders,
    vertical borders) without affecting the content, which may already have
    ANSI formatting from Rich's Text markup.

    Policy-aware: returns lines unchanged when policy.color=False.

    Args:
        lines: The text lines to colorize
        start_color: Start color for the gradient
        end_color: End color for the gradient
        border: Border style name
        title: Optional title (unused but kept for API compatibility)
        policy: Optional RenderPolicy. If policy.color=False, returns lines unchanged.

    Returns:
        Colorized lines (or original lines if color disabled)
    """
    # Check policy - skip colorization if color is disabled
    if policy is not None and not policy.color:
        return lines

    style = get_border_style(border)
    border_chars = get_border_chars(style)
    colored_lines = []

    for idx, line in enumerate(lines):
        position = idx / max(len(lines) - 1, 1)
        color = interpolate_color(start_color, end_color, position)

        clean_line = strip_ansi(line)

        # Detect line type
        # We check if it starts with a corner or vertical bar
        is_top = clean_line.startswith(style.top_left)
        is_bottom = clean_line.startswith(style.bottom_left)
        is_vertical = clean_line.startswith(style.vertical)

        if is_top or is_bottom:
            # Top or bottom border (possibly with title)
            # Color all characters that are part of the border set
            colored_lines.append(
                _colorize_line_with_ansi(line, color, lambda c, i, t: c in border_chars, policy)
            )
        elif is_vertical:
            # Content line with vertical borders
            # Color only the first and last visible characters
            colored_lines.append(
                _colorize_line_with_ansi(line, color, lambda c, i, t: i == 0 or i == t - 1, policy)
            )
        else:
            # Not a border line (e.g. empty or just content?)
            colored_lines.append(line)

    return colored_lines


def calculate_diagonal_position(
    row_idx: int, visual_col: int, total_rows: int, max_col: int
) -> float:
    """Calculate diagonal gradient position (0.0 to 1.0) for a character."""
    row_progress = row_idx / max(total_rows - 1, 1)
    col_progress = visual_col / max(max_col - 1, 1)
    return (row_progress + col_progress) / 2.0


def get_border_chars(style: BorderStyle) -> set[str]:
    """Extract all border characters from a style for efficient lookup.

    Args:
        style: BorderStyle instance to extract characters from

    Returns:
        Set of all border characters used by the style
    """
    chars = {
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
    # Special case for THICK style which uses lower half block for bottom border
    if style.horizontal == "▀":
        chars.add("▄")
    return chars


def process_title_in_line(
    clean_line: str,
    title: str,
    row_idx: int,
    total_rows: int,
    max_col: int,
    start_color: str,
    end_color: str,
    border_chars: set,
    apply_to_border: bool,
    apply_to_content: bool,
) -> str:
    """Process a line containing the title, applying gradient selectively."""
    colored_line = ""
    visual_col = 0
    i = 0

    while i < len(clean_line):
        char = clean_line[i]

        # Calculate color for current position
        diagonal_position = calculate_diagonal_position(row_idx, visual_col, total_rows, max_col)
        char_color = interpolate_color(start_color, end_color, diagonal_position)

        # Check if we're at the title position
        if title in clean_line[i : i + len(title) + 2]:  # +2 for spaces
            title_part = clean_line[i : i + len(title) + 2]

            if apply_to_content:
                # Color the title portion character by character
                for tc in title_part:
                    tc_position = calculate_diagonal_position(
                        row_idx, visual_col, total_rows, max_col
                    )
                    tc_color = interpolate_color(start_color, end_color, tc_position)
                    colored_line += colorize(tc, tc_color)
                    visual_col += 1
            else:
                # Keep title as-is
                colored_line += title_part
                visual_col += len(title_part)

            i += len(title_part)
            continue

        # Regular border character
        if apply_to_border and char in border_chars:
            colored_line += colorize(char, char_color)
        else:
            colored_line += char

        visual_col += 1
        i += 1

    return colored_line


def process_regular_line(
    clean_line: str,
    row_idx: int,
    total_rows: int,
    max_col: int,
    start_color: str,
    end_color: str,
    border_chars: set,
    apply_to_border: bool,
    apply_to_content: bool,
) -> str:
    """Process a regular line (no title) with gradient coloring."""
    colored_chars = []
    visual_col = 0

    for char in clean_line:
        # Calculate color for this position
        diagonal_position = calculate_diagonal_position(row_idx, visual_col, total_rows, max_col)
        char_color = interpolate_color(start_color, end_color, diagonal_position)

        # Determine if this is border or content character
        is_border_char = row_idx == 0 or row_idx == total_rows - 1 or char in border_chars

        # Apply color based on settings
        if (is_border_char and apply_to_border) or (not is_border_char and apply_to_content):
            colored_chars.append(colorize(char, char_color))
        else:
            colored_chars.append(char)

        visual_col += 1

    return "".join(colored_chars)


def apply_diagonal_gradient(
    lines: list[str],
    start_color: str,
    end_color: str,
    style: BorderStyle,
    title: str | None,
    apply_to_border: bool,
    apply_to_content: bool,
) -> list[str]:
    """Apply diagonal gradient (top-left to bottom-right) character-by-character."""
    total_rows = len(lines)
    max_col = max(visual_width(strip_ansi(line)) for line in lines)
    border_chars = get_border_chars(style)

    colored_lines = []
    for row_idx, line in enumerate(lines):
        clean_line = strip_ansi(line)

        # Special handling for title line (first line with title)
        if row_idx == 0 and title:
            colored_line = process_title_in_line(
                clean_line,
                title,
                row_idx,
                total_rows,
                max_col,
                start_color,
                end_color,
                border_chars,
                apply_to_border,
                apply_to_content,
            )
        else:
            colored_line = process_regular_line(
                clean_line,
                row_idx,
                total_rows,
                max_col,
                start_color,
                end_color,
                border_chars,
                apply_to_border,
                apply_to_content,
            )

        colored_lines.append(colored_line)

    return colored_lines


def apply_vertical_rainbow(
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
                colored_lines.append(colorize(clean, color))
            else:
                colored_lines.append(line)
        elif is_content_line:
            # Content line with vertical borders
            left_border = clean[0]
            right_border = clean[-1]
            content = clean[len(left_border) : -len(right_border)]

            if mode == "content":
                # Color content only
                colored_line = left_border + colorize(content, color) + right_border
            elif mode == "border":
                # Color borders only
                colored_line = (
                    colorize(left_border, color) + content + colorize(right_border, color)
                )
            else:  # both
                # Color everything
                colored_line = (
                    colorize(left_border, color)
                    + colorize(content, color)
                    + colorize(right_border, color)
                )

            colored_lines.append(colored_line)
        else:
            colored_lines.append(line)

    return colored_lines


def apply_diagonal_rainbow(
    lines: list[str],
    style: BorderStyle,
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
                colored_chars.append(colorize(char, char_color))
            else:
                colored_chars.append(char)

            # Update visual column position
            visual_col += 1

        colored_lines.append("".join(colored_chars))

    return colored_lines
