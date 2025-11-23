from __future__ import annotations

from typing import TYPE_CHECKING, NotRequired, TypedDict

from styledconsole.console import Console

if TYPE_CHECKING:
    from styledconsole.console import Console


class TestResult(TypedDict):
    name: str
    status: str  # PASS, FAIL, SKIP, ERROR
    duration: float
    message: NotRequired[str]


def _calculate_status(
    passed: int, failed: int, skipped: int, errors: int, total: int
) -> tuple[str, str, str]:
    """Determine overall status, color, and emoji."""
    if failed > 0 or errors > 0:
        return "FAILED", "red", "❌"
    elif passed == total and total > 0:
        return "PASSED", "green", "✅"
    elif total == 0:
        return "NO TESTS", "yellow", "⚠️"
    else:
        return "MIXED", "yellow", "⚠️"


def _list_failures(console: Console, results: list[TestResult]) -> None:
    """List failed tests."""
    failures = [r for r in results if r["status"].upper() in ("FAIL", "ERROR")]
    if not failures:
        return

    console.newline()
    console.rule("[bold red]Failures & Errors[/]", style="red")
    console.newline()

    for fail in failures:
        status = fail["status"].upper()
        icon = "❌" if status == "FAIL" else "💥"
        color = "red" if status == "FAIL" else "crimson"

        content = [f"{icon} [bold]{fail['name']}[/]"]
        if "message" in fail:
            content.append("")
            content.append(f"[{color}]{fail['message']}[/]")

        console.frame(
            content=content,
            border="minimal",
            border_color=color,
            padding=0,
        )


def test_summary(
    results: list[TestResult],
    total_duration: float | None = None,
    *,
    console: Console | None = None,
) -> None:
    """
    Displays a comprehensive summary of test execution.

    Args:
        results: A list of TestResult dictionaries.
        total_duration: Optional total duration of the test run.
        console: Optional Console instance to use.
    """
    if console is None:
        console = Console()

    total = len(results)
    passed = sum(1 for r in results if r["status"].upper() == "PASS")
    failed = sum(1 for r in results if r["status"].upper() == "FAIL")
    skipped = sum(1 for r in results if r["status"].upper() == "SKIP")
    errors = sum(1 for r in results if r["status"].upper() == "ERROR")

    overall_status, color, emoji = _calculate_status(passed, failed, skipped, errors, total)

    # Header
    console.frame(
        content=[
            f"[bold]{emoji}  Test Execution Summary[/]",
            "",
            f"Total:   [bold]{total}[/]",
            f"Passed:  [green]{passed}[/]",
            f"Failed:  [red]{failed}[/]",
            f"Skipped: [yellow]{skipped}[/]",
            f"Errors:  [crimson]{errors}[/]",
            "",
            f"Duration: {total_duration:.2f}s" if total_duration is not None else "",
        ],
        title=f" {overall_status} ",
        border="thick",
        border_color=color,
        title_color=color,
        padding=1,
        align="left",
    )

    # List failures if any
    _list_failures(console, results)
