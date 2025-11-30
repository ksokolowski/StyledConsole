from __future__ import annotations

from typing import TYPE_CHECKING, Any, NotRequired, TypedDict

from rich.markup import escape

from styledconsole.console import Console
from styledconsole.utils.text import pad_to_width, visual_width

if TYPE_CHECKING:
    from styledconsole.console import Console


# Configuration for status themes
# Using emojis from SAFE_EMOJIS for consistent width handling
# VS16 emojis (⚠️, ℹ️) are now supported via automatic spacing adjustment
STATUS_THEME = {
    "PASS": {"color": "green", "emoji": "✅"},
    "FAIL": {"color": "red", "emoji": "❌"},
    "SKIP": {"color": "yellow", "emoji": "⚠️"},  # VS16 warning sign - auto-adjusted
    "ERROR": {"color": "crimson", "emoji": "💥"},
}
DEFAULT_STATUS = {"color": "blue", "emoji": "ℹ️"}  # VS16 info sign - auto-adjusted


class StatusEntry(TypedDict):
    """Represents a single status entry for summary rendering."""

    name: str
    status: str
    duration: NotRequired[float]
    message: NotRequired[str]


def _build_status_lines(
    name: str,
    status: str,
    duration: float | None,
    message: str | None,
) -> tuple[str, str | None, list[str]]:
    """Build header/detail/message lines with markup (escaping user input)."""

    status_key = status.upper()
    theme = STATUS_THEME.get(status_key, DEFAULT_STATUS)
    color = theme["color"]
    emoji = theme["emoji"]

    header_line = f"{emoji}  [bold]{escape(name)}[/]"

    detail_line: str | None = None
    if duration is not None:
        detail_line = f"[{color}]Duration: {duration:.2f}s[/]"

    message_lines: list[str] = []
    if message:
        message_lines.append(escape(message))

    return header_line, detail_line, message_lines


def _render_status_frame(
    *,
    console: Console,
    name: str,
    status: str,
    duration: float | None,
    message: str | None,
    content_width: int | None,
    **kwargs: Any,
) -> None:
    """Render a single status frame, optionally using a shared content width."""

    status_key = status.upper()
    theme = STATUS_THEME.get(status_key, DEFAULT_STATUS)
    color = theme["color"]

    header_line, detail_line, message_lines = _build_status_lines(
        name=name,
        status=status_key,
        duration=duration,
        message=message,
    )

    candidate_lines: list[str] = [header_line]
    if detail_line is not None:
        candidate_lines.append(detail_line)
    candidate_lines.extend(message_lines)

    # Determine content width: either shared width from caller or per-frame width
    if content_width is None:
        if candidate_lines:
            content_width = max(visual_width(line, markup=True) for line in candidate_lines)
        else:
            content_width = 0

    padded_lines: list[str] = []
    if header_line:
        padded_lines.append(pad_to_width(header_line, content_width, align="left", markup=True))
    if detail_line is not None:
        padded_lines.append(pad_to_width(detail_line, content_width, align="left", markup=True))
    if message_lines:
        padded_lines.append(pad_to_width("", content_width, align="left", markup=True))
        for line in message_lines:
            padded_lines.append(pad_to_width(line, content_width, align="left", markup=True))

    frame_args = {
        "title": f" {status_key} ",
        "border": "rounded",
        "border_color": color,
        "title_color": color,
        "padding": 1,
        "align": "left",
    }
    frame_args.update(kwargs)

    console.frame(content=padded_lines, **frame_args)


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

    _render_status_frame(
        console=console,
        name=test_name,
        status=status,
        duration=duration,
        message=message,
        content_width=None,
        **kwargs,
    )


def status_summary(
    results: list[StatusEntry],
    *,
    console: Console | None = None,
    **kwargs: Any,
) -> None:
    """Render a group of status frames with a shared content width.

    This ensures that related status frames (e.g. in a verification script)
    have consistent interior widths, while reusing the same visual style as
    :func:`status_frame`.
    """

    if console is None:
        console = Console()

    # First pass: compute shared content width based on all visible lines.
    all_candidate_lines: list[str] = []
    for entry in results:
        name = entry["name"]
        status = entry["status"]
        duration = entry.get("duration")
        message = entry.get("message")

        header_line, detail_line, message_lines = _build_status_lines(
            name=name,
            status=status,
            duration=duration,
            message=message,
        )

        all_candidate_lines.append(header_line)
        if detail_line is not None:
            all_candidate_lines.append(detail_line)
        all_candidate_lines.extend(message_lines)

    if all_candidate_lines:
        shared_width = max(visual_width(line, markup=True) for line in all_candidate_lines)
    else:
        shared_width = 0

    # Second pass: render each frame using the shared width.
    for entry in results:
        _render_status_frame(
            console=console,
            name=entry["name"],
            status=entry["status"],
            duration=entry.get("duration"),
            message=entry.get("message"),
            content_width=shared_width,
            **kwargs,
        )
