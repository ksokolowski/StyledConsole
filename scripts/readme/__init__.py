"""README generation module.

This module provides a unified system for generating README.md with
example images from a single source of truth.

Usage:
    python -m scripts.readme          # Generate README.md only
    python -m scripts.readme --images # Regenerate images + README.md
    python -m scripts.readme --all    # Regenerate everything

Structure:
    scripts/readme/
    ├── __init__.py      # This file
    ├── __main__.py      # CLI entry point
    ├── generate.py      # Main generation logic
    ├── examples.py      # Example definitions (single source of truth)
    ├── template.md      # README template with placeholders
    └── images/          # Generated images (output)
"""
