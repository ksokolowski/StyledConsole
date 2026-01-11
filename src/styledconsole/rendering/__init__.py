"""Renderer layer for StyledConsole - output generation from ConsoleObjects.

This module provides renderers that convert ConsoleObjects to various output formats:
- TerminalRenderer: ANSI terminal output via Rich
- HTMLRenderer: HTML output (fragment or document)

Key Concepts:
- Renderers implement the Renderer protocol
- RenderContext carries environment and configuration
- Each renderer handles type dispatch internally

Example:
    >>> from styledconsole.rendering import (
    ...     TerminalRenderer,
    ...     HTMLRenderer,
    ...     RenderContext,
    ... )
    >>> from styledconsole.model import Frame, Text
    >>>
    >>> # Create a frame
    >>> frame = Frame(
    ...     content=Text(content="Hello World"),
    ...     title="Greeting",
    ...     effect="ocean",
    ... )
    >>>
    >>> # Render to terminal
    >>> terminal = TerminalRenderer()
    >>> terminal.render(frame)
    >>>
    >>> # Render to HTML
    >>> html_renderer = HTMLRenderer()
    >>> html = html_renderer.render_fragment(frame)
    >>> html_renderer.render_document(frame, "output.html")
    >>>
    >>> # Use custom context
    >>> ctx = RenderContext(width=120, color=True)
    >>> terminal.render(frame, context=ctx)
"""

from styledconsole.rendering.base import BaseRenderer, Renderer
from styledconsole.rendering.context import RenderContext
from styledconsole.rendering.html import HTMLRenderer
from styledconsole.rendering.terminal import TerminalRenderer

__all__ = [
    "BaseRenderer",
    "HTMLRenderer",
    "RenderContext",
    "Renderer",
    "TerminalRenderer",
]
