"""Object type registry for model deserialization.

This module provides the type registry that maps type names to ConsoleObject
classes, enabling deserialization from dictionaries, JSON, and YAML.

Example:
    >>> from styledconsole.model.registry import create_object
    >>>
    >>> # Create object from dict
    >>> obj = create_object({"type": "text", "content": "Hello"})
    >>> print(obj)  # Text(content='Hello', style=None)
    >>>
    >>> # Create nested objects
    >>> frame = create_object({
    ...     "type": "frame",
    ...     "title": "Greeting",
    ...     "content": {"type": "text", "content": "Hello World"},
    ... })
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from styledconsole.model.base import ConsoleObject


def _get_object_types() -> dict[str, type]:
    """Get the object type registry."""
    from styledconsole.model.objects import (
        Banner,
        Frame,
        Group,
        Layout,
        Rule,
        Spacer,
        Table,
        Text,
    )

    return {
        "text": Text,
        "frame": Frame,
        "banner": Banner,
        "table": Table,
        "layout": Layout,
        "vertical": Layout,
        "horizontal": Layout,
        "grid": Layout,
        "group": Group,
        "spacer": Spacer,
        "rule": Rule,
    }


def _parse_text(data: dict[str, Any]) -> dict[str, Any]:
    """Parse text-specific fields."""
    return {"content": data.get("content", "")}


def _parse_frame(data: dict[str, Any]) -> dict[str, Any]:
    """Parse frame-specific fields."""
    kwargs: dict[str, Any] = {}
    if "content" in data:
        kwargs["content"] = create_object(data["content"])
    kwargs["title"] = data.get("title")
    kwargs["subtitle"] = data.get("subtitle")
    kwargs["border"] = data.get("border", "solid")
    kwargs["effect"] = data.get("effect")
    kwargs["width"] = data.get("width")
    kwargs["padding"] = data.get("padding", 1)
    kwargs["align"] = data.get("align", "left")
    return kwargs


def _parse_banner(data: dict[str, Any]) -> dict[str, Any]:
    """Parse banner-specific fields."""
    return {
        "text": data.get("text", ""),
        "font": data.get("font", "standard"),
        "effect": data.get("effect"),
    }


def _parse_table(data: dict[str, Any]) -> dict[str, Any]:
    """Parse table-specific fields."""
    from styledconsole.model.objects import Column

    kwargs: dict[str, Any] = {}
    if "columns" in data:
        kwargs["columns"] = tuple(
            Column.from_dict(col) if isinstance(col, dict) else Column(header=col)
            for col in data["columns"]
        )
    if "rows" in data:
        kwargs["rows"] = tuple(tuple(row) for row in data["rows"])
    kwargs["title"] = data.get("title")
    kwargs["border"] = data.get("border", "solid")
    kwargs["effect"] = data.get("effect")
    return kwargs


def _parse_layout(data: dict[str, Any], type_name: str) -> dict[str, Any]:
    """Parse layout-specific fields."""
    kwargs: dict[str, Any] = {}
    if "children" in data:
        kwargs["children"] = tuple(create_object(child) for child in data["children"])
    # Handle direction based on type alias
    direction_map = {"vertical": "vertical", "horizontal": "horizontal", "grid": "grid"}
    kwargs["direction"] = direction_map.get(type_name, data.get("direction", "vertical"))
    kwargs["gap"] = data.get("gap", 0)
    kwargs["columns"] = data.get("columns")
    kwargs["equal_width"] = data.get("equal_width", False)
    return kwargs


def _parse_group(data: dict[str, Any]) -> dict[str, Any]:
    """Parse group-specific fields."""
    kwargs: dict[str, Any] = {}
    if "children" in data:
        kwargs["children"] = tuple(create_object(child) for child in data["children"])
    return kwargs


def _parse_spacer(data: dict[str, Any]) -> dict[str, Any]:
    """Parse spacer-specific fields."""
    return {"lines": data.get("lines", 1)}


def _parse_rule(data: dict[str, Any]) -> dict[str, Any]:
    """Parse rule-specific fields."""
    return {"title": data.get("title")}


# Type-specific parser dispatch table
_TYPE_PARSERS: dict[str, Any] = {
    "text": _parse_text,
    "frame": _parse_frame,
    "banner": _parse_banner,
    "table": _parse_table,
    "group": _parse_group,
    "spacer": _parse_spacer,
    "rule": _parse_rule,
}


def create_object(data: dict[str, Any]) -> ConsoleObject:
    """Create a ConsoleObject from a dictionary.

    Uses the 'type' key to determine which class to instantiate.
    Recursively creates nested objects.

    Args:
        data: Dictionary with 'type' key and object attributes.

    Returns:
        Appropriate ConsoleObject instance.

    Raises:
        ValueError: If 'type' key is missing or unknown.
    """
    from styledconsole.model.base import Style

    if not isinstance(data, dict):
        raise ValueError(f"Expected dict, got {type(data).__name__}")

    type_name = data.get("type")
    if type_name is None:
        raise ValueError("Missing 'type' key in object definition")

    object_types = _get_object_types()
    if type_name not in object_types:
        from styledconsole.utils.suggestions import format_error_with_suggestion

        error_msg = format_error_with_suggestion(
            f"Unknown object type: '{type_name}'",
            type_name,
            list(object_types.keys()),
            max_distance=2,
        )
        raise ValueError(error_msg)

    obj_class = object_types[type_name]

    # Build kwargs from data
    kwargs: dict[str, Any] = {}

    # Handle style if present
    if "style" in data:
        kwargs["style"] = Style.from_dict(data["style"])

    # Dispatch to type-specific parser
    if type_name in ("layout", "vertical", "horizontal", "grid"):
        kwargs.update(_parse_layout(data, type_name))
    elif type_name in _TYPE_PARSERS:
        kwargs.update(_TYPE_PARSERS[type_name](data))

    return obj_class(**kwargs)


def from_json(json_str: str) -> ConsoleObject:
    """Create ConsoleObject from JSON string."""
    import json

    data = json.loads(json_str)
    return create_object(data)


def from_yaml(yaml_str: str) -> ConsoleObject:
    """Create ConsoleObject from YAML string.

    Raises:
        ImportError: If PyYAML is not installed.
    """
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(yaml_str)
        return create_object(data)
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML parsing: pip install pyyaml") from e


__all__ = ["create_object", "from_json", "from_yaml"]
