"""Jinja2 template support for declarative definitions.

This module provides Jinja2 integration for powerful template
processing with loops, conditionals, filters, and inheritance.

Example:
    >>> from styledconsole.declarative.jinja import render_jinja, load_jinja_file
    >>>
    >>> # Render inline Jinja2 template
    >>> template = '''
    ... type: layout
    ... children:
    ...   {% for item in items %}
    ...   - frame: "{{ item.name }}"
    ...     effect: "{{ 'ocean' if item.ok else 'fire' }}"
    ...   {% endfor %}
    ... '''
    >>> obj = render_jinja(template, items=[{"name": "A", "ok": True}])
    >>>
    >>> # Load from file
    >>> obj = load_jinja_file("dashboard.yaml.j2", services=services)

Requirements:
    pip install styledconsole[jinja]
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from styledconsole.model.base import ConsoleObject

# Custom filters for StyledConsole templates
_CUSTOM_FILTERS: dict[str, Any] = {}


def _get_jinja_env() -> Any:
    """Get configured Jinja2 environment.

    Returns:
        Jinja2 Environment with custom filters.

    Raises:
        ImportError: If Jinja2 is not installed.
    """
    try:
        from jinja2 import BaseLoader, Environment, StrictUndefined
    except ImportError as e:
        raise ImportError(
            "Jinja2 is required for Jinja template support: pip install styledconsole[jinja]"
        ) from e

    env = Environment(
        loader=BaseLoader(),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Add custom filters
    env.filters.update(_CUSTOM_FILTERS)

    # Add built-in filters for StyledConsole
    env.filters["icon"] = _filter_icon
    env.filters["effect"] = _filter_effect
    env.filters["status_icon"] = _filter_status_icon
    env.filters["status_effect"] = _filter_status_effect

    return env


def _filter_icon(name: str) -> str:
    """Jinja filter to get icon by name.

    Usage in template: {{ "check" | icon }}
    """
    from styledconsole import icons

    icon_map = {
        "check": icons.CHECK_MARK_BUTTON,
        "cross": icons.CROSS_MARK,
        "warning": icons.WARNING,
        "info": icons.INFORMATION,
        "star": icons.STAR,
        "sparkles": icons.SPARKLES,
        "gear": icons.GEAR,
        "rocket": icons.ROCKET,
        "fire": icons.FIRE,
        "bell": icons.BELL,
        "ok": icons.CHECK_MARK_BUTTON,
        "error": icons.CROSS_MARK,
    }
    try:
        return str(icon_map.get(name) or icons.get(name) or name)
    except (KeyError, AttributeError):
        return name


def _filter_effect(status: str) -> str:
    """Jinja filter to map status to effect.

    Usage in template: {{ status | effect }}
    """
    effect_map = {
        "ok": "ocean",
        "success": "ocean",
        "running": "ocean",
        "healthy": "ocean",
        "warning": "sunset",
        "degraded": "sunset",
        "error": "fire",
        "critical": "fire",
        "failed": "fire",
        "stopped": "steel",
        "pending": "steel",
        "unknown": "steel",
    }
    return effect_map.get(status.lower(), "steel")


def _filter_status_icon(status: str) -> str:
    """Jinja filter to get status icon.

    Usage in template: {{ service.status | status_icon }}
    """
    from styledconsole import icons

    icon_map = {
        "ok": icons.CHECK_MARK_BUTTON,
        "success": icons.CHECK_MARK_BUTTON,
        "running": icons.CHECK_MARK_BUTTON,
        "healthy": icons.CHECK_MARK_BUTTON,
        "warning": icons.WARNING,
        "degraded": icons.WARNING,
        "error": icons.CROSS_MARK,
        "critical": icons.CROSS_MARK,
        "failed": icons.CROSS_MARK,
        "stopped": icons.CROSS_MARK,
        "pending": icons.COUNTERCLOCKWISE_ARROWS_BUTTON,
        "unknown": icons.RED_QUESTION_MARK,
    }
    return str(icon_map.get(status.lower(), icons.RED_QUESTION_MARK))


def _filter_status_effect(status: str) -> str:
    """Jinja filter to get effect for status.

    Usage in template: {{ service.status | status_effect }}
    """
    return _filter_effect(status)


def add_filter(name: str, func: Any) -> None:
    """Register a custom Jinja2 filter.

    Args:
        name: Filter name to use in templates.
        func: Filter function.

    Example:
        >>> def uppercase(value):
        ...     return value.upper()
        >>> add_filter("upper", uppercase)
        >>> # In template: {{ name | upper }}
    """
    _CUSTOM_FILTERS[name] = func


def render_jinja(
    template: str,
    *,
    format: str = "yaml",
    use_shorthand: bool = True,
    **variables: Any,
) -> ConsoleObject:
    """Render a Jinja2 template to a ConsoleObject.

    Args:
        template: Jinja2 template string.
        format: Output format after rendering ("yaml" or "json").
        use_shorthand: Whether to normalize shorthand syntax.
        **variables: Template variables.

    Returns:
        ConsoleObject parsed from rendered template.

    Raises:
        ImportError: If Jinja2 is not installed.
        ValueError: If format is not supported.

    Example:
        >>> template = '''
        ... type: frame
        ... title: "{{ title }}"
        ... content: "{{ message }}"
        ... effect: "{{ 'ocean' if success else 'fire' }}"
        ... '''
        >>> obj = render_jinja(template, title="Status", message="OK", success=True)
    """
    env = _get_jinja_env()
    jinja_template = env.from_string(template)
    rendered = jinja_template.render(**variables)

    # Parse the rendered output
    if format == "yaml":
        from styledconsole.declarative.loader import load_yaml

        return load_yaml(rendered, use_shorthand=use_shorthand)
    elif format == "json":
        from styledconsole.declarative.loader import load_json

        return load_json(rendered, use_shorthand=use_shorthand)
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'yaml' or 'json'.")


def load_jinja_file(
    path: str | Path,
    *,
    format: str | None = None,
    use_shorthand: bool = True,
    **variables: Any,
) -> ConsoleObject:
    """Load and render a Jinja2 template file.

    Auto-detects format from file extension:
    - .yaml.j2, .yml.j2 → YAML
    - .json.j2 → JSON

    Args:
        path: Path to the template file.
        format: Override format detection ("yaml" or "json").
        use_shorthand: Whether to normalize shorthand syntax.
        **variables: Template variables.

    Returns:
        ConsoleObject parsed from rendered template.

    Raises:
        FileNotFoundError: If file doesn't exist.
        ImportError: If Jinja2 is not installed.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Template file not found: {path}")

    template = path.read_text(encoding="utf-8")

    # Auto-detect format from extension
    if format is None:
        name = path.name.lower()
        if name.endswith(".yaml.j2") or name.endswith(".yml.j2"):
            format = "yaml"
        elif name.endswith(".json.j2"):
            format = "json"
        else:
            # Default to YAML
            format = "yaml"

    return render_jinja(
        template,
        format=format,
        use_shorthand=use_shorthand,
        **variables,
    )


def render_jinja_string(
    template: str,
    **variables: Any,
) -> str:
    """Render a Jinja2 template to a string (without parsing).

    Useful for generating raw output or debugging.

    Args:
        template: Jinja2 template string.
        **variables: Template variables.

    Returns:
        Rendered string.
    """
    env = _get_jinja_env()
    jinja_template = env.from_string(template)
    return jinja_template.render(**variables)


__all__ = [
    "add_filter",
    "load_jinja_file",
    "render_jinja",
    "render_jinja_string",
]
