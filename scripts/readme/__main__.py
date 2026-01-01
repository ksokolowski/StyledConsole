#!/usr/bin/env python3
"""CLI entry point for README generation.

Usage:
    python -m scripts.readme              # Generate README.md only
    python -m scripts.readme --images     # Regenerate images + README.md
    python -m scripts.readme --all        # Same as --images
    python -m scripts.readme --help       # Show help

    # Direct execution also works:
    uv run python scripts/readme/generate.py --images
    uv run python scripts/readme/examples.py  # Images only
"""

import sys
from pathlib import Path


def show_help():
    """Show usage help."""
    print(__doc__)
    print("Options:")
    print("  --images, -i   Regenerate all images before generating README")
    print("  --all, -a      Same as --images")
    print("  --help, -h     Show this help message")


def main():
    """Main entry point."""
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        return

    # Handle both module and direct execution
    try:
        from .generate import main as generate_main
    except ImportError:
        # Direct execution
        sys.path.insert(0, str(Path(__file__).parent))
        from generate import main as generate_main

    generate_main()


if __name__ == "__main__":
    main()
