# StyledConsole Developer Guide

**Version:** 0.5.0
**Last Updated:** November 30, 2025
**Audience:** Contributors and advanced users

______________________________________________________________________

## Table of Contents

1. [Architecture Overview](#architecture-overview)
1. [Module Structure](#module-structure)
1. [Core Components](#core-components)
1. [Extending the Library](#extending-the-library)
1. [API Reference](#api-reference)
1. [Testing](#testing)
1. [Code Style](#code-style)

______________________________________________________________________

## Architecture Overview

### System Layers

```text
┌─────────────────────────────────────────────────────────┐
│                  User Application                       │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │   Console API           │  ← Public facade
        │   (console.py)          │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │   Rendering Engine      │  ← Orchestrates rendering
        │   (rendering_engine.py) │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │   Rich Backend          │  ← ANSI rendering
        │   (Panel, Text, Group)  │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │   Terminal/HTML Export  │  ← Output targets
        └─────────────────────────┘
```

### Data Flow

```text
Console.frame(content, title, border)
  ↓
RenderingEngine.print_frame()
  ↓
box_mapping.get_box_style(border)  → Rich Box
  ↓
Rich Panel(content, box=box)
  ↓
rich_console.print()  → Terminal
  ↓
ExportManager.export_html()  → HTML (if recording)
```

### Design Patterns

| Pattern      | Usage                                     |
| ------------ | ----------------------------------------- |
| **Facade**   | `Console` class wraps managers            |
| **Strategy** | Gradient engine (position, color, target) |
| **Adapter**  | `box_mapping.py` adapts borders to Rich   |

______________________________________________________________________

## Module Structure

```text
src/styledconsole/
├── __init__.py                   # Public exports
├── console.py                    # Console facade (main API)
├── emojis.py                     # EMOJI constants (100+)
├── types.py                      # Type aliases
├── animation.py                  # Animation runner
│
├── core/                         # Core rendering
│   ├── box_mapping.py            # Border → Rich Box mapping
│   ├── rendering_engine.py       # Rich Panel coordinator
│   ├── banner.py                 # ASCII art (pyfiglet)
│   ├── gradient_utils.py         # Gradient application
│   ├── styles.py                 # Border style definitions
│   ├── export_manager.py         # HTML export
│   └── terminal_manager.py       # Terminal detection
│
├── effects/                      # Gradient effects (v0.4.0)
│   ├── engine.py                 # Unified apply_gradient()
│   └── strategies.py             # Strategy classes
│
├── presets/                      # High-level presets
│   ├── status.py                 # status_frame()
│   ├── summary.py                # test_summary()
│   └── dashboard.py              # dashboard layouts
│
└── utils/                        # Utilities
    ├── text.py                   # Emoji-safe width calculation
    ├── color.py                  # Color parsing & gradients
    ├── terminal.py               # Terminal capabilities
    ├── validation.py             # Input validation
    └── wrap.py                   # Text wrapping
```

______________________________________________________________________

## Core Components

### Console (Facade)

The main entry point. Delegates to specialized managers.

```python
class Console:
    def __init__(self, record=False, width=None, detect_terminal=True, debug=False):
        self._rich_console = RichConsole(record=record, width=width)
        self._terminal_manager = TerminalManager() if detect_terminal else None
        self._rendering_engine = RenderingEngine(self._rich_console)
        self._export_manager = ExportManager(self._rich_console)
```

**Public Methods:**

- `frame()` - Render bordered frame
- `banner()` - Render ASCII art banner
- `text()` - Print styled text
- `rule()` - Print horizontal rule
- `newline()` - Print blank line
- `clear()` - Clear screen
- `export_html()` - Export to HTML
- `export_text()` - Export plain text

### RenderingEngine

Orchestrates Rich-native rendering.

```python
class RenderingEngine:
    def print_frame(self, content, title, border, colors, gradients, ...):
        box = get_box_style(border)
        panel = Panel(content, title=title, box=box, ...)
        self._console.print(panel)
```

### Gradient Engine (Strategy Pattern)

Located in `effects/engine.py` and `effects/strategies.py`.

```python
def apply_gradient(
    lines: list[str],
    position_strategy: PositionStrategy,
    color_source: ColorSource,
    target_filter: TargetFilter,
    border_chars: set[str],
) -> list[str]:
    ...
```

**Position Strategies:**

- `VerticalPosition` - Top (0.0) → Bottom (1.0)
- `HorizontalPosition` - Left (0.0) → Right (1.0)
- `DiagonalPosition` - Top-left → Bottom-right
- `OffsetPositionStrategy` - Adds offset for animation

**Color Sources:**

- `LinearGradient(start, end)` - Two-color interpolation
- `RainbowSpectrum()` - 7-color ROYGBIV

**Target Filters:**

- `ContentOnly` - Skip border characters
- `BorderOnly` - Skip content characters
- `Both` - Color everything

### Text Utilities

Located in `utils/text.py`. Critical for emoji support.

```python
# Visual width (emoji-aware)
visual_width("✅")  # Returns 2
visual_width("⚠️")  # Returns 1 (VS16 corrected)

# Spacing adjustment
adjust_emoji_spacing_in_text("⚠️ Warning")  # "⚠️  Warning"

# Validation
validate_emoji("👨‍💻")  # {"safe": False, "reason": "ZWJ sequence"}
```

### Color Utilities

Located in `utils/color.py`.

```python
# Parse any color format
parse_color("dodgerblue")      # (30, 144, 255)
parse_color("#1E90FF")         # (30, 144, 255)
parse_color((30, 144, 255))    # (30, 144, 255)

# Gradient interpolation
interpolate_color("red", "blue", 0.5)  # Midpoint hex
```

______________________________________________________________________

## Extending the Library

### Adding a Position Strategy

```python
# In effects/strategies.py
class RadialPosition:
    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        center_row = total_rows / 2
        center_col = total_cols / 2
        distance = math.sqrt((row - center_row)**2 + (col - center_col)**2)
        max_distance = math.sqrt(center_row**2 + center_col**2)
        return min(distance / max_distance, 1.0)
```

### Adding a Color Source

```python
class FirePalette:
    def get_color(self, position: float) -> str:
        # Map 0.0-1.0 to yellow → orange → red → black
        colors = ["#FFFF00", "#FF8000", "#FF0000", "#400000"]
        ...
```

### Adding a Border Style

```python
# In core/styles.py
FIRE = BorderStyle(
    name="fire",
    top_left="🔥", top_right="🔥",
    bottom_left="🔥", bottom_right="🔥",
    horizontal="═", vertical="║"
)
BORDERS["fire"] = FIRE

# In core/box_mapping.py
def get_box_style(name: str) -> Box:
    mapping = {
        ...
        "fire": box.DOUBLE,  # Map to closest Rich box
    }
```

______________________________________________________________________

## API Reference

### Console.frame()

```python
def frame(
    self,
    content: str | list[str],
    title: str | None = None,
    border: str = "solid",
    width: int | None = None,
    padding: int = 1,
    align: Literal["left", "center", "right"] = "left",
    content_color: ColorType | None = None,
    border_color: ColorType | None = None,
    title_color: ColorType | None = None,
    border_gradient_start: ColorType | None = None,
    border_gradient_end: ColorType | None = None,
) -> None
```

### Console.banner()

```python
def banner(
    self,
    text: str,
    font: str = "standard",
    start_color: ColorType | None = None,
    end_color: ColorType | None = None,
    border: str | None = None,
    width: int | None = None,
    align: Literal["left", "center", "right"] = "center",
    padding: int = 1,
) -> None
```

### Console.text()

```python
def text(
    self,
    text: str,
    color: ColorType | None = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    dim: bool = False,
    end: str = "\n",
) -> None
```

### Type Aliases

```python
ColorType = str | tuple[int, int, int]
AlignType = Literal["left", "center", "right"]
```

______________________________________________________________________

## Testing

### Running Tests

```bash
# All tests with coverage
uv run pytest --cov=src/styledconsole --cov-report=html

# Specific file
uv run pytest tests/unit/test_frame.py -v

# Run examples
uv run python examples/run_all.py
```

### Test Structure

```text
tests/
├── unit/           # Isolated component tests
├── integration/    # Cross-component tests
└── snapshots/      # Visual regression tests
```

### Writing Tests

```python
def test_frame_with_emoji():
    console = Console(record=True, width=80)
    console.frame("✅ Success", title="Status")
    output = console.export_text()
    assert "✅" in output
    assert "Status" in output
```

### Snapshot Testing

```python
def test_frame_visual(snapshot):
    console = Console(record=True, width=60)
    console.frame("Test", border="rounded")
    assert console.export_text() == snapshot

# Update snapshots: pytest --snapshot-update
```

______________________________________________________________________

## Code Style

### Principles

1. **Type hints everywhere** - All public APIs fully typed
1. **Docstrings with examples** - Every public function documented
1. **Single Responsibility** - Keep modules under 200 lines
1. **Test everything** - Maintain 95%+ coverage

### Formatting

```bash
# Lint
uv run ruff check src/ tests/

# Format
uv run ruff format src/ tests/
```

### Commit Messages

```text
feat(frame): Add gradient border support
fix(emoji): Correct VS16 width calculation
docs: Update USER_GUIDE with examples
test: Add snapshot tests for banners
refactor(engine): Extract color normalization
```

______________________________________________________________________

## Appendix: CSS4 Colors

148 named colors supported. Common ones:

| Category | Colors                                       |
| -------- | -------------------------------------------- |
| Reds     | `red`, `crimson`, `indianred`, `darkred`     |
| Blues    | `blue`, `dodgerblue`, `royalblue`, `navy`    |
| Greens   | `green`, `lime`, `limegreen`, `forestgreen`  |
| Yellows  | `yellow`, `gold`, `orange`, `darkorange`     |
| Grays    | `gray`, `silver`, `darkgray`, `lightgray`    |
| Others   | `cyan`, `magenta`, `purple`, `pink`, `coral` |

Full list: See `src/styledconsole/utils/color_data.py`

______________________________________________________________________

## Appendix: EMOJI Constants

100+ constants in `src/styledconsole/emojis.py`:

| Category   | Examples                                    |
| ---------- | ------------------------------------------- |
| Status     | `CHECK`, `CROSS`, `WARNING`, `INFO`         |
| Circles    | `RED_CIRCLE`, `GREEN_CIRCLE`, `BLUE_CIRCLE` |
| Stars      | `STAR`, `SPARKLES`, `FIRE`, `LIGHTNING`     |
| Tech       | `LAPTOP`, `GEAR`, `WRENCH`, `PACKAGE`       |
| Activities | `ROCKET`, `TARGET`, `TROPHY`, `PARTY`       |

Full list: See `src/styledconsole/emojis.py`
