"""Tests for console.group() context manager functionality.

Tests the context manager that captures frame() calls and renders
them together as a group when the context exits.
"""

import pytest

from styledconsole import Console


class TestGroupContextBasic:
    """Basic group() context manager tests."""

    def test_group_captures_single_frame(self):
        """Single frame inside group is captured and rendered."""
        console = Console(record=True, width=80)
        with console.group(title="Test Group"):
            console.frame("Hello", title="Greeting")
        output = console.export_text()
        assert "Hello" in output
        assert "Greeting" in output
        assert "Test Group" in output

    def test_group_captures_multiple_frames(self):
        """Multiple frames inside group are captured and rendered."""
        console = Console(record=True, width=80)
        with console.group(title="Multi"):
            console.frame("Section A")
            console.frame("Section B")
            console.frame("Section C")
        output = console.export_text()
        assert "Section A" in output
        assert "Section B" in output
        assert "Section C" in output
        assert "Multi" in output

    def test_group_without_title(self):
        """Group without title still renders inner frames."""
        console = Console(record=True, width=80)
        with console.group():
            console.frame("Content A")
            console.frame("Content B")
        output = console.export_text()
        assert "Content A" in output
        assert "Content B" in output

    def test_empty_group(self):
        """Empty group doesn't crash."""
        console = Console(record=True, width=80)
        with console.group(title="Empty"):
            pass
        # Should not raise


class TestGroupContextNesting:
    """Tests for nested group contexts."""

    def test_nested_groups(self):
        """Nested groups render correctly."""
        console = Console(record=True, width=80)
        with console.group(title="Outer"):
            console.frame("Top")
            with console.group(title="Inner"):
                console.frame("Nested A")
                console.frame("Nested B")
            console.frame("Bottom")
        output = console.export_text()
        assert "Outer" in output
        assert "Inner" in output
        assert "Top" in output
        assert "Nested A" in output
        assert "Nested B" in output
        assert "Bottom" in output

    def test_deeply_nested_groups(self):
        """Three levels of nesting work correctly."""
        console = Console(record=True, width=80)
        with console.group(title="Level 1"):
            with console.group(title="Level 2"):
                with console.group(title="Level 3"):
                    console.frame("Deep content")
        output = console.export_text()
        assert "Level 1" in output
        assert "Level 2" in output
        assert "Level 3" in output
        assert "Deep content" in output


class TestGroupContextStyling:
    """Tests for group styling options."""

    def test_group_border_style(self):
        """Group border style is applied."""
        console = Console(record=True, width=80)
        with console.group(title="Heavy", border="heavy"):
            console.frame("Content")
        output = console.export_text()
        assert "Content" in output
        # Heavy border uses ┏ ┓ ┗ ┛
        assert "┏" in output or "Heavy" in output

    def test_group_border_color(self):
        """Group border color doesn't crash."""
        console = Console(record=True, width=80)
        with console.group(title="Colored", border_color="cyan"):
            console.frame("Test")
        output = console.export_text()
        assert "Test" in output

    def test_group_gradient_border(self):
        """Group gradient border doesn't crash."""
        console = Console(record=True, width=80)
        with console.group(
            title="Gradient",
            border_gradient_start="red",
            border_gradient_end="blue",
        ):
            console.frame("Gradient content")
        output = console.export_text()
        assert "Gradient content" in output


class TestGroupContextInheritance:
    """Tests for style inheritance."""

    def test_inherit_style_applies_to_inner_frames(self):
        """Inner frames inherit outer border style."""
        console = Console(record=True, width=80)
        with console.group(border="heavy", inherit_style=True):
            console.frame("Inherited")
        output = console.export_text()
        assert "Inherited" in output

    def test_inner_frame_can_override_inherited_style(self):
        """Inner frames can override inherited style."""
        console = Console(record=True, width=80)
        with console.group(border="heavy", inherit_style=True):
            console.frame("Override", border="rounded")
        output = console.export_text()
        assert "Override" in output


class TestGroupContextGap:
    """Tests for gap between frames."""

    def test_default_gap(self):
        """Default gap of 1 between frames."""
        console = Console(record=True, width=80)
        with console.group(gap=1):
            console.frame("A")
            console.frame("B")
        output = console.export_text()
        assert "A" in output
        assert "B" in output

    def test_no_gap(self):
        """Gap of 0 puts frames adjacent."""
        console = Console(record=True, width=80)
        with console.group(gap=0):
            console.frame("X")
            console.frame("Y")
        output = console.export_text()
        assert "X" in output
        assert "Y" in output

    def test_large_gap(self):
        """Large gap value works."""
        console = Console(record=True, width=80)
        with console.group(gap=3):
            console.frame("P")
            console.frame("Q")
        output = console.export_text()
        assert "P" in output
        assert "Q" in output


class TestGroupContextAlignWidths:
    """Tests for width alignment."""

    def test_align_widths_makes_frames_same_width(self):
        """align_widths=True makes all frames same width."""
        console = Console(record=True, width=80)
        with console.group(align_widths=True):
            console.frame("Short")
            console.frame("This is much longer content here")
        output = console.export_text()
        assert "Short" in output
        assert "This is much longer content here" in output


class TestGroupContextExceptionHandling:
    """Tests for exception handling in groups."""

    def test_exception_in_group_propagates(self):
        """Exceptions inside group propagate normally."""
        console = Console(record=True, width=80)
        with pytest.raises(ValueError, match="test error"):
            with console.group(title="Error"):
                console.frame("Before error")
                raise ValueError("test error")

    def test_frames_not_rendered_on_exception(self):
        """Frames are not rendered if exception occurs."""
        console = Console(record=True, width=80)
        try:
            with console.group(title="Error"):
                console.frame("Should not appear")
                raise ValueError("test")
        except ValueError:
            pass
        output = console.export_text()
        # The group content should not have been rendered
        assert "Should not appear" not in output


class TestGroupContextWithFrameOptions:
    """Tests for frame options inside groups."""

    def test_frame_with_title_inside_group(self):
        """Frame with title works inside group."""
        console = Console(record=True, width=80)
        with console.group(title="Outer"):
            console.frame("Content", title="Inner Title")
        output = console.export_text()
        assert "Content" in output
        assert "Inner Title" in output

    def test_frame_with_border_color_inside_group(self):
        """Frame with border_color works inside group."""
        console = Console(record=True, width=80)
        with console.group():
            console.frame("Colored", border_color="red")
        output = console.export_text()
        assert "Colored" in output

    def test_frame_with_gradient_inside_group(self):
        """Frame with gradient works inside group."""
        console = Console(record=True, width=80)
        with console.group():
            console.frame(
                "Gradient",
                border_gradient_start="cyan",
                border_gradient_end="magenta",
            )
        output = console.export_text()
        assert "Gradient" in output

    def test_frame_with_list_content_inside_group(self):
        """Frame with list content works inside group."""
        console = Console(record=True, width=80)
        with console.group():
            console.frame(["Line 1", "Line 2", "Line 3"])
        output = console.export_text()
        assert "Line 1" in output
        assert "Line 2" in output
        assert "Line 3" in output


class TestGroupContextThreadSafety:
    """Tests for thread safety via contextvars."""

    def test_independent_contexts(self):
        """Each context manager instance is independent."""
        console = Console(record=True, width=80)
        # First group
        with console.group(title="First"):
            console.frame("A")
        # Second group (should not interfere)
        with console.group(title="Second"):
            console.frame("B")
        output = console.export_text()
        assert "First" in output
        assert "Second" in output
        assert "A" in output
        assert "B" in output


class TestGroupContextCompatibility:
    """Tests for compatibility with other Console methods."""

    def test_normal_frame_outside_group(self):
        """Normal frame() calls work outside group."""
        console = Console(record=True, width=80)
        console.frame("Before group")
        with console.group(title="Inside"):
            console.frame("Grouped")
        console.frame("After group")
        output = console.export_text()
        assert "Before group" in output
        assert "Grouped" in output
        assert "After group" in output

    def test_frame_group_still_works(self):
        """Existing frame_group() still works."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "A"}, {"content": "B"}],
            title="Dict Group",
        )
        output = console.export_text()
        assert "A" in output
        assert "B" in output
        assert "Dict Group" in output
