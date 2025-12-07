#!/usr/bin/env python3
"""
Test actual cursor position after printing ZWJ emoji in Kitty.

This uses ANSI escape sequences to query cursor position.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))


def measure_visual_width_terminal(s: str) -> int | None:
    """Measure actual visual width by checking cursor position."""
    import termios
    import tty

    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        # Set terminal to raw mode
        tty.setraw(fd)

        # Move to column 1, print string, query cursor position
        sys.stdout.write("\r")  # Go to column 1
        sys.stdout.write(s)  # Print the string
        sys.stdout.write("\x1b[6n")  # Query cursor position (DSR)
        sys.stdout.flush()

        # Read response: ESC [ row ; col R
        response = ""
        while True:
            ch = sys.stdin.read(1)
            response += ch
            if ch == "R":
                break

        # Parse response
        # Format: \x1b[row;colR
        if response.startswith("\x1b["):
            parts = response[2:-1].split(";")
            if len(parts) == 2:
                col = int(parts[1])
                return col - 1  # Column is 1-indexed, width is col-1

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        sys.stdout.write("\n")

    return None


def main():
    print("=" * 50)
    print("TERMINAL CURSOR POSITION TEST")
    print("=" * 50)
    print()
    print("This measures actual cursor position after printing.")
    print("Press Enter after each measurement...\n")

    from styledconsole.utils.text import visual_width

    test_cases = [
        "XXXXXXXXXX",  # 10 X
        "🚀 Rocket!",  # Should be 10
        "⚠️ Warning",  # Should be 10 (modern) or 9 (standard)
        "👨‍💻 Hello!!",  # Should be 10
        "👨‍💻 Developer",  # Should be 12
    ]

    print("Visual width comparison:")
    print("-" * 50)
    print(f"{'String':<25} {'Calculated':<12} {'Actual':<10}")
    print("-" * 50)

    for s in test_cases:
        calc = visual_width(s)
        actual = measure_visual_width_terminal(s)
        match = "✓" if calc == actual else "✗"
        display = s if len(s) < 20 else s[:17] + "..."
        print(f"{display:<25} {calc:<12} {actual or '?':<10} {match}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
