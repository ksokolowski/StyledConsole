# REFACTOR-002: Extract Color Normalization Utility

**Finding ID:** A2 (Architecture Review)
**Priority:** 🔴 **HIGH**
**Status:** ⏳ Planned
**Complexity:** Low
**Impact:** +caching, +testability, -20 LOC duplication
**Target Version:** v0.4.0
**Dependencies:** None (can start immediately)

______________________________________________________________________

## Problem Statement

### Current State

`normalize_color()` is defined as a **nested function** inside `RenderingEngine.print_frame()` (lines 117-136), making it:

- ❌ Untestable in isolation
- ❌ Not cacheable (recreated on every frame render)
- ❌ Inaccessible to other modules needing color normalization
- ❌ Duplicated logic exists in `effects.py` via `_colorize()`

### Evidence

**Location 1: rendering_engine.py:117-136**

```python
def print_frame(self, content, ...):
    # Helper to convert color names to hex for Rich compatibility
    def normalize_color(color: str | None) -> str | None:
        """Convert color name to hex if it's not already hex."""
        if not color:
            return None
        color = color.strip()
        if color.startswith("#"):
            return color
        try:
            from styledconsole.utils.color import parse_color, rgb_to_hex
            r, g, b = parse_color(color)
            return rgb_to_hex(r, g, b)
        except Exception:  # ❌ Too broad!
            return color
```

**Location 2: effects.py:52-58** (similar logic)

```python
def _colorize(text: str, color: str) -> str:
    """Apply color to text using ANSI codes."""
    r, g, b = parse_color(color)  # Parses but doesn't normalize
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
```

### Why This Matters

1. **Performance:** Function recreated on every `print_frame()` call (no caching possible)
1. **Testing:** Cannot unit test color normalization logic independently
1. **Reusability:** Other modules (banner, layout) may need same normalization
1. **Error handling:** Broad `except Exception` hides real bugs

______________________________________________________________________

## Specification

### Goals

1. Extract `normalize_color()` to `utils/color.py` as standalone function
1. Add LRU caching for repeated color lookups
1. Improve error handling (specific exceptions)
1. Make function unit-testable
1. Reuse in `effects.py` and other modules

### Non-Goals

- ❌ Change color parsing logic (that stays in `parse_color()`)
- ❌ Modify Rich integration behavior
- ❌ Break existing API

______________________________________________________________________

## Implementation Plan

### Step 1: Create Utility Function (30 minutes)

**File:** `src/styledconsole/utils/color.py`

**Add after `interpolate_color()` function (line ~240):**

```python
@lru_cache(maxsize=256)
def normalize_color_for_rich(color: str | None) -> str | None:
    """Convert CSS4/Rich color name to hex for Rich compatibility.

    Rich's Panel and Text renderables prefer hex colors over named colors
    for consistent rendering across terminals. This function normalizes
    all color inputs to hex format.

    Args:
        color: Color in any supported format (CSS4 name, Rich name, hex, RGB tuple string)

    Returns:
        Hex color string (#RRGGBB) or None if color is None.
        Returns original string if parsing fails (let Rich handle it).

    Raises:
        No exceptions raised - returns original on parse failure.

    Example:
        >>> normalize_color_for_rich("lime")
        '#00FF00'
        >>> normalize_color_for_rich("#FF0000")
        '#FF0000'
        >>> normalize_color_for_rich("bright_green")  # Rich color
        '#00FF00'
        >>> normalize_color_for_rich(None)
        None
        >>> normalize_color_for_rich("invalid_color")
        'invalid_color'  # Returns original, let Rich handle

    Note:
        Cached with LRU cache (256 entries) for performance.
        Cache size covers all CSS4 (148) + common Rich colors (100+).
    """
    if not color:
        return None

    color = color.strip()

    # Already hex - return as-is
    if color.startswith("#"):
        return color

    # Try parsing as CSS4/Rich color name
    try:
        r, g, b = parse_color(color)
        return rgb_to_hex(r, g, b)
    except (ValueError, KeyError) as e:
        # Parsing failed - return original and let Rich try
        # This handles edge cases like Rich's special color names
        return color
```

**Update exports in `__init__.py`:**

```python
from styledconsole.utils.color import (
    # ... existing exports
    normalize_color_for_rich,  # Add this
)
```

**Acceptance Criteria:**

- [ ] Function added to `utils/color.py`
- [ ] LRU cache decorator present
- [ ] Specific exception handling (ValueError, KeyError)
- [ ] Comprehensive docstring with examples
- [ ] Exported in `__init__.py`

______________________________________________________________________

### Step 2: Add Unit Tests (1 hour)

**File:** `tests/unit/test_color_utils.py`

**Add new test class:**

```python
class TestNormalizeColorForRich:
    """Tests for normalize_color_for_rich() function."""

    def test_none_input(self):
        """None input returns None."""
        assert normalize_color_for_rich(None) is None

    def test_hex_passthrough(self):
        """Hex colors returned unchanged."""
        assert normalize_color_for_rich("#FF0000") == "#FF0000"
        assert normalize_color_for_rich("#00ff00") == "#00ff00"
        assert normalize_color_for_rich("#123ABC") == "#123ABC"

    def test_css4_color_names(self):
        """CSS4 color names converted to hex."""
        assert normalize_color_for_rich("red") == "#FF0000"
        assert normalize_color_for_rich("lime") == "#00FF00"
        assert normalize_color_for_rich("blue") == "#0000FF"
        assert normalize_color_for_rich("dodgerblue") == "#1E90FF"

    def test_rich_color_names(self):
        """Rich color names converted to hex."""
        assert normalize_color_for_rich("bright_green") == "#00FF00"
        # Add more Rich colors as needed

    def test_case_insensitive(self):
        """Color names are case-insensitive."""
        assert normalize_color_for_rich("RED") == "#FF0000"
        assert normalize_color_for_rich("Lime") == "#00FF00"
        assert normalize_color_for_rich("DODGERBLUE") == "#1E90FF"

    def test_whitespace_handling(self):
        """Leading/trailing whitespace stripped."""
        assert normalize_color_for_rich("  red  ") == "#FF0000"
        assert normalize_color_for_rich("\tlime\n") == "#00FF00"

    def test_invalid_color_returns_original(self):
        """Invalid colors return original string."""
        # Rich might understand colors we don't parse
        assert normalize_color_for_rich("invalid_color") == "invalid_color"
        assert normalize_color_for_rich("notacolor") == "notacolor"

    def test_caching_works(self):
        """LRU cache improves performance for repeated calls."""
        from styledconsole.utils.color import normalize_color_for_rich

        # Clear cache
        normalize_color_for_rich.cache_clear()

        # First call - cache miss
        result1 = normalize_color_for_rich("red")
        assert result1 == "#FF0000"

        # Second call - should hit cache
        result2 = normalize_color_for_rich("red")
        assert result2 == "#FF0000"
        assert result1 is result2  # Same object (cached)

        # Check cache stats
        info = normalize_color_for_rich.cache_info()
        assert info.hits >= 1  # At least one cache hit

    def test_cache_size_limit(self):
        """Cache respects maxsize=256."""
        from styledconsole.utils.color import normalize_color_for_rich

        normalize_color_for_rich.cache_clear()

        # Fill cache beyond limit
        for i in range(300):
            color = f"#{i:06X}"  # Generate unique hex colors
            normalize_color_for_rich(color)

        info = normalize_color_for_rich.cache_info()
        assert info.maxsize == 256
        assert info.currsize <= 256  # Respects limit
```

**Run tests:**

```bash
pytest tests/unit/test_color_utils.py::TestNormalizeColorForRich -v
```

**Acceptance Criteria:**

- [ ] All new tests pass
- [ ] Coverage for normalize_color_for_rich() = 100%
- [ ] Cache behavior verified

______________________________________________________________________

### Step 3: Refactor RenderingEngine (30 minutes)

**File:** `src/styledconsole/core/rendering_engine.py`

**Before (lines 117-136):**

```python
def print_frame(self, content, ...):
    # Helper to convert color names to hex for Rich compatibility
    def normalize_color(color: str | None) -> str | None:
        """Convert color name to hex if it's not already hex."""
        if not color:
            return None
        # ... 20 lines ...
```

**After:**

```python
def print_frame(self, content, ...):
    from styledconsole.utils.color import normalize_color_for_rich

    # Normalize all colors to hex for Rich compatibility
    content_color = normalize_color_for_rich(content_color)
    border_color = normalize_color_for_rich(border_color)
    title_color = normalize_color_for_rich(title_color)
    start_color = normalize_color_for_rich(start_color)
    end_color = normalize_color_for_rich(end_color)
```

**Changes:**

- Remove nested `normalize_color()` function (lines 117-136, -20 lines)
- Import and use `normalize_color_for_rich()` from utils
- Keep all 5 color normalization calls (content, border, title, start, end)

**Acceptance Criteria:**

- [ ] Nested function removed
- [ ] Import added at top or inline
- [ ] All 5 colors normalized using utility
- [ ] Code reduction: -20 LOC

______________________________________________________________________

### Step 4: Update Effects Module (1 hour)

**File:** `src/styledconsole/effects.py`

**Current `_colorize()` function (lines 52-58):**

```python
def _colorize(text: str, color: str) -> str:
    """Apply color to text using ANSI codes."""
    r, g, b = parse_color(color)
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
```

**Refactored:**

```python
def _colorize(text: str, color: str) -> str:
    """Apply color to text using ANSI codes.

    Args:
        color: Color in any format (CSS4/Rich name, hex, RGB tuple string)

    Returns:
        Text with ANSI color codes applied
    """
    from styledconsole.utils.color import normalize_color_for_rich, hex_to_rgb

    # Normalize to hex first (handles all color formats)
    hex_color = normalize_color_for_rich(color)

    # If normalization failed, try parsing directly
    if hex_color and hex_color.startswith("#"):
        r, g, b = hex_to_rgb(hex_color)
    else:
        # Fallback: parse directly (may raise ValueError)
        r, g, b = parse_color(color)

    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
```

**Benefits:**

- Consistent color handling with RenderingEngine
- Caching benefits for repeated color usage in gradients
- Better error handling

**Acceptance Criteria:**

- [ ] `_colorize()` uses `normalize_color_for_rich()`
- [ ] All gradient functions work unchanged
- [ ] `test_effects.py` tests pass

______________________________________________________________________

### Step 5: Integration Testing (30 minutes)

**Verify no regressions across modules:**

```bash
# Run full test suite
pytest --cov=src/styledconsole --cov-report=term-missing

# Specific module tests
pytest tests/unit/test_rendering_engine.py -v
pytest tests/unit/test_effects.py -v
pytest tests/unit/test_color_utils.py -v
pytest tests/integration/ -v

# Visual validation
python examples/run_all_visual.py
```

**Manual Testing Checklist:**

- [ ] Frames with CSS4 colors render correctly
- [ ] Frames with hex colors render correctly
- [ ] Gradient effects work with all color formats
- [ ] Banner colors work correctly
- [ ] No visible regressions in examples

**Performance Validation:**

```python
# benchmark_color_normalization.py
import time
from styledconsole.utils.color import normalize_color_for_rich

def benchmark_normalization(n=10000):
    colors = ["red", "lime", "blue", "#FF0000", "#00FF00", "#0000FF"]

    start = time.perf_counter()
    for _ in range(n):
        for color in colors:
            normalize_color_for_rich(color)
    elapsed = time.perf_counter() - start

    print(f"{n * len(colors)} normalizations in {elapsed:.3f}s")
    print(f"Rate: {(n * len(colors)) / elapsed:.0f} ops/sec")

    info = normalize_color_for_rich.cache_info()
    print(f"Cache: {info.hits} hits, {info.misses} misses, {info.currsize} entries")

benchmark_normalization()
```

**Expected:** >100K ops/sec with 99%+ cache hit rate on repeated colors

**Acceptance Criteria:**

- [ ] All 654 tests pass
- [ ] Coverage remains ≥95.96%
- [ ] No visual regressions
- [ ] Cache provides 10x+ speedup on repeated colors

______________________________________________________________________

## Documentation Updates

### Update API Reference

**File:** `doc/reference/COLOR_SYSTEM.md` (create if doesn't exist)

````markdown
## Color Normalization

### `normalize_color_for_rich(color)`

Converts any color format to hex for Rich compatibility.

**Parameters:**
- `color` (str | None): Color in CSS4, Rich, hex, or RGB format

**Returns:**
- str | None: Hex color (#RRGGBB) or None

**Example:**
```python
from styledconsole.utils.color import normalize_color_for_rich

# CSS4 colors
normalize_color_for_rich("red")  # '#FF0000'

# Already hex
normalize_color_for_rich("#FF0000")  # '#FF0000'

# Rich colors
normalize_color_for_rich("bright_green")  # '#00FF00'
````

**Performance:**

- Cached with LRU (256 entries)
- 100K+ normalizations/sec with caching

````

### Update Copilot Instructions

**File:** `.github/copilot-instructions.md`

**Add to "Color System" section:**

```markdown
### Color Normalization

**Always use `normalize_color_for_rich()` when passing colors to Rich:**

```python
from styledconsole.utils.color import normalize_color_for_rich

# ✅ Correct: Normalize before passing to Rich
hex_color = normalize_color_for_rich("lime")
panel = Panel("content", border_style=hex_color)

# ❌ Avoid: Inline nested normalization functions
def my_function():
    def normalize(c):  # Don't nest - use utility!
        ...
````

**Acceptance Criteria:**

- [ ] API reference updated
- [ ] Copilot instructions updated
- [ ] Examples demonstrate usage

______________________________________________________________________

## Success Metrics

### Code Quality

| Metric                                  | Before | After | Improvement      |
| --------------------------------------- | ------ | ----- | ---------------- |
| Nested functions in rendering_engine.py | 1      | 0     | ✅ Eliminated    |
| LOC in print_frame()                    | 117    | ~97   | -17%             |
| Testable color utils                    | 9      | 10    | +1 function      |
| Cache hit rate (repeated colors)        | 0%     | 99%+  | 🚀 Major speedup |

### Testing

- [ ] New test class: `TestNormalizeColorForRich` (10+ tests)
- [ ] Unit test coverage: 100% for new function
- [ ] Integration tests: All existing tests pass
- [ ] Performance: 10x+ speedup on repeated color normalization

### API Consistency

- [ ] Same normalization logic used in RenderingEngine and effects
- [ ] Reusable by future modules (banner, layout, etc.)
- [ ] Clear error handling (no broad exceptions)

______________________________________________________________________

## Risk Analysis

### Risk 1: Rich Might Not Understand Some Color Names

**Probability:** Low
**Impact:** Low (graceful fallback)

**Mitigation:**

- Return original string if parsing fails (Rich tries as fallback)
- Document known edge cases in function docstring

### Risk 2: Cache Memory Usage

**Probability:** Very Low
**Impact:** Negligible

**Analysis:**

- Cache size: 256 entries × ~40 bytes/entry = ~10 KB
- Trade-off: 10 KB memory for 100x speedup = worth it

### Risk 3: Import Cycle

**Probability:** Very Low
**Impact:** High (build failure)

**Mitigation:**

- `utils/color.py` has no dependencies on `core/` modules
- Verify import structure before commit

______________________________________________________________________

## Timeline

| Task                             | Duration    | Blocker   |
| -------------------------------- | ----------- | --------- |
| Step 1: Create utility           | 30 min      | None      |
| Step 2: Unit tests               | 1 hour      | Step 1    |
| Step 3: Refactor RenderingEngine | 30 min      | Step 1    |
| Step 4: Update effects           | 1 hour      | Step 1    |
| Step 5: Integration testing      | 30 min      | Steps 2-4 |
| Documentation                    | 30 min      | All steps |
| **Total**                        | **4 hours** |           |

**Can be completed in:** 1 day (half-day coding sprint)

**Dependencies:**

- None (independent task, can start immediately)

**Recommended before:**

- REFACTOR-001 (simplifies that refactor)
- REFACTOR-003 (provides utility for gradient consolidation)

______________________________________________________________________

## References

### Code Locations

- `src/styledconsole/core/rendering_engine.py:117-136` - Current nested function
- `src/styledconsole/effects.py:52-58` - Similar logic in effects
- `src/styledconsole/utils/color.py` - Target location for utility

### Related Findings

- **A2:** Color Normalization Duplication (Architecture Review)
- **Q4:** Inconsistent Error Handling (Code Quality Review)

______________________________________________________________________

**Status Log:**

- [ ] Task created: 2025-11-01
- [ ] Implementation started: \[DATE\]
- [ ] Testing completed: \[DATE\]
- [ ] Merged to main: \[DATE\]
- [ ] Included in release: v0.4.0
