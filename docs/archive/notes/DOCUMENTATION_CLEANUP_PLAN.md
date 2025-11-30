# Documentation Cleanup Plan

**Created:** November 30, 2025
**Status:** 🔄 In Progress
**Goal:** Reduce documentation sprawl, eliminate duplication, archive outdated content

______________________________________________________________________

## Execution Log

| Phase                              | Status  | Date   | Notes                                                   |
| ---------------------------------- | ------- | ------ | ------------------------------------------------------- |
| 1. Archive stray root docs         | ✅ Done | Nov 30 | code_review.md, improvement_proposals.md moved          |
| 2. Archive completed planned tasks | ✅ Done | Nov 30 | REFACTOR_001/002, ANSI_LAYOUT_WRAPPING, API_CONSISTENCY |
| 3. Archive project planning docs   | ✅ Done | Nov 30 | RICH_API_ANALYSIS.md, EXAMPLES_REDESIGN_PLAN.md         |
| 4. Archive old notes               | ✅ Done | Nov 30 | Files already in completed/                             |
| 5. Consolidate gradient docs       | ⏳ Skip | Nov 30 | Docs are complementary, not duplicates                  |
| 6. Archive COLOR_STANDARDIZATION   | ✅ Done | Nov 30 | Was changelog, not guide                                |
| 7. Move GALLERY_EXAMPLES_FIX       | ✅ Done | Nov 30 | Now in planned/                                         |
| 8. Review remaining planned        | 🔄 Next |        |                                                         |

______________________________________________________________________

## Codebase Validation Summary

### Actual API (from code inspection)

**Console class methods (console.py):**

- `frame()` - ✅ supports gradients via `start_color`/`end_color` and `border_gradient_start`/`border_gradient_end`
- `banner()` - ✅ uses `start_color`/`end_color` (NOT `style`/`colors`)
- `text()` - ✅ supports `color`, `bold`, `italic`, `underline`, `dim`
- `rule()` - ✅ supports `title`, `color`, `style`, `align`
- `newline()` - ✅ simple utility
- `clear()` - ✅ clears screen
- `export_html()` - ✅ requires `record=True`
- `export_text()` - ✅ requires `record=True`
- `print()` - ✅ passthrough to Rich

**Effects module (effects/__init__.py):**

- `gradient_frame()` - ✅ exists, uses Strategy pattern
- `diagonal_gradient_frame()` - ✅ exists
- `rainbow_frame()` - ✅ exists
- `rainbow_cycling_frame()` - ✅ exists

**Animation (animation.py):**

- `Animation.run()` - ✅ exists, basic but functional

**Version:** `__version__ = "0.4.0"` (per __init__.py)

### Documentation vs Reality Check

| Doc Claims               | Reality                    | Action                        |
| ------------------------ | -------------------------- | ----------------------------- |
| v0.5.0 features          | Code is v0.4.0             | Update docs to match          |
| `style="gradient"`       | Not in API                 | Docs are correct (deprecated) |
| Animation guide          | Animation exists but basic | Guide is aspirational         |
| REFACTOR-001/002         | TASKS.md says completed    | Move to completed/            |
| ANSI_LAYOUT_WRAPPING_BUG | Says "SOLVED"              | Move to completed/            |
| API_CONSISTENCY          | Phase 1-3 completed        | Move to completed/            |

______________________________________________________________________

## Current State Analysis

### Document Count by Location

| Location                | Files | Lines   | Status                |
| ----------------------- | ----- | ------- | --------------------- |
| `/doc/` (root)          | 4     | ~1,200  | Mixed - needs cleanup |
| `/doc/project/`         | 7     | ~6,200  | Some outdated         |
| `/doc/guides/`          | 7     | ~1,700  | Some overlap          |
| `/doc/reference/`       | 3     | ~980    | OK                    |
| `/doc/notes/`           | 5     | ~1,300  | Some should archive   |
| `/doc/tasks/`           | 2     | ~450    | Should archive        |
| `/doc/tasks/planned/`   | 7     | ~1,000+ | Need review           |
| `/doc/tasks/completed/` | 24    | ~5,000+ | OK (historical)       |
| **Total**               | ~60   | ~18,000 | **Needs reduction**   |

______________________________________________________________________

## Phase 1: Immediate Cleanup (Archive/Delete)

### Root `/doc/` - Files to Archive

| File                       | Lines | Action               | Reason                          |
| -------------------------- | ----- | -------------------- | ------------------------------- |
| `code_review.md`           | 101   | → `tasks/completed/` | One-time review, not living doc |
| `improvement_proposals.md` | 61    | → `tasks/completed/` | Proposals now in planned/       |

### `/doc/project/` - Files to Archive

| File                        | Lines | Action               | Reason                           |
| --------------------------- | ----- | -------------------- | -------------------------------- |
| `RICH_API_ANALYSIS.md`      | 936   | → `tasks/completed/` | Analysis complete, decision made |
| `EXAMPLES_REDESIGN_PLAN.md` | 387   | → `tasks/completed/` | Planning doc, examples done      |

### `/doc/notes/` - Files to Archive

| File                                  | Lines | Action               | Reason               |
| ------------------------------------- | ----- | -------------------- | -------------------- |
| `DOCUMENTATION_ORGANIZATION_OCT20.md` | 173   | → `tasks/completed/` | Historical org notes |
| `CHANGELOG_2025-10-18.md`             | 221   | → `tasks/completed/` | Old changelog        |
| `REFACTORING_2025-01-18.md`           | 166   | → `tasks/completed/` | Refactoring notes    |

### `/doc/tasks/` Root - Files to Move

| File                      | Lines | Action             | Reason            |
| ------------------------- | ----- | ------------------ | ----------------- |
| `GALLERY_EXAMPLES_FIX.md` | 451   | → `tasks/planned/` | Not completed yet |

______________________________________________________________________

## Phase 2: Consolidation (Merge Duplicates)

### Gradient Documentation (3 docs → 1)

**Current:**

- `guides/GRADIENT_EFFECTS.md` (77 lines) - User guide
- `guides/ANIMATED_GRADIENTS.md` (89 lines) - Animation guide
- `reference/GRADIENT_ENGINE.md` (86 lines) - Technical reference

**Problem:** Three docs about gradients, unclear which to read first.

**Action:** Merge into single `guides/GRADIENTS.md` with sections:

1. Basic Effects (from GRADIENT_EFFECTS)
1. Animation (from ANIMATED_GRADIENTS)
1. Technical Reference (from GRADIENT_ENGINE)

**Estimated result:** ~200 lines (from 252)

### Color Documentation (2 docs → 1)

**Current:**

- `guides/COLOR_STANDARDIZATION.md` (631 lines) - Example update log
- `reference/CSS4-COLORS.md` (516 lines) - Color reference

**Problem:** COLOR_STANDARDIZATION is mostly a changelog of one example update, not a guide.

**Action:**

- Archive `COLOR_STANDARDIZATION.md` to completed/ (it's a change log)
- Keep `CSS4-COLORS.md` as the single color reference

### API Documentation

**Current:**

- `notes/CONSOLE_API_IMPROVEMENTS.md` (476 lines) - Future ideas

**Problem:** This is a planning/ideas document in notes/, should be in tasks/planned/

**Action:** → Move to `tasks/planned/` or archive if ideas are stale

______________________________________________________________________

## Phase 3: Review Large Documents

### Keep (Active & Valuable)

| File                       | Lines | Status                    |
| -------------------------- | ----- | ------------------------- |
| `DOCUMENTATION_POLICY.md`  | 985   | ✅ Keep - Core policy     |
| `project/PLAN.md`          | 1,247 | ✅ Keep - Architecture    |
| `project/SPECIFICATION.md` | 1,253 | ✅ Keep - Requirements    |
| `project/TASKS.md`         | 149   | ✅ Keep - Active tracking |
| `project/ROADMAP.md`       | 313   | ✅ Keep - Future plans    |
| `project/TASKS_ARCHIVE.md` | 2,116 | ✅ Keep - History         |

### Review for Trimming

| File                           | Lines | Action                         |
| ------------------------------ | ----- | ------------------------------ |
| `guides/THICK_STYLE.md`        | 416   | Review - may be too detailed   |
| `reference/EMOJI_CONSTANTS.md` | 384   | Review - may overlap with code |

______________________________________________________________________

## Phase 4: Tasks/Planned Review

### Current Planned Tasks

| File                                   | Lines | Action                   |
| -------------------------------------- | ----- | ------------------------ |
| `README.md`                            | 200+  | ✅ Keep as index         |
| `REFACTOR_001_DUAL_RENDERING_PATHS.md` | ~150  | Review - still relevant? |
| `REFACTOR_002_COLOR_NORMALIZATION.md`  | ~100  | Review - still relevant? |
| `API_CONSISTENCY_V0.3.x.md`            | ?     | Review - v0.3.0 done     |
| `ANSI_LAYOUT_WRAPPING_BUG.md`          | ?     | Review - fixed?          |
| `BORDER_GRADIENT_FIX.md`               | ?     | Review - fixed?          |
| `TEST_REVISION_PLAN.md`                | ?     | Review - executed?       |

**Action:** Review each - archive if done, keep if still planned.

______________________________________________________________________

## Execution Order

### Step 1: Quick Wins (15 min)

- Archive root-level stray docs
- Move GALLERY_EXAMPLES_FIX to planned/

### Step 2: Archive Outdated Notes (10 min)

- Archive old changelogs and org docs

### Step 3: Consolidate Gradients (30 min)

- Create unified GRADIENTS.md
- Delete individual gradient docs

### Step 4: Clean Up Colors (10 min)

- Archive COLOR_STANDARDIZATION.md
- Keep CSS4-COLORS.md

### Step 5: Review Planned Tasks (20 min)

- Check each planned task for relevance
- Archive completed ones

______________________________________________________________________

## Expected Results

| Metric            | Before  | After   | Reduction  |
| ----------------- | ------- | ------- | ---------- |
| Active docs       | ~35     | ~15     | -57%       |
| Total lines       | ~18,000 | ~10,000 | -44%       |
| Duplicate content | High    | Low     | Eliminated |
| Stale docs        | Many    | Zero    | Cleaned    |

______________________________________________________________________

## Files to Keep (Final State)

### `/doc/`

- `README.md` - Index
- `DOCUMENTATION_POLICY.md` - Policy

### `/doc/project/`

- `SPECIFICATION.md` - What we build
- `PLAN.md` - How we build
- `ROADMAP.md` - Future versions
- `TASKS.md` - Current work
- `TASKS_ARCHIVE.md` - History

### `/doc/guides/`

- `EMOJI_SUPPORT.md` - Emoji guide ✅ Done
- `GRADIENTS.md` - All gradient info (NEW)
- `HTML_EXPORT.md` - Export guide
- `API_CONVENTIONS.md` - API patterns
- `THICK_STYLE.md` - Border details (review for trim)

### `/doc/reference/`

- `CSS4-COLORS.md` - Color palette
- `EMOJI_CONSTANTS.md` - EMOJI class

### `/doc/notes/`

- `VERIFICATION_REPORT.md` - Test verification
- `CONSOLE_API_IMPROVEMENTS.md` - API ideas (or move to planned/)

### `/doc/tasks/planned/`

- Active task plans only

### `/doc/tasks/completed/`

- All historical docs (no changes)
