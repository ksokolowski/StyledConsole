"""Frame rendering with borders, padding, and titles.

This module provides high-level frame rendering that builds on BorderStyle primitives.

v0.4.0: FrameRenderer now uses Rich Panel via adapter pattern for ANSI-safe rendering.
Legacy render() API maintained for backward compatibility.

.. deprecated:: 0.4.0
    Direct use of ``FrameRenderer`` is deprecated. Use ``Console.frame()`` instead.
    ``FrameRenderer`` will be removed in v1.0.0.
"""

import warnings
from dataclasses import dataclass

from styledconsole.core.frame_adapter import FrameAdapter
from styledconsole.core.styles import BorderStyle
from styledconsole.types import AlignType


@dataclass
class Frame:
    """Configuration for a rendered frame.

    Attributes:
        content: Text content to display (single line or list of lines)
        title: Optional title for the frame
        border: Border style name or BorderStyle object
        width: Frame width (auto-calculated if None)
        padding: Internal padding (left/right spaces)
        align: Content alignment ("left", "center", "right")
        min_width: Minimum frame width (when auto-calculating)
        max_width: Maximum frame width (when auto-calculating)
        content_color: Color for content text (hex, rgb, or CSS4 name)
        border_color: Color for border (hex, rgb, or CSS4 name)
        title_color: Color for title (hex, rgb, or CSS4 name)
        start_color: Starting color for content gradient (overrides content_color)
        end_color: Ending color for content gradient
    """

    content: str | list[str]
    title: str | None = None
    border: str | BorderStyle = "solid"
    width: int | None = None
    padding: int = 1
    align: AlignType = "left"
    min_width: int = 20
    max_width: int = 100
    content_color: str | None = None
    border_color: str | None = None
    title_color: str | None = None
    start_color: str | None = None
    end_color: str | None = None


class FrameRenderer(FrameAdapter):
    """Renders frames with borders, titles, and padding.

    .. deprecated:: 0.4.0
        Direct use of ``FrameRenderer`` is deprecated and will be removed in v1.0.0.
        Use ``Console.frame()`` instead for new code.

    v0.4.0+: This class now uses Rich Panel rendering via FrameAdapter.
    The legacy custom rendering has been replaced with Rich's ANSI-safe Panel.

    Migration Guide:
        >>> # ❌ Deprecated (will be removed in v1.0.0):
        >>> from styledconsole.core.frame import FrameRenderer
        >>> renderer = FrameRenderer()
        >>> lines = renderer.render("Hello, World!", border="solid")
        >>> for line in lines:
        ...     print(line)

        >>> # ✅ Recommended (use Console facade):
        >>> from styledconsole import Console
        >>> console = Console()
        >>> console.frame("Hello, World!", border="solid")

    Note:
        While still functional, consider using ``Console.frame()`` for new code.
        The ``FrameRenderer`` class provides backward compatibility but delegates
        to Rich Panel internally.

    Example:
        >>> renderer = FrameRenderer()  # doctest: +SKIP
        >>> lines = renderer.render("Hello, World!", border="solid")
        >>> for line in lines:
        ...     print(line)
    """

    # Valid alignment options (kept for compatibility)
    VALID_ALIGNMENTS = {"left", "center", "right"}

    def __init__(self) -> None:
        """Initialize the frame renderer.

        .. deprecated:: 0.4.0
            Use ``Console.frame()`` instead. This class will be removed in v1.0.0.

        Raises:
            DeprecationWarning: When instantiated directly (suppressed in tests).
        """
        # Issue deprecation warning
        warnings.warn(
            "FrameRenderer is deprecated as of v0.4.0 and will be removed in v1.0.0. "
            "Use Console.frame() instead. See https://github.com/your-repo/styledconsole "
            "for migration guide.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__()

    # render() method inherited from FrameAdapter
    # No override needed - adapter handles all the logic


__all__ = [
    "Frame",
    "FrameRenderer",
    "AlignType",
]
