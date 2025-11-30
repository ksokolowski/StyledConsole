# StyledConsole Developer Guide

**Version:** 0.6.0
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

```mermaid
flowchart TB
    subgraph User["User Application"]
        APP[Application Code]
    end

    subgraph Facade["Public API Layer"]
        CONSOLE[Console<br/>console.py]
    end

    subgraph Managers["Manager Layer"]
        RE[RenderingEngine]
        EM[ExportManager]
        TM[TerminalManager]
    end

    subgraph Core["Core Layer"]
        BM[box_mapping]
        GU[gradient_utils]
        ST[styles]
        BN[banner]
    end

    subgraph Effects["Effects Layer"]
        ENG[engine.py]
        STR[strategies.py]
    end

    subgraph Utils["Utilities Layer"]
        TXT[text.py]
        CLR[color.py]
        WRP[wrap.py]
        TRM[terminal.py]
    end

    subgraph Backend["Rich Backend"]
        RICH[Rich Console<br/>Panel, Text, Group]
    end

    APP --> CONSOLE
    CONSOLE --> RE
    CONSOLE --> EM
    CONSOLE --> TM
    RE --> BM
    RE --> GU
    RE --> ST
    RE --> BN
    RE --> ENG
    ENG --> STR
    RE --> TXT
    RE --> CLR
    RE --> WRP
    TM --> TRM
    RE --> RICH
    EM --> RICH

    style CONSOLE fill:#4CAF50,color:#fff
    style RICH fill:#673AB7,color:#fff
```

### Data Flow: Frame Rendering

```mermaid
sequenceDiagram
    participant App as Application
    participant Con as Console
    participant RE as RenderingEngine
    participant BM as box_mapping
    participant Rich as Rich Console

    App->>Con: frame(content, title, border)
    Con->>RE: print_frame(...)
    RE->>BM: get_box_style(border)
    BM-->>RE: Rich Box object
    RE->>Rich: Panel(content, box=box)
    Rich->>Rich: render to ANSI
    Rich-->>App: Terminal output
```

### Data Flow: Gradient Application

```mermaid
sequenceDiagram
    participant RE as RenderingEngine
    participant GE as Gradient Engine
    participant PS as PositionStrategy
    participant CS as ColorSource

    RE->>GE: apply_gradient(lines, strategy, colors)
    loop For each character
        GE->>PS: calculate(row, col)
        PS-->>GE: position (0.0-1.0)
        GE->>CS: get_color(position)
        CS-->>GE: hex color
        GE->>GE: wrap char with ANSI
    end
    GE-->>RE: colorized lines
```

### Design Patterns

```mermaid
classDiagram
    class Console {
        <<Facade>>
        +frame()
        +banner()
        +text()
        +export_html()
    }

    class RenderingEngine {
        <<Coordinator>>
        +print_frame()
        +print_banner()
    }

    class PositionStrategy {
        <<Strategy>>
        +calculate() float
    }

    class VerticalPosition {
        +calculate()
    }

    class HorizontalPosition {
        +calculate()
    }

    class DiagonalPosition {
        +calculate()
    }

    class ColorSource {
        <<Strategy>>
        +get_color() str
    }

    class LinearGradient {
        +get_color()
    }

    class RainbowSpectrum {
        +get_color()
    }

    Console --> RenderingEngine
    PositionStrategy <|-- VerticalPosition
    PositionStrategy <|-- HorizontalPosition
    PositionStrategy <|-- DiagonalPosition
    ColorSource <|-- LinearGradient
    ColorSource <|-- RainbowSpectrum
```

| Pattern      | Usage                                     |
| ------------ | ----------------------------------------- |
| **Facade**   | `Console` class wraps managers            |
| **Strategy** | Gradient engine (position, color, target) |
| **Adapter**  | `box_mapping.py` adapts borders to Rich   |

______________________________________________________________________

## Module Structure

### Package Dependency Graph

```mermaid
flowchart LR
    subgraph styledconsole
        INIT[__init__.py]
        CON[console.py]
        EMO[emojis.py]
        TYP[types.py]
        ANI[animation.py]
    end

    subgraph core
        RE[rendering_engine]
        EM[export_manager]
        TM[terminal_manager]
        BM[box_mapping]
        GU[gradient_utils]
        ST[styles]
        BN[banner]
    end

    subgraph effects
        ENG[engine]
        STR[strategies]
    end

    subgraph utils
        TXT[text]
        CLR[color]
        WRP[wrap]
        TRM[terminal]
        VAL[validation]
        ED[emoji_data]
        CD[color_data]
    end

    subgraph presets
        STA[status]
        SUM[summary]
        DSH[dashboard]
    end

    CON --> RE
    CON --> EM
    CON --> TM
    RE --> BM
    RE --> GU
    RE --> ST
    RE --> BN
    RE --> ENG
    ENG --> STR
    TXT --> ED
    CLR --> CD
    STA --> CON
    SUM --> CON
    DSH --> CON

    style CON fill:#4CAF50,color:#fff
    style RE fill:#2196F3,color:#fff
    style ENG fill:#FF9800,color:#fff
```

### Directory Structure

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
    ├── emoji_data.py             # SAFE_EMOJIS dictionary
    ├── color.py                  # Color parsing & gradients
    ├── color_data.py             # CSS4 color definitions
    ├── terminal.py               # Terminal capabilities
    ├── validation.py             # Input validation
    └── wrap.py                   # Text wrapping
```

______________________________________________________________________

## Core Components

### Console (Facade)

The main entry point. Delegates to specialized managers.

```mermaid
classDiagram
    class Console {
        -RichConsole _rich_console
        -TerminalManager _terminal_manager
        -RenderingEngine _rendering_engine
        -ExportManager _export_manager
        +frame(content, title, border, ...)
        +banner(text, font, colors, ...)
        +text(text, color, bold, ...)
        +rule(title, color)
        +newline()
        +clear()
        +export_html() str
        +export_text() str
    }

    class RenderingEngine {
        -RichConsole _console
        +print_frame(...)
        +print_banner(...)
        +print_text(...)
        +print_rule(...)
    }

    class ExportManager {
        -RichConsole _console
        +export_html() str
        +export_text() str
    }

    class TerminalManager {
        +profile TerminalProfile
        +detect_capabilities()
    }

    Console --> RenderingEngine
    Console --> ExportManager
    Console --> TerminalManager
```

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

```mermaid
flowchart LR
    subgraph Input
        LINES[Text Lines]
        BORDER[Border Chars]
    end

    subgraph Strategies
        PS[Position Strategy]
        CS[Color Source]
        TF[Target Filter]
    end

    subgraph Engine
        AG[apply_gradient]
    end

    subgraph Output
        COLORED[Colorized Lines<br/>with ANSI codes]
    end

    LINES --> AG
    BORDER --> AG
    PS --> AG
    CS --> AG
    TF --> AG
    AG --> COLORED

    style AG fill:#FF9800,color:#fff
```

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

```mermaid
flowchart TB
    subgraph text.py
        VW[visual_width]
        SG[split_graphemes]
        PTW[pad_to_width]
        TTW[truncate_to_width]
    end

    subgraph Helpers
        GWL[_grapheme_width_legacy]
        GWS[_grapheme_width_standard]
        PAS[_parse_ansi_sequence]
        SEG[_should_extend_grapheme]
    end

    subgraph emoji_data.py
        SE[SAFE_EMOJIS<br/>1048 entries]
        VS16[VARIATION_SELECTOR_16]
    end

    VW --> SG
    VW --> GWL
    VW --> GWS
    SG --> PAS
    SG --> SEG
    GWL --> VS16
    GWS --> VS16

    style SE fill:#E91E63,color:#fff
```

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

```mermaid
flowchart LR
    subgraph Input
        NAME[Color Name<br/>dodgerblue]
        HEX[Hex Code<br/>#1E90FF]
        RGB[RGB Tuple<br/>30, 144, 255]
    end

    subgraph color.py
        PC[parse_color]
        IC[interpolate_color]
        HTR[hex_to_rgb]
        RTH[rgb_to_hex]
    end

    subgraph color_data.py
        CSS4[CSS4_COLORS<br/>148 colors]
    end

    subgraph Output
        TUPLE["(R, G, B)"]
    end

    NAME --> PC
    HEX --> PC
    RGB --> PC
    PC --> CSS4
    PC --> HTR
    PC --> TUPLE
    IC --> PC
    IC --> RTH

    style CSS4 fill:#9C27B0,color:#fff
```

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

```mermaid
classDiagram
    class PositionStrategy {
        <<interface>>
        +calculate(row, col, total_rows, total_cols) float
    }

    class VerticalPosition {
        +calculate() float
    }

    class HorizontalPosition {
        +calculate() float
    }

    class DiagonalPosition {
        +calculate() float
    }

    class RadialPosition {
        +calculate() float
    }

    PositionStrategy <|.. VerticalPosition
    PositionStrategy <|.. HorizontalPosition
    PositionStrategy <|.. DiagonalPosition
    PositionStrategy <|.. RadialPosition

    note for RadialPosition "Custom strategy example"
```

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

```mermaid
flowchart LR
    subgraph "styles.py"
        BS[BorderStyle]
        BORDERS[BORDERS dict]
    end

    subgraph "box_mapping.py"
        GBS[get_box_style]
        MAP[Style Mapping]
    end

    subgraph "Rich"
        RBOX[Rich Box<br/>ROUNDED, DOUBLE, etc.]
    end

    BS --> BORDERS
    BORDERS --> GBS
    GBS --> MAP
    MAP --> RBOX

    style RBOX fill:#673AB7,color:#fff
```

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
