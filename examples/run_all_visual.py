#!/usr/bin/env python3
"""Run All Examples Runner

Executes all StyledConsole examples in sequence for visual inspection.
Organized by category: Basic → Showcase → Gallery → Testing

Press Enter between examples to control the pace.
"""

import subprocess
import sys
from pathlib import Path


def print_separator(title: str, char: str = "="):
    """Print a visual separator with title."""
    width = 80
    padding = (width - len(title) - 2) // 2
    print()
    print(char * width)
    print(f"{char * padding} {title} {char * padding}")
    print(char * width)
    print()


def run_example(example_path: Path, auto_continue: bool = False):
    """Run a single example file."""
    print(f"\n📁 Running: {example_path.relative_to(Path.cwd())}")
    print("-" * 80)

    try:
        # Run the example
        result = subprocess.run(
            [sys.executable, str(example_path)],
            capture_output=False,
            text=True,
            check=True,
        )

        print("-" * 80)
        print(f"✅ Completed: {example_path.name}")

        if not auto_continue:
            input("\nPress Enter to continue to next example...")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {example_path.name}")
        print(f"Exit code: {e.returncode}")
        if not auto_continue:
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != "y":
                sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)


def main():
    """Run all examples in organized sequence."""
    examples_dir = Path(__file__).parent

    # Check for auto-continue mode
    auto_continue = "--auto" in sys.argv or "-a" in sys.argv

    print_separator("🎨 STYLEDCONSOLE EXAMPLES SHOWCASE 🎨", "=")
    print("This will run all examples in sequence for visual inspection.")
    print(f"Mode: {'AUTO (no pauses)' if auto_continue else 'INTERACTIVE (press Enter between examples)'}")
    print()

    if not auto_continue:
        input("Press Enter to start...")

    # Category 1: Basic Examples (01-09)
    print_separator("📚 BASIC EXAMPLES", "=")
    basic_dir = examples_dir / "basic"
    basic_examples = sorted(basic_dir.glob("*.py"))

    for example in basic_examples:
        if example.name == "__init__.py":
            continue
        run_example(example, auto_continue)

    # Category 2: Showcase Examples
    print_separator("✨ SHOWCASE EXAMPLES", "=")
    showcase_dir = examples_dir / "showcase"
    showcase_examples = sorted(showcase_dir.glob("*.py"))

    for example in showcase_examples:
        if example.name == "__init__.py":
            continue
        run_example(example, auto_continue)

    # Category 3: Gallery Examples
    print_separator("🎨 GALLERY EXAMPLES", "=")
    gallery_dir = examples_dir / "gallery"
    if gallery_dir.exists():
        gallery_examples = sorted(gallery_dir.glob("*.py"))

        for example in gallery_examples:
            if example.name == "__init__.py":
                continue
            run_example(example, auto_continue)

    # Category 4: Testing Examples
    print_separator("🧪 TESTING EXAMPLES", "=")
    testing_dir = examples_dir / "testing"
    if testing_dir.exists():
        testing_examples = sorted(testing_dir.glob("*.py"))

        for example in testing_examples:
            if example.name == "__init__.py":
                continue
            run_example(example, auto_continue)

    # Final summary
    print_separator("🎉 ALL EXAMPLES COMPLETED", "=")
    print("✅ Successfully ran all examples!")
    print()
    print("Examples demonstrated:")
    print("  📚 Basic: Frame creation, emojis, alignments, borders, renderers, layouts, Console API")
    print("  ✨ Showcase: Banners, CI/CD dashboard, digital poetry, advanced dashboard")
    print("  🎨 Gallery: Border style gallery")
    print("  🧪 Testing: UX validation summaries")
    print()
    print("Phase 2 improvements visible:")
    print("  🔒 AlignType: Type-safe alignment parameters (60+ uses across examples)")
    print("  📦 Public API: Clean __all__ exports in all modules")
    print("  ✨ IDE Support: Autocomplete for align='left'|'center'|'right'")
    print()
    print_separator("", "=")


if __name__ == "__main__":
    main()
