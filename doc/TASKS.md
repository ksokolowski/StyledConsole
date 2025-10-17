# TASKS (Phase 3: Implementation Breakdown)

**Project:** StyledConsole
**Version:** 0.1.0
**Date Started:** October 17, 2025
**Status:** 🚧 In Progress - M1: Core Setup & Utilities

---

## Progress Overview

**Overall Progress:** 5/21 tasks completed (24%)

| Milestone | Tasks | Completed | Progress |
|-----------|-------|-----------|----------|
| - **M1: Core Setup & Utilities** ✅✅✅✅✅ 100% (Oct 17-24, 2025) - Week 1 **COMPLETE** |
| **M2** Rendering Engine | 5 | 0 | ⬜⬜⬜⬜⬜ 0% |
| **M3** Preset Functions | 3 | 0 | ⬜⬜⬜ 0% |
| **M4** Export & Fallbacks | 3 | 0 | ⬜⬜⬜ 0% |
| **M5** Testing & Release | 5 | 0 | ⬜⬜⬜⬜⬜ 0% |

**Total Effort:** 34 days (~7 weeks)
**Days Completed:** 7.5 / 34
**Days Remaining:** 26.5
**Current Task:** T-006 Frame Renderer Core---

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
- 5 rendering methods: render_horizontal, render_vertical, render_top_border, render_bottom_border, render_divider
- Centered title support in top borders
- Case-insensitive style lookup via get_border_style()
- All 58 unit tests passing
- Test coverage: 100% (58/58 lines covered)
- Styles exported from styledconsole.core and styledconsole main module
- Branch: feature/T-005-border-styles
- Files: src/styledconsole/core/styles.py, tests/unit/test_styles.py

**Implementation Files:**
- `styledconsole/core/styles.py`
- `tests/unit/test_styles.py`

---

## M2: Rendering Engine (Week 3-4)

### T-006: Frame Renderer Core
**Priority:** High
**Effort:** 3 days
**Dependencies:** T-002, T-003, T-005
**Assigned to:** TBD

**Description:**
Implement core frame rendering with borders, padding, and titles.

**Acceptance Criteria:**
- [ ] `Frame` dataclass defined
- [ ] `FrameRenderer` class implemented
- [ ] Renders frames with all border styles
- [ ] Handles title placement (centered by default)
- [ ] Applies padding correctly
- [ ] Calculates frame width automatically or uses specified width
- [ ] Emoji-safe alignment maintained
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

### T-007: Banner Renderer
**Priority:** High
**Effort:** 2 days
**Dependencies:** T-003, T-006
**Assigned to:** TBD

**Description:**
Implement FIGlet banner rendering with gradient support.

**Acceptance Criteria:**
- [ ] `Banner` dataclass defined
- [ ] `BannerRenderer` class implemented
- [ ] Integrates with pyfiglet
- [ ] Supports multiple fonts (slant, standard, banner)
- [ ] Applies gradient coloring per line
- [ ] Handles emoji in banner text (fallback to ASCII)
- [ ] Unit tests with different fonts
- [ ] Visual snapshot tests
- [ ] Test coverage ≥85%

**Test Cases:**
```python
def test_banner_rendering():
    banner = BannerRenderer().render("TEST", font="slant")
    assert len(banner.splitlines()) > 1  # Multi-line output
    assert "TEST" in banner  # Original text visible in output

def test_banner_with_gradient():
    banner = BannerRenderer().render(
        "GO",
        font="slant",
        gradient=("#00ff00", "#0000ff")
    )
    # Verify gradient applied
```

**Implementation Files:**
- `styledconsole/core/banner.py`
- `tests/unit/test_banner.py`
- `tests/visual/test_banner_snapshots.py`

---

### T-008: Layout Composer
**Priority:** Medium
**Effort:** 2 days
**Dependencies:** T-006
**Assigned to:** TBD

**Description:**
Implement layout composition for nested frames and multi-section displays.

**Acceptance Criteria:**
- [ ] `Layout` class supports vertical stacking
- [ ] `Layout` class supports horizontal alignment
- [ ] Frames can be nested without alignment issues
- [ ] Maintains consistent spacing between elements
- [ ] Unit tests for nested layouts
- [ ] Integration tests with console
- [ ] Test coverage ≥85%

**Implementation Files:**
- `styledconsole/core/layout.py`
- `tests/unit/test_layout.py`

---

### T-009: Console Class Core API
**Priority:** High
**Effort:** 2.5 days
**Dependencies:** T-004, T-006, T-007
**Assigned to:** TBD

**Description:**
Implement the main Console facade class with Rich backend integration and complete public API surface.

**Acceptance Criteria:**
- [ ] `Console` class initialized with Rich console
- [ ] `frame()` method with all parameters (title, border, colors, padding, width)
- [ ] `banner()` method delegates to BannerRenderer
- [ ] `text()` method for styled text output
- [ ] `rule()` method for horizontal rules
- [ ] `newline()` method for spacing
- [ ] `export_html()` method with inline_styles option
- [ ] `export_text()` method (ANSI stripped)
- [ ] `terminal_profile` property
- [ ] `clear()` method
- [ ] Terminal detection on initialization
- [ ] Recording mode for HTML export
- [ ] **Debug logging support** (when debug=True)
- [ ] **`file` parameter** for custom output streams
- [ ] Unit tests for all methods
- [ ] Integration tests end-to-end
- [ ] Test coverage ≥90%

**Test Cases:**
```python
def test_console_frame():
    console = Console(record=True)
    console.frame("Test content", title="Title")
    output = console.export_text()  # Get raw output
    assert "Title" in output
    assert "Test content" in output

def test_console_detection():
    console = Console(detect_terminal=True)
    assert console.terminal_profile is not None
    assert isinstance(console.terminal_profile.color_depth, int)

def test_debug_logging():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    console = Console(debug=True)
    console.frame("Test")  # Should log internally
    # Check logs contain "Rendering frame"

def test_complete_api():
    console = Console(record=True)
    console.text("Hello", color="blue", bold=True)
    console.rule("Section", color="gray")
    console.newline(2)
    console.frame("Content", border="solid")
    console.banner("TEST", font="slant")

    html = console.export_html(inline_styles=True)
    text = console.export_text()
    assert html and text
```

**Implementation Files:**
- `styledconsole/console.py`
- `styledconsole/__init__.py` (public exports)
- `tests/unit/test_console.py`
- `tests/integration/test_console_integration.py`

---

## M3: Preset Functions & Layouts (Week 5-6)

### T-010: Status Frame Preset
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

### Week 1 (Oct 17-23, 2025)

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
  - 5 rendering methods: render_horizontal, render_vertical, render_top_border, render_bottom_border, render_divider
  - Centered title support in top borders with overflow handling
  - Case-insensitive style lookup via get_border_style()
  - All 58 unit tests passing with 100% coverage
  - Styles exported from styledconsole.core and styledconsole main module
  - Branch: feature/T-005-border-styles
  - Files: src/styledconsole/core/styles.py, tests/unit/test_styles.py

**🎉 MILESTONE M1 COMPLETE! Core Setup & Utilities - 5/5 tasks (100%)**

### Week 2 (Oct 24-30, 2025)
- *TBD*

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
