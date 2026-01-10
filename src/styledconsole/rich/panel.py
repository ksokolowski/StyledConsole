"""VS16-aware Panel replacement for Rich.

This module provides `StyledPanel`, a subclass of `rich.panel.Panel` that
correctly handles VS16 (variation selector 16) emoji widths in titles and content.

Rich's default Panel miscalculates width when titles or content contain VS16 emojis,
leading to broken borders or misaligned titles.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.measure import Measurement
from rich.panel import Panel as RichPanel

from styledconsole.rich.cells import cell_len

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions


class StyledPanel(RichPanel):
    """Panel class with VS16-aware width calculation.

    Drop-in replacement for rich.panel.Panel that correctly handles
    emoji width in panel titles and content.
    """

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        """Override measurement to use VS16-aware cell_len."""
        # Measure content
        renderable = self.renderable
        if hasattr(renderable, "__rich_measure__"):
            content_measure = renderable.__rich_measure__(console, options)
        else:
            # Fallback: render and measure
            content_width = cell_len(str(renderable))
            content_measure = Measurement(content_width, content_width)

        from rich.padding import Padding

        _, pad_right, _, pad_left = Padding.unpack(self.padding)
        padding_width = pad_left + pad_right
        border_width = 2

        min_width = content_measure.minimum + border_width + padding_width
        max_width = content_measure.maximum + border_width + padding_width

        # Account for title if present
        if self.title:
            title_width = cell_len(str(self.title)) + 4  # Title + spacing
            min_width = max(min_width, title_width + border_width)

        return Measurement(min_width, max_width)
