"""Progress bar wrapper for StyledConsole.

This module provides a styled progress bar that integrates with
Console themes and provides a simplified API for tracking progress.

Example:
    >>> from styledconsole import Console
    >>> console = Console()
    >>> with console.progress() as progress:
    ...     task = progress.add_task("Processing...", total=100)
    ...     for i in range(100):
    ...         progress.update(task, advance=1)
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

if TYPE_CHECKING:
    from rich.console import Console as RichConsole

    from styledconsole.core.theme import Theme


class StyledProgress:
    """A styled progress bar wrapper around Rich's Progress.

    Provides a simplified API for common progress tracking scenarios
    while integrating with StyledConsole's theme system.

    Attributes:
        theme: Optional theme for styling the progress bar.
        progress: The underlying Rich Progress instance.

    Example:
        >>> progress = StyledProgress()
        >>> with progress:
        ...     task = progress.add_task("Working...", total=50)
        ...     for i in range(50):
        ...         progress.update(task, advance=1)
    """

    def __init__(
        self,
        *,
        theme: Theme | None = None,
        console: RichConsole | None = None,
        transient: bool = False,
        auto_refresh: bool = True,
        expand: bool = False,
    ) -> None:
        """Initialize the styled progress bar.

        Args:
            theme: Optional theme for color styling.
            console: Optional Rich Console instance.
            transient: If True, progress disappears after completion.
            auto_refresh: If True, automatically refresh the display.
            expand: If True, progress bar expands to full width.
        """
        self._theme = theme
        self._transient = transient
        self._auto_refresh = auto_refresh
        self._expand = expand
        self._console = console
        self._progress: Progress | None = None

    def _get_columns(self) -> list[Any]:
        """Build progress columns based on theme."""
        # Get colors from theme or use defaults
        if self._theme:
            primary = self._theme.primary
            muted = self._theme.muted
            success = self._theme.success
        else:
            primary = "cyan"
            muted = "gray"
            success = "green"

        return [
            SpinnerColumn(),
            TextColumn(f"[{primary}]{{task.description}}[/]"),
            BarColumn(complete_style=success, finished_style=success),
            TaskProgressColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            TextColumn(f"[{muted}]•[/]"),
            TimeRemainingColumn(),
        ]

    def _create_progress(self) -> Progress:
        """Create the Rich Progress instance."""
        return Progress(
            *self._get_columns(),
            console=self._console,
            transient=self._transient,
            auto_refresh=self._auto_refresh,
            expand=self._expand,
        )

    def __enter__(self) -> StyledProgress:
        """Start the progress display."""
        self._progress = self._create_progress()
        self._progress.__enter__()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Stop the progress display."""
        if self._progress:
            result = self._progress.__exit__(exc_type, exc_val, exc_tb)
            self._progress = None
            return result
        return False

    def add_task(
        self,
        description: str,
        *,
        total: float | None = 100.0,
        completed: float = 0,
        visible: bool = True,
        **fields: Any,
    ) -> TaskID:
        """Add a new task to track.

        Args:
            description: Task description to display.
            total: Total steps for completion (None for indeterminate).
            completed: Initial completed steps.
            visible: Whether task is visible.
            **fields: Additional fields for the task.

        Returns:
            TaskID for updating this task.

        Raises:
            RuntimeError: If called outside context manager.
        """
        if self._progress is None:
            raise RuntimeError("Progress must be used as a context manager")
        return self._progress.add_task(
            description,
            total=total,
            completed=completed,
            visible=visible,
            **fields,
        )

    def update(
        self,
        task_id: TaskID,
        *,
        advance: float | None = None,
        completed: float | None = None,
        total: float | None = None,
        description: str | None = None,
        visible: bool | None = None,
        **fields: Any,
    ) -> None:
        """Update a task's progress.

        Args:
            task_id: The task to update.
            advance: Amount to advance progress by.
            completed: Set absolute completed value.
            total: Update total steps.
            description: Update task description.
            visible: Update visibility.
            **fields: Update additional fields.

        Raises:
            RuntimeError: If called outside context manager.
        """
        if self._progress is None:
            raise RuntimeError("Progress must be used as a context manager")
        self._progress.update(
            task_id,
            advance=advance,
            completed=completed,
            total=total,
            description=description,
            visible=visible,
            **fields,
        )

    def reset(
        self,
        task_id: TaskID,
        *,
        total: float | None = None,
        completed: float = 0,
        description: str | None = None,
        visible: bool | None = None,
    ) -> None:
        """Reset a task's progress.

        Args:
            task_id: The task to reset.
            total: New total (or keep existing).
            completed: New completed value (default 0).
            description: New description (or keep existing).
            visible: New visibility (or keep existing).

        Raises:
            RuntimeError: If called outside context manager.
        """
        if self._progress is None:
            raise RuntimeError("Progress must be used as a context manager")
        self._progress.reset(
            task_id,
            total=total,
            completed=completed,
            description=description,
            visible=visible,
        )

    def remove_task(self, task_id: TaskID) -> None:
        """Remove a task from the progress display.

        Args:
            task_id: The task to remove.

        Raises:
            RuntimeError: If called outside context manager.
        """
        if self._progress is None:
            raise RuntimeError("Progress must be used as a context manager")
        self._progress.remove_task(task_id)

    @property
    def finished(self) -> bool:
        """Check if all tasks are finished."""
        if self._progress is None:
            return True
        return self._progress.finished


@contextmanager
def styled_progress(
    *,
    theme: Theme | None = None,
    console: RichConsole | None = None,
    transient: bool = False,
) -> Iterator[StyledProgress]:
    """Context manager for styled progress tracking.

    This is a convenience function for creating a StyledProgress
    context manager.

    Args:
        theme: Optional theme for color styling.
        console: Optional Rich Console instance.
        transient: If True, progress disappears after completion.

    Yields:
        StyledProgress instance for adding and updating tasks.

    Example:
        >>> with styled_progress() as progress:
        ...     task = progress.add_task("Working...", total=100)
        ...     for i in range(100):
        ...         progress.update(task, advance=1)
    """
    progress = StyledProgress(theme=theme, console=console, transient=transient)
    with progress:
        yield progress
