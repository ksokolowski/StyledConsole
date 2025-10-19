# Documentation Reorganization Plan

**Date:** October 19, 2025
**Purpose:** Organize documentation by status (completed vs planned)

---

## Documents to Move to tasks/completed/

### Completed Work & Analysis (Actions Finished)

1. **REFACTORING_SUMMARY.md** - Summary of completed Phase 1-4 refactoring
2. **PHASE4_ANALYSIS.md** - Analysis that led to completing Phase 4
3. **PHASE4_RESEARCH_PLAN.md** - Research completed, Phase 4 done
4. **REFACTORING_PLAN_v2.md** - Refactoring plan (executed and completed)
5. **EARLY_IMPROVEMENT_PLAN.md** - Early improvements (completed)
6. **GPT5-codebase-review.md** - Review completed
7. **Gemini_codebase-review_v2.md** - Review completed
8. **UX_TESTING_SUMMARY.md** - Testing completed Oct 19
9. **UX_VALIDATION_REPORT.md** - Validation completed (100% passed)
10. **VARIATION_SELECTOR_ISSUE.md** - Fixed in prototype, documented
11. **STATUS_REPORT.md** - Historical status (snapshot in time)

### Analysis Documents (Reference, not tasks)

12. **COLOR_SYSTEM_COMPARISON.md** - Analysis completed (v0.1.0 is better)
13. **GRADIENT_RAINBOW_COMPARISON.md** - Analysis completed (recommends T-027)
14. **LEGACY_ANALYSIS_AND_IMPROVEMENTS.md** - Analysis completed (recommends T-020 through T-026)

---

## Documents to Move to tasks/planned/

### Future Work & Recommendations

*None directly* - Future tasks are properly tracked in TASKS.md (M6 milestone: T-020 through T-027)

The analysis documents above (COLOR_SYSTEM_COMPARISON, GRADIENT_RAINBOW_COMPARISON, LEGACY_ANALYSIS_AND_IMPROVEMENTS) contain recommendations that have been converted to tasks in TASKS.md.

---

## Documents to KEEP in doc/ (Root Level)

### Active Reference Documentation

1. **TASKS.md** - Active task tracking (M1-M6, includes future tasks)
2. **PLAN.md** - Project architecture plan (living document)
3. **ROADMAP.md** - Product roadmap (v0.1.0 through v1.0)
4. **SPECIFICATION.md** - Technical specifications (reference)
5. **README.md** - Documentation index

### Guidelines & Standards (Evergreen)

6. **EMOJI_GUIDELINES.md** - Tier 1 emoji usage guide
7. **EMOJI-STRATEGY.md** - Emoji support strategy
8. **EMOJI_RENDERING.md** - Technical emoji rendering details
9. **CSS4-COLORS.md** - CSS4 color reference
10. **THICK_STYLE.md** - Border style documentation
11. **BORDER_GRADIENTS.md** - Gradient border guide
12. **GRADIENT_IMPLEMENTATION.md** - Gradient technical details

---

## Action Items

1. Create tasks/completed/ if not exists ✓ (already exists)
2. Create tasks/planned/ if not exists ✓ (already exists)
3. Move 14 completed documents to tasks/completed/
4. Update README.md with new structure
5. Keep 12 active/reference docs in doc/

---

## Rationale

**Completed Documents:**
- Actions already taken (refactoring done, reviews done, testing done)
- Historical snapshots (status reports)
- Analysis that led to completed work
- Archived for reference but not actionable

**Active Documents:**
- Living documentation (TASKS, PLAN, ROADMAP)
- Reference guides users consult regularly (EMOJI_GUIDELINES, color guides)
- Technical specifications still relevant

**Result:** Cleaner doc/ folder focused on active/useful docs, with completed work properly archived.
