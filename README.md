# StyledConsole

[![Python >=3.10](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Version](https://img.shields.io/badge/version-0.10.4-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole/releases)
[![Tests](https://img.shields.io/badge/tests-1328%20passing-success.svg)](https://github.com/ksokolowski/StyledConsole)
[![Coverage](https://img.shields.io/badge/coverage-79%25-brightgreen.svg)](https://github.com/ksokolowski/StyledConsole)
[![PyPI](https://img.shields.io/pypi/v/styledconsole.svg)](https://pypi.org/project/styledconsole/)

**A multi-interface Python library for elegant terminal output** — use Python code, JSON/YAML configuration, or Jinja2 templates to create beautiful CLI experiences.

```bash
pip install styledconsole              # Core library
pip install styledconsole[yaml]        # + YAML support
pip install styledconsole[jinja]       # + Jinja2 templates
pip install styledconsole[all]         # Everything
```

______________________________________________________________________

## Three Ways to Style Your Terminal

### Python API (Full Power)

The complete API with builders, effects, gradients, themes, and export capabilities.

```python
from styledconsole import Console, icons, EffectSpec

console = Console()
console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful\n{icons.ROCKET} Deployed to production",
    title="Status",
    effect=EffectSpec.gradient("green", "cyan"),
)
```

### JSON/YAML Configuration (No Code Required)

Perfect for config-driven UIs and non-programmers. JSON Schema available for IDE autocomplete.

```python
from styledconsole import Console

console = Console()
console.render_dict({
    "type": "frame",
    "title": "Status",
    "content": "Build successful!",
    "effect": "success"
})
```

### Jinja2 Templates (Dynamic Content)

Generate UIs from data with loops, conditionals, and filters.

```python
from styledconsole import Console, render_jinja

template = """
type: frame
title: Server Status
content:
  type: group
  items:
  {% for server in servers %}
    - "{{ server.status | status_icon }} {{ server.name }}: {{ server.status }}"
  {% endfor %}
"""
obj = render_jinja(template, servers=[{"name": "API", "status": "running"}])
Console().render_object(obj)
```

______________________________________________________________________

## CLI Preview Tool

Explore features without writing code:

```bash
styledconsole demo              # Interactive feature showcase
styledconsole palette           # List 90 color palettes
styledconsole effects fire      # Preview effect presets
styledconsole icons rocket      # Search 200+ icons
styledconsole render config.yaml # Render a config file
styledconsole schema            # Get JSON Schema for IDE config
```

______________________________________________________________________

## Key Features

| Feature                   | Description                                                     |
| ------------------------- | --------------------------------------------------------------- |
| **Gradient Engine**       | Rainbow and linear gradients on borders, text, backgrounds      |
| **Smart Icons**           | 224 icons with automatic ASCII fallback for CI/legacy terminals |
| **Effects System**        | 47 presets + 90 color palettes + phase animations               |
| **Builder Pattern**       | Fluent API for complex layouts                                  |
| **Environment Detection** | Auto-adapts for `NO_COLOR`, `CI`, `TERM=dumb`                   |
| **Export Formats**        | HTML, PNG, WebP, GIF with full emoji support                    |
| **JSON Schema**           | IDE autocomplete for YAML/JSON configuration files              |
| **22 Built-in Templates** | Ready-to-use UI patterns                                        |

______________________________________________________________________

## Documentation

| Guide                                          | Description                                                |
| ---------------------------------------------- | ---------------------------------------------------------- |
| **[Getting Started](docs/GETTING_STARTED.md)** | **Zero to dashboard in minutes — start here!**             |
| [Python API](docs/PYTHON_API.md)               | Complete API reference — builders, effects, themes, export |
| [Declarative Guide](docs/DECLARATIVE.md)       | JSON/YAML configuration for config-driven UIs              |
| [Jinja2 Templates](docs/JINJA_TEMPLATES.md)    | Dynamic templates with loops and filters                   |
| [Visual Gallery](docs/GALLERY.md)              | Screenshots and animated demos                             |
| [Developer Guide](docs/DEVELOPER_GUIDE.md)     | Architecture and contributing                              |

______________________________________________________________________

## Quick Links

- [Examples Repository](https://github.com/ksokolowski/StyledConsole-Examples) — 60+ working demos
- [Changelog](CHANGELOG.md) — Version history

______________________________________________________________________

## Support

| Platform        | Link                                                                       |
| --------------- | -------------------------------------------------------------------------- |
| GitHub Sponsors | [github.com/sponsors/ksokolowski](https://github.com/sponsors/ksokolowski) |
| Ko-fi           | [ko-fi.com/styledconsole](https://ko-fi.com/styledconsole)                 |

______________________________________________________________________

**Apache License 2.0** — Built on [Rich](https://github.com/Textualize/rich), [PyFiglet](https://github.com/pwaller/pyfiglet), and [emoji](https://pypi.org/project/emoji/).
