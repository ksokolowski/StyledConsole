#!/usr/bin/env python3
"""
Run All Examples

Interactive menu to run any StyledConsole example or run them all sequentially.
"""

import subprocess
from pathlib import Path

from styledconsole import ROUNDED, SOLID


def get_all_examples():
    """Get all example scripts organized by category."""
    examples_dir = Path(__file__).parent

    categories = {
        "Basic Examples": sorted(examples_dir.glob("basic/*.py")),
        "Showcase Examples": sorted(examples_dir.glob("showcase/*.py")),
        "Gallery Examples": sorted(examples_dir.glob("gallery/*.py")),
    }

    # Filter out old/deprecated examples
    for category in categories:
        categories[category] = [ex for ex in categories[category] if not ex.stem.endswith("_old")]

    return categories


def display_menu(categories):
    """Display the example selection menu."""
    width = 70

    print()
    print(ROUNDED.render_top_border(width, "🎨 StyledConsole Examples"))
    print(ROUNDED.render_line(width, "", align="center"))
    print(ROUNDED.render_line(width, "Choose an example to run:", align="center"))
    print(ROUNDED.render_line(width, "", align="center"))
    print(ROUNDED.render_bottom_border(width))
    print()

    example_list = []
    idx = 1

    for category, examples in categories.items():
        print(SOLID.render_top_border(width, f"📁 {category}"))

        for example in examples:
            name = example.stem
            example_list.append(example)
            print(SOLID.render_line(width, f"  [{idx:2}] {name}", align="left"))
            idx += 1

        print(SOLID.render_bottom_border(width))
        print()

    # Special options
    print(SOLID.render_top_border(width, "⚡ Special Options"))
    print(SOLID.render_line(width, f"  [{idx:2}] Run ALL examples", align="left"))
    all_idx = idx
    idx += 1
    print(SOLID.render_line(width, "  [ 0] Exit", align="left"))
    print(SOLID.render_bottom_border(width))
    print()

    return example_list, all_idx


def run_example(example_path):
    """Run a single example script."""
    width = 70

    print()
    print("=" * 80)
    print(ROUNDED.render_top_border(width, f"🚀 Running: {example_path.name}"))
    print(ROUNDED.render_bottom_border(width))
    print("=" * 80)
    print()

    # Run the example
    result = subprocess.run(
        ["uv", "run", str(example_path)],
        cwd=example_path.parent.parent,
    )

    print()
    print("=" * 80)
    print(ROUNDED.render_top_border(width, "✅ Example Complete"))
    print(ROUNDED.render_bottom_border(width))
    print("=" * 80)
    print()

    return result.returncode == 0


def run_all_examples(example_list):
    """Run all examples sequentially."""
    width = 70

    print()
    print(SOLID.render_top_border(width, "🎪 Running All Examples"))
    print(SOLID.render_line(width, f"Total: {len(example_list)} examples", align="center"))
    print(SOLID.render_bottom_border(width))
    print()

    success_count = 0
    for i, example in enumerate(example_list, 1):
        print(f"\n[{i}/{len(example_list)}] ", end="")
        if run_example(example):
            success_count += 1

        if i < len(example_list):
            input("\nPress Enter to continue to next example...")

    # Summary
    print()
    print(SOLID.render_top_border(width, "📊 Summary"))
    print(
        SOLID.render_line(width, f"Completed: {success_count}/{len(example_list)}", align="center")
    )
    print(SOLID.render_bottom_border(width))
    print()


def main():
    """Main interactive loop."""
    categories = get_all_examples()

    while True:
        example_list, all_idx = display_menu(categories)

        try:
            choice = input("Enter your choice: ").strip()

            if not choice or choice == "0":
                print()
                print(ROUNDED.render_top_border(50, "👋 Goodbye!"))
                print(
                    ROUNDED.render_line(50, "Thanks for exploring StyledConsole!", align="center")
                )
                print(ROUNDED.render_bottom_border(50))
                print()
                break

            choice_num = int(choice)

            if choice_num == all_idx:
                run_all_examples(example_list)
            elif 1 <= choice_num <= len(example_list):
                run_example(example_list[choice_num - 1])
                input("\nPress Enter to return to menu...")
            else:
                print(f"\n❌ Invalid choice: {choice_num}")
                input("Press Enter to continue...")

        except ValueError:
            print(f"\n❌ Invalid input: '{choice}'")
            input("Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted!")
            break


if __name__ == "__main__":
    main()
