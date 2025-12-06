"""Progress bar wrapper for StyledConsole.

This module provides a styled progress bar that integrates with
Console themes and provides a simplified API for tracking progress.

Policy-aware: When terminal capabilities are limited (TERM=dumb, NO_COLOR,
piped output), the progress bar automatically falls back to a simple
text-based format that works everywhere.

Example:
    >>> from styledconsole import Console
    >>> console = Console()
    >>> with console.progress() as progress:
    ...     task = progress.add_task("Processing...", total=100)
    ...     for i in range(100):
    ...         progress.update(task, advance=1)
"""

from __future__ import annotations

import sys
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Literal

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    ProgressColumn,
    SpinnerColumn,
    Task,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.text import Text

if TYPE_CHECKING:
    from rich.console import Console as RichConsole

    from styledconsole.core.theme import Theme
    from styledconsole.policy import RenderPolicy


@dataclass
class _FallbackTask:
    """Internal task state for fallback progress mode."""

    task_id: int
    description: str
    total: float | None
    completed: float = 0.0
    visible: bool = True
    start_time: float = field(default_factory=time.time)
    last_print_time: float = field(default_factory=time.time)


class MofNThemedColumn(ProgressColumn):
    """A themed column showing completed/total steps."""

    def __init__(self, color: str = "gray", table_column: Any | None = None):
        super().__init__(table_column=table_column)
        self.color = color

    def render(self, task: Task) -> Text:
        """Show completed/total."""
        completed = int(task.completed)
        if task.total is None:
            return Text(f"{completed}/?", style=self.color)
        return Text(f"{completed}/{int(task.total)}", style=self.color)


class StyledProgress:
    """A styled progress bar wrapper around Rich's Progress.

    Provides a simplified API for common progress tracking scenarios
    while integrating with StyledConsole's theme system.

    Policy-aware: When policy indicates limited terminal (unicode=False,
    color=False, or non-TTY), falls back to simple text-based progress
    that works in all environments.

    Attributes:
        theme: Optional theme for styling the progress bar.
        progress: The underlying Rich Progress instance.
        policy: Optional RenderPolicy for environment-aware rendering.

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
        policy: RenderPolicy | None = None,
    ) -> None:
        """Initialize the styled progress bar.

        Args:
            theme: Optional theme for color styling.
            console: Optional Rich Console instance.
            transient: If True, progress disappears after completion.
            auto_refresh: If True, automatically refresh the display.
            expand: If True, progress bar expands to full width.
            policy: Optional RenderPolicy for environment-aware rendering.
                    If provided and indicates limited terminal, uses text fallback.
        """
        self._theme = theme
        self._transient = transient
        self._auto_refresh = auto_refresh
        self._expand = expand
        self._console = console
        self._policy = policy
        self._progress: Progress | None = None
        self._use_fallback = self._should_use_fallback()
        self._fallback_tasks: dict[int, _FallbackTask] = {}
        self._next_task_id = 0
        self._in_context = False

    def _should_use_fallback(self) -> bool:
        """Determine if we should use text-based fallback.

        Returns True when:
        - Not a TTY (piped, redirected)
        - Policy disables unicode (TERM=dumb)
        - Policy disables color (NO_COLOR)
        """
        # Check TTY - if not TTY and no policy override, use fallback
        # But if policy explicitly enables color, Rich can still work
        if not sys.stdout.isatty() and (self._policy is None or not self._policy.color):
            return True

        # Check policy
        # TERM=dumb means no cursor control, must use fallback
        return self._policy is not None and not self._policy.unicode

    def _get_columns(self) -> list[Any]:
        """Build progress columns based on theme."""
        # Check if we are using a specific theme or just default
        is_themed = self._theme is not None and self._theme.name != "default"

        if is_themed and self._theme:
            primary = self._theme.primary
            secondary = self._theme.secondary
            muted = self._theme.muted

            return [
                SpinnerColumn(style=primary),
                TextColumn(f"[{primary}]{{task.description}}[/]"),
                BarColumn(complete_style=primary, finished_style=primary, pulse_style=primary),
                TaskProgressColumn(text_format=f"[{secondary}]{{task.percentage:>3.0f}}%[/]"),
                MofNThemedColumn(color=muted),
                TimeElapsedColumn(),
                TextColumn(f"[{muted}]•[/]"),
                TimeRemainingColumn(),
            ]

        # Default / Classic Behavior (Green Bar)
        return [
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="green", finished_style="green", pulse_style="green"),
            TaskProgressColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            TextColumn("•"),
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

    def _format_time(self, seconds: float) -> str:
        """Format elapsed time as MM:SS."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def _print_fallback_progress(self, task: _FallbackTask, force: bool = False) -> None:
        """Print text-based progress for a task.

        Args:
            task: The task to print progress for.
            force: Force print even if recently printed.
        """
        if not task.visible:
            return

        # Rate limit to avoid spamming output (print every 0.5 seconds or on force)
        now = time.time()
        if not force and (now - task.last_print_time) < 0.5:
            return

        task.last_print_time = now

        elapsed = now - task.start_time
        elapsed_str = self._format_time(elapsed)

        if task.total is not None and task.total > 0:
            percent = min(100, int((task.completed / task.total) * 100))
            bar_width = 20
            filled = int(bar_width * task.completed / task.total)
            bar = "#" * filled + "." * (bar_width - filled)

            # Estimate remaining time
            if task.completed > 0:
                rate = task.completed / elapsed
                remaining = (task.total - task.completed) / rate if rate > 0 else 0
                remaining_str = self._format_time(remaining)
            else:
                remaining_str = "--:--"

            line = (
                f"  {task.description} [{bar}] {percent:3d}% "
                f"({int(task.completed)}/{int(task.total)}) "
                f"{elapsed_str} / {remaining_str}"
            )
        else:
            # Indeterminate progress
            line = f"  {task.description} ... {elapsed_str}"

        print(line, file=sys.stderr, flush=True)

    def __enter__(self) -> StyledProgress:
        """Start the progress display."""
        self._in_context = True
        if not self._use_fallback:
            self._progress = self._create_progress()
            self._progress.__enter__()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Literal[False]:
        """Stop the progress display."""
        self._in_context = False

        if self._use_fallback:
            # Print final state for all tasks
            for task in self._fallback_tasks.values():
                if task.visible and task.total and task.completed >= task.total:
                    self._print_fallback_progress(task, force=True)
            self._fallback_tasks.clear()
            return False

        if self._progress:
            self._progress.__exit__(exc_type, exc_val, exc_tb)
            self._progress = None
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
        if not self._in_context:
            raise RuntimeError("Progress must be used as a context manager")

        if self._use_fallback:
            task_id = self._next_task_id
            self._next_task_id += 1
            task = _FallbackTask(
                task_id=task_id,
                description=description,
                total=total,
                completed=completed,
                visible=visible,
            )
            self._fallback_tasks[task_id] = task
            # Print initial state
            self._print_fallback_progress(task, force=True)
            return TaskID(task_id)

        if self._progress is None:
            raise RuntimeError("Progress must be used as a context manager")
        return self._progress.add_task(
            description,
            total=total,
            completed=int(completed),
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
        if not self._in_context:
            raise RuntimeError("Progress must be used as a context manager")

        if self._use_fallback:
            task = self._fallback_tasks.get(int(task_id))
            if task:
                if advance is not None:
                    task.completed += advance
                if completed is not None:
                    task.completed = completed
                if total is not None:
                    task.total = total
                if description is not None:
                    task.description = description
                if visible is not None:
                    task.visible = visible
                self._print_fallback_progress(task)
            return

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
        if not self._in_context:
            raise RuntimeError("Progress must be used as a context manager")

        if self._use_fallback:
            task = self._fallback_tasks.get(int(task_id))
            if task:
                if total is not None:
                    task.total = total
                task.completed = completed
                if description is not None:
                    task.description = description
                if visible is not None:
                    task.visible = visible
                task.start_time = time.time()
                self._print_fallback_progress(task, force=True)
            return

        if self._progress is None:
            raise RuntimeError("Progress must be used as a context manager")
        self._progress.reset(
            task_id,
            total=total,
            completed=int(completed),
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
        if not self._in_context:
            raise RuntimeError("Progress must be used as a context manager")

        if self._use_fallback:
            self._fallback_tasks.pop(int(task_id), None)
            return

        if self._progress is None:
            raise RuntimeError("Progress must be used as a context manager")
        self._progress.remove_task(task_id)

    @property
    def finished(self) -> bool:
        """Check if all tasks are finished."""
        if self._use_fallback:
            return all(
                t.total is None or t.completed >= t.total for t in self._fallback_tasks.values()
            )

        if self._progress is None:
            return True
        return self._progress.finished


@contextmanager
def styled_progress(
    *,
    theme: Theme | None = None,
    console: RichConsole | None = None,
    transient: bool = False,
    policy: RenderPolicy | None = None,
) -> Iterator[StyledProgress]:
    """Context manager for styled progress tracking.

    This is a convenience function for creating a StyledProgress
    context manager.

    Args:
        theme: Optional theme for color styling.
        console: Optional Rich Console instance.
        transient: If True, progress disappears after completion.
        policy: Optional RenderPolicy for environment-aware rendering.

    Yields:
        StyledProgress instance for adding and updating tasks.

    Example:
        >>> with styled_progress() as progress:
        ...     task = progress.add_task("Working...", total=100)
        ...     for i in range(100):
        ...         progress.update(task, advance=1)
    """
    progress = StyledProgress(theme=theme, console=console, transient=transient, policy=policy)
    with progress:
        yield progress
