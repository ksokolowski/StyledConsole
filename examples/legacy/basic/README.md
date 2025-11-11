# StyledConsole Examples

This directory contains examples demonstrating the StyledConsole library features, progressing from basic to advanced usage patterns.

## Quick Start

The **Console API** is the recommended entry point for most use cases. It provides a high-level interface for all library features.

```python
from styledconsole import Console

console = Console()
console.frame("Hello, World!", title="Greeting", border="rounded")
console.banner("WELCOME", font="slant", gradient_start="blue", gradient_end="cyan")
console.text("Status: ", color="cyan", bold=True, end="")
console.text("✓ Ready", color="green", bold=True)
```

## Example Progression

### Basic Examples (Console API)

Start here to learn the recommended patterns:

1. **01_simple_frame.py** - Frame rendering basics

   - Simple frames with titles and borders
   - Content alignment and width control
   - Multi-line content handling
   - **API Used**: `Console.frame()`

1. **02_emoji_support.py** - Emoji and Unicode handling

   - Emoji in titles and content
   - Proper width calculation for emojis
   - Styled text output
   - **API Used**: `Console.frame()`, `Console.text()`

1. **03_alignments.py** - Content alignment options

   - Left, center, and right alignment
   - Multi-line alignment
   - Width-based alignment
   - **API Used**: `Console.frame()`

1. **04_border_styles.py** - Border style showcase

   - All 8 built-in border styles
   - Dynamic style selection
   - Case-insensitive style names
   - **API Used**: `Console.frame()`, `Console.rule()`

### Advanced Examples (Direct API)

Use these when you need more control:

5. **05_frame_renderer.py** - Direct FrameRenderer usage

   - **When to use**: Generating frames as `list[str]` for composition
   - **When to use**: Custom rendering pipelines
   - **When to use**: Integration with LayoutComposer
   - **Note**: For standard usage, prefer `Console.frame()`

1. **06_banner_renderer.py** - Banner rendering with Console

   - ASCII art banners with pyfiglet fonts
   - Gradient coloring
   - Border frames around banners
   - **API Used**: `Console.banner()`
   - **Advanced**: Shows BannerRenderer utility methods (font listing, preview)

1. **07_layout_composer.py** - Complex layouts

   - Vertical stacking of multiple elements
   - Side-by-side placement
   - Grid layouts (multi-column, multi-row)
   - **Integration**: Console + LayoutComposer + FrameRenderer
   - **When to use**: Dashboards, complex multi-section displays

1. **08_console_api.py** - Comprehensive Console showcase

   - Complete feature overview
   - Recording and export (HTML/text)
   - Terminal detection
   - Real-world workflow examples

### Showcase Examples

9. **09_showcase.py** - Kitchen sink demonstration
   - All features in one place
   - Real-world application scenarios
   - Best practices showcase

## Architecture Overview

### Recommended Pattern (High-Level)

```python
from styledconsole import Console

console = Console()
# Direct output - simple and clean
console.frame("Content", title="Title")
console.banner("TITLE", font="slant")
console.text("Styled text", color="cyan", bold=True)
```

**Pros:**

- Simple, intuitive API
- Automatic output to terminal
- Built-in styling and formatting
- Recording support for exports
- Terminal detection and adaptation

**Use for:** 99% of use cases

### Advanced Pattern (Low-Level)

```python
from styledconsole import FrameRenderer, BannerRenderer, LayoutComposer

frame_renderer = FrameRenderer()
composer = LayoutComposer()

# Generate frames as list[str]
frame1 = frame_renderer.render("Section 1", title="A")
frame2 = frame_renderer.render("Section 2", title="B")

# Compose layout
layout = composer.stack([frame1, frame2], spacing=2)

# Manual output
for line in layout:
    print(line)
```

**Pros:**

- Fine-grained control over rendering
- Composable elements (frames as data)
- Integration with custom pipelines
- No automatic output (you control when/how)

**Use for:**

- Complex multi-section layouts (LayoutComposer)
- Custom rendering pipelines
- Generating output for non-terminal destinations
- Building your own abstractions on top

## Feature Matrix

| Feature            | Console API              | Direct Renderers             |
| ------------------ | ------------------------ | ---------------------------- |
| Frame rendering    | ✅ `console.frame()`     | ✅ `FrameRenderer.render()`  |
| Banner rendering   | ✅ `console.banner()`    | ✅ `BannerRenderer.render()` |
| Styled text        | ✅ `console.text()`      | ❌ Use Rich directly         |
| Rules/dividers     | ✅ `console.rule()`      | ❌ Use Rich directly         |
| Layout composition | ⚠️ Via `console.print()` | ✅ `LayoutComposer`          |
| Auto output        | ✅ Yes                   | ❌ Manual `print()`          |
| Recording/Export   | ✅ Built-in              | ❌ N/A                       |
| Terminal detection | ✅ Built-in              | ❌ N/A                       |
| Debug logging      | ✅ Built-in              | ❌ N/A                       |

Legend:

- ✅ Fully supported
- ⚠️ Supported with helper
- ❌ Not applicable / use alternative

## When to Use What

### Use Console API when:

- ✅ Building CLI applications
- ✅ Creating user interfaces with styled output
- ✅ Need automatic terminal detection
- ✅ Want recording/export capabilities
- ✅ Prefer simple, high-level interface

### Use Direct Renderers when:

- ✅ Building complex layouts with LayoutComposer
- ✅ Need frames as data (`list[str]`) for further processing
- ✅ Integrating with custom rendering pipelines
- ✅ Building abstractions on top of StyledConsole
- ✅ Need precise control over output timing

### Integration Pattern:

You can mix both approaches:

```python
from styledconsole import Console, FrameRenderer, LayoutComposer

console = Console()
frame_renderer = FrameRenderer()
composer = LayoutComposer()

# Use renderers to create composable elements
header = frame_renderer.render("Dashboard", title="App")
footer = frame_renderer.render("© 2025", title="Info")

# Use composer for layout
layout = composer.stack([header, footer], spacing=2)

# Use Console for output with styling
for line in layout:
    console.print(line)
```

## Running Examples

All examples are standalone and can be run directly:

```bash
# Run individual examples
python examples/basic/01_simple_frame.py
python examples/basic/06_banner_renderer.py
python examples/basic/07_layout_composer.py

# Or with uv
uv run examples/basic/01_simple_frame.py
```

## Learn More

- **Main Documentation**: See project README.md
- **API Reference**: See docstrings in source code
- **Test Suite**: See `tests/` for comprehensive usage examples
- **Type Hints**: All APIs are fully type-annotated

## Contributing Examples

When adding new examples:

1. Follow the naming convention: `##_descriptive_name.py`
1. Start with a clear docstring explaining the example
1. Use Console API for basic examples
1. Use direct renderers only when demonstrating advanced features
1. Include comments explaining each step
1. Show both simple and complex variations
1. Test that examples run without errors

______________________________________________________________________

*StyledConsole - Beautiful console output made simple*
