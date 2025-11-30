# Animated Gradients Guide

**Purpose:** Guide on creating dynamic, animated terminal interfaces
**Audience:** Developers building interactive CLI tools
**Status:** Active (v0.4.0)

## Introduction

StyledConsole v0.4.0 introduces **Animated Gradients**, allowing you to bring your terminal UIs to life with smooth, cycling color effects. This is powered by the Unified Gradient Engine and the new `Animation` class.

## Quick Start

The easiest way to create an animation is to use the `Animation` runner with a generator that yields frames.

```python
from styledconsole.animation import Animation
from styledconsole.effects.engine import apply_gradient
from styledconsole.effects.strategies import (
    DiagonalPosition,
    RainbowSpectrum,
    OffsetPositionStrategy,
    Both
)

def frame_generator():
    offset = 0.0
    while True:
        # 1. Create strategy with current offset
        pos_strategy = OffsetPositionStrategy(
            DiagonalPosition(),
            offset=offset
        )

        # 2. Apply gradient to your lines
        colored_lines = apply_gradient(
            base_lines,
            pos_strategy,
            RainbowSpectrum(),
            Both(),
            border_chars
        )

        # 3. Yield the frame string
        yield "\n".join(colored_lines)

        # 4. Update offset for next frame
        offset += 0.05

# Run the animation
Animation.run(frame_generator(), fps=20, duration=10)
```

## Core Components

### 1. `OffsetPositionStrategy`

This is the key to animation. It wraps any static position strategy (like `VerticalPosition` or `DiagonalPosition`) and adds a float `offset`.

- `offset=0.0`: Normal gradient
- `offset=0.5`: Gradient shifted halfway
- `offset=1.0`: Back to start (loops)

By incrementing the offset in a loop, you create the illusion of movement.

### 2. `Animation.run()`

Handles the render loop details:

- Hides the cursor
- Prints the frame
- Moves the cursor back up to overwrite the previous frame
- Handles `Ctrl+C` gracefully
- Manages frame timing (FPS)

**Parameters:**

- `frames`: Iterator yielding strings
- `fps`: Frames per second (default: 10)
- `duration`: Stop after N seconds (optional)

## Best Practices

1. **Pre-render Base Content**: Don't re-render the text/layout every frame if it doesn't change. Render it once to a buffer, then just apply colors in the loop.
1. **Smoothness vs. CPU**: 20-30 FPS is usually smooth enough for terminal animations. Higher FPS uses more CPU.
1. **Clean Exit**: Always ensure your generator handles cleanup or that you use `Animation.run` which handles cursor visibility restoration.

## Example

See `examples/demo_animation.py` for a complete, runnable example.
