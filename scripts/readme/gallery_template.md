# StyledConsole Visual Gallery

> Auto-generated visual showcase of StyledConsole capabilities.
> See the main [README](../README.md) for installation and documentation.

______________________________________________________________________

## Hero Animation

![StyledConsole Animation](images/gradient_animation.webp)

______________________________________________________________________

## Feature Showcase

<!-- EXAMPLE_IMAGE:basic_frame --> <!-- EXAMPLE_IMAGE:gradient_frame -->

<!-- EXAMPLE_IMAGE:status_messages --> <!-- EXAMPLE_IMAGE:icons_showcase -->

______________________________________________________________________

## Smart Icon System

Use the `icons` facade for policy-aware symbols with automatic ASCII fallback.

<!-- EXAMPLE:icons_showcase -->

| Environment          | Output | Symbol        |
| -------------------- | ------ | ------------- |
| Modern Terminal      | `🚀`   | Emoji         |
| CI / Legacy Terminal | `>>>`  | Colored ASCII |

______________________________________________________________________

## Full Color Palette

Use named colors, bright variants, hex RGB, and ANSI 256-color codes.

<!-- EXAMPLE_FULL:text_styles -->

______________________________________________________________________

## Multiline Gradient Text

Apply smooth color gradients across multiple lines of text.

<!-- EXAMPLE_FULL:gradient_text -->

______________________________________________________________________

## Rich Text Styling

Apply bold, italic, underline, strikethrough, and dim effects to any text.

<!-- EXAMPLE_FULL:font_styles -->

______________________________________________________________________

## Advanced Frame Engine

Build complex, multi-layered UI architectures with 8 beautiful border styles.

<!-- EXAMPLE_FULL:nested_frames -->

### 8 Beautiful Border Styles

<!-- EXAMPLE_FULL:border_styles -->

______________________________________________________________________

## ASCII Art Banners

Generate massive, high-impact headers using 500+ fonts with gradient support.

<!-- EXAMPLE_FULL:rainbow_banner -->

______________________________________________________________________

## Live Animations & Progress

Create dynamic terminal experiences with themed progress bars.

<!-- markdownlint-disable MD033 -->

<img src="images/progress_animation.webp" alt="Progress Animation"/>
<!-- markdownlint-enable MD033 -->

```python
from styledconsole import StyledProgress
from styledconsole.animation import Animation

# Themed progress bars with automatic color inheritance
with StyledProgress() as progress:
    task = progress.add_task("Assets", total=100)
    progress.update(task, advance=50)

# Frame-based animation engine for cycling gradients
Animation.run(gradient_generator, fps=20, duration=5)
```

______________________________________________________________________

## Declarative Layout Engine

Build complex dashboards using dictionary/JSON structure.

<!-- EXAMPLE_FULL:declarative_layout -->

______________________________________________________________________

## Data-Driven Tables

Feed JSON data directly into our table builder for beautiful tables.

<!-- EXAMPLE_FULL:json_table -->

______________________________________________________________________

## Real-World Examples

### CI/CD Pipeline Dashboard

<!-- EXAMPLE_FULL:build_report -->

### Error Reporting with Style

<!-- EXAMPLE_FULL:error_report -->

______________________________________________________________________

## Quick Start Example

<!-- EXAMPLE_FULL:basic_frame -->

______________________________________________________________________

## More Examples

For a comprehensive gallery of **over 40 working examples**, visit:

**[StyledConsole-Examples](https://github.com/ksokolowski/StyledConsole-Examples)**

```bash
# Run the local quick start demo
uv run examples/quick_start.py
```
