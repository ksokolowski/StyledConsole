# Planned Tasks

**Updated:** November 30, 2025
**Status:** Active tasks awaiting implementation

______________________________________________________________________

## Overview

This directory contains tasks that are planned but not yet completed.
Completed tasks are moved to `completed/`.

______________________________________________________________________

## Current Active Tasks

### 🔴 BORDER_GRADIENT_FIX.md

**Status:** Blocked - Analysis
**Priority:** CRITICAL (Blocking User)
**Target:** v0.3.1 (Hotfix)

Border gradients causing rendering bugs when combined with content that has Rich Text markup. Post-processing approach interferes with existing ANSI codes.

______________________________________________________________________

### 🟡 GALLERY_EXAMPLES_FIX.md

**Status:** Blocked - Requires systematic fixing
**Priority:** High
**Target:** v0.4.1

5 gallery examples have API violations:

- Wrong banner API (`style=` instead of `start_color=`/`end_color=`)
- Manual frame drawing (forbidden)
- Raw emoji usage (should use EMOJI constants)

______________________________________________________________________

### 🟡 TEST_REVISION_PLAN.md

**Status:** Planning
**Priority:** Medium
**Target:** v0.4.0+

Post-refactor test cleanup:

- Private method tests from old FrameRenderer
- Banner integration width tests
- Debug logging message updates

______________________________________________________________________

## Completed Refactors (Archived)

The following major refactors have been completed and moved to `completed/`:

| Task                                | Status       | Notes                         |
| ----------------------------------- | ------------ | ----------------------------- |
| REFACTOR_001_DUAL_RENDERING_PATHS   | ✅ Completed | Adapter pattern implemented   |
| REFACTOR_002_COLOR_NORMALIZATION    | ✅ Completed | Color normalization extracted |
| REFACTOR_003_GRADIENT_CONSOLIDATION | ✅ Completed | Strategy pattern implemented  |
| API_CONSISTENCY_V0.3.x              | ✅ Completed | Phases 1-3 done               |
| ANSI_LAYOUT_WRAPPING_BUG            | ✅ Completed | SOLVED                        |

______________________________________________________________________

## Guidelines

For each planned task:

1. **Status** must be current (not-started, in-progress, blocked)
1. **Priority** determines order (CRITICAL > High > Medium)
1. **Target** version for completion
1. Archive to `completed/` when done
