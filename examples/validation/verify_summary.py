from styledconsole.console import Console
from styledconsole.presets.summary import TestResult, test_summary


def main():
    console = Console()
    console.clear()
    console.rule("Test Summary Verification")
    console.newline()

    # Scenario 1: All Passed
    results_pass: list[TestResult] = [
        {"name": "test_auth", "status": "PASS", "duration": 0.12},
        {"name": "test_db", "status": "PASS", "duration": 0.45},
        {"name": "test_api", "status": "PASS", "duration": 0.23},
    ]
    test_summary(results_pass, total_duration=0.80, console=console)
    console.newline()
    console.rule()
    console.newline()

    # Scenario 2: Mixed Results
    results_mixed: list[TestResult] = [
        {"name": "test_auth", "status": "PASS", "duration": 0.12},
        {
            "name": "test_payment",
            "status": "FAIL",
            "duration": 1.05,
            "message": "AssertionError: 200 != 500",
        },
        {"name": "test_legacy", "status": "SKIP", "duration": 0.00},
        {"name": "test_profile", "status": "ERROR", "duration": 0.05, "message": "TimeoutError"},
    ]
    test_summary(results_mixed, total_duration=1.22, console=console)
    console.newline()
    console.rule()
    console.newline()

    # Scenario 3: No Tests
    test_summary([], total_duration=0.0, console=console)

    console.newline()
    console.rule("End Verification")


if __name__ == "__main__":
    main()
