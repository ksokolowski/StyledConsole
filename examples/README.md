# StyledConsole Examples

This directory contains examples demonstrating the capabilities of StyledConsole.

## Structure

- **`basic/`** - Simple, focused examples for learning individual features
- **`showcase/`** - Complex, creative examples demonstrating multiple features together
- **`gallery/`** - Visual gallery of all border styles and color gradients

## Running Examples

All examples can be run directly with UV:

```bash
# Run a specific example
uv run examples/basic/01_simple_frame.py

# Run all basic examples
for f in examples/basic/*.py; do echo "=== $f ===" && uv run "$f"; done

# Run showcase examples
uv run examples/showcase/digital_poetry.py
```

## Basic Examples

1. **`01_simple_frame.py`** - Basic frame rendering with different border styles
2. **`02_emoji_support.py`** - Emoji-safe rendering demonstrations
3. **`03_alignments.py`** - Text alignment options (left, center, right)
4. **`04_border_styles.py`** - All 8 predefined border styles
5. **`05_color_parsing.py`** - Color parsing and CSS4 named colors
6. **`06_terminal_detection.py`** - Terminal capability detection

## Showcase Examples

- **`digital_poetry.py`** - Creative multi-line poem about StyledConsole
- **`feature_matrix.py`** - Feature comparison table with emojis
- **`gradient_demo.py`** - Color gradient demonstrations
- **`emoji_gallery.py`** - Emoji alignment showcase

## Gallery

- **`border_gallery.py`** - Visual catalog of all border styles
- **`color_gallery.py`** - CSS4 color palette showcase

## Contributing Examples

When adding new examples:
- Keep basic examples focused on one feature
- Make showcase examples creative and visually appealing
- Include comments explaining key concepts
- Test with different terminal emulators
- Verify emoji rendering works correctly
