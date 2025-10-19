# StyledConsole

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.1.0-brightgreen.svg)](https://github.com/yourusername/styledconsole/releases/tag/v0.1.0)
[![Tests](https://img.shields.io/badge/tests-612%20passing-success.svg)](https://github.com/yourusername/styledconsole)
[![Coverage](https://img.shields.io/badge/coverage-96.30%25-brightgreen.svg)](https://github.com/yourusername/styledconsole)

A modern Python library for elegant terminal output with rich formatting, colors, emoji support, and export capabilities.

**✨ v0.1.0 Released!** Production-ready with 612 tests passing and 96.30% coverage.

## ✨ Features

- 🎨 **Rich Formatting**: Frames with 8 border styles, ASCII art banners (500+ fonts), and styled text
- 🌈 **Advanced Colors**: 148 CSS4 color names, hex codes, RGB tuples, gradients, and rainbow effects
- 🌟 **Gradient Effects**: Vertical, diagonal, and 7-color ROYGBIV rainbow gradients
- 😀 **Emoji Support**: Tier 1 emoji support (✅🔥🎉🚀⚡💡🎨💎) with proper width calculation
- 📦 **8 Border Styles**: solid, rounded, double, heavy, thick, ascii, minimal, dots
- 📊 **Layout System**: Stack, side-by-side, and grid layouts for complex compositions
- 💾 **Export**: HTML and plain-text export with ANSI-to-HTML conversion
- 🔍 **Terminal Detection**: Auto-detect color depth, ANSI support, and emoji safety
- 🏗️ **Clean Architecture**: Facade pattern with specialized managers (96.30% test coverage)

## 🚀 Installation

```bash
pip install styledconsole
```

Or with UV:

```bash
uv add styledconsole
```

## 📖 Quick Start

```python
from styledconsole import Console

console = Console()

# Beautiful frames with borders
console.frame("Hello, World!", title="Greeting", border="rounded")

# ASCII art banners
console.banner("SUCCESS", font="slant")

# Styled text with colors
console.text("Important message", bold=True, color="red")

# Horizontal rules
console.rule("Section Title", color="cyan")

# Multiple lines in a frame
console.frame([
    "Line 1",
    "Line 2",
    "Line 3"
], title="Multi-line", border="double")
```

### Gradient Effects

```python
from styledconsole.effects import gradient_frame, diagonal_gradient_frame, rainbow_frame

# Vertical gradient (top to bottom)
gradient_frame(
    ["Line 1", "Line 2", "Line 3"],
    start_color="red",
    end_color="blue",
    target="content"  # or "border" or "both"
)

# Diagonal gradient (top-left to bottom-right)
diagonal_gradient_frame(
    ["Beautiful", "Diagonal", "Flow"],
    start_color="lime",
    end_color="magenta",
    target="both"
)

# Rainbow effect (7-color ROYGBIV spectrum)
rainbow_frame(
    ["Red", "Orange", "Yellow", "Green", "Blue"],
    direction="vertical"  # or "diagonal"
)
```

### Layout System

```python
from styledconsole.core.layout import LayoutComposer

composer = LayoutComposer()

# Stack vertically
output = composer.stack([
    "First block",
    "Second block",
    "Third block"
], spacing=1)

# Side by side
output = composer.side_by_side([
    "Left column",
    "Right column"
], spacing=3)

# Grid layout
output = composer.grid([
    ["Cell 1", "Cell 2", "Cell 3"],
    ["Cell 4", "Cell 5", "Cell 6"]
])
```

### Export

```python
# Record output and export to HTML
console = Console(record=True)
console.frame("Example output")
console.banner("EXPORTED", font="slant")

html = console.export_html()  # Get HTML with colors
text = console.export_text()  # Get plain text
```

## 🛠️ Development Status

**v0.1.0 Released!** 🎉

This project is **production-ready** with comprehensive testing and documentation.

Implementation status:
- ✅ Core Setup & Utilities (M1) - Complete
- ✅ Rendering Engine (M2) - Complete
- ✅ Console API & Effects (M3) - Complete
- ✅ Export & Terminal Detection (M4) - Complete
- ✅ Testing & Documentation (M5) - Complete

**Quality Metrics:**
- 612 tests passing (100%)
- 96.30% test coverage
- Zero known bugs
- All examples working
- Full type hints with Literal types

## 📚 Documentation

**User Documentation:**
- `README.md` - This file with quick start and examples
- `CHANGELOG.md` - Version history and release notes
- `examples/` - 20+ working examples demonstrating all features
- `RELEASE_ANNOUNCEMENT.md` - v0.1.0 release details

**Developer Documentation:**
- `doc/REFACTORING_SUMMARY.md` - Architecture overview and achievements
- `doc/REFACTORING_PLAN_v2.md` - Comprehensive refactoring documentation
- `doc/PHASE4_RESEARCH_PLAN.md` - Research methodology and validation
- `doc/EMOJI_GUIDELINES.md` - Emoji support and safe usage guide

**API Reference:**
All public APIs include comprehensive docstrings with type hints.

## 🔒 API Stability

StyledConsole follows [Semantic Versioning 2.0.0](https://semver.org/):

- **Public API**: All items in `__all__` are considered public and stable
  - Breaking changes will increment the major version (e.g., 1.x.x → 2.0.0)
  - New features will increment the minor version (e.g., 1.1.x → 1.2.0)
  - Bug fixes will increment the patch version (e.g., 1.1.1 → 1.1.2)

- **Internal APIs**: Items prefixed with `_` are internal and may change without notice
  - Not part of the public API contract
  - Should not be used in production code

- **Type Safety**: All public APIs include type hints
  - Use `Literal` types for parameters with specific valid values (e.g., `align: Literal["left", "center", "right"]`)
  - IDE autocomplete and type checkers will help catch errors early

- **Deprecation Policy**: When removing features
  - Deprecated features will show warnings for at least one minor version
  - Alternatives will be documented in deprecation messages
  - Deprecated features removed only in major version bumps

**Current Version**: 0.1.0 (Production Ready - Public API stable, internal implementation may be refined)

## 🤝 Contributing

This is a personal project, but feedback and suggestions are welcome!

## 📄 License

Apache License 2.0 - See LICENSE file for details.

## 🙏 Acknowledgments

Built with:
- [Rich](https://github.com/Textualize/rich) - Terminal formatting
- [PyFiglet](https://github.com/pwaller/pyfiglet) - ASCII art text
- [wcwidth](https://github.com/jquast/wcwidth) - Unicode width calculation
- [ansi2html](https://github.com/pycontribs/ansi2html) - HTML export
