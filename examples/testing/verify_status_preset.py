from styledconsole.console import Console
from styledconsole.presets.status import status_frame


def main():
    console = Console()
    console.clear()
    console.rule("Status Frame Verification")
    console.newline()

    # Test Case 1: PASS
    status_frame("Authentication Module", "PASS", duration=0.45, console=console)
    console.newline()

    # Test Case 2: FAIL with message
    status_frame(
        "Database Connection",
        "FAIL",
        duration=5.21,
        message="ConnectionRefusedError: Unable to connect to localhost:5432",
        console=console,
    )
    console.newline()

    # Test Case 3: SKIP
    status_frame(
        "Payment Integration", "SKIP", message="Skipped: API key not found", console=console
    )
    console.newline()

    # Test Case 4: ERROR
    status_frame(
        "User Profile Load",
        "ERROR",
        duration=1.02,
        message="TimeoutError: Request timed out",
        console=console,
    )
    console.newline()

    # Test Case 5: Custom/Unknown Status
    status_frame("Legacy System", "UNKNOWN", console=console)
    console.newline()

    console.rule("End Verification")


if __name__ == "__main__":
    main()
