# StyledConsole Jinja2 Templates

**Version:** 0.10.0
**Last Updated:** January 2026

Generate dynamic terminal UIs from data using Jinja2 templates. Perfect for server status displays, reports, dashboards that update from live data.

______________________________________________________________________

## Table of Contents

1. [Quick Start](#quick-start)
1. [Installation](#installation)
1. [When to Use Jinja2](#when-to-use-jinja2)
1. [Basic Syntax](#basic-syntax)
1. [Built-in Filters](#built-in-filters)
1. [Loops](#loops)
1. [Conditionals](#conditionals)
1. [Custom Filters](#custom-filters)
1. [Loading Templates](#loading-templates)
1. [Examples](#examples)

______________________________________________________________________

## Quick Start

```python
from styledconsole import Console, render_jinja

# Template with dynamic data
template = """
type: frame
title: Server Status
content:
  type: group
  items:
  {% for server in servers %}
    - "{{ server.status | status_icon }} {{ server.name }}: {{ server.status }}"
  {% endfor %}
effect: {{ 'success' if all_healthy else 'warning' }}
"""

# Render with data
servers = [
    {"name": "API", "status": "running"},
    {"name": "Database", "status": "running"},
    {"name": "Cache", "status": "warning"},
]

ui = render_jinja(template, servers=servers, all_healthy=False)
Console().render_object(ui)
```

______________________________________________________________________

## Installation

```bash
# Install with Jinja2 support
pip install styledconsole[jinja]

# Or install everything
pip install styledconsole[all]
```

______________________________________________________________________

## When to Use Jinja2

| Scenario                     | Recommended Approach    |
| ---------------------------- | ----------------------- |
| Static UI, no variables      | JSON/YAML               |
| Simple variable substitution | JSON/YAML with `${var}` |
| List of items from data      | **Jinja2**              |
| Conditional display          | **Jinja2**              |
| Complex data transformation  | **Jinja2**              |
| Computed values              | **Jinja2**              |

**Use Jinja2 when you need:**

- Loops (`{% for %}`)
- Conditionals (`{% if %}`)
- Filters for data transformation
- Complex logic in templates

______________________________________________________________________

## Basic Syntax

### Variables

```yaml
# Simple variable
title: {{ title }}

# With default value
title: {{ title | default('Untitled') }}

# Object properties
content: {{ server.name }} - {{ server.status }}
```

### Expressions

```yaml
# String concatenation
title: "{{ prefix }} - {{ suffix }}"

# Arithmetic
content: "Progress: {{ current / total * 100 }}%"

# Ternary-style conditional
effect: {{ 'success' if status == 'ok' else 'error' }}
```

______________________________________________________________________

## Built-in Filters

StyledConsole provides custom Jinja2 filters for terminal UIs.

### status_icon

Converts status strings to appropriate icons.

```yaml
content: "{{ status | status_icon }} {{ message }}"
```

| Input                                        | Output |
| -------------------------------------------- | ------ |
| `running`, `online`, `success`, `pass`, `ok` | ✅     |
| `warning`, `warn`, `degraded`                | ⚠️     |
| `error`, `fail`, `failed`, `offline`, `down` | ❌     |
| `pending`, `waiting`, `queued`               | ⏳     |
| `info`, `unknown`                            | ℹ️     |

### status_effect

Converts status to appropriate effect preset.

```yaml
effect: {{ status | status_effect }}
```

| Input                                | Output    |
| ------------------------------------ | --------- |
| `running`, `online`, `success`, `ok` | `success` |
| `warning`, `degraded`                | `warning` |
| `error`, `fail`, `offline`           | `error`   |
| Others                               | `info`    |

### icon

Gets a specific icon by name.

```yaml
content: "{{ 'ROCKET' | icon }} Deploying..."
```

### Example: Status Display

```yaml
type: frame
title: {{ service.name }}
content: "{{ service.status | status_icon }} {{ service.status | title }}"
effect: {{ service.status | status_effect }}
```

______________________________________________________________________

## Loops

Generate repeated content from lists.

### Basic Loop

```yaml
type: group
items:
{% for item in items %}
  - "{{ item }}"
{% endfor %}
```

### Loop with Index

```yaml
type: group
items:
{% for server in servers %}
  - "{{ loop.index }}. {{ server.name }}: {{ server.status }}"
{% endfor %}
```

### Nested Loops

```yaml
type: layout
items:
{% for category in categories %}
  - type: frame
    title: {{ category.name }}
    content:
      type: group
      items:
      {% for item in category.items %}
        - "{{ item }}"
      {% endfor %}
{% endfor %}
```

### Loop Variables

| Variable      | Description                   |
| ------------- | ----------------------------- |
| `loop.index`  | Current iteration (1-indexed) |
| `loop.index0` | Current iteration (0-indexed) |
| `loop.first`  | True if first iteration       |
| `loop.last`   | True if last iteration        |
| `loop.length` | Total number of items         |

______________________________________________________________________

## Conditionals

Show or hide content based on conditions.

### Basic If

```yaml
type: frame
title: Status
content:
  type: group
  items:
    - "Server: {{ server.name }}"
{% if server.error %}
    - "Error: {{ server.error }}"
{% endif %}
```

### If-Else

```yaml
effect: {% if healthy %}success{% else %}error{% endif %}
```

### If-Elif-Else

```yaml
{% if status == 'running' %}
effect: success
{% elif status == 'warning' %}
effect: warning
{% else %}
effect: error
{% endif %}
```

### Inline Conditional

```yaml
title: "{{ 'All Systems OK' if all_healthy else 'Issues Detected' }}"
effect: {{ 'success' if all_healthy else 'warning' }}
```

### Conditional Items

```yaml
type: group
items:
{% for alert in alerts %}
{% if alert.severity == 'critical' %}
  - type: frame
    title: "CRITICAL: {{ alert.title }}"
    content: {{ alert.message }}
    effect: error
{% endif %}
{% endfor %}
```

______________________________________________________________________

## Custom Filters

Register your own filters for domain-specific transformations.

```python
from styledconsole import add_jinja_filter, render_jinja

# Define a custom filter
def format_bytes(value):
    """Format bytes as human-readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if value < 1024:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} PB"

# Register the filter
add_jinja_filter("format_bytes", format_bytes)

# Use in templates
template = """
type: frame
title: Disk Usage
content: "Used: {{ bytes_used | format_bytes }} / {{ bytes_total | format_bytes }}"
"""

ui = render_jinja(template, bytes_used=1073741824, bytes_total=10737418240)
```

### Multiple Custom Filters

```python
from styledconsole import add_jinja_filter

# Percentage formatter
def as_percent(value, decimals=1):
    return f"{value * 100:.{decimals}f}%"

# Duration formatter
def format_duration(seconds):
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours}h {mins}m"

# Register filters
add_jinja_filter("as_percent", as_percent)
add_jinja_filter("duration", format_duration)
```

______________________________________________________________________

## Loading Templates

### From String

```python
from styledconsole import render_jinja

template = """
type: frame
title: {{ title }}
content: {{ content }}
"""

ui = render_jinja(template, title="Hello", content="World")
```

### From File

```python
from styledconsole import load_jinja_file

# Load .yaml.j2 or .json.j2 file
ui = load_jinja_file("templates/dashboard.yaml.j2",
    servers=server_list,
    timestamp=datetime.now()
)
```

### render_jinja_string

For templates that output the final YAML/JSON as a string (useful for debugging):

```python
from styledconsole import render_jinja_string

template = """
type: frame
title: {{ title }}
"""

# Get the rendered YAML string (before parsing)
yaml_string = render_jinja_string(template, title="Debug")
print(yaml_string)  # See the actual YAML output
```

______________________________________________________________________

## Examples

### Server Status Dashboard

```yaml
# dashboard.yaml.j2
type: layout
items:
  - type: banner
    text: STATUS
    font: slant
    effect: {{ 'success' if all_healthy else 'warning' }}

  - type: spacer
    lines: 1

  - type: frame
    title: "Servers ({{ servers | length }})"
    content:
      type: group
      items:
      {% for server in servers %}
        - "{{ server.status | status_icon }} {{ server.name }}: {{ server.status }} ({{ server.uptime }})"
      {% endfor %}
    effect: {{ 'success' if all_healthy else 'warning' }}

{% if alerts %}
  - type: frame
    title: "Alerts ({{ alerts | length }})"
    content:
      type: group
      items:
      {% for alert in alerts %}
        - "{{ alert.severity | status_icon }} {{ alert.message }}"
      {% endfor %}
    effect: error
{% endif %}
```

```python
from styledconsole import Console, load_jinja_file

servers = [
    {"name": "api-1", "status": "running", "uptime": "99.9%"},
    {"name": "api-2", "status": "running", "uptime": "99.8%"},
    {"name": "db-1", "status": "warning", "uptime": "95.2%"},
]

alerts = [
    {"severity": "warning", "message": "High memory usage on db-1"},
]

ui = load_jinja_file("dashboard.yaml.j2",
    servers=servers,
    alerts=alerts,
    all_healthy=all(s["status"] == "running" for s in servers)
)

Console().render_object(ui)
```

### Metrics Report

```yaml
# metrics.yaml.j2
type: frame
title: "{{ report_name }} - {{ timestamp }}"
content:
  type: table
  columns: [Metric, Value, Status]
  rows:
  {% for metric in metrics %}
    - - {{ metric.name }}
      - "{{ metric.value }}{{ metric.unit }}"
      - "{{ metric.status | status_icon }}"
  {% endfor %}
border: heavy
effect: {{ 'success' if overall_status == 'healthy' else 'warning' }}
```

### Build Report

```yaml
# build.yaml.j2
type: layout
items:
  - type: banner
    text: BUILD
    effect: {{ 'success' if build.success else 'error' }}

  - type: frame
    title: Summary
    content:
      type: group
      items:
        - "{{ 'ROCKET' | icon }} Version: {{ build.version }}"
        - "{{ 'TIMER_CLOCK' | icon }} Duration: {{ build.duration }}"
        - "{{ build.status | status_icon }} Status: {{ build.status }}"

{% for stage in build.stages %}
  - type: frame
    title: "{{ stage.name }}"
    content: "{{ stage.status | status_icon }} {{ stage.message }}"
    effect: {{ stage.status | status_effect }}
{% endfor %}

{% if build.errors %}
  - type: frame
    title: Errors
    content:
      type: group
      items:
      {% for error in build.errors %}
        - "{{ 'CROSS_MARK' | icon }} {{ error }}"
      {% endfor %}
    effect: error
{% endif %}
```

### Configuration Display

```yaml
# config.yaml.j2
type: frame
title: Configuration
content:
  type: group
  items:
  {% for key, value in config.items() %}
    - "{{ key }}: {{ value }}"
  {% endfor %}
border: rounded
effect: info
```

```python
config = {
    "host": "localhost",
    "port": 8080,
    "debug": True,
    "workers": 4,
}

ui = render_jinja(template, config=config)
```

______________________________________________________________________

## Tips & Best Practices

### 1. Keep Templates Simple

Split complex templates into smaller, reusable parts.

### 2. Use Filters for Formatting

Don't do complex formatting in the template — create custom filters.

```python
# Good: Use filter
content: "{{ bytes | format_bytes }}"

# Bad: Complex logic in template
content: "{{ (bytes / 1024 / 1024) | round(2) }} MB"
```

### 3. Validate Your Data

Ensure your data has the expected structure before rendering.

### 4. Use Default Values

Prevent errors from missing data.

```yaml
title: {{ title | default('Untitled') }}
effect: {{ status | status_effect | default('info') }}
```

### 5. Debug with render_jinja_string

If your output looks wrong, check the intermediate YAML:

```python
from styledconsole import render_jinja_string

yaml_output = render_jinja_string(template, **data)
print(yaml_output)  # See what YAML is being generated
```

______________________________________________________________________

## Reference

### Functions

| Function                                | Description                             |
| --------------------------------------- | --------------------------------------- |
| `render_jinja(template, **vars)`        | Render template string to ConsoleObject |
| `render_jinja_string(template, **vars)` | Render template to YAML string          |
| `load_jinja_file(path, **vars)`         | Load and render .yaml.j2/.json.j2 file  |
| `add_jinja_filter(name, func)`          | Register custom filter                  |

### Built-in Filters

| Filter          | Description                             |
| --------------- | --------------------------------------- |
| `status_icon`   | Status string to icon                   |
| `status_effect` | Status string to effect preset          |
| `icon`          | Icon name to icon character             |
| `default`       | Provide default value (Jinja2 built-in) |
| `title`         | Title case (Jinja2 built-in)            |
| `upper`         | Uppercase (Jinja2 built-in)             |
| `lower`         | Lowercase (Jinja2 built-in)             |
| `length`        | Get length (Jinja2 built-in)            |

______________________________________________________________________

## See Also

- [Python API](PYTHON_API.md) — Full-featured Python interface
- [Declarative Guide](DECLARATIVE.md) — JSON/YAML for simpler use cases
- [Visual Gallery](GALLERY.md) — Screenshots and demos
- [Jinja2 Documentation](https://jinja.palletsprojects.com/) — Full Jinja2 reference
- [Examples Repository](https://github.com/ksokolowski/StyledConsole-Examples) — 50+ working demos
