#!/usr/bin/env python3
"""Test script to explore animation and progress behavior on limited terminals.

Run with different environment settings to see the effects:

    # Normal terminal
    uv run python examples/validation/test_limited_terminal.py

    # Simulate dumb terminal
    TERM=dumb uv run python examples/validation/test_limited_terminal.py

    # Simulate NO_COLOR
    NO_COLOR=1 uv run python examples/validation/test_limited_terminal.py

    # Simulate pipe (no TTY)
    uv run python examples/validation/test_limited_terminal.py | cat

    # Simulate CI environment
    CI=true uv run python examples/validation/test_limited_terminal.py
"""

import os
import sys
import time

from styledconsole import Console, RenderPolicy
from styledconsole.animation import Animation


def print_environment_info():
    """Print current environment detection info."""
    print("=" * 60)
    print("ENVIRONMENT DETECTION")
    print("=" * 60)
    print(f"  TERM={os.environ.get('TERM', '(not set)')}")
    print(f"  NO_COLOR={os.environ.get('NO_COLOR', '(not set)')}")
    print(f"  FORCE_COLOR={os.environ.get('FORCE_COLOR', '(not set)')}")
    print(f"  CI={os.environ.get('CI', '(not set)')}")
    print(f"  GITHUB_ACTIONS={os.environ.get('GITHUB_ACTIONS', '(not set)')}")
    print(f"  stdout.isatty()={sys.stdout.isatty()}")
    print()

    # Show detected policy
    policy = RenderPolicy.from_env()
    print("DETECTED POLICY (RenderPolicy.from_env()):")
    print(f"  unicode: {policy.unicode}")
    print(f"  color: {policy.color}")
    print(f"  emoji: {policy.emoji}")
    print(f"  force_ascii_icons: {policy.force_ascii_icons}")
    print(f"  border_style_fallback: {policy.border_style_fallback}")
    print(f"  icon_mode: {policy.icon_mode}")
    print("=" * 60)
    print()


def test_simple_animation():
    """Test basic animation with cursor control."""
    print("TEST 1: Simple Animation (cursor control)")
    print("-" * 40)
    print("Watch for garbage escape codes if terminal is limited...")
    print()

    frames = [
        "Loading .  ",
        "Loading .. ",
        "Loading ...",
        "Loading  ..",
        "Loading   .",
    ]

    def frame_generator():
        for _ in range(3):  # 3 cycles
            for frame in frames:
                yield frame + "\n"

    Animation.run(frame_generator(), fps=5, duration=3)
    print("Animation complete.\n")


def test_spinner_animation():
    """Test spinner-style animation."""
    print("TEST 2: Spinner Animation")
    print("-" * 40)

    spinners = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def spinner_generator():
        for _ in range(20):
            for s in spinners:
                yield f"{s} Processing...\n"

    Animation.run(spinner_generator(), fps=10, duration=2)
    print("Spinner complete.\n")


def test_progress_bar():
    """Test progress bar rendering."""
    print("TEST 3: Progress Bar (Rich-based)")
    print("-" * 40)

    console = Console()
    print(f"Console policy: {console.policy}")
    print()

    with console.progress() as progress:
        task = progress.add_task("Downloading...", total=100)
        for _ in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)

    print("Progress complete.\n")


def test_progress_with_explicit_policy():
    """Test progress with explicit minimal policy."""
    print("TEST 4: Progress Bar with Minimal Policy")
    print("-" * 40)

    console = Console(policy=RenderPolicy.minimal())
    print(f"Console policy: {console.policy}")
    print()

    with console.progress() as progress:
        task = progress.add_task("Processing...", total=50)
        for _ in range(50):
            time.sleep(0.03)
            progress.update(task, advance=1)

    print("Progress complete.\n")


def test_multiline_animation():
    """Test multi-line animation using Console.render_frame()."""
    print("TEST 5: Animated Frame Content")
    print("-" * 40)
    print("This animates content inside a properly rendered frame.")
    print("On limited terminals, you'll see each frame printed separately.")
    print()

    console = Console()

    def animated_frames():
        for i in range(10):
            filled = "█" * (i + 1)
            empty = "░" * (9 - i)
            content = [
                f"Step {i + 1:2}/10",
                f"[{filled}{empty}]",
            ]
            # Use the library's render_frame for proper alignment
            frame = console.render_frame(
                content,
                title="Progress",
                border="rounded",
                width=20,
            )
            yield frame + "\n"

    Animation.run(animated_frames(), fps=2, duration=6)
    print("Animated frame complete.\n")


def test_frame_rendering():
    """Test frame rendering (should work on all terminals)."""
    print("TEST 6: Frame Rendering (should always work)")
    print("-" * 40)

    # With auto-detected policy
    console = Console()
    console.frame(
        "This is a test frame with auto-detected policy.",
        title="Auto Policy",
        border="rounded",
    )

    # With minimal policy
    console_minimal = Console(policy=RenderPolicy.minimal())
    console_minimal.frame(
        "This frame uses minimal (ASCII) policy.",
        title="Minimal Policy",
        border="ascii",
    )
    print()


def test_simple_text_progress():
    """Test what a simple non-animated progress would look like."""
    print("TEST 7: Simple Text Progress (no cursor control needed)")
    print("-" * 40)
    print("This is how progress COULD work on limited terminals:")
    print()

    total = 20
    for i in range(total + 1):
        filled = "█" * i
        empty = "░" * (total - i)
        percent = (i / total) * 100
        # Just print each line - no cursor control
        print(f"\r[{filled}{empty}] {percent:5.1f}%", end="", flush=True)
        time.sleep(0.1)
    print()  # Final newline
    print()
    print("For limited terminals, we could print each update on a new line:")
    for i in range(0, total + 1, 5):
        percent = (i / total) * 100
        print(f"  Progress: {percent:.0f}% ({i}/{total})")
        time.sleep(0.2)
    print("Text progress complete.\n")


def main():
    """Run all tests."""
    print_environment_info()

    print("\n>>> TEST 1 (Simple Animation)")
    test_simple_animation()

    print("\n>>> TEST 2 (Spinner Animation)")
    test_spinner_animation()

    print("\n>>> TEST 3 (Progress Bar)")
    test_progress_bar()

    print("\n>>> TEST 4 (Progress with Minimal Policy)")
    test_progress_with_explicit_policy()

    print("\n>>> TEST 5 (Multi-line Animation)")
    test_multiline_animation()

    print("\n>>> TEST 6 (Frame Rendering)")
    test_frame_rendering()

    print("\n>>> TEST 7 (Simple Text Progress)")
    test_simple_text_progress()

    print("=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)
    print()
    print("Observations:")
    print("- If you saw garbage characters like '[?25l' or '[3A',")
    print("  your terminal doesn't support ANSI cursor control.")
    print("- Progress bars may have displayed incorrectly if")
    print("  the terminal lacks proper cursor/refresh support.")
    print("- Frames should always render correctly (static output).")


if __name__ == "__main__":
    main()
