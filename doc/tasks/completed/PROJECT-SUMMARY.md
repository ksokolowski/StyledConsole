# StyledConsole - Project Summary

**Library Name:** StyledConsole
**Package Name:** `styledconsole`
**Version:** 0.1.0 (in development)
**Date:** October 17, 2025
**Status:** ✅ Ready for Implementation

---

## Quick Facts

**What:** Emoji-safe ANSI console rendering library for Python
**Install:** `pip install styledconsole` _(when published)_
**License:** Apache License 2.0
**Python:** ≥3.10
**Package Manager:** UV (Astral)

---

## One-Line Pitch

> **StyledConsole** makes it effortless to create beautiful, emoji-safe console output with frames, banners, and dashboards that work perfectly in terminals and CI/CD logs.

---

## Key Features

✅ **Emoji-Safe Rendering** - Proper Unicode width calculation
✅ **CSS4 Color Names** - 148 human-readable colors (coral, dodgerblue, etc.)
✅ **Multiple Border Styles** - solid, double, rounded, heavy, ascii
✅ **HTML Export** - Same visual output for web reports
✅ **Preset Functions** - Ready-to-use layouts for common scenarios
✅ **FIGlet Banners** - Large ASCII art headers
✅ **Gradient Support** - Rainbow and custom color gradients

---

## Installation & Setup

```bash
# Install UV (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project
uv init --lib styledconsole
cd styledconsole

# Add dependencies
uv add "rich>=13.7" "pyfiglet>=1.0.2" "wcwidth>=0.2.13" "ansi2html>=1.8.0"

# Add dev tools
uv add --dev "pytest>=8.0" "ruff>=0.3" "pre-commit>=3.6"

# Sync
uv sync
```

---

## Example Usage

```python
from styledconsole import Console

console = Console()

# Simple frame
console.frame(
    "✅ Build completed successfully!",
    title="CI/CD Status",
    border="rounded",
    border_color="green",
    padding=1
)

# Banner with gradient
console.banner("SUCCESS", font="slant", gradient="rainbow")

# Preset functions
from styledconsole.presets import status_frame, dashboard_small

status_frame("Login Test ✅", status="PASS")
dashboard_small(
    banner="Test Results",
    stats={"passed": 182, "failed": 3, "skipped": 7}
)
```

---

## Documentation Structure

### Phase 1: Specify ✅
- `SPECIFICATION.md` - User journeys, success criteria, design principles
- `USER-STORIES-CATALOG.md` - 26 comprehensive user stories
- `USER-STORIES-QUICK-REF.md` - Quick reference with code examples
- `EMOJI-STRATEGY.md` - Tiered emoji support strategy
- `CSS4-COLORS.md` - Complete color reference

### Phase 2: Plan ✅
- `PLAN.md` - Complete architecture, API design, implementation details

### Phase 3: Tasks ✅
- `TASKS.md` - 21 implementation tasks across 5 milestones
- Total effort: 34 days (≈7 weeks)

### Phase 4: Implement 🔜
- Ready to begin with T-001: Project Setup & Structure

### Supporting Documents ✅
- `SDD-UPDATES-SUMMARY.md` - Critical updates log
- `FINAL-CORRECTIONS.md` - ANSI output behavior clarifications
- `UV-MIGRATION.md` - Poetry → UV migration guide
- `UV-SUMMARY.md` - UV quick reference
- `LIBRARY-RENAME.md` - PyTermFrame → StyledConsole rename
- `RENAME-COMPLETE.md` - Rename verification

---

## Architecture Overview

```
User Application
       ↓
Console (Facade)
       ↓
┌──────┴──────┬──────────┬─────────┐
│             │          │         │
Preset     Frame      Banner    Export
Functions  Renderer   Renderer  (HTML)
│             │          │         │
└──────┬──────┴──────────┴─────────┘
       ↓
Rich (ANSI Backend)
       ↓
Terminal / CI Log / HTML
```

---

## Core API

### Console Class

```python
console = Console(debug=False)

# Render frame
console.frame(
    content: str,
    title: str | None = None,
    border: str = "solid",
    border_color: str = "white",
    padding: int = 0,
    align: str = "left",
    width: int | None = None,
) -> None

# Render banner
console.banner(
    text: str,
    font: str = "standard",
    color: str | None = None,
    gradient: str | None = None,
) -> None

# Other methods
console.text(text, style)
console.rule(title, style)
console.newline(count)
console.clear()
console.export_html() -> str
console.export_text() -> str
console.terminal_profile -> TerminalProfile
```

### Preset Functions

```python
from styledconsole.presets import (
    status_frame,      # Test results
    test_summary,      # Pass/fail statistics
    dashboard_small,   # 3-panel compact
    dashboard_medium,  # Standard reporting
    dashboard_large,   # Full-featured
    banner_alert,      # Large headers
)
```

### Exceptions

```python
from styledconsole import (
    StyledConsoleError,  # Base exception
    RenderError,         # Frame/banner rendering failures
    ExportError,         # HTML/text export failures
    TerminalError,       # Terminal capability issues
)
```

---

## Development Roadmap

### v0.1.0 - MVP (Current) 🎯
- Core rendering (frames, banners, text)
- 5 border styles
- CSS4 color names (148 colors)
- Tier 1 emoji support (basic icons)
- HTML export
- 5 preset functions
- **Effort:** 34 days

### v0.2.0 - Enhanced 🔮
- Tier 2 emoji support (modifiers)
- Nested frames
- Configuration file support
- Additional preset functions

### v0.3.0 - Advanced 🔮
- YAML template system
- Tier 3 emoji support (ZWJ sequences)
- Advanced layout composition

### v0.5.0+ - Future 🔮
- Textual backend for interactive dashboards
- Robot Framework integration package
- Theme engine with color schemes

---

## Technology Stack

**Core Dependencies:**
- Rich ≥13.7 - ANSI rendering engine
- pyfiglet ≥1.0.2 - ASCII art banners
- wcwidth ≥0.2.13 - Unicode width calculation
- ansi2html ≥1.8.0 - HTML export

**Dev Dependencies:**
- pytest ≥8.0 - Testing framework
- pytest-cov ≥4.1 - Coverage reporting
- pytest-snapshot ≥0.9 - Snapshot testing
- ruff ≥0.3 - Linting, formatting, type checking
- pre-commit ≥3.6 - Git hooks

**Package Manager:** UV (Astral) - 10-100x faster than Poetry/pip

---

## Design Principles

1. **SOLID Architecture** - Clean separation of concerns
2. **Stateless Operations** - No thread safety concerns
3. **Terminal-Focused** - Let terminal handle accessibility
4. **Standard Practices** - PEP 8, SemVer, PyPI conventions
5. **Modern Python** - Leverages Python ≥3.10 features

---

## Key Decisions

✅ **UV over Poetry** - Faster, standard PEP 621 format, Python version management
✅ **Apache 2.0 License** - Permissive, business-friendly
✅ **Ruff only** - Single tool for linting/formatting/type checking
✅ **Tier 1 Emojis (MVP)** - 200 basic icons, reliable alignment
✅ **CSS4 Colors** - Human-readable names (coral vs #FF7F50)
✅ **StyledConsole name** - More descriptive than PyTermFrame

---

## Testing Strategy

- **Unit Tests:** ≥90% coverage target
- **Emoji Alignment Tests:** All Tier 1 icons (200+)
- **CSS4 Color Tests:** All 148 named colors
- **Border Style Tests:** All 5 styles × colors
- **Platform Tests:** Linux, macOS, Windows
- **Python Version Tests:** 3.10, 3.11, 3.12
- **CI/CD:** GitHub Actions integration

---

## Success Metrics

**Adoption:**
- 1,000+ PyPI downloads in first 3 months
- 100+ GitHub stars in first 6 months

**Quality:**
- ≥90% test coverage
- <5 emoji alignment bugs in v0.1
- 100% documentation coverage

**Performance:**
- <10ms single frame render
- <50ms dashboard with 5 frames
- <200ms HTML export (100 frames)

---

## Use Cases

**Primary:**
- CLI tool developers - Visual output
- Test engineers - Test result formatting
- DevOps teams - Status dashboards

**Secondary:**
- Data scientists - Notebook output
- Robot Framework users - Enhanced logging

**Example Scenarios (26 user stories):**
1. Test result frames
2. Configuration displays
3. Progress indicators
4. Error messages
5. Welcome screens
6. System monitoring
7. Build summaries
8. And 19 more...

---

## Contributing

```bash
# Clone repository
git clone https://github.com/user/styledconsole.git
cd styledconsole

# Setup development environment
uv sync

# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format .

# Run pre-commit checks
uv run pre-commit run --all-files
```

---

## Next Steps

1. **Check PyPI availability** - Verify `styledconsole` package name is free
2. **Create repository** - GitHub repo with proper README
3. **Start T-001** - Project setup with UV
4. **Implement M1** - Utilities (T-002 through T-005)
5. **Implement M2** - Core rendering (T-006 through T-008)
6. **Continue through M5** - Complete MVP

---

## Resources

- **Documentation:** `/doc/` directory (12 markdown files)
- **UV Guide:** `UV-MIGRATION.md`, `UV-SUMMARY.md`
- **User Stories:** `USER-STORIES-CATALOG.md` (26 stories)
- **Colors:** `CSS4-COLORS.md` (148 colors)
- **Emojis:** `EMOJI-STRATEGY.md` (3-tier approach)

---

**Status:** 📚 Complete SDD - Ready to code!
**Next:** T-001 Project Setup & Structure
**Timeline:** 34 days to v0.1.0 MVP

---

*Last Updated: October 17, 2025*
*Library Name: StyledConsole (formerly PyTermFrame)*
