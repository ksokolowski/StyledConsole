"""Mapping from StyledConsole border styles to Rich box styles.

This module provides compatibility between our legacy border names and Rich's
native box styles, allowing seamless transition to Rich Panel.
"""

from rich import box

# Map our border style names to Rich box styles
BORDER_TO_BOX = {
    "solid": box.SQUARE,
    "rounded": box.ROUNDED,
    "double": box.DOUBLE,
    "heavy": box.HEAVY,
    "thick": box.HEAVY,  # Alias for heavy
    "ascii": box.ASCII,
    "minimal": box.MINIMAL,
    "dots": box.ASCII,  # Fallback to ASCII for dots
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
