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

        i = 0
        line_len = len(clean_line)

        while i < line_len:
            char = clean_line[i]
            chars_consumed = 1

            # Build the complete emoji sequence by looking ahead for modifiers/joiners
            # We need to handle:
            # 1. VS16 (U+FE0F) - Variation Selector 16
            # 2. Skin Tones (U+1F3FB-U+1F3FF)
            # 3. ZWJ sequences (U+200D + following chars)
            # 4. Regional Indicators for flags (pairs of U+1F1E6-U+1F1FF)

            j = i + 1
            while j < line_len:
                next_char = clean_line[j]
                next_ord = ord(next_char)

                # Check for VS16
                if next_char == "\ufe0f":
                    char += next_char
                    chars_consumed += 1
                    j += 1
                    continue

                # Check for Skin Tone Modifiers (U+1F3FB to U+1F3FF)
                if 0x1F3FB <= next_ord <= 0x1F3FF:
                    char += next_char
                    chars_consumed += 1
                    j += 1
                    # After skin tone, check for VS16
                    if j < line_len and clean_line[j] == "\ufe0f":
                        char += clean_line[j]
                        chars_consumed += 1
                        j += 1
                    continue

                # Check for ZWJ (Zero-Width Joiner)
                if next_char == "\u200d":
                    # Consume ZWJ and the next character(s)
                    char += next_char
                    chars_consumed += 1
                    j += 1

                    # ZWJ is always followed by another emoji, consume it
                    if j < line_len:
                        char += clean_line[j]
                        chars_consumed += 1
                        j += 1

                        # Check for VS16 after the emoji following ZWJ
                        if j < line_len and clean_line[j] == "\ufe0f":
                            char += clean_line[j]
                            chars_consumed += 1
                            j += 1
                    continue

                # Check for Regional Indicator pairs (flags)
                # Regional Indicators: U+1F1E6 to U+1F1FF
                # If current char is a regional indicator and next is too, they form a flag
                curr_ord = ord(char[0] if len(char) == 1 else char[-1])
                if 0x1F1E6 <= curr_ord <= 0x1F1FF and 0x1F1E6 <= next_ord <= 0x1F1FF:
                    char += next_char
                    chars_consumed += 1
                    j += 1
                    continue

                # No more modifiers/joiners, break
                break

            # Determine if this is a border character
            # We check the base character (first char of sequence) against border_chars
            is_border = row == 0 or row == total_rows - 1 or char[0] in border_chars

            # Check if we should color this character
            # Note: We pass the column index 'i' which represents the character index.
            if not target_filter.should_color(char[0], is_border, row, i):
                colored_chars.append(char)
                i += chars_consumed
                continue

            # Calculate position for this character
            position = position_strategy.calculate(row, i, total_rows, max_col)

            # Get color for this position
            color = color_source.get_color(position)

            # Colorize and append the entire sequence
            colored_chars.append(colorize(char, color))

            i += chars_consumed

        colored_lines.append("".join(colored_chars))

    return colored_lines
