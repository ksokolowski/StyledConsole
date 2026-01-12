# StyledConsole Declarative Guide

**Version:** 0.10.0
**Last Updated:** January 2026

Create beautiful terminal UIs using JSON or YAML configuration files. No Python expertise required — just define your layout in a config file and render it.

______________________________________________________________________

## Table of Contents

1. [Quick Start](#quick-start)
1. [Installation](#installation)
1. [Basic Concepts](#basic-concepts)
1. [Component Types](#component-types)
1. [Shorthand Syntax](#shorthand-syntax)
1. [Built-in Templates](#built-in-templates)
1. [Variables](#variables)
1. [Loading from Files](#loading-from-files)
1. [Examples](#examples)
1. [Reference](#reference)

______________________________________________________________________

## Quick Start

### JSON Example

```python
from styledconsole import Console

console = Console()

# Define your UI as a dictionary
console.render_dict({
    "type": "frame",
    "title": "Welcome",
    "content": "Hello from JSON configuration!",
    "border": "rounded",
    "effect": "success"
})
```

### YAML Example

```python
from styledconsole import Console, load_yaml

console = Console()

# Load from YAML string
ui = load_yaml("""
type: frame
title: Welcome
content: Hello from YAML!
border: rounded
effect: ocean
""")

console.render_object(ui)
```

______________________________________________________________________

## Installation

```bash
# Core library (JSON support built-in)
pip install styledconsole

# Add YAML support
pip install styledconsole[yaml]

# Or install everything
pip install styledconsole[all]
```

______________________________________________________________________

## Basic Concepts

### Everything is a Component

StyledConsole UIs are built from components. Each component has a `type` and properties specific to that type.

```yaml
type: frame           # What kind of component
title: My Frame       # Properties specific to frames
content: Hello!
border: rounded
```

### Nesting Components

Components can contain other components:

```yaml
type: frame
title: Dashboard
content:
  type: group
  items:
    - type: text
      content: "Line 1"
    - type: text
      content: "Line 2"
```

______________________________________________________________________

## Component Types

### Frame

A bordered box with optional title.

```yaml
type: frame
title: Status
content: All systems operational
border: rounded       # solid, rounded, double, heavy, ascii, minimal, dashed
effect: success       # Optional: gradient effect
width: 50             # Optional: fixed width
padding: 1            # Optional: internal padding
```

### Text

Styled text content.

```yaml
type: text
content: Important message
style:
  bold: true
  color: red
```

### Banner

Large ASCII art text.

```yaml
type: banner
text: HELLO
font: slant           # standard, slant, banner, big, small, mini
effect: fire
```

### Table

Data in rows and columns.

```yaml
type: table
title: Server Status
columns:
  - Server
  - Status
  - Uptime
rows:
  - [api-1, Online, 99.9%]
  - [api-2, Online, 99.8%]
  - [db-1, Maintenance, 95.2%]
border: heavy
effect: ocean
```

### Group

A container for multiple items (vertical layout).

```yaml
type: group
items:
  - type: text
    content: Header
  - type: frame
    title: Section 1
    content: Content here
  - type: frame
    title: Section 2
    content: More content
```

### Layout

Vertical layout with automatic spacing.

```yaml
type: layout
items:
  - type: banner
    text: DASHBOARD
    effect: rainbow
  - type: spacer
    lines: 1
  - type: frame
    title: Status
    content: Online
```

### Rule

A horizontal line separator.

```yaml
type: rule
style: cyan
```

### Spacer

Vertical spacing.

```yaml
type: spacer
lines: 2
```

______________________________________________________________________

## Shorthand Syntax

For common patterns, use shorthand syntax to reduce verbosity.

### String as Text

```yaml
# Shorthand
items:
  - "Just a string becomes text"

# Equivalent to
items:
  - type: text
    content: "Just a string becomes text"
```

### Frame Shorthand

```yaml
# Shorthand
frame: My content
title: My Title

# Equivalent to
type: frame
content: My content
title: My Title
```

### List of Strings

```yaml
# Content as list
type: frame
title: Status
content:
  - "Line 1"
  - "Line 2"
  - "Line 3"
```

______________________________________________________________________

## Built-in Templates

StyledConsole includes 22 ready-to-use templates for common UI patterns.

### Using Templates

```python
from styledconsole import Console

console = Console()

# Use a template with variables
console.render_template("info_box", title="Notice", content="Server maintenance scheduled")
console.render_template("success_box", content="Deployment complete!")
console.render_template("error_box", title="Error", content="Connection failed")
```

### Available Templates

#### Alert Boxes

| Template      | Description          | Variables          |
| ------------- | -------------------- | ------------------ |
| `info_box`    | Blue information box | `title`, `content` |
| `warning_box` | Yellow warning box   | `title`, `content` |
| `error_box`   | Red error box        | `title`, `content` |
| `success_box` | Green success box    | `title`, `content` |
| `tip_box`     | Aurora gradient tip  | `title`, `content` |
| `note_box`    | Steel gradient note  | `title`, `content` |

#### Headers

| Template           | Description           | Variables                |
| ------------------ | --------------------- | ------------------------ |
| `header_banner`    | Large ASCII banner    | `text`, `font`, `effect` |
| `dashboard_header` | Dashboard title frame | `title`, `subtitle`      |
| `page_header`      | Simple page header    | `title`                  |

#### Status & Metrics

| Template        | Description         | Variables                            |
| --------------- | ------------------- | ------------------------------------ |
| `status_card`   | Status display card | `title`, `status`, `message`         |
| `metric_card`   | Metric with value   | `label`, `value`, `unit`, `trend`    |
| `progress_card` | Progress display    | `title`, `current`, `total`, `label` |

#### Notifications

| Template       | Description          | Variables                  |
| -------------- | -------------------- | -------------------------- |
| `notification` | Notification message | `title`, `message`, `type` |
| `toast`        | Brief toast message  | `message`, `type`          |

#### Content

| Template     | Description     | Variables                   |
| ------------ | --------------- | --------------------------- |
| `section`    | Content section | `title`, `content`          |
| `card`       | Simple card     | `title`, `content`          |
| `code_block` | Code display    | `title`, `code`, `language` |

#### Data Display

| Template     | Description     | Variables        |
| ------------ | --------------- | ---------------- |
| `key_value`  | Key-value pairs | `title`, `items` |
| `list_panel` | List of items   | `title`, `items` |

#### Layouts

| Template         | Description               | Variables         |
| ---------------- | ------------------------- | ----------------- |
| `two_column`     | Two-column layout         | `left`, `right`   |
| `sidebar_layout` | Sidebar with main content | `sidebar`, `main` |

#### App Patterns

| Template       | Description         | Variables                     |
| -------------- | ------------------- | ----------------------------- |
| `confirmation` | Confirmation dialog | `title`, `message`, `options` |
| `loading`      | Loading indicator   | `message`                     |
| `empty_state`  | Empty state display | `title`, `message`, `action`  |

### Template Examples

```python
# Info box
console.render_template("info_box",
    title="System Notice",
    content="Scheduled maintenance tonight at 2 AM"
)

# Metric card
console.render_template("metric_card",
    label="CPU Usage",
    value="45",
    unit="%",
    trend="up"
)

# Key-value display
console.render_template("key_value",
    title="Configuration",
    items="Host: localhost\nPort: 8080\nDebug: true"
)
```

______________________________________________________________________

## Variables

Templates support variable substitution using `${variable:default}` syntax.

### Basic Variables

```yaml
type: frame
title: ${title:Untitled}
content: Hello, ${name:World}!
```

```python
console.render_template("my_template", title="Welcome", name="Alice")
# Output: title="Welcome", content="Hello, Alice!"

console.render_template("my_template")
# Output: title="Untitled", content="Hello, World!"
```

### Variables in Templates

All built-in templates use variables:

```python
# Template: info_box
# Definition:
# type: frame
# title: ${title:Info}
# content: ${content}
# effect: info

console.render_template("info_box", title="Notice", content="Check your inbox")
```

______________________________________________________________________

## Loading from Files

### JSON Files

```python
from styledconsole import Console, load_json

console = Console()

# Load from file
with open("dashboard.json") as f:
    ui = load_json(f.read())

console.render_object(ui)
```

**dashboard.json:**

```json
{
    "type": "layout",
    "items": [
        {
            "type": "banner",
            "text": "DASHBOARD",
            "effect": "rainbow"
        },
        {
            "type": "frame",
            "title": "Status",
            "content": "All systems operational",
            "effect": "success"
        }
    ]
}
```

### YAML Files

```python
from styledconsole import Console, load_yaml

console = Console()

# Load from file
with open("dashboard.yaml") as f:
    ui = load_yaml(f.read())

console.render_object(ui)
```

**dashboard.yaml:**

```yaml
type: layout
items:
  - type: banner
    text: DASHBOARD
    effect: rainbow

  - type: frame
    title: Status
    content: All systems operational
    effect: success
```

______________________________________________________________________

## Examples

### Simple Status Display

```yaml
type: frame
title: Build Status
content: |
  Tests: 427 passed
  Coverage: 94%
  Duration: 2.3s
border: rounded
effect: success
```

### Dashboard Layout

```yaml
type: layout
items:
  - type: banner
    text: MONITOR
    font: slant
    effect: ocean

  - type: spacer
    lines: 1

  - type: group
    items:
      - type: frame
        title: CPU
        content: "Usage: 45%"
        effect: success

      - type: frame
        title: Memory
        content: "Used: 2.4GB / 8GB"
        effect: info

      - type: frame
        title: Disk
        content: "Free: 120GB"
        effect: warning
```

### Server Status Table

```yaml
type: frame
title: Server Status
content:
  type: table
  columns: [Region, Server, Status, Uptime]
  rows:
    - [US-East, api-1, Online, 99.9%]
    - [US-West, api-2, Online, 99.8%]
    - [EU, api-3, Maintenance, 95.2%]
border: heavy
effect: ocean
```

### Notification Panel

```yaml
type: layout
items:
  - type: frame
    title: Notifications
    content:
      type: group
      items:
        - "INFO: New version available"
        - "WARNING: Disk space low"
        - "SUCCESS: Backup completed"
    border: rounded
    effect: info
```

______________________________________________________________________

## Reference

### Component Properties

#### Frame

| Property  | Type             | Description        |
| --------- | ---------------- | ------------------ |
| `type`    | string           | `"frame"`          |
| `title`   | string           | Frame title        |
| `content` | string/component | Frame content      |
| `border`  | string           | Border style       |
| `effect`  | string           | Effect preset name |
| `width`   | int              | Fixed width        |
| `padding` | int              | Internal padding   |

#### Text

| Property  | Type   | Description      |
| --------- | ------ | ---------------- |
| `type`    | string | `"text"`         |
| `content` | string | Text content     |
| `style`   | object | Style properties |

#### Banner

| Property | Type   | Description   |
| -------- | ------ | ------------- |
| `type`   | string | `"banner"`    |
| `text`   | string | Banner text   |
| `font`   | string | Font name     |
| `effect` | string | Effect preset |

#### Table

| Property  | Type   | Description    |
| --------- | ------ | -------------- |
| `type`    | string | `"table"`      |
| `title`   | string | Table title    |
| `columns` | list   | Column headers |
| `rows`    | list   | Row data       |
| `border`  | string | Border style   |
| `effect`  | string | Effect preset  |

#### Group

| Property | Type   | Description      |
| -------- | ------ | ---------------- |
| `type`   | string | `"group"`        |
| `items`  | list   | Child components |

#### Layout

| Property | Type   | Description      |
| -------- | ------ | ---------------- |
| `type`   | string | `"layout"`       |
| `items`  | list   | Child components |

#### Spacer

| Property | Type   | Description           |
| -------- | ------ | --------------------- |
| `type`   | string | `"spacer"`            |
| `lines`  | int    | Number of blank lines |

#### Rule

| Property | Type   | Description      |
| -------- | ------ | ---------------- |
| `type`   | string | `"rule"`         |
| `style`  | string | Line color/style |

### Effect Presets

Available effects: `fire`, `ocean`, `sunset`, `forest`, `aurora`, `success`, `warning`, `error`, `info`, `rainbow`, `rainbow_neon`, `cyberpunk`, `matrix`, `dracula`, `nord_aurora`

### Border Styles

Available borders: `solid`, `rounded`, `double`, `heavy`, `ascii`, `minimal`, `dashed`, `thick`

______________________________________________________________________

## See Also

- [Python API](PYTHON_API.md) — Full-featured Python interface
- [Jinja2 Templates](JINJA_TEMPLATES.md) — Dynamic templates with loops and conditionals
- [Visual Gallery](GALLERY.md) — Screenshots and demos
- [Examples Repository](https://github.com/ksokolowski/StyledConsole-Examples) — 50+ working demos
