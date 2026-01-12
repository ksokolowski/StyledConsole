# StyledConsole Migration Guide

**Version:** 0.10.0
**Last Updated:** January 2026

This guide helps you upgrade from earlier versions of StyledConsole to v0.10.0.

______________________________________________________________________

## Table of Contents

1. [What's New in v0.10.0](#whats-new-in-v0100)
1. [Migration Overview](#migration-overview)
1. [Classic API to v0.10.0](#classic-api-to-v0100)
1. [Gradient Syntax Changes](#gradient-syntax-changes)
1. [New Features](#new-features)
1. [Breaking Changes](#breaking-changes)
1. [Deprecations](#deprecations)

______________________________________________________________________

## What's New in v0.10.0

### Three Interfaces

v0.10.0 introduces two new ways to create UIs alongside the classic Python API:

| Interface      | Best For                           | Power Level |
| -------------- | ---------------------------------- | ----------- |
| **Python API** | Full control, complex apps         | Full        |
| **JSON/YAML**  | Config-driven UIs, non-programmers | Medium      |
| **Jinja2**     | Dynamic templates, data-driven UIs | Medium      |

### New Python API Features

- **Builder Pattern**: Fluent API for constructing components
- **Model Objects**: Immutable dataclasses for UI elements
- **90 Color Palettes**: Curated palettes with category filtering
- **Phase Animations**: Smooth gradient animations
- **22 Built-in Templates**: Ready-to-use UI patterns

______________________________________________________________________

## Migration Overview

**Good news:** All v0.9.x code continues to work in v0.10.0. Migration is optional but recommended for new code.

### Quick Comparison

```python
# Classic API (still works)
console.frame("Hello!", title="Greeting", border="rounded", effect="success")

# Builder Pattern (new)
frame = console.build_frame().title("Greeting").content("Hello!").border("rounded").effect("success").build()
console.render_object(frame)

# Model Objects (new)
from styledconsole.model import Frame
frame = Frame(content="Hello!", title="Greeting", border="rounded", effect="success")
console.render_object(frame)

# Declarative (new)
console.render_dict({"type": "frame", "title": "Greeting", "content": "Hello!", "effect": "success"})
```

______________________________________________________________________

## Classic API to v0.10.0

### Frames

```python
# Classic
console.frame("Content", title="Title", border="rounded", border_color="cyan")

# Builder
frame = (
    console.build_frame()
    .title("Title")
    .content("Content")
    .border("rounded")
    .border_color("cyan")
    .build()
)
console.render_object(frame)

# Model
from styledconsole.model import Frame
frame = Frame(content="Content", title="Title", border="rounded", border_color="cyan")
console.render_object(frame)

# Declarative
console.render_dict({
    "type": "frame",
    "title": "Title",
    "content": "Content",
    "border": "rounded",
    "border_color": "cyan"
})
```

### Banners

```python
# Classic
console.banner("HELLO", font="slant", effect="fire")

# Builder
banner = console.build_banner().text("HELLO").font("slant").effect("fire").build()
console.render_object(banner)

# Model
from styledconsole.model import Banner
banner = Banner(text="HELLO", font="slant", effect="fire")
console.render_object(banner)

# Declarative
console.render_dict({
    "type": "banner",
    "text": "HELLO",
    "font": "slant",
    "effect": "fire"
})
```

### Tables

```python
# Classic (using presets)
from styledconsole.presets.tables import create_table_from_config
table = create_table_from_config(
    theme={"border_style": "heavy"},
    data={
        "columns": [{"header": "Name"}, {"header": "Value"}],
        "rows": [["CPU", "45%"], ["RAM", "2.1GB"]]
    }
)
console.print(table)

# Builder (new)
table = (
    console.build_table()
    .title("Metrics")
    .columns("Name", "Value")
    .row("CPU", "45%")
    .row("RAM", "2.1GB")
    .border("heavy")
    .build()
)
console.render_object(table)

# Model
from styledconsole.model import Table
table = Table(
    title="Metrics",
    columns=["Name", "Value"],
    rows=[["CPU", "45%"], ["RAM", "2.1GB"]],
    border="heavy"
)
console.render_object(table)
```

### Frame Groups

```python
# Classic
console.frame_group([
    {"content": "Panel 1", "title": "First"},
    {"content": "Panel 2", "title": "Second"},
], title="Dashboard")

# Builder with Layout
from styledconsole.model import Spacer
frame1 = console.build_frame().title("First").content("Panel 1").build()
frame2 = console.build_frame().title("Second").content("Panel 2").build()

layout = (
    console.build_layout()
    .add(frame1)
    .add(frame2)
    .build()
)
console.render_object(layout)

# Declarative
console.render_dict({
    "type": "layout",
    "items": [
        {"type": "frame", "title": "First", "content": "Panel 1"},
        {"type": "frame", "title": "Second", "content": "Panel 2"}
    ]
})
```

______________________________________________________________________

## Gradient Syntax Changes

### v0.9.x (Legacy)

```python
# Still works but shows deprecation warning
console.frame(
    "Content",
    border_gradient_start="red",
    border_gradient_end="blue"
)

console.banner("TEXT", start_color="red", end_color="blue")
console.banner("TEXT", rainbow=True)
```

### v0.10.0 (Recommended)

```python
from styledconsole import EffectSpec, EFFECTS

# Using effect parameter
console.frame("Content", effect=EffectSpec.gradient("red", "blue"))
console.frame("Content", effect="fire")  # Preset name
console.frame("Content", effect=EFFECTS.rainbow)  # Registry

console.banner("TEXT", effect=EffectSpec.gradient("red", "blue"))
console.banner("TEXT", effect="rainbow")
```

______________________________________________________________________

## New Features

### Builder Pattern

Fluent API for step-by-step construction:

```python
# Chain methods for readable code
dashboard = (
    console.build_layout()
    .add(console.build_banner().text("DASHBOARD").effect("rainbow").build())
    .add(console.build_frame().title("Status").content("Online").effect("success").build())
    .add(console.build_table().columns("Metric", "Value").row("CPU", "45%").build())
    .build()
)
console.render_object(dashboard)
```

### Model Objects

Immutable dataclasses for programmatic UI construction:

```python
from styledconsole.model import Layout, Frame, Banner, Table, Text, Spacer, Rule, Style

# Compose UIs from model objects
layout = Layout(items=[
    Banner(text="REPORT", effect="ocean"),
    Spacer(lines=1),
    Frame(content="All systems operational", title="Status", effect="success"),
    Table(
        columns=["Server", "Status"],
        rows=[["api-1", "Online"], ["api-2", "Online"]]
    ),
])
console.render_object(layout)
```

### Declarative JSON/YAML

Build UIs from configuration:

```python
from styledconsole import Console, load_yaml

# Load from YAML
ui = load_yaml("""
type: layout
items:
  - type: banner
    text: DASHBOARD
    effect: rainbow
  - type: frame
    title: Status
    content: All systems operational
    effect: success
""")
console.render_object(ui)
```

### Jinja2 Templates

Dynamic UIs from data:

```python
from styledconsole import render_jinja

template = """
type: frame
title: Servers
content:
  type: group
  items:
{% for server in servers %}
    - "{{ server.status | status_icon }} {{ server.name }}"
{% endfor %}
"""
ui = render_jinja(template, servers=[{"name": "api", "status": "running"}])
Console().render_object(ui)
```

### 90 Color Palettes

```python
from styledconsole import get_palette, list_palettes, EffectSpec

# Browse palettes by category
vibrant = list_palettes("vibrant")
pastel = list_palettes("pastel")

# Use in effects
console.frame("Content", effect=EffectSpec.from_palette("ocean_depths"))
```

### Built-in Templates

22 ready-to-use UI patterns:

```python
console.render_template("info_box", title="Notice", content="Server maintenance tonight")
console.render_template("success_box", content="Deployment complete!")
console.render_template("metric_card", label="CPU", value="45", unit="%")
```

______________________________________________________________________

## Breaking Changes

### v0.10.0 has no breaking changes

All v0.9.x code continues to work. New features are additive.

______________________________________________________________________

## Deprecations

The following are deprecated and will show warnings. They will be removed in v1.0.0:

### Gradient Parameters

```python
# Deprecated
console.frame(..., border_gradient_start="red", border_gradient_end="blue")
console.banner(..., start_color="red", end_color="blue")
console.banner(..., rainbow=True)

# Use instead
console.frame(..., effect=EffectSpec.gradient("red", "blue"))
console.banner(..., effect=EffectSpec.gradient("red", "blue"))
console.banner(..., effect="rainbow")
```

### Direct Rich Access

```python
# Deprecated (internal API)
console._rich_console.print(...)

# Use instead
console.print(...)
console.render_object(...)
```

______________________________________________________________________

## Recommended Migration Path

### Step 1: Update Effects

Replace legacy gradient syntax with `effect=` parameter:

```python
# Before
console.frame("Content", border_gradient_start="red", border_gradient_end="blue")

# After
console.frame("Content", effect=EffectSpec.gradient("red", "blue"))
# Or use presets
console.frame("Content", effect="fire")
```

### Step 2: Try Builders for New Code

For new complex UIs, try the builder pattern:

```python
frame = (
    console.build_frame()
    .title("Status")
    .content("All systems go")
    .effect("success")
    .build()
)
console.render_object(frame)
```

### Step 3: Consider Declarative for Config-Driven UIs

If your UI is driven by configuration files, consider JSON/YAML:

```python
# Load UI from config file
with open("ui_config.yaml") as f:
    ui = load_yaml(f.read())
console.render_object(ui)
```

### Step 4: Use Jinja2 for Dynamic Content

For UIs that change based on data, use Jinja2 templates:

```python
ui = load_jinja_file("dashboard.yaml.j2", servers=server_list, alerts=alert_list)
console.render_object(ui)
```

______________________________________________________________________

## Need Help?

- [Python API Guide](PYTHON_API.md) — Full API reference
- [Declarative Guide](DECLARATIVE.md) — JSON/YAML configuration
- [Jinja2 Templates](JINJA_TEMPLATES.md) — Dynamic templates
- [Examples Repository](https://github.com/ksokolowski/StyledConsole-Examples) — 50+ working demos

______________________________________________________________________

## Version History

| Version  | Highlights                                                    |
| -------- | ------------------------------------------------------------- |
| v0.10.0  | Builder pattern, Model objects, JSON/YAML/Jinja2, 90 palettes |
| v0.9.9.5 | Horizontal/grid layouts, phase animations, StyledColumns      |
| v0.9.9   | Image export (PNG, WebP, GIF)                                 |
| v0.9.5   | Icons module with ASCII fallback                              |
| v0.9.0   | Effects system, EFFECTS registry                              |
| v0.8.0   | Themes                                                        |
| v0.7.0   | Frame groups                                                  |

See [CHANGELOG.md](../CHANGELOG.md) for full version history.
