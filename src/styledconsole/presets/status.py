from __future__ import annotations

from typing import TYPE_CHECKING, Any, NotRequired, TypedDict

from rich.markup import escape

from styledconsole.console import Console
from styledconsole.icons import icons

if TYPE_CHECKING:
    from styledconsole.console import Console


# Configuration for status themes
# Using icons module for policy-aware emoji/ASCII fallback
# Colors use semantic names that themes can resolve (success, error, warning, info)
STATUS_THEME = {
    "PASS": {"color": "success", "icon": icons.CHECK},
    "FAIL": {"color": "error", "icon": icons.CROSS},
    "SKIP": {"color": "warning", "icon": icons.WARNING},
    "ERROR": {"color": "error", "icon": icons.FIRE},
}
DEFAULT_STATUS = {"color": "info", "icon": icons.INFO}


class StatusEntry(TypedDict):
    """Represents a single status entry for summary rendering."""

    name: str
    status: str
    duration: NotRequired[float]
    message: NotRequired[str]


def _build_status_content(
    name: str,
    status: str,
    duration: float | None,
    message: str | None,
) -> tuple[list[str], str]:
    """Build content lines and color for a status frame.

    Returns:
        Tuple of (content_lines, color) for the frame.
    """
    status_key = status.upper()
    theme = STATUS_THEME.get(status_key, DEFAULT_STATUS)
    color = theme["color"]
    icon = str(theme["icon"])  # Uses icons module for policy-aware rendering

    lines: list[str] = [f"{icon}  [bold]{escape(name)}[/]"]

    if duration is not None:
        lines.append(f"[{color}]Duration: {duration:.2f}s[/]")

    if message:
        lines.append("")
        lines.append(escape(message))

    return lines, color


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

    content, _ = _build_status_content(
        name=test_name,
        status=status_key,
        duration=duration,
        message=message,
    )

    frame_args = {
        "title": f" {status_key} ",
        "border": "rounded",
        "border_color": color,
        "title_color": color,
        "padding": 1,
        "align": "left",
    }
    frame_args.update(kwargs)

    console.frame(content=content, **frame_args)


def status_summary(
    results: list[StatusEntry],
    *,
    console: Console | None = None,
    **kwargs: Any,
) -> None:
    """Render a group of status frames with aligned widths.

    Uses console.group() with align_widths=True to ensure all status frames
    have consistent interior widths, creating a visually cohesive display.

    Args:
        results: List of StatusEntry dictionaries with name, status, duration, message.
        console: Optional Console instance to use.
        **kwargs: Additional arguments passed to each frame.
    """
    if console is None:
        console = Console()

    # Use context manager with align_widths for automatic width alignment
    with console.group(align_widths=True, gap=1):
        for entry in results:
            status_key = entry["status"].upper()
            theme = STATUS_THEME.get(status_key, DEFAULT_STATUS)
            color = theme["color"]

            content, _ = _build_status_content(
                name=entry["name"],
                status=status_key,
                duration=entry.get("duration"),
                message=entry.get("message"),
            )

            frame_args = {
                "title": f" {status_key} ",
                "border": "rounded",
                "border_color": color,
                "title_color": color,
                "padding": 1,
                "align": "left",
            }
            frame_args.update(kwargs)

            console.frame(content=content, **frame_args)
