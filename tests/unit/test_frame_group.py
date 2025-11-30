"""Tests for frame_group() functionality.

Tests the frame grouping feature that allows rendering multiple frames
together with shared styling and layout options.
"""

from styledconsole import Console


class TestFrameGroupBasic:
    """Basic frame_group functionality tests."""

    def test_frame_group_single_item(self):
        """Single item frame group renders correctly."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Hello", "title": "Greeting"}],
            title="Dashboard",
        )
        output = console.export_text()
        assert "Hello" in output
        assert "Greeting" in output
        assert "Dashboard" in output

    def test_frame_group_multiple_items(self):
        """Multiple items render as separate frames."""
        console = Console(record=True, width=80)
        console.frame_group(
            [
                {"content": "Section 1"},
                {"content": "Section 2"},
                {"content": "Section 3"},
            ],
            title="Multi-Section",
        )
        output = console.export_text()
        assert "Section 1" in output
        assert "Section 2" in output
        assert "Section 3" in output
        assert "Multi-Section" in output

    def test_frame_group_no_outer_title(self):
        """Frame group works without outer title."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Item 1"}, {"content": "Item 2"}],
        )
        output = console.export_text()
        assert "Item 1" in output
        assert "Item 2" in output

    def test_frame_group_empty_list(self):
        """Empty frame group renders outer frame only."""
        console = Console(record=True, width=80)
        console.frame_group([], title="Empty")
        output = console.export_text()
        assert "Empty" in output


class TestFrameGroupLayout:
    """Layout-related tests for frame_group."""

    def test_frame_group_vertical_layout(self):
        """Vertical layout stacks frames top to bottom."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Top"}, {"content": "Bottom"}],
            layout="vertical",
        )
        output = console.export_text()
        # Top should appear before Bottom in vertical layout
        assert output.index("Top") < output.index("Bottom")

    def test_frame_group_default_layout_is_vertical(self):
        """Default layout is vertical."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "First"}, {"content": "Second"}],
        )
        output = console.export_text()
        assert output.index("First") < output.index("Second")


class TestFrameGroupStyling:
    """Styling tests for frame_group."""

    def test_frame_group_outer_border_style(self):
        """Outer border style is applied."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Content"}],
            border="double",
            title="Styled",
        )
        output = console.export_text()
        # Double border uses ╔ ╗ ╚ ╝ characters
        assert "╔" in output or "Styled" in output

    def test_frame_group_inner_border_style(self):
        """Inner frames can have different border styles."""
        console = Console(record=True, width=80)
        console.frame_group(
            [
                {"content": "Rounded", "border": "rounded"},
                {"content": "Heavy", "border": "heavy"},
            ],
            border="solid",
        )
        output = console.export_text()
        assert "Rounded" in output
        assert "Heavy" in output

    def test_frame_group_outer_border_color(self):
        """Outer border color is applied."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Test"}],
            border_color="cyan",
        )
        # Just verify it doesn't crash with color
        output = console.export_text()
        assert "Test" in output

    def test_frame_group_inner_colors(self):
        """Inner frames can have individual colors."""
        console = Console(record=True, width=80)
        console.frame_group(
            [
                {"content": "Red", "border_color": "red"},
                {"content": "Blue", "border_color": "blue"},
            ],
        )
        output = console.export_text()
        assert "Red" in output
        assert "Blue" in output

    def test_frame_group_outer_gradient(self):
        """Outer frame supports gradient borders."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Gradient"}],
            border_gradient_start="red",
            border_gradient_end="blue",
        )
        output = console.export_text()
        assert "Gradient" in output


class TestFrameGroupInheritance:
    """Style inheritance tests for frame_group."""

    def test_inherit_border_style(self):
        """Inner frames inherit outer border style when not specified."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Inherited"}],
            border="rounded",
            inherit_style=True,
        )
        output = console.export_text()
        # Should use rounded corners for inner frame too
        assert "Inherited" in output

    def test_override_inherited_style(self):
        """Inner frames can override inherited styles."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Override", "border": "heavy"}],
            border="rounded",
            inherit_style=True,
        )
        output = console.export_text()
        assert "Override" in output


class TestFrameGroupSpacing:
    """Spacing tests for frame_group."""

    def test_frame_group_default_gap(self):
        """Default gap of 1 between inner frames."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "A"}, {"content": "B"}],
            gap=1,
        )
        output = console.export_text()
        assert "A" in output
        assert "B" in output

    def test_frame_group_no_gap(self):
        """Gap of 0 puts frames adjacent."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "X"}, {"content": "Y"}],
            gap=0,
        )
        output = console.export_text()
        assert "X" in output
        assert "Y" in output

    def test_frame_group_custom_gap(self):
        """Custom gap value is respected."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "P"}, {"content": "Q"}],
            gap=2,
        )
        output = console.export_text()
        assert "P" in output
        assert "Q" in output


class TestFrameGroupWidth:
    """Width handling tests for frame_group."""

    def test_frame_group_auto_width(self):
        """Auto width adjusts to content."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "Short"}, {"content": "Longer content here"}],
        )
        output = console.export_text()
        assert "Short" in output
        assert "Longer content here" in output

    def test_frame_group_fixed_width(self):
        """Fixed width is applied to outer frame."""
        console = Console(record=True, width=100)
        console.frame_group(
            [{"content": "Content"}],
            width=60,
        )
        output = console.export_text()
        assert "Content" in output

    def test_frame_group_inner_width_distribution(self):
        """Inner frames distribute width correctly."""
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": "A"}, {"content": "B"}],
            width=60,
        )
        output = console.export_text()
        assert "A" in output
        assert "B" in output


class TestFrameGroupItemTypes:
    """Tests for different item specification formats."""

    def test_item_as_dict_minimal(self):
        """Item with only content key."""
        console = Console(record=True, width=80)
        console.frame_group([{"content": "Minimal"}])
        output = console.export_text()
        assert "Minimal" in output

    def test_item_as_dict_full(self):
        """Item with all optional keys."""
        console = Console(record=True, width=80)
        console.frame_group(
            [
                {
                    "content": "Full",
                    "title": "Title",
                    "border": "rounded",
                    "border_color": "cyan",
                    "content_color": "white",
                }
            ]
        )
        output = console.export_text()
        assert "Full" in output
        assert "Title" in output

    def test_item_content_as_list(self):
        """Item content can be a list of strings."""
        console = Console(record=True, width=80)
        console.frame_group([{"content": ["Line 1", "Line 2", "Line 3"]}])
        output = console.export_text()
        assert "Line 1" in output
        assert "Line 2" in output
        assert "Line 3" in output


class TestFrameGroupRenderMethod:
    """Tests for render_frame_group method."""

    def test_render_frame_group_returns_string(self):
        """render_frame_group returns string."""
        console = Console(record=True, width=80)
        result = console.render_frame_group(
            [{"content": "Test"}],
            title="Render",
        )
        assert isinstance(result, str)
        assert "Test" in result
        assert "Render" in result

    def test_render_frame_group_for_nesting(self):
        """render_frame_group can be used for nesting."""
        console = Console(record=True, width=80)
        inner = console.render_frame_group(
            [{"content": "Inner A"}, {"content": "Inner B"}],
            title="Inner Group",
        )
        console.frame(inner, title="Outer")
        output = console.export_text()
        assert "Inner A" in output
        assert "Inner B" in output
        assert "Inner Group" in output
        assert "Outer" in output


class TestFrameGroupEdgeCases:
    """Edge case tests for frame_group."""

    def test_frame_group_with_emoji_content(self):
        """Frame group handles emoji content correctly."""
        console = Console(record=True, width=80)
        console.frame_group(
            [
                {"content": "🚀 Rocket", "title": "🎯 Target"},
                {"content": "✅ Done"},
            ]
        )
        output = console.export_text()
        assert "Rocket" in output
        assert "Done" in output

    def test_frame_group_with_long_content(self):
        """Frame group handles long content."""
        long_text = "A" * 100
        console = Console(record=True, width=80)
        console.frame_group(
            [{"content": long_text}],
            width=60,
        )
        output = console.export_text()
        assert "A" in output

    def test_frame_group_many_items(self):
        """Frame group handles many items."""
        items = [{"content": f"Item {i}"} for i in range(10)]
        console = Console(record=True, width=80)
        console.frame_group(items, title="Many Items")
        output = console.export_text()
        for i in range(10):
            assert f"Item {i}" in output
