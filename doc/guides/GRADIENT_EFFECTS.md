# Gradient Effects Guide

**Purpose:** How to use static gradient effects (Vertical, Diagonal, Rainbow)
**Audience:** Developers using StyledConsole
**Status:** Active (v0.4.0)

## Overview

StyledConsole allows you to apply color gradients to:

- **Content**: The text inside the frame.
- **Border**: The frame border itself.
- **Both**: Content and border simultaneously.

## 1. Vertical Gradients

Colors transition from top to bottom.

```python
from styledconsole import gradient_frame

gradient_frame(
    ["Line 1", "Line 2", "Line 3"],
    start_color="red",
    end_color="blue",
    target="both",  # 'content', 'border', or 'both'
    border="rounded"
)
```

## 2. Diagonal Gradients

Colors transition from top-left to bottom-right.

```python
from styledconsole import diagonal_gradient_frame

diagonal_gradient_frame(
    ["Diagonal", "Gradient", "Effect"],
    start_color="cyan",
    end_color="magenta",
    target="both",
    border="double"
)
```

## 3. Rainbow Effects

Applies a full 7-color spectrum (ROYGBIV).

```python
from styledconsole import rainbow_frame

rainbow_frame(
    ["🌈 Rainbow", "✨ Magic"],
    mode="both",  # 'content', 'border', or 'both'
    border="heavy"
)
```

## 4. Customizing Colors

You can use any CSS4 color name or hex code.

- **Names**: "red", "blue", "lightseagreen", "goldenrod"
- **Hex**: "#FF0000", "#00FF00"

## Advanced: Using the Engine Directly

For more control, use `apply_gradient` with specific strategies (see [Gradient Engine Reference](../reference/GRADIENT_ENGINE.md)).

```python
from styledconsole.effects.engine import apply_gradient
from styledconsole.effects.strategies import VerticalPosition, LinearGradient, Both

# ... custom logic ...
```
