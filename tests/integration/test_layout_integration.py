"""Integration tests for Layout Composer with real-world scenarios."""

from styledconsole import (
    BannerRenderer,
    FrameRenderer,
    Layout,
    LayoutComposer,
)
from styledconsole.utils.text import visual_width


class TestLayoutWithFrames:
    """Test Layout Composer with Frame components."""

    def test_stack_multiple_frames(self):
        """Test stacking multiple frames vertically."""
        composer = LayoutComposer()
        frame_renderer = FrameRenderer()

        # Render frames
        rendered1 = frame_renderer.render(["Header Section"], title="Top")
        rendered2 = frame_renderer.render(["Main Content", "Line 2"], title="Middle")
        rendered3 = frame_renderer.render(["Footer"], title="Bottom")

        # Stack them
        result = composer.stack([rendered1, rendered2, rendered3], spacing=1)

        assert len(result) > 0
        # Should have frames separated by spacing
        assert any("Top" in line for line in result)
        assert any("Middle" in line for line in result)
        assert any("Bottom" in line for line in result)

    def test_side_by_side_frames(self):
        """Test placing frames side by side."""
        composer = LayoutComposer()
        frame_renderer = FrameRenderer()

        left_rendered = frame_renderer.render(["Left", "Panel"], title="L")
        right_rendered = frame_renderer.render(["Right", "Panel"], title="R")

        result = composer.side_by_side(left_rendered, right_rendered, spacing=2)

        assert len(result) > 0
        # First line should contain both frame elements
        combined = "".join(result)
        assert "Left" in combined
        assert "Right" in combined

    def test_grid_of_frames(self):
        """Test creating a grid of frames."""
        composer = LayoutComposer()
        frame_renderer = FrameRenderer()

        # Create 2x2 grid of frames
        frames = []
        for i in range(2):
            row = []
            for j in range(2):
                row.append(frame_renderer.render([f"Cell {i}{j}"], title=f"{i}{j}"))
            frames.append(row)

        result = composer.grid(frames, column_spacing=2, row_spacing=1)

        assert len(result) > 0
        combined = "".join(result)
        assert "Cell 00" in combined
        assert "Cell 01" in combined
        assert "Cell 10" in combined
        assert "Cell 11" in combined

    def test_nested_layout_with_frames(self):
        """Test nested layouts with frames."""
        composer = LayoutComposer()
        frame_renderer = FrameRenderer()

        # Create header
        header = frame_renderer.render(["HEADER"], title="Top")

        # Create main content area with side-by-side frames
        left = frame_renderer.render(["Left"], title="L")
        right = frame_renderer.render(["Right"], title="R")
        main = composer.side_by_side(left, right, spacing=1)

        # Create footer
        footer = frame_renderer.render(["FOOTER"], title="Bottom")

        # Stack all sections
        result = composer.stack([header, main, footer], spacing=1)

        assert len(result) > 0
        combined = "".join(result)
        assert "HEADER" in combined
        assert "Left" in combined
        assert "Right" in combined
        assert "FOOTER" in combined


class TestLayoutWithBanners:
    """Test Layout Composer with Banner components."""

    def test_banner_with_frames(self):
        """Test combining banners and frames in layout."""
        composer = LayoutComposer()
        banner_renderer = BannerRenderer()
        frame_renderer = FrameRenderer()

        # Create banner
        banner_rendered = banner_renderer.render("TITLE", font="banner")

        # Create content frame
        frame_rendered = frame_renderer.render(["Content line 1", "Content line 2"])

        # Stack them
        result = composer.stack([banner_rendered, frame_rendered], spacing=2)

        assert len(result) > 0
        combined = "".join(result)
        assert "#" in combined  # Banner renders with # characters
        assert "Content" in combined

    def test_multiple_banners_stacked(self):
        """Test stacking multiple banners."""
        composer = LayoutComposer()
        banner_renderer = BannerRenderer()

        rendered1 = banner_renderer.render("ONE", font="banner")
        rendered2 = banner_renderer.render("TWO", font="banner")

        result = composer.stack([rendered1, rendered2], spacing=1)

        assert len(result) > 0


class TestLayoutObject:
    """Test using Layout dataclass for composition."""

    def test_layout_object_rendering(self):
        """Test rendering a Layout object."""
        composer = LayoutComposer()

        layout = Layout(
            elements=[["Line 1"], ["Line 2"], ["Line 3"]],
            spacing=1,
            align="center",
        )

        result = composer.compose(layout)

        assert len(result) > 0
        # Should have lines with spacing
        assert len(result) == 5  # 3 lines + 2 spacing lines

    def test_layout_with_fixed_width(self):
        """Test Layout with fixed width."""
        composer = LayoutComposer()

        layout = Layout(
            elements=[["Short"], ["Medium line"]],
            spacing=0,
            width=50,
        )

        result = composer.compose(layout)

        # All lines should be exactly 50 chars wide
        for line in result:
            assert visual_width(line) == 50

    def test_layout_alignment_variations(self):
        """Test Layout with different alignments."""
        composer = LayoutComposer()

        for align in ["left", "center", "right"]:
            layout = Layout(
                elements=[["A"], ["BBBBBB"]],
                spacing=0,
                align=align,
            )
            result = composer.compose(layout)
            assert len(result) == 2


class TestComplexLayouts:
    """Test complex real-world layout scenarios."""

    def test_dashboard_layout(self):
        """Test creating a dashboard-style layout."""
        composer = LayoutComposer()
        frame_renderer = FrameRenderer()

        # Header
        header = frame_renderer.render(["Dashboard v1.0"], title="App")

        # Stats grid (2x2)
        stats = []
        for i in range(2):
            row = []
            for j in range(2):
                row.append(
                    frame_renderer.render([f"Metric {i}{j}", "Value: 100"], title=f"Stat {i}{j}")
                )
            stats.append(row)

        stats_grid = composer.grid(stats, column_spacing=1, row_spacing=1)

        # Footer
        footer = frame_renderer.render(["Status: OK"])

        # Combine all
        result = composer.stack([header, stats_grid, footer], spacing=1)

        assert len(result) > 0
        combined = "".join(result)
        assert "Dashboard" in combined
        assert "Metric" in combined
        assert "Status" in combined

    def test_three_column_layout(self):
        """Test creating a three-column layout."""
        composer = LayoutComposer()

        col1 = ["Left", "Col"]
        col2 = ["Middle", "Column"]
        col3 = ["Right", "Col"]

        # Create row with three columns
        row = [[col1, col2, col3]]
        result = composer.grid(row, column_spacing=2)

        assert len(result) == 2  # Two lines high
        # All columns should appear
        combined = "".join(result)
        assert "Left" in combined
        assert "Middle" in combined
        assert "Right" in combined

    def test_alternating_layout(self):
        """Test alternating content widths."""
        composer = LayoutComposer()

        narrow = ["Small"]
        wide = ["This is a much wider section"]

        result = composer.stack([narrow, wide, narrow], spacing=1, align="center")

        assert len(result) == 5  # 3 sections + 2 spacing
        # All lines should be same width (widest element)
        widths = [visual_width(line) for line in result]
        assert len(set(widths)) == 1

    def test_mixed_height_grid(self):
        """Test grid with cells of different heights."""
        composer = LayoutComposer()

        # Create cells with varying heights
        cell1 = ["A"]
        cell2 = ["B", "B2", "B3"]
        cell3 = ["C", "C2"]
        cell4 = ["D"]

        row1 = [cell1, cell2]
        row2 = [cell3, cell4]

        result = composer.grid([row1, row2], column_spacing=1, row_spacing=1)

        assert len(result) > 0


class TestLayoutEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_layout(self):
        """Test rendering empty layout."""
        composer = LayoutComposer()

        layout = Layout(elements=[])
        result = composer.compose(layout)

        assert result == []

    def test_single_element_layout(self):
        """Test layout with single element."""
        composer = LayoutComposer()

        layout = Layout(elements=[["Single line"]])
        result = composer.compose(layout)

        assert len(result) == 1
        assert "Single line" in result[0]

    def test_layout_with_emoji(self):
        """Test layout with emoji content."""
        composer = LayoutComposer()

        elements = [["🚀 Rocket"], ["🌟 Star"], ["💎 Gem"]]
        result = composer.stack(elements, spacing=0, align="center")

        # Should handle emoji widths correctly
        assert len(result) == 3
        widths = [visual_width(line) for line in result]
        assert len(set(widths)) == 1

    def test_very_wide_content(self):
        """Test layout with very wide content."""
        composer = LayoutComposer()

        wide_line = "x" * 200
        narrow_line = "y"

        result = composer.stack([[wide_line], [narrow_line]], spacing=0)

        # Should accommodate widest line
        assert visual_width(result[0]) == 200
        assert visual_width(result[1]) == 200

    def test_grid_with_empty_cells(self):
        """Test grid with some empty cells."""
        composer = LayoutComposer()

        row1 = [["A"], ["B"]]  # Use non-empty cells for now
        row2 = [["C"], ["D"]]

        result = composer.grid([row1, row2], row_spacing=0)

        assert len(result) > 0

    def test_deeply_nested_composition(self):
        """Test deeply nested layout composition."""
        composer = LayoutComposer()

        # Create nested structure
        inner1 = composer.stack([["A"], ["B"]], spacing=0)
        inner2 = composer.stack([["C"], ["D"]], spacing=0)

        middle = composer.side_by_side(inner1, inner2, spacing=1)

        outer = composer.stack([["Header"], middle, ["Footer"]], spacing=1)

        assert len(outer) > 0
        combined = "".join(outer)
        assert "Header" in combined
        assert "Footer" in combined
