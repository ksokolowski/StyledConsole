"""Mapping from StyledConsole border styles to Rich box styles.

This module provides compatibility between our legacy border names and Rich's
native box styles, allowing seamless transition to Rich Panel.

Policy-aware: Use get_box_style_for_policy() to automatically fall back
to ASCII borders when policy.unicode=False.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich import box
from rich.box import Box

from styledconsole.core.registry import Registry

if TYPE_CHECKING:
    from styledconsole.policy import RenderPolicy

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

# Custom box style for ROUNDED_THICK - combines thick sides with thick rounded corners
# Uses thick rounded corners (╭╮╰╯) with thick block sides for visual consistency
ROUNDED_THICK_BOX = Box(
    "╭▀▀╮\n"  # top: thick rounded corners with upper half blocks
    "█ ██\n"  # head: full blocks with space for content
    "█▀▀█\n"  # head_row: blocks and upper half blocks
    "█ ██\n"  # mid: full blocks with space
    "█▀▀█\n"  # row: blocks and upper half blocks
    "█▄▄█\n"  # foot_row: blocks and lower half blocks
    "█ ██\n"  # foot: full blocks with space
    "╰▄▄╯\n"  # bottom: thick rounded corners with lower half blocks
)

# Custom box style for MINIMAL - simple top and bottom lines with no sides
# Uses spaces for sides and em-dash for top/bottom
MINIMAL_BOX = Box(
    " ── \n"  # top: space dash dash space
    "    \n"  # head: all spaces
    " ── \n"  # head_row: space dash dash space
    "    \n"  # mid: all spaces
    " ── \n"  # row: space dash dash space
    " ── \n"  # foot_row: space dash dash space
    "    \n"  # foot: all spaces
    " ── \n"  # bottom: space dash dash space
)

# Custom box style for DOTS - uses middle dots (·) for a lighter, more elegant appearance
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
    "····\n"  # top: · · · ·
    "· ··\n"  # head: · space · ·
    "····\n"  # head_row: · · · ·
    "· ··\n"  # mid: · space · ·
    "····\n"  # row: · · · ·
    "····\n"  # foot_row: · · · ·
    "· ··\n"  # foot: · space · ·
    "····\n"  # bottom: · · · ·
)


class BoxRegistry(Registry[Box]):
    """Registry for Rich box styles."""

    def __init__(self) -> None:
        super().__init__("box style")


# Registry mapping our border style names to Rich box styles
BORDER_TO_BOX = BoxRegistry()

# Register mappings
BORDER_TO_BOX.register("solid", box.SQUARE)
BORDER_TO_BOX.register("rounded", box.ROUNDED)
BORDER_TO_BOX.register("double", box.DOUBLE)
BORDER_TO_BOX.register("heavy", box.HEAVY)
BORDER_TO_BOX.register("thick", THICK_BOX)
BORDER_TO_BOX.register("rounded_thick", ROUNDED_THICK_BOX)
BORDER_TO_BOX.register("ascii", box.ASCII)
BORDER_TO_BOX.register("minimal", MINIMAL_BOX)
BORDER_TO_BOX.register("dots", DOTS_BOX)


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
    try:
        return BORDER_TO_BOX.get(border_name)
    except KeyError as e:
        raise ValueError(str(e)) from e


def get_box_style_for_policy(
    border_name: str,
    policy: RenderPolicy | None = None,
) -> box.Box:
    """Get Rich box style with policy-aware fallback.

    When policy.unicode=False, automatically returns ASCII box style
    regardless of the requested border style. This ensures graceful
    degradation on terminals that don't support Unicode.

    Args:
        border_name: Border style name (solid, rounded, double, etc.)
        policy: Optional RenderPolicy. If policy.unicode=False, returns ASCII.

    Returns:
        Rich Box instance (ASCII if unicode disabled, otherwise requested style).

    Example:
        >>> from styledconsole.policy import RenderPolicy
        >>> policy = RenderPolicy.minimal()  # unicode=False
        >>> get_box_style_for_policy("rounded", policy)
        <ASCII box>  # Falls back to ASCII
    """
    # If policy disables unicode, force ASCII borders
    if policy is not None and not policy.unicode:
        return box.ASCII

    return get_box_style(border_name)
