"""Template system for reusable declarative definitions.

This module provides a template system that allows defining reusable
console object templates with variables that can be filled in later.

Variables use the format ${name} or ${name:default} for defaults.

Example:
    >>> from styledconsole.declarative.templates import Template
    >>>
    >>> # Define a template
    >>> tmpl = Template({
    ...     "type": "frame",
    ...     "title": "${title}",
    ...     "content": {"type": "text", "content": "${message}"},
    ...     "effect": "${effect:ocean}"
    ... })
    >>>
    >>> # Render with variables
    >>> data = tmpl.render(title="Hello", message="World")
    >>> # {'type': 'frame', 'title': 'Hello', 'content': {...}, 'effect': 'ocean'}
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

# Pattern for ${var} or ${var:default}
_VAR_PATTERN = re.compile(r"\$\{([^}:]+)(?::([^}]*))?\}")


@dataclass
class Template:
    """A reusable template for console object definitions.

    Templates contain variable placeholders in the format ${name} or
    ${name:default}. When rendered, these are replaced with provided values.

    Attributes:
        definition: The template definition with placeholders.
        name: Optional template name for registry.
        description: Optional description.

    Example:
        >>> tmpl = Template({"type": "text", "content": "${msg}"})
        >>> tmpl.render(msg="Hello")
        {'type': 'text', 'content': 'Hello'}
    """

    definition: dict[str, Any]
    name: str | None = None
    description: str | None = None

    def render(self, **variables: Any) -> dict[str, Any]:
        """Render the template with variable substitution.

        Args:
            **variables: Variable values to substitute.

        Returns:
            Dictionary with variables replaced.

        Raises:
            ValueError: If required variable is missing.
        """
        result = _substitute(self.definition, variables)
        # definition is always dict, so result is always dict
        return dict(result) if isinstance(result, dict) else {"value": result}

    def get_variables(self) -> list[TemplateVariable]:
        """Get list of variables used in this template.

        Returns:
            List of TemplateVariable with name and default.
        """
        return _extract_variables(self.definition)

    def validate(self, **variables: Any) -> list[str]:
        """Validate that all required variables are provided.

        Args:
            **variables: Variable values to check.

        Returns:
            List of missing required variable names.
        """
        missing = []
        for var in self.get_variables():
            if var.default is None and var.name not in variables:
                missing.append(var.name)
        return missing


@dataclass
class TemplateVariable:
    """A variable in a template.

    Attributes:
        name: Variable name.
        default: Default value, or None if required.
    """

    name: str
    default: str | None = None

    @property
    def required(self) -> bool:
        """Whether this variable is required (no default)."""
        return self.default is None


@dataclass
class TemplateRegistry:
    """Registry for reusable templates.

    Provides a way to store and retrieve named templates.

    Example:
        >>> registry = TemplateRegistry()
        >>> registry.register("info_box", Template({
        ...     "type": "frame",
        ...     "title": "Info",
        ...     "content": {"type": "text", "content": "${message}"},
        ...     "effect": "ocean"
        ... }))
        >>> registry.render("info_box", message="Hello!")
    """

    _templates: dict[str, Template] = field(default_factory=dict)

    def register(self, name: str, template: Template | dict[str, Any]) -> None:
        """Register a template.

        Args:
            name: Template name.
            template: Template instance or definition dict.
        """
        if isinstance(template, dict):
            template = Template(definition=template, name=name)
        else:
            template = Template(
                definition=template.definition,
                name=name,
                description=template.description,
            )
        self._templates[name] = template

    def get(self, name: str) -> Template | None:
        """Get a template by name.

        Args:
            name: Template name.

        Returns:
            Template if found, None otherwise.
        """
        return self._templates.get(name)

    def render(self, name: str, **variables: Any) -> dict[str, Any]:
        """Render a named template.

        Args:
            name: Template name.
            **variables: Variable values.

        Returns:
            Rendered dictionary.

        Raises:
            KeyError: If template not found.
            ValueError: If required variables missing.
        """
        template = self._templates.get(name)
        if template is None:
            available = ", ".join(sorted(self._templates.keys()))
            raise KeyError(f"Template '{name}' not found. Available: {available}")
        return template.render(**variables)

    def list_templates(self) -> list[str]:
        """Get list of registered template names."""
        return list(self._templates.keys())

    def unregister(self, name: str) -> bool:
        """Remove a template.

        Args:
            name: Template name.

        Returns:
            True if removed, False if not found.
        """
        if name in self._templates:
            del self._templates[name]
            return True
        return False


# Built-in templates
BUILTIN_TEMPLATES: dict[str, dict[str, Any]] = {
    "info_box": {
        "type": "frame",
        "title": "${title:Info}",
        "content": {"type": "text", "content": "${message}"},
        "effect": "ocean",
        "border": "rounded",
    },
    "warning_box": {
        "type": "frame",
        "title": "${title:Warning}",
        "content": {"type": "text", "content": "${message}"},
        "effect": "sunset",
        "border": "heavy",
    },
    "error_box": {
        "type": "frame",
        "title": "${title:Error}",
        "content": {"type": "text", "content": "${message}"},
        "effect": "fire",
        "border": "double",
    },
    "success_box": {
        "type": "frame",
        "title": "${title:Success}",
        "content": {"type": "text", "content": "${message}"},
        "effect": "forest",
        "border": "rounded",
    },
    "header_banner": {
        "type": "banner",
        "text": "${text}",
        "font": "${font:slant}",
        "effect": "${effect:ocean}",
    },
    "section": {
        "type": "vertical",
        "gap": 1,
        "children": [
            {"type": "rule", "title": "${title}"},
            {"type": "text", "content": "${content}"},
        ],
    },
    "key_value": {
        "type": "table",
        "columns": ["Key", "Value"],
        "rows": "${rows}",
        "border": "rounded",
    },
}


def _substitute(data: Any, variables: dict[str, Any]) -> Any:
    """Recursively substitute variables in data structure.

    Args:
        data: Data to process (str, list, dict, or primitive).
        variables: Variable values.

    Returns:
        Data with variables substituted.
    """
    if isinstance(data, str):
        return _substitute_string(data, variables)
    elif isinstance(data, dict):
        return {key: _substitute(value, variables) for key, value in data.items()}
    elif isinstance(data, list):
        return [_substitute(item, variables) for item in data]
    else:
        return data


def _substitute_string(text: str, variables: dict[str, Any]) -> Any:
    """Substitute variables in a string.

    If the entire string is a single variable reference and the value
    is not a string, return the value directly (allows non-string values).

    Args:
        text: String with ${var} placeholders.
        variables: Variable values.

    Returns:
        Substituted string or value.
    """
    # Check if entire string is a single variable
    match = _VAR_PATTERN.fullmatch(text)
    if match:
        name, default = match.groups()
        if name in variables:
            return variables[name]
        elif default is not None:
            return default
        else:
            raise ValueError(f"Missing required variable: ${{{name}}}")

    # Multiple variables or mixed content - substitute as string
    def replace(m: re.Match[str]) -> str:
        name, default = m.groups()
        if name in variables:
            return str(variables[name])
        elif default is not None:
            return default
        else:
            raise ValueError(f"Missing required variable: ${{{name}}}")

    return _VAR_PATTERN.sub(replace, text)


def _extract_variables(data: Any) -> list[TemplateVariable]:
    """Extract all variables from a data structure.

    Args:
        data: Data to scan.

    Returns:
        List of unique TemplateVariable instances.
    """
    seen: dict[str, TemplateVariable] = {}

    def scan(item: Any) -> None:
        if isinstance(item, str):
            for match in _VAR_PATTERN.finditer(item):
                name, default = match.groups()
                if name not in seen:
                    seen[name] = TemplateVariable(name=name, default=default)
        elif isinstance(item, dict):
            for value in item.values():
                scan(value)
        elif isinstance(item, list):
            for elem in item:
                scan(elem)

    scan(data)
    return list(seen.values())


def get_builtin_registry() -> TemplateRegistry:
    """Get a registry pre-populated with built-in templates.

    Returns:
        TemplateRegistry with built-in templates registered.
    """
    registry = TemplateRegistry()
    for name, definition in BUILTIN_TEMPLATES.items():
        registry.register(name, Template(definition=definition, name=name))
    return registry


__all__ = [
    "BUILTIN_TEMPLATES",
    "Template",
    "TemplateRegistry",
    "TemplateVariable",
    "get_builtin_registry",
]
