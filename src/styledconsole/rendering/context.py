"""RenderContext - environment and configuration for rendering.

This module provides the RenderContext dataclass that carries rendering
configuration and environment information to renderers.

Example:
    >>> from styledconsole.rendering import RenderContext
    >>>
    >>> # Auto-detect terminal capabilities
    >>> ctx = RenderContext.auto_detect()
    >>>
    >>> # Create context for HTML output
    >>> ctx = RenderContext.for_html(width=120)
    >>>
    >>> # Create context for image output
    >>> ctx = RenderContext.for_image(width=100, dpi=144)
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from styledconsole.core.theme import Theme


@dataclass
class RenderContext:
    """Environment and configuration for rendering.

    RenderContext carries all information renderers need to produce output:
    - Terminal capabilities (color support, emoji support)
    - Dimensions (width, height)
    - Theme (colors for semantic names)
    - Image-specific options (font, DPI)

    Attributes:
        color: Whether color output is enabled.
        emoji: Whether emoji output is enabled.
        color_depth: Color depth (16, 256, or 16777216 for truecolor).
        width: Output width in characters.
        height: Output height in lines.
        theme: Theme for resolving semantic colors.
        font_family: Font for image rendering.
        font_size: Font size for image rendering.
        dpi: DPI for image rendering.
        background_color: Background color for image rendering.

    Example:
        >>> ctx = RenderContext(width=80, color=True, emoji=True)
        >>> ctx = RenderContext.auto_detect()
    """

    # Terminal capabilities
    color: bool = True
    emoji: bool = True
    color_depth: int = 256  # 16, 256, or 16777216 (truecolor)

    # Dimensions
    width: int = 80
    height: int = 24

    # Theme
    theme: Theme | None = None

    # Image rendering options
    font_family: str = "JetBrains Mono"
    font_size: int = 14
    dpi: int = 144
    background_color: str = "#1e1e1e"

    # Animation
    animate: bool = True

    @classmethod
    def auto_detect(cls) -> RenderContext:
        """Create context by detecting terminal capabilities.

        Detects:
        - Terminal width/height
        - Color support from RenderPolicy
        - Emoji support

        Returns:
            RenderContext configured for current terminal.
        """
        from styledconsole.policy import RenderPolicy

        policy = RenderPolicy.from_env()
        size = shutil.get_terminal_size()

        return cls(
            color=policy.color,
            emoji=policy.emoji,
            color_depth=256,  # Conservative default
            width=size.columns,
            height=size.lines,
        )

    @classmethod
    def for_html(cls, width: int = 120, theme: Theme | None = None) -> RenderContext:
        """Create context optimized for HTML output.

        Args:
            width: Output width in characters.
            theme: Optional theme for color resolution.

        Returns:
            RenderContext for HTML rendering.
        """
        return cls(
            color=True,
            emoji=True,
            color_depth=16777216,  # Full truecolor
            width=width,
            theme=theme,
        )

    @classmethod
    def for_image(
        cls,
        width: int = 120,
        dpi: int = 144,
        font_family: str = "JetBrains Mono",
        font_size: int = 14,
        background_color: str = "#1e1e1e",
        theme: Theme | None = None,
    ) -> RenderContext:
        """Create context optimized for image output.

        Args:
            width: Output width in characters.
            dpi: Image DPI.
            font_family: Font for text rendering.
            font_size: Font size in points.
            background_color: Background color (hex).
            theme: Optional theme for color resolution.

        Returns:
            RenderContext for image rendering.
        """
        return cls(
            color=True,
            emoji=True,
            color_depth=16777216,
            width=width,
            dpi=dpi,
            font_family=font_family,
            font_size=font_size,
            background_color=background_color,
            theme=theme,
        )

    @classmethod
    def minimal(cls) -> RenderContext:
        """Create minimal context with no colors or emoji.

        Useful for testing or plain text output.

        Returns:
            RenderContext with minimal features.
        """
        return cls(
            color=False,
            emoji=False,
            color_depth=16,
            width=80,
        )


__all__ = ["RenderContext"]
