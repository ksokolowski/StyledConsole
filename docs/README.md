# StyledConsole Documentation

**Version:** 0.9.9
**Last Updated:** January 2, 2026

______________________________________________________________________

## Documentation Overview

StyledConsole provides comprehensive documentation for both users and contributors.

| Document                                 | Purpose                              | Audience     |
| ---------------------------------------- | ------------------------------------ | ------------ |
| [USER_GUIDE.md](USER_GUIDE.md)           | Complete API reference with examples | All users    |
| [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) | Architecture and development guide   | Contributors |
| [../CHANGELOG.md](../CHANGELOG.md)       | Version history and release notes    | All users    |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | Development workflow and standards   | Contributors |

______________________________________________________________________

## Quick Start

**Installation:**

```bash
pip install styledconsole
```

**Basic Example:**

```python
from styledconsole import Console, icons

console = Console()
console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful",
    title=f"{icons.SPARKLES} Status",
    border="rounded",
    border_gradient_start="green",
    border_gradient_end="cyan"
)
```

______________________________________________________________________

## Learning Resources

### Getting Started

- [Installation & Setup](USER_GUIDE.md#installation)
- [Quick Start Examples](USER_GUIDE.md#quick-start)
- [Basic Concepts](USER_GUIDE.md#core-concepts)

### Core Features

- [Frames & Borders](USER_GUIDE.md#frames--borders)
- [Colors & Gradients](USER_GUIDE.md#colors--gradients)
- [Text Styling](USER_GUIDE.md#text-styling)
- [Banners](USER_GUIDE.md#banners)

### Advanced Topics

- [Emoji Support](USER_GUIDE.md#emoji-reference)
- [Icon Provider](USER_GUIDE.md#icon-provider)
- [Render Policy](USER_GUIDE.md#render-policy)
- [HTML Export](USER_GUIDE.md#html-export)
- [Theme System](USER_GUIDE.md#themes)

### For Contributors

**Development Workflow:**

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:

- Development environment setup
- Running tests and QA
- Code quality requirements
- Git workflow and commit conventions

**Architecture & Design:**

See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for:

- Architecture overview
- Module structure and patterns
- Design decisions and rationale
- Testing strategy

______________________________________________________________________

## External Resources

### Examples Repository

Comprehensive examples and visual showcases:
👉 **[StyledConsole-Examples](https://github.com/ksokolowski/StyledConsole-Examples)**

### Community

- Report issues: [GitHub Issues](https://github.com/ksokolowski/StyledConsole/issues)
- Source code: [GitHub Repository](https://github.com/ksokolowski/StyledConsole)
- Support the project: [Ko-fi](https://ko-fi.com/styledconsole)

______________________________________________________________________

## Version Information

- **Current Version:** 0.9.8.1
- **Python:** ≥3.10
- **License:** Apache-2.0
- **Status:** Production Ready

See [CHANGELOG.md](../CHANGELOG.md) for complete version history.
