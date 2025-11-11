"""Mapping from StyledConsole border styles to Rich box styles.

This module provides compatibility between our legacy border names and Rich's
native box styles, allowing seamless transition to Rich Panel.
"""

from rich import box
from rich.box import Box

# Custom box style for THICK - uses block characters (█ ▀ ▄) for a bold, thick appearance
# Uses upper blocks (▀) for top, lower blocks (▄) for bottom for proper visual alignment
THICK_BOX = Box(
    "█▀██\n"  # top: blocks and upper half blocks
    "█ ██\n"  # head: full blocks with space for content
    "█▀██\n"  # head_row: blocks and upper half blocks
    "█ ██\n"  # mid: full blocks with space
    "█▀██\n"  # row: blocks and upper half blocks
    "█▄██\n"  # foot_row: blocks and lower half blocks (transition to bottom)
    "█ ██\n"  # foot: full blocks with space
    "█▄██\n"  # bottom: blocks and lower half blocks (sits at baseline)
)

# Custom box style for DOTS - uses periods for all characters
# Format: 8 lines, each with EXACTLY 4 characters (no spaces between them)
# Line 1: top (top_left, top, top_divider, top_right)
# Line 2: head (head_left, space, head_vertical, head_right)
# Line 3: head_row (head_row_left, head_row_horizontal, head_row_cross, head_row_right)
# Line 4: mid (mid_left, space, mid_vertical, mid_right)
# Line 5: row (row_left, row_horizontal, row_cross, row_right)
# Line 6: foot_row (foot_row_left, foot_row_horizontal, foot_row_cross, foot_row_right)
# Line 7: foot (foot_left, space, foot_vertical, foot_right)
# Line 8: bottom (bottom_left, bottom, bottom_divider, bottom_right)
DOTS_BOX = Box(
    "....\n"  # top: . . . .
    ". ..\n"  # head: . space . .
    "....\n"  # head_row: . . . .
    ". ..\n"  # mid: . space . .
    "....\n"  # row: . . . .
    "....\n"  # foot_row: . . . .
    ". ..\n"  # foot: . space . .
    "....\n"  # bottom: . . . .
)

# Map our border style names to Rich box styles
BORDER_TO_BOX = {
    "solid": box.SQUARE,
    "rounded": box.ROUNDED,
    "double": box.DOUBLE,
    "heavy": box.HEAVY,
    "thick": THICK_BOX,  # Custom thick style with heavy box drawing
    "ascii": box.ASCII,
    "minimal": box.MINIMAL,
    "dots": DOTS_BOX,  # Custom dotted style with periods
}


def get_box_style(border_name: str) -> box.Box:
    """Get Rich box style from border name.

    Args:
        border_name: Border style name (case-insensitive: solid, rounded, double, etc.)

    Returns:
        Rich Box instance for the requested style.

    Raises:
        ValueError: If border_name is not recognized.

    Example:
        >>> box_style = get_box_style("rounded")
        >>> # Use with Panel: Panel("content", box=box_style)
        >>> box_style = get_box_style("SOLID")  # Case insensitive
    """
    # Normalize to lowercase for case-insensitive matching
    border_name_lower = border_name.lower()

    if border_name_lower not in BORDER_TO_BOX:
        raise ValueError(
            f"Unknown border style: {border_name}. Valid options: {', '.join(BORDER_TO_BOX.keys())}"
        )
    return BORDER_TO_BOX[border_name_lower]
