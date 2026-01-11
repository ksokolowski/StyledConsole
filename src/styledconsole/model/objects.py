"""Concrete ConsoleObject types for the model layer.

This module defines all renderable object types:
- Text: Plain or styled text content
- Frame: Bordered frame/panel containing content
- Banner: ASCII art banner text
- Table: Tabular data display
- Layout: Container for arranging multiple objects
- Group: Logical grouping without visual container
- Spacer: Empty space for layout purposes
- Rule: Horizontal rule/divider

All objects are immutable (frozen dataclasses) and output-agnostic.

Example:
    >>> from styledconsole.model import Text, Frame, Layout
    >>>
    >>> # Simple text
    >>> text = Text(content="Hello World")
    >>>
    >>> # Frame with nested content
    >>> frame = Frame(
    ...     content=Text(content="Status: OK"),
    ...     title="System",
    ...     effect="ocean",
    ... )
    >>>
    >>> # Layout combining multiple objects
    >>> layout = Layout(
    ...     children=(frame, Text(content="Footer")),
    ...     direction="vertical",
    ... )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Literal

from styledconsole.model.base import ConsoleObject, Style

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class Text(ConsoleObject):
    """Plain or styled text content.

    The simplest ConsoleObject - represents a string of text with optional styling.

    Attributes:
        content: The text content to display.
        style: Optional Style for text formatting.

    Example:
        >>> text = Text(content="Hello World")
        >>> styled = Text(content="Error!", style=Style(color="red", bold=True))
    """

    _type: ClassVar[str] = "text"

    content: str = ""

    def _content_to_dict(self) -> dict[str, Any]:
        return {"content": self.content}


@dataclass(frozen=True)
class Frame(ConsoleObject):
    """Bordered frame/panel containing content.

    A visual container with a border, optional title, and visual effects.

    Attributes:
        content: The ConsoleObject to display inside the frame.
        title: Optional title displayed in the border.
        subtitle: Optional subtitle displayed below the title.
        border: Border style name (e.g., "solid", "rounded", "heavy").
        effect: Visual effect (gradient, rainbow, etc.) as string preset or EffectSpec.
        width: Explicit width. None for auto-width.
        padding: Internal padding (spaces around content).
        align: Content alignment within the frame.

    Example:
        >>> from styledconsole.model import Frame, Text
        >>>
        >>> frame = Frame(
        ...     content=Text(content="Hello"),
        ...     title="Greeting",
        ...     border="rounded",
        ...     effect="ocean",
        ... )
    """

    _type: ClassVar[str] = "frame"

    content: ConsoleObject | None = None
    title: str | None = None
    subtitle: str | None = None
    border: str = "solid"
    effect: str | None = None  # Preset name or None; EffectSpec handled at render time
    width: int | None = None
    padding: int = 1
    align: Literal["left", "center", "right"] = "left"

    def _content_to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.content is not None:
            result["content"] = self.content.to_dict()
        if self.title is not None:
            result["title"] = self.title
        if self.subtitle is not None:
            result["subtitle"] = self.subtitle
        if self.border != "solid":
            result["border"] = self.border
        if self.effect is not None:
            result["effect"] = self.effect
        if self.width is not None:
            result["width"] = self.width
        if self.padding != 1:
            result["padding"] = self.padding
        if self.align != "left":
            result["align"] = self.align
        return result


@dataclass(frozen=True)
class Banner(ConsoleObject):
    """ASCII art banner text.

    Renders text as large ASCII art using pyfiglet fonts.

    Attributes:
        text: Text to render as ASCII art.
        font: Pyfiglet font name (e.g., "standard", "slant", "banner").
        effect: Visual effect (gradient, rainbow, etc.).

    Example:
        >>> banner = Banner(text="HELLO", effect="fire")
        >>> banner = Banner(text="Welcome", font="slant", effect="ocean")
    """

    _type: ClassVar[str] = "banner"

    text: str = ""
    font: str = "standard"
    effect: str | None = None

    def _content_to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"text": self.text}
        if self.font != "standard":
            result["font"] = self.font
        if self.effect is not None:
            result["effect"] = self.effect
        return result


@dataclass(frozen=True)
class Column:
    """Table column definition.

    Attributes:
        header: Column header text.
        width: Column width. None for auto-width.
        align: Content alignment within column.
        style: Optional style for column content.
    """

    header: str
    width: int | None = None
    align: Literal["left", "center", "right"] = "left"
    style: Style | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        result: dict[str, Any] = {"header": self.header}
        if self.width is not None:
            result["width"] = self.width
        if self.align != "left":
            result["align"] = self.align
        if self.style is not None:
            style_dict = self.style.to_dict()
            if style_dict:
                result["style"] = style_dict
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Column:
        """Create Column from dictionary."""
        return cls(
            header=data["header"],
            width=data.get("width"),
            align=data.get("align", "left"),
            style=Style.from_dict(data["style"]) if "style" in data else None,
        )


@dataclass(frozen=True)
class Table(ConsoleObject):
    """Tabular data display.

    Displays data in a structured table with columns and rows.

    Attributes:
        columns: Column definitions as tuple of Column objects.
        rows: Data rows as tuple of tuples (each row is a tuple of cells).
        title: Optional table title.
        border: Border style name.
        effect: Visual effect for the table.

    Example:
        >>> from styledconsole.model import Table, Column
        >>>
        >>> table = Table(
        ...     columns=(
        ...         Column(header="Name", width=20),
        ...         Column(header="Status", align="center"),
        ...     ),
        ...     rows=(
        ...         ("API Server", "Online"),
        ...         ("Database", "Online"),
        ...     ),
        ...     title="Services",
        ...     effect="steel",
        ... )
    """

    _type: ClassVar[str] = "table"

    columns: tuple[Column, ...] = field(default_factory=tuple)
    rows: tuple[tuple[Any, ...], ...] = field(default_factory=tuple)
    title: str | None = None
    border: str = "solid"
    effect: str | None = None

    def _content_to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.columns:
            result["columns"] = [col.to_dict() for col in self.columns]
        if self.rows:
            result["rows"] = [list(row) for row in self.rows]
        if self.title is not None:
            result["title"] = self.title
        if self.border != "solid":
            result["border"] = self.border
        if self.effect is not None:
            result["effect"] = self.effect
        return result


@dataclass(frozen=True)
class Layout(ConsoleObject):
    """Container for arranging multiple objects.

    Arranges child objects in a specified direction with configurable gaps.

    Attributes:
        children: Child objects to arrange.
        direction: Layout direction ("vertical", "horizontal", "grid").
        gap: Space between children.
        columns: Number of columns for grid layout.
        equal_width: Make all children equal width.

    Example:
        >>> from styledconsole.model import Layout, Frame, Text
        >>>
        >>> # Vertical layout
        >>> layout = Layout(
        ...     children=(
        ...         Frame(content=Text(content="Top")),
        ...         Frame(content=Text(content="Bottom")),
        ...     ),
        ...     direction="vertical",
        ...     gap=1,
        ... )
        >>>
        >>> # Horizontal layout
        >>> row = Layout(
        ...     children=(frame1, frame2, frame3),
        ...     direction="horizontal",
        ...     gap=2,
        ... )
        >>>
        >>> # Grid layout
        >>> grid = Layout(
        ...     children=(item1, item2, item3, item4),
        ...     direction="grid",
        ...     columns=2,
        ... )
    """

    _type: ClassVar[str] = "layout"

    children: tuple[ConsoleObject, ...] = field(default_factory=tuple)
    direction: Literal["vertical", "horizontal", "grid"] = "vertical"
    gap: int = 0
    columns: int | None = None
    equal_width: bool = False

    def _content_to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        if self.direction != "vertical":
            result["direction"] = self.direction
        if self.gap != 0:
            result["gap"] = self.gap
        if self.columns is not None:
            result["columns"] = self.columns
        if self.equal_width:
            result["equal_width"] = True
        return result


@dataclass(frozen=True)
class Group(ConsoleObject):
    """Logical grouping without visual container.

    Groups multiple objects together without adding visual elements.
    Useful for treating multiple objects as a single unit.

    Attributes:
        children: Objects in this group.

    Example:
        >>> group = Group(children=(text1, text2, text3))
    """

    _type: ClassVar[str] = "group"

    children: tuple[ConsoleObject, ...] = field(default_factory=tuple)

    def _content_to_dict(self) -> dict[str, Any]:
        if self.children:
            return {"children": [child.to_dict() for child in self.children]}
        return {}


@dataclass(frozen=True)
class Spacer(ConsoleObject):
    """Empty space for layout purposes.

    Adds vertical blank lines for spacing.

    Attributes:
        lines: Number of blank lines.

    Example:
        >>> spacer = Spacer(lines=2)
    """

    _type: ClassVar[str] = "spacer"

    lines: int = 1

    def _content_to_dict(self) -> dict[str, Any]:
        if self.lines != 1:
            return {"lines": self.lines}
        return {}


@dataclass(frozen=True)
class Rule(ConsoleObject):
    """Horizontal rule/divider.

    Renders a horizontal line, optionally with a title.

    Attributes:
        title: Optional title displayed in the rule.
        style: Style for the rule.

    Example:
        >>> rule = Rule()  # Simple line
        >>> rule = Rule(title="Section 2", style=Style(color="cyan"))
    """

    _type: ClassVar[str] = "rule"

    title: str | None = None

    def _content_to_dict(self) -> dict[str, Any]:
        if self.title is not None:
            return {"title": self.title}
        return {}


__all__ = [
    "Banner",
    "Column",
    "Frame",
    "Group",
    "Layout",
    "Rule",
    "Spacer",
    "Table",
    "Text",
]
