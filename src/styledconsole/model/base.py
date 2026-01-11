"""Base classes for the ConsoleObject model layer.

This module provides the foundational classes for StyledConsole's model layer:
- Style: Text styling attributes (color, bold, italic, etc.)
- ConsoleObject: Base class for all renderable objects

The model layer is output-agnostic - these objects describe what to render,
not how to render it. Rendering is handled by the renderer layer.

Example:
    >>> from styledconsole.model import Style, ConsoleObject
    >>>
    >>> # Style can be used standalone
    >>> style = Style(color="cyan", bold=True)
    >>>
    >>> # ConsoleObjects are immutable
    >>> text = Text(content="Hello", style=style)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    pass


@dataclass(frozen=True)
class Style:
    """Text styling attributes.

    Immutable dataclass containing visual style properties for text content.
    All properties are optional with sensible defaults.

    Attributes:
        color: Foreground color (CSS4 name, hex, or semantic like "success").
        background: Background color.
        bold: Bold text weight.
        italic: Italic text style.
        underline: Underlined text.
        dim: Dimmed/muted text.
        strikethrough: Strikethrough text.

    Example:
        >>> style = Style(color="green", bold=True)
        >>> error_style = Style(color="red", bold=True, underline=True)
    """

    color: str | None = None
    background: str | None = None
    bold: bool = False
    italic: bool = False
    underline: bool = False
    dim: bool = False
    strikethrough: bool = False

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary, excluding None/False values."""
        result: dict[str, Any] = {}
        if self.color is not None:
            result["color"] = self.color
        if self.background is not None:
            result["background"] = self.background
        if self.bold:
            result["bold"] = True
        if self.italic:
            result["italic"] = True
        if self.underline:
            result["underline"] = True
        if self.dim:
            result["dim"] = True
        if self.strikethrough:
            result["strikethrough"] = True
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Style:
        """Create Style from dictionary."""
        return cls(
            color=data.get("color"),
            background=data.get("background"),
            bold=data.get("bold", False),
            italic=data.get("italic", False),
            underline=data.get("underline", False),
            dim=data.get("dim", False),
            strikethrough=data.get("strikethrough", False),
        )

    def merge_with(self, other: Style | None) -> Style:
        """Create new Style merging this with another (other takes precedence)."""
        if other is None:
            return self
        return Style(
            color=other.color if other.color is not None else self.color,
            background=other.background if other.background is not None else self.background,
            bold=other.bold or self.bold,
            italic=other.italic or self.italic,
            underline=other.underline or self.underline,
            dim=other.dim or self.dim,
            strikethrough=other.strikethrough or self.strikethrough,
        )


@dataclass(frozen=True)
class ConsoleObject:
    """Base class for all renderable console objects.

    ConsoleObject is an immutable (frozen) dataclass that serves as the
    base for all visual elements in StyledConsole. It provides:

    - Serialization: to_dict(), to_json(), to_yaml()
    - Deserialization: from_dict()
    - Type identification for renderers

    All subclasses should:
    1. Use @dataclass(frozen=True)
    2. Define a _type class variable for serialization
    3. Override _content_to_dict() if needed

    Attributes:
        style: Optional Style for the object.

    Example:
        >>> # Subclass usage
        >>> @dataclass(frozen=True)
        ... class MyObject(ConsoleObject):
        ...     _type: ClassVar[str] = "my_object"
        ...     content: str
    """

    _type: ClassVar[str] = "object"

    style: Style | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary.

        Returns:
            Dict with 'type' key and all object attributes.
        """
        result: dict[str, Any] = {"type": self._type}

        # Add style if present
        if self.style is not None:
            style_dict = self.style.to_dict()
            if style_dict:
                result["style"] = style_dict

        # Add subclass-specific content
        result.update(self._content_to_dict())

        return result

    def _content_to_dict(self) -> dict[str, Any]:
        """Subclass hook for adding content to serialization.

        Override this in subclasses to add type-specific fields.
        Default implementation adds all dataclass fields except 'style'.

        Returns:
            Dict of additional fields to serialize.
        """
        result: dict[str, Any] = {}
        for key, value in asdict(self).items():
            if key == "style":
                continue
            if value is None:
                continue
            # Handle nested ConsoleObjects
            if isinstance(value, ConsoleObject):
                result[key] = value.to_dict()
            elif isinstance(value, tuple) and value and isinstance(value[0], ConsoleObject):
                result[key] = [item.to_dict() for item in value]
            elif isinstance(value, Style):
                style_dict = value.to_dict()
                if style_dict:
                    result[key] = style_dict
            else:
                result[key] = value
        return result

    def to_json(self, indent: int | None = 2) -> str:
        """Serialize to JSON string.

        Args:
            indent: JSON indentation. None for compact.

        Returns:
            JSON string representation.
        """
        return json.dumps(self.to_dict(), indent=indent)

    def to_yaml(self) -> str:
        """Serialize to YAML string.

        Returns:
            YAML string representation.

        Raises:
            ImportError: If PyYAML is not installed.
        """
        try:
            import yaml  # type: ignore[import-untyped]

            return yaml.safe_dump(self.to_dict(), default_flow_style=False, sort_keys=False)
        except ImportError as e:
            msg = "PyYAML is required for YAML serialization: pip install pyyaml"
            raise ImportError(msg) from e

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConsoleObject:
        """Create ConsoleObject from dictionary.

        Uses the 'type' key to dispatch to the appropriate subclass.

        Args:
            data: Dict with 'type' key identifying the object type.

        Returns:
            Appropriate ConsoleObject subclass instance.

        Raises:
            ValueError: If 'type' key is missing or unknown.
        """
        from styledconsole.model.registry import create_object

        return create_object(data)


__all__ = ["ConsoleObject", "Style"]
