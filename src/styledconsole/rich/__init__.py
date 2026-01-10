"""VS16-aware Rich class replacements.

This package provides drop-in replacements for Rich classes that fix VS16
(variation selector 16) emoji width calculation issues in modern terminals.

These implementations can be:
1. Used internally by StyledConsole for correct emoji rendering
2. Submitted as PRs to Rich (textualize/rich)

Usage:
    from styledconsole.rich import cell_len, StyledText, StyledPanel, StyledAlign

    # Use cell_len for accurate emoji width measurement
    width = cell_len("Hello ✅ World")  # Correctly returns 14

    # Use StyledPanel instead of rich.panel.Panel
    panel = StyledPanel("Content with ✅ emoji", title="Status")
"""

from styledconsole.rich.cells import cached_cell_len, cell_len

__all__ = [
    "cached_cell_len",
    "cell_len",
]
