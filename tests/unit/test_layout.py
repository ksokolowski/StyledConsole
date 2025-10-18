"""Unit tests for Layout and LayoutComposer."""

import pytest

from styledconsole import Layout, LayoutComposer
from styledconsole.utils.text import visual_width


class TestLayout:
    """Test Layout dataclass configuration."""

    def test_layout_defaults(self):
        """Test Layout with default values."""
        elements = [["Line 1"], ["Line 2"]]
        layout = Layout(elements=elements)
        assert layout.elements == elements
        assert layout.align == "left"
        assert layout.spacing == 1
        assert layout.width is None

    def test_layout_custom_values(self):
        """Test Layout with custom values."""
        elements = [["A"], ["B"]]
        layout = Layout(
            elements=elements,
            align="center",
            spacing=2,
            width=50,
        )
        assert layout.elements == elements
        assert layout.align == "center"
        assert layout.spacing == 2
        assert layout.width == 50

    def test_layout_immutable(self):
        """Test that Layout is immutable (frozen)."""
        layout = Layout(elements=[["Test"]])
        with pytest.raises(AttributeError):
            layout.align = "right"  # type: ignore


class TestLayoutComposer:
    """Test LayoutComposer class."""

    def test_composer_initialization(self):
        """Test LayoutComposer initializes correctly."""
        composer = LayoutComposer()
        assert composer is not None

    def test_stack_empty_elements(self):
        """Test stacking with empty elements list."""
        composer = LayoutComposer()
        result = composer.stack([])
        assert result == []

    def test_stack_single_element(self):
        """Test stacking a single element."""
        composer = LayoutComposer()
        element = ["Line 1", "Line 2"]
        result = composer.stack([element])

        assert len(result) == 2
        assert result == element

    def test_stack_multiple_elements(self):
        """Test stacking multiple elements."""
        composer = LayoutComposer()
        elem1 = ["First"]
        elem2 = ["Second"]
        elem3 = ["Third"]

        result = composer.stack([elem1, elem2, elem3], spacing=1)

        # Should have: 1 line + spacing + 1 line + spacing + 1 line = 5 lines
        assert len(result) == 5
        assert "First" in result[0]
        assert "Second" in result[2]
        assert "Third" in result[4]

    def test_stack_with_no_spacing(self):
        """Test stacking with zero spacing."""
        composer = LayoutComposer()
        elem1 = ["Line1"]
        elem2 = ["Line2"]

        result = composer.stack([elem1, elem2], spacing=0)

        # Should have exactly 2 lines (no spacing)
        assert len(result) == 2
        assert "Line1" in result[0]
        assert "Line2" in result[1]

    def test_stack_with_custom_spacing(self):
        """Test stacking with custom spacing."""
        composer = LayoutComposer()
        elem1 = ["A"]
        elem2 = ["B"]

        result = composer.stack([elem1, elem2], spacing=3)

        # Should have: 1 line + 3 blank lines + 1 line = 5 lines
        assert len(result) == 5
        assert "A" in result[0]
        assert result[1].strip() == ""  # Blank line
        assert result[2].strip() == ""  # Blank line
        assert result[3].strip() == ""  # Blank line
        assert "B" in result[4]

    def test_stack_left_alignment(self):
        """Test stacking with left alignment."""
        composer = LayoutComposer()
        elem1 = ["Short"]
        elem2 = ["Much longer line"]

        result = composer.stack([elem1, elem2], align="left", spacing=0)

        # Both should be padded to same width (longer one)
        widths = [visual_width(line) for line in result]
        assert len(set(widths)) == 1  # All same width

        # Short line should be padded on right (left aligned)
        assert result[0].startswith("Short")
        assert result[0].rstrip() == "Short"

    def test_stack_center_alignment(self):
        """Test stacking with center alignment."""
        composer = LayoutComposer()
        elem1 = ["X"]
        elem2 = ["XXXXXXXXXX"]

        result = composer.stack([elem1, elem2], align="center", spacing=0)

        # All lines should have same width
        widths = [visual_width(line) for line in result]
        assert len(set(widths)) == 1

        # Short line should be centered
        assert result[0].strip() == "X"
        # Should have padding on both sides
        left_pad = len(result[0]) - len(result[0].lstrip())
        right_pad = len(result[0]) - len(result[0].rstrip())
        assert abs(left_pad - right_pad) <= 1  # Nearly equal padding

    def test_stack_right_alignment(self):
        """Test stacking with right alignment."""
        composer = LayoutComposer()
        elem1 = ["Short"]
        elem2 = ["Much longer line"]

        result = composer.stack([elem1, elem2], align="right", spacing=0)

        # All lines should have same width
        widths = [visual_width(line) for line in result]
        assert len(set(widths)) == 1

        # Short line should be padded on left (right aligned)
        assert result[0].strip() == "Short"
        assert result[0].endswith("Short")

    def test_stack_with_fixed_width(self):
        """Test stacking with fixed width parameter."""
        composer = LayoutComposer()
        elem1 = ["Short"]
        elem2 = ["Line"]

        result = composer.stack([elem1, elem2], width=50, spacing=0)

        # All lines should be exactly 50 characters wide
        for line in result:
            assert visual_width(line) == 50

    def test_stack_multiline_elements(self):
        """Test stacking elements with multiple lines."""
        composer = LayoutComposer()
        elem1 = ["Line 1A", "Line 1B", "Line 1C"]
        elem2 = ["Line 2A", "Line 2B"]

        result = composer.stack([elem1, elem2], spacing=1)

        # Should have: 3 lines + 1 spacing + 2 lines = 6 lines
        assert len(result) == 6

    def test_stack_with_emoji(self):
        """Test stacking with emoji content."""
        composer = LayoutComposer()
        elem1 = ["🚀 Rocket"]
        elem2 = ["Plain text"]

        result = composer.stack([elem1, elem2], spacing=0)

        # Should handle emoji width correctly
        widths = [visual_width(line) for line in result]
        assert len(set(widths)) == 1  # Consistent width

    def test_compose_method(self):
        """Test compose method with Layout object."""
        composer = LayoutComposer()
        layout = Layout(
            elements=[["Line 1"], ["Line 2"]],
            align="center",
            spacing=2,
        )

        result = composer.compose(layout)
        assert len(result) > 0

    def test_side_by_side_simple(self):
        """Test placing two elements side by side."""
        composer = LayoutComposer()
        left = ["Left 1", "Left 2"]
        right = ["Right 1", "Right 2"]

        result = composer.side_by_side(left, right, spacing=2)

        # Should have 2 lines (one per row)
        assert len(result) == 2
        # Each line should contain both left and right content
        assert "Left 1" in result[0] and "Right 1" in result[0]
        assert "Left 2" in result[1] and "Right 2" in result[1]

    def test_side_by_side_different_heights(self):
        """Test side by side with different element heights."""
        composer = LayoutComposer()
        left = ["A", "B", "C"]
        right = ["X"]

        result = composer.side_by_side(left, right, spacing=2)

        # Should have 3 lines (height of tallest element)
        assert len(result) == 3
        # First line should have both elements
        assert "A" in result[0] and "X" in result[0]

    def test_side_by_side_custom_spacing(self):
        """Test side by side with custom spacing."""
        composer = LayoutComposer()
        left = ["L"]
        right = ["R"]

        result1 = composer.side_by_side(left, right, spacing=1)
        result5 = composer.side_by_side(left, right, spacing=5)

        # More spacing should result in wider lines
        assert visual_width(result5[0]) > visual_width(result1[0])

    def test_grid_simple(self):
        """Test simple 2x2 grid."""
        composer = LayoutComposer()
        row1 = [["A"], ["B"]]
        row2 = [["C"], ["D"]]

        result = composer.grid([row1, row2], column_spacing=2, row_spacing=1)

        # Should have: 1 row + spacing + 1 row = 3 lines
        assert len(result) == 3
        # First row should have A and B
        assert "A" in result[0] and "B" in result[0]
        # Last row should have C and D
        assert "C" in result[2] and "D" in result[2]

    def test_grid_multiline_cells(self):
        """Test grid with multi-line cells."""
        composer = LayoutComposer()
        cell1 = ["Line1", "Line2"]
        cell2 = ["X"]
        row = [[cell1, cell2]]

        result = composer.grid(row)

        # Should have 2 lines (height of tallest cell)
        assert len(result) == 2

    def test_grid_empty_rows(self):
        """Test grid with empty rows."""
        composer = LayoutComposer()
        result = composer.grid([])
        assert result == []

    def test_grid_single_column(self):
        """Test grid with single column."""
        composer = LayoutComposer()
        row1 = [["A"]]
        row2 = [["B"]]

        result = composer.grid([row1, row2], row_spacing=1)

        # Should have: 1 row + spacing + 1 row = 3 lines
        assert len(result) == 3

    def test_grid_with_alignment(self):
        """Test grid with different alignments."""
        composer = LayoutComposer()
        cell1 = ["Short"]
        cell2 = ["Much longer"]
        row = [[cell1, cell2]]

        for align in ["left", "center", "right"]:
            result = composer.grid(row, align=align)
            assert len(result) == 1

    def test_calculate_max_width(self):
        """Test internal max width calculation."""
        composer = LayoutComposer()
        elements = [
            ["Short"],
            ["Much longer line"],
            ["X"],
        ]

        max_width = composer._calculate_max_width(elements)
        assert max_width == visual_width("Much longer line")

    def test_calculate_max_width_with_emoji(self):
        """Test max width calculation with emoji."""
        composer = LayoutComposer()
        elements = [
            ["Plain"],
            ["🚀 Emoji"],
        ]

        max_width = composer._calculate_max_width(elements)
        assert max_width == visual_width("🚀 Emoji")

    def test_align_line_left(self):
        """Test line alignment to the left."""
        composer = LayoutComposer()
        line = "Test"
        aligned = composer._align_line(line, 10, "left")

        assert visual_width(aligned) == 10
        assert aligned.startswith("Test")
        assert aligned.rstrip() == "Test"

    def test_align_line_center(self):
        """Test line alignment to center."""
        composer = LayoutComposer()
        line = "X"
        aligned = composer._align_line(line, 9, "center")

        assert visual_width(aligned) == 9
        assert aligned.strip() == "X"

    def test_align_line_right(self):
        """Test line alignment to the right."""
        composer = LayoutComposer()
        line = "Test"
        aligned = composer._align_line(line, 10, "right")

        assert visual_width(aligned) == 10
        assert aligned.endswith("Test")

    def test_align_line_already_wide(self):
        """Test aligning line that's already at target width."""
        composer = LayoutComposer()
        line = "Exact width"
        width = visual_width(line)
        aligned = composer._align_line(line, width, "left")

        assert aligned == line

    def test_align_line_wider_than_target(self):
        """Test aligning line that exceeds target width."""
        composer = LayoutComposer()
        line = "Very long line"
        aligned = composer._align_line(line, 5, "left")

        # Should return as-is (no truncation)
        assert aligned == line

    def test_complex_nested_layout(self):
        """Test complex nested layout scenario."""
        composer = LayoutComposer()

        # Create some nested elements
        elem1 = ["Header"]
        elem2 = ["Content line 1", "Content line 2"]
        elem3 = ["Footer"]

        result = composer.stack([elem1, elem2, elem3], spacing=1, align="center")

        # Should have proper structure
        assert len(result) > 0
        # All lines should have consistent width
        widths = [visual_width(line) for line in result]
        assert len(set(widths)) == 1
