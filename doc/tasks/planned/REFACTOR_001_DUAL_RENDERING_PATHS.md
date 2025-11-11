# REFACTOR-001: Eliminate Dual Rendering Paths

**Finding ID:** A1 (Architecture Review)
**Priority:** 🔴 **HIGH**
**Status:** ⏳ Planned
**Complexity:** High
**Impact:** -400 LOC, 40% maintenance reduction
**Target Version:** v0.4.0 (deprecation) → v1.0.0 (removal)

______________________________________________________________________

## Problem Statement

### Current State

v0.3.0 maintains **two complete rendering implementations**:

1. **Rich-native path** (v0.3.0):

   - `RenderingEngine.print_frame()` → Rich `Panel`
   - ANSI-safe, no wrapping bugs
   - 117 lines in `rendering_engine.py`

1. **Legacy path** (v0.1.0):

   - `FrameRenderer.render()` → custom line-by-line rendering
   - Still exported in `__init__.py` for backward compatibility
   - 356 lines in `frame.py`

### Why This Is Critical

**Technical Debt:**

- **Code duplication:** Width calculation, padding, alignment logic exists in both paths
- **Bug propagation:** Fixes must be applied to both implementations
- **API confusion:** Users don't know which to use (`Console.frame()` vs `FrameRenderer.render()`)
- **Maintenance burden:** Testing both paths for same functionality

**Evidence from Codebase:**

```python
# rendering_engine.py:74-216 (Rich-native)
def print_frame(self, content, *, title, border, ...):
    panel = Panel(content_renderable, **panel_kwargs)
    self._rich_console.print(panel)

# frame.py:50-406 (Legacy - 356 lines!)
class FrameRenderer:
    def render(self, content, *, title, border, ...):
        # Custom line-by-line rendering
        # Duplicates width calc, padding, alignment
```

**Current Usage:**

- `Console.frame()` → calls `RenderingEngine.print_frame()` (Rich Panel)
- `effects.py` → still uses `FrameRenderer` directly (line 22)
- Public API exports both (`__init__.py:16`)

______________________________________________________________________

## Specification

### Goals

1. **Single rendering path:** All frame rendering uses Rich Panel by v1.0
1. **Backward compatibility:** Existing code continues working through v0.4.x
1. **Clear migration:** Users transition smoothly with deprecation warnings
1. **Code reduction:** Eliminate ~400 LOC of duplicate logic

### Non-Goals

- ❌ Break existing code in v0.4.x
- ❌ Remove FrameRenderer before v1.0
- ❌ Change public API signatures

______________________________________________________________________

## Implementation Plan

### Phase 1: Create Adapter Pattern (v0.4.0-alpha) - 3 days

**Task:** Wrap legacy `FrameRenderer` API with Rich Panel backend

**New File:** `src/styledconsole/core/frame_adapter.py`

```python
"""Adapter for FrameRenderer → Rich Panel migration.

Provides backward-compatible FrameRenderer.render() that delegates
to RenderingEngine.print_frame() internally.
"""

from io import StringIO
from rich.console import Console as RichConsole
from styledconsole.core.rendering_engine import RenderingEngine
from styledconsole.core.frame import Frame  # Keep dataclass

class FrameAdapter:
    """Adapts legacy FrameRenderer API to Rich Panel rendering.

    v0.4.0: Replaces FrameRenderer implementation
    v1.0.0: FrameRenderer removed entirely
    """

    def __init__(self):
        # Create internal rendering engine for delegation
        self._buffer = StringIO()
        self._rich_console = RichConsole(file=self._buffer, record=False)
        self._engine = RenderingEngine(self._rich_console)

    def render(
        self,
        content: str | list[str],
        *,
        title: str | None = None,
        border: str = "solid",
        # ... all legacy parameters
    ) -> list[str]:
        """Legacy API: Returns list of rendered lines.

        Internally delegates to RenderingEngine.print_frame(),
        captures output, and splits into lines.
        """
        # Reset buffer
        self._buffer.seek(0)
        self._buffer.truncate(0)

        # Delegate to Rich Panel rendering
        self._engine.print_frame(
            content,
            title=title,
            border=border,
            # ... map all parameters
        )

        # Return as list of lines (legacy format)
        output = self._buffer.getvalue()
        return output.splitlines()
```

**Changes Required:**

- Create `frame_adapter.py` (~80 LOC)
- Update `frame.py`: Replace `FrameRenderer` implementation with `FrameAdapter`
- Keep `Frame` dataclass (still useful)
- Add deprecation warnings to `FrameRenderer` docstring

**Testing:**

- Run existing `test_frame.py` tests (should pass with adapter)
- Add adapter-specific tests in `test_frame_adapter.py`
- Verify `effects.py` still works

**Acceptance Criteria:**

- [ ] `FrameAdapter` delegates to `RenderingEngine`
- [ ] All 654 tests pass with adapter
- [ ] `effects.py` works unchanged (imports `FrameRenderer`, gets adapter)
- [ ] Output identical to v0.3.0 for all border styles

______________________________________________________________________

### Phase 2: Deprecation Warnings (v0.4.0-beta) - 1 day

**Task:** Add deprecation notices for direct `FrameRenderer` usage

**Changes:**

```python
# frame.py
import warnings

class FrameRenderer(FrameAdapter):
    """Frame renderer (DEPRECATED).

    .. deprecated:: 0.4.0
        Use ``Console.frame()`` instead. Direct use of ``FrameRenderer``
        will be removed in v1.0.0.

    Example::
        # ❌ Deprecated:
        renderer = FrameRenderer()
        lines = renderer.render("content", border="solid")

        # ✅ Recommended:
        from styledconsole import Console
        console = Console()
        console.frame("content", border="solid")
    """

    def __init__(self):
        warnings.warn(
            "FrameRenderer is deprecated as of v0.4.0 and will be removed in v1.0.0. "
            "Use Console.frame() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__()
```

**Documentation Updates:**

- Update `doc/migration/v0.1_to_v0.3.md` → add v0.4 deprecation notes
- Update README.md examples (remove `FrameRenderer` usage)
- Update `.github/copilot-instructions.md` (mark FrameRenderer as deprecated)

**Acceptance Criteria:**

- [ ] Deprecation warnings appear when `FrameRenderer()` called directly
- [ ] `Console.frame()` produces no warnings
- [ ] Documentation updated with migration path

______________________________________________________________________

### Phase 3: Refactor Effects Module (v0.4.0-rc1) - 2 days

**Task:** Eliminate `effects.py` dependency on legacy renderer

**Current Problem:**

```python
# effects.py:22 - imports legacy renderer
from styledconsole.core.frame import FrameRenderer

def gradient_frame(...):
    renderer = FrameRenderer()  # Uses legacy (now deprecated)
```

**Solution Option A - Console Integration:**

```python
# effects.py
from styledconsole import Console
from io import StringIO

def gradient_frame(
    content: str | list[str],
    *,
    start_color: str = "cyan",
    end_color: str = "magenta",
    # ... other params
) -> list[str]:
    """Create frame with gradient effect."""
    # Use Console facade instead of FrameRenderer
    buffer = StringIO()
    console = Console(file=buffer, detect_terminal=False)

    # Console.frame() already supports gradients!
    console.frame(
        content,
        start_color=start_color,
        end_color=end_color,
        # ...
    )

    return buffer.getvalue().splitlines()
```

**Solution Option B - Dependency Injection:**

```python
# effects.py
from styledconsole.core.rendering_engine import RenderingEngine

def gradient_frame(
    content: str | list[str],
    *,
    renderer: RenderingEngine | None = None,
    # ... other params
) -> list[str]:
    """Create frame with gradient effect.

    Args:
        renderer: Optional RenderingEngine. If None, creates default.
    """
    if renderer is None:
        from io import StringIO
        from rich.console import Console as RichConsole
        buffer = StringIO()
        rich_console = RichConsole(file=buffer)
        renderer = RenderingEngine(rich_console)

    # Use renderer.print_frame()
    renderer.print_frame(...)
    # Capture and return output
```

**Recommendation:** **Option A** (simpler, uses public API)

**Changes Required:**

- Refactor `gradient_frame()` to use `Console`
- Refactor `diagonal_gradient_frame()` to use `Console`
- Refactor `rainbow_frame()` to use `Console`
- Update tests in `test_effects.py`
- Remove `FrameRenderer` import from `effects.py`

**Acceptance Criteria:**

- [ ] `effects.py` imports `Console` instead of `FrameRenderer`
- [ ] All gradient functions produce identical output
- [ ] `test_effects.py` tests pass (654 total)
- [ ] No deprecation warnings from effects module

______________________________________________________________________

### Phase 4: Code Cleanup (v0.4.0 release) - 1 day

**Task:** Remove unreachable legacy code paths

**Files to Clean:**

1. **`frame.py`:**

   - Keep: `Frame` dataclass, `FrameRenderer` (as deprecated adapter)
   - Remove: `_calculate_width()`, `_render_content_line()`, gradient methods
   - Reduction: ~250 LOC → ~80 LOC

1. **`__init__.py`:**

   - Keep export: `FrameRenderer` (with deprecation warning visible)
   - Add comment: `# Deprecated in v0.4.0, removed in v1.0.0`

1. **`rendering_engine.py`:**

   - Remove duplicate `normalize_color()` nested function (moved to utils)
   - Simplification: ~117 LOC → ~100 LOC

**Acceptance Criteria:**

- [ ] Code reduction: -270 LOC in v0.4.0
- [ ] All tests pass
- [ ] Coverage remains ≥95%
- [ ] No functional regressions

______________________________________________________________________

### Phase 5: Complete Removal (v1.0.0) - 1 day

**Task:** Remove deprecated `FrameRenderer` entirely

**Changes:**

1. **Delete:** `src/styledconsole/core/frame_adapter.py`
1. **Update `frame.py`:** Remove `FrameRenderer` class entirely, keep `Frame` dataclass
1. **Update `__init__.py`:** Remove `FrameRenderer` from exports
1. **Update tests:** Delete `test_frame_adapter.py`

**Migration Guide:** Update `doc/migration/v0.4_to_v1.0.md`:

````markdown
# v0.4 → v1.0 Migration

## Removed: FrameRenderer

**Deprecated in:** v0.4.0
**Removed in:** v1.0.0

### Before (v0.4.x):
```python
from styledconsole.core.frame import FrameRenderer
renderer = FrameRenderer()
lines = renderer.render("content", border="solid")
for line in lines:
    print(line)
````

### After (v1.0+):

```python
from styledconsole import Console
console = Console()
console.frame("content", border="solid")
```

### Why?

- Dual rendering paths eliminated
- Rich Panel provides ANSI-safe rendering
- Simpler codebase, easier maintenance

````

**Acceptance Criteria:**
- [ ] `FrameRenderer` removed from codebase
- [ ] `Frame` dataclass retained (still useful for internal use)
- [ ] All imports updated
- [ ] Documentation reflects v1.0 API
- [ ] All tests pass (expected ~630 tests after adapter tests removed)

---

## Testing Strategy

### Regression Testing

**v0.4.0 Test Plan:**
1. Run full test suite: `pytest --cov=src/styledconsole` (target: 654 tests pass)
2. Visual regression: `python examples/run_all_visual.py` (manual inspection)
3. Snapshot tests: `pytest tests/snapshots/` (detect visual changes)
4. Deprecation warnings: `pytest -W error::DeprecationWarning` (should fail if warnings present)

**v1.0.0 Test Plan:**
1. Run updated test suite (expected ~630 tests)
2. Coverage check (maintain ≥95%)
3. Example validation: All `examples/` run without errors
4. Migration guide validation: Test code snippets in migration doc

### Performance Testing

**Benchmark:** Frame rendering speed before/after refactor

```python
# benchmark_frame_rendering.py
import time
from styledconsole import Console

def benchmark_frames(n=1000):
    console = Console(file=open("/dev/null", "w"))
    start = time.perf_counter()
    for i in range(n):
        console.frame(f"Line {i}", border="solid", width=80)
    elapsed = time.perf_counter() - start
    print(f"{n} frames in {elapsed:.2f}s ({n/elapsed:.0f} frames/sec)")

benchmark_frames()
````

**Acceptance:** v0.4.0 performance ≥ v0.3.0 performance (Rich Panel should be faster)

______________________________________________________________________

## Risk Analysis

### Risk 1: Breaking Changes in Effects Module

**Probability:** Medium
**Impact:** High (users depend on `gradient_frame()`)

**Mitigation:**

- Comprehensive integration tests for effects
- Keep effect function signatures unchanged
- Add tests comparing old vs new output (should be identical)

### Risk 2: Adapter Performance Overhead

**Probability:** Low
**Impact:** Low

**Mitigation:**

- Benchmark adapter vs direct Rich Panel (should be negligible)
- If >10% slower, optimize adapter or skip adapter pattern

### Risk 3: Undiscovered FrameRenderer Dependencies

**Probability:** Medium
**Impact:** Medium

**Mitigation:**

- Grep codebase for all `FrameRenderer` imports: `grep -r "FrameRenderer" src/ examples/`
- Check user-facing examples carefully
- Add integration tests that import from `__init__.py`

______________________________________________________________________

## Success Metrics

### Code Quality

| Metric                    | v0.3.0 | v0.4.0 Target | v1.0.0 Target |
| ------------------------- | ------ | ------------- | ------------- |
| Total LOC (frame.py)      | 406    | ~180          | ~80           |
| Total LOC (effects.py)    | 637    | ~350          | ~350          |
| Rendering implementations | 2      | 1 (adapter)   | 1 (native)    |
| Test count                | 654    | 654           | ~630          |
| Coverage                  | 95.96% | ≥95%          | ≥95%          |

### API Clarity

- [ ] No user confusion about which renderer to use (Console only)
- [ ] Clear deprecation path documented
- [ ] Migration guide available
- [ ] Examples use recommended patterns

### Maintenance

- [ ] Single bug fix location (no dual path updates)
- [ ] Faster feature development (one implementation)
- [ ] Cleaner codebase (less cognitive load)

______________________________________________________________________

## Dependencies

### Blocking Issues

- None (can start immediately)

### Related Tasks

- **REFACTOR-002:** Extract `normalize_color()` helper (should be done first)
- **REFACTOR-003:** Consolidate gradient logic (can be done after Phase 3)

______________________________________________________________________

## Timeline

| Phase                     | Duration   | Milestone      |
| ------------------------- | ---------- | -------------- |
| Phase 1: Adapter          | 3 days     | v0.4.0-alpha   |
| Phase 2: Deprecation      | 1 day      | v0.4.0-beta    |
| Phase 3: Effects refactor | 2 days     | v0.4.0-rc1     |
| Phase 4: Cleanup          | 1 day      | v0.4.0 release |
| Phase 5: Removal          | 1 day      | v1.0.0         |
| **Total (v0.4.0)**        | **7 days** |                |
| **Total (v1.0.0)**        | **+1 day** |                |

**Estimated Start:** After v0.3.1 patch release
**v0.4.0 Target:** November 15, 2025
**v1.0.0 Target:** December 1, 2025

______________________________________________________________________

## References

### Code Locations

- `src/styledconsole/core/rendering_engine.py:74-216` - Rich-native implementation
- `src/styledconsole/core/frame.py:50-406` - Legacy implementation
- `src/styledconsole/effects.py:22` - FrameRenderer dependency
- `src/styledconsole/__init__.py:16` - Public API export

### Related Documentation

- `doc/migration/v0.1_to_v0.3.md` - Existing migration guide
- `doc/project/PLAN.md` - Architecture overview
- `.github/copilot-instructions.md` - AI coding guidance

### Design Rationale

**Why deprecate instead of immediate removal?**

- Respect semantic versioning (breaking change = major version)
- Give users time to migrate (6 weeks: v0.4.0 → v1.0.0)
- Allow ecosystem tools to update (e.g., Robot Framework integrations)

**Why keep Frame dataclass?**

- Useful for internal state management
- Type-safe configuration object
- Not part of public API (internal use only in v1.0+)

______________________________________________________________________

**Status Updates:**

- [ ] Phase 1 started: \[DATE\]
- [ ] Phase 1 completed: \[DATE\]
- [ ] Phase 2 started: \[DATE\]
- [ ] Phase 2 completed: \[DATE\]
- [ ] Phase 3 started: \[DATE\]
- [ ] Phase 3 completed: \[DATE\]
- [ ] Phase 4 started: \[DATE\]
- [ ] Phase 4 completed (v0.4.0 released): \[DATE\]
- [ ] Phase 5 completed (v1.0.0 released): \[DATE\]
