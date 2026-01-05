"""Context object for encapsulating rendering styling and configuration.

This module provides the `StyleContext` class, which implements the Context Object Pattern
to solve the "parameter explosion" issue in RenderingEngine and Console methods.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from styledconsole.effects.spec import EffectSpec
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

    # Border Gradient (DEPRECATED: Use effect= instead)
    border_gradient_start: str | None = None
    border_gradient_end: str | None = None
    border_gradient_direction: str = "vertical"

    # Content Styling
    content_color: str | None = None

    # Content Gradient (DEPRECATED: Use effect= instead)
    start_color: str | None = None
    end_color: str | None = None

    # Effect System (v0.9.9.3+)
    effect: EffectSpec | None = None

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
        elif isinstance(self.margin, (tuple, list)):
            if len(self.margin) == 4:
                object.__setattr__(self, "margin", tuple(self.margin))
            else:
                raise ValueError(
                    "`margin` must be an int or a 4-tuple/list (top, right, bottom, left)"
                )

        # Validate content gradient pairs: both or none
        if bool(self.start_color) ^ bool(self.end_color):
            raise ValueError("`start_color` and `end_color` must both be provided or both be None")

        # Validate border gradient pairs: both or none
        if bool(self.border_gradient_start) ^ bool(self.border_gradient_end):
            raise ValueError(
                "`border_gradient_start` and `border_gradient_end` "
                "must both be provided or both be None"
            )
