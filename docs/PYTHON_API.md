# 🐍 StyledConsole Python API

**Version:** 0.10.0
**Last Updated:** January 2026

The Python API provides complete control over StyledConsole's features. This is the **most powerful interface**, offering builders, model objects, effects, themes, and export capabilities.

______________________________________________________________________

## 📑 Table of Contents

1. [Quick Start](#-quick-start)
1. [Console Basics](#-console-basics)
1. [Frames & Borders](#-frames--borders)
1. [Frame Groups](#-frame-groups)
1. [Banners](#-banners)
1. [Builder Pattern](#-builder-pattern) *(New in v0.10.0)*
1. [Model Objects](#-model-objects) *(New in v0.10.0)*
1. [Effects System](#-effects-system)
1. [Palettes](#-palettes)
1. [Colors & Gradients](#-colors--gradients)
1. [Emojis](#-emojis)
1. [Icons & Terminal Fallback](#-icons--terminal-fallback)
1. [Themes](#-themes)
1. [Render Policy](#-render-policy)
1. [Export Formats](#-export-formats)
1. [Presets](#-presets)
1. [Tips & Best Practices](#-tips--best-practices)
1. [API Conventions](#-api-conventions)
1. [Troubleshooting](#-troubleshooting)
1. [API Reference](#-api-reference)

______________________________________________________________________

## 🚀 Quick Start

```python
from styledconsole import Console, icons, EffectSpec

console = Console()

# Simple frame
console.frame("Hello, World!", title="Greeting")

# Frame with gradient effect
console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful\n{icons.ROCKET} Deployed to production",
    title=f"{icons.SPARKLES} Status",
    border="rounded",
    effect=EffectSpec.gradient("green", "cyan"),
)
```

**Output:**

```
╭──────── ✨ Status ─────────╮
│ ✅ Build successful        │
│ 🚀 Deployed to production  │
╰────────────────────────────╯
```

______________________________________________________________________

## 🎛️ Console Basics

The `Console` class is the main entry point for all rendering operations.

```python
from styledconsole import Console, RenderPolicy

# Default console (auto-detects terminal capabilities)
console = Console()

# With explicit policy
console = Console(policy=RenderPolicy.ci_friendly())

# With recording enabled for export
console = Console(record=True)

# With theme
from styledconsole import THEMES
console = Console(theme=THEMES.MONOKAI)

# With debug logging
console = Console(debug=True)
```

### Console Parameters

| Parameter         | Type         | Default     | Description                              |
| ----------------- | ------------ | ----------- | ---------------------------------------- |
| `policy`          | RenderPolicy | auto-detect | Controls color, unicode, emoji rendering |
| `theme`           | Theme        | None        | Apply consistent styling                 |
| `record`          | bool         | False       | Enable recording for export              |
| `detect_terminal` | bool         | True        | Auto-detect terminal capabilities        |
| `debug`           | bool         | False       | Enable debug logging                     |

______________________________________________________________________

## 🖼️ Frames & Borders

### Basic Frame

```python
console.frame("Hello, World!", title="Greeting")
```

### 8 Border Styles

| Style     | Characters | Use Case                |
| --------- | ---------- | ----------------------- |
| `solid`   | `┌─┐│└┘`   | Default, professional   |
| `rounded` | `╭─╮│╰╯`   | Friendly, modern        |
| `double`  | `╔═╗║╚╝`   | Emphasis, headers       |
| `heavy`   | `┏━┓┃┗┛`   | Bold emphasis           |
| `thick`   | `█▀▄`      | Block style             |
| `ascii`   | `+--\|+`   | Universal compatibility |
| `minimal` | `─│`       | Clean, subtle           |
| `dashed`  | `┄┆`       | Drafts, previews        |

### Frame Parameters

```python
console.frame(
    content="Your content here",
    title="Title",
    border="rounded",           # Border style
    width=60,                   # Frame width
    padding=1,                  # Internal padding
    align="center",             # Content alignment: left|center|right
    frame_align="center",       # Frame position on screen
    margin=(1, 2, 1, 2),        # Margin: (top, right, bottom, left)
    content_color="white",      # Content text color
    border_color="blue",        # Border color
    title_color="cyan",         # Title color
    effect="fire",              # Effect preset or EffectSpec
)
```

### Margins & Alignment

You can control the positioning of the frame itself using `frame_align` and `margin`:

- `align`: Controls content *inside* the frame
- `frame_align`: Controls the frame's position on the screen
- `margin`: Adds space *outside* the border. Accepts `int` (all sides) or `tuple` (top, right, bottom, left)

```python
# Centered frame with 2 lines of vertical margin
console.frame(
    "Centered content",
    align="center",
    frame_align="center",
    margin=(2, 0, 2, 0)
)
```

### Gradient Borders

```python
from styledconsole import Console, EFFECTS, EffectSpec

console = Console()

# Using preset names
console.frame("Fire effect!", effect="fire")

# Using EFFECTS registry (IDE autocomplete support)
console.frame("Ocean vibes", effect=EFFECTS.ocean)

# Custom gradient
console.frame(
    "Custom gradient",
    effect=EffectSpec.gradient("red", "blue")
)

# Rainbow effect
console.frame("Rainbow!", effect=EffectSpec.rainbow())
```

<details>
<summary>Legacy syntax (deprecated)</summary>

```python
# Still works, but shows deprecation warning
console.frame(
    "Gradient magic!",
    border_gradient_start="red",
    border_gradient_end="blue"
)
```

</details>

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

## 📦 Frame Groups

Combine multiple frames into organized layouts.

### Basic Frame Group

```python
console.frame_group(
    [
        {"content": "Status: Online", "title": "System"},
        {"content": "CPU: 45%\nMemory: 2.1GB", "title": "Resources"},
        {"content": "Last backup: 2h ago", "title": "Backup"},
    ],
    title="Dashboard",
    border="double",
)
```

### Item Options

Each item in the list is a dictionary with these options:

| Key             | Required | Description                 |
| --------------- | -------- | --------------------------- |
| `content`       | ✅       | Frame content (str or list) |
| `title`         | ❌       | Individual frame title      |
| `border`        | ❌       | Border style for this frame |
| `border_color`  | ❌       | Border color                |
| `content_color` | ❌       | Content text color          |
| `title_color`   | ❌       | Title color                 |

### Layout Options

```python
# Vertical (default)
console.frame_group(items, layout="vertical", gap=1)

# Horizontal (side-by-side)
console.frame_group(items, layout="horizontal", gap=2)

# Grid (auto-columns)
console.frame_group(items, layout="grid", columns="auto", min_columns=2, item_width=35)

# Grid (fixed columns)
console.frame_group(items, layout="grid", columns=3, item_width=30)
```

### Styling Options

```python
# Individual frame styling
console.frame_group(
    [
        {"content": "All systems OK", "title": "Success", "border_color": "green"},
        {"content": "High usage", "title": "Warning", "border_color": "yellow"},
        {"content": "Connection failed", "title": "Error", "border_color": "red"},
    ],
    title="System Report",
    border="heavy",
)

# Outer frame gradient
console.frame_group(
    [{"content": "A"}, {"content": "B"}],
    effect=EffectSpec.gradient("cyan", "magenta"),
)
```

### Style Inheritance

Use `inherit_style=True` to have inner frames inherit the outer border style:

```python
console.frame_group(
    [
        {"content": "Section A"},
        {"content": "Section B"},
    ],
    border="heavy",
    inherit_style=True,  # Inner frames also use "heavy" border
)
```

### Gap Control

Control spacing between inner frames with `gap`:

```python
console.frame_group(
    [{"content": "Top"}, {"content": "Bottom"}],
    gap=0,  # No gap between frames (default: 1)
)
```

### Render to String (for Nesting)

Use `render_frame_group()` to get a string for nesting:

```python
# Render inner group to string
inner = console.render_frame_group(
    [{"content": "Sub-A"}, {"content": "Sub-B"}],
    title="Inner",
)

# Embed in outer frame
console.frame(inner, title="Outer")
```

### Frame Group Parameters

| Parameter       | Type           | Default      | Description                |
| --------------- | -------------- | ------------ | -------------------------- |
| `items`         | list           | *required*   | List of frame item dicts   |
| `title`         | str            | None         | Outer frame title          |
| `border`        | str            | `"rounded"`  | Outer border style         |
| `width`         | int            | None (auto)  | Outer frame width          |
| `padding`       | int            | 1            | Outer frame padding        |
| `align`         | str            | `"left"`     | Content alignment          |
| `border_color`  | str            | None         | Outer border color         |
| `title_color`   | str            | None         | Outer title color          |
| `effect`        | str/EffectSpec | None         | Gradient effect            |
| `layout`        | str            | `"vertical"` | Layout mode                |
| `gap`           | int            | 1            | Lines between inner frames |
| `inherit_style` | bool           | False        | Inner frames inherit style |

### Context Manager (console.group)

For more complex or dynamic layouts, use the `console.group()` context manager:

```python
from styledconsole import Console, EMOJI

console = Console()

with console.group(title="Dashboard", border="double", border_color="cyan"):
    console.frame("System status: Online", title="Status")
    console.frame("CPU: 45%\nMemory: 2.1GB", title="Resources")
    console.frame("Last backup: 2h ago", title="Backup")
```

#### Nested Groups

Groups can be nested for complex hierarchies:

```python
with console.group(title="Project Overview", border="heavy"):
    console.frame("Main application ready", title="App Status")

    with console.group(title="Services", border="rounded"):
        console.frame("Database connected", title="DB")
        console.frame("Cache active", title="Redis")

    console.frame("All tests passing", title="CI/CD")
```

#### Width Alignment

Use `align_widths=True` to make all inner frames the same width:

```python
with console.group(title="System Report", align_widths=True):
    console.frame("All systems operational", title="Success", border_color="green")
    console.frame("High memory usage detected", title="Warning", border_color="yellow")
    console.frame("Connection failed", title="Error", border_color="red")
```

#### Context Manager Parameters

| Parameter       | Type           | Default     | Description                  |
| --------------- | -------------- | ----------- | ---------------------------- |
| `title`         | str            | None        | Outer frame title            |
| `border`        | str            | `"rounded"` | Outer border style           |
| `width`         | int            | None (auto) | Outer frame width            |
| `padding`       | int            | 1           | Outer frame padding          |
| `border_color`  | str            | None        | Outer border color           |
| `title_color`   | str            | None        | Outer title color            |
| `effect`        | str/EffectSpec | None        | Gradient effect              |
| `gap`           | int            | 1           | Lines between inner frames   |
| `inherit_style` | bool           | False       | Inner frames inherit style   |
| `align_widths`  | bool           | False       | Make inner frames same width |

#### When to Use Which API

| Scenario                      | Recommended API        |
| ----------------------------- | ---------------------- |
| Dynamic content, nesting      | `console.group()`      |
| Simple, data-driven layouts   | `frame_group()`        |
| Complex gradient compositions | `render_frame()`       |
| Embedding in outer frames     | `render_frame_group()` |

______________________________________________________________________

## 🔤 Banners

ASCII art text with gradient support using 500+ fonts.

```python
from styledconsole import Console, EFFECTS, EffectSpec

console = Console()

# Basic banner
console.banner("HELLO", font="slant")

# With effects
console.banner("LAUNCH", font="banner", effect="fire")
console.banner("SUCCESS", font="big", effect=EFFECTS.success)

# Custom gradient
console.banner(
    "CUSTOM",
    font="banner",
    effect=EffectSpec.gradient("red", "blue")
)
```

### Available Fonts

Common pyfiglet fonts: `standard`, `slant`, `banner`, `big`, `small`, `mini`

<details>
<summary>Legacy syntax (deprecated)</summary>

```python
# Still works, but shows deprecation warning
console.banner("LAUNCH", font="banner", start_color="red", end_color="blue")
console.banner("RAINBOW", font="slant", rainbow=True)
```

</details>

______________________________________________________________________

## 🏗️ Builder Pattern

*New in v0.10.0*

Fluent API for constructing complex layouts step-by-step.

### FrameBuilder

```python
from styledconsole import Console

console = Console()

frame = (
    console.build_frame()
    .title("Status Report")
    .content("All systems operational")
    .border("rounded")
    .effect("success")
    .width(50)
    .build()
)
console.render_object(frame)
```

### TableBuilder

```python
table = (
    console.build_table()
    .title("Server Status")
    .columns("Server", "Status", "Uptime")
    .row("api-1", "Online", "99.9%")
    .row("api-2", "Online", "99.8%")
    .row("db-1", "Maintenance", "95.2%")
    .border("heavy")
    .effect("ocean")
    .build()
)
console.render_object(table)
```

### BannerBuilder

```python
banner = (
    console.build_banner()
    .text("DEPLOY")
    .font("slant")
    .effect("fire")
    .build()
)
console.render_object(banner)
```

### LayoutBuilder

```python
from styledconsole.model import Text, Rule, Spacer

layout = (
    console.build_layout()
    .add(Text("Welcome to the Dashboard", style={"bold": True}))
    .add(Rule())
    .add(Spacer(lines=1))
    .add(frame)  # Add a previously built frame
    .add(table)  # Add a previously built table
    .build()
)
console.render_object(layout)
```

### Chaining Builders

```python
# Build complete dashboards fluently
header = console.build_banner().text("DASHBOARD").effect("rainbow").build()
status = console.build_frame().title("Status").content("Online").effect("success").build()
metrics = console.build_table().columns("Metric", "Value").row("CPU", "45%").row("RAM", "2.1GB").build()

dashboard = (
    console.build_layout()
    .add(header)
    .add(Spacer(lines=1))
    .add(status)
    .add(metrics)
    .build()
)
console.render_object(dashboard)
```

______________________________________________________________________

## 📊 Model Objects

*New in v0.10.0*

Immutable dataclasses representing UI components. Use these for programmatic UI construction.

### Available Models

```python
from styledconsole.model import (
    Text,       # Styled text
    Frame,      # Bordered frame
    Banner,     # ASCII art banner
    Table,      # Data table
    Layout,     # Vertical layout container
    Group,      # Generic group of items
    Spacer,     # Vertical spacing
    Rule,       # Horizontal rule
    Style,      # Text styling
)
```

### Text

```python
from styledconsole.model import Text, Style

# Simple text
text = Text("Hello, World!")

# Styled text
text = Text(
    "Important message",
    style=Style(bold=True, color="red")
)
```

### Frame

```python
from styledconsole.model import Frame

frame = Frame(
    content="Frame content here",
    title="My Frame",
    border="rounded",
    effect="ocean",
    width=50,
)
```

### Table

```python
from styledconsole.model import Table

table = Table(
    title="Server Status",
    columns=["Server", "Status", "Uptime"],
    rows=[
        ["api-1", "Online", "99.9%"],
        ["api-2", "Online", "99.8%"],
    ],
    border="heavy",
)
```

### Layout

```python
from styledconsole.model import Layout, Text, Frame, Spacer, Rule, Style

layout = Layout(items=[
    Text("Dashboard Header", style=Style(bold=True)),
    Rule(),
    Spacer(lines=1),
    Frame(content="Status: Online", title="System"),
    Frame(content="CPU: 45%", title="Resources"),
])
```

### Rendering Model Objects

```python
from styledconsole import Console
from styledconsole.model import Frame

console = Console()

# Create model object
frame = Frame(content="Hello!", title="Greeting", effect="success")

# Render it
console.render_object(frame)
```

______________________________________________________________________

## ✨ Effects System

The effects system provides gradients, rainbows, and color effects.

### Using Presets

```python
from styledconsole import Console, EFFECTS

console = Console()

# By name (string)
console.frame("Content", effect="fire")

# By registry (IDE autocomplete support)
console.frame("Content", effect=EFFECTS.ocean)
console.frame("Content", effect=EFFECTS.rainbow)
console.frame("Content", effect=EFFECTS.cyberpunk)
```

### Available Presets (32 total)

| Category           | Presets                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| 🔥 **Gradients**   | `fire`, `ocean`, `sunset`, `forest`, `aurora`, `lavender`, `peach`, `mint`, `steel`, `gold`                               |
| 🌈 **Rainbows**    | `rainbow`, `rainbow_pastel`, `rainbow_neon`, `rainbow_muted`, `rainbow_reverse`, `rainbow_horizontal`, `rainbow_diagonal` |
| 🎨 **Themed**      | `matrix`, `cyberpunk`, `retro`, `vaporwave`, `dracula`, `nord_aurora`                                                     |
| 📊 **Semantic**    | `success`, `warning`, `error`, `info`, `neutral`                                                                          |
| 🖼️ **Border-only** | `border_fire`, `border_ocean`, `border_rainbow`, `border_gold`                                                            |

### Custom Effects with EffectSpec

```python
from styledconsole import EffectSpec

# Two-color gradient
effect = EffectSpec.gradient("red", "blue")
effect = EffectSpec.gradient("#ff6b6b", "#4ecdc4", direction="horizontal")

# Multi-stop gradient (3+ colors)
effect = EffectSpec.multi_stop(["red", "yellow", "green"])
effect = EffectSpec.multi_stop(
    colors=["#ff0000", "#00ff00", "#0000ff"],
    stops=[0.0, 0.5, 1.0]  # Custom positions
)

# Rainbow effects
effect = EffectSpec.rainbow()
effect = EffectSpec.rainbow(saturation=0.8, brightness=1.0)
effect = EffectSpec.rainbow(neon=True)  # Cyberpunk colors
```

### Effect Modifiers

Effects are immutable, so modifiers return new instances:

```python
from styledconsole import EFFECTS

# Change direction
effect = EFFECTS.fire.with_direction("horizontal")
effect = EFFECTS.ocean.with_direction("diagonal")

# Change target
effect = EFFECTS.rainbow.with_target("border")   # Only apply to border
effect = EFFECTS.fire.with_target("content")     # Only apply to content

# Reverse colors
effect = EFFECTS.sunset.reversed()
```

### Target Options

| Target      | Effect Applied To            |
| ----------- | ---------------------------- |
| `"both"`    | Border and content (default) |
| `"border"`  | Border only                  |
| `"content"` | Content text only            |

### Direction Options

| Direction      | Description              |
| -------------- | ------------------------ |
| `"vertical"`   | Top to bottom (default)  |
| `"horizontal"` | Left to right            |
| `"diagonal"`   | Top-left to bottom-right |

### Phase Animation

```python
from styledconsole import EffectSpec, cycle_phase

phase = 0.0
for _ in range(30):
    console.frame("Animated!", effect=EffectSpec.rainbow(phase=phase))
    phase = cycle_phase(phase)  # Increments and wraps at 1.0
```

### Animated Gradients (Advanced)

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

## 🎨 Palettes

90 curated color palettes organized by category.

```python
from styledconsole import PALETTES, get_palette, list_palettes, get_palette_categories, EffectSpec

# Get a palette
ocean = get_palette("ocean_depths")  # {"colors": [...], "categories": [...]}

# List palettes by category
vibrant = list_palettes("vibrant")   # ["fire", "neon", "sunset", ...]
pastel = list_palettes("pastel")     # ["pastel_candy", "soft_dream", ...]

# Get all categories
categories = get_palette_categories()  # {"vibrant": 45, "pastel": 12, ...}

# Use palette in effect
console.frame("Content", effect=EffectSpec.from_palette("ocean_depths"))
```

### Categories

`warm`, `cool`, `vibrant`, `muted`, `pastel`, `dark`, `bright`, `monochrome`, `rainbow`

______________________________________________________________________

## 🌈 Colors & Gradients

### Color Formats

```python
# CSS4 color names (148 supported)
console.frame("Text", border_color="dodgerblue")

# Extended named colors (949+)
console.frame("Text", border_color="azure_radiance")

# Hex codes
console.frame("Text", border_color="#1E90FF")

# RGB tuples
console.frame("Text", border_color=(30, 144, 255))
```

### Common Status Colors

| Purpose    | Recommended Colors            |
| ---------- | ----------------------------- |
| ✅ Success | `lime`, `green`, `limegreen`  |
| ❌ Error   | `red`, `crimson`, `indianred` |
| ⚠️ Warning | `yellow`, `gold`, `orange`    |
| ℹ️ Info    | `blue`, `dodgerblue`, `cyan`  |
| ⚪ Neutral | `gray`, `silver`, `white`     |

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

______________________________________________________________________

## 😀 Emojis

> [!TIP]
> **For terminal output, use [`icons`](#-icons--terminal-fallback) instead of `EMOJI`.**
> The `icons` module provides automatic fallback to colored ASCII in environments
> that don't support emoji (CI/CD, SSH, Windows cmd). Use `EMOJI` for raw emoji
> access in special cases (HTML export, custom rendering).

StyledConsole uses the [`emoji`](https://pypi.org/project/emoji/) package as its emoji backend, providing access to **4000+ emojis** with CLDR standard names.

### Quick Reference

| Emoji Type    | Support   | Example        |
| ------------- | --------- | -------------- |
| Standard      | ✅ Full   | ✅ ❌ 🚀 💡 🎉 |
| VS16          | ✅ Full   | ⚠️ ℹ️ ⚙️ ⏱️    |
| Skin tones    | ⚠️ Varies | 👍🏽 👋🏻          |
| ZWJ sequences | ❌ None   | 👨‍💻 👨‍👩‍👧          |

### Using EMOJI Constants

All emoji names follow CLDR (Unicode Common Locale Data Repository) canonical names:

```python
from styledconsole import EMOJI, E  # E is short alias

# Status indicators (canonical names)
EMOJI.CHECK_MARK_BUTTON   # ✅
EMOJI.CROSS_MARK          # ❌
EMOJI.WARNING             # ⚠️
EMOJI.INFORMATION         # ℹ️

# Common icons
EMOJI.ROCKET              # 🚀
EMOJI.FIRE                # 🔥
EMOJI.STAR                # ⭐
EMOJI.SPARKLES            # ✨

# Technology
EMOJI.LAPTOP              # 💻
EMOJI.GEAR                # ⚙️
EMOJI.BAR_CHART           # 📊
EMOJI.PACKAGE             # 📦
```

### Search & Discovery

Find emojis by partial name:

```python
# Search for emojis containing "check"
results = EMOJI.search("check")
# Returns: [('CHECK_MARK', '✔️'), ('CHECK_MARK_BUTTON', '✅'), ...]

# Limit results
results = EMOJI.search("circle", limit=5)

# Safe access with default
emoji = EMOJI.get("ROCKET", default="*")  # Returns 🚀 or "*" if not found

# Check if emoji exists
if "ROCKET" in EMOJI:
    print("Rocket available!")

# Get count of available emojis
print(f"{len(EMOJI)} emojis available")  # ~4000+
```

### CuratedEmojis: Organized Categories

For discoverability, use the curated category lists:

```python
from styledconsole import CuratedEmojis, EMOJI

# Status indicators for CLI apps
for name in CuratedEmojis.STATUS:
    print(f"{name}: {getattr(EMOJI, name)}")
# CHECK_MARK_BUTTON: ✅, CROSS_MARK: ❌, WARNING: ⚠️, ...

# Colored circles (great for status dots)
for name in CuratedEmojis.CIRCLES:
    print(f"{name}: {getattr(EMOJI, name)}")
# RED_CIRCLE: 🔴, YELLOW_CIRCLE: 🟡, GREEN_CIRCLE: 🟢, ...

# File/folder related
CuratedEmojis.FILES
# ['FILE_FOLDER', 'OPEN_FILE_FOLDER', 'PAGE_FACING_UP', ...]

# Development tools
CuratedEmojis.DEV
# ['ROCKET', 'FIRE', 'STAR', 'SPARKLES', 'LIGHT_BULB', 'GEAR', ...]
```

### Unicode Arrows (Special)

Unicode arrows are available alongside emojis:

```python
EMOJI.ARROW_UP      # ↑
EMOJI.ARROW_DOWN    # ↓
EMOJI.ARROW_LEFT    # ←
EMOJI.ARROW_RIGHT   # →
```

### Modern Terminal Support: ZWJ Sequences

StyledConsole supports **ZWJ (Zero Width Joiner)** sequences and **Skin Tone Modifiers** in modern terminals. These are rendered as single glyphs with correct width calculation.

| Emoji Type    | Modern Terminals¹ | Standard Terminals² | Example |
| ------------- | ----------------- | ------------------- | ------- |
| ZWJ Sequences | ✅ Supported      | ⚠️ Degraded         | 👨‍💻 👨‍👩‍👧   |
| Skin Tones    | ✅ Supported      | ⚠️ Degraded         | 👍🏽 👋🏻   |
| Rainbow Flag  | ✅ Supported³     | ⚠️ Degraded         | 🏳️‍🌈      |

1. **Modern Terminals:** Kitty, WezTerm, Ghostty, iTerm2, Alacritty
1. **Standard Terminals:** Gnome Terminal, VSCode built-in, Windows Terminal
1. **Rainbow Flag:** Specifically tuned for modern width (3) vs legacy (3) to ensure alignment

#### Using ZWJ Sequences

```python
from styledconsole import Console, EMOJI

console = Console()
# These now align perfectly in modern terminals!
console.frame([
    f"{EMOJI.MAN_TECHNOLOGIST} Developer at work",
    f"{EMOJI.RAINBOW_FLAG} Pride in terminal",
], title="ZWJ Support")
```

______________________________________________________________________

## 🎯 Icons & Terminal Fallback

> [!IMPORTANT]
> **The `icons` module is the recommended way to display symbols in terminal output.**
> It provides 204 icons with automatic fallback to colored ASCII in environments
> that don't support emoji.

The `icons` module provides **policy-aware icons** that automatically choose between Unicode emojis and colored ASCII based on terminal capabilities.

### Why Use Icons?

| Environment     | EMOJI        | icons        |
| --------------- | ------------ | ------------ |
| Modern terminal | ✅           | ✅           |
| CI/CD (Jenkins) | ❌ (boxes)   | ✅ (colored) |
| SSH sessions    | ❌ (broken)  | ✅ (ASCII)   |
| Windows cmd.exe | ❌ (garbled) | ✅ (colored) |
| Piped output    | ❌ (broken)  | ✅ (plain)   |

### Using Icons

```python
from styledconsole import icons, set_icon_mode

# Access icons via attributes - automatically chooses emoji or ASCII
print(f"{icons.CHECK_MARK_BUTTON} Tests passed")  # ✅ or (OK) in green
print(f"{icons.CROSS_MARK} Build failed")         # ❌ or (FAIL) in red
print(f"{icons.WARNING} Deprecation")             # ⚠️ or (WARN) in yellow
print(f"{icons.ROCKET} Deploying...")             # 🚀 or >>> in cyan

# Force specific mode globally
set_icon_mode("ascii")   # Force colored ASCII everywhere
set_icon_mode("emoji")   # Force emoji everywhere
set_icon_mode("auto")    # Auto-detect (default)
```

### Icon Categories

| Category  | Examples                                              | Count |
| --------- | ----------------------------------------------------- | ----- |
| STATUS    | CHECK_MARK_BUTTON, CROSS_MARK, WARNING, INFO          | 11    |
| STARS     | STAR, SPARKLES, GLOWING_STAR                          | 7     |
| DOCUMENT  | FILE_FOLDER, CLIPBOARD, MEMO                          | 9     |
| TECH      | LAPTOP, MOBILE_PHONE, KEYBOARD                        | 16    |
| TOOLS     | WRENCH, HAMMER, GEAR                                  | 13    |
| TRANSPORT | ROCKET, AUTOMOBILE, AIRPLANE                          | 10    |
| WEATHER   | SUN, MOON, CLOUD, DROPLET, HIGH_VOLTAGE               | 12    |
| ARROWS    | ARROW_RIGHT, ARROW_UP, COUNTERCLOCKWISE_ARROWS_BUTTON | 15    |

### Icon Properties

```python
from styledconsole import icons

icon = icons.get("CHECK_MARK_BUTTON")
print(icon.emoji)       # "✅"
print(icon.ascii)       # "(OK)"
print(icon.color)       # "green"
print(icon.as_emoji())  # Always returns emoji
print(icon.as_ascii())  # Always returns colored ASCII
```

### Migrating from EMOJI to icons

> [!NOTE]
> **Existing code using `EMOJI` continues to work.** This migration is recommended
> but not required.

#### Quick Migration

| Before (EMOJI)                    | After (icons)                     |
| --------------------------------- | --------------------------------- |
| `from styledconsole import EMOJI` | `from styledconsole import icons` |
| `EMOJI.CHECK_MARK_BUTTON`         | `icons.CHECK_MARK_BUTTON`         |
| `EMOJI.ROCKET`                    | `icons.ROCKET`                    |
| `f"{EMOJI.STAR} Done"`            | `f"{icons.STAR} Done"`            |

#### Name Differences

Most names are identical. A few icons use shorter names:

| EMOJI Name      | icons Name |
| --------------- | ---------- |
| `FLEXED_BICEPS` | `MUSCLE`   |
| `OPTICAL_DISK`  | `CD`       |
| `CRESCENT_MOON` | `MOON`     |
| `HAMBURGER`     | `BURGER`   |

#### Icon Multiplication

Icons are objects, not strings. To repeat them:

```python
# Before (EMOJI - string)
stars = EMOJI.STAR * 5  # "⭐⭐⭐⭐⭐"

# After (icons - object)
stars = str(icons.STAR) * 5  # "⭐⭐⭐⭐⭐"
# Or use icons.STAR.as_emoji() * 5
```

#### When to Keep Using EMOJI

Use `EMOJI` directly for:

- HTML export (raw emoji access)
- Custom rendering pipelines
- Emoji search/discovery (`EMOJI.search()`)
- Accessing emojis not in the icons facade

______________________________________________________________________

## 🎨 Themes

Apply consistent styling across your application.

```python
from styledconsole import Console, THEMES

console = Console(theme=THEMES.MONOKAI)
console.frame("Content matches the theme!", title="Themed Output")
```

### Available Themes

| Theme         | Primary             | Secondary           | Success           | Description                          |
| ------------- | ------------------- | ------------------- | ----------------- | ------------------------------------ |
| **DARK**      | 🟦 `cyan`           | 🟪 `magenta`        | 🟩 `bright_green` | Standard high-contrast dark mode     |
| **LIGHT**     | 🟦 `blue`           | 🟪 `magenta`        | 🟩 `green`        | Clean light mode for white terminals |
| **MONOKAI**   | 🟪 `magenta`        | 🟦 `bright_blue`    | 🟩 `green`        | Classic IDE theme, retro feel        |
| **NORD**      | 🟦 `bright_blue`    | 🟪 `magenta`        | 🟩 `green`        | Cool arctic blue palette             |
| **DRACULA**   | 🟪 `bright_magenta` | 🟪 `purple`         | 🟩 `green`        | High contrast dark theme             |
| **SOLARIZED** | 🟦 `cyan`           | 🟩 `green`          | 🟩 `green`        | Precision colors for eye comfort     |
| **FIRE**      | 🟥 `red`            | 🟧 `orange3`        | 🟨 `yellow`       | 🔥 Intense gradients for alerts      |
| **SUNNY**     | 🟨 `gold3`          | 🟧 `orange1`        | 🟩 `bright_green` | ☀️ Warm, positive vibes              |
| **RAINBOW**   | 🟪 `magenta`        | 🟦 `cyan`           | 🟩 `bright_green` | 🌈 Full-spectrum gradients           |
| **OCEAN**     | 🟦 `blue`           | 🟦 `cyan`           | 🟩 `green`        | 🌊 Deep blue monochromatic           |
| **SUNSET**    | 🟥 `red`            | 🟪 `magenta`        | 🟩 `bright_green` | 🌅 Warm red-to-yellow                |
| **NEON**      | 🟩 `bright_green`   | 🟪 `bright_magenta` | 🟩 `bright_green` | ⚡ Cyberpunk aesthetic               |

### Themed Progress Bars

Progress bars automatically adapt to your chosen theme with **Dual-mode** behavior:

1. **Default Console (No Theme):**

   - **Behavior:** Classic "Green Means Go"
   - **Color:** Green bar for both running and finished states

1. **Themed Console (e.g., FIRE):**

   - **Behavior:** Fully immersive theming
   - **Color:** Uses the theme's **Primary** color for running and finished states
   - **Components:** Spinners, percent text, and steps all colored to match

```python
# Green bar (classic)
console = Console()
with console.progress() as progress:
    ...

# Red bar (immersive)
console = Console(theme=THEMES.FIRE)
with console.progress() as progress:
    ...
```

______________________________________________________________________

## 🔧 Render Policy

**RenderPolicy** is the central control mechanism for adapting output to different terminal environments.

### Why Use RenderPolicy?

StyledConsole is **policy-aware** throughout the entire rendering pipeline:

- **Colors:** Skipped when `policy.color=False`
- **Unicode borders:** Falls back to ASCII when `policy.unicode=False`
- **Emojis:** Uses colored ASCII fallback when `policy.emoji=False`
- **Gradients:** Plain text when colors disabled
- **Progress bars:** Text-based fallback without cursor control

### Automatic Detection

```python
from styledconsole import Console

# Auto-detects capabilities from environment
console = Console()

# Access the detected policy
print(console.policy)
# RenderPolicy(color=True, unicode=True, emoji=True, ...)
```

### Environment Variables

| Variable         | Effect                               |
| ---------------- | ------------------------------------ |
| `NO_COLOR`       | Disables all color output            |
| `FORCE_COLOR`    | Forces color even without TTY        |
| `TERM=dumb`      | Disables Unicode and emoji           |
| `CI=true`        | Conservative mode (colors, no emoji) |
| `GITHUB_ACTIONS` | CI-friendly output                   |
| `GITLAB_CI`      | CI-friendly output                   |
| `JENKINS_URL`    | CI-friendly output                   |

### Explicit Policy Control

```python
from styledconsole import Console, RenderPolicy

# Factory methods for common scenarios
policy = RenderPolicy.full()          # All features enabled
policy = RenderPolicy.minimal()       # ASCII only, no colors
policy = RenderPolicy.ci_friendly()   # Colors, ASCII icons
policy = RenderPolicy.no_color()      # Respects NO_COLOR standard

# Use with Console
console = Console(policy=RenderPolicy.ci_friendly())

# Auto-detect with overrides
policy = RenderPolicy.from_env().with_override(emoji=False)
console = Console(policy=policy)
```

### Policy Properties

| Property  | True                | False                |
| --------- | ------------------- | -------------------- |
| `color`   | ANSI color codes    | Plain text           |
| `unicode` | Unicode box drawing | ASCII `+--+`         |
| `emoji`   | Unicode emoji       | Colored ASCII `(OK)` |

### Creating Custom Policies

```python
from styledconsole import RenderPolicy, Console

# Full manual control
policy = RenderPolicy(
    color=True,     # Enable ANSI colors
    unicode=True,   # Use Unicode borders
    emoji=False,    # Use ASCII icons
)
console = Console(policy=policy)

# Override specific settings
base = RenderPolicy.from_env()
custom = base.with_override(
    emoji=False,    # Force ASCII icons
    color=True,     # Force colors on
)
```

### Global Default Policy

```python
from styledconsole import set_default_policy, reset_default_policy, RenderPolicy

# Set for entire application
set_default_policy(RenderPolicy.ci_friendly())

# All new Console instances use this policy
console1 = Console()  # Uses ci_friendly
console2 = Console()  # Uses ci_friendly

# Reset to auto-detection
reset_default_policy()
```

### What Gets Affected

| Component        | policy.color=False | policy.unicode=False | policy.emoji=False  |
| ---------------- | ------------------ | -------------------- | ------------------- |
| Frame borders    | No color           | ASCII `+--+`         | (no effect)         |
| Border gradients | Skipped            | (no effect)          | (no effect)         |
| Content colors   | Plain text         | (no effect)          | (no effect)         |
| icons module     | Plain ASCII        | (no effect)          | Colored ASCII       |
| Progress bars    | Text-based         | ASCII progress       | (no effect)         |
| Presets (status) | Plain text         | ASCII borders        | Colored ASCII icons |

### Example: CI/CD Output

```python
from styledconsole import Console, RenderPolicy, icons

# In CI environment - auto-detected
console = Console()  # Detects CI=true, uses conservative settings

# Explicit CI mode
console = Console(policy=RenderPolicy.ci_friendly())

# Works in all environments
console.frame(
    f"{icons.CHECK_MARK_BUTTON} All tests passed\n{icons.ROCKET} Deploying...",
    title="Build Status",
    border="rounded",
    border_color="green"
)

# Output in modern terminal:
# ╭────── Build Status ──────╮
# │ ✅ All tests passed      │
# │ 🚀 Deploying...          │
# ╰──────────────────────────╯

# Output in CI (ASCII mode):
# +------ Build Status ------+
# | (OK) All tests passed    |
# | >>> Deploying...         |
# +--------------------------+
```

______________________________________________________________________

## 📤 Export Formats

### HTML Export

```python
from styledconsole import Console

# Initialize with recording
console = Console(record=True)

# Generate content
console.frame("Hello, World!", title="Demo")
console.banner("REPORT", effect="ocean")

# Export to HTML
html = console.export_html()

with open("output.html", "w") as f:
    f.write(html)
```

#### HTML Customization

```python
html = console.export_html(
    page_title="My Dashboard",
    theme=MONOKAI,
    theme_css="body { background: #222; }",
    inline_styles=True,
    clear_screen=True  # Clear buffer after export
)
```

### Plain Text Export

```python
console = Console(record=True)
console.frame("Content", title="Demo")

# Get ANSI-stripped plain text
text = console.export_text()
```

### Image Export

> Requires: `pip install styledconsole[image]`

Export console output as high-quality images using Pillow. Supports PNG, WebP (static and animated), and GIF formats.

#### Static Image Export

```python
from styledconsole import Console, icons

console = Console(record=True)
console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful",
    title="Status",
    border="rounded",
)

# Export as WebP (recommended - smaller file size)
console.export_webp("output.webp")

# Export as PNG with retina scaling
console.export_png("output.png", scale=2.0)

# Export as GIF
console.export_gif("output.gif")
```

#### Export Methods

| Method          | Format | Best For                   |
| --------------- | ------ | -------------------------- |
| `export_webp()` | WebP   | Modern format, small files |
| `export_png()`  | PNG    | Universal compatibility    |
| `export_gif()`  | GIF    | Legacy support, animations |

#### WebP Parameters

```python
console.export_webp(
    "output.webp",
    quality=90,       # Image quality (0-100)
    animated=False,   # Set True for animated output
    fps=10,           # Frames per second (animated only)
    loop=0,           # Loop count (0 = infinite)
)
```

#### PNG Parameters

```python
console.export_png(
    "output.png",
    scale=1.0,        # Scale factor (2.0 for retina)
)
```

#### GIF Parameters

```python
console.export_gif(
    "output.gif",
    fps=10,           # Frames per second
    loop=0,           # Loop count (0 = infinite)
)
```

#### Advanced: Direct ImageExporter Usage

For more control, use the `ImageExporter` class directly:

```python
from styledconsole.export import get_image_exporter, get_image_theme
from rich.console import Console as RichConsole

# Create custom theme
ImageTheme = get_image_theme()
custom_theme = ImageTheme(
    background="#000000",
    foreground="#ffffff",
    font_size=16,
    padding=30,
)

# Create Rich console with recording
rich_console = RichConsole(record=True)
rich_console.print("[bold red]Hello[/bold red] [green]World[/green]")

# Export with custom theme
ImageExporter = get_image_exporter()
exporter = ImageExporter(rich_console, theme=custom_theme)
exporter.save_webp("custom.webp")
```

#### Theme Properties

| Property      | Default   | Description              |
| ------------- | --------- | ------------------------ |
| `background`  | `#1e1e2e` | Background color (hex)   |
| `foreground`  | `#cdd6f4` | Default text color (hex) |
| `font_size`   | `14`      | Font size in pixels      |
| `padding`     | `20`      | Padding around content   |
| `line_height` | `1.2`     | Line height multiplier   |

______________________________________________________________________

## 📋 Presets

Pre-built, high-level components for common CLI patterns.

> 💡 **Policy-Aware:** All presets respect the Console's render policy. They use the
> `icons` module for symbols, so they degrade gracefully in CI/CD environments,
> SSH sessions, and terminals without emoji support.

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
    {"title": f"{EMOJI.BAR_CHART} CPU Load", "content": "45% Usage\n8 Cores Active"},
    {"title": f"{EMOJI.PACKAGE} Memory", "content": "2.4GB / 8GB Used"},
    {"title": f"{EMOJI.GLOBE_WITH_MERIDIANS} Network", "content": "In: 1.2 MB/s\nOut: 0.4 MB/s"},
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

## 💡 Tips & Best Practices

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

## 📐 API Conventions

### Color Parameters

| Context        | Parameter       | Example                                      |
| -------------- | --------------- | -------------------------------------------- |
| Single element | `color`         | `console.text("Hi", color="cyan")`           |
| Frame content  | `content_color` | `console.frame("Hi", content_color="white")` |
| Frame border   | `border_color`  | `console.frame("Hi", border_color="blue")`   |
| Effects        | `effect`        | `console.frame("Hi", effect="fire")`         |

### Alignment

- `console.frame(..., align="center")` — Centers content inside frame
- `console.banner(..., align="center")` — Centers ASCII art

### Debugging

```python
console = Console(debug=True)  # Enable debug logging
```

______________________________________________________________________

## 🔍 Troubleshooting

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

### Gradients look choppy

**Cause:** Terminal with limited color support
**Solution:** Use a true-color terminal (256+ colors)

______________________________________________________________________

## 📚 API Reference

### Console Methods

| Method              | Description                      |
| ------------------- | -------------------------------- |
| `frame()`           | Render bordered frame            |
| `banner()`          | Render ASCII art banner          |
| `text()`            | Render styled text               |
| `frame_group()`     | Render multiple frames           |
| `group()`           | Context manager for frame groups |
| `columns()`         | Render content in columns        |
| `print()`           | Print any renderable             |
| `render_object()`   | Render a model object            |
| `render_dict()`     | Render from dictionary config    |
| `render_template()` | Render built-in template         |
| `build_frame()`     | Get FrameBuilder                 |
| `build_table()`     | Get TableBuilder                 |
| `build_banner()`    | Get BannerBuilder                |
| `build_layout()`    | Get LayoutBuilder                |
| `export_html()`     | Export to HTML                   |
| `export_png()`      | Export to PNG                    |
| `export_webp()`     | Export to WebP                   |
| `export_gif()`      | Export to GIF                    |
| `export_text()`     | Export to plain text             |

### Top-Level Imports

```python
from styledconsole import (
    # Core
    Console,
    RenderPolicy,

    # Effects
    EFFECTS,
    EffectSpec,
    cycle_phase,

    # Palettes
    PALETTES,
    get_palette,
    list_palettes,
    get_palette_categories,

    # Icons & Emoji
    icons,
    set_icon_mode,
    EMOJI,
    CuratedEmojis,

    # Themes
    THEMES,

    # Declarative
    load_json,
    load_yaml,
    render_jinja,
)

# Model Objects (separate import)
from styledconsole.model import (
    Text, Frame, Banner, Table, Layout, Group, Spacer, Rule, Style
)
```

______________________________________________________________________

## 🔗 See Also

- [Declarative Guide](DECLARATIVE.md) — JSON/YAML configuration
- [Jinja2 Templates](JINJA_TEMPLATES.md) — Dynamic templates
- [Visual Gallery](GALLERY.md) — Screenshots and demos
- [Migration Guide](MIGRATION.md) — Upgrading from earlier versions
- [Developer Guide](DEVELOPER_GUIDE.md) — Architecture and internals
- [Examples Repository](https://github.com/ksokolowski/StyledConsole-Examples) — 50+ working demos
