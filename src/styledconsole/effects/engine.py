"""Unified gradient application engine.

Applies color gradients to frames using pluggable strategies for
position calculation, color generation, and target filtering.
"""

from styledconsole.effects.strategies import (
    ColorSource,
    PositionStrategy,
    TargetFilter,
)
from styledconsole.utils.text import split_graphemes, strip_ansi, visual_width


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
    if not lines:
        return []

    from io import StringIO

    from rich.console import Console as RichConsole
    from rich.text import Text

    # Use a temporary console for rendering Text objects back to ANSI strings
    buffer = StringIO()
    console = RichConsole(file=buffer, force_terminal=True, width=10000)

    # Calculate max width for normalization using one pass over plain text
    # We can't use strip_ansi here because we want to use the Rich Text plain property later
    # but for max_width calculation, strip_ansi logic on original strings is fine/fastest for now
    total_rows = len(lines)
    max_col = max(visual_width(strip_ansi(line)) for line in lines)

    colored_lines = []

    for row, line in enumerate(lines):
        # 1. Parse line into Rich Text to preserve existing ANSI styles
        text = Text.from_ansi(line)
        plain_text = text.plain

        # 2. Iterate over graphemes (logical visual characters)
        # Note: text.plain does NOT contain ANSI codes, so split_graphemes works purely on unicode
        graphemes = split_graphemes(plain_text)

        current_idx = 0  # String index
        visual_col = 0  # Visual column index

        for grapheme in graphemes:
            g_len = len(grapheme)
            g_width = visual_width(grapheme)

            # If width is 0, it's likely a control char or zero-width joiner not handled by
            # split_graphemes logic? split_graphemes on plain text should return actual content.
            # However, if split_graphemes handles ANSI, but we passed plain text, it's fine.

            if g_width > 0:
                # Check is_border on the plain character
                is_border = row == 0 or row == total_rows - 1 or grapheme[0] in border_chars

                if target_filter.should_color(grapheme[0], is_border, row, visual_col):
                    position = position_strategy.calculate(row, visual_col, total_rows, max_col)
                    color = color_source.get_color(position)

                    # Apply color to the range in the Text object
                    # We use "color" style type. Rich handles hex codes.
                    text.stylize(color, current_idx, current_idx + g_len)

            current_idx += g_len
            visual_col += g_width

        # 3. Render back to ANSI string
        console.print(text, end="")
        colored_lines.append(buffer.getvalue())
        buffer.seek(0)
        buffer.truncate()

    return colored_lines
