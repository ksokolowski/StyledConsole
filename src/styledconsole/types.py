"""Type aliases and protocols for StyledConsole.

This module provides centralized type definitions used across the library,
including Literal types for better IDE support and type checking.
"""

from typing import Literal, Protocol, TypedDict

# Type alias for alignment options
AlignType = Literal["left", "center", "right"]

# Type alias for layout options
LayoutType = Literal["vertical"]

# Type alias for color values (hex string, rgb string, named color, or RGB tuple)
ColorType = str | tuple[int, int, int]


class FrameGroupItem(TypedDict, total=False):
    """Type definition for frame_group item dictionaries.

    Only 'content' is required. All other fields are optional and will
    inherit from the outer frame_group settings if not specified.
    """

    content: str | list[str]  # Required: frame content
    title: str | None  # Optional: frame title
    border: str  # Optional: border style (default: inherit)
    border_color: str | None  # Optional: border color
    content_color: str | None  # Optional: content color
    title_color: str | None  # Optional: title color


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
    "FrameGroupItem",
    "LayoutType",
    "Renderer",
]
