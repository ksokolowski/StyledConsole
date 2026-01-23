"""JSON Schema for StyledConsole declarative configurations.

This module provides access to the JSON Schema for validating
StyledConsole configuration files (JSON/YAML).

Usage:
    from styledconsole.schemas import get_schema_path, get_schema

    # Get path to schema file (for IDE configuration)
    schema_path = get_schema_path()

    # Get schema as Python dict
    schema = get_schema()
"""

from pathlib import Path
from typing import Any

__all__ = ["SCHEMA_PATH", "get_schema", "get_schema_path"]

# Path to the schema file
SCHEMA_PATH = Path(__file__).parent / "styledconsole.schema.json"


def get_schema_path() -> Path:
    """Get the path to the JSON Schema file.

    Returns:
        Path to styledconsole.schema.json

    Example:
        >>> from styledconsole.schemas import get_schema_path
        >>> path = get_schema_path()
        >>> print(path)
        /path/to/styledconsole/schemas/styledconsole.schema.json
    """
    return SCHEMA_PATH


def get_schema() -> dict[str, Any]:
    """Load and return the JSON Schema as a Python dictionary.

    Returns:
        The schema as a dict

    Example:
        >>> from styledconsole.schemas import get_schema
        >>> schema = get_schema()
        >>> print(schema["title"])
        StyledConsole Configuration
    """
    import json

    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
