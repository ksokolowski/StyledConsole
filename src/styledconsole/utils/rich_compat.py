"""Rich compatibility utilities for VS16 emoji width fixes.

This module provides shared utilities for patching Rich's cell_len function
to correctly handle VS16 (variation selector 16) emoji sequences in modern
terminals.

VS16 Emoji Width Issue:
Rich's cell_len() uses wcwidth which returns 1 for VS16 emoji like ☁️, ⚙️, ✅.
Modern terminals render these at width 2, causing layout misalignment in
panels, tables, columns, etc.

Usage:
    from styledconsole.utils.rich_compat import patched_cell_len

    with patched_cell_len():
        # Rich operations with correct emoji width
        console.print(panel_with_emoji)
"""

from __future__ import annotations

from collections.abc import Callable, Generator
from contextlib import contextmanager

from styledconsole.utils.terminal import is_modern_terminal

# Rich modules that cache cell_len at import time and need patching.
# We must patch ALL modules that import cell_len directly, not just rich.cells,
# because Python's import creates separate local references.
_RICH_MODULES_TO_PATCH = (
    "rich.cells",
    "rich.segment",
    "rich.text",
    "rich.containers",
    "rich.panel",
    "rich._wrap",
)


@contextmanager
def patched_cell_len() -> Generator[None, None, None]:
    """Context manager to temporarily patch Rich's cell_len with visual_width.

    This fixes VS16 emoji width miscalculation in modern terminals.
    Rich's cell_len returns 1 for VS16 emojis, but modern terminals render
    them at width 2, causing layout misalignment.

    We must patch cell_len in ALL Rich modules that import it directly,
    not just in rich.cells, because Python's import system creates separate
    references.

    Example:
        >>> from styledconsole.utils.rich_compat import patched_cell_len
        >>> with patched_cell_len():
        ...     # Rich Panel/Table/Columns will use correct emoji width
        ...     console.print(StyledPanel("Status: ✅"))
    """
    if not is_modern_terminal():
        # No patch needed for non-modern terminals
        yield
        return

    # Import Rich modules dynamically to avoid import-time side effects
    import rich._wrap
    import rich.cells
    import rich.containers
    import rich.panel
    import rich.segment
    import rich.text

    from styledconsole.utils.text import visual_width

    def _patched_cell_len(text: str) -> int:
        """Use visual_width for accurate emoji width in modern terminals."""
        return visual_width(text)

    # Clear LRU cache FIRST to prevent stale cached width values
    if hasattr(rich.cells.cached_cell_len, "cache_clear"):
        rich.cells.cached_cell_len.cache_clear()

    # Save original functions from ALL modules that use cell_len
    originals: dict[str, Callable[[str], int]] = {
        "cells.cell_len": rich.cells.cell_len,
        "cells.cached_cell_len": rich.cells.cached_cell_len,
        "segment.cell_len": rich.segment.cell_len,
        "segment.cached_cell_len": rich.segment.cached_cell_len,
        "text": rich.text.cell_len,
        "containers": rich.containers.cell_len,
        "panel": rich.panel.cell_len,
        "_wrap": rich._wrap.cell_len,
    }

    # Patch ALL modules including segment and cached_cell_len
    rich.cells.cell_len = _patched_cell_len  # type: ignore[assignment]
    rich.cells.cached_cell_len = _patched_cell_len  # type: ignore[assignment]
    rich.segment.cell_len = _patched_cell_len  # type: ignore[assignment]
    rich.segment.cached_cell_len = _patched_cell_len  # type: ignore[assignment]
    rich.text.cell_len = _patched_cell_len  # type: ignore[assignment]
    rich.containers.cell_len = _patched_cell_len  # type: ignore[assignment]
    rich.panel.cell_len = _patched_cell_len  # type: ignore[assignment]
    rich._wrap.cell_len = _patched_cell_len  # type: ignore[assignment]

    try:
        yield
    finally:
        # Restore ALL originals
        rich.cells.cell_len = originals["cells.cell_len"]  # type: ignore[assignment]
        rich.cells.cached_cell_len = originals["cells.cached_cell_len"]  # type: ignore[assignment]
        rich.segment.cell_len = originals["segment.cell_len"]  # type: ignore[assignment]
        rich.segment.cached_cell_len = originals["segment.cached_cell_len"]  # type: ignore[assignment]
        rich.text.cell_len = originals["text"]  # type: ignore[assignment]
        rich.containers.cell_len = originals["containers"]  # type: ignore[assignment]
        rich.panel.cell_len = originals["panel"]  # type: ignore[assignment]
        rich._wrap.cell_len = originals["_wrap"]  # type: ignore[assignment]


__all__ = ["patched_cell_len"]
