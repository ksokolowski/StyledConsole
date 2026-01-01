#!/usr/bin/env python3
"""Generate README.md from template with example code and image injection.

Uses template.md as source and replaces placeholders with actual code
and images from examples.py (single source of truth).

Placeholder formats:
  <!-- EXAMPLE:name -->        - Insert code block only
  <!-- EXAMPLE_IMAGE:name -->  - Insert image only
  <!-- EXAMPLE_FULL:name -->   - Insert both image and code

Usage:
  uv run python scripts/readme/generate.py           # Generate README only
  uv run python scripts/readme/generate.py --images  # Regenerate images + README
  python -m scripts.readme --images                  # Same, as module
"""

import re
import sys
from pathlib import Path

# Paths relative to this module
MODULE_DIR = Path(__file__).parent
PROJECT_ROOT = MODULE_DIR.parent.parent
TEMPLATE_PATH = MODULE_DIR / "template.md"
IMAGES_DIR = MODULE_DIR / "images"
OUTPUT_PATH = PROJECT_ROOT / "README.md"

# Image path in README (relative to project root)
README_IMAGE_PATH = "docs/images"


def _import_examples():
    """Import examples module, handling both direct and module execution."""
    try:
        # Try relative import first (when run as module)
        from .examples import EXAMPLES, generate_all_images
    except ImportError:
        # Direct execution - add parent to path
        sys.path.insert(0, str(MODULE_DIR))
        from examples import EXAMPLES, generate_all_images
    return EXAMPLES, generate_all_images


def get_image_path(name: str) -> str:
    """Get the image path for an example (relative to project root)."""
    return f"{README_IMAGE_PATH}/{name}.webp"


def generate_readme(regenerate_images: bool = False) -> None:
    """Generate README.md from template.

    Args:
        regenerate_images: If True, regenerate all images before updating README.
    """
    examples, generate_all_images = _import_examples()

    if regenerate_images:
        generate_all_images()

    if not TEMPLATE_PATH.exists():
        print(f"Template not found: {TEMPLATE_PATH}")
        print("Please create template.md with placeholders.")
        return

    template = TEMPLATE_PATH.read_text()

    # Replace <!-- EXAMPLE:name --> with code block
    def replace_code(match):
        name = match.group(1)
        if name not in examples:
            print(f"  Warning: Unknown example '{name}'")
            return match.group(0)
        code = examples[name]["code"]
        return f"```python\n{code}\n```"

    # Replace <!-- EXAMPLE_IMAGE:name --> with image
    def replace_image(match):
        name = match.group(1)
        if name not in examples:
            print(f"  Warning: Unknown example '{name}'")
            return match.group(0)
        image_path = get_image_path(name)
        alt_text = name.replace("_", " ").title()
        return f'<img src="{image_path}" alt="{alt_text}"/>'

    # Replace <!-- EXAMPLE_FULL:name --> with image + code
    def replace_full(match):
        name = match.group(1)
        if name not in examples:
            print(f"  Warning: Unknown example '{name}'")
            return match.group(0)
        code = examples[name]["code"]
        image_path = get_image_path(name)
        alt_text = name.replace("_", " ").title()
        return f'''<!-- markdownlint-disable MD033 -->
<img src="{image_path}" alt="{alt_text}"/>
<!-- markdownlint-enable MD033 -->

```python
{code}
```'''

    output = template
    output = re.sub(r"<!-- EXAMPLE_FULL:(\w+) -->", replace_full, output)
    output = re.sub(r"<!-- EXAMPLE_IMAGE:(\w+) -->", replace_image, output)
    output = re.sub(r"<!-- EXAMPLE:(\w+) -->", replace_code, output)

    OUTPUT_PATH.write_text(output)
    print(f"Generated: {OUTPUT_PATH}")


def main():
    """CLI entry point."""
    import sys

    regenerate = "--images" in sys.argv or "-i" in sys.argv
    full = "--all" in sys.argv or "-a" in sys.argv

    if full:
        regenerate = True

    generate_readme(regenerate_images=regenerate)


if __name__ == "__main__":
    main()
