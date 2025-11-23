"""Unified gradient application engine.

Applies color gradients to frames using pluggable strategies for
position calculation, color generation, and target filtering.
"""

from styledconsole.core.gradient_utils import colorize
from styledconsole.effects.strategies import (
    ColorSource,
    PositionStrategy,
    TargetFilter,
)
from styledconsole.utils.text import strip_ansi, visual_width


def apply_gradient(
    lines: list[str],
    position_strategy: PositionStrategy,
    color_source: ColorSource,
    target_filter: TargetFilter,
    border_chars: set[str],
) -> list[str]:
    """Apply gradient to frame lines using pluggable strategies.

    This is the unified gradient engine that replaces duplicate functions.

    Args:
        lines: Frame lines (with ANSI codes)
        position_strategy: How to calculate position for each character
        color_source: What color to use at each position
        target_filter: Which characters to color (content, border, both)
        border_chars: Set of border characters for detection

    Returns:
        Colored frame lines
    """
    total_rows = len(lines)
    if not lines:
        return []

    # Calculate max width for normalization
    max_col = max(visual_width(strip_ansi(line)) for line in lines)

    colored_lines = []

    for row, line in enumerate(lines):
        clean_line = strip_ansi(line)  # Work with clean text
        colored_chars = []

        # We need to track visual column index because some chars might be wide (emojis)
        # But for now, let's assume 1 char = 1 col for the loop index,
        # and rely on the strategy to handle it if needed.
        # Actually, the strategies take 'col' which implies character index in the string.
        # Let's stick to the plan's logic which iterates over chars.

        for col, char in enumerate(clean_line):
            # Determine if this is a border character
            # We also consider the first and last rows as "border rows" generally,
            # but the specific check depends on the character.
            # The original logic often checked row index too.
            # Let's rely on the char check + row index check if needed,
            # but the plan says "is_border = char in border_chars".
            # Wait, the original logic had:
            # is_border_char = row_idx == 0 or row_idx == total_rows - 1 or char in border_chars
            # I should probably include the row check for robustness, or pass it to the filter?
            # The filter takes (char, is_border, row, col).
            # So I should determine 'is_border' here.

            is_border = row == 0 or row == total_rows - 1 or char in border_chars

            # Check if we should color this character
            if not target_filter.should_color(char, is_border, row, col):
                colored_chars.append(char)
                continue

            # Calculate position for this character
            position = position_strategy.calculate(row, col, total_rows, max_col)

            # Get color for this position
            color = color_source.get_color(position)

            # Colorize and append
            colored_chars.append(colorize(char, color))

        colored_lines.append("".join(colored_chars))

    return colored_lines
