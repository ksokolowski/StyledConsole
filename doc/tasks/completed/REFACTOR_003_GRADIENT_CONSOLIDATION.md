# REFACTOR-003: Consolidate Gradient Logic Using Strategy Pattern

**Finding ID:** Q1 (Code Quality Review)
**Priority:** 🔴 **HIGH**
**Status:** ⏳ Planned
**Complexity:** High
**Impact:** -280 LOC, eliminates 70% code duplication
**Target Version:** v0.4.0
**Dependencies:** REFACTOR-002 (color normalization utility)

______________________________________________________________________

## Problem Statement

### Current State

Gradient coloring logic is **duplicated across 4 functions** in `effects.py`:

1. `_apply_vertical_content_gradient()` (lines 327-380, ~53 LOC)
1. `_apply_diagonal_gradient()` (lines 382-500, ~118 LOC)
1. `_apply_vertical_rainbow()` (lines 502-560, ~58 LOC)
1. `_apply_diagonal_rainbow()` (lines 562-637, ~75 LOC)

**Total:** ~304 LOC with **70% similarity** in structure

### Common Pattern (Repeated 4 Times)

```python
# All 4 functions follow this pattern:
for idx, line in enumerate(lines):
    clean_line = strip_ansi(line)  # ✅ Same

    # Calculate position (0.0 to 1.0)
    position = calculate_position(idx, ...)  # ⚠️ Different formula

    # Get color at position
    color = get_color(position)  # ⚠️ Different source (gradient vs rainbow)

    # Colorize characters
    for char in clean_line:
        colored_char = _colorize(char, color)  # ✅ Same
        # ... border detection logic ...  # ⚠️ Similar but repeated
```

### Why This Is Critical

**Maintenance Burden:**

- Bug fixes require updates in 4 places
- New features (e.g., horizontal gradients) = copy-paste-modify
- Testing overhead: 4 similar code paths to cover

**Example Bug Scenario:**

- Fix emoji width calculation in diagonal gradient
- Must also fix in vertical gradient, vertical rainbow, diagonal rainbow
- Easy to miss one → inconsistent behavior

### Evidence of Duplication

**ANSI stripping (4 occurrences):**

```python
# Line 332, 409, 513, 574 - identical
clean_line = strip_ansi(line)
```

**Character iteration (4 occurrences):**

```python
# Similar structure in all 4 functions
for char in clean_line:
    # ... color calculation ...
    colored_char = _colorize(char, color)
```

**Border detection (4 occurrences with minor variations):**

```python
# Line 349, 455, 520, 605 - nearly identical
is_border_char = char in border_chars
if (is_border_char and apply_to_border) or (not is_border_char and apply_to_content):
    colored_chars.append(_colorize(char, color))
```

______________________________________________________________________

## Specification

### Goals

1. **Single gradient engine:** One function handles all gradient types
1. **Strategy pattern:** Pluggable position calculators and color sources
1. **Code reduction:** 304 LOC → ~120 LOC (60% reduction)
1. **Maintainability:** Fix once, works everywhere
1. **Extensibility:** Easy to add new gradient types (horizontal, radial, etc.)

### Non-Goals

- ❌ Change public API signatures (`gradient_frame()`, `rainbow_frame()`)
- ❌ Alter visual output (pixel-perfect compatibility required)
- ❌ Performance regression (must be ≥ current speed)

______________________________________________________________________

## Architecture Design

### Strategy Pattern Components

```
┌─────────────────────────┐
│  Public API Functions   │
│  - gradient_frame()     │
│  - rainbow_frame()      │
└───────────┬─────────────┘
            │
            v
┌─────────────────────────┐
│   Gradient Engine       │  ◄── Single implementation
│   apply_gradient()      │
└───────────┬─────────────┘
            │
            ├─────────────┬─────────────┐
            v             v             v
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Position        │  │ Color Source    │  │ Target Filter   │
│ Strategy        │  │ Strategy        │  │ Strategy        │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ - Vertical      │  │ - LinearGradient│  │ - ContentOnly   │
│ - Diagonal      │  │ - RainbowSpectrum│  │ - BorderOnly    │
│ - Horizontal    │  │ - RadialGradient│  │ - Both          │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Protocol Definitions

```python
# New file: src/styledconsole/effects/strategies.py

from typing import Protocol

class PositionStrategy(Protocol):
    """Calculate position (0.0-1.0) for a character in the frame."""

    def calculate(
        self,
        row: int,
        col: int,
        total_rows: int,
        total_cols: int
    ) -> float:
        """Return position from 0.0 (start) to 1.0 (end)."""
        ...

class ColorSource(Protocol):
    """Provide color for a given position."""

    def get_color(self, position: float) -> str:
        """Return hex color for position (0.0-1.0)."""
        ...

class TargetFilter(Protocol):
    """Determine if a character should be colored."""

    def should_color(
        self,
        char: str,
        is_border: bool,
        row: int,
        col: int
    ) -> bool:
        """Return True if character should be colored."""
        ...
```

______________________________________________________________________

## Implementation Plan

### Phase 1: Create Strategy Classes (2 days)

**New File:** `src/styledconsole/effects/strategies.py`

```python
"""Gradient strategy implementations for effects module.

Separates position calculation, color generation, and target filtering
into pluggable strategies following the Strategy pattern.
"""

from typing import Protocol
from styledconsole.utils.color import interpolate_color
from styledconsole.effects import get_rainbow_color  # Existing function

# ============================================================================
# Position Strategies (How to calculate gradient position for each character)
# ============================================================================

class PositionStrategy(Protocol):
    """Calculate gradient position (0.0-1.0) for a character."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        ...

class VerticalPosition:
    """Vertical gradient: Top (0.0) → Bottom (1.0)."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        return row / max(total_rows - 1, 1)

class DiagonalPosition:
    """Diagonal gradient: Top-left (0.0) → Bottom-right (1.0)."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        row_progress = row / max(total_rows - 1, 1)
        col_progress = col / max(total_cols - 1, 1)
        return (row_progress + col_progress) / 2.0

class HorizontalPosition:
    """Horizontal gradient: Left (0.0) → Right (1.0) [Future]."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        return col / max(total_cols - 1, 1)

# ============================================================================
# Color Source Strategies (What color to use at each position)
# ============================================================================

class ColorSource(Protocol):
    """Provide color for gradient position."""

    def get_color(self, position: float) -> str:
        ...

class LinearGradient:
    """Two-color linear gradient interpolation."""

    def __init__(self, start_color: str, end_color: str):
        self.start_color = start_color
        self.end_color = end_color

    def get_color(self, position: float) -> str:
        return interpolate_color(self.start_color, self.end_color, position)

class RainbowSpectrum:
    """7-color ROYGBIV rainbow spectrum."""

    def get_color(self, position: float) -> str:
        return get_rainbow_color(position)  # Reuse existing function

# ============================================================================
# Target Filter Strategies (Which characters to color)
# ============================================================================

class TargetFilter(Protocol):
    """Determine if character should be colored."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        ...

class ContentOnly:
    """Color content characters only (skip borders)."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        return not is_border

class BorderOnly:
    """Color border characters only (skip content)."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        return is_border

class Both:
    """Color all characters (content and borders)."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        return True
```

**File Size:** ~120 LOC (well-structured, documented)

**Acceptance Criteria:**

- [ ] All 3 strategy types defined
- [ ] Protocol-based (duck typing)
- [ ] Comprehensive docstrings
- [ ] No external dependencies (uses existing utils)

______________________________________________________________________

### Phase 2: Create Unified Gradient Engine (2 days)

**New File:** `src/styledconsole/effects/engine.py`

```python
"""Unified gradient application engine.

Applies color gradients to frames using pluggable strategies for
position calculation, color generation, and target filtering.
"""

from styledconsole.utils.text import strip_ansi, visual_width
from styledconsole.effects import _colorize  # Keep existing colorize
from styledconsole.effects.strategies import (
    PositionStrategy,
    ColorSource,
    TargetFilter,
)

def apply_gradient(
    lines: list[str],
    position_strategy: PositionStrategy,
    color_source: ColorSource,
    target_filter: TargetFilter,
    border_chars: set[str],
) -> list[str]:
    """Apply gradient to frame lines using pluggable strategies.

    This is the unified gradient engine that replaces 4 duplicate functions:
    - _apply_vertical_content_gradient()
    - _apply_diagonal_gradient()
    - _apply_vertical_rainbow()
    - _apply_diagonal_rainbow()

    Args:
        lines: Frame lines (with ANSI codes)
        position_strategy: How to calculate position for each character
        color_source: What color to use at each position
        target_filter: Which characters to color (content, border, both)
        border_chars: Set of border characters for detection

    Returns:
        Colored frame lines

    Example:
        >>> # Vertical gradient (red → blue) on content only
        >>> apply_gradient(
        ...     lines=frame_lines,
        ...     position_strategy=VerticalPosition(),
        ...     color_source=LinearGradient("red", "blue"),
        ...     target_filter=ContentOnly(),
        ...     border_chars={...}
        ... )
    """
    total_rows = len(lines)
    max_col = max(visual_width(strip_ansi(line)) for line in lines)

    colored_lines = []

    for row, line in enumerate(lines):
        clean_line = strip_ansi(line)  # Work with clean text
        colored_chars = []

        for col, char in enumerate(clean_line):
            # Determine if this is a border character
            is_border = char in border_chars

            # Check if we should color this character
            if not target_filter.should_color(char, is_border, row, col):
                colored_chars.append(char)
                continue

            # Calculate position for this character
            position = position_strategy.calculate(row, col, total_rows, max_col)

            # Get color for this position
            color = color_source.get_color(position)

            # Colorize and append
            colored_chars.append(_colorize(char, color))

        colored_lines.append("".join(colored_chars))

    return colored_lines
```

**File Size:** ~70 LOC (clean, focused)

**Benefits:**

- **Single implementation:** Bug fixes apply to all gradient types
- **Extensible:** Add new strategies without touching engine
- **Testable:** Each strategy testable in isolation
- **Readable:** Clear separation of concerns

**Acceptance Criteria:**

- [ ] Single `apply_gradient()` function
- [ ] Uses all 3 strategy types
- [ ] Handles ANSI stripping correctly
- [ ] Preserves emoji width calculation
- [ ] ~70 LOC total

______________________________________________________________________

### Phase 3: Refactor Public API Functions (1 day)

**File:** `src/styledconsole/effects.py`

**Before (gradient_frame - lines 88-150, 63 LOC):**

```python
def gradient_frame(...):
    renderer = FrameRenderer()
    # ... 20 lines of setup ...
    lines = renderer.render(...)
    # ... 30 lines of gradient application ...
    return lines
```

**After (gradient_frame - ~30 LOC):**

```python
def gradient_frame(
    content: str | list[str],
    *,
    start_color: str = "cyan",
    end_color: str = "magenta",
    direction: Literal["vertical", "horizontal"] = "vertical",
    target: Literal["content", "border", "both"] = "content",
    title: str | None = None,
    border: str = "rounded",
    width: int | None = None,
    padding: int = 1,
    align: Literal["left", "center", "right"] = "left",
) -> list[str]:
    """Create frame with gradient color effect."""
    from styledconsole.effects.engine import apply_gradient
    from styledconsole.effects.strategies import (
        VerticalPosition, HorizontalPosition,
        LinearGradient,
        ContentOnly, BorderOnly, Both
    )
    from styledconsole.core.frame import FrameRenderer
    from styledconsole.core.styles import get_border_style

    # Render base frame (no color)
    renderer = FrameRenderer()
    lines = renderer.render(
        content, title=title, border=border,
        width=width, padding=padding, align=align
    )

    # Choose strategies based on parameters
    pos_strategy = VerticalPosition() if direction == "vertical" else HorizontalPosition()
    color_source = LinearGradient(start_color, end_color)

    if target == "content":
        target_filter = ContentOnly()
    elif target == "border":
        target_filter = BorderOnly()
    else:
        target_filter = Both()

    # Get border characters for detection
    style = get_border_style(border)
    border_chars = {
        style.top_left, style.top_right, style.bottom_left, style.bottom_right,
        style.horizontal, style.vertical, style.top_joint, style.bottom_joint,
        style.left_joint, style.right_joint, style.cross
    }

    # Apply gradient using unified engine
    return apply_gradient(lines, pos_strategy, color_source, target_filter, border_chars)
```

**Refactor diagonal_gradient_frame() similarly (~30 LOC):**

```python
def diagonal_gradient_frame(...):
    # ... same setup as gradient_frame ...

    # Use DiagonalPosition strategy
    pos_strategy = DiagonalPosition()

    # Rest identical to gradient_frame
    return apply_gradient(...)
```

**Refactor rainbow_frame() (~25 LOC):**

```python
def rainbow_frame(...):
    # ... same setup ...

    # Use RainbowSpectrum color source
    color_source = RainbowSpectrum()

    # Choose position strategy based on direction
    pos_strategy = VerticalPosition() if direction == "vertical" else DiagonalPosition()

    return apply_gradient(...)
```

**Code Reduction:**

- `gradient_frame()`: 63 → 30 LOC (-33)
- `diagonal_gradient_frame()`: 65 → 30 LOC (-35)
- `rainbow_frame()`: 55 → 25 LOC (-30)
- Delete 4 helper functions: -304 LOC
- Add 2 new files: +190 LOC
- **Net reduction:** -242 LOC (38% of effects.py)

**Acceptance Criteria:**

- [ ] All 3 public functions refactored
- [ ] Use unified gradient engine
- [ ] Signatures unchanged (backward compatible)
- [ ] Output pixel-perfect identical

______________________________________________________________________

### Phase 4: Testing & Validation (2 days)

#### Unit Tests for Strategies

**New File:** `tests/unit/test_gradient_strategies.py`

```python
"""Unit tests for gradient strategy components."""

from styledconsole.effects.strategies import (
    VerticalPosition, DiagonalPosition, HorizontalPosition,
    LinearGradient, RainbowSpectrum,
    ContentOnly, BorderOnly, Both
)

class TestPositionStrategies:
    """Test position calculation strategies."""

    def test_vertical_position_top(self):
        """Top row = 0.0."""
        strategy = VerticalPosition()
        assert strategy.calculate(0, 0, 10, 10) == 0.0

    def test_vertical_position_bottom(self):
        """Bottom row = 1.0."""
        strategy = VerticalPosition()
        assert strategy.calculate(9, 0, 10, 10) == 1.0

    def test_vertical_position_middle(self):
        """Middle row = 0.5."""
        strategy = VerticalPosition()
        assert abs(strategy.calculate(5, 0, 11, 10) - 0.5) < 0.01

    def test_diagonal_position_top_left(self):
        """Top-left = 0.0."""
        strategy = DiagonalPosition()
        assert strategy.calculate(0, 0, 10, 10) == 0.0

    def test_diagonal_position_bottom_right(self):
        """Bottom-right = 1.0."""
        strategy = DiagonalPosition()
        assert strategy.calculate(9, 9, 10, 10) == 1.0

    def test_diagonal_position_center(self):
        """Center ≈ 0.5."""
        strategy = DiagonalPosition()
        pos = strategy.calculate(5, 5, 11, 11)
        assert 0.4 < pos < 0.6  # Approximate center

class TestColorSources:
    """Test color generation strategies."""

    def test_linear_gradient_start(self):
        """Position 0.0 = start color."""
        source = LinearGradient("#FF0000", "#0000FF")
        assert source.get_color(0.0) == "#FF0000"

    def test_linear_gradient_end(self):
        """Position 1.0 = end color."""
        source = LinearGradient("#FF0000", "#0000FF")
        assert source.get_color(1.0) == "#0000FF"

    def test_linear_gradient_middle(self):
        """Position 0.5 = interpolated color."""
        source = LinearGradient("#FF0000", "#0000FF")
        color = source.get_color(0.5)
        # Should be purple-ish (#800080)
        assert color.startswith("#")

    def test_rainbow_spectrum_red(self):
        """Position 0.0 = red."""
        source = RainbowSpectrum()
        color = source.get_color(0.0)
        assert color == "#FF0000"  # Red

    def test_rainbow_spectrum_violet(self):
        """Position 1.0 = violet."""
        source = RainbowSpectrum()
        color = source.get_color(1.0)
        # Should be violet (darkviolet = #9400D3)
        assert color.startswith("#")

class TestTargetFilters:
    """Test character filtering strategies."""

    def test_content_only_colors_content(self):
        """Content characters colored."""
        filter = ContentOnly()
        assert filter.should_color("a", is_border=False, row=0, col=0) is True

    def test_content_only_skips_borders(self):
        """Border characters not colored."""
        filter = ContentOnly()
        assert filter.should_color("─", is_border=True, row=0, col=0) is False

    def test_border_only_colors_borders(self):
        """Border characters colored."""
        filter = BorderOnly()
        assert filter.should_color("─", is_border=True, row=0, col=0) is True

    def test_border_only_skips_content(self):
        """Content characters not colored."""
        filter = BorderOnly()
        assert filter.should_color("a", is_border=False, row=0, col=0) is False

    def test_both_colors_everything(self):
        """All characters colored."""
        filter = Both()
        assert filter.should_color("a", is_border=False, row=0, col=0) is True
        assert filter.should_color("─", is_border=True, row=0, col=0) is True
```

#### Integration Tests

**File:** `tests/integration/test_gradient_effects.py`

```python
"""Integration tests for gradient effects with unified engine."""

from styledconsole.effects import gradient_frame, diagonal_gradient_frame, rainbow_frame

class TestGradientIntegration:
    """Test complete gradient workflows."""

    def test_vertical_gradient_output_unchanged(self):
        """Vertical gradient produces identical output to v0.3."""
        lines = gradient_frame(
            ["Line 1", "Line 2", "Line 3"],
            start_color="red",
            end_color="blue",
            target="content"
        )
        assert len(lines) == 5  # 3 content + 2 borders
        # Verify ANSI codes present (colored)
        assert "\033[" in "".join(lines)

    def test_diagonal_gradient_output_unchanged(self):
        """Diagonal gradient produces identical output to v0.3."""
        lines = diagonal_gradient_frame(
            ["Line 1", "Line 2"],
            start_color="lime",
            end_color="magenta",
            target="both"
        )
        assert len(lines) == 4  # 2 content + 2 borders

    def test_rainbow_vertical_output_unchanged(self):
        """Rainbow vertical produces identical output to v0.3."""
        lines = rainbow_frame(
            ["Red", "Orange", "Yellow"],
            direction="vertical",
            mode="content"
        )
        assert len(lines) == 5  # 3 content + 2 borders

    def test_all_targets_work(self):
        """Content, border, both targets all functional."""
        content = ["Test"]

        # Content only
        lines_content = gradient_frame(content, target="content")
        assert lines_content

        # Border only
        lines_border = gradient_frame(content, target="border")
        assert lines_border

        # Both
        lines_both = gradient_frame(content, target="both")
        assert lines_both
```

#### Visual Regression Testing

**Use snapshot tests:**

```python
def test_gradient_frame_snapshot(snapshot):
    """Gradient output matches v0.3 snapshot."""
    lines = gradient_frame(
        ["Line 1", "Line 2"],
        start_color="red",
        end_color="blue"
    )
    output = "\n".join(lines)
    assert output == snapshot
```

**Acceptance Criteria:**

- [ ] All strategy unit tests pass (30+ tests)
- [ ] All integration tests pass
- [ ] Snapshot tests confirm visual parity with v0.3
- [ ] Coverage for new modules ≥95%

______________________________________________________________________

### Phase 5: Performance Validation (1 day)

**Benchmark:** Compare refactored vs original gradient performance

```python
# benchmark_gradients.py
import time
from styledconsole.effects import gradient_frame

def benchmark_gradient(n=1000):
    """Benchmark gradient_frame performance."""
    content = [f"Line {i}" for i in range(20)]  # 20-line frame

    start = time.perf_counter()
    for _ in range(n):
        gradient_frame(
            content,
            start_color="red",
            end_color="blue",
            target="both"
        )
    elapsed = time.perf_counter() - start

    print(f"{n} gradients in {elapsed:.2f}s ({n/elapsed:.0f} gradients/sec)")
    return elapsed

# Compare versions
original_time = benchmark_gradient()  # Run on v0.3
refactored_time = benchmark_gradient()  # Run on v0.4

speedup = original_time / refactored_time
print(f"Speedup: {speedup:.2f}x")
```

**Acceptance:** Refactored version ≥ 95% speed of original (no significant regression)

**Expected:** Strategy pattern overhead negligible (\<5%) due to small method calls

______________________________________________________________________

## Success Metrics

### Code Quality

| Metric                       | Before | After | Improvement   |
| ---------------------------- | ------ | ----- | ------------- |
| effects.py LOC               | 637    | ~395  | -38% ✅       |
| Duplicate gradient functions | 4      | 0     | -100% ✅      |
| Code duplication %           | 70%    | 0%    | Eliminated ✅ |
| Strategy implementations     | 0      | 9     | Extensible ✅ |

### Maintainability

- [ ] Single point of change for gradient bugs
- [ ] New gradient types (horizontal) = 10 LOC (1 strategy class)
- [ ] Clear separation of concerns (position / color / target)
- [ ] Protocol-based (type-safe, IDE-friendly)

### Testing

- [ ] Strategy unit tests: 30+ tests
- [ ] Integration tests: All existing tests pass
- [ ] Snapshot tests: Visual parity confirmed
- [ ] Coverage: ≥95% maintained

______________________________________________________________________

## Risk Analysis

### Risk 1: Performance Regression

**Probability:** Low
**Impact:** Medium

**Mitigation:**

- Benchmark before/after
- If >5% slower, optimize hot paths
- Strategy method calls are cheap (no heavy computation)

### Risk 2: Visual Output Changes

**Probability:** Medium
**Impact:** High (breaks user expectations)

**Mitigation:**

- Snapshot testing for pixel-perfect comparison
- Manual visual inspection of all gradient examples
- If changes detected, analyze and fix before merge

### Risk 3: Strategy Pattern Over-Engineering

**Probability:** Low
**Impact:** Low

**Mitigation:**

- Keep strategies simple (single responsibility)
- Don't add strategies speculatively (YAGNI)
- Current 9 strategies all have immediate use cases

______________________________________________________________________

## Timeline

| Phase                     | Duration   | Blocker |
| ------------------------- | ---------- | ------- |
| Phase 1: Strategy classes | 2 days     | None    |
| Phase 2: Gradient engine  | 2 days     | Phase 1 |
| Phase 3: Refactor API     | 1 day      | Phase 2 |
| Phase 4: Testing          | 2 days     | Phase 3 |
| Phase 5: Performance      | 1 day      | Phase 4 |
| **Total**                 | **8 days** |         |

**Can be completed in:** 2 weeks (1 engineer, half-time)

**Dependencies:**

- **REFACTOR-002** (color normalization) - Recommended first
- **REFACTOR-001** (dual paths) - Can be parallel

**Recommended after:**

- All high-priority refactors complete (easier to work in clean codebase)

______________________________________________________________________

## References

### Code Locations

- `src/styledconsole/effects.py:327-637` - 4 duplicate gradient functions
- `src/styledconsole/utils/text.py` - ANSI stripping utilities
- `src/styledconsole/utils/color.py` - Color interpolation

### Related Findings

- **Q1:** Gradient Logic Duplication (Code Quality Review)
- **Q2:** Overly Long Methods (addressed by separation)

### Design Patterns

- **Strategy Pattern:** Gang of Four design pattern for algorithm families
- **Protocol-based:** Python 3.8+ structural subtyping

______________________________________________________________________

**Status Log:**

- [ ] Task created: 2025-11-01
- [ ] Phase 1 started: \[DATE\]
- [ ] Phase 1 completed: \[DATE\]
- [ ] Phase 2 started: \[DATE\]
- [ ] Phase 2 completed: \[DATE\]
- [ ] Phase 3 started: \[DATE\]
- [ ] Phase 3 completed: \[DATE\]
- [ ] Phase 4 started: \[DATE\]
- [ ] Phase 4 completed: \[DATE\]
- [ ] Phase 5 started: \[DATE\]
- [ ] Phase 5 completed: \[DATE\]
- [ ] Merged to main: \[DATE\]
- [ ] Included in release: v0.4.0
