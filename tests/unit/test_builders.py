"""Unit tests for the builder layer.

Tests cover:
- FrameBuilder with all options
- BannerBuilder with all options
- TableBuilder with columns and rows
- LayoutBuilder with all directions
- Factory methods
- Validation errors
"""

from __future__ import annotations

import pytest

from styledconsole.builders import (
    BannerBuilder,
    FrameBuilder,
    LayoutBuilder,
    TableBuilder,
)
from styledconsole.model import Banner, Frame, Layout, Table, Text


class TestFrameBuilder:
    """Tests for FrameBuilder."""

    def test_simple_frame(self):
        """Build simple frame with content."""
        frame = FrameBuilder().content("Hello").build()
        assert isinstance(frame, Frame)
        assert isinstance(frame.content, Text)
        assert frame.content.content == "Hello"

    def test_frame_with_title(self):
        """Build frame with title."""
        frame = FrameBuilder().content("Body").title("Title").build()
        assert frame.title == "Title"

    def test_frame_with_effect(self):
        """Build frame with effect."""
        frame = FrameBuilder().content("X").effect("ocean").build()
        assert frame.effect == "ocean"

    def test_frame_with_border(self):
        """Build frame with border style."""
        frame = FrameBuilder().content("X").border("rounded").build()
        assert frame.border == "rounded"

    def test_frame_with_width(self):
        """Build frame with explicit width."""
        frame = FrameBuilder().content("X").width(40).build()
        assert frame.width == 40

    def test_frame_with_padding(self):
        """Build frame with custom padding."""
        frame = FrameBuilder().content("X").padding(2).build()
        assert frame.padding == 2

    def test_frame_with_align(self):
        """Build frame with alignment."""
        frame = FrameBuilder().content("X").align("center").build()
        assert frame.align == "center"

    def test_frame_with_style(self):
        """Build frame with text style."""
        frame = FrameBuilder().content("X").style(color="red", bold=True).build()
        assert frame.style is not None
        assert frame.style.color == "red"
        assert frame.style.bold is True

    def test_frame_content_list(self):
        """Build frame with list content."""
        frame = FrameBuilder().content(["Line 1", "Line 2"]).build()
        assert frame.content.content == "Line 1\nLine 2"

    def test_frame_chaining(self):
        """Builder methods return self for chaining."""
        builder = FrameBuilder()
        result = builder.content("X").title("T").border("heavy").effect("fire")
        assert result is builder

    def test_frame_validation_no_content(self):
        """Validation fails without content."""
        with pytest.raises(ValueError, match="Frame content is required"):
            FrameBuilder().build()

    def test_frame_validation_width_too_small(self):
        """Validation fails with width < 3."""
        with pytest.raises(ValueError, match="Frame width must be at least 3"):
            FrameBuilder().content("X").width(2).build()

    def test_frame_validation_negative_padding(self):
        """Validation fails with negative padding."""
        with pytest.raises(ValueError, match="Padding cannot be negative"):
            FrameBuilder().content("X").padding(-1).build()

    def test_frame_factory_info(self):
        """Info factory creates blue-ish frame."""
        frame = FrameBuilder.info("Message", "Info").build()
        assert frame.title == "Info"
        assert frame.effect == "ocean"
        assert frame.border == "rounded"

    def test_frame_factory_success(self):
        """Success factory creates green-ish frame."""
        frame = FrameBuilder.success("Done", "Success").build()
        assert frame.title == "Success"
        assert frame.effect == "forest"

    def test_frame_factory_warning(self):
        """Warning factory creates orange-ish frame."""
        frame = FrameBuilder.warning("Alert", "Warning").build()
        assert frame.title == "Warning"
        assert frame.effect == "fire"
        assert frame.border == "heavy"

    def test_frame_factory_error(self):
        """Error factory creates red frame."""
        frame = FrameBuilder.error("Failed", "Error").build()
        assert frame.title == "Error"
        assert frame.effect == "fire"
        assert frame.border == "double"


class TestBannerBuilder:
    """Tests for BannerBuilder."""

    def test_simple_banner(self):
        """Build simple banner."""
        banner = BannerBuilder().text("HELLO").build()
        assert isinstance(banner, Banner)
        assert banner.text == "HELLO"

    def test_banner_with_font(self):
        """Build banner with custom font."""
        banner = BannerBuilder().text("X").font("slant").build()
        assert banner.font == "slant"

    def test_banner_with_effect(self):
        """Build banner with effect."""
        banner = BannerBuilder().text("X").effect("fire").build()
        assert banner.effect == "fire"

    def test_banner_validation_no_text(self):
        """Validation fails without text."""
        with pytest.raises(ValueError, match="Banner text is required"):
            BannerBuilder().build()

    def test_banner_factory_title(self):
        """Title factory creates ocean banner."""
        banner = BannerBuilder.title("DEMO").build()
        assert banner.text == "DEMO"
        assert banner.effect == "ocean"

    def test_banner_factory_header(self):
        """Header factory creates slant fire banner."""
        banner = BannerBuilder.header("HEADER").build()
        assert banner.font == "slant"
        assert banner.effect == "fire"


class TestTableBuilder:
    """Tests for TableBuilder."""

    def test_simple_table(self):
        """Build simple table."""
        table = TableBuilder().columns("A", "B").add_row("1", "2").build()
        assert isinstance(table, Table)
        assert len(table.columns) == 2
        assert len(table.rows) == 1

    def test_table_with_multiple_rows(self):
        """Build table with multiple rows."""
        table = (
            TableBuilder()
            .columns("Name", "Value")
            .add_row("X", "1")
            .add_row("Y", "2")
            .add_row("Z", "3")
            .build()
        )
        assert len(table.rows) == 3

    def test_table_with_rows_method(self):
        """Build table using rows() method."""
        table = TableBuilder().columns("A", "B").rows([["1", "2"], ["3", "4"]]).build()
        assert len(table.rows) == 2

    def test_table_with_title(self):
        """Build table with title."""
        table = TableBuilder().columns("A").title("My Table").build()
        assert table.title == "My Table"

    def test_table_with_effect(self):
        """Build table with effect."""
        table = TableBuilder().columns("A").effect("steel").build()
        assert table.effect == "steel"

    def test_table_column_options(self):
        """Build table with column options."""
        table = (
            TableBuilder()
            .column("Name", width=20, align="left")
            .column("Value", width=10, align="right")
            .build()
        )
        assert table.columns[0].width == 20
        assert table.columns[1].align == "right"

    def test_table_validation_no_columns(self):
        """Validation fails without columns."""
        with pytest.raises(ValueError, match="Table must have at least one column"):
            TableBuilder().build()

    def test_table_validation_row_mismatch(self):
        """Validation fails with row/column count mismatch."""
        with pytest.raises(ValueError, match="Row has 3 cells but table has 2 columns"):
            (
                TableBuilder()
                .columns("A", "B")
                .add_row("1", "2", "3")  # Too many cells
                .build()
            )

    def test_table_factory_simple(self):
        """Simple factory creates table from data."""
        table = TableBuilder.simple(
            ["Name", "Age"],
            [["Alice", 30], ["Bob", 25]],
        ).build()
        assert len(table.columns) == 2
        assert len(table.rows) == 2

    def test_table_factory_key_value(self):
        """Key-value factory creates two-column table."""
        table = TableBuilder.key_value(
            {"name": "Alice", "age": 30},
            title="Person",
        ).build()
        assert table.title == "Person"
        assert len(table.columns) == 2
        assert table.columns[0].header == "Key"


class TestLayoutBuilder:
    """Tests for LayoutBuilder."""

    def test_vertical_layout(self):
        """Build vertical layout."""
        text1 = Text(content="A")
        text2 = Text(content="B")
        layout = LayoutBuilder().vertical().add(text1, text2).build()
        assert isinstance(layout, Layout)
        assert layout.direction == "vertical"
        assert len(layout.children) == 2

    def test_horizontal_layout(self):
        """Build horizontal layout."""
        layout = LayoutBuilder().horizontal().add(Text(content="X")).build()
        assert layout.direction == "horizontal"

    def test_grid_layout(self):
        """Build grid layout."""
        layout = LayoutBuilder().grid(columns=3).build()
        assert layout.direction == "grid"
        assert layout.columns == 3

    def test_layout_with_gap(self):
        """Build layout with gap."""
        layout = LayoutBuilder().gap(2).build()
        assert layout.gap == 2

    def test_layout_equal_width(self):
        """Build layout with equal width."""
        layout = LayoutBuilder().equal_width().build()
        assert layout.equal_width is True

    def test_layout_chaining(self):
        """Builder methods return self for chaining."""
        builder = LayoutBuilder()
        result = builder.vertical().gap(1).equal_width()
        assert result is builder

    def test_layout_validation_negative_gap(self):
        """Validation fails with negative gap."""
        with pytest.raises(ValueError, match="Gap cannot be negative"):
            LayoutBuilder().gap(-1).build()

    def test_layout_validation_zero_columns(self):
        """Validation fails with columns < 1."""
        with pytest.raises(ValueError, match="Columns must be at least 1"):
            LayoutBuilder().grid(columns=0).build()

    def test_layout_factory_row(self):
        """Row factory creates horizontal layout."""
        text = Text(content="X")
        layout = LayoutBuilder.row(text, gap=3).build()
        assert layout.direction == "horizontal"
        assert layout.gap == 3

    def test_layout_factory_column(self):
        """Column factory creates vertical layout."""
        text = Text(content="X")
        layout = LayoutBuilder.column(text, gap=2).build()
        assert layout.direction == "vertical"
        assert layout.gap == 2

    def test_layout_factory_dashboard(self):
        """Dashboard factory creates vertical layout with header."""
        header = Banner(text="HEADER")
        content = Frame(content=Text(content="Body"))
        layout = LayoutBuilder.dashboard(header, content, gap=1).build()
        assert layout.direction == "vertical"
        assert len(layout.children) == 2


class TestBuilderIntegration:
    """Integration tests for builders."""

    def test_nested_builders(self):
        """Build complex nested structure."""
        frame1 = FrameBuilder().content("Left").title("L").build()
        frame2 = FrameBuilder().content("Right").title("R").build()
        row = LayoutBuilder.row(frame1, frame2).build()

        banner = BannerBuilder().text("DASHBOARD").effect("fire").build()
        dashboard = LayoutBuilder.dashboard(banner, row).build()

        assert len(dashboard.children) == 2
        assert isinstance(dashboard.children[0], Banner)
        assert isinstance(dashboard.children[1], Layout)

    def test_builder_produces_serializable_objects(self):
        """Built objects can be serialized."""
        frame = FrameBuilder().content("Test").title("T").effect("ocean").build()
        json_str = frame.to_json()
        assert "Test" in json_str
        assert "ocean" in json_str

    def test_validate_method(self):
        """validate() returns errors without raising."""
        builder = FrameBuilder()
        errors = builder.validate()
        assert len(errors) == 1
        assert "content is required" in errors[0]
