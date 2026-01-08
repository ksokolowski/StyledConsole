"""Dashboard layout preset for StyledConsole.

Provides a grid-based dashboard layout using Console API methods.
"""

from typing import Any, TypedDict

from typing_extensions import NotRequired

from styledconsole.console import Console


class DashboardWidget(TypedDict):
    """
    Configuration for a single dashboard widget.

    Attributes:
        title: The title of the widget.
        content: The content to display (string or list of strings).
        border_color: Optional border color for the widget (default: secondary).
            Supports semantic names (primary, success, error, etc.) for theme support.
        width: Optional fixed width for the widget.
        ratio: Optional flex ratio (default: 1).
    """

    title: str
    content: str | list[str] | Any
    border_color: NotRequired[str]
    width: NotRequired[int]
    ratio: NotRequired[int]


def dashboard(
    title: str,
    widgets: list[DashboardWidget],
    columns: int = 2,
    *,
    header_color: str = "primary",
    console: Console | None = None,
) -> None:
    """
    Render a dashboard layout with a grid of widgets.

    Uses Console API methods for rendering to maintain architectural consistency.
    Widget content is rendered using console.render_frame(), and grid layout
    is achieved through Rich's Table.grid accessed via console.print().

    Args:
        title: The main title of the dashboard.
        widgets: A list of widget configurations.
        columns: Number of columns in the grid (default: 2).
        header_color: Color for the header frame border (default: blue).
        console: Optional Console instance.

    Example:
        >>> from styledconsole import Console
        >>> from styledconsole.presets.dashboard import dashboard, DashboardWidget
        >>> widgets = [
        ...     {"title": "CPU", "content": "Usage: 45%"},
        ...     {"title": "Memory", "content": "Used: 8GB / 16GB"},
        ... ]
        >>> dashboard("System Monitor", widgets)
    """
    if console is None:
        console = Console()

    # Import Rich Table only for grid layout (accessed via console.print pass-through)
    from rich.table import Table
    from rich.text import Text

    # Import patched_cell_len from table module for emoji width fix
    from styledconsole.table import _patched_cell_len

    # Render header using Console frame method
    console.frame(
        title,
        border="rounded",
        border_color=header_color,
        align="center",
    )

    # Use patched cell_len context for proper emoji width in grid layout
    with _patched_cell_len():
        # Create grid for widget layout
        grid_table = Table.grid(expand=True, padding=1)
        for _ in range(columns):
            grid_table.add_column(ratio=1)

        # Render each widget using Console API and collect for grid
        row_widgets: list[str | Text] = []
        for widget in widgets:
            widget_border_color = widget.get("border_color", "secondary")
            widget_content = widget["content"]

            # Normalize content to string or list
            if isinstance(widget_content, (str, list)):
                # Render widget frame using Console API
                rendered = console.render_frame(
                    widget_content,
                    title=widget["title"],
                    border="rounded",
                    border_color=widget_border_color,
                    title_color=widget_border_color,
                )
                row_widgets.append(Text.from_ansi(rendered))
            else:
                # For Rich renderables, wrap in a simple text representation
                # (backwards compatibility for complex content)
                row_widgets.append(Text(str(widget_content)))

            if len(row_widgets) == columns:
                grid_table.add_row(*row_widgets)
                row_widgets = []

        # Add remaining widgets if row is incomplete
        if row_widgets:
            while len(row_widgets) < columns:
                row_widgets.append(Text(""))
            grid_table.add_row(*row_widgets)

        # Print grid using Console's Rich pass-through
        console.print(grid_table)
