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

# Jinja2 support (optional dependency)
try:
    from styledconsole.declarative.jinja import (
        add_filter as add_jinja_filter,
    )
    from styledconsole.declarative.jinja import (
        load_jinja_file,
        render_jinja,
        render_jinja_string,
    )

    _HAS_JINJA = True
except ImportError:
    _HAS_JINJA = False

    def _jinja_not_installed(*args: object, **kwargs: object) -> object:
        raise ImportError(
            "Jinja2 is required for Jinja template support: pip install styledconsole[jinja]"
        )

    add_jinja_filter = _jinja_not_installed  # type: ignore[assignment]
    load_jinja_file = _jinja_not_installed  # type: ignore[assignment]
    render_jinja = _jinja_not_installed  # type: ignore[assignment]
    render_jinja_string = _jinja_not_installed  # type: ignore[assignment]

__all__ = [
    "BUILTIN_TEMPLATES",
    "Declarative",
    "Template",
    "TemplateRegistry",
    "TemplateVariable",
    "add_jinja_filter",
    "create",
    "from_template",
    "get_builtin_registry",
    "get_declarative",
    "load_dict",
    "load_file",
    "load_jinja_file",
    "load_json",
    "load_yaml",
    "normalize",
    "parse_data",
    "render",
    "render_jinja",
    "render_jinja_string",
]
