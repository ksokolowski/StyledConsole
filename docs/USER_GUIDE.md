# StyledConsole User Guide

**Version:** 0.9.1
**Last Updated:** December 7, 2025

______________________________________________________________________

## Table of Contents

1. [Quick Start](#quick-start)
1. [Frames & Borders](#frames--borders)
1. [Frame Groups](#frame-groups)
1. [Banners](#banners)
1. [Colors & Gradients](#colors--gradients)
1. [Emojis](#emojis)
1. [Icons & Terminal Fallback](#icons--terminal-fallback)
1. [Render Policy](#render-policy)
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
    f"{EMOJI.CHECK_MARK_BUTTON} Build successful\n{EMOJI.ROCKET} Deployed to production",
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

## Frame Groups

> **New in v0.7.0**

Frame groups allow you to combine multiple frames into organized layouts, perfect for dashboards, status panels, and multi-section displays.

### Basic Frame Group

```python
from styledconsole import Console

console = Console()

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
    border_gradient_start="cyan",
    border_gradient_end="magenta",
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

| Parameter               | Type | Default      | Description                |
| ----------------------- | ---- | ------------ | -------------------------- |
| `items`                 | list | *required*   | List of frame item dicts   |
| `title`                 | str  | None         | Outer frame title          |
| `border`                | str  | `"rounded"`  | Outer border style         |
| `width`                 | int  | None (auto)  | Outer frame width          |
| `padding`               | int  | 1            | Outer frame padding        |
| `align`                 | str  | `"left"`     | Content alignment          |
| `border_color`          | str  | None         | Outer border color         |
| `title_color`           | str  | None         | Outer title color          |
| `border_gradient_start` | str  | None         | Outer gradient start       |
| `border_gradient_end`   | str  | None         | Outer gradient end         |
| `layout`                | str  | `"vertical"` | Layout mode                |
| `gap`                   | int  | 1            | Lines between inner frames |
| `inherit_style`         | bool | False        | Inner frames inherit style |

### Context Manager (console.group)

> **New in v0.7.0**

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

| Parameter               | Type | Default     | Description                  |
| ----------------------- | ---- | ----------- | ---------------------------- |
| `title`                 | str  | None        | Outer frame title            |
| `border`                | str  | `"rounded"` | Outer border style           |
| `width`                 | int  | None (auto) | Outer frame width            |
| `padding`               | int  | 1           | Outer frame padding          |
| `border_color`          | str  | None        | Outer border color           |
| `title_color`           | str  | None        | Outer title color            |
| `border_gradient_start` | str  | None        | Outer gradient start         |
| `border_gradient_end`   | str  | None        | Outer gradient end           |
| `gap`                   | int  | 1           | Lines between inner frames   |
| `inherit_style`         | bool | False       | Inner frames inherit style   |
| `align_widths`          | bool | False       | Make inner frames same width |

#### When to Use Which API

| Scenario                      | Recommended API        |
| ----------------------------- | ---------------------- |
| Dynamic content, nesting      | `console.group()`      |
| Simple, data-driven layouts   | `frame_group()`        |
| Complex gradient compositions | `render_frame()`       |
| Embedding in outer frames     | `render_frame_group()` |

### Future Plans

- **Horizontal layout**: Side-by-side frames
- **Grid layout**: Matrix arrangement
- **Composite pattern**: `frame()` returning renderables for arbitrary nesting

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

## Themes

> **New in v0.8.0**

StyledConsole includes a powerful theming engine that ensures consistency across your application.

### Using Themes

```python
from styledconsole import Console, THEMES

# Apply a predefined theme
console = Console(theme=THEMES.MONOKAI)
console.frame("Content matches the theme!", title="Themed Output")
```

### Available Themes

| Theme         | Primary             | Secondary          | Success           | Style Description                            |
| :------------ | :------------------ | :----------------- | :---------------- | :------------------------------------------- |
| **DARK**      | 🟦 `cyan`           | 🟪 `magenta`       | 🟩 `bright_green` | Standard high-contrast dark mode             |
| **LIGHT**     | 🟦 `blue`           | 🟪 `magenta`       | 🟩 `green`        | Clean light mode for white terminals         |
| **MONOKAI**   | 🟪 `magenta`        | 🟦 `bright_blue`   | 🟩 `green`        | Classic IDE theme, retro feel                |
| **NORD**      | 🟦 `bright_blue`    | 🟪 `magenta`       | 🟩 `green`        | Cool arctic blue palette, soft contrast      |
| **DRACULA**   | 🟪 `bright_magenta` | 🟪 `purple`        | 🟩 `green`        | Vignette-style dark theme with high contrast |
| **SOLARIZED** | 🟦 `cyan`           | � `green`          | 🟩 `green`        | Precision colors designed for eye comfort    |
| **FIRE**      | 🟥 `red`            | 🟧 `orange3`       | 🟨 `yellow`       | 🔥 Intense gradients for critical alerts     |
| **SUNNY**     | 🟨 `gold3`          | 🟧 `orange1`       | 🟩 `bright_green` | ☀️ Warm, positive, high-energy vibes         |
| **RAINBOW**   | 🟪 `magenta`        | 🟦 `cyan`          | 🟩 `bright_green` | 🌈 Animated full-spectrum gradients          |
| **OCEAN**     | 🟦 `blue`           | 🟦 `cyan`          | 🟩 `green`        | 🌊 Deep blue monochromatic gradients         |
| **SUNSET**    | 🟥 `red`            | � `magenta`        | 🟩 `bright_green` | 🌅 Warm red-to-yellow gradient transitions   |
| **NEON**      | � `bright_green`    | � `bright_magenta` | 🟩 `bright_green` | ⚡ Cyberpunk aesthetic with high saturation  |

### Themed Progress Bars

Progress bars automatically adapt to your chosen theme, with a special "Dual-mode" behavior:

1. **Default Console (No Theme)**:

   - **Behavior**: Classic "Green Means Go".
   - **Color**: Green bar for both running and finished states.

1. **Themed Console (e.g., FIRE)**:

   - **Behavior**: Fully immersive theming.
   - **Color**: Uses the theme's **Primary** color (e.g., Red for Fire) for *both* running and finished states, ensuring the aesthetic is preserved.
   - **Components**: Spinners, percent text, and steps are all colored to match the theme.

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

## Emojis

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

### Unsupported: ZWJ Sequences

ZWJ (Zero Width Joiner) sequences break alignment:

| Don't Use         | Use Instead  | Constant                    |
| ----------------- | ------------ | --------------------------- |
| 👨‍👩‍👧 (Family)       | 👥 (People)  | `EMOJI.BUSTS_IN_SILHOUETTE` |
| 👩‍💻 (Technologist) | 💻 (Laptop)  | `EMOJI.LAPTOP`              |
| 🏳️‍🌈 (Rainbow Flag) | 🌈 (Rainbow) | `EMOJI.RAINBOW`             |

______________________________________________________________________

## Icons & Terminal Fallback

While `EMOJI` provides raw Unicode emojis, the `icons` module provides **policy-aware icons** that automatically fall back to colored ASCII in terminals that don't support emoji.

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

______________________________________________________________________

## Render Policy

**RenderPolicy** is the central control mechanism for adapting output to different terminal environments. It automatically detects terminal capabilities and adjusts rendering accordingly.

### Why Use RenderPolicy?

StyledConsole is **policy-aware** throughout the entire rendering pipeline:

- **Colors**: Skipped when `policy.color=False`
- **Unicode borders**: Falls back to ASCII when `policy.unicode=False`
- **Emojis**: Uses colored ASCII fallback when `policy.emoji=False`
- **Gradients**: Plain text when colors disabled
- **Progress bars**: Text-based fallback without cursor control

### Automatic Detection

By default, Console auto-detects the best policy from the environment:

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
    f"{icons.CHECK} All tests passed\n{icons.ROCKET} Deploying...",
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

## Presets

Presets are pre-built, high-level components for common CLI patterns.

> **💡 Policy-Aware**: All presets respect the Console's render policy. They use the
> `icons` module for symbols, so they degrade gracefully in CI/CD environments,
> SSH sessions, and terminals without emoji support.

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
