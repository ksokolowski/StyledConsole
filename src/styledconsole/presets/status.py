from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rich.markup import escape

from styledconsole.console import Console

if TYPE_CHECKING:
    from styledconsole.console import Console


# Configuration for status themes
STATUS_THEME = {
    "PASS": {"color": "green", "emoji": "✅"},
    "FAIL": {"color": "red", "emoji": "❌"},
    "SKIP": {"color": "yellow", "emoji": "⚠️"},
    "ERROR": {"color": "crimson", "emoji": "💥"},
}
DEFAULT_STATUS = {"color": "blue", "emoji": "ℹ️"}


def status_frame(
    test_name: str,
    status: str,
    duration: float | None = None,
    message: str | None = None,
    *,
    console: Console | None = None,
    **kwargs: Any,
) -> None:
    """
    Displays a status frame for a test result.

    Args:
        test_name: The name of the test.
        status: The status of the test (PASS, FAIL, SKIP, ERROR).
        duration: Optional duration of the test in seconds.
        message: Optional additional message to display.
        console: Optional Console instance to use. If None, a new Console is created.
        **kwargs: Additional arguments passed to console.frame().
    """
    if console is None:
        console = Console()

    status_key = status.upper()
    theme = STATUS_THEME.get(status_key, DEFAULT_STATUS)
    color = theme["color"]
    emoji = theme["emoji"]

    # Build content
    # Escape user input to prevent markup injection
    content_lines = [f"{emoji}  [bold]{escape(test_name)}[/]"]

    details = []
    if duration is not None:
        details.append(f"Duration: {duration:.2f}s")

    if details:
        content_lines.append(f"[{color}]{' | '.join(details)}[/]")

    if message:
        content_lines.append("")
        content_lines.append(escape(message))

    # Default arguments that can be overridden by kwargs
    frame_args = {
        "title": f" {status_key} ",
        "border": "rounded",
        "border_color": color,
        "title_color": color,
        "padding": 1,
        "align": "left",
    }
    frame_args.update(kwargs)

    console.frame(content=content_lines, **frame_args)
