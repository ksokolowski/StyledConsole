# PLAN (Phase 2: Technical Plan)

**Project:** StyledConsole
**Version:** 0.1.0
**Date:** October 17, 2025
**License:** Apache License 2.0
**Status:** Planning Complete

---

## Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  User Application                       │
│  (CLI tools, test scripts, CI/CD pipelines)             │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │   StyledConsole API     │
        │  (High-Level Facade)    │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │   Preset Functions      │
        │  (status_frame,         │
        │   dashboard_small, etc) │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────────────────┐
        │     Core Rendering Engine           │
        ├─────────────────────────────────────┤
        │  • Frame Renderer                   │
        │  • Banner Renderer                  │
        │  • Layout Composer                  │
        │  • Text Utilities (emoji-safe)      │
        └────────────┬────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │   Rich Backend          │
        │  (ANSI rendering)       │
        └────────────┬────────────┘
                     │
        ┌────────────┴─────────────────────┐
        │        Output Targets            │
        ├──────────────────────────────────┤
        │  • Console (ANSI)                │
        │  • HTML Export (ansi2html)       │
        │  • Terminal Detection            │
        └──────────────────────────────────┘
```

### Module Structure

```
styledconsole/
├── __init__.py                   # Public API exports
├── console.py                    # Console class (main facade)
│
├── core/                         # Core rendering logic
│   ├── __init__.py
│   ├── frame.py                  # Frame rendering
│   ├── banner.py                 # Banner (FIGlet) rendering
│   ├── layout.py                 # Layout composition
│   └── styles.py                 # Border styles, themes
│
├── presets/                      # High-level preset functions
│   ├── __init__.py
│   ├── status.py                 # status_frame()
│   ├── dashboards.py             # dashboard_small/medium/large()
│   └── reports.py                # test_summary(), etc.
│
├── utils/                        # Utilities
│   ├── __init__.py
│   ├── text.py                   # Emoji width, grapheme handling
│   ├── color.py                  # RGB/hex, gradients
│   └── terminal.py               # Capability detection
│
├── export/                       # Export functionality
│   ├── __init__.py
│   └── html.py                   # HTML export via ansi2html
│
└── tests/                        # Test suite
    ├── unit/                     # Unit tests
    ├── integration/              # Integration tests
    ├── visual/                   # Snapshot tests
    └── fixtures/                 # Test data
```

## Technology Stack

### Core Dependencies

| Package | Version | Purpose | Justification |
|---------|---------|---------|---------------|
| **rich** | ≥13.7 | ANSI rendering, emoji safety | Mature, well-tested, handles complex Unicode correctly |
| **pyfiglet** | ≥1.0.2 | ASCII art banners | Standard for banner text generation |
| **wcwidth** | ≥0.2.13 | Unicode width calculation | Reliable emoji width detection |
| **ansi2html** | ≥1.8.0 | HTML export | Proven ANSI→HTML conversion |

**Total Core Dependencies:** 4 packages ✅ (meets ≤5 constraint)

### Development Dependencies

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "pytest-snapshot>=0.9",
    "ruff>=0.3",              # Linting, formatting, and type checking
    "pre-commit>=3.6",
]
```

**Package Manager:** UV (Astral's fast Python package manager)
- 10-100x faster than Poetry/pip
- Standard PEP 621 pyproject.toml format
- Built-in Python version management
- Same team as Ruff (Astral)

### Python Version

- **Minimum:** Python 3.10
- **Tested:** 3.10, 3.11, 3.12
- **Features Used:**
  - Dataclasses (3.7+)
  - Type hints with `|` union syntax (3.10+)
  - `match` statements (optional, 3.10+)
  - Structural pattern matching (optional)

## Component Design

### 1. Console Class (Main Facade)

**Purpose:** Primary entry point for all rendering operations

**Complete Public API:**

```python
from typing import Any, TextIO
from rich.console import Console as RichConsole
import logging
import sys

class Console:
    """High-level console rendering facade."""

    def __init__(
        self,
        *,
        detect_terminal: bool = True,
        record: bool = True,
        width: int | None = None,
        file: TextIO | None = None,
        debug: bool = False,
    ):
        """Initialize console with terminal detection.

        Args:
            detect_terminal: Auto-detect terminal capabilities
            record: Enable HTML export mode
            width: Fixed width (None = auto-detect)
            file: Output stream (default: sys.stdout)
            debug: Enable debug logging for library internals
        """
        self._rich_console = RichConsole(
            record=record,
            width=width,
            file=file or sys.stdout
        )
        self._profile: TerminalProfile | None = None
        self._logger = logging.getLogger('styledconsole') if debug else None

        if detect_terminal:
            self._profile = detect_terminal_capabilities()
            if self._logger:
                self._logger.debug(f"Detected terminal: {self._profile}")

    # === Core Rendering Methods ===

    def frame(
        self,
        content: str | Any,
        *,
        title: str | None = None,
        border: str = "rounded",
        border_color: str | None = None,
        title_color: str | None = None,
        padding: int = 1,
        width: int | None = None,
    ) -> None:
        """Render a framed block.

        Args:
            content: Text content or renderable object
            title: Optional frame title (centered)
            border: Border style ('solid', 'double', 'rounded', 'heavy', 'ascii')
            border_color: CSS4 color name or hex
            title_color: Title text color (default: border_color)
            padding: Inner padding (spaces)
            width: Fixed width (None = auto-fit content)
        """

    def banner(
        self,
        text: str,
        *,
        font: str = "slant",
        color: str | None = None,
        gradient: tuple[str, str] | None = None,
    ) -> None:
        """Render a banner with FIGlet.

        Args:
            text: Banner text (ASCII recommended)
            font: FIGlet font name ('slant', 'standard', 'banner')
            color: Solid color (CSS4 name or hex)
            gradient: Gradient colors (start, end) - overrides color
        """

    def text(
        self,
        text: str,
        *,
        color: str | None = None,
        bold: bool = False,
        italic: bool = False,
    ) -> None:
        """Print styled text.

        Args:
            text: Text to print
            color: Text color (CSS4 name or hex)
            bold: Bold text
            italic: Italic text
        """

    def rule(
        self,
        title: str = "",
        *,
        color: str | None = None,
        style: str = "─",
    ) -> None:
        """Print a horizontal rule.

        Args:
            title: Optional centered title
            color: Rule color
            style: Line character ('─', '═', '-')
        """

    def newline(self, count: int = 1) -> None:
        """Print blank lines.

        Args:
            count: Number of blank lines
        """

    # === Export Methods ===

    def export_html(self, *, inline_styles: bool = True) -> str:
        """Export recorded output as HTML.

        Args:
            inline_styles: Use inline CSS (True) or classes (False)

        Returns:
            HTML string with ANSI formatting preserved

        Raises:
            ExportError: If recording not enabled
        """

    def export_text(self) -> str:
        """Export recorded output as plain text (ANSI codes stripped).

        Returns:
            Plain text without formatting
        """

    # === Utility Methods ===

    @property
    def terminal_profile(self) -> TerminalProfile | None:
        """Get detected terminal capabilities."""
        return self._profile

    def clear(self) -> None:
        """Clear the console (if supported)."""
        if self._profile and self._profile.ansi_support:
            self._rich_console.clear()
```

**Public Exports (`__init__.py`):**

```python
# Main API
from styledconsole.console import Console

# Exceptions
from styledconsole.exceptions import (
    StyledConsoleError,
    RenderError,
    ExportError,
    TerminalError,
)

# Preset functions
from styledconsole.presets import (
    status_frame,
    test_summary,
    dashboard_small,
    dashboard_medium,
    dashboard_large,
)

# Utilities
from styledconsole.utils.color import get_color_names

__version__ = "0.1.0"
__all__ = [
    "Console",
    "StyledConsoleError",
    "RenderError",
    "ExportError",
    "TerminalError",
    "status_frame",
    "test_summary",
    "dashboard_small",
    "dashboard_medium",
    "dashboard_large",
    "get_color_names",
]
```

### 2. Color Utilities

**Purpose:** Parse and convert colors with CSS4 named color support

**Supported Color Formats:**

1. **Hex:** `#FF0000`, `#f00` (shorthand)
2. **RGB tuples:** `rgb(255, 0, 0)`, `(255, 0, 0)`
3. **CSS4 named colors:** 148 colors from W3C standard

**CSS4 Named Colors** (148 total, examples):
```python
CSS4_COLORS = {
    # Basic
    'red': '#ff0000', 'green': '#008000', 'blue': '#0000ff',
    'yellow': '#ffff00', 'orange': '#ffa500', 'purple': '#800080',

    # Extended blues
    'aliceblue': '#f0f8ff', 'dodgerblue': '#1e90ff', 'lightblue': '#add8e6',
    'navy': '#000080', 'skyblue': '#87ceeb', 'steelblue': '#4682b4',

    # Vibrant colors
    'coral': '#ff7f50', 'tomato': '#ff6347', 'gold': '#ffd700',
    'lime': '#00ff00', 'cyan': '#00ffff', 'magenta': '#ff00ff',

    # Nature colors
    'aquamarine': '#7fffd4', 'lightseagreen': '#20b2aa', 'seagreen': '#2e8b57',
    'olive': '#808000', 'teal': '#008080', 'indigo': '#4b0082',

    # Grays (both spellings)
    'gray': '#808080', 'grey': '#808080',
    'darkgray': '#a9a9a9', 'darkgrey': '#a9a9a9',
    'lightgray': '#d3d3d3', 'lightgrey': '#d3d3d3',

    # ... 148 total colors
}
```

**Implementation:**

```python
def parse_color(value: str) -> tuple[int, int, int]:
    """
    Parse color from multiple formats.

    Supports:
    - CSS4 named colors (case-insensitive): 'dodgerblue', 'CORAL'
    - Hex: '#FF0000', '#f00'
    - RGB: 'rgb(255,0,0)', '(255, 0, 0)'

    Returns RGB tuple: (r, g, b)
    """
    value = value.strip().lower()

    # Try CSS4 named color first (most user-friendly)
    if value in CSS4_COLORS:
        return hex_to_rgb(CSS4_COLORS[value])

    # Try hex format
    if value.startswith('#'):
        return hex_to_rgb(value)

    # Try rgb() format
    if 'rgb' in value:
        return parse_rgb_string(value)

    raise ValueError(f"Unknown color format: {value}")

def interpolate_color(start: str, end: str, t: float) -> str:
    """
    Interpolate between two colors for gradients.

    Works with any color format (names, hex, rgb).

    Example:
        interpolate_color('coral', 'dodgerblue', 0.5)
        # Returns middle color between coral and dodgerblue
    """
    r1, g1, b1 = parse_color(start)
    r2, g2, b2 = parse_color(end)

    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)

    return rgb_to_hex(r, g, b)

def get_color_names() -> list[str]:
    """Return list of all supported CSS4 color names."""
    return sorted(CSS4_COLORS.keys())
```

**User-Friendly API Examples:**

```python
# All these work!
console.frame("Alert", color="red")
console.frame("Info", color="dodgerblue")
console.frame("Success", color="lightseagreen")
console.frame("Warning", color="coral")
console.frame("Error", color="#FF0000")  # Also supports hex

# Gradients work with color names
console.banner("DEPLOY", gradient=("gold", "orange"))
console.banner("OCEAN", gradient=("lightblue", "navy"))
```

**Benefits:**
- **Memorable:** "coral" is easier than "#ff7f50"
- **Consistent:** Same color names across matplotlib, CSS, web
- **Discoverable:** `get_color_names()` lists all options

---

### 3. Frame Renderer

**Purpose:** Handle frame rendering with emoji-safe alignment

**Key Algorithms:**

```python
def render_frame(
    content: str,
    title: str | None,
    border_style: BorderStyle,
    width: int | None = None,
) -> list[str]:
    """
    Render frame with proper alignment.

    Algorithm:
    1. Measure content width (emoji-safe via wcwidth)
    2. Determine frame width (auto or specified)
    3. Apply padding to content lines
    4. Generate border lines with title (if present)
    5. Return list of styled lines
    """
    # Calculate visual width
    content_lines = content.splitlines()
    max_width = max(visual_width(line) for line in content_lines)

    # Determine frame dimensions
    inner_width = width or (max_width + 2 * padding)

    # Build frame
    top = border_style.render_top(inner_width, title)
    middle = [border_style.render_content(line, inner_width, padding)
              for line in content_lines]
    bottom = border_style.render_bottom(inner_width)

    return [top] + middle + [bottom]
```

**Border Styles:**

```python
@dataclass
class BorderStyle:
    """Define border character sets."""
    top_left: str
    top_right: str
    bottom_left: str
    bottom_right: str
    horizontal: str
    vertical: str
    name: str

# Predefined styles
BORDERS = {
    "solid": BorderStyle("┌", "┐", "└", "┘", "─", "│", "solid"),
    "double": BorderStyle("╔", "╗", "╚", "╝", "═", "║", "double"),
    "rounded": BorderStyle("╭", "╮", "╰", "╯", "─", "│", "rounded"),
    "ascii": BorderStyle("+", "+", "+", "+", "-", "|", "ascii"),
}
```

### 3. Emoji-Safe Text Utilities

**Purpose:** Handle Unicode width calculations correctly

**Emoji Support Strategy:**

StyledConsole uses a **tiered approach** to emoji/icon support:

| Tier | Type | Examples | Codepoints | Width | MVP Status |
|------|------|----------|------------|-------|------------|
| **1** | Basic Icons | ✅ ❌ ⚠️ 🚀 ❤️ 🎉 | 1 | 2 | ✅ v0.1 |
| **2** | Modified Emojis | 👍🏽 👨🏻 🏳️ | 2-3 | 2-4 | 🔜 v0.2 |
| **3** | ZWJ Sequences | 👨‍👩‍👧‍👦 👨‍💻 🏳️‍🌈 | 4+ | 2-4 | 🔮 v0.3+ |

**Tier 1 (MVP v0.1):** Focus on single-codepoint basic icons that are universally supported and have predictable width=2 behavior. These cover 95% of test reporting use cases (status indicators, simple decorations).

**Implementation:**

```python
from wcwidth import wcswidth
import regex

def visual_width(text: str) -> int:
    """
    Calculate visual width of text including Tier 1 basic icons.

    Uses wcwidth library which handles single-codepoint emojis well.

    Known Limitations (v0.1):
    - Tier 2 (skin tones) may have ±1 width errors
    - Tier 3 (ZWJ sequences) may break or misalign
    - Future versions will add grapheme cluster analysis
    """
    # Strip ANSI codes first
    clean = strip_ansi(text)

    # Calculate width using wcwidth
    width = wcswidth(clean)

    # Fallback for unsupported characters
    if width < 0:
        return len(clean)  # Conservative fallback

    return width

def split_graphemes(text: str) -> list[str]:
    """
    Split text into grapheme clusters.

    Works well for Tier 1 icons. Tier 2/3 may need enhanced logic.
    """
    return regex.findall(r'\X', text)

def pad_to_width(text: str, width: int, align: str = "left") -> str:
    """Pad text to specified visual width."""
    current = visual_width(text)
    padding = max(0, width - current)

    if align == "left":
        return text + " " * padding
    elif align == "right":
        return " " * padding + text
    else:  # center
        left_pad = padding // 2
        right_pad = padding - left_pad
        return " " * left_pad + text + " " * right_pad
```

### 4. Banner Renderer

**Purpose:** Generate FIGlet banners with gradients

```python
from pyfiglet import Figlet

def render_banner(
    text: str,
    font: str = "slant",
    gradient: tuple[str, str] | None = None,
) -> str:
    """Render banner text with optional gradient."""
    fig = Figlet(font=font)
    banner = fig.renderText(text)

    if gradient:
        # Apply gradient per line
        lines = banner.splitlines()
        start_color, end_color = gradient
        colored_lines = []

        for i, line in enumerate(lines):
            t = i / max(len(lines) - 1, 1)
            color = interpolate_color(start_color, end_color, t)
            colored_lines.append(apply_color(line, color))

        return "\n".join(colored_lines)

    return banner
```

### 5. Terminal Detection

**Purpose:** Detect terminal capabilities for graceful degradation

```python
import os
import sys

@dataclass
class TerminalProfile:
    """Terminal capability profile."""
    ansi_support: bool
    color_depth: int  # 8, 256, or 16777216 (truecolor)
    emoji_safe: bool
    width: int
    height: int

def detect_terminal_capabilities() -> TerminalProfile:
    """
    Detect terminal capabilities.

    Checks:
    - TERM environment variable
    - COLORTERM for truecolor
    - isatty() for pipe detection
    - Terminal size
    """
    # Check if output is a terminal
    is_tty = sys.stdout.isatty()

    # Detect color support
    term = os.getenv("TERM", "")
    colorterm = os.getenv("COLORTERM", "")

    if "truecolor" in colorterm or "24bit" in colorterm:
        color_depth = 16777216
    elif "256" in term:
        color_depth = 256
    elif term and term != "dumb":
        color_depth = 8
    else:
        color_depth = 0

    # Detect emoji support (heuristic)
    emoji_safe = (
        is_tty
        and color_depth >= 256
        and os.getenv("LANG", "").endswith("UTF-8")
    )

    # Get terminal size
    size = os.get_terminal_size()

    return TerminalProfile(
        ansi_support=is_tty and color_depth > 0,
        color_depth=color_depth,
        emoji_safe=emoji_safe,
        width=size.columns,
        height=size.lines,
    )
```

### 6. HTML Exporter

**Purpose:** Convert ANSI output to HTML for reports

```python
from ansi2html import Ansi2HTMLConverter

class HtmlExporter:
    """Export console output to HTML."""

    def __init__(self):
        self.converter = Ansi2HTMLConverter(inline=True, scheme="ansi2html")

    def export(self, ansi_text: str) -> str:
        """Convert ANSI text to HTML fragment."""
        html = self.converter.convert(ansi_text, full=False)

        # Wrap in div with monospace styling
        return f'<div style="font-family: monospace; white-space: pre;">{html}</div>'
```

### 7. Preset Functions

**Purpose:** High-level convenience functions

```python
# presets/status.py
def status_frame(
    test_name: str,
    status: str,
    *,
    message: str | None = None,
) -> None:
    """Render a test status frame.

    Displays formatted test status instantly - library formats content,
    doesn't measure or track timing. ANSI output captured by CI/CD logs.
    """
    console = get_console()

    # Choose color based on status
    color = {
        "PASS": "green",
        "FAIL": "red",
        "SKIP": "yellow",
    }.get(status.upper(), "white")

    # Build content
    lines = [f"[bold {color}]{status}[/] {test_name}"]
    if message:
        lines.append(message)

    content = "\n".join(lines)

    console.frame(
        content,
        title=f"Test: {test_name}",
        border="rounded",
        border_color=color,
    )

# presets/dashboards.py
def dashboard_small(
    stats: dict[str, int],
    *,
    title: str = "Test Results",
) -> None:
    """Render a small dashboard with statistics."""
    console = get_console()

    # Banner header
    console.banner(f"📊 {title}", font="slant")

    # Stats frame
    lines = []
    for key, value in stats.items():
        color = _get_stat_color(key)
        lines.append(f"[{color}]{key}:[/] {value}")

    console.frame(
        "\n".join(lines),
        border="double",
        padding=2,
    )
```

## Data Flow

### Rendering Flow

```
User Code
    ↓
Console.frame(content, **options)
    ↓
Frame Renderer
    ├→ Text Utilities (measure width, handle emojis)
    ├→ Color Utilities (apply gradients)
    └→ Border Styles (generate frame)
    ↓
Rich Backend
    ├→ Rich Console.print()
    └→ Record to buffer (if enabled)
    ↓
Output
    ├→ Terminal (ANSI codes)
    └→ HTML Export (ansi2html)
```

### Export Flow

```
Console.export_html()
    ↓
Get recorded ANSI output from Rich
    ↓
ansi2html Converter
    ├→ Parse ANSI codes
    ├→ Generate HTML spans
    └→ Apply inline CSS
    ↓
HTML Fragment
```

## Performance Considerations

### Optimization Strategies

1. **Width Calculation Caching**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=1024)
   def visual_width(text: str) -> int:
       """Cached width calculation."""
   ```

2. **Lazy HTML Export**
   - Only convert to HTML on explicit `export_html()` call
   - Avoid overhead during normal rendering

3. **Border Reuse**
   - Pre-generate common border patterns
   - Cache border strings by width

4. **Minimal Rich Overhead**
   - Use Rich only for final rendering
   - Do layout calculations in pure Python

### Performance Targets

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Simple frame | <10ms | `time.perf_counter()` |
| Banner render | <40ms | FIGlet + gradient |
| Dashboard (5 frames) | <50ms | End-to-end |
| HTML export (100 frames) | <200ms | Batch export |

## Debug Logging

**Purpose:** Internal debugging for library developers, not for normal user operations.

**Usage:**

```python
import logging
from styledconsole import Console

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('styledconsole')

console = Console(debug=True)
console.frame("Test")  # Logs: "Rendering frame with border=rounded, width=auto"
```

**What Gets Logged (debug=True):**
- Terminal capability detection results
- Frame dimension calculations
- Color parsing operations
- Font loading from pyfiglet
- HTML export operations

**What Does NOT Get Logged:**
- User content (privacy)
- Normal rendering operations (performance)
- ANSI output (user controls this)

**Rationale:** This is a styling library, not an application. Users control output via their terminal. Debug logging is ONLY for troubleshooting library bugs, not for operational logging.

---

## Error Handling Strategy

### Error Categories

1. **User Input Errors**
   - Invalid color values → Clear error with valid examples
   - Unsupported border style → List available styles
   - Invalid font name → List available fonts

2. **Terminal Capability Errors**
   - No ANSI support → Fallback to plain text with warning
   - Emoji unsupported → Replace with ASCII alternatives
   - Width too narrow → Warn and clip content

3. **Export Errors**
   - ansi2html failure → Return plain text fallback
   - Memory issues → Suggest streaming mode

### Exception Hierarchy

```python
class StyledConsoleError(Exception):
    """Base exception for styledconsole."""

class RenderError(StyledConsoleError):
    """Error during rendering."""

class ExportError(StyledConsoleError):
    """Error during export."""

class TerminalError(StyledConsoleError):
    """Terminal capability issue (warning only, non-fatal)."""
```

### Error Handling Examples

```python
from styledconsole import Console, RenderError, ExportError

# Example 1: Invalid color name
try:
    console = Console()
    console.frame("Test", border_color="not-a-color")
except RenderError as e:
    print(f"Invalid color: {e}")
    print("Valid colors: use get_color_names() or hex values")

# Example 2: Export without recording
try:
    console = Console(record=False)
    console.frame("Test")
    html = console.export_html()  # Will raise ExportError
except ExportError as e:
    print(f"Export failed: {e}")
    print("Solution: Initialize with record=True")

# Example 3: Graceful degradation (no exception)
console = Console(detect_terminal=True)
if console.terminal_profile and not console.terminal_profile.ansi_support:
    # Terminal doesn't support colors - library handles gracefully
    console.frame("Still works in plain text!")

# Example 4: Invalid border style
try:
    console.frame("Test", border="invalid")
except RenderError as e:
    print(f"Error: {e}")
    print("Available borders: solid, double, rounded, heavy, ascii")
```

**Error Philosophy:**
- **Fail fast** for invalid user input (colors, styles, fonts)
- **Graceful degradation** for terminal limitations (no exception)
- **Clear messages** with actionable suggestions

---

## Testing Strategy

### Test Levels

1. **Unit Tests** (pytest)
   - Text utilities (emoji width, padding)
   - Color utilities (gradient interpolation)
   - Frame rendering (border generation)
   - Terminal detection (mocked environment)

2. **Integration Tests**
   - Console API end-to-end
   - Preset functions
   - HTML export pipeline

3. **Visual Snapshot Tests** (pytest-snapshot)
   - Frame rendering output
   - Banner output
   - Dashboard layouts
   - Compare against baseline files

4. **Cross-Platform Tests** (GitHub Actions matrix)
   - Linux (Ubuntu 22.04, 24.04)
   - macOS (latest)
   - Windows (Windows Server)

### Test Coverage Target

- **Line Coverage:** ≥90%
- **Branch Coverage:** ≥85%
- **Public API:** 100% documented and tested

## Deployment & Distribution

### Packaging

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "styledconsole"
version = "0.1.0"
description = "Emoji-safe ANSI console rendering library"
requires-python = ">=3.10"
license = {text = "Apache-2.0"}
dependencies = [
    "rich>=13.7",
    "pyfiglet>=1.0.2",
    "wcwidth>=0.2.13",
    "ansi2html>=1.8.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "pytest-snapshot>=0.9",
    "ruff>=0.3",
    "pre-commit>=3.6",
]
```

### Release Process

1. **Version Bump** (semantic versioning)
2. **Run Full Test Suite** (all platforms)
3. **Update CHANGELOG.md**
4. **Build Wheel and Source Distribution** (`uv build`)
5. **Publish to PyPI** (`uv publish`)
6. **Tag Git Release**
7. **Update Documentation**

**UV Commands:**
```bash
# Build
uv build

# Publish to PyPI
uv publish

# Test in isolated environment
uv run pytest

# Test multiple Python versions
uv run --python 3.10 pytest
uv run --python 3.11 pytest
uv run --python 3.12 pytest
```

### Documentation

- **Hosting:** ReadTheDocs or GitHub Pages
- **Generator:** MkDocs with Material theme
- **Sections:**
  - Quick Start
  - API Reference (auto-generated)
  - Preset Functions Guide
  - Examples Gallery
  - Contributing Guide

## Security Considerations

### Input Sanitization

- **HTML Export:** Escape all user-provided content
- **ANSI Injection:** Validate/strip malicious ANSI codes
- **Path Traversal:** No file system access in MVP

### Dependencies

- **Supply Chain:** Use UV lock file (uv.lock)
- **Vulnerability Scanning:** Dependabot enabled
- **Version Pinning:** Minimum versions specified

## Migration & Compatibility

### Future Backend Support

Design allows pluggable backends:

```python
class RenderBackend(Protocol):
    """Backend interface for future Textual support."""

    def render_frame(self, frame: Frame) -> None: ...
    def render_banner(self, banner: Banner) -> None: ...
```

### Deprecation Policy

- No breaking changes in 0.x versions
- Deprecation warnings for 2 minor versions
- Clear migration guides for 1.0

---

## Validation Checklist

- [x] Architecture clearly defined
- [x] Technology stack justified
- [x] Module structure specified
- [x] Component interfaces designed
- [x] Data flow documented
- [x] Performance targets set
- [x] Error handling strategy defined
- [x] Testing strategy planned
- [x] Deployment process outlined
- [x] Security considerations addressed

**Status:** ✅ Planning phase complete - Ready for Tasks breakdown
