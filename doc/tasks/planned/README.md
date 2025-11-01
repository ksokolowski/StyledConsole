# Refactoring Action Plans - Summary

**Generated:** November 1, 2025
**Based on:** Deep Design & Code Quality Analysis (v0.3.0)
**Target Version:** v0.4.0
**Status:** 📋 Planning Phase

---

## Overview

This directory contains **specification-driven action plans** for architectural improvements and code quality enhancements identified in the comprehensive codebase review.

Each plan follows the **Documentation Policy** (doc/DOCUMENTATION_POLICY.md):
- ✅ Traceable findings (ID references)
- ✅ Actionable steps with acceptance criteria
- ✅ Prioritized by impact and complexity
- ✅ Specification-based (why, what, how)

---

## High Priority Plans (v0.4.0)

### 🔴 REFACTOR-001: Eliminate Dual Rendering Paths
**File:** [`REFACTOR_001_DUAL_RENDERING_PATHS.md`](REFACTOR_001_DUAL_RENDERING_PATHS.md)
**Finding:** A1 (Architecture Review)
**Impact:** -400 LOC, 40% maintenance reduction
**Duration:** 7 days (v0.4.0) + 1 day (v1.0.0 cleanup)

**Problem:** v0.3.0 maintains both Rich-native (`RenderingEngine`) and legacy (`FrameRenderer`) implementations, causing:
- Code duplication (width calc, padding, alignment)
- Bug propagation risk (fix must apply to both)
- API confusion (which to use?)

**Solution:** Adapter pattern → deprecation (v0.4) → removal (v1.0)

**Phases:**
1. Create `FrameAdapter` (wraps legacy API with Rich backend)
2. Add deprecation warnings
3. Refactor `effects.py` to use Console API
4. Code cleanup (-270 LOC)
5. Complete removal in v1.0

**Dependencies:** None (can start immediately)

---

### 🔴 REFACTOR-002: Extract Color Normalization Utility
**File:** [`REFACTOR_002_COLOR_NORMALIZATION.md`](REFACTOR_002_COLOR_NORMALIZATION.md)
**Finding:** A2 (Architecture Review)
**Impact:** +caching, +testability, -20 LOC duplication
**Duration:** 4 hours (half-day sprint)

**Problem:** `normalize_color()` defined as **nested function** in `RenderingEngine.print_frame()`:
- Not testable in isolation
- Not cacheable (recreated every call)
- Duplicated logic in `effects.py`

**Solution:** Extract to `utils/color.py` with LRU caching

**Steps:**
1. Create `normalize_color_for_rich()` utility (30 min)
2. Add comprehensive unit tests (1 hour)
3. Refactor RenderingEngine (30 min)
4. Update effects module (1 hour)
5. Integration testing (30 min)

**Dependencies:** None (quick win, recommended first)

---

### 🔴 REFACTOR-003: Consolidate Gradient Logic
**File:** [`REFACTOR_003_GRADIENT_CONSOLIDATION.md`](REFACTOR_003_GRADIENT_CONSOLIDATION.md)
**Finding:** Q1 (Code Quality Review)
**Impact:** -280 LOC, eliminates 70% duplication
**Duration:** 8 days (2 weeks half-time)

**Problem:** **4 nearly-identical gradient functions** (304 LOC total):
- `_apply_vertical_content_gradient()`
- `_apply_diagonal_gradient()`
- `_apply_vertical_rainbow()`
- `_apply_diagonal_rainbow()`

**Solution:** Strategy pattern with pluggable components

**Architecture:**
```
Gradient Engine (unified)
├── Position Strategies (Vertical, Diagonal, Horizontal)
├── Color Sources (LinearGradient, RainbowSpectrum)
└── Target Filters (ContentOnly, BorderOnly, Both)
```

**Phases:**
1. Create strategy classes (2 days)
2. Build unified gradient engine (2 days)
3. Refactor public API functions (1 day)
4. Testing & validation (2 days)
5. Performance benchmarking (1 day)

**Dependencies:** REFACTOR-002 recommended first

---

## Implementation Roadmap

### Timeline (v0.4.0 - 3 weeks)

```
Week 1: Foundation
├─ Day 1-2: REFACTOR-002 (Color normalization) ✅ Quick win
├─ Day 3-5: REFACTOR-001 Phase 1-3 (Adapter + deprecation)
└─ Day 6-7: REFACTOR-001 Phase 4 (Cleanup)

Week 2-3: Consolidation
├─ Day 8-9: REFACTOR-003 Phase 1 (Strategies)
├─ Day 10-11: REFACTOR-003 Phase 2 (Engine)
├─ Day 12: REFACTOR-003 Phase 3 (API refactor)
├─ Day 13-14: REFACTOR-003 Phase 4 (Testing)
└─ Day 15: REFACTOR-003 Phase 5 (Performance)

Final: Integration & Release
├─ Day 16-17: Full integration testing
├─ Day 18: Documentation updates
├─ Day 19: Migration guide completion
└─ Day 20: v0.4.0 release
```

### Dependencies Graph

```
REFACTOR-002 (Color norm)
    ↓
    ├─→ REFACTOR-001 (Dual paths) ← Can be parallel
    └─→ REFACTOR-003 (Gradients)
```

**Recommendation:** Execute in order (002 → 001 → 003) for cleanest implementation.

---

## Success Metrics

### Code Quality Improvements

| Metric | v0.3.0 | v0.4.0 Target | Improvement |
|--------|--------|---------------|-------------|
| Total LOC (src/) | 5,477 | 4,957 | -9.5% ✅ |
| Code duplication | ~15% | ~5% | -67% ✅ |
| Longest method | 132 lines | <60 lines | -54% ✅ |
| Rendering implementations | 2 | 1 | -50% ✅ |
| Test coverage | 95.96% | ≥96% | Maintained ✅ |

### Maintainability Gains

- **Single bug fix location:** No more dual-path updates
- **Faster feature development:** One implementation vs two
- **Cleaner architecture:** Strategy pattern for extensibility
- **Better testability:** Isolated components

### Developer Experience

- [ ] Clear API (no confusion about which renderer to use)
- [ ] Reusable utilities (color normalization, gradients)
- [ ] Extensible design (add gradient types easily)
- [ ] Comprehensive tests (>95% coverage maintained)

---

## Risk Management

### High-Risk Areas

1. **Visual Output Changes** (REFACTOR-003)
   - **Mitigation:** Snapshot testing for pixel-perfect comparison
   - **Validation:** Manual inspection of all examples

2. **Breaking Changes** (REFACTOR-001)
   - **Mitigation:** Deprecation warnings in v0.4, removal in v1.0
   - **Validation:** Clear migration guide

3. **Performance Regression** (REFACTOR-003)
   - **Mitigation:** Benchmark before/after (accept <5% regression)
   - **Validation:** Strategy pattern overhead should be negligible

### Rollback Plan

Each refactor is **atomic** with clear acceptance criteria:
- If tests fail → investigate and fix
- If >5% performance regression → optimize or revert
- If visual regressions → analyze root cause, fix before merge

---

## Medium Priority (v0.5.0+)

These plans address medium-priority findings and can be tackled after v0.4.0 release:

### 🟡 Architecture Improvements
- **A4:** Dependency injection for TerminalManager (+testability)
- **A5:** Centralize logging setup (-60 LOC duplication)

### 🟡 Code Quality
- **Q2:** Break up 100+ line methods (SRP violations)
- **Q3:** Replace magic numbers with named constants
- **Q4:** Improve error handling specificity

### 🟡 Performance
- **P1:** Fix string concatenation in tight loops (O(n²) → O(n))
- **P2:** Pre-strip ANSI codes in gradients (reduce regex overhead)
- **P3:** Cache emoji width calculations

### 🟡 Extensibility
- **E1:** BorderStyleRegistry for custom styles
- **E2:** Theme system for color presets

---

## Testing Strategy

### Per-Refactor Testing

Each plan includes:
- **Unit tests:** Isolated component testing
- **Integration tests:** Cross-component workflows
- **Snapshot tests:** Visual regression prevention
- **Performance tests:** Benchmark before/after

### Pre-Release Validation (v0.4.0)

```bash
# Full test suite
pytest --cov=src/styledconsole --cov-report=html

# Visual validation
python examples/run_all_visual.py

# Performance benchmarks
python benchmarks/run_all.py

# Deprecation warnings check
pytest -W error::DeprecationWarning
```

**Acceptance:** All tests pass, coverage ≥95.96%, no visual regressions

---

## References

### Source Documents

- **Analysis Report:** Architecture & Code Quality Review (2025-11-01)
- **Documentation Policy:** `doc/DOCUMENTATION_POLICY.md`
- **Architecture Overview:** `doc/project/PLAN.md`
- **Current Tasks:** `doc/project/TASKS.md`

### Codebase References

- `src/styledconsole/core/rendering_engine.py` - Rich-native rendering
- `src/styledconsole/core/frame.py` - Legacy renderer
- `src/styledconsole/effects.py` - Gradient implementations
- `src/styledconsole/utils/color.py` - Color utilities

### External Resources

- **Strategy Pattern:** Gang of Four Design Patterns
- **Semantic Versioning:** https://semver.org/
- **Python Protocols:** PEP 544 (Structural Subtyping)

---

## Status Updates

### Completion Tracking

- [ ] REFACTOR-001 completed: [DATE] → v0.4.0 release
- [ ] REFACTOR-002 completed: [DATE] → v0.4.0 release
- [ ] REFACTOR-003 completed: [DATE] → v0.4.0 release
- [ ] v0.4.0 released: [TARGET: November 15, 2025]
- [ ] REFACTOR-001 Phase 5: [DATE] → v1.0.0 release
- [ ] v1.0.0 released: [TARGET: December 1, 2025]

### Change Log

- **2025-11-01:** Initial plans created based on analysis
- [Future entries as work progresses]

---

## Contributing

These action plans are **living documents**. Update status as work progresses:

1. Mark phases complete with dates
2. Note any deviations from plan (with rationale)
3. Update metrics after completion
4. Move completed plans to `doc/tasks/completed/` upon release

**Questions?** Refer to `doc/DOCUMENTATION_POLICY.md` for documentation guidelines.
