# Emoji Support in StyledConsole

**Purpose:** Complete guide to emoji usage in StyledConsole
**Audience:** Developers using emoji features
**Status:** Active (v0.4.0)
**Last Updated:** November 30, 2025

______________________________________________________________________

## Overview

StyledConsole provides robust emoji support with automatic width handling. Use the `EMOJI` constants for guaranteed compatibility across all features (frames, banners, gradients).

**What works:**

- ✅ Standard emojis (single codepoint)
- ✅ VS16 emojis (auto-adjusted width)
- ⚠️ Skin tones (terminal-dependent)
- ❌ ZWJ sequences (not supported)

______________________________________________________________________

## Quick Start

```python
from styledconsole import Console, EMOJI

console = Console()

# Use EMOJI constants for guaranteed compatibility
console.frame(
    f"{EMOJI.CHECK} Build successful\n{EMOJI.ROCKET} Deployed to production",
    title=f"{EMOJI.SPARKLES} Status"
)
```

Output:

```text
┌─────────────── ✨ Status ───────────────┐
│ ✅ Build successful                     │
│ 🚀 Deployed to production               │
└─────────────────────────────────────────┘
```

______________________________________________________________________

## Quick Reference

| Emoji Type      | Support   | Example        | Notes                       |
| --------------- | --------- | -------------- | --------------------------- |
| Standard emojis | ✅ Full   | ✅ ❌ 🚀 💡 🎉 | Single codepoint, width 2   |
| VS16 emojis     | ✅ Full   | ⚠️ ℹ️ ⚙️ ⏱️    | Auto-adjusted to width 1    |
| Skin tones      | ⚠️ Varies | 👍🏽 👋🏻          | May break in some terminals |
| ZWJ sequences   | ❌ None   | 👨‍💻 👨‍👩‍👧          | Renders as multiple emojis  |
| Flags           | ⚠️ Varies | 🇺🇸 🇬🇧          | Terminal-dependent          |

______________________________________________________________________

## Using EMOJI Constants

### Import

```python
from styledconsole import EMOJI      # Recommended
from styledconsole.emojis import E   # Short alias
```

### Categories

StyledConsole provides **100+ pre-validated emoji constants** organized by category:

#### Status & Indicators

```python
EMOJI.CHECK         # ✅  Success
EMOJI.CROSS         # ❌  Failure
EMOJI.WARNING       # ⚠️  Warning (VS16)
EMOJI.INFO          # ℹ️  Information (VS16)
EMOJI.QUESTION      # ❓  Question
EMOJI.REFRESH       # 🔄  Refresh/reload
```

#### Colored Circles

```python
EMOJI.RED_CIRCLE    # 🔴  Error/critical
EMOJI.YELLOW_CIRCLE # 🟡  Warning/pending
EMOJI.GREEN_CIRCLE  # 🟢  Success/online
EMOJI.BLUE_CIRCLE   # 🔵  Info/neutral
EMOJI.PURPLE_CIRCLE # 🟣  Special
EMOJI.ORANGE_CIRCLE # 🟠  Caution
```

#### Stars & Highlights

```python
EMOJI.STAR          # ⭐  Star
EMOJI.SPARKLES      # ✨  Sparkles
EMOJI.FIRE          # 🔥  Fire/hot
EMOJI.LIGHTNING     # ⚡  Lightning/fast
EMOJI.GLOWING_STAR  # 🌟  Glowing star
```

#### Technology

```python
EMOJI.LAPTOP        # 💻  Computer
EMOJI.GEAR          # ⚙️  Settings (VS16)
EMOJI.WRENCH        # 🔧  Tools
EMOJI.TEST_TUBE     # 🧪  Testing
EMOJI.CHART_BAR     # 📊  Charts
EMOJI.PACKAGE       # 📦  Package
EMOJI.FOLDER        # 📁  Folder
EMOJI.FILE          # 📄  File
```

#### Activities

```python
EMOJI.ROCKET        # 🚀  Launch/deploy
EMOJI.TARGET        # 🎯  Goal/target
EMOJI.TROPHY        # 🏆  Achievement
EMOJI.PARTY         # 🎉  Celebration
EMOJI.GIFT          # 🎁  Gift/reward
EMOJI.ART           # 🎨  Creative
```

#### Navigation

```python
EMOJI.ARROW_RIGHT   # →   Right arrow
EMOJI.ARROW_LEFT    # ←   Left arrow
EMOJI.ARROW_UP      # ↑   Up arrow
EMOJI.ARROW_DOWN    # ↓   Down arrow
EMOJI.HEAVY_RIGHT   # ➡   Heavy right arrow
```

#### Symbols

```python
EMOJI.LIGHTBULB     # 💡  Idea
EMOJI.LOCK          # 🔒  Locked/secure
EMOJI.KEY           # 🔑  Key/access
EMOJI.LINK          # 🔗  Link
EMOJI.MAG           # 🔍  Search
EMOJI.BELL          # 🔔  Notification
```

### Helper Methods

```python
# Quick status messages
EMOJI.success("Build complete")   # "✅ Build complete"
EMOJI.error("Test failed")        # "❌ Test failed"
EMOJI.warning("Deprecated")       # "⚠️ Deprecated"
EMOJI.info("Version 2.0")         # "ℹ️ Version 2.0"
```

______________________________________________________________________

## Supported Emojis

### Standard Emojis (Full Support)

Single-codepoint emojis work perfectly with all features:

```text
Status:    ✅ ❌ ⭕ 🔴 🟡 🟢 🔵 🟣 🟠 ⚫ ⚪
Effects:   ⭐ ✨ 💫 🌟 ⚡ 🔥 💥
Tech:      💻 🖥 📱 💾 📦 📁 📂 📄 📝 🔧 🔨 🧪 🔬 📊 📈 📉
Common:    🚀 🎯 🎨 🎉 🎊 🎁 🏆 💎 👍 👎 👋 👥 👤
```

### VS16 Emojis (Auto-Adjusted)

VS16 (Variation Selector-16) emojis are fully supported with automatic width correction:

```text
⚠️ ℹ️ ⚙️ ⏱️ ⏸️ ⏹️ ⏺️ ▶️ ◀️ ☀️ ❄️ ☁️ ✈️ ❤️ ✉️ ☎️
```

**How it works:**

- VS16 emojis render as width 1 (not 2) in terminals
- Library detects VS16 and adds compensating space automatically
- No manual adjustment needed

______________________________________________________________________

## Unsupported Emojis

### ZWJ Sequences

**ZWJ (Zero Width Joiner) sequences cannot be supported.**

ZWJ combines multiple emojis into composite glyphs:

| Sequence | Components               | Problem                      |
| -------- | ------------------------ | ---------------------------- |
| 👨‍💻       | 👨 + ZWJ + 💻            | Renders as 👨💻 (2 emojis)   |
| 👨‍👩‍👧       | 👨 + ZWJ + 👩 + ZWJ + 👧 | Renders as 👨👩👧 (3 emojis) |
| 🏳️‍🌈       | 🏳️ + ZWJ + 🌈            | Renders as 🏳️🌈 (2 emojis)   |

This breaks frame alignment because width calculation expects 1 emoji but terminal renders multiple.

### Simple Alternatives

| Don't Use         | Use Instead  | Constant        |
| ----------------- | ------------ | --------------- |
| 👨‍👩‍👧 (Family)       | 👥 (People)  | `EMOJI.PEOPLE`  |
| 👩‍💻 (Technologist) | 💻 (Laptop)  | `EMOJI.LAPTOP`  |
| 🏳️‍🌈 (Rainbow Flag) | 🌈 (Rainbow) | `EMOJI.RAINBOW` |

______________________________________________________________________

## Common Patterns

### Status Indicators

```python
from styledconsole import Console, EMOJI

console = Console()

# Test results
results = [
    f"{EMOJI.CHECK} test_login - passed",
    f"{EMOJI.CHECK} test_signup - passed",
    f"{EMOJI.CROSS} test_payment - failed",
    f"{EMOJI.WARNING} test_cache - skipped",
]

console.frame("\n".join(results), title=f"{EMOJI.TEST_TUBE} Test Results")
```

### Dashboard Headers

```python
# Section headers with emojis
console.banner("METRICS", start_color="cyan", end_color="blue")

console.frame(
    f"{EMOJI.CHART_BAR} CPU: 45%\n{EMOJI.CHART_BAR} Memory: 72%",
    title=f"{EMOJI.GEAR} System Status",
    border="rounded"
)
```

### Progress Indicators

```python
# Use colored circles for status
status = [
    f"{EMOJI.GREEN_CIRCLE} Database: Online",
    f"{EMOJI.GREEN_CIRCLE} API: Online",
    f"{EMOJI.YELLOW_CIRCLE} Cache: Warming",
    f"{EMOJI.RED_CIRCLE} Worker: Offline",
]

console.frame("\n".join(status), title=f"{EMOJI.GLOBE} Services")
```

______________________________________________________________________

## How It Works

### Width Calculation

StyledConsole uses corrected width calculation for all emoji types:

```python
from styledconsole.utils.text import visual_width

visual_width("✅")   # Returns 2 (standard emoji)
visual_width("⚠️")   # Returns 1 (VS16 emoji, corrected)
visual_width("Hello") # Returns 5 (ASCII text)
```

### Automatic Spacing

The library adds compensating space after VS16 emojis:

```python
from styledconsole.utils.text import adjust_emoji_spacing_in_text

adjust_emoji_spacing_in_text("⚠️ Warning")  # "⚠️  Warning" (extra space)
adjust_emoji_spacing_in_text("✅ Done")     # "✅ Done" (unchanged)
```

### Result: Perfect Alignment

```text
┌──────────────────────────────┐
│ ✅ PASS   │ Test completed   │  ← width 2 + 1 space
│ ⚠️  SKIP  │ Not implemented  │  ← width 1 + 2 spaces
│ ❌ FAIL   │ Assertion error  │  ← width 2 + 1 space
└──────────────────────────────┘
```

______________________________________________________________________

## API Reference

### validate_emoji()

Check if an emoji is safe to use:

```python
from styledconsole.utils.text import validate_emoji

result = validate_emoji("✅")
print(result["safe"])      # True
print(result["width"])     # 2

result = validate_emoji("👨‍💻")
print(result["safe"])      # False (ZWJ sequence)
print(result["reason"])    # "ZWJ sequence detected"
```

### visual_width()

Get the display width of any string:

```python
from styledconsole.utils.text import visual_width

visual_width("🚀 Launch")  # 9 (emoji=2, space=1, text=6)
visual_width("⚠️ Alert")   # 8 (emoji=1, space=1, text=5, +1 auto)
```

______________________________________________________________________

## Terminal Compatibility

### Recommended Terminals

| Terminal               | Emoji Support | Notes               |
| ---------------------- | ------------- | ------------------- |
| **iTerm2** (macOS)     | ✅ Excellent  | Full emoji support  |
| **Windows Terminal**   | ✅ Excellent  | Windows 10+         |
| **Kitty**              | ✅ Excellent  | Linux               |
| **Alacritty**          | ✅ Good       | Cross-platform      |
| **VS Code Terminal**   | ✅ Good       | Built-in terminal   |
| **GNOME Terminal**     | ⚠️ Good       | Some width issues   |
| **macOS Terminal.app** | ⚠️ Basic      | Limited emoji fonts |

### Recommended Fonts

For best emoji rendering, use a font with emoji support:

- **JetBrains Mono** + system emoji fallback
- **Fira Code** + system emoji fallback
- **Nerd Fonts** (any variant)

______________________________________________________________________

## Troubleshooting

### Emoji appears "glued" to text

**Symptom:** `⚙️Services` instead of `⚙️ Services`

**Cause:** VS16 emoji width mismatch (older library versions)

**Solution:** Update to v0.3.0+ (automatic spacing handles this)

### Frame borders are misaligned

**Symptom:** Right border is offset by 2-4 characters

**Cause:** ZWJ sequence in title or content

**Solution:** Replace ZWJ emoji with simple alternative (see table above)

### Emoji shows as boxes or question marks

**Symptom:** `□` or `?` instead of emoji

**Cause:** Terminal font doesn't support emoji

**Solution:**

1. Use a terminal from the recommended list
1. Install a Nerd Font or font with emoji support
1. Check terminal emoji rendering settings

### Different emojis have inconsistent spacing

**Symptom:** Some emojis align, others don't

**Cause:** Mixing VS16 and standard emojis without using constants

**Solution:** Use `EMOJI` constants consistently—they handle all width variations

______________________________________________________________________

## Version History

| Version | Date          | Changes                                                 |
| ------- | ------------- | ------------------------------------------------------- |
| v0.4.0  | November 2025 | Strategy pattern for gradients, improved emoji handling |
| v0.3.0  | November 2025 | Full VS16 support with automatic spacing                |
| v0.1.0  | October 2025  | Basic Tier 1 emoji support                              |

______________________________________________________________________

## See Also

- **Examples:** `examples/gallery/emojis_showcase.py`
- **Source:** `src/styledconsole/emojis.py` (100+ constants)
- **Reference:** `doc/reference/EMOJI_CONSTANTS.md` (full constant list)
