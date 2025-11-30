# HTML Export Guide

**Purpose:** Guide developers on how to export StyledConsole output to HTML.
**Audience:** Developers integrating console output into web reports or dashboards.
**Status:** Active (v0.5.0)

StyledConsole provides a powerful HTML export feature that preserves all ANSI styling, colors, and gradients. It builds upon Rich's export capabilities but adds enhanced customization options.

## 1. Basic Export

To export output, you must initialize the `Console` with `record=True`.

```python
from styledconsole import Console

# 1. Initialize with recording enabled
console = Console(record=True)

# 2. Print content
console.print("Hello, [bold blue]World![/]")
console.banner("Status Report", start_color="green", end_color="blue")

# 3. Export to HTML
html = console.export_html()

# 4. Save to file
with open("output.html", "w") as f:
    f.write(html)
```

## 2. Enhanced Customization (v0.5.0+)

The `ExportManager` (accessible via `console.export_html`) supports additional parameters for customization.

### Page Title

Set a custom title for the HTML page (displayed in browser tab).

```python
html = console.export_html(page_title="My Dashboard")
```

### Custom CSS

Inject custom CSS to style the page background, fonts, or container.

```python
custom_css = """
body {
    background-color: #1a1a1a;
    font-family: 'Fira Code', monospace;
}
.rich-terminal {
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    border-radius: 8px;
    margin: 2rem auto;
    max-width: 1000px;
}
"""

html = console.export_html(theme_css=custom_css)
```

### Themes

Apply a specific terminal theme to the export.

```python
from rich.terminal_theme import MONOKAI

html = console.export_html(theme=MONOKAI)
```

### Clearing Buffer

Clear the recording buffer after export to start fresh.

```python
html = console.export_html(clear_screen=True)
```

## 3. Full Example

See `examples/showcase/demo_html_export.py` for a complete runnable example.

```python
from styledconsole import Console
from rich.terminal_theme import MONOKAI

def export_dashboard():
    console = Console(record=True, width=100)

    # ... render content ...
    console.banner("REPORT", start_color="red", end_color="yellow")

    html = console.export_html(
        page_title="System Report",
        theme=MONOKAI,
        theme_css="body { background: #222; }",
        inline_styles=True
    )

    with open("report.html", "w") as f:
        f.write(html)
```
