#!/usr/bin/env python3
"""
StyledConsole Examples Launcher
================================

This script launches the examples runner from the StyledConsole-Examples repository.

The comprehensive examples have been moved to a separate repository for better
organization and maintenance. This launcher provides a convenient way to run
examples from the main StyledConsole repository.

Usage:
    # From StyledConsole repository
    python examples/run_examples.py

    # Or use make command
    make examples

Repository Structure:
    StyledConsole/         - Main library
    StyledConsole-Examples/  - Examples repository (separate)

For more information, visit:
https://github.com/ksokolowski/StyledConsole-Examples
"""

import subprocess
import sys
from pathlib import Path


def find_examples_repo() -> Path:
    """Try to locate the StyledConsole-Examples repository.

    Returns:
        Path to the examples repository

    Raises:
        FileNotFoundError: If examples repository is not found
    """
    # Try common locations
    current_dir = Path(__file__).parent.parent.resolve()

    possible_locations = [
        # Same parent directory (sibling repositories)
        current_dir.parent / "StyledConsole-Examples",
        # In parent's parent (for nested structures)
        current_dir.parent.parent / "StyledConsole-Examples",
        # Relative to home
        Path.home() / "StyledConsole-Examples",
        Path.home() / "Projects" / "StyledConsole-Examples",
        Path.home() / "Code" / "StyledConsole-Examples",
        # Development environments
        Path("/home/falcon/New/StyledConsole-Examples"),
    ]

    for location in possible_locations:
        if location.exists() and (location / "run_examples.py").exists():
            return location

    raise FileNotFoundError(
        "StyledConsole-Examples repository not found.\n\n"
        "Please clone the examples repository:\n"
        "  git clone https://github.com/ksokolowski/StyledConsole-Examples\n\n"
        "Tried locations:\n" + "\n".join(f"  - {loc}" for loc in possible_locations)
    )


def main():
    """Launch the examples runner."""
    try:
        # Find examples repository
        examples_repo = find_examples_repo()
        runner_script = examples_repo / "run_examples.py"

        print(f"✅ Found examples repository: {examples_repo}")
        print("🚀 Launching examples runner...\n")

        # Forward all arguments to the examples runner
        result = subprocess.run(
            [sys.executable, str(runner_script), *sys.argv[1:]],
            cwd=examples_repo,
        )

        sys.exit(result.returncode)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        print(
            "\n💡 Tip: Clone the examples repository next to StyledConsole:",
            file=sys.stderr,
        )
        print("  cd ..", file=sys.stderr)
        print("  git clone https://github.com/ksokolowski/StyledConsole-Examples", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
