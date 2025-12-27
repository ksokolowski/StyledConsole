"""Border style definitions for frames and dividers.

This module defines box-drawing characters for various border styles.
"""

from dataclasses import dataclass

from styledconsole.core.registry import Registry
from styledconsole.types import AlignType
from styledconsole.utils.text import pad_to_width, truncate_to_width, visual_width


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
        """Render top border with optional centered title (emoji-safe).

        Uses visual width calculation to handle emojis and wide characters correctly.

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
            >>> style.render_top_border(20, "🚀 Title")
            '┌──── 🚀 Title ────┐'  # Emoji visual width handled
        """
        if title is None or title == "":
            # Simple top border without title
            inner_width = width - 2  # Subtract corners
            return self.top_left + self.render_horizontal(inner_width) + self.top_right

        # Top border with centered title (emoji-safe)
        inner_width = width - 2  # Subtract corners
        title_with_spaces = f" {title} "
        title_visual_width = visual_width(title_with_spaces)

        if title_visual_width >= inner_width:
            # Title is too long, truncate using emoji-safe truncation
            if inner_width > 2:
                truncated = truncate_to_width(title, inner_width - 2)  # -2 for spaces
                truncated_with_spaces = f" {truncated} "
                truncated_visual_width = visual_width(truncated_with_spaces)
                padding_needed = inner_width - truncated_visual_width
                return (
                    self.top_left
                    + self.render_horizontal(padding_needed)
                    + truncated_with_spaces
                    + self.top_right
                )
            else:
                # No room for title
                return self.top_left + self.render_horizontal(inner_width) + self.top_right

        # Calculate padding for centering (using visual width)
        remaining = inner_width - title_visual_width
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

        For THICK style, uses LOWER HALF BLOCK (▄) instead of UPPER HALF BLOCK (▀)
        to create proper thick frame illusion.

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

        # Special case for THICK style: use LOWER HALF BLOCK for bottom border
        if self.name == "thick" and self.horizontal == "▀":
            horizontal_char = "▄"  # LOWER HALF BLOCK (U+2584)
        else:
            horizontal_char = self.horizontal

        return (
            self.bottom_left
            + self.render_horizontal(inner_width, horizontal_char)
            + self.bottom_right
        )

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

    def render_line(self, width: int, content: str = "", align: AlignType = "left") -> str:
        """Render a content line with borders (emoji-safe).

        Uses visual width calculation to handle emojis and wide characters correctly.

        Args:
            width: Total width of the line (including borders)
            content: Content text to display (will be truncated if too long)
            align: Text alignment - "left", "center", or "right"

        Returns:
            Content line with left and right borders, properly aligned

        Example:
            >>> style = BORDERS["solid"]
            >>> style.render_line(20, "Hello")
            '│Hello             │'
            >>> style.render_line(20, "🚀 Rocket", align="left")
            '│🚀 Rocket         │'  # Emoji visual width handled
            >>> style.render_line(20, "Hello", align="center")
            '│      Hello       │'
            >>> style.render_line(20, "Hello", align="right")
            '│             Hello│'
        """
        if width < 2:
            return self.vertical * width

        inner_width = width - 2  # Subtract left and right borders

        # Handle empty content
        if not content:
            return self.vertical + " " * inner_width + self.vertical

        # Truncate content if visually too long (emoji-safe)
        if visual_width(content) > inner_width:
            content = truncate_to_width(content, inner_width)

        # Use pad_to_width for emoji-safe padding based on alignment
        if align == "center":
            # For center alignment, calculate padding and split
            content_vis_width = visual_width(content)
            padding_needed = inner_width - content_vis_width
            left_pad = padding_needed // 2
            right_pad = padding_needed - left_pad
            inner = " " * left_pad + content + " " * right_pad
        elif align == "right":
            # Right align: pad on the left
            inner = pad_to_width(content, inner_width, align="right")
        else:  # left (default)
            # Left align: pad on the right
            inner = pad_to_width(content, inner_width, align="left")

        return self.vertical + inner + self.vertical


class BorderRegistry(Registry[BorderStyle]):
    """Registry for border styles."""

    def __init__(self) -> None:
        super().__init__("border style")


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

ROUNDED_THICK = BorderStyle(
    name="rounded_thick",
    top_left="╭",
    top_right="╮",
    bottom_left="╰",
    bottom_right="╯",
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

# Registry instance for all predefined border styles
BORDERS = BorderRegistry()

# Register predefined styles
BORDERS.register("solid", SOLID)
BORDERS.register("double", DOUBLE)
BORDERS.register("rounded", ROUNDED)
BORDERS.register("heavy", HEAVY)
BORDERS.register("thick", THICK)
BORDERS.register("rounded_thick", ROUNDED_THICK)
BORDERS.register("ascii", ASCII)
BORDERS.register("minimal", MINIMAL)
BORDERS.register("dots", DOTS)


def get_border_style(name: str) -> BorderStyle:
    """Get a border style by name.

    Args:
        name: Name of the border style (case-insensitive)

    Returns:
        BorderStyle object

    Raises:
        ValueError: If the border style name is not found

    Example:
        >>> style = get_border_style("solid")
        >>> style.name
        'solid'
        >>> style = get_border_style("DOUBLE")
        >>> style.name
        'double'
    """
    try:
        return BORDERS.get(name)
    except KeyError as e:
        raise ValueError(str(e)) from e


def list_border_styles() -> list[str]:
    """Get list of all available border style names.

    Returns:
        Sorted list of border style names

    Example:
        >>> styles = list_border_styles()
        >>> print(styles)
        ['ascii', 'dots', 'double', 'heavy', 'minimal', 'rounded', 'solid', 'thick']
    """
    return BORDERS.list_all()


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


__all__ = [
    "ASCII",
    "BORDERS",
    "DOTS",
    "DOUBLE",
    "HEAVY",
    "MINIMAL",
    "ROUNDED",
    "SOLID",
    "THICK",
    "BorderStyle",
    "get_border_chars",
    "get_border_style",
    "list_border_styles",
]
