"""Border style definitions and rendering utilities.

This module provides predefined border styles using Unicode box-drawing characters
and ASCII fallbacks, along with helper functions for rendering borders.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class BorderStyle:
    """Represents a border style with Unicode box-drawing characters.

    Attributes:
        name: Human-readable name of the border style
        top_left: Top-left corner character
        top_right: Top-right corner character
        bottom_left: Bottom-left corner character
        bottom_right: Bottom-right corner character
        horizontal: Horizontal line character
        vertical: Vertical line character
        left_joint: Left T-junction character (for titles/dividers)
        right_joint: Right T-junction character (for titles/dividers)
        top_joint: Top T-junction character
        bottom_joint: Bottom T-junction character
        cross: Cross/plus junction character (intersection)
    """

    name: str
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    horizontal: str
    vertical: str
    left_joint: str
    right_joint: str
    top_joint: str
    bottom_joint: str
    cross: str

    def render_horizontal(self, width: int, char: str | None = None) -> str:
        """Render a horizontal line of specified width.

        Args:
            width: Width of the line in characters
            char: Optional character to use (defaults to style's horizontal char)

        Returns:
            Horizontal line string

        Example:
            >>> style = BORDERS["solid"]
            >>> style.render_horizontal(10)
            '──────────'
        """
        character = char if char is not None else self.horizontal
        return character * width

    def render_vertical(self, height: int, char: str | None = None) -> list[str]:
        """Render a vertical line of specified height.

        Args:
            height: Height of the line in rows
            char: Optional character to use (defaults to style's vertical char)

        Returns:
            List of strings, one per line

        Example:
            >>> style = BORDERS["solid"]
            >>> lines = style.render_vertical(3)
            >>> lines
            ['│', '│', '│']
        """
        character = char if char is not None else self.vertical
        return [character] * height

    def render_top_border(self, width: int, title: str | None = None) -> str:
        """Render top border with optional centered title.

        Args:
            width: Total width of the border (including corners)
            title: Optional title text to center in the border

        Returns:
            Top border string with title if provided

        Example:
            >>> style = BORDERS["solid"]
            >>> style.render_top_border(20)
            '┌──────────────────┐'
            >>> style.render_top_border(20, "Title")
            '┌───── Title ──────┐'
        """
        if title is None:
            # Simple top border without title
            inner_width = width - 2  # Subtract corners
            return self.top_left + self.render_horizontal(inner_width) + self.top_right

        # Top border with centered title
        inner_width = width - 2  # Subtract corners
        title_with_spaces = f" {title} "
        title_len = len(title_with_spaces)

        if title_len >= inner_width:
            # Title is too long, truncate
            truncated = title[: inner_width - 2] if inner_width > 2 else ""
            return (
                self.top_left
                + self.render_horizontal(inner_width - len(truncated))
                + truncated
                + self.top_right
            )

        # Calculate padding for centering
        remaining = inner_width - title_len
        left_pad = remaining // 2
        right_pad = remaining - left_pad

        return (
            self.top_left
            + self.render_horizontal(left_pad)
            + title_with_spaces
            + self.render_horizontal(right_pad)
            + self.top_right
        )

    def render_bottom_border(self, width: int) -> str:
        """Render bottom border.

        Args:
            width: Total width of the border (including corners)

        Returns:
            Bottom border string

        Example:
            >>> style = BORDERS["solid"]
            >>> style.render_bottom_border(20)
            '└──────────────────┘'
        """
        inner_width = width - 2  # Subtract corners
        return self.bottom_left + self.render_horizontal(inner_width) + self.bottom_right

    def render_divider(self, width: int) -> str:
        """Render horizontal divider with side joints.

        Args:
            width: Total width of the divider (including joints)

        Returns:
            Divider string with left and right joints

        Example:
            >>> style = BORDERS["solid"]
            >>> style.render_divider(20)
            '├──────────────────┤'
        """
        inner_width = width - 2  # Subtract joints
        return self.left_joint + self.render_horizontal(inner_width) + self.right_joint


# Predefined border styles
SOLID = BorderStyle(
    name="solid",
    top_left="┌",
    top_right="┐",
    bottom_left="└",
    bottom_right="┘",
    horizontal="─",
    vertical="│",
    left_joint="├",
    right_joint="┤",
    top_joint="┬",
    bottom_joint="┴",
    cross="┼",
)

DOUBLE = BorderStyle(
    name="double",
    top_left="╔",
    top_right="╗",
    bottom_left="╚",
    bottom_right="╝",
    horizontal="═",
    vertical="║",
    left_joint="╠",
    right_joint="╣",
    top_joint="╦",
    bottom_joint="╩",
    cross="╬",
)

ROUNDED = BorderStyle(
    name="rounded",
    top_left="╭",
    top_right="╮",
    bottom_left="╰",
    bottom_right="╯",
    horizontal="─",
    vertical="│",
    left_joint="├",
    right_joint="┤",
    top_joint="┬",
    bottom_joint="┴",
    cross="┼",
)

HEAVY = BorderStyle(
    name="heavy",
    top_left="┏",
    top_right="┓",
    bottom_left="┗",
    bottom_right="┛",
    horizontal="━",
    vertical="┃",
    left_joint="┣",
    right_joint="┫",
    top_joint="┳",
    bottom_joint="┻",
    cross="╋",
)

THICK = BorderStyle(
    name="thick",
    top_left="█",
    top_right="█",
    bottom_left="█",
    bottom_right="█",
    horizontal="▀",
    vertical="█",
    left_joint="█",
    right_joint="█",
    top_joint="█",
    bottom_joint="█",
    cross="█",
)

ASCII = BorderStyle(
    name="ascii",
    top_left="+",
    top_right="+",
    bottom_left="+",
    bottom_right="+",
    horizontal="-",
    vertical="|",
    left_joint="+",
    right_joint="+",
    top_joint="+",
    bottom_joint="+",
    cross="+",
)

MINIMAL = BorderStyle(
    name="minimal",
    top_left=" ",
    top_right=" ",
    bottom_left=" ",
    bottom_right=" ",
    horizontal="─",
    vertical=" ",
    left_joint=" ",
    right_joint=" ",
    top_joint=" ",
    bottom_joint=" ",
    cross=" ",
)

DOTS = BorderStyle(
    name="dots",
    top_left="·",
    top_right="·",
    bottom_left="·",
    bottom_right="·",
    horizontal="·",
    vertical="·",
    left_joint="·",
    right_joint="·",
    top_joint="·",
    bottom_joint="·",
    cross="·",
)

# Dictionary of all predefined border styles
BORDERS: dict[str, BorderStyle] = {
    "solid": SOLID,
    "double": DOUBLE,
    "rounded": ROUNDED,
    "heavy": HEAVY,
    "thick": THICK,
    "ascii": ASCII,
    "minimal": MINIMAL,
    "dots": DOTS,
}


def get_border_style(name: str) -> BorderStyle:
    """Get a border style by name.

    Args:
        name: Name of the border style (case-insensitive)

    Returns:
        BorderStyle object

    Raises:
        KeyError: If the border style name is not found

    Example:
        >>> style = get_border_style("solid")
        >>> style.name
        'solid'
        >>> style = get_border_style("DOUBLE")
        >>> style.name
        'double'
    """
    name_lower = name.lower()
    if name_lower not in BORDERS:
        available = ", ".join(sorted(BORDERS.keys()))
        raise KeyError(f"Unknown border style: {name!r}. Available styles: {available}")
    return BORDERS[name_lower]


def list_border_styles() -> list[str]:
    """Get list of all available border style names.

    Returns:
        Sorted list of border style names

    Example:
        >>> styles = list_border_styles()
        >>> "solid" in styles
        True
        >>> "double" in styles
        True
    """
    return sorted(BORDERS.keys())
