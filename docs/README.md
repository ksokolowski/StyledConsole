# StyledConsole Documentation

**Version:** 0.10.0
**Last Updated:** January 2026

______________________________________________________________________

## Documentation Overview

StyledConsole offers three interfaces for creating terminal UIs. Choose the approach that fits your needs:

| Guide                                  | Description                                 | Best For                           |
| -------------------------------------- | ------------------------------------------- | ---------------------------------- |
| [Python API](PYTHON_API.md)            | Complete API with builders, effects, themes | Full control, complex apps         |
| [Declarative](DECLARATIVE.md)          | JSON/YAML configuration                     | Config-driven UIs, non-programmers |
| [Jinja2 Templates](JINJA_TEMPLATES.md) | Dynamic templates with loops/conditionals   | Data-driven UIs                    |

### Additional Resources

| Document                              | Description                     |
| ------------------------------------- | ------------------------------- |
| [Visual Gallery](GALLERY.md)          | Screenshots and animated demos  |
| [Migration Guide](MIGRATION.md)       | Upgrading from earlier versions |
| [Developer Guide](DEVELOPER_GUIDE.md) | Architecture and contributing   |
| [Changelog](../CHANGELOG.md)          | Version history                 |

______________________________________________________________________

## Quick Start

**Installation:**

```bash
pip install styledconsole              # Core library
pip install styledconsole[yaml]        # + YAML support
pip install styledconsole[jinja]       # + Jinja2 templates
pip install styledconsole[all]         # Everything
```

**Three Ways to Create UIs:**

```python
from styledconsole import Console, icons, EffectSpec

console = Console()

# 1. Python API (full power)
console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful",
    title="Status",
    effect=EffectSpec.gradient("green", "cyan")
)

# 2. Declarative (config-driven)
console.render_dict({
    "type": "frame",
    "title": "Status",
    "content": "Build successful!",
    "effect": "success"
})

# 3. Jinja2 (dynamic templates)
from styledconsole import render_jinja
ui = render_jinja("""
type: frame
title: {{ title }}
content: {{ message }}
""", title="Status", message="Build successful!")
console.render_object(ui)
```

______________________________________________________________________

## Learning Path

### New Users

1. Start with [Python API](PYTHON_API.md) — the most comprehensive guide
1. Browse the [Visual Gallery](GALLERY.md) for inspiration
1. Try the [Examples Repository](https://github.com/ksokolowski/StyledConsole-Examples)

### Config-Driven UIs

1. Read the [Declarative Guide](DECLARATIVE.md) for JSON/YAML basics
1. Explore [Built-in Templates](DECLARATIVE.md#built-in-templates) — 22 ready-to-use patterns
1. For dynamic content, see [Jinja2 Templates](JINJA_TEMPLATES.md)

### Upgrading

- See [Migration Guide](MIGRATION.md) for changes in v0.10.0
- Check [Changelog](../CHANGELOG.md) for version history

### Contributing

- [CONTRIBUTING.md](../CONTRIBUTING.md) — Development workflow
- [Developer Guide](DEVELOPER_GUIDE.md) — Architecture and internals

______________________________________________________________________

## External Resources

- **Examples:** [StyledConsole-Examples](https://github.com/ksokolowski/StyledConsole-Examples) — 50+ working demos
- **Issues:** [GitHub Issues](https://github.com/ksokolowski/StyledConsole/issues)
- **Source:** [GitHub Repository](https://github.com/ksokolowski/StyledConsole)
- **Support:** [Ko-fi](https://ko-fi.com/styledconsole)

______________________________________________________________________

## Version Information

|             |                  |
| ----------- | ---------------- |
| **Version** | 0.10.0           |
| **Python**  | ≥3.10            |
| **License** | Apache-2.0       |
| **Status**  | Production Ready |
