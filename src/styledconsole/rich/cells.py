"""VS16-aware cell_len replacement for Rich.

This module provides a fixed cell_len() that correctly handles VS16
(variation selector 16) emoji sequences in modern terminals.

VS16 Emoji Width Issue:
Rich's cell_len() uses wcwidth which returns 1 for VS16 emoji like ✅, ❌, ⭐.
Modern terminals render these at width 2, causing layout misalignment in
panels, tables, columns, etc.

This implementation can be:
1. Used internally by StyledConsole
2. Submitted as a PR to Rich (textualize/rich)

Usage:
    from styledconsole.rich.cells import cell_len, cached_cell_len

    # Correct width for VS16 emoji
    width = cell_len("✅")  # Returns 2 (correct)
    width = cell_len("Status: ✅")  # Returns 10 (correct)
"""

from __future__ import annotations

from functools import lru_cache

from styledconsole.utils.text import visual_width


def cell_len(text: str) -> int:
    """Calculate the cell width of text, handling VS16 emoji correctly.

    This is a drop-in replacement for rich.cells.cell_len that fixes
    VS16 emoji width calculation for modern terminals.

    Args:
        text: String to measure

    Returns:
        Cell width (number of terminal columns)

    Example:
        >>> cell_len("Hello")
        5
        >>> cell_len("✅")  # VS16 emoji
        2
        >>> cell_len("🚀")  # Standard emoji
        2
        >>> cell_len("Status: ✅")
        10
    """
    return visual_width(text)


@lru_cache(maxsize=4096)
def cached_cell_len(text: str) -> int:
    """Cached version of cell_len for performance.

    Uses LRU cache to avoid recalculating width for repeated strings.
    Cache size of 4096 balances memory usage with hit rate for typical
    terminal UI applications.

    Args:
        text: String to measure

    Returns:
        Cell width (number of terminal columns)
    """
    return cell_len(text)


def get_character_cell_size(character: str) -> int:
    """Get cell size of a single character, VS16-aware.

    Args:
        character: Single character to measure

    Returns:
        Cell width (1 or 2 for most characters)
    """
    return cell_len(character)


__all__ = ["cached_cell_len", "cell_len", "get_character_cell_size"]
