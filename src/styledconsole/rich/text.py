"""VS16-aware Text replacement for Rich.

This module provides `StyledText`, a subclass of `rich.text.Text` that
correctly handles VS16 (variation selector 16) emoji widths in modern terminals.

Rich's default Text class uses wcwidth which miscalculates VS16 emojis as width 1.
StyledText overrides measurement to use our VS16-aware `cell_len`.
"""

from __future__ import annotations

from rich.measure import Measurement
from rich.text import Text as RichText

from styledconsole.rich.cells import cell_len


class StyledText(RichText):
    """Text class with VS16-aware width calculation.

    Drop-in replacement for rich.text.Text that correctly handles
    emoji width in modern terminals.
    """

    @property
    def cell_len(self) -> int:
        """Calculate cell length using VS16-aware measurement."""
        return cell_len(self.plain)

    def __rich_measure__(self, console: object, options: object) -> Measurement:
        """Override measurement to use VS16-aware cell_len."""
        text = self.plain
        width = cell_len(text)
        return Measurement(width, width)
