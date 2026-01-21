# Getting Started with StyledConsole

> **StyledConsole is to Rich what Tailwind is to CSS** — opinionated, declarative, fast.

This guide takes you from zero to a beautiful terminal dashboard in minutes. Each section builds on the previous, showing you the most common use cases.

______________________________________________________________________

## Installation

```bash
pip install styledconsole
```

______________________________________________________________________

## 1. Your First Frame (30 seconds)

The simplest way to create styled output:

```python
from styledconsole import Console

console = Console()
console.frame("Hello, World!")
```

Output:
```
╭─────────────────╮
│ Hello, World!   │
╰─────────────────╯
```

Add a title and choose a border style:

```python
console.frame(
    "Build completed successfully",
    title="Status",
    border="rounded",  # or "double", "heavy", "minimal"
)
```

______________________________________________________________________

## 2. Adding Emojis and Icons

Use the `icons` facade for terminal-safe symbols with automatic ASCII fallback:

```python
from styledconsole import Console, icons

console = Console()

console.frame(
    [
        f"{icons.CHECK_MARK_BUTTON} Tests passed",
        f"{icons.PACKAGE} Dependencies installed",
        f"{icons.ROCKET} Ready to deploy",
    ],
    title=f"{icons.SPARKLES} Build Status",
)
```

Output:
```
╭────── ✨ Build Status ──────╮
│ ✅ Tests passed             │
│ 📦 Dependencies installed   │
│ 🚀 Ready to deploy          │
╰─────────────────────────────╯
```

**Common icons:** `CHECK_MARK_BUTTON`, `CROSS_MARK`, `WARNING`, `ROCKET`, `GEAR`, `SPARKLES`, `FIRE`, `PACKAGE`, `GLOBE_WITH_MERIDIANS`, `HIGH_VOLTAGE`

______________________________________________________________________

## 3. Colors and Text Styles

### Colored Text

```python
console.text("Success!", color="green")
console.text("Warning: check config", color="yellow")
console.text("Error: connection failed", color="red")
console.text("Custom color", color="#ff6b6b")  # Hex RGB
```

### Text Styles

```python
console.text("Important", bold=True)
console.text("Emphasis", italic=True)
console.text("Notice", underline=True)
console.text("Removed", strike=True)

# Combine styles
console.text("Critical Error", bold=True, color="red", underline=True)
```

### Colored Frames

```python
console.frame(
    "Server is online",
    title="Status",
    border_color="green",
)
```

______________________________________________________________________

## 4. Gradients — Make It Beautiful

Gradients transform ordinary output into eye-catching displays:

```python
from styledconsole import Console, EffectSpec

console = Console()

# Simple two-color gradient
console.frame(
    "Gradient on the border",
    title="Demo",
    effect=EffectSpec.gradient("cyan", "magenta"),
)
```

### Preset Effects (32+ built-in)

```python
# Use named presets for instant styling
console.frame("Fire effect", effect="fire")
console.frame("Ocean vibes", effect="ocean")
console.frame("Matrix style", effect="matrix")
console.frame("Cyberpunk neon", effect="cyberpunk")

# Semantic presets for status
console.frame("Operation successful", effect="success")
console.frame("Proceed with caution", effect="warning")
console.frame("Action failed", effect="error")
```

### Rainbow Gradients

```python
# Full spectrum rainbow
console.frame("Rainbow!", effect=EffectSpec.rainbow())

# Neon rainbow (cyberpunk colors)
console.frame("Neon!", effect=EffectSpec.rainbow(neon=True))
```

### Gradient Directions

```python
# Vertical (default), horizontal, or diagonal
console.frame("Top to bottom", effect=EffectSpec.gradient("red", "blue", direction="vertical"))
console.frame("Left to right", effect=EffectSpec.gradient("red", "blue", direction="horizontal"))
console.frame("Corner to corner", effect=EffectSpec.gradient("red", "blue", direction="diagonal"))
```

______________________________________________________________________

## 5. Background Effects — Visual Impact

Apply gradients to the background for striking visuals:

```python
from styledconsole import Console, EffectSpec

console = Console()

# Background gradient (text stays readable)
console.frame(
    [
        "System Status: ONLINE",
        "All services operational",
    ],
    title="Dashboard",
    effect=EffectSpec.gradient("#1e3a5f", "#2d5a87", layer="background"),
    border="heavy",
)
```

### Alert Boxes with Background Severity

```python
# Success alert
console.frame(
    f"{icons.CHECK_MARK_BUTTON} Deployment completed",
    title="SUCCESS",
    effect=EffectSpec.gradient("#10b981", "#065f46", layer="background"),
)

# Warning alert
console.frame(
    f"{icons.WARNING} High memory usage",
    title="WARNING",
    effect=EffectSpec.gradient("#f59e0b", "#92400e", layer="background"),
)

# Error alert
console.frame(
    f"{icons.CROSS_MARK} Connection failed",
    title="ERROR",
    effect=EffectSpec.gradient("#ef4444", "#991b1b", layer="background"),
)
```

### Multi-Stop Gradients

```python
# Sunset colors flowing across
sunset = EffectSpec.multi_stop(
    ["#ff6b6b", "#feca57", "#ff9ff3", "#54a0ff"],
    layer="background",
    direction="horizontal",
)
console.frame("Sunset gradient", effect=sunset)
```

______________________________________________________________________

## 6. Progress Bars

Show task progress with styled progress bars:

```python
from styledconsole import StyledProgress
import time

with StyledProgress() as progress:
    task = progress.add_task("Downloading...", total=100)

    for i in range(100):
        time.sleep(0.02)
        progress.update(task, advance=1)
```

### Multiple Parallel Tasks

```python
with StyledProgress() as progress:
    download = progress.add_task("Downloading", total=100)
    extract = progress.add_task("Extracting", total=100)
    install = progress.add_task("Installing", total=100)

    # Update tasks as work completes
    progress.update(download, advance=50)
    progress.update(extract, advance=30)
    progress.update(install, advance=10)
```

______________________________________________________________________

## 7. Building a Dashboard

Combine everything into a real-world monitoring dashboard:

```python
from styledconsole import Console, EffectSpec, icons

console = Console()

# Header banner
console.banner("MONITOR", font="small", effect="ocean")
console.newline()

# Status bar
console.frame(
    f"{icons.GLOBE_WITH_MERIDIANS} Region: us-east-1  |  "
    f"{icons.ALARM_CLOCK} Updated: 14:32:15  |  "
    f"{icons.CHECK_MARK_BUTTON} All Systems Operational",
    effect="info",
    border="minimal",
)
console.newline()

# Service status grid
services = [
    {"title": "API", "content": f"{icons.CHECK_MARK_BUTTON} Online", "effect": "success"},
    {"title": "Database", "content": f"{icons.CHECK_MARK_BUTTON} Online", "effect": "success"},
    {"title": "Cache", "content": f"{icons.WARNING} Degraded", "effect": "warning"},
    {"title": "Queue", "content": f"{icons.CHECK_MARK_BUTTON} Online", "effect": "success"},
]

console.frame_group(
    services,
    layout="grid",
    columns=2,
    item_width=30,
)
console.newline()

# Metrics with background gradients
console.text("[bold]Performance Metrics[/]")

metrics = [
    {"title": "CPU", "content": "45%", "colors": ("#22c55e", "#16a34a")},
    {"title": "Memory", "content": "78%", "colors": ("#eab308", "#ca8a04")},
    {"title": "Disk", "content": "32%", "colors": ("#3b82f6", "#2563eb")},
]

for metric in metrics:
    console.frame(
        metric["content"],
        title=metric["title"],
        effect=EffectSpec.gradient(metric["colors"][0], metric["colors"][1], layer="background"),
        border="rounded",
        width=20,
    )
```

______________________________________________________________________

## 8. Quick Reference

### Frame Options

```python
console.frame(
    content,                    # str or list of strings
    title="Title",              # Optional title
    border="rounded",           # solid, double, rounded, heavy, minimal, dots, ascii
    border_color="cyan",        # Named color or hex
    effect="ocean",             # Named preset or EffectSpec
    width=50,                   # Fixed width
    align="center",             # left, center, right
    padding=1,                  # Internal padding
)
```

### EffectSpec Methods

```python
# Two-color gradient
EffectSpec.gradient("start", "end", direction="vertical", target="both", layer="foreground")

# Rainbow spectrum
EffectSpec.rainbow(neon=False, direction="vertical", layer="foreground")

# Multi-stop gradient
EffectSpec.multi_stop(["color1", "color2", "color3"], direction="horizontal", layer="background")

# From curated palette (90 available)
EffectSpec.from_palette("ocean_depths", layer="foreground")
```

### Named Effects

| Category | Effects |
|----------|---------|
| **Gradients** | `fire`, `ocean`, `sunset`, `forest`, `aurora`, `gold`, `mint`, `peach` |
| **Rainbows** | `rainbow`, `rainbow_pastel`, `rainbow_neon`, `rainbow_muted` |
| **Themed** | `matrix`, `cyberpunk`, `vaporwave`, `dracula`, `nord_aurora` |
| **Semantic** | `success`, `warning`, `error`, `info`, `neutral` |

### Common Icons

| Icon | Name | Usage |
|------|------|-------|
| ✅ | `CHECK_MARK_BUTTON` | Success, completed |
| ❌ | `CROSS_MARK` | Error, failed |
| ⚠️ | `WARNING` | Warnings, caution |
| 🚀 | `ROCKET` | Deploy, launch |
| ⚙️ | `GEAR` | Settings, config |
| 📦 | `PACKAGE` | Dependencies, packages |
| ✨ | `SPARKLES` | Features, highlights |
| 🔥 | `FIRE` | Hot, trending |
| 🌐 | `GLOBE_WITH_MERIDIANS` | Network, global |
| ⚡ | `HIGH_VOLTAGE` | Performance, speed |

______________________________________________________________________

## Next Steps

- **[PYTHON_API.md](PYTHON_API.md)** — Full API reference
- **[GALLERY.md](GALLERY.md)** — Visual examples gallery
- **[DECLARATIVE.md](DECLARATIVE.md)** — JSON/YAML configuration
- **[JINJA_TEMPLATES.md](JINJA_TEMPLATES.md)** — Dynamic templates

______________________________________________________________________

## Complete Example: CI/CD Dashboard

```python
#!/usr/bin/env python3
"""CI/CD Pipeline Dashboard — Complete Example."""

from styledconsole import Console, EffectSpec, icons

console = Console()

# Pipeline header
console.banner("BUILD #1847", font="small", effect="ocean")
console.newline()

# Build info
console.frame(
    [
        f"{icons.BOOKMARK} Branch: main",
        f"{icons.BUSTS_IN_SILHOUETTE} Author: alice",
        f"{icons.MEMO} Commit: fix(auth): resolve token refresh",
    ],
    title="Build Info",
    effect=EffectSpec.gradient("#6366f1", "#8b5cf6", layer="background"),
    border="rounded",
)
console.newline()

# Pipeline stages
stages = [
    {"title": "Checkout", "content": f"{icons.CHECK_MARK_BUTTON} 2s", "effect": "success"},
    {"title": "Install", "content": f"{icons.CHECK_MARK_BUTTON} 45s", "effect": "success"},
    {"title": "Lint", "content": f"{icons.CHECK_MARK_BUTTON} 12s", "effect": "success"},
    {"title": "Test", "content": f"{icons.GEAR} Running...", "effect": "info"},
    {"title": "Build", "content": f"{icons.HOURGLASS_NOT_DONE} Pending", "effect": "neutral"},
    {"title": "Deploy", "content": f"{icons.HOURGLASS_NOT_DONE} Pending", "effect": "neutral"},
]

console.frame_group(stages, layout="horizontal", gap=1)
console.newline()

# Test results
console.frame(
    [
        f"{icons.CHECK_MARK_BUTTON} Unit Tests:        427/427 passed",
        f"{icons.CHECK_MARK_BUTTON} Integration Tests:  52/52 passed",
        f"{icons.WARNING} Coverage:          94.2% (target: 95%)",
    ],
    title=f"{icons.BAR_CHART} Test Results",
    effect="success",
    border="heavy",
)
```

This creates a complete, professional CI/CD dashboard with emojis, colors, gradients, and grid layouts — all in under 50 lines of code.
