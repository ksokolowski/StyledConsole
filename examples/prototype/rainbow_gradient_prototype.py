#!/usr/bin/env python3
"""Prototype: Rainbow Effects and Border Gradients

This prototype demonstrates:
1. Rainbow gradient effect (auto-generates gradient from red→violet)
2. Border gradients (vertical gradient on borders)
3. Diagonal gradients (top-left to bottom-right)
4. Combined effects (rainbow content + rainbow border)
5. Character-by-character coloring for diagonal effects

Status: PROTOTYPE - Not integrated into main library yet
"""

from styledconsole.core.frame import FrameRenderer
from styledconsole.core.styles import get_border_style
from styledconsole.utils.color import interpolate_color
from styledconsole.utils.text import strip_ansi, visual_width

# Rainbow color spectrum (7 colors: ROYGBIV)
# Using CSS4 color names for readability
RAINBOW_COLORS = [
    "red",  # #FF0000
    "orange",  # #FFA500
    "yellow",  # #FFFF00
    "lime",  # #00FF00 (bright green for rainbow spectrum)
    "blue",  # #0000FF
    "indigo",  # #4B0082
    "darkviolet",  # #9400D3
]

RAINBOW_CSS4 = ["red", "orange", "yellow", "lime", "blue", "indigo", "darkviolet"]


def get_rainbow_color(position: float) -> str:
    """Get color from rainbow spectrum at position 0.0-1.0.

    Args:
        position: Position in rainbow (0.0 = red, 1.0 = violet)

    Returns:
        Hex color string
    """
    if position <= 0:
        return RAINBOW_COLORS[0]
    if position >= 1:
        return RAINBOW_COLORS[-1]

    # Find which two colors to interpolate between
    segment_size = 1.0 / (len(RAINBOW_COLORS) - 1)
    segment_index = int(position / segment_size)
    segment_index = min(segment_index, len(RAINBOW_COLORS) - 2)

    # Calculate position within this segment (0.0-1.0)
    local_position = (position - segment_index * segment_size) / segment_size

    # Interpolate between the two colors
    color1 = RAINBOW_COLORS[segment_index]
    color2 = RAINBOW_COLORS[segment_index + 1]

    return interpolate_color(color1, color2, local_position)


class RainbowFrameRenderer(FrameRenderer):
    """Extended FrameRenderer with rainbow and border gradient support."""

    def render_rainbow(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: str = "left",
        rainbow_content: bool = True,
        rainbow_border: bool = False,
    ) -> list[str]:
        """Render frame with rainbow gradient effect.

        Args:
            content: Content to render
            title: Optional title
            border: Border style
            width: Frame width
            padding: Padding
            align: Alignment
            rainbow_content: Apply rainbow gradient to content
            rainbow_border: Apply rainbow gradient to border

        Returns:
            List of rendered lines
        """
        # Normalize content to list
        if isinstance(content, str):
            content_lines = content.splitlines() if content else [""]
        else:
            content_lines = content if content else [""]

        # Get border style
        style = get_border_style(border)

        # Calculate width
        if width is None:
            width = self._calculate_width(content_lines, title, padding, 20, 100)

        lines: list[str] = []
        total_lines = len(content_lines) + 2  # +2 for top and bottom borders

        # Top border
        top_border = style.render_top_border(width, title)
        if rainbow_border:
            # First line of border (top) - position 0
            color = get_rainbow_color(0.0)
            top_border = self._colorize(top_border, color)
        lines.append(top_border)

        # Content lines
        for idx, line in enumerate(content_lines):
            content_line = self._render_content_line(style, line, width, padding, align)

            # Calculate rainbow position for this line
            line_position = (idx + 1) / (total_lines - 1)

            if rainbow_content:
                # Apply rainbow to content
                content_color = get_rainbow_color(line_position)
                content_line = self._colorize_content_in_line(
                    content_line, style, content_color, None
                )

            if rainbow_border:
                # Apply rainbow to border
                border_color = get_rainbow_color(line_position)
                content_line = self._colorize_borders_in_line(content_line, style, border_color)

            lines.append(content_line)

        # Bottom border
        bottom_border = style.render_bottom_border(width)
        if rainbow_border:
            # Last line of border (bottom) - position 1.0
            color = get_rainbow_color(1.0)
            bottom_border = self._colorize(bottom_border, color)
        lines.append(bottom_border)

        return lines

    def render_with_border_gradient(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: str = "left",
        border_gradient_start: str = "red",
        border_gradient_end: str = "blue",
        content_gradient_start: str | None = None,
        content_gradient_end: str | None = None,
    ) -> list[str]:
        """Render frame with border gradient.

        Args:
            content: Content to render
            title: Optional title
            border: Border style
            width: Frame width
            padding: Padding
            align: Alignment
            border_gradient_start: Starting color for border
            border_gradient_end: Ending color for border
            content_gradient_start: Optional gradient for content
            content_gradient_end: Optional gradient for content

        Returns:
            List of rendered lines
        """
        # Normalize content to list
        if isinstance(content, str):
            content_lines = content.splitlines() if content else [""]
        else:
            content_lines = content if content else [""]

        # Get border style
        style = get_border_style(border)

        # Calculate width
        if width is None:
            width = self._calculate_width(content_lines, title, padding, 20, 100)

        lines: list[str] = []
        total_lines = len(content_lines) + 2  # +2 for top and bottom borders

        # Top border with gradient start color
        top_border = style.render_top_border(width, title)
        border_color = border_gradient_start
        top_border = self._colorize(top_border, border_color)
        lines.append(top_border)

        # Content lines with interpolated border colors
        for idx, line in enumerate(content_lines):
            content_line = self._render_content_line(style, line, width, padding, align)

            # Calculate gradient position for this line
            line_position = (idx + 1) / (total_lines - 1)

            # Apply content gradient if specified
            if content_gradient_start and content_gradient_end:
                content_color = interpolate_color(
                    content_gradient_start,
                    content_gradient_end,
                    idx / max(len(content_lines) - 1, 1),
                )
                content_line = self._colorize_content_in_line(
                    content_line, style, content_color, None
                )

            # Apply border gradient
            border_color = interpolate_color(
                border_gradient_start, border_gradient_end, line_position
            )
            content_line = self._colorize_borders_in_line(content_line, style, border_color)

            lines.append(content_line)

        # Bottom border with gradient end color
        bottom_border = style.render_bottom_border(width)
        border_color = border_gradient_end
        bottom_border = self._colorize(bottom_border, border_color)
        lines.append(bottom_border)

        return lines

    def render_diagonal_gradient(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: str = "left",
        gradient_start: str = "red",
        gradient_end: str = "blue",
        apply_to_border: bool = True,
        apply_to_content: bool = True,
    ) -> list[str]:
        """Render frame with diagonal gradient (top-left to bottom-right).

        This creates a gradient that flows diagonally across the frame,
        with each character colored based on its position from top-left (0,0)
        to bottom-right (max_row, max_col).

        Args:
            content: Content to render
            title: Optional title
            border: Border style
            width: Frame width
            padding: Padding
            align: Alignment
            gradient_start: Starting color (top-left corner)
            gradient_end: Ending color (bottom-right corner)
            apply_to_border: Apply diagonal gradient to borders
            apply_to_content: Apply diagonal gradient to content

        Returns:
            List of rendered lines with diagonal gradient
        """
        # Normalize content to list
        if isinstance(content, str):
            content_lines = content.splitlines() if content else [""]
        else:
            content_lines = content if content else [""]

        # Get border style
        style = get_border_style(border)

        # Calculate width
        if width is None:
            width = self._calculate_width(content_lines, title, padding, 20, 100)

        # Build frame without colors first
        lines: list[str] = []

        # Top border
        top_border = style.render_top_border(width, title)
        lines.append(top_border)

        # Content lines
        for line in content_lines:
            content_line = self._render_content_line(style, line, width, padding, align)
            lines.append(content_line)

        # Bottom border
        bottom_border = style.render_bottom_border(width)
        lines.append(bottom_border)

        # Now apply diagonal gradient character-by-character
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

            # Special handling for title line (first line with title)
            if row_idx == 0 and title:
                # For title line, we need to preserve the structure
                # The line format is: corner + horizontal + title + horizontal + corner
                # We'll color the border parts but leave spaces around title for now
                colored_line = ""
                visual_col = 0
                i = 0

                while i < len(clean_line):
                    char = clean_line[i]

                    # Calculate position
                    row_progress = row_idx / max(total_rows - 1, 1)
                    col_progress = visual_col / max(max_col - 1, 1)
                    diagonal_position = (row_progress + col_progress) / 2.0
                    char_color = interpolate_color(gradient_start, gradient_end, diagonal_position)

                    # Check if we're at the title position
                    # Title is embedded in the line, so detect it
                    if title in clean_line[i : i + len(title) + 2]:  # +2 for spaces around title
                        # We're at the title - color title if content coloring is on
                        if apply_to_content:
                            # Color the title portion
                            title_part = clean_line[i : i + len(title) + 2]
                            for tc in title_part:
                                tc_progress = visual_col / max(max_col - 1, 1)
                                tc_position = (row_progress + tc_progress) / 2.0
                                tc_color = interpolate_color(
                                    gradient_start, gradient_end, tc_position
                                )
                                colored_line += self._colorize(tc, tc_color)
                                visual_col += 1
                            i += len(title_part)
                        else:
                            # Keep title as-is
                            colored_line += clean_line[i : i + len(title) + 2]
                            visual_col += len(title) + 2
                            i += len(title) + 2
                        continue

                    # Regular border character
                    if apply_to_border and char in border_chars:
                        colored_line += self._colorize(char, char_color)
                    else:
                        colored_line += char

                    visual_col += 1
                    i += 1

                colored_lines.append(colored_line)
            else:
                # Regular line without title
                colored_chars = []
                visual_col = 0

                for char in clean_line:
                    # Calculate diagonal position (0.0 to 1.0)
                    row_progress = row_idx / max(total_rows - 1, 1)
                    col_progress = visual_col / max(max_col - 1, 1)
                    diagonal_position = (row_progress + col_progress) / 2.0

                    # Get color for this position
                    char_color = interpolate_color(gradient_start, gradient_end, diagonal_position)

                    # Determine if this is border or content character
                    is_border_char = (
                        row_idx == 0  # Top border
                        or row_idx == total_rows - 1  # Bottom border
                        or char in border_chars  # Border character
                    )

                    # Apply color based on settings
                    if (is_border_char and apply_to_border) or (
                        not is_border_char and apply_to_content
                    ):
                        colored_chars.append(self._colorize(char, char_color))
                    else:
                        colored_chars.append(char)

                    # Update visual column position
                    visual_col += 1

                colored_lines.append("".join(colored_chars))

        return colored_lines

    def render_diagonal_rainbow(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "rounded",
        width: int | None = None,
        padding: int = 1,
        align: str = "left",
        apply_to_border: bool = True,
        apply_to_content: bool = True,
    ) -> list[str]:
        """Render frame with diagonal rainbow effect (top-left to bottom-right).

        Creates a rainbow that flows diagonally from red (top-left) to
        violet (bottom-right) with smooth color transitions.

        Args:
            content: Content to render
            title: Optional title
            border: Border style
            width: Frame width
            padding: Padding
            align: Alignment
            apply_to_border: Apply diagonal rainbow to borders
            apply_to_content: Apply diagonal rainbow to content

        Returns:
            List of rendered lines with diagonal rainbow
        """
        # Normalize content to list
        if isinstance(content, str):
            content_lines = content.splitlines() if content else [""]
        else:
            content_lines = content if content else [""]

        # Get border style
        style = get_border_style(border)

        # Calculate width
        if width is None:
            width = self._calculate_width(content_lines, title, padding, 20, 100)

        # Build frame without colors first
        lines: list[str] = []

        # Top border
        top_border = style.render_top_border(width, title)
        lines.append(top_border)

        # Content lines
        for line in content_lines:
            content_line = self._render_content_line(style, line, width, padding, align)
            lines.append(content_line)

        # Bottom border
        bottom_border = style.render_bottom_border(width)
        lines.append(bottom_border)

        # Now apply diagonal rainbow character-by-character
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

            # Special handling for title line (first line with title)
            if row_idx == 0 and title:
                # For title line, we need to preserve the structure
                colored_line = ""
                visual_col = 0
                i = 0

                while i < len(clean_line):
                    char = clean_line[i]

                    # Calculate position
                    row_progress = row_idx / max(total_rows - 1, 1)
                    col_progress = visual_col / max(max_col - 1, 1)
                    diagonal_position = (row_progress + col_progress) / 2.0
                    char_color = get_rainbow_color(diagonal_position)

                    # Check if we're at the title position
                    if title in clean_line[i : i + len(title) + 2]:  # +2 for spaces around title
                        # We're at the title - color title if content coloring is on
                        if apply_to_content:
                            # Color the title portion
                            title_part = clean_line[i : i + len(title) + 2]
                            for tc in title_part:
                                tc_progress = visual_col / max(max_col - 1, 1)
                                tc_position = (row_progress + tc_progress) / 2.0
                                tc_color = get_rainbow_color(tc_position)
                                colored_line += self._colorize(tc, tc_color)
                                visual_col += 1
                            i += len(title_part)
                        else:
                            # Keep title as-is
                            colored_line += clean_line[i : i + len(title) + 2]
                            visual_col += len(title) + 2
                            i += len(title) + 2
                        continue

                    # Regular border character
                    if apply_to_border and char in border_chars:
                        colored_line += self._colorize(char, char_color)
                    else:
                        colored_line += char

                    visual_col += 1
                    i += 1

                colored_lines.append(colored_line)
            else:
                # Regular line without title
                colored_chars = []
                visual_col = 0

                for char in clean_line:
                    # Calculate diagonal position (0.0 to 1.0)
                    row_progress = row_idx / max(total_rows - 1, 1)
                    col_progress = visual_col / max(max_col - 1, 1)
                    diagonal_position = (row_progress + col_progress) / 2.0

                    # Get rainbow color for this position
                    char_color = get_rainbow_color(diagonal_position)

                    # Determine if this is border or content character
                    is_border_char = (
                        row_idx == 0 or row_idx == total_rows - 1 or char in border_chars
                    )

                    # Apply color based on settings
                    if (is_border_char and apply_to_border) or (
                        not is_border_char and apply_to_content
                    ):
                        colored_chars.append(self._colorize(char, char_color))
                    else:
                        colored_chars.append(char)

                    # Update visual column position
                    visual_col += 1

                colored_lines.append("".join(colored_chars))

        return colored_lines


def main():
    """Demonstrate rainbow and border gradient effects."""
    renderer = RainbowFrameRenderer()

    print("\n" + "=" * 80)
    print(" " * 25 + "🌈 RAINBOW & GRADIENT PROTOTYPE 🌈")
    print("=" * 80)
    print()

    # Demo 1: Rainbow content only
    print("1️⃣  RAINBOW CONTENT (content only):")
    print("-" * 80)
    lines = renderer.render_rainbow(
        [
            "Line 1 - Red",
            "Line 2 - Orange",
            "Line 3 - Yellow",
            "Line 4 - Green",
            "Line 5 - Blue",
            "Line 6 - Indigo",
            "Line 7 - Violet",
        ],
        title="🌈 Rainbow Content",
        border="rounded",
        rainbow_content=True,
        rainbow_border=False,
        width=40,
    )
    for line in lines:
        print(line)
    print()

    # Demo 2: Rainbow border only
    print("2️⃣  RAINBOW BORDER (border only):")
    print("-" * 80)
    lines = renderer.render_rainbow(
        [
            "Plain text content",
            "No color gradient",
            "on the content itself",
            "But look at",
            "the borders!",
            "They're rainbow! 🌈",
        ],
        title="🎨 Rainbow Border",
        border="double",
        rainbow_content=False,
        rainbow_border=True,
        width=40,
    )
    for line in lines:
        print(line)
    print()

    # Demo 3: Both rainbow content AND border!
    print("3️⃣  DOUBLE RAINBOW (content + border):")
    print("-" * 80)
    lines = renderer.render_rainbow(
        ["Ultimate", "Rainbow", "Effect", "Content AND Border", "Both rainbow! 🌈✨"],
        title="🌈🌈 DOUBLE RAINBOW 🌈🌈",
        border="heavy",
        rainbow_content=True,
        rainbow_border=True,
        width=40,
    )
    for line in lines:
        print(line)
    print()

    # Demo 4: Custom border gradient (red → blue)
    print("4️⃣  BORDER GRADIENT (red → blue):")
    print("-" * 80)
    lines = renderer.render_with_border_gradient(
        ["Top border is RED", "Middle borders transition", "Bottom border is BLUE"],
        title="🔴→🔵 Gradient Border",
        border="rounded",
        border_gradient_start="red",
        border_gradient_end="blue",
        width=40,
    )
    for line in lines:
        print(line)
    print()

    # Demo 5: Border gradient + Content gradient (ULTIMATE!)
    print("5️⃣  ULTIMATE COMBO (border gradient + content gradient):")
    print("-" * 80)
    lines = renderer.render_with_border_gradient(
        [
            "Border: Red → Blue",
            "Content: Yellow → Magenta",
            "Two gradients at once!",
            "Visual feast! 🎨",
        ],
        title="🎨 Double Gradient",
        border="double",
        border_gradient_start="red",
        border_gradient_end="blue",
        content_gradient_start="yellow",
        content_gradient_end="magenta",
        width=45,
    )
    for line in lines:
        print(line)
    print()

    # Demo 6: Fire effect (yellow → red border)
    print("6️⃣  FIRE EFFECT (yellow → red):")
    print("-" * 80)
    lines = renderer.render_with_border_gradient(
        ["🔥 Flames at top", "🔥 Heat in middle", "🔥 Fire at bottom"],
        title="🔥 FIRE FRAME 🔥",
        border="heavy",
        border_gradient_start="yellow",
        border_gradient_end="red",
        width=35,
    )
    for line in lines:
        print(line)
    print()

    # Demo 7: Ocean effect (cyan → blue)
    print("7️⃣  OCEAN EFFECT (cyan → blue):")
    print("-" * 80)
    lines = renderer.render_with_border_gradient(
        ["🌊 Surface water", "🌊 Deeper water", "🌊 Ocean depths"],
        title="🌊 Ocean Frame",
        border="rounded",
        border_gradient_start="cyan",
        border_gradient_end="darkblue",
        content_gradient_start="lightblue",
        content_gradient_end="blue",
        width=35,
    )
    for line in lines:
        print(line)
    print()

    # Demo 8: Diagonal gradient (red → blue) - Content only
    print("8️⃣  DIAGONAL GRADIENT (top-left to bottom-right) - Content:")
    print("-" * 80)
    lines = renderer.render_diagonal_gradient(
        [
            "Top-left: RED",
            "Center: PURPLE",
            "Bottom-right: BLUE",
            "Diagonal flow!",
            "Each character colored!",
        ],
        title="↘ Diagonal Gradient",
        border="rounded",
        gradient_start="red",
        gradient_end="blue",
        apply_to_border=False,
        apply_to_content=True,
        width=45,
    )
    for line in lines:
        print(line)
    print()

    # Demo 9: Diagonal gradient - Border only
    print("9️⃣  DIAGONAL GRADIENT - Border only:")
    print("-" * 80)
    lines = renderer.render_diagonal_gradient(
        ["Plain content", "No gradient here", "Check the borders!"],
        title="🎨 Diagonal Border",
        border="double",
        gradient_start="yellow",
        gradient_end="magenta",
        apply_to_border=True,
        apply_to_content=False,
        width=40,
    )
    for line in lines:
        print(line)
    print()

    # Demo 10: Diagonal gradient - BOTH border and content!
    print("🔟 DIAGONAL GRADIENT - Border + Content:")
    print("-" * 80)
    lines = renderer.render_diagonal_gradient(
        ["Everything flows", "From top-left", "To bottom-right", "Stunning effect! ✨"],
        title="↘ Full Diagonal",
        border="heavy",
        gradient_start="lime",
        gradient_end="red",
        apply_to_border=True,
        apply_to_content=True,
        width=40,
    )
    for line in lines:
        print(line)
    print()

    # Demo 11: Diagonal RAINBOW effect - Content only
    print("1️⃣1️⃣ DIAGONAL RAINBOW (red→violet) - Content:")
    print("-" * 80)
    lines = renderer.render_diagonal_rainbow(
        [
            "Top-left: RED 🔴",
            "Diagonal: RAINBOW 🌈",
            "Bottom-right: VIOLET 🟣",
            "7 colors flowing",
            "Character by character!",
        ],
        title="🌈 Diagonal Rainbow",
        border="rounded",
        apply_to_border=False,
        apply_to_content=True,
        width=45,
    )
    for line in lines:
        print(line)
    print()

    # Demo 12: Diagonal RAINBOW - Border only
    print("1️⃣2️⃣ DIAGONAL RAINBOW - Border only:")
    print("-" * 80)
    lines = renderer.render_diagonal_rainbow(
        ["Content is plain", "But look at borders!", "Rainbow diagonal! 🌈"],
        title="🎨 Rainbow Border Diagonal",
        border="double",
        apply_to_border=True,
        apply_to_content=False,
        width=45,
    )
    for line in lines:
        print(line)
    print()

    # Demo 13: ULTIMATE - Diagonal rainbow on EVERYTHING!
    print("1️⃣3️⃣ ULTIMATE DIAGONAL RAINBOW (border + content):")
    print("-" * 80)
    lines = renderer.render_diagonal_rainbow(
        ["Red in top-left", "Rainbow cascade", "Violet bottom-right", "ULTIMATE effect! 🌈✨🎨"],
        title="🌈↘ ULTIMATE DIAGONAL 🌈",
        border="heavy",
        apply_to_border=True,
        apply_to_content=True,
        width=45,
    )
    for line in lines:
        print(line)
    print()

    print("=" * 80)
    print("✨ Prototype complete! All effects working (including DIAGONAL)! ✨")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
