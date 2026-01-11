"""Shorthand syntax normalization for declarative definitions.

This module provides utilities to normalize shorthand syntax into the
canonical dictionary format that create_object() expects.

Supported shorthand formats:
- String: "Hello" → {"type": "text", "content": "Hello"}
- List of strings: ["a", "b"] → vertical layout with text children
- Frame shorthand: {"frame": "content"} → frame with text content
- Banner shorthand: {"banner": "TEXT"} → banner with text
- Quick frame: {"title": "T", "content": "C"} → frame (type inferred)

Example:
    >>> from styledconsole.declarative.shorthand import normalize
    >>>
    >>> # String becomes Text
    >>> normalize("Hello")
    {'type': 'text', 'content': 'Hello'}
    >>>
    >>> # List becomes vertical Layout
    >>> normalize(["Item 1", "Item 2"])
    {'type': 'vertical', 'children': [{'type': 'text', 'content': 'Item 1'}, ...]}
"""

from __future__ import annotations

from typing import Any


def normalize(data: Any) -> dict[str, Any]:
    """Normalize shorthand syntax to canonical dictionary format.

    This function recursively processes input data, converting shorthand
    formats into the full dictionary structure expected by create_object().

    Args:
        data: Input in any supported format (str, list, dict with shorthand).

    Returns:
        Normalized dictionary with 'type' key.

    Example:
        >>> normalize("Hello")
        {'type': 'text', 'content': 'Hello'}
        >>> normalize(["a", "b"])
        {'type': 'vertical', 'children': [...]}
    """
    if isinstance(data, str):
        return _normalize_string(data)
    elif isinstance(data, list):
        return _normalize_list(data)
    elif isinstance(data, dict):
        return _normalize_dict(data)
    else:
        raise TypeError(f"Cannot normalize type: {type(data).__name__}")


def _normalize_string(data: str) -> dict[str, Any]:
    """Normalize a string to Text object."""
    return {"type": "text", "content": data}


def _normalize_list(data: list[Any]) -> dict[str, Any]:
    """Normalize a list to vertical Layout."""
    return {
        "type": "vertical",
        "children": [normalize(item) for item in data],
    }


def _normalize_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize a dictionary, handling shorthand keys."""
    # Already has 'type' key - just normalize children recursively
    if "type" in data:
        return _normalize_typed_dict(data)

    # Check for shorthand keys
    if "frame" in data:
        return _normalize_frame_shorthand(data)
    if "banner" in data:
        return _normalize_banner_shorthand(data)
    if "row" in data:
        return _normalize_row_shorthand(data)
    if "column" in data:
        return _normalize_column_shorthand(data)
    if "grid" in data:
        return _normalize_grid_shorthand(data)

    # Infer type from keys
    if "content" in data and ("title" in data or "border" in data or "effect" in data):
        return _normalize_inferred_frame(data)
    if "text" in data and "font" in data:
        return _normalize_inferred_banner(data)
    if "columns" in data and "rows" in data:
        return _normalize_inferred_table(data)
    if "children" in data:
        return _normalize_inferred_layout(data)

    # Can't determine type
    raise ValueError(
        f"Cannot infer type from keys: {list(data.keys())}. "
        "Add explicit 'type' key or use shorthand format."
    )


def _normalize_typed_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize a dict that already has 'type' key."""
    result = dict(data)
    type_name = data["type"]

    # Normalize content recursively for types that have it
    if "content" in result and type_name in ("frame",):
        content = result["content"]
        if not isinstance(content, dict) or "type" not in content:
            result["content"] = normalize(content)

    # Normalize children recursively
    if "children" in result:
        result["children"] = [normalize(child) for child in result["children"]]

    return result


def _normalize_frame_shorthand(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize {"frame": content, ...} shorthand."""
    content = data["frame"]
    result: dict[str, Any] = {
        "type": "frame",
        "content": normalize(content),
    }

    # Copy other keys
    for key in ("title", "subtitle", "border", "effect", "width", "padding", "style"):
        if key in data:
            result[key] = data[key]

    return result


def _normalize_banner_shorthand(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize {"banner": text, ...} shorthand."""
    text = data["banner"]
    result: dict[str, Any] = {
        "type": "banner",
        "text": text,
    }

    # Copy other keys
    for key in ("font", "effect", "style"):
        if key in data:
            result[key] = data[key]

    return result


def _normalize_row_shorthand(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize {"row": [...], ...} shorthand for horizontal layout."""
    children = data["row"]
    if not isinstance(children, list):
        children = [children]

    result: dict[str, Any] = {
        "type": "horizontal",
        "children": [normalize(child) for child in children],
    }

    # Copy layout options
    for key in ("gap", "equal_width", "style"):
        if key in data:
            result[key] = data[key]

    return result


def _normalize_column_shorthand(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize {"column": [...], ...} shorthand for vertical layout."""
    children = data["column"]
    if not isinstance(children, list):
        children = [children]

    result: dict[str, Any] = {
        "type": "vertical",
        "children": [normalize(child) for child in children],
    }

    # Copy layout options
    for key in ("gap", "style"):
        if key in data:
            result[key] = data[key]

    return result


def _normalize_grid_shorthand(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize {"grid": [...], ...} shorthand."""
    children = data["grid"]
    if not isinstance(children, list):
        children = [children]

    result: dict[str, Any] = {
        "type": "grid",
        "children": [normalize(child) for child in children],
    }

    # Copy grid options
    for key in ("columns", "gap", "equal_width", "style"):
        if key in data:
            result[key] = data[key]

    return result


def _normalize_inferred_frame(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize dict with frame-like keys to Frame."""
    result: dict[str, Any] = {"type": "frame"}

    # Normalize content
    if "content" in data:
        result["content"] = normalize(data["content"])

    # Copy other keys
    for key in ("title", "subtitle", "border", "effect", "width", "padding", "style"):
        if key in data:
            result[key] = data[key]

    return result


def _normalize_inferred_banner(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize dict with banner-like keys to Banner."""
    return {
        "type": "banner",
        "text": data.get("text", ""),
        "font": data.get("font", "standard"),
        "effect": data.get("effect"),
        "style": data.get("style"),
    }


def _normalize_inferred_table(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize dict with table-like keys to Table."""
    result: dict[str, Any] = {"type": "table"}

    for key in ("columns", "rows", "title", "border", "effect", "style"):
        if key in data:
            result[key] = data[key]

    return result


def _normalize_inferred_layout(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize dict with children to Layout."""
    result: dict[str, Any] = {
        "type": data.get("direction", "vertical"),
        "children": [normalize(child) for child in data["children"]],
    }

    for key in ("gap", "columns", "equal_width", "style"):
        if key in data:
            result[key] = data[key]

    return result


__all__ = ["normalize"]
