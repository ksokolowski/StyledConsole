# ✨ StyledConsole ✨

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.9.5-brightgreen.svg)](https://github.com/yourusername/styledconsole/releases/tag/v0.9.5)
[![Tests](https://img.shields.io/badge/tests-898%20passing-success.svg)](https://github.com/yourusername/styledconsole)
[![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen.svg)](https://github.com/yourusername/styledconsole)
[![MyPy](https://img.shields.io/badge/mypy-passing-success.svg)](https://github.com/yourusername/styledconsole)

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

## 🌟 What Can You Create?

### 🎁 Built On Industry-Standard Emoji Package

**New in v0.9.1:** Direct integration with the [`emoji` PyPI package](https://pypi.org/project/emoji/) for 4000+ officially-supported emojis:

- **Single source of truth:** All emoji names follow CLDR canonical standard (e.g., `CHECK_MARK_BUTTON`, not `CHECK`)
- **4000+ emojis:** Complete Unicode emoji database with search capabilities
- **Type-safe access:** CLDR names via attribute access (not magic strings)
- **Curated categories:** Pre-organized emoji sets for common use cases
- **Zero maintenance:** Automatically stays in sync with official emoji releases

```python
from styledconsole import EMOJI, CuratedEmojis

# Direct access to 4000+ emojis
print(EMOJI.ROCKET)           # 🚀
print(EMOJI.CHECK_MARK_BUTTON)  # ✅
print(EMOJI.CROSS_MARK)        # ❌

# Search by keyword
results = EMOJI.search("party")  # [('PARTY_POPPER', '🎉'), ...]

# Curated quick-pick sets
CuratedEmojis.DEV     # Pre-selected dev icons
CuratedEmojis.STATUS  # Status indicators
CuratedEmojis.NATURE  # Nature emojis
```

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

### 😀 4000+ Emojis with Perfect Alignment

No more broken layouts from emoji width issues! Direct integration with the `emoji` package:

```python
from styledconsole import Console, EMOJI

console = Console()

console.frame([
    f"{EMOJI.ROCKET} Deploy to production",
    f"{EMOJI.CHECK_MARK_BUTTON} All tests passing",
    f"{EMOJI.FIRE} Performance optimized",
    f"{EMOJI.SPARKLES} Ready to ship!",
], title=f"{EMOJI.PACKAGE} Release v2.0", border="rounded")
```

**New in v0.9.1:** DRY architecture using `emoji` package as single source of truth:

```python
from styledconsole import EMOJI, CuratedEmojis

# 4000+ emojis with CLDR canonical names
print(EMOJI.CHECK_MARK_BUTTON)  # ✅
print(EMOJI.CROSS_MARK)         # ❌

# Search for emojis
results = EMOJI.search("rocket")  # [('ROCKET', '🚀'), ...]

# Curated categories for quick discovery
CuratedEmojis.STATUS  # ['CHECK_MARK_BUTTON', 'CROSS_MARK', 'WARNING', ...]
CuratedEmojis.DEV     # ['ROCKET', 'FIRE', 'STAR', 'SPARKLES', ...]
CuratedEmojis.NATURE  # ['FIRE', 'WATER_WAVE', 'RAINBOW', ...]
```

Available curated categories:

- **STATUS:** ✅ ❌ ⚠️ ℹ️ ❓ 🔄
- **DEV:** 🚀 🔥 ⭐ ✨ 💻 🔧
- **NATURE:** 🌊 🌈 ⚡ 🌸 🌳
- **UI:** 📦 📁 📊 📈 🔔 ⚙️
- **And 10+ more curated sets!**

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

### 🚀 Icon Provider (Colored ASCII Fallback)

**New in v0.9.0:** Automatic emoji→ASCII conversion with ANSI colors for CI/CD compatibility:

```python
from styledconsole import icons, set_icon_mode

# Auto-detects terminal capability (default)
print(f"{icons.CHECK_MARK_BUTTON} Tests passed")  # ✅ or (OK) in green
print(f"{icons.CROSS_MARK} Build failed")         # ❌ or (FAIL) in red
print(f"{icons.WARNING} Deprecation")             # ⚠️ or (WARN) in yellow

# Force specific mode globally
set_icon_mode("ascii")   # Force ASCII everywhere
set_icon_mode("emoji")   # Force emoji everywhere
set_icon_mode("auto")    # Auto-detect (default)
```

**224 icons in 16 categories:** Status, Stars, Documents, Books, Tech, Tools, Activity, Transport, Weather, Plants, Food, People, Arrows, Symbols, Hearts, and more!

### 🔧 Render Policy (Environment-Aware Rendering)

**New in v0.9.0:** Automatically adapts output based on terminal capabilities:

```python
from styledconsole import Console, RenderPolicy

# Auto-detect from environment (NO_COLOR, CI, TERM=dumb)
console = Console()  # Uses RenderPolicy.from_env() by default

# CI-friendly: colors but no emoji
console = Console(policy=RenderPolicy.ci_friendly())

# ASCII-only for logs/pipes
console = Console(policy=RenderPolicy(unicode=False, color=False, emoji=False))
```

**Detects:** `NO_COLOR`, `FORCE_COLOR`, `TERM=dumb`, `CI`, `GITHUB_ACTIONS`, `GITLAB_CI`

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
    f"{EMOJI.CHECK_MARK_BUTTON} Build successful\n"
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
    f"{EMOJI.CHECK_MARK_BUTTON} Lint checks passed",
    f"{EMOJI.CHECK_MARK_BUTTON} Unit tests: 427/427",
    f"{EMOJI.CHECK_MARK_BUTTON} Integration tests: 52/52",
    f"{EMOJI.WARNING} Coverage: 94% (target: 95%)",
    f"{EMOJI.ROCKET} Deploying to staging...",
], title=f"{EMOJI.BAR_CHART} Pipeline Status", border="heavy", border_color="green")
```

### Error Reporting with Style

```python
console.frame(
    f"{EMOJI.CROSS_MARK} Connection refused\n\n"
    f"   Host: database.example.com:5432\n"
    f"   Error: ETIMEDOUT after 30s\n"
    f"   Retry: 3/3 attempts failed\n\n"
    f"{EMOJI.LIGHT_BULB} Check firewall settings",
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

# Run specific category
uv run python examples/run_examples.py --category gallery
```

______________________________________________________________________

## 🏗️ Built On Giants

| Library                                              | What it brings                              |
| ---------------------------------------------------- | ------------------------------------------- |
| [emoji](https://pypi.org/project/emoji/)             | 🎁 4000+ official Unicode emojis (CLDR)     |
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

**v0.9.1** — Production Ready ✅

|             |             |
| ----------- | ----------- |
| 🧪 Tests    | 898 passing |
| 📊 Coverage | 89%         |
| 🔍 MyPy     | 0 errors    |
| 📚 Examples | 38 working  |
| 🐍 Python   | 3.10 - 3.13 |

**Recent Improvements (v0.9.0 - v0.9.1):**

- ✅ Full mypy type checking with 0 errors
- ✅ DRY emoji architecture (4000+ emojis from `emoji` package)
- ✅ Icon Provider with colored ASCII fallback (224 icons)
- ✅ Render Policy for environment-aware output
- ✅ Advanced progress theming
- ✅ Gradient engine consolidation (Strategy Pattern)
- ✅ Windows compatibility fixes
- ✅ Enhanced pre-commit hooks

______________________________________________________________________

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on our development workflow (`make qa`, `make test`, etc.).

______________________________________________________________________

## 📄 License

Apache License 2.0

______________________________________________________________________

**🎨 Make your terminal beautiful. ✨ Make your output memorable. 🚀**

```bash
pip install styledconsole
```
