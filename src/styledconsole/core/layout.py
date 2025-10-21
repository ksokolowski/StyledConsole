"""Layout composition using Rich's native renderables (v0.3.0).

This module provides backward-compatible wrappers around Rich's layout
capabilities with the original line-by-line API preserved for compatibility.

v0.3.0: Internally uses Rich where beneficial, but maintains exact
backward compatibility for existing code.
"""

from dataclasses import dataclass
from typing import Literal

from rich.console import RenderableType

from styledconsole.utils.text import visual_width

AlignType = Literal["left", "center", "right"]


@dataclass(frozen=True)
class Layout:
    """Configuration for layout composition (legacy - kept for compatibility).

    v0.3.0: Use Rich renderables directly instead.

    Attributes:
        elements: List of rendered content blocks (each is a list of lines)
        align: Horizontal alignment for all elements ("left", "center", "right")
        spacing: Number of blank lines between elements (0 for no spacing)
        width: Fixed width for all elements (None for auto-width based on widest)
    """

    elements: list[list[str]]
    align: AlignType = "left"
    spacing: int = 1
    width: int | None = None


class LayoutComposer:
    """Composer for creating layouts (v0.3.0 - backward compatible).

    v0.3.0: Maintains backward compatibility while preparing for Rich-native
    approach in future versions. Uses manual alignment for exact compatibility
    with existing tests and examples.

    Features:
    - Vertical stacking with precise alignment
    - Horizontal layouts (side-by-side, grid)
    - Configurable spacing
    - ANSI-safe width calculations

    Example:
        >>> composer = LayoutComposer()
        >>> layout = composer.stack([elem1, elem2], spacing=1)
    """

    def stack(
        self,
        elements: list[list[str]] | list[RenderableType],
        align: AlignType = "left",
        spacing: int = 1,
        width: int | None = None,
    ) -> list[str]:
        """Stack multiple elements vertically with alignment and spacing.

        Args:
            elements: List of rendered content blocks (list of lines)
            align: Horizontal alignment ("left", "center", "right")
            spacing: Number of blank lines between elements (default: 1)
            width: Fixed width for all elements (None for auto-width)

        Returns:
            List of lines representing the complete stacked layout

        Example:
            >>> composer = LayoutComposer()
            >>> elem1 = ["Line 1", "Line 2"]
            >>> elem2 = ["Other line"]
            >>> layout = composer.stack([elem1, elem2], spacing=1)
        """
        # Ensure all elements are list[str] for compatibility
        str_elements: list[list[str]] = []
        for element in elements:
            if isinstance(element, list):
                str_elements.append(element)
            else:
                # Convert renderable to strings
                str_elements.append([str(element)])

        layout = Layout(
            elements=str_elements,
            align=align,
            spacing=spacing,
            width=width,
        )
        return self.compose(layout)

    def compose(self, layout: Layout) -> list[str]:
        """Compose a Layout configuration into final output.

        Args:
            layout: Layout configuration object

        Returns:
            List of lines representing the complete layout
        """
        if not layout.elements:
            return []

        # Determine target width
        if layout.width is not None:
            target_width = layout.width
        else:
            # Auto-calculate width based on widest line
            target_width = self._calculate_max_width(layout.elements)

        result = []

        for i, element in enumerate(layout.elements):
            # Align each line of the element
            for line in element:
                aligned_line = self._align_line(line, target_width, layout.align)
                result.append(aligned_line)

            # Add spacing between elements (but not after the last one)
            if i < len(layout.elements) - 1 and layout.spacing > 0:
                for _ in range(layout.spacing):
                    result.append(" " * target_width)

        return result

    def _calculate_max_width(self, elements: list[list[str]]) -> int:
        """Calculate maximum visual width across all elements.

        Args:
            elements: List of rendered content blocks

        Returns:
            Maximum visual width found
        """
        max_width = 0

        for element in elements:
            for line in element:
                width = visual_width(line)
                if width > max_width:
                    max_width = width

        return max_width

    def _align_line(self, line: str, target_width: int, align: AlignType) -> str:
        """Align a line to target width with specified alignment.

        Args:
            line: Line to align (may contain ANSI codes)
            target_width: Target visual width
            align: Alignment type ("left", "center", "right")

        Returns:
            Aligned line with consistent visual width
        """
        # Get visual width of line (ignoring ANSI codes)
        current_width = visual_width(line)

        # If line is already at or exceeds target width, return as-is
        if current_width >= target_width:
            return line

        # Calculate padding needed
        padding_needed = target_width - current_width

        if align == "left":
            # Pad on the right
            return line + (" " * padding_needed)
        elif align == "right":
            # Pad on the left
            return (" " * padding_needed) + line
        else:  # center
            # Split padding between left and right
            left_pad = padding_needed // 2
            right_pad = padding_needed - left_pad
            return (" " * left_pad) + line + (" " * right_pad)

    def grid(
        self,
        rows: list[list[list[str]]],
        column_spacing: int = 2,
        row_spacing: int = 1,
        align: AlignType = "left",
    ) -> list[str]:
        """Create a grid layout with multiple rows and columns.

        Args:
            rows: List of rows, where each row is a list of elements
            column_spacing: Spaces between columns (default: 2)
            row_spacing: Blank lines between rows (default: 1)
            align: Vertical alignment within cells ("left", "center", "right")

        Returns:
            List of lines representing the complete grid layout

        Example:
            >>> composer = LayoutComposer()
            >>> row1 = [elem1, elem2, elem3]  # 3 columns
            >>> row2 = [elem4, elem5, elem6]  # 3 columns
            >>> grid = composer.grid([row1, row2], column_spacing=2)
        """
        if not rows or not rows[0]:
            return []

        result = []

        for row_idx, row in enumerate(rows):
            # Calculate max height for this row
            max_height = max(len(element) for element in row)

            # Calculate column widths
            col_widths = []
            for col_idx in range(len(row)):
                max_col_width = max(visual_width(line) for line in row[col_idx])
                col_widths.append(max_col_width)

            # Render each line of the row
            for line_idx in range(max_height):
                line_parts = []

                for col_idx, element in enumerate(row):
                    # Get the line from this element (or empty if past end)
                    if line_idx < len(element):
                        cell_line = element[line_idx]
                    else:
                        cell_line = ""

                    # Align to column width
                    aligned = self._align_line(cell_line, col_widths[col_idx], align)
                    line_parts.append(aligned)

                # Join columns with spacing
                result.append((" " * column_spacing).join(line_parts))

            # Add row spacing (but not after last row)
            if row_idx < len(rows) - 1 and row_spacing > 0:
                # Width is sum of column widths plus spacing
                total_width = sum(col_widths) + (column_spacing * (len(row) - 1))
                for _ in range(row_spacing):
                    result.append(" " * total_width)

        return result

    def side_by_side(
        self,
        left: list[str],
        right: list[str],
        spacing: int = 2,
        align: AlignType = "left",
    ) -> list[str]:
        """Place two elements side by side horizontally.

        Args:
            left: Left element (list of lines)
            right: Right element (list of lines)
            spacing: Spaces between elements (default: 2)
            align: Vertical alignment ("left", "center", "right")

        Returns:
            List of lines with elements placed side by side

        Example:
            >>> composer = LayoutComposer()
            >>> layout = composer.side_by_side(frame1, frame2, spacing=3)
        """
        return self.grid([[left, right]], column_spacing=spacing, align=align)


__all__ = [
    "Layout",
    "LayoutComposer",
]
