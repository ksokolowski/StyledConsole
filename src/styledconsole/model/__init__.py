"""Model layer for StyledConsole - output-agnostic object representations.

This module provides immutable, serializable objects that describe console output
without being tied to any specific rendering backend.

Core Concepts:
- **ConsoleObject**: Base class for all renderable objects
- **Style**: Text styling attributes (color, bold, etc.)
- **Object Types**: Text, Frame, Banner, Table, Layout, Group, Spacer, Rule

Key Features:
- Immutable (frozen dataclasses)
- Serializable to/from JSON and YAML
- Composable (nested structures)
- Output-agnostic (rendering handled separately)

Example:
    >>> from styledconsole.model import Text, Frame, Layout, Style
    >>>
    >>> # Create styled text
    >>> text = Text(content="Hello World", style=Style(color="cyan", bold=True))
    >>>
    >>> # Create a frame with content
    >>> frame = Frame(
    ...     content=text,
    ...     title="Greeting",
    ...     border="rounded",
    ...     effect="ocean",
    ... )
    >>>
    >>> # Combine in a layout
    >>> layout = Layout(
    ...     children=(frame, Text(content="Footer")),
    ...     direction="vertical",
    ...     gap=1,
    ... )
    >>>
    >>> # Serialize to JSON
    >>> print(layout.to_json())
    >>>
    >>> # Deserialize from dict
    >>> from styledconsole.model import create_object
    >>> obj = create_object({
    ...     "type": "frame",
    ...     "title": "Status",
    ...     "content": {"type": "text", "content": "OK"},
    ... })
"""

from styledconsole.model.base import ConsoleObject, Style
from styledconsole.model.objects import (
    Banner,
    Column,
    Frame,
    Group,
    Layout,
    Rule,
    Spacer,
    Table,
    Text,
)
from styledconsole.model.registry import create_object, from_json, from_yaml

__all__ = [
    "Banner",
    "Column",
    "ConsoleObject",
    "Frame",
    "Group",
    "Layout",
    "Rule",
    "Spacer",
    "Style",
    "Table",
    "Text",
    "create_object",
    "from_json",
    "from_yaml",
]
