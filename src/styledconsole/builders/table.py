"""TableBuilder for constructing Table objects with a fluent API.

Example:
    >>> from styledconsole.builders import TableBuilder
    >>>
    >>> table = (TableBuilder()
    ...     .columns("Name", "Status", "Uptime")
    ...     .add_row("API", "Online", "14d 3h")
    ...     .add_row("Database", "Online", "14d 3h")
    ...     .title("Services")
    ...     .effect("steel")
    ...     .build())
"""

from __future__ import annotations

from typing import Any

from styledconsole.builders.base import BaseBuilder, _resolve_effect
from styledconsole.model import Column, Style, Table


class TableBuilder(BaseBuilder[Table]):
    """Fluent builder for Table objects.

    Provides a chainable API for constructing tables with columns,
    rows, titles, and effects.

    Example:
        >>> table = (TableBuilder()
        ...     .columns("Name", "Value")
        ...     .add_row("CPU", "45%")
        ...     .add_row("Memory", "72%")
        ...     .title("System Stats")
        ...     .build())
    """

    def __init__(self) -> None:
        """Initialize builder with default values."""
        self._columns: list[Column] = []
        self._rows: list[tuple[Any, ...]] = []
        self._title: str | None = None
        self._border: str = "solid"
        self._effect: str | None = None
        self._style: Style | None = None

    def columns(self, *headers: str | Column) -> TableBuilder:
        """Set table columns.

        Args:
            *headers: Column headers as strings or Column objects.

        Returns:
            Self for chaining.
        """
        self._columns = [col if isinstance(col, Column) else Column(header=col) for col in headers]
        return self

    def column(
        self,
        header: str,
        width: int | None = None,
        align: str = "left",
    ) -> TableBuilder:
        """Add a column with options.

        Args:
            header: Column header text.
            width: Column width. None for auto.
            align: Content alignment ("left", "center", "right").

        Returns:
            Self for chaining.
        """
        self._columns.append(Column(header=header, width=width, align=align))  # type: ignore[arg-type]
        return self

    def add_row(self, *cells: Any) -> TableBuilder:
        """Add a data row.

        Args:
            *cells: Cell values for each column.

        Returns:
            Self for chaining.
        """
        self._rows.append(tuple(cells))
        return self

    def rows(self, rows: list[list[Any]] | list[tuple[Any, ...]]) -> TableBuilder:
        """Set all rows at once.

        Args:
            rows: List of rows, where each row is a list/tuple of cell values.

        Returns:
            Self for chaining.
        """
        self._rows = [tuple(row) for row in rows]
        return self

    def title(self, title: str) -> TableBuilder:
        """Set table title.

        Args:
            title: Title text displayed above the table.

        Returns:
            Self for chaining.
        """
        self._title = title
        return self

    def border(self, border: str) -> TableBuilder:
        """Set border style.

        Args:
            border: Border style name.

        Returns:
            Self for chaining.
        """
        self._border = border
        return self

    def effect(self, effect: str | None) -> TableBuilder:
        """Set visual effect.

        Args:
            effect: Effect preset name or None.

        Returns:
            Self for chaining.
        """
        self._effect = _resolve_effect(effect)
        return self

    def style(self, color: str | None = None, bold: bool = False) -> TableBuilder:
        """Set default text style.

        Args:
            color: Text color.
            bold: Bold text.

        Returns:
            Self for chaining.
        """
        self._style = Style(color=color, bold=bold)
        return self

    def _validate(self) -> list[str]:
        """Validate builder state."""
        errors = []
        if not self._columns:
            errors.append("Table must have at least one column")
        for row in self._rows:
            if len(row) != len(self._columns):
                errors.append(
                    f"Row has {len(row)} cells but table has {len(self._columns)} columns"
                )
                break
        return errors

    def _build(self) -> Table:
        """Build the Table object."""
        return Table(
            columns=tuple(self._columns),
            rows=tuple(self._rows),
            title=self._title,
            border=self._border,
            effect=self._effect,
            style=self._style,
        )

    # Factory methods

    @classmethod
    def simple(cls, headers: list[str], data: list[list[Any]]) -> TableBuilder:
        """Create a simple table from headers and data.

        Args:
            headers: Column header strings.
            data: List of row data.

        Returns:
            Configured TableBuilder.
        """
        return cls().columns(*headers).rows(data)

    @classmethod
    def key_value(cls, data: dict[str, Any], title: str | None = None) -> TableBuilder:
        """Create a key-value table.

        Args:
            data: Dictionary of key-value pairs.
            title: Optional table title.

        Returns:
            Configured TableBuilder.
        """
        builder = cls().columns("Key", "Value")
        for key, value in data.items():
            builder.add_row(key, value)
        if title:
            builder.title(title)
        return builder


__all__ = ["TableBuilder"]
