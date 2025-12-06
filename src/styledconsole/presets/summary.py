from __future__ import annotations

from typing import TYPE_CHECKING, NotRequired, TypedDict

from styledconsole.console import Console
from styledconsole.icons import icons

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
    """Determine overall status, color, and icon.

    Uses semantic color names and icons module for policy-aware rendering.
    """
    if failed > 0 or errors > 0:
        return "FAILED", "error", str(icons.CROSS_MARK)
    elif passed == total and total > 0:
        return "PASSED", "success", str(icons.CHECK_MARK_BUTTON)
    elif total == 0:
        return "NO TESTS", "warning", str(icons.WARNING)
    else:
        return "MIXED", "warning", str(icons.WARNING)


def _list_failures(console: Console, results: list[TestResult]) -> None:
    """List failed tests.

    Uses semantic color 'error' and icons module for policy-aware rendering.
    """
    failures = [r for r in results if r["status"].upper() in ("FAIL", "ERROR")]
    if not failures:
        return

    console.newline()
    console.rule("[bold]Failures & Errors[/]", style="error")
    console.newline()

    for fail in failures:
        status = fail["status"].upper()
        icon = str(icons.CROSS_MARK) if status == "FAIL" else str(icons.FIRE)

        content = [f"{icon} [bold]{fail['name']}[/]"]
        if "message" in fail:
            content.append("")
            content.append(fail["message"])

        console.frame(
            content=content,
            border="minimal",
            border_color="error",
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

    overall_status, color, icon = _calculate_status(passed, failed, skipped, errors, total)

    # Header - uses semantic colors that themes can resolve
    # The border_color uses semantic names resolved by console.frame()
    console.frame(
        content=[
            f"[bold]{icon}  Test Execution Summary[/]",
            "",
            f"Total:   [bold]{total}[/]",
            f"Passed:  {passed}",
            f"Failed:  {failed}",
            f"Skipped: {skipped}",
            f"Errors:  {errors}",
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
