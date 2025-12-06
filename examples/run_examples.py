#!/usr/bin/env python3
"""
StyledConsole Example Runner

Run examples interactively or in batch mode.

Usage:
    python run_examples.py           # Interactive menu
    python run_examples.py --all     # Run all examples (with pauses)
    python run_examples.py --auto    # Run all examples (no pauses)
"""

import subprocess
import sys
from pathlib import Path

from styledconsole import Console, icons

console = Console()


def get_all_examples() -> dict[str, list[Path]]:
    """Get all example scripts organized by category."""
    examples_dir = Path(__file__).parent

    categories = {
        "Gallery": sorted(examples_dir.glob("gallery/*.py")),
        "Use Cases": sorted(examples_dir.glob("usecases/*.py")),
        "Demos": sorted(examples_dir.glob("demos/*.py")),
        "Validation": sorted(examples_dir.glob("validation/*.py")),
    }

    # Filter out __init__.py and _old files
    for category in categories:
        categories[category] = [
            ex
            for ex in categories[category]
            if ex.name != "__init__.py" and not ex.stem.endswith("_old")
        ]

    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def display_menu(categories: dict[str, list[Path]]) -> tuple[list[Path], int]:
    """Display the example selection menu."""
    console.newline()
    console.frame(
        f"{icons.SPARKLES} Choose an example to run",
        title=f"{icons.ARTIST_PALETTE} StyledConsole Examples",
        border="rounded",
        border_color="cyan",
        width=70,
        align="center",
    )
    console.newline()

    example_list = []
    idx = 1

    for category, examples in categories.items():
        lines = []
        for example in examples:
            example_list.append(example)
            lines.append(f"  [{idx:2}] {example.stem}")
            idx += 1

        console.frame(
            lines,
            title=f"{icons.FILE_FOLDER} {category}",
            border="solid",
            width=70,
            align="left",
        )
        console.newline()

    # Special options
    all_idx = idx
    console.frame(
        [
            f"  [{idx:2}] Run ALL examples",
            "  [ 0] Exit",
        ],
        title=f"{icons.HIGH_VOLTAGE} Options",
        border="solid",
        width=70,
        align="left",
    )
    console.newline()

    return example_list, all_idx


def run_example(example_path: Path, auto_continue: bool = False) -> bool:
    """Run a single example script."""
    console.newline()
    console.rule(f"{icons.ROCKET} Running: {example_path.name}", color="cyan")
    console.newline()

    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            cwd=example_path.parent,
        )

        success = result.returncode == 0

        console.newline()
        if success:
            console.text(f"{icons.CHECK_MARK_BUTTON} Completed: {example_path.name}", color="green")
        else:
            console.text(
                f"{icons.CROSS_MARK} Failed: {example_path.name} (exit code {result.returncode})",
                color="red",
            )

        if not auto_continue:
            input("\nPress Enter to continue...")

        return success

    except KeyboardInterrupt:
        console.newline()
        console.text(f"{icons.WARNING} Interrupted", color="yellow")
        return False


def run_all_examples(example_list: list[Path], auto_continue: bool = False):
    """Run all examples sequentially."""
    total = len(example_list)

    console.newline()
    console.frame(
        f"Running {total} examples...",
        title=f"{icons.FIRE} Run All",
        border="double",
        border_color="yellow",
        width=50,
        align="center",
    )

    success_count = 0
    for i, example in enumerate(example_list, 1):
        console.newline()
        console.text(f"[{i}/{total}] ", color="dim", end="")
        if run_example(example, auto_continue):
            success_count += 1

    # Summary
    console.newline()
    status = "green" if success_count == total else "yellow"
    console.frame(
        f"Passed: {success_count}/{total}",
        title=f"{icons.BAR_CHART} Summary",
        border="double",
        border_color=status,
        width=40,
        align="center",
    )
    console.newline()


def interactive_mode(categories: dict[str, list[Path]]):
    """Run interactive menu loop."""
    while True:
        example_list, all_idx = display_menu(categories)

        try:
            choice = input("Enter your choice: ").strip()

            if not choice or choice == "0":
                console.newline()
                console.frame(
                    "Thanks for exploring StyledConsole!",
                    title=f"{icons.WAVING_HAND} Goodbye",
                    border="rounded",
                    border_color="cyan",
                    width=50,
                    align="center",
                )
                console.newline()
                break

            choice_num = int(choice)

            if choice_num == all_idx:
                run_all_examples(example_list, auto_continue=False)
            elif 1 <= choice_num <= len(example_list):
                run_example(example_list[choice_num - 1], auto_continue=False)
            else:
                console.text(f"{icons.CROSS_MARK} Invalid choice: {choice_num}", color="red")
                input("Press Enter to continue...")

        except ValueError:
            console.text(f"{icons.CROSS_MARK} Invalid input: '{choice}'", color="red")
            input("Press Enter to continue...")
        except KeyboardInterrupt:
            console.newline()
            console.text(f"{icons.WAVING_HAND} Interrupted!", color="yellow")
            break


def main():
    """Main entry point."""
    categories = get_all_examples()

    if not any(categories.values()):
        console.text(f"{icons.WARNING} No examples found!", color="yellow")
        return

    # Check command line args
    if "--all" in sys.argv:
        # Run all with pauses
        example_list = [ex for examples in categories.values() for ex in examples]
        run_all_examples(example_list, auto_continue=False)
    elif "--auto" in sys.argv or "-a" in sys.argv:
        # Run all without pauses
        example_list = [ex for examples in categories.values() for ex in examples]
        run_all_examples(example_list, auto_continue=True)
    else:
        # Interactive menu
        interactive_mode(categories)


if __name__ == "__main__":
    main()
