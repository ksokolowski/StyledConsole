# ✨ StyledConsole ✨

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.9.0-brightgreen.svg)](https://github.com/yourusername/styledconsole/releases/tag/v0.9.0)
[![Tests](https://img.shields.io/badge/tests-700%2B%20passing-success.svg)](https://github.com/yourusername/styledconsole)
[![Coverage](https://img.shields.io/badge/coverage-95%25%2B-brightgreen.svg)](https://github.com/yourusername/styledconsole)

> **🎨 Transform your boring terminal into a visual masterpiece!**

```text
┏━━━━━━━━━━━━━━━━━━━━━ ✨ StyledConsole ━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                             ┃
┃ ╭────────────────────── ✨ Features ──────────────────────╮ ┃
┃ │  🌈 Rainbow Gradients    │  🎭 Nested Frames            │ ┃
┃ │  🔤 500+ ASCII Fonts     │  😀 4000+ Emojis            │ ┃
┃ │  🎨 148 CSS4 Colors      │  💾 HTML Export              │ ┃
┃ ╰─────────────────────────────────────────────────────────╯ ┃
┃                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

______________________________________________________________________

## 🌟 What Can You Create?

### 🏛️ Nested Multi-Frame Architectures

Build complex, layered UI components with independent gradient borders:

```python
from styledconsole import Console

console = Console()

# Create nested frames with different gradient colors!
inner = console.render_frame("🔮 Core", border="double", width=20,
                              border_gradient_start="purple", border_gradient_end="magenta")
middle = console.render_frame(["Growth Layer", inner], border="rounded", width=35,
                               border_gradient_start="green", border_gradient_end="lime")
outer = console.render_frame(["🔥 Fire Layer", middle], border="heavy", width=50,
                              border_gradient_start="red", border_gradient_end="orange")
console.print(outer)
```

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🔥 Fire Layer                                  ┃
┃ ╭─────────────────────────────────╮            ┃
┃ │ Growth Layer                    │            ┃
┃ │ ╔══════════════════╗            │            ┃
┃ │ ║ 🔮 Core          ║            │            ┃
┃ │ ╚══════════════════╝            │            ┃
┃ ╰─────────────────────────────────╯            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### 🌈 Rainbow Gradient Effects

Make your frames come alive with full-spectrum ROYGBIV rainbows:

```python
from styledconsole.effects import rainbow_frame

rainbow_frame([
    "🔴 Red - Passion and energy",
    "🟠 Orange - Creativity and warmth",
    "🟡 Yellow - Joy and optimism",
    "🟢 Green - Growth and harmony",
    "🔵 Blue - Trust and depth",
    "🟣 Purple - Wisdom and magic",
], title="🌈 Rainbow Poetry", direction="vertical")
```

### 🎬 Animated Gradients

Yes, you can animate your terminal output!

```python
from styledconsole.animation import Animation
from styledconsole.effects.strategies import RainbowSpectrum, DiagonalPosition

# Create cycling rainbow animations that flow across your frames!
Animation.run(gradient_frames, fps=20, duration=10)
```

### 😀 100+ Built-in Emojis with Perfect Alignment

No more broken layouts from emoji width issues:

```python
from styledconsole import Console, EMOJI

console = Console()

console.frame([
    f"{EMOJI.ROCKET} Deploy to production",
    f"{EMOJI.CHECK} All tests passing",
    f"{EMOJI.FIRE} Performance optimized",
    f"{EMOJI.SPARKLES} Ready to ship!",
], title=f"{EMOJI.PACKAGE} Release v2.0", border="rounded")
```

Available emoji categories:

- **Status:** ✅ ❌ ⚠️ ℹ️ ❓ 🔄
- **Symbols:** ⭐ ✨ 💫 🌟 💎 🔮
- **Objects:** 📦 📁 📊 📈 🔧 ⚙️
- **Nature:** 🔥 💧 🌊 🌈 ⚡ ❄️
- **And 80+ more!**

### 🔤 Massive ASCII Art Banners

500+ fonts to make your headers impossible to miss:

```python
console.banner("DEPLOYED", font="slant", start_color="green", end_color="cyan")
```

```text
    ____  __________  __    ______  ____________
   / __ \/ ____/ __ \/ /   / __ \ \/ / ____/ __ \
  / / / / __/ / /_/ / /   / / / /\  / __/ / / / /
 / /_/ / /___/ ____/ /___/ /_/ / / / /___/ /_/ /
/_____/_____/_/   /_____/\____/ /_/_____/_____/
```

### 🎨 148 CSS4 Colors + Gradients

Use color names, hex codes, or RGB - your choice:

```python
# All these work!
console.frame("Fire!", border_color="orangered")
console.frame("Ocean!", border_color="#1E90FF")
console.frame("Custom!", border_color=(255, 128, 0))

# Gradient borders - smooth color transitions
console.frame("Sunset", border_gradient_start="gold", border_gradient_end="crimson")
console.frame("Ocean", border_gradient_start="cyan", border_gradient_end="navy")
console.frame("Forest", border_gradient_start="lime", border_gradient_end="darkgreen")
```

### 📦 8 Beautiful Border Styles

```python
borders = ["solid", "rounded", "double", "heavy", "thick", "ascii", "minimal", "dashed"]
```

```text
┌─solid──┐  ╭─rounded─╮  ╔═double══╗  ┏━heavy━━┓
│        │  │         │  ║         ║  ┃        ┃
└────────┘  ╰─────────╯  ╚═════════╝  ┗━━━━━━━━┛

█▀thick▀▀█  +--ascii--+  ─minimal──   ┄┄dashed┄┄
█        █  |         |               ┆        ┆
█▄▄▄▄▄▄▄▄█  +---------+  ──────────   ┄┄┄┄┄┄┄┄┄┄
```

______________________________________________________________________

## 🚀 Quick Start

```bash
pip install styledconsole
```

```python
from styledconsole import Console, EMOJI

console = Console()

# Your first beautiful frame
console.frame(
    f"{EMOJI.CHECK} Build successful\n"
    f"{EMOJI.ROCKET} Deployed to production",
    title=f"{EMOJI.SPARKLES} Status",
    border="rounded",
    border_gradient_start="green",
    border_gradient_end="cyan"
)
```

______________________________________________________________________

## 🎯 Real-World Examples

### CI/CD Pipeline Dashboard

```python
console.banner("BUILD", font="standard", start_color="blue", end_color="purple")

console.frame([
    f"{EMOJI.CHECK} Lint checks passed",
    f"{EMOJI.CHECK} Unit tests: 427/427",
    f"{EMOJI.CHECK} Integration tests: 52/52",
    f"{EMOJI.WARNING} Coverage: 94% (target: 95%)",
    f"{EMOJI.ROCKET} Deploying to staging...",
], title=f"{EMOJI.CHART_BAR} Pipeline Status", border="heavy", border_color="green")
```

### Error Reporting with Style

```python
console.frame(
    f"{EMOJI.CROSS} Connection refused\n\n"
    f"   Host: database.example.com:5432\n"
    f"   Error: ETIMEDOUT after 30s\n"
    f"   Retry: 3/3 attempts failed\n\n"
    f"{EMOJI.LIGHTBULB} Check firewall settings",
    title=f"{EMOJI.WARNING} Database Error",
    border="heavy",
    border_gradient_start="red",
    border_gradient_end="darkred"
)
```

### Test Summary Preset

```python
from styledconsole.presets import test_summary

test_summary(
    total=150,
    passed=145,
    failed=3,
    skipped=2,
    duration=12.5
)
```

### Export to HTML

```python
console = Console(record=True)  # Enable recording

console.banner("REPORT", font="slant")
console.frame("Generated metrics...", title="📊 Analytics")

# Export everything as HTML!
html = console.export_html()  # Full HTML with colors
text = console.export_text()  # Plain text version
```

______________________________________________________________________

## 📚 Gallery & Examples

27 working examples organized in 4 categories:

| Category         | Description                                           |
| ---------------- | ----------------------------------------------------- |
| 🎨 `gallery/`    | Visual showcases - borders, colors, emojis, gradients |
| 🎬 `demos/`      | Feature demos - animations, nested frames, rainbows   |
| 💼 `usecases/`   | Real-world - dashboards, alerts, CI/CD, reports       |
| 🔬 `validation/` | Testing - alignment checks, emoji verification        |

Run them all:

```bash
uv run python examples/run_examples.py --all
```

______________________________________________________________________

## 🏗️ Built On Giants

| Library                                              | What it brings                              |
| ---------------------------------------------------- | ------------------------------------------- |
| [Rich](https://github.com/Textualize/rich)           | 💪 The powerful rendering engine underneath |
| [PyFiglet](https://github.com/pwaller/pyfiglet)      | 🔤 500+ ASCII art fonts                     |
| [wcwidth](https://github.com/jquast/wcwidth)         | 📏 Correct Unicode width calculation        |
| [ansi2html](https://github.com/pycontribs/ansi2html) | 💾 Terminal → HTML export                   |

**Why StyledConsole instead of using Rich directly?**

- ✅ **3 lines vs 15** — Simple API for common patterns
- ✅ **Emoji handling** — Automatic width correction for terminal quirks
- ✅ **Gradient borders** — Out of the box, no configuration
- ✅ **Nested frames** — Just works™
- ✅ **Animation support** — Built-in animation engine

______________________________________________________________________

## 🛠️ Project Status

**v0.5.0** — Production Ready ✅

|             |              |
| ----------- | ------------ |
| 🧪 Tests    | 700+ passing |
| 📊 Coverage | 95%+         |
| 📚 Examples | 27 working   |
| 🐍 Python   | 3.10 - 3.13  |

______________________________________________________________________

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our development workflow (`make qa`, `make test`, etc.).

______________________________________________________________________

## 📄 License

Apache License 2.0

______________________________________________________________________

<p align="center">
  <b>🎨 Make your terminal beautiful. ✨ Make your output memorable. 🚀</b>
  <br><br>
  <code>pip install styledconsole</code>
</p>
