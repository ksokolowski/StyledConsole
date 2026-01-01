# ✨ StyledConsole ✨

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.9.8.1-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole/releases/tag/v0.9.8.1)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20the%20project-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/styledconsole)
[![Tests](https://img.shields.io/badge/tests-943%20passing-success.svg)](https://github.com/ksokolowski/StyledConsole)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole)
[![MyPy](https://img.shields.io/badge/mypy-passing-success.svg)](https://github.com/ksokolowski/StyledConsole)

<!-- markdownlint-disable MD033 -->

<p align="center">
  <img src="docs/images/gradient_animation.webp" alt="StyledConsole Animation"/>
</p>
<!-- markdownlint-enable MD033 -->

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

<!-- markdownlint-disable MD033 -->

<table>
<tr>
<td><!-- EXAMPLE_IMAGE:basic_frame --></td>
<td><!-- EXAMPLE_IMAGE:gradient_frame --></td>
</tr>
<tr>
<td><!-- EXAMPLE_IMAGE:status_messages --></td>
<td><!-- EXAMPLE_IMAGE:icons_showcase --></td>
</tr>
</table>
<!-- markdownlint-enable MD033 -->

______________________________________________________________________

## 🌟 Major Features

### 🎯 Smart Icon System

Use the `icons` facade for policy-aware symbols with automatic ASCII fallback and zero-width alignment fixes. Includes a data layer of 4000+ emojis.

<!-- EXAMPLE:icons_showcase -->

| Environment          | Output | Symbol        |
| -------------------- | ------ | ------------- |
| Modern Terminal      | `🚀`   | Emoji         |
| CI / Legacy Terminal | `>>>`  | Colored ASCII |

### 🎨 Full Color Palette

Use named colors, bright variants, hex RGB, and ANSI 256-color codes for unlimited styling possibilities.

<!-- EXAMPLE_FULL:text_styles -->

### 🌈 Multiline Gradient Text

Apply smooth color gradients across multiple lines of text using the powerful `gradient_frame` function.

<!-- EXAMPLE_FULL:gradient_text -->

### ✨ Rich Text Styling

Apply bold, italic, underline, strikethrough, and dim effects to any text — fully rendered in terminal and image export.

<!-- EXAMPLE_FULL:font_styles -->

### 🏗️ Advanced Frame Engine

Build complex, multi-layered UI architectures with 8 beautiful border styles and automatic width alignment for consistent layouts.

<!-- EXAMPLE_FULL:nested_frames -->

#### 📦 8 Beautiful Border Styles

<!-- EXAMPLE_FULL:border_styles -->

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

<!-- EXAMPLE_FULL:rainbow_banner -->

### 🔧 Environment-Aware Rendering

Automatically adapt output for CI/CD, `NO_COLOR`, or legacy terminals using a centralized `RenderPolicy`.

```python
from styledconsole import Console, RenderPolicy

# CI-friendly mode: preserves colors but uses ASCII symbols
console = Console(policy=RenderPolicy.ci_friendly())

# Detects: NO_COLOR, FORCE_COLOR, TERM=dumb, CI, GITHUB_ACTIONS
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

<!-- EXAMPLE_FULL:basic_frame -->

______________________________________________________________________

## 🎯 Real-World Examples

### CI/CD Pipeline Dashboard

<!-- EXAMPLE_FULL:build_report -->

### Error Reporting with Style

<!-- EXAMPLE_FULL:error_report -->

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
