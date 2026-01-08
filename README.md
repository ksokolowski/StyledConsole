# ✨ StyledConsole

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.9.9.5-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole/releases)
[![Tests](https://img.shields.io/badge/tests-968%20passing-success.svg)](https://github.com/ksokolowski/StyledConsole)
[![Coverage](https://img.shields.io/badge/coverage-79%25-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/ksokolowski?style=flat&logo=githubsponsors&logoColor=pink)](https://github.com/sponsors/ksokolowski)
[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support-ff5e5b?logo=ko-fi&logoColor=white)](https://ko-fi.com/styledconsole)

**A modern Python library for elegant terminal output** — rich formatting, colors, emojis, gradients, and export capabilities built on top of [Rich](https://github.com/Textualize/rich).

> 🚧 **Early Access** — Currently available on TestPyPI. Some features may be experimental. API not yet final!

```bash
pip install -i https://test.pypi.org/simple/ styledconsole
```

______________________________________________________________________

## 🎨 Visual Gallery

**See the [Visual Gallery](docs/GALLERY.md) for screenshots and animated demos.**

______________________________________________________________________

## 🚀 Why StyledConsole?

Rich is powerful, but StyledConsole adds the finishing touches:

|     | Feature                   | What It Does                                                      |
| --- | ------------------------- | ----------------------------------------------------------------- |
| 🌈  | **Gradient Engine**       | Smooth rainbows and linear gradients on borders, text, banners    |
| 🎯  | **Smart Icons**           | 224 icons with automatic ASCII fallback for CI/legacy terminals   |
| 📊  | **StyledTables**          | Beautiful tables with gradient borders and config-driven creation |
| 🔧  | **Environment Detection** | Auto-adapts for `NO_COLOR`, `CI`, `TERM=dumb`                     |
| 🏗️  | **Frame Engine**          | 8 border styles, nested frames, width alignment                   |
| 📤  | **HTML & Image Export**   | Export to HTML, PNG, WebP, GIF with full emoji support            |
| 📋  | **Declarative Layouts**   | Build entire UIs from JSON/dict config                            |

______________________________________________________________________

## ✨ Key Features

### 🎯 Smart Icon System

Policy-aware symbols with automatic ASCII fallback — works everywhere:

```python
from styledconsole import icons

print(f"{icons.ROCKET} Deploying...")      # 🚀 in modern terminals
print(f"{icons.CHECK_MARK_BUTTON} Done!")  # ✅ or >>> in CI
```

| Environment     | Output | Rendering     |
| --------------- | ------ | ------------- |
| Modern Terminal | 🚀     | Full emoji    |
| CI / Legacy     | `>>>`  | Colored ASCII |

### 🌈 Gradient Frames & Borders

Smooth color transitions on any frame border:

```python
from styledconsole import Console, EFFECTS, EffectSpec

console = Console()

# Use preset effects (32 available)
console.frame("Build successful!", title="Status", effect="fire")
console.frame("Deployed!", title="Status", effect=EFFECTS.ocean)

# Or create custom gradients
console.frame(
    "Custom gradient!",
    title="Status",
    border="rounded",
    effect=EffectSpec.gradient("green", "cyan"),
)
```

### 🔤 ASCII Art Banners

500+ fonts with integrated gradient and rainbow support:

```python
console.banner("HELLO", font="slant", effect="rainbow")
console.banner("WORLD", font="big", effect=EffectSpec.gradient("cyan", "magenta"))
console.banner("FIRE", font="banner", effect=EFFECTS.fire)
```

### 📊 StyledTables

Beautiful tables with gradient borders, created from code or config:

```python
from styledconsole.presets.tables import create_table_from_config

table = create_table_from_config(
    theme={"border_style": "heavy", "gradient": {"start": "cyan", "end": "blue"}},
    data={
        "columns": [{"header": "Service"}, {"header": "Status"}],
        "rows": [["API", "✅ Online"], ["Database", "✅ Online"]]
    }
)
console.print(table)
```

### 🔧 Environment-Aware Rendering

Automatically adapts for CI/CD pipelines and restricted terminals:

```python
from styledconsole import Console, RenderPolicy

# CI-friendly: colors preserved, ASCII symbols
console = Console(policy=RenderPolicy.ci_friendly())

# Auto-detects: NO_COLOR, FORCE_COLOR, TERM=dumb, CI, GITHUB_ACTIONS
```

### 📤 HTML & Image Export

Record terminal sessions and export to HTML or images:

```python
console = Console(record=True)
# ... render your UI ...

# HTML export (built-in)
console.export_html("output.html")

# Image export (pip install styledconsole[image])
console.export_png("output.png")
console.export_webp("output.webp")
console.export_gif("animation.gif")  # animated!
```

### 📋 Declarative Layouts

Build complex dashboards from JSON/dict — perfect for config-driven UIs:

```python
from styledconsole.presets.layouts import create_layout_from_config

layout = create_layout_from_config({
    "type": "panel",
    "title": "DASHBOARD",
    "border": "heavy",
    "content": {"type": "text", "content": "Status: Online"}
})
console.print(layout)
```

______________________________________________________________________

## 🏁 Quick Start

```bash
pip install -i https://test.pypi.org/simple/ styledconsole
```

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

**Output:**

```
╭──────── ✨ Status ─────────╮
│ ✅ Build successful        │
│ 🚀 Deployed to production  │
╰────────────────────────────╯
```

👉 **Want more examples?** Check out [StyledConsole-Examples](https://github.com/ksokolowski/StyledConsole-Examples) for 40+ real-world demos including CLI dashboards, progress bars, error reporters, and animated effects.

______________________________________________________________________

## 🏗️ Built On Giants

StyledConsole extends these excellent libraries:

| Library                                              | Contribution                 |
| ---------------------------------------------------- | ---------------------------- |
| [Rich](https://github.com/Textualize/rich)           | 💪 Core rendering engine     |
| [emoji](https://pypi.org/project/emoji/)             | 😀 4000+ Unicode emojis      |
| [PyFiglet](https://github.com/pwaller/pyfiglet)      | 🔤 500+ ASCII art fonts      |
| [wcwidth](https://github.com/jquast/wcwidth)         | 📏 Unicode width calculation |
| [ansi2html](https://github.com/pycontribs/ansi2html) | 💾 Terminal → HTML export    |

______________________________________________________________________

## 📊 Project Status

**v0.9.9.5** — 🏗️ Early Access (TestPyPI)

| Metric      | Value       |
| ----------- | ----------- |
| 🧪 Tests    | 968 passing |
| 📊 Coverage | 79%         |
| 🔍 MyPy     | 0 errors    |
| 🐍 Python   | 3.10 – 3.14 |

______________________________________________________________________

## 📚 Documentation

| Resource                                      | Description              |
| --------------------------------------------- | ------------------------ |
| 📖 [User Guide](docs/USER_GUIDE.md)           | Complete API reference   |
| 🏗️ [Developer Guide](docs/DEVELOPER_GUIDE.md) | Architecture & internals |
| 🎨 [Visual Gallery](docs/GALLERY.md)          | Screenshots & demos      |
| 📅 [Changelog](CHANGELOG.md)                  | Version history          |
| 🤝 [Contributing](CONTRIBUTING.md)            | Development workflow     |

______________________________________________________________________

## 💙 Support

If StyledConsole improves your developer experience:

| Platform           | Link                                                                       |
| ------------------ | -------------------------------------------------------------------------- |
| 💖 GitHub Sponsors | [github.com/sponsors/ksokolowski](https://github.com/sponsors/ksokolowski) |
| ☕ Ko-fi           | [ko-fi.com/styledconsole](https://ko-fi.com/styledconsole)                 |

______________________________________________________________________

## 📄 License

Apache License 2.0 — See [LICENSE](LICENSE) for details.
