# Unified Gradient Engine Reference

**Purpose:** Technical reference for the Strategy-based gradient engine
**Audience:** Contributors and advanced users extending the library
**Status:** Active (v0.4.0)

## Overview

The Unified Gradient Engine (`src/styledconsole/effects/engine.py`) replaces multiple hardcoded gradient functions with a single, extensible `apply_gradient` function. It uses the **Strategy Pattern** to decouple:

1. **Position Calculation** (Where am I?)
1. **Color Generation** (What color is this?)
1. **Target Filtering** (Should I paint this?)

## Architecture

### Core Engine

```python
def apply_gradient(
    lines: list[str],
    position_strategy: PositionStrategy,
    color_source: ColorSource,
    target_filter: TargetFilter,
    border_chars: set[str],
) -> list[str]:
    ...
```

The engine iterates over every character in the frame, calculates its position using the strategy, gets the color, and applies it if the filter allows.

### Strategies (`src/styledconsole/effects/strategies.py`)

#### 1. Position Strategies (`PositionStrategy`)

Calculates a `0.0` to `1.0` float value based on row/column.

- **`VerticalPosition`**: Top (0.0) → Bottom (1.0)
- **`HorizontalPosition`**: Left (0.0) → Right (1.0)
- **`DiagonalPosition`**: Top-Left (0.0) → Bottom-Right (1.0)
- **`OffsetPositionStrategy`**: Wraps another strategy and adds an offset (used for animations).

#### 2. Color Sources (`ColorSource`)

Returns a hex color string for a given position `0.0-1.0`.

- **`LinearGradient`**: Interpolates between two colors.
- **`RainbowSpectrum`**: Maps position to 7-color ROYGBIV spectrum.

#### 3. Target Filters (`TargetFilter`)

Decides whether to color a character.

- **`ContentOnly`**: Skips border characters.
- **`BorderOnly`**: Skips content characters.
- **`Both`**: Colors everything.

## Extending the Engine

To add a new effect, implement the relevant protocol.

### Example: Radial Gradient

```python
class RadialPosition:
    def calculate(self, row, col, total_rows, total_cols) -> float:
        # Calculate distance from center...
        return distance_normalized
```

### Example: Custom Palette

```python
class FirePalette:
    def get_color(self, position: float) -> str:
        # Map 0.0-1.0 to Yellow-Orange-Red-Black
        ...
```

## Performance

The engine is optimized to:

- Strip ANSI codes only once per line.
- Use cached border character lookups.
- Minimize object creation in the inner loop.
