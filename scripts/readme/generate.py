#!/usr/bin/env python3
"""Generate README.md and docs/GALLERY.md from templates.

README.md is a focused, PyPI-compatible document (no images).
GALLERY.md is an auto-generated visual showcase with images.

Placeholder formats (used in gallery_template.md):
  <!-- EXAMPLE:name -->        - Insert code block only
  <!-- EXAMPLE_IMAGE:name -->  - Insert image only
  <!-- EXAMPLE_FULL:name -->   - Insert both image and code

Usage:
  uv run python scripts/readme/generate.py           # Generate both files
  uv run python scripts/readme/generate.py --images  # Regenerate images + docs
  python -m scripts.readme --images                  # Same, as module
"""

import re
import shutil
import sys
from pathlib import Path

# Paths relative to this module
MODULE_DIR = Path(__file__).parent
PROJECT_ROOT = MODULE_DIR.parent.parent

# Template paths
README_TEMPLATE = MODULE_DIR / "template.md"
GALLERY_TEMPLATE = MODULE_DIR / "gallery_template.md"

# Output paths
README_OUTPUT = PROJECT_ROOT / "README.md"
GALLERY_OUTPUT = PROJECT_ROOT / "docs" / "GALLERY.md"

# Image path in gallery (relative to docs/)
GALLERY_IMAGE_PATH = "images"


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
    """Get the image path for an example (relative to docs/)."""
    return f"{GALLERY_IMAGE_PATH}/{name}.webp"


def process_template(template_content: str, examples: dict) -> str:
    """Process a template, replacing placeholders with code and images.

    Args:
        template_content: The template markdown content.
        examples: Dictionary of example name -> {code, generator}.

    Returns:
        Processed markdown content.
    """

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
        return f"![{alt_text}]({image_path})"

    # Replace <!-- EXAMPLE_FULL:name --> with image + code
    def replace_full(match):
        name = match.group(1)
        if name not in examples:
            print(f"  Warning: Unknown example '{name}'")
            return match.group(0)
        code = examples[name]["code"]
        image_path = get_image_path(name)
        alt_text = name.replace("_", " ").title()
        return f"""![{alt_text}]({image_path})

```python
{code}
```"""

    output = template_content
    output = re.sub(r"<!-- EXAMPLE_FULL:(\w+) -->", replace_full, output)
    output = re.sub(r"<!-- EXAMPLE_IMAGE:(\w+) -->", replace_image, output)
    output = re.sub(r"<!-- EXAMPLE:(\w+) -->", replace_code, output)

    return output


def generate_readme() -> None:
    """Generate README.md from template (simple copy, no placeholders)."""
    if not README_TEMPLATE.exists():
        print(f"Template not found: {README_TEMPLATE}")
        return

    shutil.copy(README_TEMPLATE, README_OUTPUT)
    print(f"Generated: {README_OUTPUT}")


def generate_gallery(examples: dict) -> None:
    """Generate docs/GALLERY.md from gallery template with placeholder replacement.

    Args:
        examples: Dictionary of example name -> {code, generator}.
    """
    if not GALLERY_TEMPLATE.exists():
        print(f"Template not found: {GALLERY_TEMPLATE}")
        return

    # Ensure docs directory exists
    GALLERY_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    template = GALLERY_TEMPLATE.read_text()
    output = process_template(template, examples)

    GALLERY_OUTPUT.write_text(output)
    print(f"Generated: {GALLERY_OUTPUT}")


def generate_all(regenerate_images: bool = False) -> None:
    """Generate both README.md and docs/GALLERY.md.

    Args:
        regenerate_images: If True, regenerate all images first.
    """
    examples, generate_all_images_fn = _import_examples()

    if regenerate_images:
        print("Regenerating images...")
        generate_all_images_fn()

    print("Generating documentation...")
    generate_readme()
    generate_gallery(examples)


def main():
    """CLI entry point."""
    regenerate = "--images" in sys.argv or "-i" in sys.argv
    full = "--all" in sys.argv or "-a" in sys.argv

    if full:
        regenerate = True

    generate_all(regenerate_images=regenerate)


if __name__ == "__main__":
    main()
