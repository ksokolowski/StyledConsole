"""Custom exceptions for the StyledConsole library."""


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
