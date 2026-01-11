"""Base classes and protocols for the renderer layer.

This module defines the Renderer protocol that all renderers implement,
providing a consistent interface for rendering ConsoleObjects to various outputs.

Example:
    >>> from styledconsole.rendering import TerminalRenderer, RenderContext
    >>> from styledconsole.model import Text
    >>>
    >>> renderer = TerminalRenderer()
    >>> text = Text(content="Hello World")
    >>> renderer.render(text)  # Prints to stdout
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from styledconsole.model import ConsoleObject
    from styledconsole.rendering.context import RenderContext


@runtime_checkable
class Renderer(Protocol):
    """Protocol for all renderers.

    Renderers take ConsoleObjects and produce output in a specific format.
    Each renderer handles the conversion from the abstract model to a
    concrete representation (ANSI, HTML, image bytes, etc.).

    The render() method is the main entry point. It accepts:
    - obj: The ConsoleObject to render
    - target: Where to send output (stdout, file, StringIO, etc.)
    - context: RenderContext with environment info

    Different renderers may return different types:
    - TerminalRenderer: None (prints to target)
    - HTMLRenderer: str (HTML string)
    - ImageRenderer: bytes (image data)
    """

    def render(
        self,
        obj: ConsoleObject,
        target: Any = None,
        context: RenderContext | None = None,
    ) -> Any:
        """Render a ConsoleObject to the specified target.

        Args:
            obj: The ConsoleObject to render.
            target: Output destination. Type depends on renderer:
                - TerminalRenderer: IO[str] or None for stdout
                - HTMLRenderer: str path or IO[str]
                - ImageRenderer: str path or IO[bytes]
            context: Rendering context with environment info.
                If None, a default context is created.

        Returns:
            Renderer-specific result:
                - TerminalRenderer: None
                - HTMLRenderer: str (HTML content)
                - ImageRenderer: bytes (image data)
        """
        ...


class BaseRenderer:
    """Base class for renderers with common functionality.

    Provides shared logic for context handling and object dispatch.
    Subclasses should implement _render_* methods for each object type.
    """

    def _get_context(self, context: RenderContext | None) -> RenderContext:
        """Get or create a RenderContext.

        Args:
            context: Provided context or None.

        Returns:
            The provided context or a default one.
        """
        if context is not None:
            return context
        return self._default_context()

    def _default_context(self) -> RenderContext:
        """Create the default context for this renderer.

        Override in subclasses to provide appropriate defaults.
        """
        from styledconsole.rendering.context import RenderContext

        return RenderContext.auto_detect()

    def _dispatch(self, obj: ConsoleObject, context: RenderContext) -> Any:
        """Dispatch to type-specific render method.

        Args:
            obj: ConsoleObject to render.
            context: Rendering context.

        Returns:
            Rendered output (type depends on renderer).

        Raises:
            TypeError: If object type is not supported.
        """
        from styledconsole.model import (
            Banner,
            Frame,
            Group,
            Layout,
            Rule,
            Spacer,
            Table,
            Text,
        )

        if isinstance(obj, Text):
            return self._render_text(obj, context)
        elif isinstance(obj, Frame):
            return self._render_frame(obj, context)
        elif isinstance(obj, Banner):
            return self._render_banner(obj, context)
        elif isinstance(obj, Table):
            return self._render_table(obj, context)
        elif isinstance(obj, Layout):
            return self._render_layout(obj, context)
        elif isinstance(obj, Group):
            return self._render_group(obj, context)
        elif isinstance(obj, Spacer):
            return self._render_spacer(obj, context)
        elif isinstance(obj, Rule):
            return self._render_rule(obj, context)
        else:
            raise TypeError(f"Unsupported object type: {type(obj).__name__}")

    # Subclasses must implement these methods
    def _render_text(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError

    def _render_frame(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError

    def _render_banner(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError

    def _render_table(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError

    def _render_layout(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError

    def _render_group(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError

    def _render_spacer(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError

    def _render_rule(self, obj: Any, context: RenderContext) -> Any:
        raise NotImplementedError


__all__ = ["BaseRenderer", "Renderer"]
