"""VS16-aware Align replacement for Rich.

This module provides `StyledAlign`, a subclass of `rich.align.Align` that
correctly handles VS16 (variation selector 16) emoji widths when calculating alignment/padding.

Rich's default Align uses cell_len which miscalculates width for VS16 emojis,
causing off-center or misaligned text.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rich.align import Align as RichAlign
from rich.segment import Segment

from styledconsole.rich.cells import cell_len

if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderResult


class StyledAlign(RichAlign):
    """Align class with VS16-aware width calculation.

    Drop-in replacement for rich.align.Align that correctly handles
    emoji width when centering or right-aligning content.
    """

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render with VS16-aware alignment."""
        # First render the content
        rendered = list(console.render(self.renderable, options))

        if self.align == "left":
            yield from rendered
            return

        # Calculate actual content width using VS16-aware cell_len
        lines = Segment.split_lines(rendered)

        for line in lines:
            line_text = "".join(seg.text for seg in line)
            content_width = cell_len(line_text)

            available = options.max_width

            if self.align == "center":
                pad_left = (available - content_width) // 2
                pad_right = available - content_width - pad_left
            else:  # right
                pad_left = available - content_width
                pad_right = 0

            # Ensure non-negative padding
            pad_left = max(0, pad_left)
            pad_right = max(0, pad_right)

            if pad_left > 0:
                yield Segment(" " * pad_left)
            yield from line
            if pad_right > 0:
                yield Segment(" " * pad_right)
            yield Segment.line()
