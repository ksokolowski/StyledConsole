"""Tests for presets/tables.py - GradientTable and table factories."""

from io import StringIO

from rich.console import Console

from styledconsole.presets.tables import (
    GradientTable,
    create_table_from_config,
)


class TestGradientTable:
    """Tests for GradientTable class."""

    def test_create_basic_gradient_table(self):
        """Create a basic GradientTable instance."""
        table = GradientTable(title="Test Table")
        assert table is not None

    def test_add_column(self):
        """Add column to GradientTable."""
        table = GradientTable()
        table.add_column("Name")
        table.add_column("Value", style="cyan")
        assert table is not None

    def test_add_row(self):
        """Add row to GradientTable."""
        table = GradientTable()
        table.add_column("Name")
        table.add_column("Value")
        table.add_row("foo", "bar")
        assert table is not None

    def test_gradient_table_with_colors(self):
        """GradientTable with gradient colors."""
        table = GradientTable(
            title="Gradient",
            border_gradient_start="cyan",
            border_gradient_end="blue",
        )
        table.add_column("Col1")
        table.add_row("value")
        assert table is not None

    def test_gradient_table_multiple_rows(self):
        """GradientTable with multiple rows for gradient effect."""
        table = GradientTable(
            border_gradient_start="green",
            border_gradient_end="yellow",
        )
        table.add_column("Index")
        table.add_column("Data")
        for i in range(5):
            table.add_row(str(i), f"Row {i}")
        assert table is not None

    def test_gradient_table_render(self):
        """Test that GradientTable renders without errors."""
        table = GradientTable(
            border_gradient_start="cyan",
            border_gradient_end="magenta",
        )
        table.add_column("Key")
        table.add_column("Value")
        table.add_row("a", "1")
        table.add_row("b", "2")

        # Render to string to exercise __rich_console__
        console = Console(file=StringIO(), force_terminal=True, width=80)
        console.print(table)
        output = console.file.getvalue()
        assert "Key" in output
        assert "Value" in output

    def test_gradient_directions(self):
        """Test different gradient directions."""
        for direction in ["horizontal", "vertical", "diagonal"]:
            table = GradientTable(
                border_gradient_direction=direction,
            )
            table.add_column("Test")
            table.add_row("data")
            assert table is not None

    def test_gradient_target_options(self):
        """Test different gradient target options."""
        for target in ["border", "content", "both"]:
            table = GradientTable(target=target)
            table.add_column("Test")
            table.add_row("data")
            assert table is not None


class TestCreateTableFromConfig:
    """Tests for create_table_from_config factory."""

    def test_basic_table_config(self):
        """Create table from basic config."""
        theme = {}
        data = {
            "columns": [{"header": "Name"}, {"header": "Age"}],
            "rows": [["Alice", "30"], ["Bob", "25"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_table_config_with_title(self):
        """Create table with title from config."""
        theme = {"title": "Users"}
        data = {
            "columns": [{"header": "Name"}],
            "rows": [["Alice"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_table_config_with_title_style(self):
        """Create table with title and title_style."""
        theme = {"title": "Users", "title_style": "bold cyan"}
        data = {
            "columns": [{"header": "Name"}],
            "rows": [["Alice"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_table_config_with_gradient(self):
        """Create gradient table from config."""
        theme = {
            "gradient": {
                "start": "cyan",
                "end": "magenta",
                "direction": "horizontal",
            }
        }
        data = {
            "columns": [{"header": "Key"}, {"header": "Value"}],
            "rows": [["a", "1"], ["b", "2"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_table_config_with_border_style(self):
        """Create table with border_style."""
        theme = {"border_style": "double"}
        data = {
            "columns": [{"header": "Test"}],
            "rows": [["data"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_empty_rows(self):
        """Table with columns but no rows."""
        theme = {}
        data = {
            "columns": [{"header": "Empty"}, {"header": "Table"}],
            "rows": [],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_column_with_style_and_justify(self):
        """Column configuration with style and justify."""
        theme = {}
        data = {
            "columns": [
                {"header": "Name", "style": "bold", "justify": "center"},
                {"header": "Value", "no_wrap": True},
            ],
            "rows": [["foo", "bar"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_cell_with_dict_format(self):
        """Row cells as dict with text and style."""
        theme = {}
        data = {
            "columns": [{"header": "Status"}],
            "rows": [[{"text": "OK", "color": "green"}]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_cell_with_icon(self):
        """Row cells with icon reference."""
        theme = {}
        data = {
            "columns": [{"header": "Status"}],
            "rows": [[{"icon": "CHECK_MARK", "text": "Done"}]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_table_with_padding(self):
        """Table with custom padding."""
        theme = {"padding": (1, 2)}
        data = {
            "columns": [{"header": "Test"}],
            "rows": [["data"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None

    def test_table_with_target(self):
        """Table with gradient target option."""
        theme = {"target": "both"}
        data = {
            "columns": [{"header": "Test"}],
            "rows": [["data"]],
        }
        table = create_table_from_config(theme, data)
        assert table is not None
