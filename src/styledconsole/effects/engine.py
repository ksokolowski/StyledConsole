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
    # Must specify color_system="truecolor" to preserve exact RGB colors,
    # otherwise Rich may downgrade to 256 or 16 colors based on environment
    buffer = StringIO()
    console = RichConsole(file=buffer, force_terminal=True, width=10000, color_system="truecolor")

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
        graphemes = split_graphemes(plain_text)

        current_idx = 0  # String index
        visual_col = 0  # Visual column index

        # Group adjacent characters with the same target color to minimize ANSI codes
        pending_style = None
        pending_start = 0
        pending_end = 0

        for grapheme in graphemes:
            g_len = len(grapheme)
            g_width = visual_width(grapheme)

            if g_width > 0:
                # Check is_border on the plain character
                is_border = row == 0 or row == total_rows - 1 or grapheme[0] in border_chars

                if target_filter.should_color(grapheme[0], is_border, row, visual_col):
                    position = position_strategy.calculate(row, visual_col, total_rows, max_col)
                    color = color_source.get_color(position)

                    if pending_style == color and pending_end == current_idx:
                        # Extend existing style range
                        pending_end += g_len
                    else:
                        # Apply previous pending style if any
                        if pending_style:
                            text.stylize(pending_style, pending_start, pending_end)

                        # Start new style range
                        pending_style = color
                        pending_start = current_idx
                        pending_end = current_idx + g_len
                else:
                    # Character should not be colored, apply pending style and reset
                    if pending_style:
                        text.stylize(pending_style, pending_start, pending_end)
                        pending_style = None

            current_idx += g_len
            visual_col += g_width

        # Apply final pending style
        if pending_style:
            text.stylize(pending_style, pending_start, pending_end)

        # 3. Render back to ANSI string
        console.print(text, end="")
        colored_lines.append(buffer.getvalue())
        buffer.seek(0)
        buffer.truncate()

    return colored_lines
