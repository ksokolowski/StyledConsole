# StyledConsole

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.5.0-brightgreen.svg)](https://github.com/yourusername/styledconsole/releases/tag/v0.5.0)
[![Tests](https://img.shields.io/badge/tests-700%2B%20passing-success.svg)](https://github.com/yourusername/styledconsole)
[![Coverage](https://img.shields.io/badge/coverage-95%25%2B-brightgreen.svg)](https://github.com/yourusername/styledconsole)

A modern Python library for elegant terminal output with rich formatting, colors, emoji support, and export capabilities.

**✨ v0.5.0 Released!** Documentation consolidated, examples reorganized, with 700+ tests passing and 95%+ coverage.

## ✨ Features

- 🎨 **Rich Formatting**: Frames with 8 border styles, ASCII art banners (500+ fonts), and styled text
- 🌈 **Advanced Colors**: 148 CSS4 color names, hex codes, RGB tuples, gradients, and rainbow effects
- 🌟 **Gradient Effects**: Vertical, diagonal, and 7-color ROYGBIV rainbow gradients
- 😀 **Emoji Support**: Tier 1 emoji support (✅🔥🎉🚀⚡💡🎨💎) with proper width calculation
- 📦 **8 Border Styles**: solid, rounded, double, heavy, thick, ascii, minimal, dots
- 📊 **Layout System**: Rich-native Group, Columns, Table for powerful compositions
- 💾 **Export**: HTML and plain-text export with ANSI-to-HTML conversion
- 🔍 **Terminal Detection**: Auto-detect color depth, ANSI support, and emoji safety
- 🏗️ **Clean Architecture**: Rich-native rendering (v0.3.0) with 95.96% test coverage
- ✅ **ANSI-Safe**: No wrapping bugs, proper alignment with emoji (v0.3.0)

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

# Frame with gradient border (v0.3.0)
console.frame(
    "Gradient Border",
    border="rounded",
    border_gradient_start="blue",
    border_gradient_end="purple"
)
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

### Layout System (v0.3.0 Rich-Native)

```python
from rich.console import Group
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from styledconsole import Console
from styledconsole.core.box_mapping import get_box_style

console = Console()

# Stack vertically with Group
panel1 = Panel("First block", box=get_box_style("solid"))
panel2 = Panel("Second block", box=get_box_style("solid"))
panel3 = Panel("Third block", box=get_box_style("solid"))

from rich.text import Text
group = Group(panel1, Text(""), panel2, Text(""), panel3)
console._rich_console.print(group)

# Side by side with Columns
left = Panel("Left column", box=get_box_style("rounded"))
right = Panel("Right column", box=get_box_style("rounded"))

columns = Columns([left, right], padding=(0, 2))
console._rich_console.print(columns)

# Grid layout with Table.grid
grid = Table.grid(padding=(0, 2))
grid.add_row(
    Panel("Cell 1", box=get_box_style("solid")),
    Panel("Cell 2", box=get_box_style("solid")),
    Panel("Cell 3", box=get_box_style("solid"))
)
grid.add_row(
    Panel("Cell 4", box=get_box_style("solid")),
    Panel("Cell 5", box=get_box_style("solid")),
    Panel("Cell 6", box=get_box_style("solid"))
)
console._rich_console.print(grid)
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

**v0.5.0 Released!** 🎉

This project is **production-ready** with comprehensive testing and documentation.

**v0.5.0 Documentation & Structure:**

- ✅ 4 master docs: USER_GUIDE, DEVELOPER_GUIDE, PROJECT_STATUS, DOCUMENTATION_POLICY
- ✅ 27 examples in 4 categories: gallery, usecases, demos, validation
- ✅ Unified example runner with `--all` and `--auto` flags
- ✅ Gallery examples standardized with EMOJI constants
- ✅ Project root cleaned (24 files removed)

**Previous Releases:**

- v0.4.0: Animated gradients, unified gradient engine, preset functions
- v0.3.0: Rich-native rendering, ANSI-safe frames, 100% backward compatible
- v0.1.0: Foundation - frames, banners, layouts, CSS4 colors, HTML export

**Quality Metrics:**

- 700+ tests passing (100%)
- 95%+ test coverage
- Zero known bugs
- 27 examples working
- Full type hints with Literal types

## 📚 Documentation

**User Documentation:**

- `README.md` - This file with quick start and examples
- `CHANGELOG.md` - Version history and release notes
- `docs/USER_GUIDE.md` - Complete user guide with API reference
- `examples/` - 27 working examples demonstrating all features

**Developer Documentation:**

- `docs/DEVELOPER_GUIDE.md` - Architecture, module structure, contributing
- `docs/PROJECT_STATUS.md` - Roadmap, active tasks, changelog
- `docs/DOCUMENTATION_POLICY.md` - Documentation standards

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

**Current Version**: 0.5.0 (Production Ready - 100% backward compatible with v0.1.0)

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
