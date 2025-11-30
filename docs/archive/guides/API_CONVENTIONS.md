# API Conventions & Best Practices

**Purpose:** Define standard naming conventions and behaviors for the StyledConsole API.
**Audience:** Developers using or contributing to the library.
**Status:** Active (v0.4.0)

This guide outlines the standard conventions used across the StyledConsole API. Following these patterns ensures consistent behavior and predictable results.

## 1. Color Parameter Conventions

StyledConsole uses a standardized naming scheme for color parameters to avoid ambiguity.

### Single-Region APIs

For APIs that affect a single visual element (like text or a simple banner), use the `color` parameter.

- **`color`**: Sets the solid color of the text or element.
  - Accepts: CSS4 names ("red", "dodgerblue"), hex codes ("#ff0000"), or RGB tuples.

```python
console.text("Hello", color="cyan")
console.rule("Title", color="green")
```

### Multi-Region APIs (Frames)

For APIs that have distinct visual regions (border, content, title), use specific color parameters.

- **`content_color`**: Sets the color of the text content inside the frame.
- **`border_color`**: Sets the color of the border characters.
- **`title_color`**: Sets the color of the title text.

```python
console.frame(
    "Content",
    content_color="white",
    border_color="blue",
    title_color="cyan"
)
```

### Gradients

For gradient effects, use `start_color` and `end_color`.

- **`start_color`**: The starting color of the gradient.
- **`end_color`**: The ending color of the gradient.

```python
console.banner("Gradient", start_color="red", end_color="blue")
```

> **Note:** Avoid using `style="gradient"` or passing tuples to `color` parameters. Always use explicit `start_color` and `end_color` for clarity.

______________________________________________________________________

## 2. Alignment & Layout

Alignment behavior depends on the context of the API.

### Frame Alignment (`console.frame`)

The `align` parameter controls the alignment of the **content inside the frame**.

- **`align="left"`** (default): Content is left-aligned within the box.
- **`align="center"`**: Content is centered within the box.
- **`align="right"`**: Content is right-aligned within the box.

The frame **itself** is rendered as a single block and then aligned as a unit:

- `align="left"` (default): Frame block printed starting at the left edge.
- `align="center"`: Entire frame block centered within the console width.
- `align="right"`: Entire frame block right-aligned.

Internally, `console.frame` first computes emoji/markup-safe line widths and then
centers/aligns the resulting ANSI frame as a whole. No additional Rich layout
wrappers are required for basic frame alignment.

### Banner Alignment (`console.banner`)

The `align` parameter controls the alignment of the **ASCII art** relative to the screen or specified width.

- **`align="center"`** (default): The banner is centered.
- **`align="left"`**: The banner is left-aligned.
- **`align="right"`**: The banner is right-aligned.

### Text Alignment (`console.text`)

`console.text` does not have an `align` parameter. To align text, wrap it in a frame or use a layout component.

```python
# To center text:
console.frame("Centered Text", align="center", border="none")
```

### Deterministic Layout & Markup

For predictable results, especially in scripts or non-interactive environments, always specify an explicit `width`.

```python
# Deterministic centering within 80 columns
console.banner("Title", width=80, align="center")

# Frames with Rich markup in content or titles
console.frame(
  ["[bold]Primary[/] status", "[green]OK[/]"],
  title="[cyan]Service[/]",
  border="rounded",
  width=40,
  align="center",
)
```

> **Note:** StyledConsole's internal layout functions are aware of Rich
> markup tags when computing frame widths and truncation, so alignment is
> based on the visible text, not the raw tag characters.

______________________________________________________________________

## 3. Error Handling & Validation

StyledConsole aims to be helpful but robust.

### Unknown Values

- **Colors**: Unknown color names will typically fall back to the default terminal color or raise a `StyleError` (Rich exception) depending on the context.
- **Borders/Fonts**: Invalid border or font names will raise a `ValueError` or `KeyError` with a helpful message listing available options.

### Ambiguous Configurations

- **Partial Gradients**: Providing `start_color` without `end_color` (or vice versa) is undefined behavior. In most cases, it will fall back to a solid color using the provided value, or ignore the gradient effect. Always provide both.

### Debugging

Enable debug mode to see detailed logs about rendering decisions and fallbacks.

```python
console = Console(debug=True)
```
