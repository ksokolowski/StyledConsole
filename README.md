# ✨ StyledConsole ✨

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.9.9-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole/releases/tag/v0.9.9)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20the%20project-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/styledconsole)
[![Tests](https://img.shields.io/badge/tests-869%20passing-success.svg)](https://github.com/ksokolowski/StyledConsole)
[![Coverage](https://img.shields.io/badge/coverage-80%25-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole)
[![MyPy](https://img.shields.io/badge/mypy-passing-success.svg)](https://github.com/ksokolowski/StyledConsole)

![StyledConsole Animation](docs/images/gradient_animation.webp)

______________________________________________________________________

## 🚀 Introduction

StyledConsole is a production-ready Python library for creating elegant and expressive terminal output.
It provides ANSI-safe rendering with rich formatting, colors, emojis, gradients and more — making your console output both beautiful and practical.

- 🎨 ANSI-safe styled output
- 🌈 Colors and gradients support
- 😄 Emoji and icon support
- 🧱 Structured tables and layouts
- 📄 Optional HTML and image export
- 🛠️ Designed for developer experience and usability

```bash
pip install styledconsole
```

![Basic Frame](docs/images/basic_frame.webp) ![Gradient Frame](docs/images/gradient_frame.webp)

![Status Messages](docs/images/status_messages.webp) ![Icons Showcase](docs/images/icons_showcase.webp)

______________________________________________________________________

## 🌟 Major Features

### 🎯 Smart Icon System

Use the `icons` facade for policy-aware symbols with automatic ASCII fallback and zero-width alignment fixes. Includes a data layer of 4000+ emojis.

```python
from styledconsole import icons

print(f"{icons.ROCKET} Deploying...")  # Auto-detects terminal
print(f"{icons.CHECK_MARK_BUTTON} Done!")
```

| Environment          | Output | Symbol        |
| -------------------- | ------ | ------------- |
| Modern Terminal      | `🚀`   | Emoji         |
| CI / Legacy Terminal | `>>>`  | Colored ASCII |

### 🎨 Full Color Palette

Use named colors, bright variants, hex RGB, and ANSI 256-color codes for unlimited styling possibilities.

![Text Styles](docs/images/text_styles.webp)

```python
# Rich color support - named colors and RGB
console.text("Red alert!", color="red")
console.text("Green success", color="green")
console.text("Blue info", color="blue")
console.text("Custom RGB", color="#ff6b6b")
```

### 🌈 Multiline Gradient Text

Apply smooth color gradients across multiple lines of text using the powerful `gradient_frame` function.

![Gradient Text](docs/images/gradient_text.webp)

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

### ✨ Rich Text Styling

Apply bold, italic, underline, strikethrough, and dim effects to any text — fully rendered in terminal and image export.

![Font Styles](docs/images/font_styles.webp)

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

### 🏗️ Advanced Frame Engine

Build complex, multi-layered UI architectures with 8 beautiful border styles and automatic width alignment for consistent layouts.

![Nested Frames](docs/images/nested_frames.webp)

```python
from styledconsole import Console

console = Console()
inner = console.render_frame("Core", border="double", width=20)
console.frame(["Application Shell", inner], border="heavy", width=40)
```

#### 📦 8 Beautiful Border Styles

![Border Styles](docs/images/border_styles.webp)

```python
# 8 beautiful border styles available
styles = ["solid", "double", "rounded", "heavy", "dots", "minimal", "thick", "ascii"]
for style in styles:
    console.frame(f"{style}", border=style, width=20)
```

### 🌈 Dynamic Gradient Engine

Apply smooth ROYGBIV rainbows, multi-color linear gradients, or custom interpolation to any frame, banner, or text element.

```python
from styledconsole.effects import rainbow_frame

# Full spectrum vertical or diagonal rainbows
rainbow_frame("Spectral Output", direction="diagonal")
```

### 🔄 Live Terminal Animations & Progress

Create dynamic terminal experiences with a frame-based animation engine and themed progress bars that automatically adapt to your chosen color palette.

<!-- markdownlint-disable MD033 -->

<img src="docs/images/progress_animation.webp" alt="Progress Animation"/>
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

### 🔤 ASCII Art Banners

Generate massive, high-impact headers using 500+ fonts with integrated gradient support and automatic centering.

![Rainbow Banner](docs/images/rainbow_banner.webp)

```python
# Full ROYGBIV rainbow spectrum
console.banner("RAINBOW", font="slant", rainbow=True)

# Two-color gradient
console.banner("HELLO", font="big", start_color="cyan", end_color="magenta")
```

### 🔧 Environment-Aware Rendering

Automatically adapt output for CI/CD, `NO_COLOR`, or legacy terminals using a centralized `RenderPolicy`.

```python
from styledconsole import Console, RenderPolicy

# CI-friendly mode: preserves colors but uses ASCII symbols
console = Console(policy=RenderPolicy.ci_friendly())

# Detects: NO_COLOR, FORCE_COLOR, TERM=dumb, CI, GITHUB_ACTIONS
```

### 🧱 Declarative Layout Engine

Build complex dashboards and UIs using a simple dictionary/JSON structure. Perfect for "Low Code" interfaces or loading configurations from files.

![Declarative Layout](docs/images/declarative_layout.webp)

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

### 📊 Data-Driven Tables

Separate your table data from styling. Feed JSON data directly into our table builder to generate beautiful, gradient-bordered tables instantly.

![Json Table](docs/images/json_table.webp)

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

### 📤 Multi-Format Export

Record your terminal session and export to HTML, plain text, or high-quality images (PNG, WebP, GIF).

```python
console = Console(record=True)
# ... render your UI ...

# Text exports
html = console.export_html()
text = console.export_text()

# Image exports (requires: pip install styledconsole[image])
console.export_webp("output.webp")  # Static or animated
console.export_png("output.png", scale=2.0)  # Retina support
console.export_gif("animation.gif")  # Animated GIF
```

______________________________________________________________________

## 🚀 Quick Start

```bash
pip install styledconsole
```

![Basic Frame](docs/images/basic_frame.webp)

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

## 🎯 Real-World Examples

### CI/CD Pipeline Dashboard

![Build Report](docs/images/build_report.webp)

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

![Error Report](docs/images/error_report.webp)

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

## 📚 Visual Laboratory

For a comprehensive gallery of **over 40 working examples**, visit our dedicated repository:

👉 **[StyledConsole-Examples](https://github.com/ksokolowski/StyledConsole-Examples)**

The examples library includes:

- 🎨 **Visual Showcases**: Gradient effects, layout stress tests, and emoji rendering.
- 🎬 **Feature Demos**: Animations, nested frames, and progress bar policies.
- 💼 **Real-World Components**: CLI menus, interactive dashboards, and log viewers.
- 🔬 **Validation Utilities**: Terminal compatibility checks and color benchmarks.

### Try it now:

```bash
# Run the local quick start demo
uv run examples/quick_start.py
```

______________________________________________________________________

## 🏗️ Built On Giants

- [emoji](https://pypi.org/project/emoji/) — 🎁 4000+ official Unicode emojis
- [Rich](https://github.com/Textualize/rich) — 💪 The powerful rendering engine
- [PyFiglet](https://github.com/pwaller/pyfiglet) — 🔤 500+ ASCII art fonts
- [wcwidth](https://github.com/jquast/wcwidth) — 📏 Correct Unicode width calculation
- [ansi2html](https://github.com/pycontribs/ansi2html) — 💾 Terminal → HTML export

______________________________________________________________________

## 🛠️ Project Status

**v0.9.8.1** — Production Ready ✅

| Metric      | Value       |
| ----------- | ----------- |
| 🧪 Tests    | 943 passing |
| 📊 Coverage | 90%         |
| 🔍 MyPy     | 0 errors    |
| 📚 Examples | 37 working  |
| 🐍 Python   | 3.10 - 3.14 |

**Recent Improvements:**

- ✅ Modern Terminal Detection (Kitty, WezTerm, Ghostty, etc.)
- ✅ Symbol Facade Unification (`icons` as primary API)
- ✅ Icon Provider with colored ASCII fallback (224 icons)
- ✅ Render Policy for environment-aware output
- ✅ Full mypy type checking with 0 errors
- ✅ Windows compatibility fixes

**See [CHANGELOG.md](CHANGELOG.md) for full release history.**

______________________________________________________________________

## 📚 Documentation

- 📖 **[User Guide](docs/USER_GUIDE.md)**: Complete API reference with examples
- 🏗️ **[Developer Guide](docs/DEVELOPER_GUIDE.md)**: Architecture and development guide
- 📅 **[Changelog](CHANGELOG.md)**: Version history and release notes
- 🤝 **[Contributing](CONTRIBUTING.md)**: Development workflow and standards

## 💙 Support StyledConsole

If StyledConsole improves your developer experience, you can support the project here:

☕ https://ko-fi.com/styledconsole

Thank you for helping keep this project alive and evolving!

______________________________________________________________________

## 🤝 Contributing

We welcome contributions! Please see the **[Contributing Guide](CONTRIBUTING.md)** for details on our development workflow (`make qa`, `make test`, etc.).

______________________________________________________________________

## 📄 License

Apache License 2.0

______________________________________________________________________
