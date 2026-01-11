"""Declarative layer for console object definitions.

This package provides declarative APIs for defining console objects
using dictionaries, JSON, YAML, and templates with shorthand syntax.

Main components:
- Declarative: High-level facade combining all features
- normalize: Shorthand syntax normalization
- Template/TemplateRegistry: Reusable templates with variables
- load_file/load_json/load_yaml: File loading utilities

Example:
    >>> from styledconsole.declarative import Declarative, create, from_template
    >>>
    >>> # Using the Declarative class
    >>> decl = Declarative()
    >>> obj = decl.create({"frame": "Hello", "title": "Greeting"})
    >>> obj = decl.from_template("info_box", message="Important!")
    >>>
    >>> # Using convenience functions
    >>> obj = create("Hello World")  # Text
    >>> obj = create(["Item 1", "Item 2"])  # vertical Layout
    >>> obj = from_template("error_box", message="Error!")
"""

from styledconsole.declarative.facade import (
    Declarative,
    create,
    from_template,
    get_declarative,
    render,
)
from styledconsole.declarative.loader import (
    load_dict,
    load_file,
    load_json,
    load_yaml,
    parse_data,
)
from styledconsole.declarative.shorthand import normalize
from styledconsole.declarative.templates import (
    BUILTIN_TEMPLATES,
    Template,
    TemplateRegistry,
    TemplateVariable,
    get_builtin_registry,
)

__all__ = [
    "BUILTIN_TEMPLATES",
    "Declarative",
    "Template",
    "TemplateRegistry",
    "TemplateVariable",
    "create",
    "from_template",
    "get_builtin_registry",
    "get_declarative",
    "load_dict",
    "load_file",
    "load_json",
    "load_yaml",
    "normalize",
    "parse_data",
    "render",
]
