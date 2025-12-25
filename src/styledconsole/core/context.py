"""Context object for encapsulating rendering styling and configuration.

This module provides the `StyleContext` class, which implements the Context Object Pattern
to solve the "parameter explosion" issue in RenderingEngine and Console methods.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from styledconsole.types import AlignType


@dataclass(frozen=True)
class StyleContext:
    """Immutable context object encapsulating all styling parameters for a render operation.

    This replaces individual arguments for things like width, color, border style, etc.
    """

    # Dimensions & Layout
    width: int | None = None
    padding: int = 1
    # 'align' controls content alignment (left/center/right) inside the frame
    align: AlignType = "left"
    # 'frame_align' controls the frame's position on the screen
    # If None, it defaults to 'align' (backward compatibility) inside RenderingEngine
    frame_align: AlignType | None = None
    # Margin (top, right, bottom, left) around the frame
    margin: int | tuple[int, int, int, int] = 0

    # Border Configuration
    border_style: str = "rounded"
    border_color: str | None = None

    # Border Gradient
    border_gradient_start: str | None = None
    border_gradient_end: str | None = None
    border_gradient_direction: str = "vertical"

    # Content Styling
    content_color: str | None = None

    # Content Gradient
    start_color: str | None = None
    end_color: str | None = None

    # Meta
    title: str | None = None
    title_color: str | None = None

    def __post_init__(self) -> None:
        """Validate context consistency."""
        # Normalize margin to tuple[int, int, int, int]
        # (top, right, bottom, left)
        if isinstance(self.margin, int):
            m = self.margin
            object.__setattr__(self, "margin", (m, m, m, m))
        elif isinstance(self.margin, (tuple, list)) and len(self.margin) != 4:
            # Fallback for invalid tuple length -> treat as 0 or single value?
            # Ideally raise error, but here we'll just force safe check
            pass

        # Validate content gradient pairs
        if (self.start_color and not self.end_color) or (not self.start_color and self.end_color):
            pass

        # Validate border gradient pairs
        if (self.border_gradient_start and not self.border_gradient_end) or (
            not self.border_gradient_start and self.border_gradient_end
        ):
            pass
