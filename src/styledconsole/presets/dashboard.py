from typing import Any, TypedDict

from rich.panel import Panel
from typing_extensions import NotRequired

from styledconsole.console import Console


class DashboardWidget(TypedDict):
    """
    Configuration for a single dashboard widget.

    Attributes:
        title: The title of the widget.
        content: The content to display (string or renderable).
        width: Optional fixed width for the widget.
        ratio: Optional flex ratio (default: 1).
    """

    title: str
    content: str | Any
    width: NotRequired[int]
    ratio: NotRequired[int]


def dashboard(
    title: str,
    widgets: list[DashboardWidget],
    columns: int = 2,
    *,
    console: Console | None = None,
) -> None:
    """
    Render a dashboard layout with a grid of widgets.

    Args:
        title: The main title of the dashboard.
        widgets: A list of widget configurations.
        columns: Number of columns in the grid (default: 2).
        console: Optional Console instance.
    """
    if console is None:
        console = Console()

    from rich.table import Table

    # Create grid
    grid_table = Table.grid(expand=True, padding=1)
    for _ in range(columns):
        grid_table.add_column(ratio=1)

    # Add rows
    row_widgets = []
    for widget in widgets:
        panel = Panel(
            widget["content"],
            title=widget["title"],
            border_style="blue",
        )
        row_widgets.append(panel)

        if len(row_widgets) == columns:
            grid_table.add_row(*row_widgets)
            row_widgets = []

    # Add remaining widgets
    if row_widgets:
        # Pad with empty strings if row is incomplete
        while len(row_widgets) < columns:
            row_widgets.append("")
        grid_table.add_row(*row_widgets)

    # Print Header then Grid
    console.print(Panel(title, style="bold white on blue", border_style="blue", expand=True))
    console.print(grid_table)
