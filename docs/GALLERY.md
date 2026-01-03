# StyledConsole Visual Gallery

> Auto-generated visual showcase of StyledConsole capabilities.
> See the main [README](../README.md) for installation and documentation.

______________________________________________________________________

## Hero Animation

![StyledConsole Animation](images/gradient_animation.webp)

______________________________________________________________________

## Feature Showcase

![Basic Frame](images/basic_frame.webp) ![Gradient Frame](images/gradient_frame.webp)

![Status Messages](images/status_messages.webp) ![Icons Showcase](images/icons_showcase.webp)

______________________________________________________________________

## Smart Icon System

Use the `icons` facade for policy-aware symbols with automatic ASCII fallback.

```python
from styledconsole import icons

print(f"{icons.ROCKET} Deploying...")  # Auto-detects terminal
print(f"{icons.CHECK_MARK_BUTTON} Done!")
```

| Environment          | Output | Symbol        |
| -------------------- | ------ | ------------- |
| Modern Terminal      | `🚀`   | Emoji         |
| CI / Legacy Terminal | `>>>`  | Colored ASCII |

______________________________________________________________________

## Full Color Palette

Use named colors, bright variants, hex RGB, and ANSI 256-color codes.

![Text Styles](images/text_styles.webp)

```python
# Rich color support - named colors and RGB
console.text("Red alert!", color="red")
console.text("Green success", color="green")
console.text("Blue info", color="blue")
console.text("Custom RGB", color="#ff6b6b")
```

______________________________________________________________________

## Multiline Gradient Text

Apply smooth color gradients across multiple lines of text.

![Gradient Text](images/gradient_text.webp)

```python
from styledconsole.effects import gradient_frame

# Apply gradient to multiline text
lines = gradient_frame(
    ["Welcome to StyledConsole!", "Beautiful gradient text", "Across multiple lines"],
    start_color="cyan",
    end_color="magenta",
    target="content",
)
for line in lines:
    print(line)
```

______________________________________________________________________

## Rich Text Styling

Apply bold, italic, underline, strikethrough, and dim effects to any text.

![Font Styles](images/font_styles.webp)

```python
from styledconsole import Console

console = Console()

# Text styling with bold, italic, underline, strikethrough
console.text("Bold text for emphasis", bold=True)
console.text("Italic text for style", italic=True)
console.text("Underlined for importance", underline=True)
console.text("Strikethrough for removed", strike=True)

# Combined styles with colors
console.text("Bold + Red + Underline", bold=True, color="red", underline=True)
console.text("Italic + Cyan + Strike", italic=True, color="cyan", strike=True)
```

______________________________________________________________________

## Advanced Frame Engine

Build complex, multi-layered UI architectures with 8 beautiful border styles.

![Nested Frames](images/nested_frames.webp)

```python
from styledconsole import Console

console = Console()
inner = console.render_frame("Core", border="double", width=20)
console.frame(["Application Shell", inner], border="heavy", width=40)
```

### 8 Beautiful Border Styles

![Border Styles](images/border_styles.webp)

```python
# 8 beautiful border styles available
styles = ["solid", "double", "rounded", "heavy", "dots", "minimal", "thick", "ascii"]
for style in styles:
    console.frame(f"{style}", border=style, width=20)
```

______________________________________________________________________

## ASCII Art Banners

Generate massive, high-impact headers using 500+ fonts with gradient support.

![Rainbow Banner](images/rainbow_banner.webp)

```python
# Full ROYGBIV rainbow spectrum
console.banner("RAINBOW", font="slant", rainbow=True)

# Two-color gradient
console.banner("HELLO", font="big", start_color="cyan", end_color="magenta")
```

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

![Declarative Layout](images/declarative_layout.webp)

```python
from styledconsole.presets.layouts import create_layout_from_config

# Build entire dashboards from a single dictionary
layout = create_layout_from_config({
    "type": "panel",
    "title": "MISSION CONTROL",
    "title_rainbow": True,
    "border": "heavy",
    "border_style": "cyan",
    "content": {
        "type": "group",
        "items": [
            {"type": "text", "content": "Orbital Station Alpha", "align": "center"},
            {"type": "rule", "style": "cyan dim"},
            {"type": "vspacer"},
            # Nested table component...
            {"type": "table", "theme": {...}, "data": {...}}
        ]
    }
})
console.print(layout)
```

______________________________________________________________________

## Data-Driven Tables

Feed JSON data directly into our table builder for beautiful tables.

![Json Table](images/json_table.webp)

```python
from styledconsole.presets.tables import create_table_from_config

# Config-driven table creation (ideal for loading from JSON/YAML)
table = create_table_from_config(
    theme={
        "border_style": "heavy",
        "gradient": {"start": "cyan", "end": "blue"},
        "title": "SERVER STATUS"
    },
    data={
        "columns": [
            {"header": "Region", "style": "bold white"},
            {"header": "Status", "justify": "center"}
        ],
        "rows": [
            ["US-East", {"text": "ONLINE", "color": "green", "icon": "CHECK_MARK_BUTTON"}],
            ["EU-West", {"text": "MAINTENANCE", "color": "yellow", "icon": "GEAR"}]
        ]
    }
)
console.print(table)
```

______________________________________________________________________

## Real-World Examples

### CI/CD Pipeline Dashboard

![Build Report](images/build_report.webp)

```python
from styledconsole import Console, icons

console = Console()
console.banner("BUILD", font="standard", start_color="blue", end_color="purple")

console.frame([
    f"{icons.CHECK_MARK_BUTTON} Lint checks passed",
    f"{icons.CHECK_MARK_BUTTON} Unit tests: 427/427",
    f"{icons.CHECK_MARK_BUTTON} Integration tests: 52/52",
    f"{icons.WARNING} Coverage: 94% (target: 95%)",
    f"{icons.ROCKET} Deploying to staging...",
], title=f"{icons.BAR_CHART} Pipeline Status", border="heavy", border_color="green")
```

### Error Reporting with Style

![Error Report](images/error_report.webp)

```python
console.frame(
    f"{icons.CROSS_MARK} Connection refused\n\n"
    f"   Host: database.example.com:5432\n"
    f"   Error: ETIMEDOUT after 30s\n"
    f"   Retry: 3/3 attempts failed\n\n"
    f"{icons.LIGHT_BULB} Check firewall settings",
    title=f"{icons.WARNING} Database Error",
    border="heavy",
    border_gradient_start="red",
    border_gradient_end="darkred"
)
```

______________________________________________________________________

## Quick Start Example

![Basic Frame](images/basic_frame.webp)

```python
from styledconsole import Console, icons

console = Console()

console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful\n"
    f"{icons.ROCKET} Deployed to production",
    title=f"{icons.SPARKLES} Status",
    border="rounded",
    border_gradient_start="green",
    border_gradient_end="cyan",
)
```

______________________________________________________________________

## More Examples

For a comprehensive gallery of **over 40 working examples**, visit:

**[StyledConsole-Examples](https://github.com/ksokolowski/StyledConsole-Examples)**

```bash
# Run the local quick start demo
uv run examples/quick_start.py
```
