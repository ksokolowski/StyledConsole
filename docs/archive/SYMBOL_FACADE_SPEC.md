# Symbol Facade Unification Specification

**Version:** 1.0
**Date:** December 7, 2025
**Target Release:** v0.9.5
**Status:** SPECIFICATION COMPLETE

______________________________________________________________________

## Executive Summary

This specification defines the unification of StyledConsole's symbol handling
systems (`icons` and `EMOJI`) into a clear hierarchical relationship. The goal
is to reduce API complexity while maintaining full backward compatibility.

**Key Decision:** Establish `icons` as the primary facade for terminal output,
with `EMOJI` serving as the underlying data layer.

______________________________________________________________________

## Problem Analysis

### Current Architecture

StyledConsole v0.9.1 exposes two parallel systems at the top-level API:

```text
┌─────────────────────────────────────────────────────────────────┐
│                        __init__.py                               │
├─────────────────────────────────────────────────────────────────┤
│  EMOJI (emoji_registry.py)    │    icons (icons.py)             │
│  ─────────────────────────    │    ─────────────────            │
│  • 4000+ emojis               │    • 224 icons                  │
│  • Pure data (str)            │    • Policy-aware (Icon)        │
│  • Always returns emoji       │    • ASCII fallback             │
│  • No terminal awareness      │    • Terminal-aware             │
└─────────────────────────────────────────────────────────────────┘
```

### Identified Issues

| Issue                    | Description                              | Impact                    |
| ------------------------ | ---------------------------------------- | ------------------------- |
| **Conceptual Overlap**   | Same names exist in both systems         | Confusion                 |
| **Abstraction Mismatch** | `EMOJI` is data, `icons` is a service    | Inconsistent mental model |
| **User Confusion**       | When to use which?                       | Poor DX                   |
| **Policy Asymmetry**     | `icons` respects policy, `EMOJI` doesn't | Inconsistent behavior     |
| **Maintenance Burden**   | Two systems to document/maintain         | Technical debt            |

### Evidence of Confusion

```python
# User must understand internal architecture to choose correctly:

# For terminal output (but which one?)
print(f"{EMOJI.CHECK_MARK_BUTTON} Done")    # ✅ - breaks in CI
print(f"{icons.CHECK_MARK_BUTTON} Done")    # ✅ or [OK] - correct

# Both work, but only one is correct for the context
```

______________________________________________________________________

## Solution Design

### Target Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                      Application Code                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              icons (Primary Facade)                              │
│  ───────────────────────────────────────────────────            │
│  • 224+ policy-aware symbols                                    │
│  • Auto emoji/ASCII based on RenderPolicy                       │
│  • Recommended for ALL terminal output                          │
│  • Uses EMOJI internally for emoji data                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ internal
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              EMOJI (Data Layer)                                  │
│  ───────────────────────────────────────────────────            │
│  • 4000+ raw emoji characters                                   │
│  • Pure data, no policy awareness                               │
│  • For advanced use: file output, non-terminal contexts         │
│  • Available but not primary API                                │
└─────────────────────────────────────────────────────────────────┘
```

### Design Principles

1. **Single Recommended API** - `icons` for terminal output
1. **Data Layer Separation** - `EMOJI` as internal data source
1. **Policy-Aware by Default** - Terminal output always respects policy
1. **Backward Compatible** - No breaking changes
1. **Progressive Disclosure** - Simple API, advanced access available

______________________________________________________________________

## Implementation Specification

### Phase 1: Internal Refactoring

**Goal:** Make `icons.py` use `EMOJI` as its emoji data source.

**Current `icon_data.py`:**

```python
# icon_data.py (current - has hardcoded emojis)
ICON_REGISTRY = {
    "CHECK_MARK_BUTTON": IconMapping(emoji="✅", ascii="(OK)", color="green"),
    "CROSS_MARK": IconMapping(emoji="❌", ascii="(FAIL)", color="red"),
    ...
}
```

**Target `icon_data.py`:**

```python
# icon_data.py (refactored - uses EMOJI)
from styledconsole.emoji_registry import EMOJI

ICON_REGISTRY = {
    "CHECK_MARK_BUTTON": IconMapping(
        emoji=EMOJI.CHECK_MARK_BUTTON,  # From emoji package
        ascii="(OK)",
        color="green"
    ),
    "CROSS_MARK": IconMapping(
        emoji=EMOJI.CROSS_MARK,         # From emoji package
        ascii="(FAIL)",
        color="red"
    ),
    ...
}
```

**Benefits:**

- Single source of truth for emoji characters
- Automatic Unicode updates via emoji package
- No hardcoded emoji literals in icon_data.py

**Files to modify:**

| File                 | Change                                           |
| -------------------- | ------------------------------------------------ |
| `utils/icon_data.py` | Replace emoji literals with `EMOJI.*` references |
| `icons.py`           | No changes needed (uses IconMapping)             |

**Test cases:**

- [ ] All 224 icons resolve to valid emojis
- [ ] No emoji literals in `icon_data.py`
- [ ] Existing tests continue to pass

______________________________________________________________________

### Phase 2: Documentation Hierarchy

**Goal:** Update all documentation to recommend `icons` as primary API.

**USER_GUIDE.md changes:**

1. Move `icons` section before `EMOJI` section
1. Add "When to use which" guidance
1. Update all terminal output examples to use `icons`

**Recommended structure:**

```markdown
## Symbols and Icons

### icons (Recommended)

For terminal output, always use the `icons` module:

    from styledconsole import icons

    print(f"{icons.CHECK_MARK_BUTTON} Tests passed")   # ✅ or (OK)
    print(f"{icons.CROSS_MARK} Build failed")   # ❌ or (FAIL)

Icons automatically adapt to terminal capabilities.

### EMOJI (Advanced)

For raw emoji access (file output, non-terminal contexts):

    from styledconsole.emojis import EMOJI

    EMOJI.CHECK_MARK_BUTTON  # Always ✅
```

**DEVELOPER_GUIDE.md changes:**

1. Update architecture diagram to show hierarchy
1. Document internal data flow: `icons → EMOJI → emoji package`
1. Add contributor guidance

**Files to modify:**

| File                              | Change                       |
| --------------------------------- | ---------------------------- |
| `docs/USER_GUIDE.md`              | Restructure symbol sections  |
| `docs/DEVELOPER_GUIDE.md`         | Update architecture diagrams |
| `.github/copilot-instructions.md` | Update guidance              |

______________________________________________________________________

### Phase 3: Export Hierarchy

**Goal:** Demote `EMOJI` in top-level exports while maintaining availability.

**Current `__init__.py`:**

```python
# Both at same level
from styledconsole.emoji_registry import EMOJI, CuratedEmojis, E
from styledconsole.icons import icons, set_icon_mode, ...
```

**Target `__init__.py`:**

```python
# Primary API (icons)
from styledconsole.icons import (
    icons,
    Icon,
    IconMode,
    IconProvider,
    set_icon_mode,
    get_icon_mode,
    reset_icon_mode,
    convert_emoji_to_ascii,
)

# Secondary API (EMOJI - still available, less prominent)
from styledconsole.emoji_registry import EMOJI, CuratedEmojis, E
```

**`__all__` ordering:**

```python
__all__ = [
    # Core
    "Console",
    # Symbols (primary)
    "icons",
    "Icon",
    "set_icon_mode",
    "get_icon_mode",
    # ... other icons exports
    # Symbols (secondary/advanced)
    "EMOJI",
    "E",
    "CuratedEmojis",
    # ... rest
]
```

**Note:** No functional change - just reordering for documentation/autocomplete.

______________________________________________________________________

### Phase 4: Example Migration

**Goal:** Update all 38 examples to use `icons` for terminal output.

**Migration pattern:**

```python
# Before
from styledconsole import EMOJI
console.frame(f"{EMOJI.CHECK_MARK_BUTTON} Done")

# After
from styledconsole import icons
console.frame(f"{icons.CHECK_MARK_BUTTON} Done")
```

**Files to migrate:**

```text
examples/
├── demos/
│   ├── icon_provider_demo.py     # Already uses icons ✓
│   └── ...
├── gallery/
│   ├── emoji_showcase.py         # Uses EMOJI (keep for showcase)
│   └── ...
├── usecases/
│   ├── test_report.py            # Migrate to icons
│   └── ...
└── validation/
    └── ...
```

**Exception:** `emoji_showcase.py` should continue using `EMOJI` as it
specifically demonstrates the emoji system.

**Test cases:**

- [ ] All examples run without errors
- [ ] Terminal output respects RenderPolicy
- [ ] CI environments show ASCII fallbacks

______________________________________________________________________

### Phase 5: Migration Warnings (Optional)

**Goal:** Help users discover the preferred API.

**Implementation:**

```python
# In emojis.py or __init__.py
import warnings

def _emit_terminal_context_warning():
    """Emit warning when EMOJI is used in terminal context."""
    warnings.warn(
        "Consider using 'icons' instead of 'EMOJI' for terminal output. "
        "icons automatically handles ASCII fallback for CI/limited terminals. "
        "See USER_GUIDE.md for details.",
        UserWarning,
        stacklevel=3
    )
```

**Decision:** Mark as optional. May be too aggressive for v0.9.5.
Consider for v1.0.0 if adoption of `icons` is low.

______________________________________________________________________

## API Reference

### Primary API: icons

```python
from styledconsole import icons, set_icon_mode, get_icon_mode

# Access icons (policy-aware)
icons.CHECK_MARK_BUTTON      # ✅ or (OK) based on terminal
icons.CROSS_MARK             # ❌ or (FAIL)
icons.WARNING                # ⚠️ or (WARN)
icons.ROCKET                 # 🚀 or (>)

# Control rendering mode
set_icon_mode("auto")        # Default: detect terminal
set_icon_mode("emoji")       # Force emoji
set_icon_mode("ascii")       # Force ASCII

# Get Icon object for advanced use
icon = icons.get("CHECK_MARK_BUTTON")
icon.emoji                   # "✅"
icon.ascii                   # "(OK)"
icon.color                   # "green"
icon.as_emoji()              # Always "✅"
icon.as_ascii()              # "(OK)" with ANSI color
```

### Secondary API: EMOJI

```python
from styledconsole.emojis import EMOJI, CuratedEmojis

# Raw emoji access (for file output, non-terminal)
EMOJI.CHECK_MARK_BUTTON      # ✅ always
EMOJI.ROCKET                 # 🚀 always

# Search and discovery
EMOJI.search("rocket")       # [("ROCKET", "🚀"), ...]
EMOJI.get("ROCKET", "*")     # "🚀" or "*"
"ROCKET" in EMOJI            # True

# Curated categories
CuratedEmojis.STATUS         # ["CHECK_MARK_BUTTON", ...]
CuratedEmojis.DEV            # ["ROCKET", "FIRE", ...]
```

______________________________________________________________________

## Test Plan

### Unit Tests

| Test                          | Description                            | File                |
| ----------------------------- | -------------------------------------- | ------------------- |
| `test_icons_use_emoji_data`   | Verify icons use EMOJI for emoji chars | `test_icons.py`     |
| `test_no_hardcoded_emojis`    | Scan icon_data.py for emoji literals   | `test_icon_data.py` |
| `test_icon_emoji_consistency` | icons.X.emoji == EMOJI.X               | `test_icons.py`     |

### Integration Tests

| Test                      | Description                      | File                  |
| ------------------------- | -------------------------------- | --------------------- |
| `test_policy_propagation` | RenderPolicy affects icon output | `test_integration.py` |
| `test_ci_fallback`        | CI environment gets ASCII        | `test_integration.py` |

### Example Validation

```bash
# Run all examples in ASCII mode to verify fallbacks
TERM=dumb uv run python examples/run_examples.py --all --auto
```

______________________________________________________________________

## Migration Guide

### For Library Users

**If you use `EMOJI` for terminal output:**

```python
# Before (works but not optimal)
from styledconsole import EMOJI
print(f"{EMOJI.CHECK_MARK_BUTTON} Done")  # May break in CI

# After (recommended)
from styledconsole import icons
print(f"{icons.CHECK_MARK_BUTTON} Done")  # Works everywhere
```

**If you use `EMOJI` for non-terminal output (keep as-is):**

```python
# This is fine - EMOJI is correct for file output
from styledconsole import EMOJI
with open("report.txt", "w") as f:
    f.write(f"{EMOJI.CHECK_MARK_BUTTON} All tests passed\n")
```

### For Contributors

1. Use `icons` in all examples and presets
1. Use `EMOJI` only in `icon_data.py` as data source
1. Never hardcode emoji literals in library code

______________________________________________________________________

## Rollback Plan

If issues arise post-release:

1. **Revert `icon_data.py`** - Restore hardcoded emojis
1. **Documentation only** - Keep hierarchy in docs without code changes
1. **Full revert** - Git revert to v0.9.1

Risk is low due to:

- No breaking API changes
- All changes are additive/organizational
- Comprehensive test coverage

______________________________________________________________________

## Success Metrics

| Metric            | Target   | Measurement                           |
| ----------------- | -------- | ------------------------------------- |
| Example migration | 100%     | All examples use `icons` for terminal |
| Doc clarity       | Improved | USER_GUIDE recommends `icons` first   |
| No regressions    | 0        | All existing tests pass               |
| User adoption     | Tracked  | Monitor GitHub issues/questions       |

______________________________________________________________________

## Timeline

| Week | Phase     | Deliverable                          |
| ---- | --------- | ------------------------------------ |
| 1    | Phase 1   | `icon_data.py` refactored            |
| 2    | Phase 2   | Documentation updated                |
| 3    | Phase 3-4 | Exports reordered, examples migrated |
| 4    | Testing   | Full test pass, review               |
| 5    | Release   | v0.9.5 published                     |

______________________________________________________________________

## Appendix: Icon Coverage Analysis

### Icons with EMOJI equivalents (migrate)

All 224 icons in `icon_data.py` have CLDR names that exist in `EMOJI`.
Migration is straightforward:

```python
# Sample mapping verification
assert icons.CHECK_MARK_BUTTON.emoji == EMOJI.CHECK_MARK_BUTTON  # ✅
assert icons.ROCKET.emoji == EMOJI.ROCKET                        # 🚀
assert icons.FIRE.emoji == EMOJI.FIRE                            # 🔥
```

### Icons without EMOJI equivalents

None. All icon emojis are standard Unicode emojis covered by the `emoji` package.

______________________________________________________________________

## References

- [emoji PyPI package](https://pypi.org/project/emoji/)
- [Unicode CLDR](https://cldr.unicode.org/)
- `docs/archive/EMOJI_PACKAGE_ANALYSIS.md` - Original integration analysis
- `docs/PROJECT_STATUS.md` - Roadmap entry for v0.9.5
