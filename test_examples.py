#!/usr/bin/env python3
"""
Test all examples to validate library functionality and UX.
"""

import subprocess
import sys
from pathlib import Path


def run_example(example_path: Path) -> tuple[bool, str]:
    """Run a single example and return success status and output."""
    try:
        result = subprocess.run(
            [sys.executable, str(example_path)],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=example_path.parent,
        )

        # Consider it successful if it runs without error
        success = result.returncode == 0
        output = result.stdout if success else result.stderr

        return success, output
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT: Example took too long to run"
    except Exception as e:
        return False, f"ERROR: {str(e)}"


def main():
    """Run all examples and report results."""
    examples_dir = Path(__file__).parent / "examples"

    # Collect all example scripts
    example_files = []
    for category in ["basic", "showcase", "gallery"]:
        category_path = examples_dir / category
        if category_path.exists():
            example_files.extend(sorted(category_path.glob("*.py")))

    print("=" * 80)
    print("🧪 TESTING STYLEDCONSOLE EXAMPLES")
    print("=" * 80)
    print()

    results = []

    for example in example_files:
        category = example.parent.name
        name = example.stem

        print(f"Running {category}/{name}...", end=" ", flush=True)

        success, output = run_example(example)
        results.append((category, name, success, output))

        if success:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
            print(f"  Error: {output[:200]}")

    print()
    print("=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, _, success, _ in results if success)
    total = len(results)

    print(f"\nTotal Examples: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("\n🎉 ALL EXAMPLES PASSED!")
        return 0
    else:
        print("\n⚠️  SOME EXAMPLES FAILED")
        print("\nFailed examples:")
        for category, name, success, output in results:
            if not success:
                print(f"  • {category}/{name}")
                print(f"    {output[:100]}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
