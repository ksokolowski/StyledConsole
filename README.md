# StyledConsole

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

A modern Python library for elegant terminal output with rich formatting, colors, emoji support, and export capabilities.

## ✨ Features

- 🎨 **Rich Formatting**: Bold, italic, underline, strikethrough with automatic fallbacks
- 🌈 **Flexible Colors**: RGB, hex, CSS4 names (148 colors), with terminal compatibility
- 😀 **Emoji Support**: 200+ common emojis with safe width calculation
- 📦 **Box & Border Styles**: 8+ border styles (ASCII, single, double, rounded, etc.)
- 📊 **Smart Layouts**: Automatic padding, alignment, and wrapping
- 💾 **Export**: HTML and plain-text output for documentation
- 🔍 **Terminal Detection**: Automatic capability detection with graceful degradation

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

# Basic text with formatting
console.print("Hello, World!", color="blue", bold=True)

# Emojis and colors
console.print("✅ Success!", color="green")
console.print("❌ Error!", color="red")

# Boxes and borders
console.box("Important Message", border="double", padding=1)
```

## 🛠️ Development Status

This project is in **active development** (MVP Phase - v0.1.0).

Current implementation status:
- 🚧 Core Setup & Utilities (M1)
- ⬜ Rendering Engine (M2)
- ⬜ Preset Functions (M3)
- ⬜ Export & Fallbacks (M4)
- ⬜ Testing & Release (M5)

## 📚 Documentation

See `doc/` directory for complete specification and design documentation:
- `SPECIFICATION.md` - User requirements and journeys
- `PLAN.md` - Technical architecture and API design
- `TASKS.md` - Implementation breakdown and progress

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

**Current Version**: 0.1.0 (Alpha - API may change before 1.0.0 release)

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
