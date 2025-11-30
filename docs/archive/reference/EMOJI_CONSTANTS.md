# Emoji Constants Reference

**Added:** v0.3.1
**Module:** `styledconsole.emojis`

## Overview

StyledConsole provides named constants for all supported emojis, making your code more readable and maintainable.

## Quick Start

```python
from styledconsole import Console, EMOJI, E

console = Console()

# Use full name
console.frame("Success!", title=f"{EMOJI.CHECK} Complete")

# Or short alias
console.text(f"{E.ROCKET} Launching...")
```

## Why Use Emoji Constants?

### ❌ Before (Raw UTF-8)

```python
console.frame("Done!", title="✅ Complete")  # Hard to read
console.text("🚀 Deploying...")  # Can't search/autocomplete
```

### ✅ After (Named Constants)

```python
console.frame("Done!", title=f"{EMOJI.CHECK} Complete")  # Readable!
console.text(f"{E.ROCKET} Deploying...")  # IDE autocomplete works!
```

## Benefits

1. **Readable** - `E.CHECK` is clearer than `✅` in source code
1. **Discoverable** - IDE autocomplete shows all available emojis
1. **Searchable** - `grep "EMOJI.ROCKET"` finds all rocket emojis
1. **Maintainable** - Change emoji in one place
1. **Safe** - Only Tier 1 (tested, safe) emojis included

## Usage Patterns

### Basic Usage

```python
from styledconsole import EMOJI

# Status indicators
print(f"{EMOJI.CHECK} Build successful")
print(f"{EMOJI.CROSS} Test failed")
print(f"{EMOJI.WARNING} High memory usage")
print(f"{EMOJI.INFO} Backup completed")
```

### In Frames

```python
console.frame(
    "Deployment complete!",
    title=f"{EMOJI.ROCKET} Deploy",
    border="rounded"
)
```

### Helper Methods

```python
# Convenience methods for common patterns
title = EMOJI.success("Deployed")   # "✅ Deployed"
error = EMOJI.error("Failed")       # "❌ Failed"
warn = EMOJI.warning("Careful")     # "⚠️ Careful"
info = EMOJI.info("Note")           # "ℹ️ Note"
```

### Short Alias

```python
from styledconsole import E  # Ultra-short alias

print(f"{E.FIRE} Hot take")
print(f"{E.SPARKLES} New feature")
```

## Available Categories

### Status & Indicators

- `CHECK` ✅ - Success, completion
- `CROSS` ❌ - Error, failure
- `WARNING` ⚠️ - Caution, warning
- `INFO` ℹ️ - Information, note

### Colored Circles

- `RED_CIRCLE` 🔴
- `YELLOW_CIRCLE` 🟡
- `GREEN_CIRCLE` 🟢
- `BLUE_CIRCLE` 🔵
- `PURPLE_CIRCLE` 🟣
- `ORANGE_CIRCLE` 🟠

### Technology & Tools

- `COMPUTER` / `LAPTOP` 💻
- `ROCKET` 🚀
- `GEAR` ⚙️
- `WRENCH` 🔧
- `HAMMER` 🔨
- `TEST_TUBE` 🧪

### Charts & Documents

- `CHART_BAR` 📊
- `CHART_INCREASING` 📈
- `CHART_DECREASING` 📉
- `PACKAGE` 📦

### Files & Folders

- `FOLDER` 📁 - Closed folder
- `OPEN_FOLDER` 📂 - Open folder
- `FILE_CABINET` 🗄 - Storage cabinet
- `CARD_FILE_BOX` 🗃 - File box
- `WASTEBASKET` 🗑 - Trash/recycle bin

### Documents & Papers

- `FILE` / `PAGE` 📄 - Generic file
- `DOCUMENT` 📃 - Document page
- `SCROLL` 📜 - Scroll/certificate
- `MEMO` 📝 - Memo with pencil
- `CLIPBOARD` 📋 - Clipboard
- `PUSHPIN` 📌 - Pin
- `PAPERCLIP` 📎 - Attachment
- `BOOKMARK` 🔖 - Bookmark ribbon
- `LABEL` 🏷 - Tag/label
- `CARD_INDEX` 📇 - Card index

### Books & Reading

- `BOOK` 📖 - Open book
- `BOOKS` 📚 - Stack of books
- `NOTEBOOK` 📓 - Notebook
- `LEDGER` 📒 - Ledger
- `CLOSED_BOOK` 📕 - Red closed book
- `GREEN_BOOK` 📗 - Green book
- `BLUE_BOOK` 📘 - Blue book
- `ORANGE_BOOK` 📙 - Orange book

### News & Media

- `NEWSPAPER` 📰 - Newspaper
- `ROLLED_NEWSPAPER` 🗞 - Rolled newspaper

### Stars & Celebration

- `STAR` ⭐
- `SPARKLES` ✨
- `PARTY` 🎉
- `CONFETTI` 🎊
- `TROPHY` 🏆
- `FIRE` 🔥

### Nature & Weather

- `RAINBOW` 🌈
- `LIGHTNING` ⚡
- `FIRE` 🔥
- `DROPLET` 💧
- `SNOWFLAKE` ❄️

### Transportation

- `ROCKET` 🚀
- `AIRPLANE` ✈️
- `CAR` 🚗
- `BIKE` 🚲

### Currency

- `DOLLAR` 💵
- `MONEY_BAG` 💰
- `GEM` / `DIAMOND` 💎

**Full list:** See `src/styledconsole/emojis.py` (100+ emojis)

## Real-World Examples

### CLI Status Messages

```python
from styledconsole import Console, EMOJI

console = Console()

# Success
console.frame(
    "All tests passed!",
    title=f"{EMOJI.CHECK} Test Results",
    border_color="green"
)

# Error
console.frame(
    "Connection timeout",
    title=f"{EMOJI.CROSS} Database Error",
    border_color="red"
)

# Warning
console.frame(
    "Memory usage: 85%",
    title=f"{EMOJI.WARNING} Resource Alert",
    border_color="yellow"
)
```

### Deployment Workflow

```python
# Starting
console.text(f"{EMOJI.ROCKET} Initiating deployment...")

# Progress
console.text(f"{EMOJI.PACKAGE} Building artifacts...")
console.text(f"{EMOJI.TEST_TUBE} Running tests...")

# Success
console.frame(
    "Version 2.1.0 deployed",
    title=f"{EMOJI.CHECK} Deploy Complete",
    border="double",
    border_color="lime"
)
```

### Dashboard Panels

```python
# Service status
console.frame(
    "CPU: 45% | Memory: 2.1GB",
    title=f"{EMOJI.GREEN_CIRCLE} API Server",
    border="rounded"
)

console.frame(
    "Queue: 1,234 pending",
    title=f"{EMOJI.YELLOW_CIRCLE} Worker Pool",
    border="rounded"
)
```

## Design Guidelines

### ✅ Do

- Use consistent emoji + color pairings
- Match emoji to message context
- Use `E.` for brevity in code
- Leverage helper methods (`EMOJI.success()`)

### ❌ Don't

- Mix emoji styles inconsistently
- Use emojis for every word (overwhelming)
- Assume all terminals render emojis (check capabilities)
- Use unsupported emojis (stick to provided constants)

## Compatibility

All emojis in `EMOJI` are:

- ✅ **Tier 1** - Simple, single-codepoint emojis
- ✅ **Width-safe** - Correct visual width calculation
- ✅ **Terminal-safe** - Work across major terminals
- ❌ **No ZWJ sequences** - Complex emojis excluded

See `doc/guides/EMOJI_SUPPORT.md` for technical details on emoji support.

## IDE Support

### VS Code

- Full autocomplete after typing `EMOJI.`
- Type hints show emoji character
- Go-to-definition works

### PyCharm

- Autocomplete with emoji preview
- Quick documentation shows character
- Find usages works perfectly

## API Reference

### Main Classes

```python
class EmojiConstants:
    """Container for all emoji constants."""

    # Status
    CHECK: Final[str] = "✅"
    CROSS: Final[str] = "❌"
    WARNING: Final[str] = "⚠️"
    INFO: Final[str] = "ℹ️"

    # ... (100+ more)

    @staticmethod
    def success(text: str = "") -> str:
        """Return check mark with optional text."""

    @staticmethod
    def error(text: str = "") -> str:
        """Return cross mark with optional text."""

    @staticmethod
    def warning(text: str = "") -> str:
        """Return warning sign with optional text."""

    @staticmethod
    def info(text: str = "") -> str:
        """Return info symbol with optional text."""
```

### Imports

```python
from styledconsole import EMOJI      # Full name
from styledconsole import E          # Short alias
from styledconsole.emojis import EmojiConstants  # Class
```

## Migration from Raw Emojis

### Search & Replace Pattern

```bash
# Find all raw emojis in your code
grep -r "✅\|❌\|⚠️\|ℹ️" examples/

# Replace with constants (manual or script)
sed -i 's/"✅/"f"{EMOJI.CHECK}/g' file.py
```

### Gradual Migration

You can mix raw emojis and constants:

```python
# Works fine
print("✅ Old way")
print(f"{EMOJI.CHECK} New way")
```

## Testing

Emoji constants are fully tested:

```python
from styledconsole import EMOJI

assert EMOJI.CHECK == "✅"
assert EMOJI.success("Done") == "✅ Done"
```

See `tests/unit/test_emojis.py` for 21 comprehensive tests.

______________________________________________________________________

**See also:**

- `doc/guides/EMOJI_SUPPORT.md` - Emoji support guide
- `examples/usecases/alerts.py` - Real-world usage examples
- `src/styledconsole/emojis.py` - Full source code
