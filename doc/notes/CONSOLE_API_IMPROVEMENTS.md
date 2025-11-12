# Console API Improvement Ideas

**Date:** November 12, 2025
**Context:** Identified during gallery examples development

## 1. Nested Frames / Frame Grouping

### Current Limitation

Users cannot easily create true nested frames (frames within frames) using Console API alone. The workaround requires:

- Using Rich Panel directly
- Accessing `console._rich_console` (internal API)
- Complex string capturing logic

### Use Case

System monitoring dashboards, multi-level information hierarchy, visual grouping of related frames.

### Example from borders_showcase.py

```python
# Current: Multiple independent frames (logical grouping, not visual nesting)
console.frame(cpu_content, title="CPU Status", border="rounded", border_color="green", width=35)
console.frame(memory_content, title="Memory Status", border="rounded", border_color="yellow", width=35)
console.frame(network_content, title="Network Status", border="rounded", border_color="cyan", width=35)
```

### Proposed API

```python
# Option A: Context manager
with console.group(title="System Dashboard", border="heavy", border_color="blue"):
    console.frame(cpu_content, title="CPU Status", border="rounded", border_color="green")
    console.frame(memory_content, title="Memory Status", border="rounded", border_color="yellow")
    console.frame(network_content, title="Network Status", border="rounded", border_color="cyan")

# Option B: Explicit nesting
dashboard = console.create_group(title="System Dashboard", border="heavy")
dashboard.frame(cpu_content, title="CPU Status", border="rounded")
dashboard.frame(memory_content, title="Memory Status", border="rounded")
console.print(dashboard)

# Option C: Container parameter
console.frame(
    [
        ("CPU Status", cpu_content, {"border": "rounded", "border_color": "green"}),
        ("Memory Status", memory_content, {"border": "rounded", "border_color": "yellow"}),
        ("Network Status", network_content, {"border": "rounded", "border_color": "cyan"}),
    ],
    container_title="System Dashboard",
    container_border="heavy",
    container_color="blue"
)
```

### Implementation Notes

- Should leverage Rich's Panel and Group internally
- Maintain emoji-safe width calculations
- Support gradient borders on both container and nested frames
- Consider padding/spacing between nested elements

### Priority

Medium - Nice-to-have for advanced use cases, not blocking basic functionality

______________________________________________________________________

## Future Ideas

Add more improvement ideas here as they're identified during development.
