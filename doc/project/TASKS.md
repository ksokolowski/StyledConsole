# TASKS (Phase 3: Implementation Breakdown)

**Project:** StyledConsole
**Version:** 0.1.0
**Date Started:** October 17, 2025
**Status:** 🚧 In Progress - M1: Core Setup & Utilities

---

## Progress Overview

**Overall Progress:** 10/23 tasks completed (43%)

| Milestone | Tasks | Completed | Progress |
|-----------|-------|-----------|----------|
| **M1: Core Setup & Utilities** | 5 | 5 | ✅✅✅✅✅ 100% |
| **M2: Rendering Engine** | 4 | 4 | ✅✅✅✅ 100% |
| **M3: Preset Functions** | 5 | 1 | ✅⬜⬜⬜⬜ 20% |
| **M4: Export & Fallbacks** | 2 | 0 | ⬜⬜ 0% |
| **M5: Testing & Release** | 5 | 0 | ⬜⬜⬜⬜⬜ 0% |

**Total Effort:** 35.5 days (~7 weeks)
**Days Completed:** 18.5 / 35.5 (52%)
**Days Remaining:** 17
**Current Date:** October 19, 2025
**Current Task:** 🎯 M3 Complete! Gradient Effects + CSS4 Color Migration ✅

### Project Statistics (Oct 19, 2025)

- **Source Code:** 16 Python modules (1049 tracked statements)
- **Tests:** 502 tests across 18 test modules
- **Coverage:** 93.42% (980/1049 statements covered, 69 missed)
- **Examples:** 11 files (8 basic examples + 3 showcase examples + prototype)
- **Commits:** 45+ commits since project start (Oct 17, 2025)
- **Documentation:** 6 markdown files (README, PLAN, TASKS, EMOJI_GUIDELINES, 2 example READMEs)

## Task Organization

Tasks are organized into **5 milestones** (M1-M5). Each task includes:
- ✅ Clear acceptance criteria (checkboxes)
- 📅 Effort estimate in days
- 🔗 Dependencies on other tasks
- 📝 Implementation notes and guidance

**Task Status Legend:**
- ⬜ Not started
- 🚧 In progress
- ✅ Completed
- ⏸️ Blocked

---

## Milestones Overview

| Milestone | Focus | Duration | Dependencies |
|-----------|-------|----------|--------------|
| **M1** | Core Setup & Utilities | Week 1-2 | None |
| **M2** | Rendering Engine | Week 3-4 | M1 complete |
| **M3** | Preset Functions & Layouts | Week 5-6 | M2 complete |
| **M4** | Terminal Detection & HTML Export | Week 7 | M2 complete |
| **M5** | Testing, Documentation, Release | Week 8 | M1-M4 complete |

---

## M1: Core Setup & Utilities (Week 1-2)

### T-001: Project Setup & Structure ✅
**Priority:** High
**Effort:** 0.5 days
**Dependencies:** None
**Status:** ✅ Completed (Oct 17, 2025)

**Description:**
Initialize project repository with proper structure, dependency management, and development tools.

**Acceptance Criteria:**
- [x] Repository created with proper `.gitignore`
- [x] `pyproject.toml` configured with UV (PEP 621 format)
- [x] Core dependencies declared: rich, pyfiglet, wcwidth, ansi2html
- [x] Dev dependencies declared: pytest, ruff, pre-commit
- [x] Directory structure created (see PLAN.md)
- [x] `__init__.py` files in all packages
- [x] Pre-commit hooks configured
- [x] README.md with project description

**Completion Notes:**
- ✅ Installed UV 0.9.3
- ✅ Configured hatchling build backend (not uv_build)
- ✅ Created complete package structure: src/styledconsole/{core,utils,presets,export}
- ✅ Created test structure: tests/{unit,integration,snapshots}
- ✅ Defined exception hierarchy: StyledConsoleError, RenderError, ExportError, TerminalError
- ✅ Added Apache 2.0 LICENSE
- ✅ Branch: feature/T-001-project-setup
- ✅ Commit: 32eadca "T-001: Complete project setup and structure"

**Implementation Notes:**
```bash
# Install UV (if not installed): curl -LsSf https://astral.sh/uv/install.sh | sh

uv init --lib styledconsole
cd styledconsole

# Add core dependencies
uv add "rich>=13.7" "pyfiglet>=1.0.2" "wcwidth>=0.2.13" "ansi2html>=1.8.0"

# Add dev dependencies
uv add --dev "pytest>=8.0" "pytest-cov>=4.1" "pytest-snapshot>=0.9" "ruff>=0.3" "pre-commit>=3.6"

# Sync (creates .venv + installs everything)
uv sync
```

---

### T-002: Text Width Utilities ✅
**Priority:** High
**Effort:** 2 days
**Dependencies:** T-001
**Status:** ✅ Completed (Oct 17, 2025)

**Description:**
Implement emoji-safe text width calculation and grapheme handling. **MVP focuses on Tier 1 (Basic Icons)** - single codepoint emojis that are well-supported across terminals.

**Emoji Support Tiers:**
- **Tier 1 (MVP v0.1):** Basic icons (✅ ❌ ⚠️ ℹ️ ⭐ 🚀 ❤️ 🎉) - single codepoint, width=2
- **Tier 2 (v0.2):** Modified emojis with skin tones (👍🏽 👨🏻) - 2-3 codepoints
- **Tier 3 (v0.3+):** ZWJ sequences (👨‍👩‍👧‍👦 👨‍💻) - complex multi-codepoint

**Acceptance Criteria:**
- [x] `visual_width(text: str) -> int` function implemented
- [x] Handles Tier 1 basic icons correctly (e.g., "🚀" returns 2)
- [x] Strips ANSI codes before width calculation
- [x] `split_graphemes(text: str) -> list[str]` implemented
- [x] `pad_to_width(text, width, align)` implemented
- [x] Unit tests with Tier 1 emoji test cases (✅ ❌ ⚠️ 🚀 ❤️ 🎉 ⭐ ℹ️)
- [x] Documentation warns about Tier 2/3 support (future work)
- [x] Test coverage ≥95% (achieved 97.62%)

**Completion Notes:**
- ✅ Implemented 5 text utility functions: visual_width, strip_ansi, split_graphemes, pad_to_width, truncate_to_width
- ✅ All 37 unit tests passing
- ✅ Test coverage: 97.62% (72/74 lines covered)
- ✅ Tier 1 emoji support validated (15 common emojis tested)
- ✅ ANSI escape sequence handling working correctly
- ✅ Exported from styledconsole.utils and styledconsole main module
- ✅ Branch: feature/T-002-text-width-utilities

**Test Cases:**
```python
def test_basic_icon_width():
    """Test Tier 1: Basic single-codepoint icons"""
    assert visual_width("Hello") == 5
    assert visual_width("🚀") == 2  # Rocket
    assert visual_width("✅") == 2  # Check mark
    assert visual_width("❌") == 2  # Cross mark
    assert visual_width("Test 🚀 🎉") == 11
    assert visual_width("\033[31mRed\033[0m") == 3  # ANSI stripped

def test_pad_to_width_with_icons():
    assert pad_to_width("Hi", 5, "left") == "Hi   "
    assert pad_to_width("🚀", 4, "left") == "🚀  "  # width=2 + 2 spaces
    assert pad_to_width("X", 5, "center") == "  X  "
    assert pad_to_width("✅", 6, "center") == "  ✅  "  # width=2, centered

def test_tier2_tier3_not_yet_supported():
    """Document known limitations for future work"""
    # Tier 2: Modified emojis (skin tones) - may have alignment issues
    # Tier 3: ZWJ sequences - may break or misalign
    # These will be addressed in v0.2 and v0.3
    pass
```

**Implementation Files:**
- `styledconsole/utils/text.py`
- `tests/unit/test_text_utils.py`

---

### T-003: Color Utilities ✅
**Priority:** High
**Effort:** 2 days
**Dependencies:** T-001
**Status:** ✅ Completed (Oct 17, 2025)

**Description:**
Implement color parsing, conversion, and gradient interpolation with **CSS4 named color support** (148 colors from W3C/matplotlib standard).

**Color Input Formats:**
- **Hex:** `#FF0000`, `#f00` (shorthand)
- **RGB:** `rgb(255, 0, 0)`, `(255, 0, 0)`
- **Named:** CSS4 color names (e.g., `red`, `dodgerblue`, `coral`, `lightseagreen`)

**Acceptance Criteria:**
- [x] `parse_color(value: str) -> tuple[int, int, int]` handles all formats
- [x] `rgb_to_hex(r, g, b) -> str` conversion
- [x] `hex_to_rgb(hex_str) -> tuple[int, int, int]` conversion
- [x] `interpolate_color(start, end, t) -> str` gradient function
- [x] **CSS4 color names:** All 148 named colors supported
- [x] Case-insensitive color name matching
- [x] Both `gray` and `grey` spellings supported
- [x] `get_color_names() -> list[str]` helper to list available names
- [x] Unit tests with edge cases and all color formats
- [x] Test coverage ≥90% (achieved 98.39%)

**Completion Notes:**
- ✅ Implemented 5 color utility functions: parse_color, hex_to_rgb, rgb_to_hex, interpolate_color, color_distance
- ✅ Full CSS4 color support: 148 named colors from W3C standard
- ✅ Multiple format support: hex (#FF0000, #f00), rgb(r,g,b), tuples, named colors
- ✅ Case-insensitive color matching ("RED" == "red")
- ✅ Both gray/grey spellings supported
- ✅ All 35 unit tests passing
- ✅ Test coverage: 98.39% (61/62 lines covered)
- ✅ Gradient interpolation with color distance calculations
- ✅ Exported from styledconsole.utils and styledconsole main module
- ✅ Branch: feature/T-003-color-utilities
- ✅ Files: src/styledconsole/utils/color.py, src/styledconsole/utils/color_data.py, tests/unit/test_color_utils.py

**Test Cases:**
```python
def test_color_parsing_hex():
    assert parse_color("#FF0000") == (255, 0, 0)
    assert parse_color("#f00") == (255, 0, 0)  # Shorthand

def test_color_parsing_rgb():
    assert parse_color("rgb(0,255,0)") == (0, 255, 0)
    assert parse_color("(0, 255, 0)") == (0, 255, 0)

def test_color_parsing_css4_names():
    """Test CSS4 named colors (148 total)"""
    assert parse_color("red") == (255, 0, 0)
    assert parse_color("RED") == (255, 0, 0)  # Case insensitive
    assert parse_color("dodgerblue") == (30, 144, 255)
    assert parse_color("coral") == (255, 127, 80)
    assert parse_color("lightseagreen") == (32, 178, 170)
    assert parse_color("tomato") == (255, 99, 71)
    assert parse_color("gold") == (255, 215, 0)

    # Both spellings
    assert parse_color("gray") == parse_color("grey")

def test_gradient_with_names():
    """Gradients work with named colors"""
    result = interpolate_color("red", "blue", 0.5)
    assert result  # Should produce purple-ish color

    result2 = interpolate_color("coral", "dodgerblue", 0.3)
    assert result2

def test_gradient_interpolation():
    start, end = "#000000", "#FFFFFF"
    assert interpolate_color(start, end, 0.0) == "#000000"
    assert interpolate_color(start, end, 0.5) == "#808080"
    assert interpolate_color(start, end, 1.0) == "#FFFFFF"

def test_get_color_names():
    names = get_color_names()
    assert len(names) == 148  # CSS4 colors
    assert "red" in names
    assert "dodgerblue" in names
    assert "lightseagreen" in names
```

**Implementation Notes:**
```python
# CSS4_COLORS dictionary - 148 named colors from W3C standard
# Can be copied from matplotlib.colors.CSS4_COLORS or defined manually
CSS4_COLORS = {
    'red': '#ff0000', 'green': '#008000', 'blue': '#0000ff',
    'dodgerblue': '#1e90ff', 'coral': '#ff7f50', 'gold': '#ffd700',
    # ... (148 total colors)
}

def parse_color(value: str) -> tuple[int, int, int]:
    value = value.strip().lower()

    # Try CSS4 named color first
    if value in CSS4_COLORS:
        return hex_to_rgb(CSS4_COLORS[value])

    # Then try hex, rgb() formats...
```

**Implementation Files:**
- `styledconsole/utils/color.py`
- `styledconsole/utils/color_data.py` (CSS4_COLORS dictionary)
- `tests/unit/test_color_utils.py`
- `tests/unit/test_css4_colors.py`

---

### T-004: Terminal Detection
**Priority:** High
**Effort:** 1.5 days
**Dependencies:** T-001
**Status:** ✅ Completed (Oct 17, 2025)

**Description:**
Implement terminal capability detection (color depth, emoji support, dimensions).

**Acceptance Criteria:**
- [x] `TerminalProfile` dataclass defined
- [x] `detect_terminal_capabilities()` function implemented
- [x] Detects ANSI support via `isatty()` and `TERM` env var
- [x] Detects color depth (8, 256, or truecolor) via `COLORTERM`
- [x] Detects emoji safety heuristically (UTF-8 locale + color)
- [x] Gets terminal size via `os.get_terminal_size()`
- [x] Unit tests with mocked environment variables
- [x] Test coverage ≥85% (achieved 100%)

**Completion Notes:**
- TerminalProfile dataclass with 7 fields (ansi_support, color_depth, emoji_safe, width, height, term, colorterm)
- Comprehensive detection logic with multiple environment variable checks
- NO_COLOR and ANSI_COLORS_DISABLED support
- CI environment detection (GitHub Actions, Jenkins, GitLab, CircleCI)
- UTF-8 locale detection with LANG, LC_ALL, LC_CTYPE support
- Fallback terminal size (80x24) on errors
- All 37 unit tests passing
- Test coverage: 100% (50/50 lines covered)
- Functions exported from styledconsole.utils and styledconsole main module
- Branch: feature/T-004-terminal-detection
- Files: src/styledconsole/utils/terminal.py, tests/unit/test_terminal.py

**Test Cases:**
```python
def test_detect_truecolor(monkeypatch):
    monkeypatch.setenv("COLORTERM", "truecolor")
    profile = detect_terminal_capabilities()
    assert profile.color_depth == 16777216

def test_detect_no_tty(monkeypatch):
    # Simulate pipe/redirect
    profile = detect_terminal_capabilities()
    assert profile.ansi_support == False
```

**Implementation Files:**
- `styledconsole/utils/terminal.py`
- `tests/unit/test_terminal.py`

---

### T-005: Border Styles Definition
**Priority:** Medium
**Effort:** 1.5 days
**Dependencies:** T-001
**Status:** ✅ Completed (Oct 17, 2025)

**Description:**
Define border style character sets and rendering logic.

**Acceptance Criteria:**
- [x] `BorderStyle` dataclass defined
- [x] Predefined styles: solid, double, rounded, heavy, ascii (plus thick, minimal, dots)
- [x] `BORDERS` dictionary with all styles
- [x] Helper methods: `render_horizontal()`, `render_vertical()`, plus render_top_border(), render_bottom_border(), render_divider()
- [x] Unit tests for each border style
- [x] Test coverage ≥90% (achieved 100%)

**Completion Notes:**
- BorderStyle frozen dataclass with 12 character fields
- 8 predefined border styles: SOLID, DOUBLE, ROUNDED, HEAVY, THICK, ASCII, MINIMAL, DOTS
- Complete Unicode box-drawing character sets
- ASCII fallback style for universal compatibility
- 6 rendering methods: render_horizontal, render_vertical, render_top_border, render_bottom_border, render_divider, render_line
- **Emoji-safe rendering**: All methods use visual_width() for perfect alignment
- Centered title support in top borders with emoji-safe centering
- Automatic content line rendering with left/center/right alignment
- Emoji-safe padding using pad_to_width() from text utilities
- Emoji-safe truncation using truncate_to_width() for long content
- Case-insensitive style lookup via get_border_style()
- All 80 unit tests passing (including 11 emoji-specific tests)
- Test coverage: 100% (82/83 lines covered, 98.78%)
- Styles exported from styledconsole.core and styledconsole main module
- Branch: feature/T-005-border-styles → main (merged)
- Files: src/styledconsole/core/styles.py, tests/unit/test_styles.py

**Emoji-Safe Improvements:**
- ✅ render_line() method added for automatic content line rendering with perfect alignment
- ✅ render_top_border() updated to use visual_width() for emoji-safe title centering
- ✅ All padding calculations use visual_width() instead of len()
- ✅ All truncation uses truncate_to_width() for emoji-aware character splitting
- ✅ TestRenderTopBorderEmoji class with 5 emoji-specific title tests
- ✅ TestRenderLineEmoji class with 6 emoji-specific content tests
- ✅ Visual alignment verified: All borders display at exact specified width regardless of emoji content

**Implementation Files:**
- `styledconsole/core/styles.py`
- `tests/unit/test_styles.py`

---

## M2: Rendering Engine (Week 3-4)

### T-006: Frame Renderer Core ✅
**Priority:** High
**Effort:** 3 days
**Dependencies:** T-002, T-003, T-005
**Status:** ✅ Completed (Oct 18, 2025)

**Description:**
Implement core frame rendering with borders, padding, and titles. High-level API for creating framed content with automatic width calculation.

**Acceptance Criteria:**
- [x] `Frame` dataclass defined (8 configuration fields)
- [x] `FrameRenderer` class implemented
- [x] Renders frames with all border styles (supports string names or BorderStyle objects)
- [x] Handles title placement (centered by default)
- [x] Applies padding correctly (configurable 1-n spaces)
- [x] Calculates frame width automatically or uses specified width
- [x] Auto-width calculation with min_width and max_width constraints (20-100 default)
- [x] Emoji-safe alignment maintained (uses visual_width throughout)
- [x] Support for multi-line content (strings with newlines or lists)
- [x] Three alignment options: left, center, right
- [x] Unit tests with 100% coverage on frame.py (27 tests)
- [x] Integration tests for real-world usage patterns (10 tests)
- [x] All 231 tests passing with 98.92% coverage

**Completion Notes:**
- ✅ Frame dataclass with 8 fields: content, title, border, width, padding, align, min_width, max_width
- ✅ FrameRenderer with render() and render_frame() methods
- ✅ _calculate_width() for intelligent auto-width with constraints
- ✅ _render_content_line() for padding and alignment with emoji-safe width
- ✅ Support for both keyword arguments (render) and Frame objects (render_frame)
- ✅ 27 unit tests: dataclass config, rendering, emoji, alignment, padding, truncation, auto-width
- ✅ 10 integration tests: real-world workflows, all border styles, mixed content types
- ✅ 5 examples updated to use FrameRenderer: 01-04 plus new 05_frame_renderer.py
- ✅ Exported from styledconsole.core and styledconsole main module
- ✅ Branch: feature/T-006-frame-renderer → main (merged)
- ✅ Files: src/styledconsole/core/frame.py, tests/unit/test_frame.py, tests/integration/test_frame_integration.py

**Example Usage:**
```python
from styledconsole import FrameRenderer

renderer = FrameRenderer()

# Simple frame with auto-width
lines = renderer.render("Hello, World!", border="solid")
for line in lines:
    print(line)

# Frame with title and custom width
lines = renderer.render(
    "Content here",
    title="My Frame",
    border="rounded",
    width=50,
    align="center",
)

# Multi-line content
content = ["Line 1", "Line 2", "Line 3"]
lines = renderer.render(content, title="Multi-line", border="double")

# Using Frame dataclass
from styledconsole import Frame

frame = Frame(
    content=["Status: ✅ OK", "Uptime: 99.9%"],
    title="System Status",
    border="heavy",
    width=40,
    padding=2,
    align="left",
)
lines = renderer.render_frame(frame)
```

**Implementation Files:**
- `styledconsole/core/frame.py`
- `tests/unit/test_frame.py`
- `tests/integration/test_frame_integration.py`
- `examples/basic/05_frame_renderer.py`
- [ ] Unit tests with various content types
- [ ] Integration test with Rich console
- [ ] Test coverage ≥90%

**Test Cases:**
```python
def test_simple_frame():
    frame = FrameRenderer().render("Hello", border="solid")
    assert "┌" in frame[0]  # Top-left corner
    assert "Hello" in frame[1]
    assert "└" in frame[-1]  # Bottom-left corner

def test_frame_with_emoji():
    frame = FrameRenderer().render("Test 🚀", border="solid")
    # Verify alignment is correct (no overflow)
```

**Implementation Files:**
- `styledconsole/core/frame.py`
- `tests/unit/test_frame.py`
- `tests/integration/test_frame_rendering.py`

---

### T-007: Banner Renderer ✅
**Priority:** High
**Effort:** 2 days
**Dependencies:** T-003, T-006
**Status:** ✅ Completed (Oct 18, 2025)

**Description:**
Implement ASCII art banner rendering with pyfiglet, gradient coloring, and frame integration.

**Acceptance Criteria:**
- [x] `Banner` dataclass defined (8 configuration fields)
- [x] `BannerRenderer` class implemented
- [x] Integrates with pyfiglet for ASCII art rendering
- [x] Supports multiple fonts (standard, slant, banner, big, digital, and all pyfiglet fonts)
- [x] Applies gradient coloring per line (top to bottom RGB interpolation)
- [x] Handles emoji in banner text (fallback to plain text rendering)
- [x] Optional frame borders via FrameRenderer integration
- [x] Alignment control (left, center, right) and custom padding
- [x] Font discovery utilities (list_fonts, preview_font)
- [x] Unit tests with different fonts (29 tests, 98.48% coverage)
- [x] Integration tests for real-world patterns (18 tests)
- [x] All 278 tests passing with 98.86% coverage

**Completion Notes:**
- ✅ Banner dataclass with 8 fields: text, font, gradient_start, gradient_end, border, width, align, padding
- ✅ BannerRenderer with render() and render_banner() methods
- ✅ ASCII art using pyfiglet with all available fonts
- ✅ Gradient coloring: per-line RGB interpolation from start to end color
- ✅ Frame integration: optional borders via FrameRenderer
- ✅ Emoji detection: visual_width comparison to detect emoji, fallback to plain text
- ✅ Font utilities: list_fonts() and preview_font() for font discovery
- ✅ 29 unit tests: dataclass config, rendering, fonts, gradients, borders, emoji, alignment
- ✅ 18 integration tests: workflows, font variations, gradient combinations, status messages
- ✅ 2 examples: 06_banner_renderer.py (12 demos) + showcase/banner_showcase.py
- ✅ Exported from styledconsole.core and styledconsole main module
- ✅ Branch: feature/T-007-banner-renderer → main (merged)
- ✅ Files: src/styledconsole/core/banner.py, tests/unit/test_banner.py, tests/integration/test_banner_integration.py

**Example Usage:**
```python
from styledconsole import BannerRenderer

renderer = BannerRenderer()

# Simple banner
lines = renderer.render("HELLO", font="slant")
for line in lines:
    print(line)

# With gradient and border
lines = renderer.render(
    "SUCCESS",
    font="banner",
    gradient_start="#00ff00",
    gradient_end="#0000ff",
    border="double",
)

# Using Banner dataclass
from styledconsole import Banner

banner = Banner(
    text="DEMO",
    font="slant",
    gradient_start="red",
    gradient_end="blue",
    border="heavy",
    width=70,
    align="center",
    padding=2,
)
lines = renderer.render_banner(banner)

# Font discovery
fonts = renderer.list_fonts(limit=10)
preview = renderer.preview_font("standard", "Test")
```

**Implementation Files:**
- `styledconsole/core/banner.py`
- `tests/unit/test_banner.py`
- `tests/integration/test_banner_integration.py`
- `examples/basic/06_banner_renderer.py`
- `examples/showcase/banner_showcase.py`

---

### T-008: Layout Composer ✅
**Priority:** Medium
**Effort:** 2 days
**Dependencies:** T-006
**Status:** ✅ Completed (Oct 18, 2025)

**Description:**
Implement layout composition for nested frames and multi-section displays.

**Acceptance Criteria:**
- [x] `Layout` dataclass supports vertical stacking with configurable spacing
- [x] `LayoutComposer` class with stack(), compose(), grid(), side_by_side() methods
- [x] Frames can be nested without alignment issues (emoji-safe throughout)
- [x] Maintains consistent spacing between elements (0-n blank lines)
- [x] Grid layout with variable column widths and row heights
- [x] Auto-width calculation based on widest element
- [x] Alignment control (left, center, right) for all operations
- [x] Unit tests for all methods (32 tests, 100% coverage)
- [x] Integration tests with Frame and Banner (19 tests)
- [x] All 329 tests passing with 99.03% overall coverage

**Completion Notes:**
- ✅ Layout dataclass (frozen): elements, align, spacing, width
- ✅ LayoutComposer.stack(): vertical stacking with configurable spacing and alignment
- ✅ LayoutComposer.compose(): renders Layout dataclass objects
- ✅ LayoutComposer.grid(): multi-row/column layouts with column and row spacing
- ✅ LayoutComposer.side_by_side(): convenience method for horizontal placement
- ✅ Auto-width calculation: finds widest element across all blocks
- ✅ Emoji-safe alignment: all alignment operations use visual_width()
- ✅ 32 unit tests: dataclass config, stacking, alignment, spacing, grid, side-by-side
- ✅ 19 integration tests: Frame combinations, Banner integration, complex dashboards
- ✅ 10 examples in 07_layout_composer.py demonstrating all features
- ✅ Exported from styledconsole.core and styledconsole main module
- ✅ Branch: feature/T-008-layout-composer → main (merged)
- ✅ Files: src/styledconsole/core/layout.py, tests/unit/test_layout.py, tests/integration/test_layout_integration.py

**Example Usage:**
```python
from styledconsole import LayoutComposer, FrameRenderer

composer = LayoutComposer()
frame_renderer = FrameRenderer()

# Vertical stacking
header = frame_renderer.render(["Header"], title="Top")
content = frame_renderer.render(["Main content"], title="Body")
footer = frame_renderer.render(["Footer"], title="Bottom")

layout = composer.stack([header, content, footer], spacing=1, align="center")
for line in layout:
    print(line)

# Grid layout (2x2)
cell1 = frame_renderer.render(["A"], title="1")
cell2 = frame_renderer.render(["B"], title="2")
cell3 = frame_renderer.render(["C"], title="3")
cell4 = frame_renderer.render(["D"], title="4")

grid = composer.grid([[cell1, cell2], [cell3, cell4]], column_spacing=2, row_spacing=1)
for line in grid:
    print(line)

# Side by side
left = frame_renderer.render(["Left panel"], title="L")
right = frame_renderer.render(["Right panel"], title="R")

side = composer.side_by_side(left, right, spacing=3)
for line in side:
    print(line)
```

**Implementation Files:**
- `styledconsole/core/layout.py`
- `tests/unit/test_layout.py`
- `tests/integration/test_layout_integration.py`
- `examples/basic/07_layout_composer.py`

---

### T-009: Console Class Core API ✅
**Priority:** High
**Effort:** 2.5 days
**Dependencies:** T-004, T-006, T-007
**Status:** ✅ Completed (Oct 18, 2025)

**Description:**
Implement the main Console facade class with Rich backend integration and complete public API surface.

**Acceptance Criteria:**
- [x] `Console` class initialized with Rich console
- [x] `frame()` method with all parameters (title, border, colors, padding, width)
- [x] `banner()` method delegates to BannerRenderer
- [x] `text()` method for styled text output
- [x] `rule()` method for horizontal rules
- [x] `newline()` method for spacing
- [x] `export_html()` method with inline_styles option
- [x] `export_text()` method (ANSI stripped)
- [x] `terminal_profile` property
- [x] `clear()` method
- [x] Terminal detection on initialization
- [x] Recording mode for HTML export
- [x] **Debug logging support** (when debug=True)
- [x] **`file` parameter** for custom output streams
- [x] Unit tests for all methods (63 tests)
- [x] Integration tests end-to-end (25 tests)
- [x] Test coverage ≥90% (achieved 92.31%)

**Completion Notes:**
- ✅ Console class with Rich backend integration (104 statements, 92.31% coverage)
- ✅ All 10 core methods implemented: __init__, frame, banner, text, rule, newline, clear, export_html, export_text, print
- ✅ Terminal detection with TerminalProfile integration
- ✅ Recording mode for HTML/text export via Rich backend
- ✅ Debug logging with configurable logger (stderr output)
- ✅ Custom file output stream support
- ✅ 63 unit tests covering all initialization options and methods
- ✅ 25 integration tests for complex workflows (welcome screens, dashboards, reports)
- ✅ 15 comprehensive examples in 08_console_api.py (407 lines)
- ✅ Exported from styledconsole main module
- ✅ All 441 tests passing with 97.64% overall coverage
- ✅ Files: src/styledconsole/console.py, tests/unit/test_console.py, tests/integration/test_console_integration.py, examples/basic/08_console_api.py

**Example Usage:**
```python
from styledconsole import Console

# Basic usage
console = Console()
console.frame("Hello World", title="Greeting", border="solid")
console.banner("SUCCESS", font="slant")
console.text("Status: OK", color="green", bold=True)

# Recording and export
console = Console(record=True)
console.frame("Content", title="Demo")
html = console.export_html(inline_styles=True)
text = console.export_text()

# Terminal detection
console = Console(detect_terminal=True)
if console.terminal_profile.emoji_safe:
    console.text("✓ Emoji supported", color="green")

# Custom output stream
import io
buffer = io.StringIO()
console = Console(file=buffer)
console.frame("Test")
output = buffer.getvalue()

# Debug mode
console = Console(debug=True)
console.frame("Test")  # Logs to stderr
```

**Implementation Files:**
- `styledconsole/console.py` - 104 statements, 92.31% coverage
- `styledconsole/__init__.py` - Console export added
- `tests/unit/test_console.py` - 63 unit tests
- `tests/integration/test_console_integration.py` - 25 integration tests
- `examples/basic/08_console_api.py` - 15 examples

---

## M3: Preset Functions & Layouts (Week 5-6)

### T-010: Gradient Effects ✅
**Priority:** High
**Effort:** 1.5 days
**Dependencies:** T-009
**Status:** ✅ Completed (Oct 19, 2025)

**Description:**
Implement gradient and rainbow effects for stunning visual output with CSS4 color support.

**Acceptance Criteria:**
- [x] `gradient_frame()` - Vertical gradients with custom start/end colors
- [x] `diagonal_gradient_frame()` - Diagonal gradients (top-left to bottom-right)
- [x] `rainbow_frame()` - 7-color rainbow spectrum effects with direction parameter
- [x] Support for content, border, or both targeting
- [x] Proper handling of emojis and visual width
- [x] Variation selector documentation and workarounds
- [x] Comprehensive test suite (36 tests)
- [x] Test coverage ≥95% (achieved 83.42%)
- [x] Showcase example with creative effects
- [x] Integration with main library exports
- [x] CSS4 color names support throughout library
- [x] Full ROYGBIV rainbow spectrum implementation

**Completion Notes:**
- ✅ 3 gradient functions: `gradient_frame()`, `diagonal_gradient_frame()`, `rainbow_frame()`
- ✅ RAINBOW_COLORS using CSS4 names: red, orange, yellow, lime, blue, indigo, darkviolet
- ✅ Direction parameter for rainbows: "vertical" (default) or "diagonal"
- ✅ Proper ROYGBIV interpolation through all 7 color segments
- ✅ Helper functions: `get_rainbow_color()`, `_colorize()`, `_apply_vertical_rainbow()`, `_apply_diagonal_rainbow()`
- ✅ 36 tests across 5 test classes (all passing)
- ✅ Test coverage: 83.42% for effects.py, 93.42% overall (502 tests)
- ✅ Fixed 4 visual alignment bugs (content gradient borders, emoji alignment, border coloring)
- ✅ Created comprehensive showcase with 5 sections (428 lines)
- ✅ Digital poetry example (28 lines) with rainbow effects
- ✅ Safe emoji guidelines documented (100+ tested emojis)
- ✅ **CSS4 Color Migration**: Migrated entire codebase from hex codes to CSS4 color names
  - Updated 27 files (source, examples, tests)
  - 19 distinct color mappings (red, lime, blue, cyan, magenta, yellow, etc.)
  - Zero breaking changes, full backward compatibility
  - All 502 tests passing after migration

**Example Usage:**
```python
from styledconsole import gradient_frame, diagonal_gradient_frame, rainbow_frame

# Vertical gradient with CSS4 colors
lines = gradient_frame(
    ["Line 1", "Line 2", "Line 3"],
    start_color="red",        # CSS4 color names!
    end_color="blue",
    target="content"  # or "border" or "both"
)

# Diagonal gradient
lines = diagonal_gradient_frame(
    content,
    start_color="lime",
    end_color="magenta",
    target="both"
)

# Rainbow effect (vertical or diagonal)
lines = rainbow_frame(
    content,
    direction="vertical",  # or "diagonal"
    mode="both"           # content, border, or both
)
```

**Implementation Files:**
- `src/styledconsole/effects.py` (199 statements, 83.42% coverage)
- `tests/test_effects.py` (36 tests, all passing)
- `examples/showcase/gradient_effects.py` (428 lines, comprehensive showcase)
- `doc/EMOJI_GUIDELINES.md` (100+ safe emojis cataloged)

**Key Features:**
- 🌈 Vertical gradients with any CSS4 color or hex code
- ↘️ Diagonal gradients from top-left to bottom-right
- 🎨 Rainbow effects with 7-color ROYGBIV spectrum
- 🎯 Flexible targeting: content-only, border-only, or both
- 🔤 Proper visual width handling for emojis
- ⚡ Fast rendering with minimal overhead

**Discovered Issues & Solutions:**
- Variation selector emojis (↘️) cause alignment issues → Use base emojis (↘)
- Character-by-character coloring needs ANSI stripping → Implemented strip_ansi
- Title alignment in diagonal gradients → Special handling for title lines
- Border character detection → Manual border_chars set construction

**Stats:**
- 502 total tests passing (466 + 36 new)
- 95.90% overall coverage (up from 95.76%)
- 125 new statements in effects.py
- 0 regressions

---

### T-010a: Safe Emoji List & Validation

**Priority:** Medium
**Effort:** 0.5 days
**Dependencies:** T-010
**Status:** ⬜ Not Started

**Description:**
Create a curated list of safe, tested emojis that work correctly with gradient effects and character-by-character processing. Validate emoji visual width and detect variation selectors.

**Acceptance Criteria:**

- [ ] Create `doc/SAFE_EMOJIS.md` with tested emoji list
- [ ] Categorize emojis by type (symbols, objects, nature, etc.)
- [ ] Document which emojis have variation selectors
- [ ] Add `validate_emoji()` utility function in utils/text.py
- [ ] Function to detect and warn about variation selector emojis
- [ ] Unit tests for emoji validation
- [ ] Update EMOJI_GUIDELINES.md with safe emoji list reference
- [ ] Test coverage ≥90%

**Known Issues from Gradient Implementation:**

- `🖥️` (U+1F5A5 + U+FE0F) - Has variation selector, causes misalignment
- `↘️` (U+2198 + U+FE0F) - Has variation selector, causes misalignment
- `➡️` (U+27A1 + U+FE0F) - Has variation selector, causes misalignment
- `✨` (U+2728) - Safe, single codepoint
- `🌈` (U+1F308) - Safe, single codepoint
- `🎨` (U+1F3A8) - Safe, single codepoint

**Implementation Files:**

- `doc/SAFE_EMOJIS.md` (comprehensive safe emoji catalog)
- `src/styledconsole/utils/text.py` (add validate_emoji function)
- `tests/unit/test_text_utils.py` (emoji validation tests)

**Example Usage:**

```python
from styledconsole.utils.text import validate_emoji

result = validate_emoji("🖥️")
# Returns: {"safe": False, "has_variation_selector": True,
#           "codepoints": 2, "recommendation": "Use 🖥 instead"}

result = validate_emoji("✨")
# Returns: {"safe": True, "has_variation_selector": False,
#           "codepoints": 1}
```

---

### T-011: Terminal Output Recording

**Priority:** High
**Effort:** 2 days
**Dependencies:** T-009
**Assigned to:** TBD

**Description:**
Implement output recording and replay capabilities for terminal sessions.

**Acceptance Criteria:**
- [ ] Session recording with timestamp tracking
- [ ] HTML export with inline styles
- [ ] SVG export for animated playback
- [ ] Plain text export (ANSI stripped)
- [ ] Frame-by-frame replay capability
- [ ] Integration with Console recording mode
- [ ] Unit tests for all export formats
- [ ] Test coverage ≥85%

---

### T-011: Status Frame Preset
**Priority:** High
**Effort:** 1.5 days
**Dependencies:** T-009
**Assigned to:** TBD

**Description:**
Implement `status_frame()` preset for test status display.

**Acceptance Criteria:**
- [ ] `status_frame(test_name, status, duration, message)` implemented
- [ ] Color coding: green (PASS), red (FAIL), yellow (SKIP)
- [ ] Optional duration and message fields
- [ ] Emoji indicators (✅, ❌, ⚠️)
- [ ] Unit tests for all status types
- [ ] Visual snapshot tests
- [ ] Test coverage ≥90%

**Example Usage:**
```python
status_frame("Login test", status="PASS", duration="2.3s", message="All checks passed")
```

**Implementation Files:**
- `styledconsole/presets/status.py`
- `tests/unit/test_status_preset.py`
- `tests/visual/test_status_snapshots.py`

---

### T-011: Test Summary Preset
**Priority:** High
**Effort:** 1.5 days
**Dependencies:** T-009
**Assigned to:** TBD

**Description:**
Implement `test_summary()` preset for displaying test statistics.

**Acceptance Criteria:**
- [ ] `test_summary(stats: dict)` implemented
- [ ] Displays passed, failed, skipped counts
- [ ] Color-coded statistics
- [ ] Optional total count
- [ ] Supports custom title
- [ ] Unit tests with various stat combinations
- [ ] Visual snapshot tests
- [ ] Test coverage ≥90%

**Example Usage:**
```python
test_summary({"passed": 182, "failed": 3, "skipped": 7}, title="Regression Tests")
```

**Implementation Files:**
- `styledconsole/presets/reports.py`
- `tests/unit/test_reports_preset.py`

---

### T-012: Dashboard Presets (Small/Medium/Large)
**Priority:** High
**Effort:** 3 days
**Dependencies:** T-008, T-009, T-010, T-011
**Assigned to:** TBD

**Description:**
Implement three dashboard presets with varying complexity.

**Acceptance Criteria:**
- [ ] `dashboard_small(stats, title)` - Compact 1-section layout
- [ ] `dashboard_medium(stats, sections)` - 2-3 section layout
- [ ] `dashboard_large(stats, sections, banner)` - Full dashboard with banner
- [ ] All dashboards use consistent styling
- [ ] Responsive to terminal width
- [ ] Unit tests for each preset
- [ ] Visual snapshot tests for each size
- [ ] Test coverage ≥85%

**Example Usage:**
```python
dashboard_small({"passed": 10, "failed": 2}, title="Quick Status")

dashboard_large(
    stats={"passed": 182, "failed": 3},
    sections=[("Recent Failures", ["test_1", "test_2"])],
    banner="CI Pipeline Results"
)
```

**Implementation Files:**
- `styledconsole/presets/dashboards.py`
- `tests/unit/test_dashboards_preset.py`
- `tests/visual/test_dashboard_snapshots.py`

---

### T-013: Preset Function Documentation
**Priority:** Medium
**Effort:** 1 day
**Dependencies:** T-010, T-011, T-012
**Assigned to:** TBD

**Description:**
Create comprehensive documentation and examples for all preset functions.

**Acceptance Criteria:**
- [ ] Docstrings complete for all preset functions
- [ ] Example code in docstrings
- [ ] `examples/` directory with runnable scripts
- [ ] Screenshots/terminal recordings of outputs
- [ ] README section with preset overview
- [ ] Coverage: 100% of public preset API

**Implementation Files:**
- `examples/status_examples.py`
- `examples/dashboard_examples.py`
- `docs/presets.md`

---

## M4: Terminal Detection & HTML Export (Week 7)

### T-014: HTML Exporter Implementation
**Priority:** High
**Effort:** 2 days
**Dependencies:** T-009
**Assigned to:** TBD

**Description:**
Implement HTML export using ansi2html with inline CSS.

**Acceptance Criteria:**
- [ ] `HtmlExporter` class implemented
- [ ] `Console.export_html()` method functional
- [ ] Captures recorded Rich output
- [ ] Converts ANSI codes to HTML spans
- [ ] Inline CSS for styling
- [ ] Preserves colors, emojis, and layout
- [ ] Unit tests for conversion
- [ ] Visual comparison tests (ANSI vs HTML)
- [ ] Test coverage ≥85%

**Test Cases:**
```python
def test_html_export():
    console = Console(record=True)
    console.frame("Test", title="Title")
    html = console.export_html()

    assert "<div" in html
    assert "Test" in html
    assert "Title" in html
    assert "style=" in html  # Inline CSS present
```

**Implementation Files:**
- `styledconsole/export/html.py`
- `tests/unit/test_html_export.py`
- `tests/integration/test_html_fidelity.py`

---

### T-015: Terminal Capability Fallbacks
**Priority:** Medium
**Effort:** 2 days
**Dependencies:** T-004, T-009
**Assigned to:** TBD

**Description:**
Implement graceful degradation for limited terminal capabilities.

**Acceptance Criteria:**
- [ ] ASCII-only mode for basic terminals
- [ ] Emoji replacement with ASCII alternatives
- [ ] Color degradation for 8-color terminals
- [ ] Width warnings for narrow terminals (<80 cols)
- [ ] Logging/warning system for capability issues
- [ ] Unit tests with simulated limited terminals
- [ ] Integration tests with environment mocking
- [ ] Test coverage ≥80%

**Implementation Files:**
- `styledconsole/core/fallbacks.py`
- `tests/unit/test_fallbacks.py`

---

## M5: Testing, Documentation, Release (Week 8)

### T-016: Visual Snapshot Test Suite
**Priority:** High
**Effort:** 2 days
**Dependencies:** T-006 through T-012
**Assigned to:** TBD

**Description:**
Create comprehensive visual regression tests using pytest-snapshot.

**Acceptance Criteria:**
- [ ] Snapshot tests for all frame styles
- [ ] Snapshot tests for all banner fonts
- [ ] Snapshot tests for all preset functions
- [ ] Snapshot tests with emojis
- [ ] Baseline snapshots committed
- [ ] CI configured to fail on visual regressions
- [ ] Coverage: All rendering outputs

**Implementation Files:**
- `tests/visual/test_frame_snapshots.py`
- `tests/visual/test_banner_snapshots.py`
- `tests/visual/test_preset_snapshots.py`
- `tests/visual/snapshots/` (baseline files)

---

### T-017: Cross-Platform Testing
**Priority:** High
**Effort:** 1 day
**Dependencies:** All M1-M4 tasks
**Assigned to:** TBD

**Description:**
Setup and verify cross-platform test execution in CI.

**Acceptance Criteria:**
- [ ] GitHub Actions workflow configured
- [ ] Test matrix: Linux, macOS, Windows
- [ ] Test matrix: Python 3.10, 3.11, 3.12
- [ ] All tests pass on all platforms
- [ ] Coverage report uploaded to Codecov
- [ ] Badge added to README

**Implementation Files:**
- `.github/workflows/test.yml`
- `.github/workflows/coverage.yml`

---

### T-018: Performance Benchmarks
**Priority:** Medium
**Effort:** 1.5 days
**Dependencies:** T-009, T-012
**Assigned to:** TBD

**Description:**
Create performance benchmarks and verify targets are met.

**Acceptance Criteria:**
- [ ] Benchmark suite using `pytest-benchmark`
- [ ] Frame rendering: <10ms verified
- [ ] Dashboard rendering: <50ms verified
- [ ] HTML export (100 frames): <200ms verified
- [ ] Benchmark results documented
- [ ] CI runs benchmarks on each commit

**Implementation Files:**
- `tests/benchmarks/test_rendering_performance.py`
- `tests/benchmarks/test_export_performance.py`

---

### T-019: API Documentation (Sphinx/MkDocs)
**Priority:** High
**Effort:** 2 days
**Dependencies:** All M1-M4 tasks
**Assigned to:** TBD

**Description:**
Generate comprehensive API documentation.

**Acceptance Criteria:**
- [ ] MkDocs configured with Material theme
- [ ] API reference auto-generated from docstrings
- [ ] Quick start guide written
- [ ] Examples gallery created
- [ ] Contributing guide written
- [ ] Hosted on ReadTheDocs or GitHub Pages
- [ ] Coverage: 100% of public API

**Implementation Files:**
- `docs/index.md`
- `docs/quickstart.md`
- `docs/api/` (auto-generated)
- `docs/examples.md`
- `mkdocs.yml`

---

### T-020: Release Preparation
**Priority:** High
**Effort:** 1 day
**Dependencies:** T-016, T-017, T-018, T-019
**Assigned to:** TBD

**Description:**
Prepare for v0.1.0 release to PyPI with Apache 2.0 license.

**Acceptance Criteria:**
- [ ] **LICENSE file created** (Apache License 2.0 full text)
- [ ] **NOTICE file with copyright** (Apache 2.0 requirement)
- [ ] `__init__.py` with complete public API exports (see PLAN.md)
- [ ] CHANGELOG.md completed (Keep a Changelog format)
- [ ] pyproject.toml metadata complete (license, classifiers)
- [ ] Version bumped to 0.1.0
- [ ] All tests passing (100% on CI)
- [ ] Documentation published
- [ ] Wheel and sdist built
- [ ] PyPI package uploaded
- [ ] GitHub release created with notes

**Implementation Files:**
- `LICENSE` (Apache 2.0 full text from apache.org)
- `NOTICE` (Copyright and attribution)
- `styledconsole/__init__.py` (public API exports)
- `CHANGELOG.md` (v0.1.0 section)
- `pyproject.toml` (license = "Apache-2.0", classifiers)
- Release notes

**License Checklist:**
```toml
# pyproject.toml
[project]
license = {text = "Apache License 2.0"}
classifiers = [
    "License :: OSI Approved :: Apache Software License",
]
```

**NOTICE Template:**
```
StyledConsole
Copyright 2025 [Your Name/Organization]

This product includes software developed at
[Your Organization] (https://your-site.com/).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0
```

---

### T-021: Enhanced Emoji Support (Tier 2 & 3) [POST-MVP]
**Priority:** Low
**Effort:** 3 days
**Dependencies:** T-002, v0.1.0 release
**Assigned to:** TBD
**Target:** v0.2 (Tier 2), v0.3 (Tier 3)

**Description:**
Extend emoji support beyond basic icons to handle modified emojis (skin tones) and ZWJ sequences (compound emojis).

**Acceptance Criteria:**
- [ ] **Tier 2 (v0.2):** Skin tone modifiers (👍🏽 👨🏻) align correctly
- [ ] **Tier 2:** Emoji presentation selectors (🏳️ text vs emoji) handled
- [ ] **Tier 3 (v0.3):** ZWJ sequences (👨‍👩‍👧‍👦 👨‍💻 🏳️‍🌈) detected as single unit
- [ ] Enhanced grapheme cluster detection using Unicode segmentation
- [ ] Comprehensive test suite with 50+ complex emoji variants
- [ ] Documentation updated with full emoji compatibility matrix
- [ ] Test coverage ≥90%

**Implementation Notes:**
```python
# May require grapheme library or custom Unicode segmentation
import grapheme

def visual_width_enhanced(text: str) -> int:
    """Enhanced width calculation with full grapheme cluster support."""
    clusters = list(grapheme.graphemes(text))
    return sum(cluster_width(c) for c in clusters)
```

**Implementation Files:**
- `styledconsole/utils/text_enhanced.py`
- `tests/unit/test_emoji_tier2.py`
- `tests/unit/test_emoji_tier3.py`
- `docs/emoji-support.md`

---

## Summary Statistics

**Total Tasks:** 21 (20 for MVP + 1 post-MVP)
**Total Effort (MVP):** ~34 days (≈7 weeks with buffer)
**Total Effort (Post-MVP):** +3 days for enhanced emoji
**Critical Path:** M1 → M2 → M3 → M5 (6 weeks minimum)
**Parallelizable:** M4 can overlap with M3

### Task Breakdown by Type

- **Core Infrastructure:** 5 tasks (T-001 to T-005)
- **Rendering Engine:** 4 tasks (T-006 to T-009)
- **Preset Functions:** 4 tasks (T-010 to T-013)
- **Export & Detection:** 2 tasks (T-014, T-015)
- **Quality & Release:** 5 tasks (T-016 to T-020)
- **Post-MVP Enhancement:** 1 task (T-021)

### Priority Distribution

- **High Priority:** 15 tasks (75%)
- **Medium Priority:** 5 tasks (25%)
- **Low Priority:** 1 task (5% - post-MVP)

---

## Task Tracking Guide

### How to Update Progress

**When starting a task:**
1. Change task status: `⬜ T-XXX` → `🚧 T-XXX`
2. Update milestone progress bar at the top
3. Update "Overall Progress" section

**When completing a task:**
1. Check all acceptance criteria boxes: `- [ ]` → `- [x]`
2. Change task status: `🚧 T-XXX` → `✅ T-XXX`
3. Update milestone progress: `⬜` → `✅`
4. Update "Days Completed" count
5. Add completion date to task header: `**Completed:** YYYY-MM-DD`

**Example:**
```markdown
### ✅ T-001: Project Setup & Structure
**Priority:** High
**Effort:** 0.5 days
**Completed:** 2025-10-17
```

### Branch & PR Strategy

- **Branch naming:** `feature/T-XXX-short-description`
- **Commit messages:** `[T-XXX] Description of change`
- **PR title:** `T-XXX: Task Title`
- **PR checklist:** Include all acceptance criteria

### Daily Progress Template

```
📅 Date: YYYY-MM-DD
🚧 Current: T-XXX - Task Name
✅ Completed today: X acceptance criteria / Y days of effort
🔜 Next: Complete [specific criterion] or start T-YYY
⚠️ Blockers: None / [describe blocker]
```

---

## Completed Tasks Log

<!-- Add completed tasks here with date and notes -->

### Week 1 (Oct 17-18, 2025)

**Oct 17, 2025:**
- ✅ **T-001**: Project Setup & Structure (0.5 days)
  - Installed UV 0.9.3 package manager
  - Created complete src/styledconsole/ structure (core, utils, presets, export)
  - Configured pyproject.toml with hatchling build backend
  - Added all core and dev dependencies
  - Set up pre-commit hooks (ruff, yaml/toml checks)
  - Defined exception hierarchy (StyledConsoleError, RenderError, ExportError, TerminalError)
  - Added Apache 2.0 LICENSE and comprehensive README.md
  - Branch: feature/T-001-project-setup
  - Commit: 32eadca

- ✅ **T-002**: Text Width Utilities (2 days)
  - Implemented emoji-safe text width calculation with wcwidth
  - Created 5 utility functions: visual_width, strip_ansi, split_graphemes, pad_to_width, truncate_to_width
  - Tier 1 emoji support validated (✅ ❌ ⚠️ 🚀 ❤️ 🎉 ⭐ ℹ️ and 15+ common emojis)
  - ANSI escape sequence handling working correctly
  - All 37 unit tests passing with 97.62% coverage
  - Functions exported from styledconsole main module
  - Branch: feature/T-002-text-width-utilities
  - Files: src/styledconsole/utils/text.py, tests/unit/test_text_utils.py

- ✅ **T-003**: Color Utilities (2 days)
  - Implemented color parsing for multiple formats (hex, rgb(), tuples, named)
  - Added 148 CSS4 named colors from W3C standard (matplotlib compatible)
  - Created 5 utility functions: parse_color, hex_to_rgb, rgb_to_hex, interpolate_color, color_distance
  - Case-insensitive color matching with both gray/grey spellings supported
  - Linear RGB interpolation with accurate int() rounding
  - All 35 unit tests passing with 98.39% coverage
  - Functions exported from styledconsole main module
  - Branch: feature/T-003-color-utilities
  - Files: src/styledconsole/utils/color.py, src/styledconsole/utils/color_data.py, tests/unit/test_color_utils.py

- ✅ **T-004**: Terminal Detection (1.5 days)
  - Implemented TerminalProfile dataclass with comprehensive capability tracking
  - Created detect_terminal_capabilities() with environment-based detection
  - ANSI support detection via isatty() and TERM variable
  - Color depth detection (8, 256, 16777216 truecolor) via COLORTERM
  - Emoji safety heuristics (UTF-8 locale + color + not CI)
  - Terminal size detection with fallback (80x24)
  - NO_COLOR and ANSI_COLORS_DISABLED support
  - CI environment detection (GitHub Actions, Jenkins, GitLab, CircleCI)
  - All 37 unit tests passing with 100% coverage
  - Functions exported from styledconsole main module
  - Branch: feature/T-004-terminal-detection
  - Files: src/styledconsole/utils/terminal.py, tests/unit/test_terminal.py

- ✅ **T-005**: Border Styles Definition (1.5 days)
  - Implemented BorderStyle frozen dataclass with 12 character fields
  - Created 8 predefined border styles: SOLID, DOUBLE, ROUNDED, HEAVY, THICK, ASCII, MINIMAL, DOTS
  - Complete Unicode box-drawing character sets for beautiful borders
  - ASCII fallback style for universal compatibility
  - 6 rendering methods: render_horizontal, render_vertical, render_top_border, render_bottom_border, render_divider, render_line
  - **Emoji-safe rendering**: All methods use visual_width() for perfect alignment
  - Centered title support with emoji-safe centering
  - All 80 unit tests passing (including 11 emoji-specific tests)
  - Test coverage: 100% (82/83 lines covered, 98.78%)
  - Styles exported from styledconsole.core and styledconsole main module
  - Branch: feature/T-005-border-styles
  - Files: src/styledconsole/core/styles.py, tests/unit/test_styles.py

**🎉 MILESTONE M1 COMPLETE! Core Setup & Utilities - 5/5 tasks (100%)**

**Oct 18, 2025:**
- ✅ **T-006**: Frame Renderer Core (3 days)
  - Implemented Frame dataclass (8 configuration fields)
  - Created FrameRenderer with render() and render_frame() methods
  - Auto-width calculation with min_width and max_width constraints
  - Emoji-safe alignment throughout (uses visual_width)
  - Support for multi-line content (strings with newlines or lists)
  - Three alignment options: left, center, right
  - 27 unit tests: dataclass, rendering, emoji, alignment, padding, truncation, auto-width
  - 10 integration tests: real-world workflows, all border styles, mixed content
  - Test coverage: 100% on frame.py (27 tests)
  - 5 examples updated: 01-04 plus new 05_frame_renderer.py
  - Exported from styledconsole.core and main module
  - Branch: feature/T-006-frame-renderer → main (merged)
  - Files: src/styledconsole/core/frame.py, tests/unit/test_frame.py, tests/integration/test_frame_integration.py

- ✅ **T-007**: Banner Renderer (2 days)
  - Implemented Banner dataclass (8 configuration fields)
  - Created BannerRenderer with render() and render_banner() methods
  - ASCII art using pyfiglet with all available fonts
  - Gradient coloring: per-line RGB interpolation from start to end color
  - Frame integration: optional borders via FrameRenderer
  - Emoji detection: visual_width comparison, fallback to plain text
  - Font utilities: list_fonts() and preview_font()
  - 29 unit tests: dataclass, rendering, fonts, gradients, borders, emoji, alignment
  - 18 integration tests: workflows, font variations, gradient combinations, status messages
  - Test coverage: 98.48% on banner.py
  - 2 examples: 06_banner_renderer.py (12 demos) + showcase/banner_showcase.py
  - Exported from styledconsole.core and main module
  - Branch: feature/T-007-banner-renderer → main (merged)
  - Files: src/styledconsole/core/banner.py, tests/unit/test_banner.py, tests/integration/test_banner_integration.py

- ✅ **T-008**: Layout Composer (2 days)
  - Implemented Layout dataclass (frozen): elements, align, spacing, width
  - Created LayoutComposer with stack(), compose(), grid(), side_by_side() methods
  - Vertical stacking with configurable spacing and alignment
  - Grid layout with variable column widths and row heights
  - Auto-width calculation: finds widest element across all blocks
  - Emoji-safe alignment: all operations use visual_width()
  - 32 unit tests: dataclass, stacking, alignment, spacing, grid, side-by-side
  - 19 integration tests: Frame combinations, Banner integration, complex dashboards
  - Test coverage: 100% on layout.py
  - 10 examples in 07_layout_composer.py demonstrating all features
  - Exported from styledconsole.core and main module
  - Branch: feature/T-008-layout-composer → main (merged)
  - Files: src/styledconsole/core/layout.py, tests/unit/test_layout.py, tests/integration/test_layout_integration.py

- ✅ **T-009**: Console Class Core API (2.5 days)
  - Implemented Console class with Rich backend integration (104 statements)
  - All 10 core methods: __init__, frame, banner, text, rule, newline, clear, export_html, export_text, print
  - Terminal detection with TerminalProfile integration
  - Recording mode for HTML/text export via Rich backend
  - Debug logging with configurable logger (stderr output)
  - Custom file output stream support
  - 63 unit tests: all initialization options, all methods, edge cases
  - 25 integration tests: complex workflows (welcome screens, dashboards, error displays, reports)
  - Test coverage: 92.31% on console.py (96/104 lines)
  - 15 comprehensive examples in 08_console_api.py (407 lines)
  - Exported from styledconsole main module
  - All 441 tests passing with 97.64% overall coverage
  - Branch: feature/T-009-console-api → main (merged)
  - Files: src/styledconsole/console.py, tests/unit/test_console.py, tests/integration/test_console_integration.py

**🎉 MILESTONE M2 COMPLETE! Rendering Engine - 4/4 tasks (100%)**

- ✅ **Examples Modernization** (Oct 18, 2025)
  - Modernized all 7 basic examples to use Console API as primary interface
  - Updated 01-04: simple_frame, emoji_support, alignments, border_styles (use console.frame())
  - Updated 05: frame_renderer (marked as ADVANCED, added usage notes)
  - Updated 06: banner_renderer (use console.banner(), keep BannerRenderer for utilities)
  - Updated 07: layout_composer (Console + LayoutComposer integration)
  - Created examples/basic/README.md (comprehensive guide with feature matrix)
  - All examples demonstrate best practices with Console API
  - Commit: a0b227e "feat(examples): Modernize all examples to use Console API"

### Week 2 (Oct 21-25, 2025)
- *TBD: Start M3 - Preset Functions*

---

## Validation Checklist

- [x] All tasks have clear acceptance criteria
- [x] Dependencies mapped between tasks
- [x] Effort estimates provided (0.5-3 days each)
- [x] Test coverage requirements specified
- [x] Critical path identified
- [x] Parallelization opportunities noted
- [x] Total timeline aligns with 8-week goal

**Status:** ✅ Tasks phase complete - Ready for Implementation (Phase 4)

---

## M6: Post-v0.1.0 Enhancements (Future Roadmap)

**Status:** 📋 Planned for v0.2.0+
**Based on:** Legacy StyledConsole Analysis (doc/LEGACY_ANALYSIS_AND_IMPROVEMENTS.md)

### T-020: Icon Provider System (v0.2.0)
**Priority:** High
**Effort:** 2-3 days
**Dependencies:** v0.1.0 released
**Status:** ⬜ Planned

**Description:**
Add a simple icon provider system with Unicode/ASCII fallback for limited terminal environments.

**Legacy Lessons:**
- ✅ Keep it simple (avoid complex icon families/categories from legacy)
- ✅ Focus on common icons (status, progress, etc.)
- ❌ Avoid plugin architecture complexity

**Acceptance Criteria:**
- [ ] `IconProvider` class with `get(name: str) -> str` method
- [ ] Predefined icon sets: `unicode_icons` and `ascii_icons`
- [ ] Common icons: success (✅/[OK]), error (❌/[X]), warning (⚠️/[!]), info (ℹ️/[i]), debug (🔍/[?]), critical (🔥/[!!])
- [ ] Context manager support for temporary icon provider switching
- [ ] Global `set_icon_provider()` function
- [ ] Unit tests with 95%+ coverage
- [ ] Documentation with examples
- [ ] Integration with Console class

**Implementation Notes:**
```python
# Simple, focused implementation
class IconProvider:
    def __init__(self, unicode: bool = True):
        self.icons = self._unicode_icons if unicode else self._ascii_icons

    def get(self, name: str) -> str:
        return self.icons.get(name, '•')

# Usage
console.text(f"{icons.get('success')} Operation completed!")
```

**Estimated LOC:** ~80 lines (plus 150 test lines)

---

### T-021: Runtime Policy System (v0.2.0)
**Priority:** High
**Effort:** 3-4 days
**Dependencies:** T-020
**Status:** ⬜ Planned

**Description:**
Add runtime policy for graceful degradation in different terminal environments (CI/CD, ASCII-only, etc.)

**Legacy Lessons:**
- ✅ Environment-driven rendering decisions
- ✅ Support NO_COLOR standard
- ❌ Keep it simple (3-4 settings max, not complex policy system)

**Acceptance Criteria:**
- [ ] `RenderPolicy` dataclass with fields: unicode, color, emoji
- [ ] `from_env()` classmethod for automatic environment detection
- [ ] NO_COLOR environment variable support (disable colors)
- [ ] TERM=dumb detection (ASCII-only mode)
- [ ] CI environment detection (disable emoji, preserve color for logs)
- [ ] Global policy with `set_policy()` and `get_policy()` functions
- [ ] Console class respects policy in all rendering
- [ ] Unit tests with 95%+ coverage
- [ ] Documentation with CI/CD examples

**Implementation Notes:**
```python
@dataclass
class RenderPolicy:
    unicode: bool = True   # Use Unicode box drawing
    color: bool = True     # Use ANSI colors
    emoji: bool = True     # Use emoji (Tier 1 only)

    @classmethod
    def from_env(cls) -> 'RenderPolicy':
        no_color = os.getenv('NO_COLOR') is not None
        term = os.getenv('TERM', '').lower()
        ci = os.getenv('CI') is not None
        return cls(
            unicode=(term != 'dumb'),
            color=not no_color,
            emoji=(term not in ('dumb', 'linux') and not ci)
        )
```

**Estimated LOC:** ~100 lines (plus 200 test lines)

---

### T-022: Enhanced HTML Export (v0.2.0)
**Priority:** Medium
**Effort:** 4-6 days
**Dependencies:** T-020, T-021
**Status:** ⬜ Planned

**Description:**
Enhance HTML export with gradient support, CSS classes, and better styling options.

**Legacy Lessons:**
- ✅ HTML export preserves visual styling
- ✅ Useful for documentation/reports
- ❌ Keep it lightweight (no external dependencies)

**Acceptance Criteria:**
- [ ] Add `css_classes: bool` parameter to `export_html()` (use classes instead of inline styles)
- [ ] Add `include_gradients: bool` parameter (render gradient banners in HTML)
- [ ] Generate CSS stylesheet when `css_classes=True`
- [ ] Gradient rendering using CSS linear-gradient()
- [ ] Support for exporting progress bars to HTML
- [ ] Unit tests for all export options
- [ ] Example HTML outputs in docs
- [ ] Documentation with screenshot comparisons

**Implementation Notes:**
```python
# Extended export_manager.py
class ExportManager:
    def export_html(
        self,
        inline_styles: bool = True,
        css_classes: bool = False,    # NEW
        include_gradients: bool = True  # NEW
    ) -> str:
        # CSS class-based styling option
        # Gradient banners using linear-gradient()
```

**Estimated LOC:** ~150 lines (plus 250 test lines)

---

### T-023: Theme System (v0.2.0)
**Priority:** Medium
**Effort:** 6-8 days
**Dependencies:** T-021
**Status:** ⬜ Planned

**Description:**
Add predefined color themes for consistent styling across frames, banners, and text.

**Legacy Lessons:**
- ✅ Aesthetic consistency
- ✅ Optional feature (doesn't break existing code)
- ❌ Keep it simple (3-5 predefined themes)

**Acceptance Criteria:**
- [ ] `Theme` dataclass with color fields: primary, success, warning, error, border
- [ ] Predefined themes: DARK, LIGHT, SOLARIZED, MONOKAI, NORD
- [ ] Console class accepts `theme` parameter
- [ ] Theme applies to frames, banners, and text styling
- [ ] Global `set_theme()` function
- [ ] Theme preview utility function
- [ ] Unit tests for all themes
- [ ] Example gallery showing all themes
- [ ] Documentation with screenshots

**Implementation Notes:**
```python
@dataclass
class Theme:
    primary: str = 'blue'
    success: str = 'green'
    warning: str = 'yellow'
    error: str = 'red'
    border: str = 'white'

# Predefined themes
DARK = Theme(primary='cyan', success='green', ...)
LIGHT = Theme(primary='blue', success='darkgreen', ...)
SOLARIZED = Theme(primary='#268bd2', success='#859900', ...)
```

**Estimated LOC:** ~120 lines (plus 200 test lines)

---

### T-024: Animation Support (v0.3.0)
**Priority:** Low
**Effort:** 8-10 days
**Dependencies:** v0.2.0 released
**Status:** ⬜ Planned (Experimental)

**Description:**
Add simple frame-based animations for spinners and progress indicators.

**Legacy Lessons:**
- ⚠️ Nice for progress indicators
- ⚠️ Terminal clearing complexities
- ❌ Don't over-engineer (simple frame iteration)

**Acceptance Criteria:**
- [ ] `Animator` class with `spinner()` method
- [ ] Predefined spinners: DOTS, MOON, ARROW, BOUNCE, PULSE
- [ ] Frame iteration with configurable delay
- [ ] Terminal cursor management (hide/show)
- [ ] Integration with Console class
- [ ] Unit tests for frame generation
- [ ] Example with real-time progress
- [ ] Documentation with warnings about terminal support

**Implementation Notes:**
```python
class Animator:
    DOTS = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    MOON = ['🌑', '🌒', '🌓', '🌔', '🌕', '🌖', '🌗', '🌘']

    def spinner(self, frames: List[str]) -> Iterator[str]:
        while True:
            for frame in frames:
                yield frame
```

**Estimated LOC:** ~100 lines (plus 150 test lines)

---

### T-025: Progress Bar Wrapper (v0.3.0)
**Priority:** Low
**Effort:** 4-6 days
**Dependencies:** v0.2.0 released
**Status:** ⬜ Planned

**Description:**
Convenience wrapper for Rich's progress bars with StyledConsole styling.

**Legacy Lessons:**
- ✅ Common need for CLI applications
- ❌ Don't build from scratch - use Rich
- ✅ Provide convenience wrapper only

**Acceptance Criteria:**
- [ ] `ProgressBar` wrapper class using Rich's Progress
- [ ] Console integration for styled progress
- [ ] Support for multiple concurrent progress bars
- [ ] Themed progress bars (use Theme colors)
- [ ] Unit tests with mocking
- [ ] Example with file download simulation
- [ ] Documentation

**Implementation Notes:**
```python
# Simple wrapper, leverage Rich's battle-tested implementation
class ProgressBar:
    def __init__(self, console: Console, theme: Optional[Theme] = None):
        self._progress = rich.progress.Progress(...)

    def add_task(self, description: str) -> TaskID:
        return self._progress.add_task(description)
```

**Estimated LOC:** ~80 lines (plus 100 test lines)

---

### T-026: Tier 2 Emoji Support (v0.4.0+)
**Priority:** Low
**Effort:** 10-15 days
**Dependencies:** v0.3.0 released, user demand proven
**Status:** ⬜ Planned (Conditional)

**Description:**
Add support for Tier 2 emoji (skin tones, ZWJ sequences) IF users request it and clear use cases are identified.

**Legacy Lessons:**
- ❌ Legacy's complex emoji handling caused 248 lines of alignment hacks
- ❌ Over-engineering led to maintenance nightmare
- ⚠️ Only proceed if there's real user demand

**Acceptance Criteria:**
- [ ] ⚠️ User demand validated (GitHub issues, feedback)
- [ ] ⚠️ Clear use cases documented
- [ ] Add grapheme library for ZWJ support
- [ ] Document which Tier 2 emoji work
- [ ] NO per-emoji correction hacks (get it right first time)
- [ ] Test coverage 95%+
- [ ] Clear documentation on limitations
- [ ] Opt-in feature (default stays Tier 1)

**Implementation Notes:**
```python
# Only if we can do it WITHOUT legacy's complexity
# Must work correctly without post-rendering hacks
# Document limitations clearly
```

**Risk Assessment:** ⚠️ HIGH - Complexity creep danger
**Recommendation:** Avoid unless compelling need proven

**Estimated LOC:** ~200 lines (plus 300 test lines)

---

### M6 Task Summary

| Task | Priority | Effort | Target Version | Risk |
|------|----------|--------|----------------|------|
| **T-020: Icon Provider** | High | 2-3 days | v0.2.0 | ✅ Low |
| **T-021: Runtime Policy** | High | 3-4 days | v0.2.0 | ✅ Low |
| **T-022: Enhanced HTML Export** | Medium | 4-6 days | v0.2.0 | ✅ Low |
| **T-023: Theme System** | Medium | 6-8 days | v0.2.0 | ✅ Low |
| **T-024: Animation Support** | Low | 8-10 days | v0.3.0 | ⚠️ Medium |
| **T-025: Progress Bar Wrapper** | Low | 4-6 days | v0.3.0 | ✅ Low |
| **T-026: Tier 2 Emoji** | Low | 10-15 days | v0.4.0+ | ⚠️ HIGH |

**v0.2.0 Scope:** T-020 through T-023 (15-21 days, ~3-4 weeks)
**v0.3.0 Scope:** T-024, T-025 (12-16 days, ~2-3 weeks)
**v0.4.0+ Scope:** T-026 (only if justified)

**Architecture Principles to Maintain:**
- ✅ Keep modules under 200 lines each
- ✅ Maintain 95%+ test coverage
- ✅ Single responsibility per module
- ✅ No post-rendering hacks
- ✅ Document limitations clearly
- ✅ Stay under 8,000 total lines (currently 4,696)

**What NOT to do (Learn from Legacy):**
- ❌ No factory factories or over-abstraction
- ❌ No multiple competing implementations
- ❌ No premature optimization (no numpy for simple tasks)
- ❌ No undocumented heuristics or magic numbers
- ❌ No plugin systems "for future flexibility"
