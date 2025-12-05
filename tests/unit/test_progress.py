"""Tests for Progress bar wrapper."""

import pytest

from styledconsole import THEMES, Console, StyledProgress
from styledconsole.core.progress import styled_progress


class TestStyledProgress:
    """Tests for StyledProgress class."""

    def test_create_styled_progress(self):
        """Test creating StyledProgress instance."""
        progress = StyledProgress()
        assert progress is not None
        assert progress.finished is True  # No tasks yet

    def test_styled_progress_with_theme(self):
        """Test StyledProgress with theme."""
        progress = StyledProgress(theme=THEMES.DARK)
        assert progress._theme == THEMES.DARK

    def test_styled_progress_context_manager(self):
        """Test using StyledProgress as context manager."""
        with StyledProgress(transient=True) as progress:
            task = progress.add_task("Test", total=10)
            assert task is not None
            for _i in range(10):
                progress.update(task, advance=1)

    def test_add_task_outside_context_raises(self):
        """Test add_task outside context raises RuntimeError."""
        progress = StyledProgress()
        with pytest.raises(RuntimeError, match="context manager"):
            progress.add_task("Test", total=10)

    def test_update_outside_context_raises(self):
        """Test update outside context raises RuntimeError."""
        progress = StyledProgress()
        with pytest.raises(RuntimeError, match="context manager"):
            progress.update(0, advance=1)

    def test_reset_outside_context_raises(self):
        """Test reset outside context raises RuntimeError."""
        progress = StyledProgress()
        with pytest.raises(RuntimeError, match="context manager"):
            progress.reset(0)

    def test_remove_task_outside_context_raises(self):
        """Test remove_task outside context raises RuntimeError."""
        progress = StyledProgress()
        with pytest.raises(RuntimeError, match="context manager"):
            progress.remove_task(0)

    def test_multiple_tasks(self):
        """Test tracking multiple tasks."""
        with StyledProgress(transient=True) as progress:
            task1 = progress.add_task("Task 1", total=5)
            task2 = progress.add_task("Task 2", total=5)

            for _i in range(5):
                progress.update(task1, advance=1)
                progress.update(task2, advance=1)

    def test_indeterminate_progress(self):
        """Test indeterminate progress (no total)."""
        with StyledProgress(transient=True) as progress:
            task = progress.add_task("Working...", total=None)
            progress.update(task, advance=1)
            progress.update(task, advance=1)

    def test_update_description(self):
        """Test updating task description."""
        with StyledProgress(transient=True) as progress:
            task = progress.add_task("Starting...", total=10)
            progress.update(task, description="Processing...")
            progress.update(task, description="Finishing...")

    def test_finished_property(self):
        """Test finished property reflects task completion."""
        with StyledProgress(transient=True) as progress:
            task = progress.add_task("Test", total=2)
            assert not progress.finished
            progress.update(task, advance=2)
            assert progress.finished


class TestConsoleProgress:
    """Tests for Console.progress() method."""

    def test_console_progress_method(self):
        """Test Console has progress method."""
        console = Console()
        assert hasattr(console, "progress")

    def test_console_progress_returns_styled_progress(self):
        """Test Console.progress() returns StyledProgress."""
        console = Console()
        progress = console.progress()
        assert isinstance(progress, StyledProgress)

    def test_console_progress_uses_theme(self):
        """Test Console.progress() uses console's theme."""
        console = Console(theme=THEMES.MONOKAI)
        progress = console.progress()
        assert progress._theme == THEMES.MONOKAI

    def test_console_progress_transient(self):
        """Test Console.progress() with transient option."""
        console = Console()
        progress = console.progress(transient=True)
        assert progress._transient is True

    def test_console_progress_full_workflow(self):
        """Test full progress workflow via Console."""
        console = Console()
        with console.progress(transient=True) as progress:
            task = progress.add_task("Processing", total=5)
            for _ in range(5):
                progress.update(task, advance=1)


class TestStyledProgressFunction:
    """Tests for styled_progress convenience function."""

    def test_styled_progress_function(self):
        """Test styled_progress context manager function."""
        with styled_progress(transient=True) as progress:
            task = progress.add_task("Test", total=3)
            for _ in range(3):
                progress.update(task, advance=1)

    def test_styled_progress_function_with_theme(self):
        """Test styled_progress with theme parameter."""
        with styled_progress(theme=THEMES.NORD, transient=True) as progress:
            task = progress.add_task("Test", total=1)
            progress.update(task, advance=1)
