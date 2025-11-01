# AI Coding Agent Instructions for StyledConsole

**Project:** StyledConsole v0.3.0
**Last Updated:** November 1, 2025
**Python:** ≥3.10 | **License:** Apache-2.0

---

## 🎯 Project Overview

StyledConsole is a production-ready Python library (654 tests, 95.96% coverage) for elegant terminal output with rich formatting, emojis, gradients, and HTML export. Built on **Rich-native integration** for ANSI-safe rendering.

**Key v0.3.0 change:** Frames now use Rich Panel internally (eliminates ANSI wrapping bugs) while maintaining 100% backward compatibility with v0.1.0 API.

**Key architectural pattern:** Facade design—`Console` class wraps specialized managers (`TerminalManager`, `RenderingEngine`, `ExportManager`) over Rich backend.

---

## 📦 Core Architecture

### Component Boundaries

1. **`Console` (Facade)**
   - Main API entry point (`src/styledconsole/console.py`)
   - Delegates to managers; never handles rendering directly
   - Public methods: `frame()`, `banner()`, `text()`, `rule()`, `newline()`, `export_html()`

2. **Rendering Engine** (v0.3.0 - Rich-native)
   - `RenderingEngine`: Uses Rich Panel for frames (ANSI-safe, no wrapping bugs)
   - `BannerRenderer`: ASCII art via pyfiglet + gradient integration (still custom)
   - `box_mapping.py`: Maps border styles (solid, rounded, etc.) to Rich box types
   - **Key change:** `Console.frame()` now uses `Panel` internally, not custom line-by-line rendering

3. **Terminal & Export**
   - `TerminalManager`: Detects capabilities (color depth, emoji safety, dimensions)
   - `ExportManager`: HTML export via ansi2html + ANSI recording

4. **Utilities** (in `utils/`)
   - `text.py`: **Emoji-safe width calculation** (visual_width, split_graphemes, truncate_to_width)
   - `color.py`: CSS4 colors (148 names) + hex/RGB conversion + gradient interpolation
   - `wrap.py`: Multiline text wrapping with emoji support
   - `terminal.py`: Terminal detection (TerminalProfile)

5. **Legacy Utilities** (in `core/` - maintained for v0.1.0 compatibility)
   - `core/frame.py`: FrameRenderer (**DEPRECATED v0.4.0** - use Console.frame() for new code, will be removed in v1.0.0)
   - `core/layout.py`: LayoutComposer (deprecated—use Rich Group, Columns, Table)
   - `effects.py`: Gradient effects (gradient_frame, diagonal_gradient_frame, rainbow_frame)

### Data Flow (v0.3.0)

```
Console.frame(content, title, border)
  ↓
RenderingEngine.print_frame()
  ↓
box_mapping.get_box_style(border) → Rich Box
  ↓
Rich Panel (with color conversion & padding)
  ↓
RichConsole.print() → ANSI terminal output
  ↓
ExportManager.export_html() → HTML string (if recording mode)
```

---

## 🎨 Key Conventions & Patterns

### Emoji Handling (CRITICAL)

**Tier 1 Emojis Only:** ✅🔥🎉🚀⚡💡🎨💎 (and ~100 more safe emojis)
- Always use `visual_width()` from `utils/text.py` for width calculations
- Never assume 1 char = 1 display width
- Border alignment uses `pad_to_width()` and `truncate_to_width()` (already emoji-safe)
- See `doc/EMOJI_GUIDELINES.md` for categorized safe emojis

**Example:**
```python
from styledconsole.utils.text import visual_width, pad_to_width

width = visual_width("🚀 Title")  # Returns 9, not 8
padded = pad_to_width("🚀 Title", 20)  # Correctly centers emoji
```

### Border Styles

**8 builtin styles** in `src/styledconsole/core/styles.py`:
- Each defined as frozen dataclass with Unicode box-drawing characters
- v0.3.0: Mapped to Rich box types via `core/box_mapping.py`
- Access via: `from styledconsole import SOLID, ROUNDED, DOUBLE, etc.`
- or `from styledconsole.core.styles import BorderStyle, BORDERS`
- Custom styles possible but discourage—use existing 8

```python
from styledconsole.core.styles import BorderStyle, BORDERS
from styledconsole.core.box_mapping import get_box_style

# Legacy (v0.1.0, still works):
style = BORDERS["solid"]  # type: BorderStyle

# v0.3.0 Rich-native:
box = get_box_style("solid")  # Returns Rich box.SQUARE
# Use with Panel: Panel("content", box=box)
```

### Color System

**CSS4 Colors (primary approach):**
```python
from styledconsole import CSS4_COLORS, parse_color, interpolate_color

# String names (148 supported):
console.frame("...", border_color="lime", content_color="blue")

# Hex codes (always supported):
console.frame("...", border_color="#FF5733")

# RGB tuples:
console.frame("...", border_color=(255, 87, 51))

# Gradient interpolation:
interpolate_color("red", "blue", 0.5)  # Returns midpoint hex code
```

### Text Utilities

**Always use from `utils/text.py`:**
- `visual_width(s)`: Emoji-aware display width (use instead of `len()`)
- `split_graphemes(s)`: Splits by grapheme cluster (handles emoji + modifiers)
- `pad_to_width(s, width, align)`: Padding aware of emoji width
- `truncate_to_width(s, width)`: Truncation preserves emoji integrity
- `strip_ansi(s)`: Removes ANSI codes for clean processing

```python
from styledconsole.utils.text import visual_width, split_graphemes

text = "🚀 Rocket"
print(visual_width(text))     # 9 (not 8)
print(split_graphemes(text))  # ['🚀', ' ', 'R', 'o', 'c', 'k', 'e', 't']
```

### Type Aliases (in `types.py`)

- `AlignType`: Literal["left", "center", "right"]
- `ColorType`: str | tuple[int, int, int]
- `Renderer`: Protocol for custom renderers

Use in function signatures for clarity.

---

## 🧪 Testing & Examples

### Test Structure

- **Unit Tests:** `tests/unit/` – isolated component testing
- **Integration Tests:** `tests/integration/` – cross-component workflows
- **Snapshots:** `tests/snapshots/` – pytest snapshot testing for visual regression
- **Examples:** `examples/basic/` (10+ examples) → `examples/showcase/` (advanced features)

### Running Tests

```bash
# All tests with coverage:
pytest --cov=src/styledconsole --cov-report=html

# Specific test file:
pytest tests/unit/test_frame.py -v

# Run all examples (validates UX):
python test_examples.py

# Run visual examples (for manual inspection):
python examples/run_all_visual.py
```

### Snapshot Testing Pattern

Example tests verify visual output hasn't changed:
```python
def test_frame_solid_border(snapshot):
    console = Console()
    # Capture output for snapshot comparison
    # ...
    assert output == snapshot  # Stored in tests/snapshots/
```

When output intentionally changes: `pytest --snapshot-update`

---

## 🔄 Development Workflows

### Adding Features

1. **If modifying rendering (frames/banners):**
   - Edit relevant `core/*.py` file
   - Add/update snapshot tests in `tests/`
   - Update example in `examples/basic/` or `examples/showcase/`
   - Ensure Console facade method exists (or add to `console.py`)

2. **If adding color/emoji features:**
   - Update `utils/color.py` or `utils/text.py`
   - Add CSS4 names to `utils/color_data.py` if new colors
   - Test with `utils/terminal.py` detection (check emoji safety)

3. **If adding export format (currently HTML only):**
   - Extend `ExportManager` in `core/export_manager.py`
   - Update `Console.export_*()` method

### Running Locally

```bash
# Setup environment (Python ≥3.10):
python -m venv venv && source venv/bin/activate

# Install with dev dependencies:
pip install -e ".[dev]"  # From pyproject.toml

# Quick validation:
python examples/basic/01_simple_frame.py
```

### Before Committing

- Run full test suite: `pytest --cov=src/styledconsole` (target: ≥95% coverage)
- Run linter: `ruff check src/ tests/`
- Format code: `ruff format src/ tests/`
- Validate examples: `python test_examples.py`

---

## 📚 Critical Files Reference

| File | Purpose |
|------|---------|
| `src/styledconsole/console.py` | Main facade—API entry point |
| `src/styledconsole/core/rendering_engine.py` | v0.3.0 Rich-native rendering coordinator |
| `src/styledconsole/core/box_mapping.py` | Border style → Rich Box mapping (v0.3.0) |
| `src/styledconsole/core/frame.py` | Frame rendering logic (legacy, still works) |
| `src/styledconsole/core/banner.py` | Banner rendering (pyfiglet) |
| `src/styledconsole/core/styles.py` | Border style definitions |
| `src/styledconsole/utils/text.py` | **Emoji-safe text utilities** (critical) |
| `src/styledconsole/utils/color.py` | Color parsing & gradients |
| `src/styledconsole/effects.py` | Gradient/rainbow effects |
| `pyproject.toml` | Dependencies: rich, pyfiglet, wcwidth, ansi2html |
| `doc/guides/EMOJI_GUIDELINES.md` | Categorized safe emoji list (100+ emojis) |
| `doc/project/PLAN.md` | Detailed architecture (1099 lines) |

---

## ⚠️ Project-Specific Gotchas

1. **Never hardcode width assumptions:**
   `"text" != visual_width("text")` when emojis present. Always use `visual_width()`.

2. **Border alignment requires emoji awareness:**
   Use `pad_to_width()` / `truncate_to_width()`, not string slicing.

3. **Rich backend integration:**
   Console wraps `rich.console.Console`, not replaces it. Access via `console._rich_console` if needed (internal API, rarely needed).

4. **Terminal detection is optional:**
   `detect_terminal=False` in Console() skips capability detection. Useful for non-terminal output.

5. **Export mode is opt-in:**
   Pass `record=True` to Console for HTML export. Normal console output doesn't record.

6. **CSS4 names are normalized:**
   `"RoyalBlue"` → `"royalblue"`. Use lowercase in code.

---

## 📖 Documentation Philosophy

This project **explicitly avoids over-documentation**. Read:
- `doc/DOCUMENTATION_POLICY.md` – why strict docs matter (learned from failed rewrite)
- `doc/project/SPECIFICATION.md` – what we're building & user journeys
- `doc/project/PLAN.md` – architecture & design rationale

**Key rule:** If it's not a design decision, architecture component, or user feature—don't document it. The code is the spec.

---

## 🚀 Common Tasks

### Add a new border style
1. Edit `core/styles.py`: Add frozen dataclass with Unicode chars
2. Register in `BORDERS` dict
3. Add snapshot test in `tests/unit/test_frame.py`
4. Add example in `examples/gallery/border_gallery.py`

### Support new color input format
1. Update `parse_color()` in `utils/color.py`
2. Add ColorType to types.py if needed
3. Test with gradients in `effects.py`
4. Add example in `examples/`

### Fix emoji rendering bug
1. Check `utils/text.py` (visual_width, split_graphemes)
2. Verify terminal detection in `utils/terminal.py`
3. Add test case in `tests/unit/test_text.py`
4. Validate with `doc/EMOJI_GUIDELINES.md` safe list

---

## 📞 Questions?

Refer to existing examples (`examples/basic/01-09`) for common patterns. The 654 passing tests are the ultimate reference for expected behavior.
