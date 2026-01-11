"""High-level declarative API for console objects.

This module provides the Declarative class that combines shorthand parsing,
template rendering, and object creation into a single, convenient interface.

Example:
    >>> from styledconsole.declarative import Declarative
    >>>
    >>> decl = Declarative()
    >>>
    >>> # Create from shorthand
    >>> frame = decl.create({"frame": "Hello World", "title": "Greeting"})
    >>>
    >>> # Use built-in templates
    >>> info = decl.from_template("info_box", message="Important info")
    >>>
    >>> # Load from file
    >>> dashboard = decl.load("dashboard.yaml")
    >>>
    >>> # Render directly to terminal
    >>> decl.render({"banner": "Welcome", "effect": "ocean"})
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from styledconsole.declarative.loader import load_dict, load_file, parse_data
from styledconsole.declarative.templates import (
    Template,
    TemplateRegistry,
    get_builtin_registry,
)

if TYPE_CHECKING:
    from styledconsole.model.base import ConsoleObject
    from styledconsole.rendering.base import Renderer
    from styledconsole.rendering.context import RenderContext


class Declarative:
    """High-level declarative API for console objects.

    Combines shorthand parsing, template rendering, file loading,
    and object creation into a convenient interface.

    Attributes:
        templates: Template registry for reusable templates.

    Example:
        >>> decl = Declarative()
        >>> obj = decl.create("Hello World")  # Creates Text
        >>> obj = decl.create({"frame": "Content", "title": "Title"})
        >>> obj = decl.from_template("info_box", message="Info!")
    """

    def __init__(
        self,
        *,
        include_builtins: bool = True,
    ) -> None:
        """Initialize the Declarative facade.

        Args:
            include_builtins: Whether to include built-in templates.
        """
        if include_builtins:
            self.templates = get_builtin_registry()
        else:
            self.templates = TemplateRegistry()

    def create(
        self,
        data: Any,
        *,
        variables: dict[str, Any] | None = None,
    ) -> ConsoleObject:
        """Create a ConsoleObject from declarative data.

        Supports all shorthand formats:
        - String: "text" → Text
        - List: ["a", "b"] → vertical Layout
        - Dict with shorthand: {"frame": "content"} → Frame
        - Dict with type: {"type": "frame", ...} → Frame

        Args:
            data: Declarative data in any supported format.
            variables: Optional template variables.

        Returns:
            ConsoleObject instance.

        Example:
            >>> decl.create("Hello")
            Text(content='Hello')
            >>> decl.create({"frame": "Content", "title": "Title"})
            Frame(content=Text(...), title='Title')
        """
        return load_dict(data, use_shorthand=True, variables=variables)

    def parse(
        self,
        data: Any,
        *,
        variables: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Parse data to normalized dictionary without creating object.

        Useful for inspection or modification before creation.

        Args:
            data: Declarative data.
            variables: Optional template variables.

        Returns:
            Normalized dictionary with 'type' key.
        """
        return parse_data(data, use_shorthand=True, variables=variables)

    def load(
        self,
        path: str | Path,
        *,
        variables: dict[str, Any] | None = None,
    ) -> ConsoleObject:
        """Load a ConsoleObject from a file.

        Auto-detects format from extension (.json, .yaml, .yml).

        Args:
            path: Path to the file.
            variables: Optional template variables.

        Returns:
            ConsoleObject instance.
        """
        return load_file(path, use_shorthand=True, variables=variables)

    def from_template(
        self,
        name: str,
        **variables: Any,
    ) -> ConsoleObject:
        """Create a ConsoleObject from a named template.

        Args:
            name: Template name.
            **variables: Template variable values.

        Returns:
            ConsoleObject instance.

        Example:
            >>> decl.from_template("info_box", message="Hello!")
            Frame(title='Info', content=Text(...), effect='ocean')
        """
        data = self.templates.render(name, **variables)
        # Use shorthand=True since template output may contain shorthand
        return load_dict(data, use_shorthand=True, variables=None)

    def register_template(
        self,
        name: str,
        template: Template | dict[str, Any],
    ) -> None:
        """Register a custom template.

        Args:
            name: Template name.
            template: Template instance or definition dict.

        Example:
            >>> decl.register_template("my_box", {
            ...     "type": "frame",
            ...     "title": "${title}",
            ...     "content": {"type": "text", "content": "${msg}"},
            ... })
        """
        self.templates.register(name, template)

    def list_templates(self) -> list[str]:
        """Get list of available template names.

        Returns:
            List of template names.
        """
        return self.templates.list_templates()

    def render(
        self,
        data: Any,
        *,
        variables: dict[str, Any] | None = None,
        renderer: Renderer | None = None,
        context: RenderContext | None = None,
    ) -> None:
        """Create and render a ConsoleObject directly.

        Convenience method that creates an object and renders it
        in a single call.

        Args:
            data: Declarative data.
            variables: Optional template variables.
            renderer: Renderer to use (defaults to TerminalRenderer).
            context: Render context.

        Example:
            >>> decl.render({"banner": "Hello", "effect": "ocean"})
        """
        obj = self.create(data, variables=variables)

        if renderer is None:
            from styledconsole.rendering import TerminalRenderer

            renderer = TerminalRenderer()

        renderer.render(obj, context=context)

    def render_template(
        self,
        name: str,
        *,
        renderer: Renderer | None = None,
        context: RenderContext | None = None,
        **variables: Any,
    ) -> None:
        """Render a named template directly.

        Args:
            name: Template name.
            renderer: Renderer to use.
            context: Render context.
            **variables: Template variable values.

        Example:
            >>> decl.render_template("info_box", message="Hello!")
        """
        obj = self.from_template(name, **variables)

        if renderer is None:
            from styledconsole.rendering import TerminalRenderer

            renderer = TerminalRenderer()

        renderer.render(obj, context=context)


# Global instance for convenience
_default_instance: Declarative | None = None


def get_declarative() -> Declarative:
    """Get the global Declarative instance.

    Returns:
        Global Declarative instance (created on first call).
    """
    global _default_instance
    if _default_instance is None:
        _default_instance = Declarative()
    return _default_instance


# Convenience functions using global instance


def create(data: Any, **variables: Any) -> ConsoleObject:
    """Create a ConsoleObject using the global Declarative instance.

    See Declarative.create() for details.
    """
    return get_declarative().create(data, variables=variables or None)


def from_template(name: str, **variables: Any) -> ConsoleObject:
    """Create from template using the global Declarative instance.

    See Declarative.from_template() for details.
    """
    return get_declarative().from_template(name, **variables)


def render(data: Any, **variables: Any) -> None:
    """Render declarative data using the global instance.

    See Declarative.render() for details.
    """
    get_declarative().render(data, variables=variables or None)


__all__ = [
    "Declarative",
    "create",
    "from_template",
    "get_declarative",
    "render",
]
