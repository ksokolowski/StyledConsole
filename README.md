# ✨ StyledConsole ✨

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.9.8b1-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole/releases/tag/v0.9.8b1)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20the%20project-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/styledconsole)
[![Tests](https://img.shields.io/badge/tests-943%20passing-success.svg)](https://github.com/ksokolowski/StyledConsole)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole)
[![MyPy](https://img.shields.io/badge/mypy-passing-success.svg)](https://github.com/ksokolowski/StyledConsole)

______________________________________________________________________

## 🚀 Introduction

StyledConsole is a production-ready Python library for creating elegant and expressive terminal output.
It provides ANSI-safe rendering with rich formatting, colors, emojis, gradients and more — making your console output both beautiful and practical.

- 🎨 ANSI-safe styled output
- 🌈 Colors and gradients support
- 😄 Emoji and icon support
- 🧱 Structured tables and layouts
- 📄 Optional HTML export
- 🛠️ Designed for developer experience and usability

______________________________________________________________________

**🎨 Make your terminal beautiful. ✨ Make your output memorable. 🚀**

```bash
pip install styledconsole
```

> **🎨 Transform your boring terminal into a visual masterpiece!**

```text
┏━━━━━━━━━━━━━━━━━━━━━ ✨ StyledConsole ━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                             ┃
┃ ╭────────────────────── ✨ Features ──────────────────────╮ ┃
┃ │  🌈 Rainbow Gradients    │  🎭 Nested Frames            │ ┃
┃ │  🔤 500+ ASCII Fonts     │  😀 4000+ Emojis             │ ┃
┃ │  🎨 148 CSS4 Colors      │  💾 HTML Export              │ ┃
┃ │  🚀 Icon Provider        │  🔧 Render Policy            │ ┃
┃ ╰─────────────────────────────────────────────────────────╯ ┃
┃                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

______________________________________________________________________

## 🌟 Major Features

### 🎯 Smart Icon System

Use the `icons` facade for policy-aware symbols with automatic ASCII fallback and zero-width alignment fixes. Includes a data layer of 4000+ emojis.

```python
from styledconsole import icons, set_icon_mode

# Primary API - auto-detects terminal capability (🚀 or >>>)
print(f"{icons.ROCKET} Deploying...")
```

| Environment          | Output | Symbol        |
| -------------------- | ------ | ------------- |
| Modern Terminal      | `🚀`   | Emoji         |
| CI / Legacy Terminal | `>>>`  | Colored ASCII |

### 🏗️ Advanced Frame Engine

Build complex, multi-layered UI architectures with 8 beautiful border styles and automatic width alignment for consistent layouts.

```python
from styledconsole import Console

console = Console()
inner = console.render_frame("Core", border="double", width=20)
console.frame(["Application Shell", inner], border="heavy", width=40)
```

```text
┏━━━━━━ Application Shell ━━━━━━┓
┃                               ┃
┃ ╔══════ Core ═══════╗         ┃
┃ ║                   ║         ┃
┃ ╚═══════════════════╝         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

#### 📦 8 Beautiful Border Styles

```text
┌─solid──┐  ╭─rounded─╮  ╔═double══╗  ┏━heavy━━┓
│        │  │         │  ║         ║  ┃        ┃
└────────┘  ╰─────────╯  ╚═════════╝  ┗━━━━━━━━┛

█▀thick▀▀█  +--ascii--+  ─minimal──   ┄┄dashed┄┄
█        █  |         |               ┆        ┆
█▄▄▄▄▄▄▄▄█  +---------+  ──────────   ┄┄┄┄┄┄┄┄┄┄
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

```python
# Slant font with custom gradient transition
console.banner("DEPLOYED", font="slant", start_color="green", end_color="cyan")
```

```text
    ____  __________  __    ______  ____________
   / __ \/ ____/ __ \/ /   / __ \ \/ / ____/ __ \
  / / / / __/ / /_/ / /   / / / /\  / __/ / / / /
 / /_/ / /___/ ____/ /___/ /_/ / / / /___/ /_/ /
/_____/_____/_/   /_____/\____/ /_/_____/_____/
```

### 🔧 Environment-Aware Rendering

Automatically adapt output for CI/CD, `NO_COLOR`, or legacy terminals using a centralized `RenderPolicy`.

```python
from styledconsole import Console, RenderPolicy

# CI-friendly mode: preserves colors but uses ASCII symbols
console = Console(policy=RenderPolicy.ci_friendly())

# Detects: NO_COLOR, FORCE_COLOR, TERM=dumb, CI, GITHUB_ACTIONS
```

### 📤 Multi-Format Export

Record your terminal session and export the results to professional, full-color HTML or clean, ANSI-stripped plain text.

```python
console = Console(record=True)
# ... render your UI ...
html = console.export_html()
text = console.export_text()
```

______________________________________________________________________

## 🚀 Quick Start

```bash
pip install styledconsole
```

```python
from styledconsole import Console, icons

console = Console()

# Your first beautiful frame
console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful\n"
    f"{icons.ROCKET} Deployed to production",
    title=f"{icons.SPARKLES} Status",
    border="rounded",
    border_gradient_start="green",
    border_gradient_end="cyan"
)
```

______________________________________________________________________

## 🎯 Real-World Examples

### CI/CD Pipeline Dashboard

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

## 📚 Gallery & Examples

38 working examples organized in 4 categories:

| Category         | Description                                           |
| ---------------- | ----------------------------------------------------- |
| 🎨 `gallery/`    | Visual showcases - borders, colors, emojis, gradients |
| 🎬 `demos/`      | Feature demos - animations, nested frames, rainbows   |
| 💼 `usecases/`   | Real-world - dashboards, alerts, CI/CD, reports       |
| 🔬 `validation/` | Testing - alignment checks, emoji verification        |

Run them all:

```bash
# Run all examples with auto-advance
uv run python examples/run_examples.py --auto
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

**v0.9.8b1** — Production Ready ✅

| Metric      | Value       |
| ----------- | ----------- |
| 🧪 Tests    | 943 passing |
| 📊 Coverage | 90%         |
| 🔍 MyPy     | 0 errors    |
| 📚 Examples | 38 working  |
| 🐍 Python   | 3.10 - 3.14 |

**Recent Improvements (v0.9.0–v0.9.8):**

- ✅ Modern Terminal Detection (Kitty, WezTerm, Ghostty, etc.)
- ✅ Context Object Pattern (`StyleContext`) & Validation
- ✅ Symbol Facade Unification (`icons` as primary API)
- ✅ DRY emoji architecture (4000+ emojis from `emoji` package)
- ✅ Icon Provider with colored ASCII fallback (224 icons)
- ✅ Render Policy for environment-aware output
- ✅ Full mypy type checking with 0 errors
- ✅ Gradient engine consolidation (Strategy Pattern)
- ✅ Windows compatibility fixes
- ✅ Enhanced pre-commit hooks

**Full release history is available in [CHANGELOG.md](CHANGELOG.md).**

______________________________________________________________________

## 📚 Documentation Architecture

StyledConsole follows a strict **5-Doc Rule** to prevent information rot. All project knowledge is centralized in exactly five master documents:

- 📖 **[User Guide](docs/USER_GUIDE.md)**: Tutorials, basic usage, and visual galleries.
- 🏗️ **[Developer Guide](docs/DEVELOPER_GUIDE.md)**: Architecture details and internal logic.
- 📅 **[Changelog](CHANGELOG.md)**: Full release history (v0.1.0 to present).
- 📈 **[Project Status](docs/PROJECT_STATUS.md)**: Roadmap, tasks, and project metrics.
- 🤝 **[Contributing](CONTRIBUTING.md)**: Dev workflow and PR standards.

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
