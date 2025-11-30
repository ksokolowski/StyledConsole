# StyledConsole User Guide

**Version:** 0.5.0
**Last Updated:** November 30, 2025

______________________________________________________________________

## Table of Contents

1. [Quick Start](#quick-start)
1. [Frames & Borders](#frames--borders)
1. [Banners](#banners)
1. [Colors & Gradients](#colors--gradients)
1. [Emojis](#emojis)
1. [Presets](#presets)
1. [HTML Export](#html-export)
1. [Tips & Best Practices](#tips--best-practices)
1. [API Conventions](#api-conventions)
1. [Migration Guide](#migration-guide)
1. [Troubleshooting](#troubleshooting)

______________________________________________________________________

## Quick Start

### Installation

```bash
pip install styledconsole
```

### Your First Frame

```python
from styledconsole import Console, EMOJI

console = Console()

console.frame(
    f"{EMOJI.CHECK} Build successful\n{EMOJI.ROCKET} Deployed to production",
    title=f"{EMOJI.SPARKLES} Status",
    border="rounded",
    border_color="cyan"
)
```

Output:

```text
╭─────────────── ✨ Status ───────────────╮
│ ✅ Build successful                     │
│ 🚀 Deployed to production               │
╰─────────────────────────────────────────╯
```

______________________________________________________________________

## Frames & Borders

### Basic Frame

```python
console.frame("Hello, World!", title="Greeting")
```

### 8 Border Styles

| Style     | Characters | Use Case                |
| --------- | ---------- | ----------------------- |
| `solid`   | ┌─┐│└┘     | Default, professional   |
| `rounded` | ╭─╮│╰╯     | Friendly, modern        |
| `double`  | ╔═╗║╚╝     | Emphasis, headers       |
| `heavy`   | ┏━┓┃┗┛     | Bold emphasis           |
| `thick`   | █▀▄        | Block style             |
| `ascii`   | +--\|+     | Universal compatibility |
| `minimal` | ─│         | Clean, subtle           |
| `dashed`  | ┄┆         | Drafts, previews        |

### Frame Parameters

```python
console.frame(
    content="Your content here",
    title="Title",
    border="rounded",           # Border style
    width=60,                   # Frame width
    padding=1,                  # Internal padding
    align="center",             # Content alignment: left|center|right
    content_color="white",      # Content text color
    border_color="blue",        # Border color
    title_color="cyan",         # Title color
)
```

### Gradient Borders

```python
console.frame(
    "Gradient magic!",
    title="Rainbow",
    border_gradient_start="red",
    border_gradient_end="blue"
)
```

### Width Best Practices

```python
# ✅ Use list of strings with explicit width
console.frame([
    "Line 1 content",
    "Line 2 with longer content",
], title="Example", width=50)

# ❌ Avoid multi-line strings (may truncate)
console.frame('''
Line 1 content
Line 2 with longer content
''', title="Example")
```

**Recommended widths:**

- Short messages: `width=40`
- Medium content: `width=60`
- Wide dashboards: `width=80`

______________________________________________________________________

## Banners

### Basic Banner

```python
console.banner("SUCCESS", font="slant")
```

### Gradient Banner

```python
console.banner(
    "LAUNCH",
    font="banner",
    start_color="red",
    end_color="blue"
)
```

### Available Fonts

Common pyfiglet fonts: `standard`, `slant`, `banner`, `big`, `small`, `mini`

______________________________________________________________________

## Colors & Gradients

### Color Formats

```python
# CSS4 color names (148 supported)
console.frame("Text", border_color="dodgerblue")

# Hex codes
console.frame("Text", border_color="#1E90FF")

# RGB tuples
console.frame("Text", border_color=(30, 144, 255))
```

### Common Status Colors

| Purpose | Recommended Colors            |
| ------- | ----------------------------- |
| Success | `lime`, `green`, `limegreen`  |
| Error   | `red`, `crimson`, `indianred` |
| Warning | `yellow`, `gold`, `orange`    |
| Info    | `blue`, `dodgerblue`, `cyan`  |
| Neutral | `gray`, `silver`, `white`     |

### Static Gradients

```python
from styledconsole import gradient_frame, diagonal_gradient_frame, rainbow_frame

# Vertical gradient (top → bottom)
gradient_frame(
    ["Line 1", "Line 2", "Line 3"],
    start_color="red",
    end_color="blue",
    target="both",  # 'content', 'border', or 'both'
    border="rounded"
)

# Diagonal gradient (top-left → bottom-right)
diagonal_gradient_frame(
    ["Diagonal", "Gradient", "Effect"],
    start_color="cyan",
    end_color="magenta",
    target="both",
    border="double"
)

# Rainbow effect (7-color spectrum)
rainbow_frame(
    ["🌈 Rainbow", "✨ Magic"],
    mode="both",
    border="heavy"
)
```

### Animated Gradients

```python
from styledconsole.animation import Animation
from styledconsole.effects.engine import apply_gradient
from styledconsole.effects.strategies import (
    DiagonalPosition, RainbowSpectrum, OffsetPositionStrategy, Both
)

def frame_generator():
    offset = 0.0
    while True:
        pos_strategy = OffsetPositionStrategy(DiagonalPosition(), offset=offset)
        colored_lines = apply_gradient(base_lines, pos_strategy, RainbowSpectrum(), Both(), border_chars)
        yield "\n".join(colored_lines)
        offset += 0.05

Animation.run(frame_generator(), fps=20, duration=10)
```

______________________________________________________________________

## Emojis

### Quick Reference

| Emoji Type    | Support   | Example        |
| ------------- | --------- | -------------- |
| Standard      | ✅ Full   | ✅ ❌ 🚀 💡 🎉 |
| VS16          | ✅ Full   | ⚠️ ℹ️ ⚙️ ⏱️    |
| Skin tones    | ⚠️ Varies | 👍🏽 👋🏻          |
| ZWJ sequences | ❌ None   | 👨‍💻 👨‍👩‍👧          |

### Using EMOJI Constants

```python
from styledconsole import EMOJI, E  # E is short alias

# Status indicators
EMOJI.CHECK         # ✅
EMOJI.CROSS         # ❌
EMOJI.WARNING       # ⚠️
EMOJI.INFO          # ℹ️

# Common icons
EMOJI.ROCKET        # 🚀
EMOJI.FIRE          # 🔥
EMOJI.STAR          # ⭐
EMOJI.SPARKLES      # ✨

# Technology
EMOJI.LAPTOP        # 💻
EMOJI.GEAR          # ⚙️
EMOJI.CHART_BAR     # 📊
EMOJI.PACKAGE       # 📦

# Helper methods
EMOJI.success("Done")   # "✅ Done"
EMOJI.error("Failed")   # "❌ Failed"
EMOJI.warning("Care")   # "⚠️ Care"
```

### Unsupported: ZWJ Sequences

ZWJ (Zero Width Joiner) sequences break alignment:

| Don't Use         | Use Instead  | Constant        |
| ----------------- | ------------ | --------------- |
| 👨‍👩‍👧 (Family)       | 👥 (People)  | `EMOJI.PEOPLE`  |
| 👩‍💻 (Technologist) | 💻 (Laptop)  | `EMOJI.LAPTOP`  |
| 🏳️‍🌈 (Rainbow Flag) | 🌈 (Rainbow) | `EMOJI.RAINBOW` |

______________________________________________________________________

## Presets

Presets are pre-built, high-level components for common CLI patterns.

### Available Presets

| Preset       | Function         | Description                         |
| ------------ | ---------------- | ----------------------------------- |
| Status Frame | `status_frame()` | Single operation result (pass/fail) |
| Test Summary | `test_summary()` | Test execution summary              |
| Dashboard    | `dashboard()`    | Grid-based monitoring layout        |

### Status Frame

Display the result of a single operation:

```python
from styledconsole.presets import status_frame

# Simple success
status_frame("Database Connection", "PASS", duration=0.05)

# Failure with error message
status_frame(
    "API Integration",
    "FAIL",
    duration=1.2,
    message="ConnectionRefusedError: Connection refused"
)
```

**Parameters:**

- `name` (str): Task or operation name
- `status` (str): Status code ("PASS", "FAIL", "SKIP", "ERROR", "WARN")
- `duration` (float, optional): Duration in seconds
- `message` (str, optional): Additional details or error message
- `console` (Console, optional): Console instance to use

### Test Summary

Generate a summary report for test results:

```python
from styledconsole.presets import test_summary

results = [
    {"name": "test_auth", "status": "PASS", "duration": 0.12},
    {"name": "test_db", "status": "PASS", "duration": 0.45},
    {"name": "test_api", "status": "FAIL", "duration": 1.05, "message": "500 Error"},
]

test_summary(results, total_duration=1.62)
```

**Parameters:**

- `results` (list): List of result dicts with `name`, `status`, `duration`, optional `message`
- `total_duration` (float, optional): Total execution time
- `console` (Console, optional): Console instance to use

### Dashboard

Create multi-panel monitoring layouts:

```python
from styledconsole.presets import dashboard
from styledconsole import EMOJI

widgets = [
    {"title": f"{EMOJI.CHART_BAR} CPU Load", "content": "45% Usage\n8 Cores Active"},
    {"title": f"{EMOJI.PACKAGE} Memory", "content": "2.4GB / 8GB Used"},
    {"title": f"{EMOJI.GLOBE} Network", "content": "In: 1.2 MB/s\nOut: 0.4 MB/s"},
    {"title": f"{EMOJI.WARNING} Alerts", "content": "No active alerts"},
]

dashboard("System Monitor", widgets, columns=2)
```

**Parameters:**

- `title` (str): Dashboard title
- `widgets` (list): List of widget dicts with `title`, `content`, optional `width`/`ratio`
- `columns` (int): Number of columns (default: 2)
- `console` (Console, optional): Console instance to use

______________________________________________________________________

## HTML Export

### Basic Export

```python
from styledconsole import Console

# Initialize with recording
console = Console(record=True)

# Generate content
console.frame("Hello, World!", title="Demo")
console.banner("REPORT", start_color="green", end_color="blue")

# Export to HTML
html = console.export_html()

with open("output.html", "w") as f:
    f.write(html)
```

### Customization Options

```python
html = console.export_html(
    page_title="My Dashboard",
    theme=MONOKAI,
    theme_css="body { background: #222; }",
    inline_styles=True,
    clear_screen=True  # Clear buffer after export
)
```

______________________________________________________________________

## Tips & Best Practices

### Variable-Length Content

```python
from styledconsole import prepare_frame_content, auto_size_content

# Wrap long content
error = "DatabaseConnectionError: Unable to connect..."
content = prepare_frame_content(error, max_width=50, max_lines=5)
console.frame(content, title="Error", width=60)

# Auto-size based on content
content, width = auto_size_content(long_text, max_width=80)
console.frame(content, width=width + 4)
```

### Terminal Width Detection

```python
console = Console(detect_terminal=True)
term_width = console.terminal_profile.width if console.terminal_profile else 80
frame_width = int(term_width * 0.9)
console.frame(content, width=frame_width)
```

### Lists Over Multi-line Strings

```python
# ✅ Recommended
console.frame([
    "Line 1",
    "Line 2",
], width=40)

# ❌ May truncate
console.frame('''
Line 1
Line 2
''')
```

______________________________________________________________________

## API Conventions

### Color Parameters

| Context        | Parameter                  | Example                                                     |
| -------------- | -------------------------- | ----------------------------------------------------------- |
| Single element | `color`                    | `console.text("Hi", color="cyan")`                          |
| Frame content  | `content_color`            | `console.frame("Hi", content_color="white")`                |
| Frame border   | `border_color`             | `console.frame("Hi", border_color="blue")`                  |
| Gradients      | `start_color`, `end_color` | `console.banner("Hi", start_color="red", end_color="blue")` |

### Alignment

- `console.frame(..., align="center")` - Centers content inside frame
- `console.banner(..., align="center")` - Centers ASCII art

### Debugging

```python
console = Console(debug=True)  # Enable debug logging
```

______________________________________________________________________

## Migration Guide

### v0.1.0 → v0.3.0+

All v0.1.0 code continues to work. New recommended patterns:

| Old Pattern                          | New Pattern            |
| ------------------------------------ | ---------------------- |
| `FrameRenderer().render(...)`        | `Console().frame(...)` |
| `LayoutComposer().stack(...)`        | Rich `Group(...)`      |
| `LayoutComposer().side_by_side(...)` | Rich `Columns(...)`    |

### Advanced Layouts (v0.3.0+)

```python
from rich.panel import Panel
from rich.console import Group
from styledconsole import Console
from styledconsole.core.box_mapping import get_box_style

console = Console()

panel1 = Panel("First", box=get_box_style("rounded"))
panel2 = Panel("Second", box=get_box_style("rounded"))

group = Group(panel1, panel2)
console._rich_console.print(group)
```

______________________________________________________________________

## Troubleshooting

### Frame borders misaligned

**Cause:** ZWJ emoji in content or title
**Solution:** Use simple emojis or EMOJI constants

### Content truncated with `...`

**Cause:** Frame width too narrow
**Solution:** Add explicit `width` parameter or use list of strings

### Emoji shows as boxes

**Cause:** Terminal font doesn't support emoji
**Solution:** Use a Nerd Font or modern terminal (iTerm2, Windows Terminal, Kitty)

### VS16 emoji "glued" to text

**Cause:** Older library version
**Solution:** Update to v0.3.0+ (automatic spacing)

### Colors not showing

**Cause:** Terminal doesn't support colors or `NO_COLOR` env set
**Solution:** Use a color-capable terminal

______________________________________________________________________

## See Also

- **Examples:** `examples/gallery/` - Visual showcases
- **Source:** `src/styledconsole/` - Library source
- **Tests:** `tests/` - Usage examples in tests
