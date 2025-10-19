"""Type aliases and protocols for StyledConsole.

This module provides centralized type definitions used across the library,
including Literal types for better IDE support and type checking.
"""

from typing import Literal, Protocol

# Type alias for alignment options
AlignType = Literal["left", "center", "right"]

# Type alias for color values (hex string, rgb string, named color, or RGB tuple)
ColorType = str | tuple[int, int, int]


class Renderer(Protocol):
    """Protocol for renderer implementations.

    Renderers convert content into formatted output lines.
    This protocol enables custom renderer implementations.
    """

    def render(self, content: str | list[str], **kwargs) -> list[str]:
        """Render content into formatted output lines.

        Args:
            content: Content to render (single string or list of lines)
            **kwargs: Renderer-specific options

        Returns:
            List of formatted output lines ready for display
        """
        ...


__all__ = [
    "AlignType",
    "ColorType",
    "Renderer",
]
