"""File loading utilities for declarative definitions.

This module provides utilities for loading console object definitions
from JSON and YAML files.

Example:
    >>> from styledconsole.declarative.loader import load_file, load_json, load_yaml
    >>>
    >>> # Load from file (auto-detects format)
    >>> obj = load_file("dashboard.yaml")
    >>>
    >>> # Load from specific format
    >>> obj = load_json("config.json")
    >>> obj = load_yaml("layout.yaml")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from styledconsole.declarative.shorthand import normalize
from styledconsole.model.registry import create_object

if TYPE_CHECKING:
    from styledconsole.model.base import ConsoleObject


def load_file(
    path: str | Path,
    *,
    use_shorthand: bool = True,
    variables: dict[str, Any] | None = None,
) -> ConsoleObject:
    """Load a ConsoleObject from a file.

    Auto-detects format based on file extension:
    - .json → JSON
    - .yaml, .yml → YAML

    Args:
        path: Path to the file.
        use_shorthand: Whether to normalize shorthand syntax.
        variables: Optional template variables to substitute.

    Returns:
        ConsoleObject parsed from file.

    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If file format not supported.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    suffix = path.suffix.lower()
    content = path.read_text(encoding="utf-8")

    if suffix == ".json":
        return load_json(content, use_shorthand=use_shorthand, variables=variables)
    elif suffix in (".yaml", ".yml"):
        return load_yaml(content, use_shorthand=use_shorthand, variables=variables)
    else:
        raise ValueError(
            f"Unsupported file format: {suffix}. Supported formats: .json, .yaml, .yml"
        )


def load_json(
    content: str,
    *,
    use_shorthand: bool = True,
    variables: dict[str, Any] | None = None,
) -> ConsoleObject:
    """Load a ConsoleObject from JSON string.

    Args:
        content: JSON string.
        use_shorthand: Whether to normalize shorthand syntax.
        variables: Optional template variables to substitute.

    Returns:
        ConsoleObject parsed from JSON.
    """
    data = json.loads(content)
    return _process_data(data, use_shorthand=use_shorthand, variables=variables)


def load_yaml(
    content: str,
    *,
    use_shorthand: bool = True,
    variables: dict[str, Any] | None = None,
) -> ConsoleObject:
    """Load a ConsoleObject from YAML string.

    Args:
        content: YAML string.
        use_shorthand: Whether to normalize shorthand syntax.
        variables: Optional template variables to substitute.

    Returns:
        ConsoleObject parsed from YAML.

    Raises:
        ImportError: If PyYAML is not installed.
    """
    try:
        import yaml  # type: ignore[import-untyped]

        data = yaml.safe_load(content)
        return _process_data(data, use_shorthand=use_shorthand, variables=variables)
    except ImportError as e:
        raise ImportError("PyYAML is required for YAML loading: pip install pyyaml") from e


def load_dict(
    data: dict[str, Any] | list[Any] | str,
    *,
    use_shorthand: bool = True,
    variables: dict[str, Any] | None = None,
) -> ConsoleObject:
    """Load a ConsoleObject from a dictionary or shorthand data.

    Args:
        data: Dictionary, list, or string data.
        use_shorthand: Whether to normalize shorthand syntax.
        variables: Optional template variables to substitute.

    Returns:
        ConsoleObject parsed from data.
    """
    return _process_data(data, use_shorthand=use_shorthand, variables=variables)


def _process_data(
    data: Any,
    *,
    use_shorthand: bool,
    variables: dict[str, Any] | None,
) -> ConsoleObject:
    """Process data into a ConsoleObject.

    Args:
        data: Raw data.
        use_shorthand: Whether to normalize shorthand.
        variables: Template variables.

    Returns:
        ConsoleObject.
    """
    # Apply template variables if provided
    if variables:
        from styledconsole.declarative.templates import _substitute

        data = _substitute(data, variables)

    # Normalize shorthand if enabled
    if use_shorthand:
        data = normalize(data)

    return create_object(data)


def parse_data(
    data: Any,
    *,
    use_shorthand: bool = True,
    variables: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Parse data to normalized dictionary without creating object.

    Useful for inspection or modification before object creation.

    Args:
        data: Raw data.
        use_shorthand: Whether to normalize shorthand.
        variables: Template variables.

    Returns:
        Normalized dictionary.
    """
    # Apply template variables if provided
    if variables:
        from styledconsole.declarative.templates import _substitute

        data = _substitute(data, variables)

    # Normalize shorthand if enabled
    if use_shorthand:
        data = normalize(data)

    # Ensure we return a dict
    if isinstance(data, dict):
        return data
    return {"type": "text", "content": str(data)}


__all__ = ["load_dict", "load_file", "load_json", "load_yaml", "parse_data"]
