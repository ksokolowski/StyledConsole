"""
StyledConsole - A modern Python library for elegant terminal output.

Provides rich formatting, colors, emoji support, and export capabilities
for creating beautiful command-line interfaces.

Example:
    >>> from styledconsole import Console
    >>> console = Console()
    >>> console.print("Hello, World!", color="blue", bold=True)
"""

from styledconsole.utils.text import (
    pad_to_width,
    split_graphemes,
    strip_ansi,
    truncate_to_width,
    visual_width,
)

__version__ = "0.1.0"
__author__ = "Krzysztof Sokołowski"
__license__ = "Apache-2.0"


# Custom exceptions
class StyledConsoleError(Exception):
    """Base exception for all StyledConsole errors."""

    pass


class RenderError(StyledConsoleError):
    """Raised when rendering fails."""

    pass


class ExportError(StyledConsoleError):
    """Raised when export operation fails."""

    pass


class TerminalError(StyledConsoleError):
    """Raised when terminal detection or interaction fails."""

    pass


# Public API will be added as components are implemented
__all__ = [
    "__version__",
    "StyledConsoleError",
    "RenderError",
    "ExportError",
    "TerminalError",
    # Text utilities
    "visual_width",
    "strip_ansi",
    "split_graphemes",
    "pad_to_width",
    "truncate_to_width",
]
