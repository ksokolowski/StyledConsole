# Code Review: `src/styledconsole/presets/status.py`

## Overview

I have performed a code review of `src/styledconsole/presets/status.py` focusing on logic, security, maintainability, and extensibility.

## Findings

| Line Number | Code Snippet                              | Issue                                                                                                                                                                   | Recommended Solution                                                                                               |
| :---------- | :---------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| **35-49**   | `if status == "PASS": ... elif ...`       | **High Cyclomatic Complexity / Repetitive Logic**: The `if/elif` chain is verbose and hard to extend.                                                                   | Refactor into a configuration dictionary (e.g., `STATUS_THEME`) mapping statuses to their color/emoji pairs.       |
| **52, 59**  | `f"{emoji} [bold]{test_name}[/]"`         | **Markup Injection Vulnerability**: If `test_name` or `message` contains Rich markup tags (e.g., `[red]`, `[/]`), it will break the rendering or allow style injection. | Sanitize inputs using `rich.markup.escape()` before embedding them in markup strings.                              |
| **11**      | `def status_frame(...)`                   | **Lack of Extensibility**: The function signature is fixed. Users cannot customize other `console.frame` parameters like `width` or `style`.                            | Add `**kwargs` to the function signature and pass them to the `console.frame()` call.                              |
| **68-72**   | `border="rounded", padding=1, ...`        | **Hardcoded Styling**: Styling choices are hardcoded inside the function, making it difficult to reuse this preset with different aesthetics.                           | Move defaults to constants or allow overriding them via `**kwargs`.                                                |
| **29-30**   | `if console is None: console = Console()` | **Hidden Object Creation**: Creating a new `Console` instance for every call (if not provided) can be expensive and may bypass global configuration.                    | This is acceptable for a utility, but consider adding a module-level default or documenting this behavior clearly. |

## Refactored Solution

The following refactoring addresses the identified issues:

1. **Security**: Uses `rich.markup.escape` to prevent injection.
1. **Maintainability**: Uses a `STATUS_THEME` dictionary.
1. **Extensibility**: Accepts `**kwargs` for flexible styling.

```python
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
    **kwargs: Any,  # Allow passing extra arguments to console.frame
) -> None:
    """
    Displays a status frame for a test result.

    Args:
        test_name: The name of the test.
        status: The status of the test (PASS, FAIL, SKIP, ERROR).
        duration: Optional duration of the test in seconds.
        message: Optional additional message to display.
        console: Optional Console instance.
        **kwargs: Additional arguments passed to console.frame().
    """
    if console is None:
        console = Console()

    # Normalize status and get theme
    status_key = status.upper()
    theme = STATUS_THEME.get(status_key, DEFAULT_STATUS)
    color = theme["color"]
    emoji = theme["emoji"]

    # Build content with escaped strings to prevent markup injection
    # Note: We escape the user input but keep our own markup tags
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
    # Update defaults with any user-provided kwargs
    frame_args.update(kwargs)

    console.frame(content=content_lines, **frame_args)
```
