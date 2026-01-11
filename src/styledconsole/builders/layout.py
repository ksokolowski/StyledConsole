"""LayoutBuilder for constructing Layout objects with a fluent API.

Example:
    >>> from styledconsole.builders import LayoutBuilder, FrameBuilder
    >>>
    >>> # Vertical layout
    >>> layout = (LayoutBuilder()
    ...     .vertical()
    ...     .gap(1)
    ...     .add(frame1)
    ...     .add(frame2)
    ...     .build())
    >>>
    >>> # Horizontal layout
    >>> row = (LayoutBuilder()
    ...     .horizontal()
    ...     .gap(2)
    ...     .add(left_frame, right_frame)
    ...     .build())
    >>>
    >>> # Grid layout
    >>> grid = (LayoutBuilder()
    ...     .grid(columns=3)
    ...     .add(item1, item2, item3, item4, item5, item6)
    ...     .build())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from styledconsole.builders.base import BaseBuilder
from styledconsole.model import Layout, Style

if TYPE_CHECKING:
    from styledconsole.model import ConsoleObject


class LayoutBuilder(BaseBuilder[Layout]):
    """Fluent builder for Layout objects.

    Provides a chainable API for arranging ConsoleObjects in
    vertical, horizontal, or grid layouts.

    Example:
        >>> layout = (LayoutBuilder()
        ...     .horizontal()
        ...     .gap(2)
        ...     .equal_width()
        ...     .add(frame1, frame2)
        ...     .build())
    """

    def __init__(self) -> None:
        """Initialize builder with default values."""
        self._children: list[ConsoleObject] = []
        self._direction: Literal["vertical", "horizontal", "grid"] = "vertical"
        self._gap: int = 0
        self._columns: int | None = None
        self._equal_width: bool = False
        self._style: Style | None = None

    def add(self, *children: ConsoleObject) -> LayoutBuilder:
        """Add child objects.

        Args:
            *children: ConsoleObjects to add to layout.

        Returns:
            Self for chaining.
        """
        self._children.extend(children)
        return self

    def direction(self, direction: Literal["vertical", "horizontal", "grid"]) -> LayoutBuilder:
        """Set layout direction.

        Args:
            direction: Layout direction.

        Returns:
            Self for chaining.
        """
        self._direction = direction
        return self

    def vertical(self) -> LayoutBuilder:
        """Set vertical (stacked) layout.

        Returns:
            Self for chaining.
        """
        self._direction = "vertical"
        return self

    def horizontal(self) -> LayoutBuilder:
        """Set horizontal (side-by-side) layout.

        Returns:
            Self for chaining.
        """
        self._direction = "horizontal"
        return self

    def grid(self, columns: int | None = None) -> LayoutBuilder:
        """Set grid layout.

        Args:
            columns: Number of columns. None for auto.

        Returns:
            Self for chaining.
        """
        self._direction = "grid"
        if columns is not None:
            self._columns = columns
        return self

    def gap(self, gap: int) -> LayoutBuilder:
        """Set gap between children.

        Args:
            gap: Gap size (lines for vertical, spaces for horizontal).

        Returns:
            Self for chaining.
        """
        self._gap = gap
        return self

    def columns(self, columns: int) -> LayoutBuilder:
        """Set number of columns for grid layout.

        Args:
            columns: Number of columns.

        Returns:
            Self for chaining.
        """
        self._columns = columns
        return self

    def equal_width(self, enabled: bool = True) -> LayoutBuilder:
        """Enable equal width for children.

        Args:
            enabled: Whether to enable equal width.

        Returns:
            Self for chaining.
        """
        self._equal_width = enabled
        return self

    def _validate(self) -> list[str]:
        """Validate builder state."""
        errors = []
        if self._gap < 0:
            errors.append("Gap cannot be negative")
        if self._columns is not None and self._columns < 1:
            errors.append("Columns must be at least 1")
        return errors

    def _build(self) -> Layout:
        """Build the Layout object."""
        return Layout(
            children=tuple(self._children),
            direction=self._direction,
            gap=self._gap,
            columns=self._columns,
            equal_width=self._equal_width,
            style=self._style,
        )

    # Factory methods

    @classmethod
    def row(cls, *children: ConsoleObject, gap: int = 2) -> LayoutBuilder:
        """Create a horizontal row.

        Args:
            *children: Child objects.
            gap: Gap between children.

        Returns:
            Configured LayoutBuilder.
        """
        return cls().horizontal().gap(gap).add(*children)

    @classmethod
    def column(cls, *children: ConsoleObject, gap: int = 1) -> LayoutBuilder:
        """Create a vertical column.

        Args:
            *children: Child objects.
            gap: Gap between children.

        Returns:
            Configured LayoutBuilder.
        """
        return cls().vertical().gap(gap).add(*children)

    @classmethod
    def dashboard(
        cls,
        header: ConsoleObject,
        *content: ConsoleObject,
        gap: int = 1,
    ) -> LayoutBuilder:
        """Create a dashboard layout with header and content.

        Args:
            header: Header object (typically a Banner).
            *content: Content objects.
            gap: Gap between elements.

        Returns:
            Configured LayoutBuilder.
        """
        return cls().vertical().gap(gap).add(header, *content)


__all__ = ["LayoutBuilder"]
