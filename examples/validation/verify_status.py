from styledconsole.console import Console
from styledconsole.presets.status import StatusEntry, status_summary


def main():
    console = Console()
    console.clear()
    console.rule("Status Frame Verification")
    console.newline()

    results: list[StatusEntry] = [
        {
            "name": "Authentication Module",
            "status": "PASS",
            "duration": 0.45,
        },
        {
            "name": "Database Connection",
            "status": "FAIL",
            "duration": 5.21,
            "message": "ConnectionRefusedError: Unable to connect to localhost:5432",
        },
        {
            "name": "Payment Integration",
            "status": "SKIP",
            "message": "Skipped: API key not found",
        },
        {
            "name": "User Profile Load",
            "status": "ERROR",
            "duration": 1.02,
            "message": "TimeoutError: Request timed out",
        },
        {
            "name": "Legacy System",
            "status": "UNKNOWN",
        },
    ]

    status_summary(results, console=console)

    console.rule("End Verification")


if __name__ == "__main__":
    main()
