# Documentation Management Policy

**Project:** StyledConsole
**Version:** 1.0
**Date:** October 19, 2025
**Status:** Active Policy

---

## 📋 Table of Contents

1. [Purpose](#purpose)
2. [Documentation Structure](#documentation-structure)
3. [Document Lifecycle](#document-lifecycle)
4. [Folder Organization](#folder-organization)
5. [Document Types](#document-types)
6. [Naming Conventions](#naming-conventions)
7. [Update Rules](#update-rules)
8. [Quality Standards](#quality-standards)
9. [Review Process](#review-process)

---

## Purpose

### Why This Policy Exists

**Problem:** Documentation can quickly become:
- ❌ Outdated (describes features no longer existing)
- ❌ Redundant (multiple docs covering same topic)
- ❌ Scattered (no clear organization)
- ❌ Inconsistent (different formats, styles, depths)

**Solution:** This policy ensures:
- ✅ Single Source of Truth (no duplicate docs)
- ✅ Living Documents (updated when code changes)
- ✅ Clear Organization (easy to find information)
- ✅ Consistent Quality (uniform format and depth)

### Guiding Principles

1. **DRY (Don't Repeat Yourself)**: One topic, one document
2. **Living Documentation**: Update docs when code changes
3. **Progressive Archival**: Move completed work to history
4. **Discoverable**: Clear naming and folder structure
5. **Minimal Maintenance**: Fewer, better docs over many mediocre ones

---

## Documentation Structure

### Folder Hierarchy

```
doc/
├── README.md                    # Documentation index (you are here)
├── DOCUMENTATION_POLICY.md      # This policy document
│
├── project/                     # Project-level documentation
│   ├── SPECIFICATION.md         # What we're building (requirements)
│   ├── PLAN.md                  # How we're building it (architecture)
│   ├── ROADMAP.md               # Future versions and features
│   └── TASKS.md                 # Active task tracking
│
├── guides/                      # User and developer guides
│   ├── EMOJI_GUIDELINES.md      # Emoji usage guide
│   ├── EMOJI-STRATEGY.md        # Emoji support strategy
│   ├── EMOJI_RENDERING.md       # Emoji technical details
│   ├── BORDER_GRADIENTS.md      # Gradient border guide
│   └── THICK_STYLE.md           # THICK border technical doc
│
├── reference/                   # Technical reference material
│   ├── CSS4-COLORS.md           # CSS4 color reference
│   └── GRADIENT_IMPLEMENTATION.md  # Gradient implementation details
│
├── tasks/                       # Task management
│   ├── completed/               # Historical: Completed work
│   └── planned/                 # Future: Planning documents (if needed)
│
├── notes/                       # Development notes and scratch work
│   ├── VERIFICATION_REPORT.md
│   └── CHANGELOG_2025-10-18.md
│
└── tips_and_tricks/             # Useful tips and workarounds
```

---

## Document Lifecycle

### States

Every document goes through these states:

```
┌─────────┐
│  Draft  │  Initial creation, work in progress
└────┬────┘
     │
     v
┌─────────┐
│ Active  │  Complete, used for reference, updated regularly
└────┬────┘
     │
     v
┌─────────┐
│Archived │  Historical, no longer updated but kept for reference
└─────────┘
```

### State Transitions

**Draft → Active:**
- Document is complete and reviewed
- Add "Status: Complete" or "Status: Active"
- Update README.md index

**Active → Archived:**
- Work described is completed
- Information no longer current
- Move to `tasks/completed/`
- Update README.md to reflect move

**Delete (Rare):**
- Document is duplicate
- Information is wrong and not salvageable
- Use `git rm` (preserves history)

---

## Folder Organization

### `/doc/project/` - Project Documentation

**Purpose:** High-level project documents that define what we're building

**What Goes Here:**
- ✅ SPECIFICATION.md - Requirements and user journeys
- ✅ PLAN.md - Architecture and technical design
- ✅ ROADMAP.md - Version planning (v0.2.0, v0.3.0, v1.0)
- ✅ TASKS.md - Active task tracking (M1-M6)

**Update Frequency:** Regular (as features are added/completed)

**Lifecycle:** Living documents (never archived)

---

### `/doc/guides/` - User & Developer Guides

**Purpose:** How-to documentation and strategies

**What Goes Here:**
- ✅ Feature guides (EMOJI_GUIDELINES.md)
- ✅ Strategy documents (EMOJI-STRATEGY.md)
- ✅ Technical deep-dives (EMOJI_RENDERING.md, THICK_STYLE.md)
- ✅ Implementation guides (BORDER_GRADIENTS.md)

**Update Frequency:** When features change or new patterns emerge

**Lifecycle:** Active, updated as needed

**Examples:**
```
guides/
├── EMOJI_GUIDELINES.md        # How to use emojis correctly
├── EMOJI-STRATEGY.md          # Why we have emoji tiers
├── EMOJI_RENDERING.md         # Technical: VS16 fix explanation
├── BORDER_GRADIENTS.md        # How to create gradient borders
└── THICK_STYLE.md             # Technical: THICK border details
```

---

### `/doc/reference/` - Technical Reference

**Purpose:** Reference material users look up (not tutorials)

**What Goes Here:**
- ✅ Color palettes (CSS4-COLORS.md)
- ✅ Algorithm details (GRADIENT_IMPLEMENTATION.md)
- ✅ API references (future: API_REFERENCE.md)
- ✅ Configuration options (future: CONFIGURATION.md)

**Update Frequency:** When APIs change or new features added

**Lifecycle:** Living documents, grow over time

---

### `/doc/tasks/completed/` - Historical Archive

**Purpose:** Completed work, decisions made, analysis done

**What Goes Here:**
- ✅ Refactoring summaries (REFACTORING_SUMMARY.md)
- ✅ Analysis reports (LEGACY_ANALYSIS_AND_IMPROVEMENTS.md)
- ✅ Testing reports (UX_TESTING_SUMMARY.md)
- ✅ Code reviews (GPT5-codebase-review.md)
- ✅ Status snapshots (STATUS_REPORT.md)
- ✅ Completed research (PHASE4_ANALYSIS.md)

**Update Frequency:** Never (historical record)

**Lifecycle:** Archive only

**Naming:** Keep original names (helps with git history)

---

### `/doc/tasks/planned/` - Future Planning (Rarely Used)

**Purpose:** Detailed planning docs for complex future features

**What Goes Here:**
- ✅ Major feature RFCs (Request for Comments)
- ✅ Research before implementation
- ✅ Large refactoring plans (before execution)

**Important:** Most future work should be in TASKS.md (M6 milestone), not separate docs

**Move to Completed:** When work starts or plan is executed

**Example:**
```
tasks/planned/
└── ANIMATION_FRAMEWORK_RFC.md  # Large feature needing detailed planning
```

---

### `/doc/notes/` - Development Notes

**Purpose:** Changelogs, verification reports, meeting notes

**What Goes Here:**
- ✅ Changelogs by date (CHANGELOG_2025-10-18.md)
- ✅ Verification reports (VERIFICATION_REPORT.md)
- ✅ Ad-hoc analysis (not formal docs)
- ✅ Debugging notes

**Update Frequency:** Ad-hoc (as needed)

**Lifecycle:** Keep as historical record

---

### `/doc/tips_and_tricks/` - Development Tips

**Purpose:** Useful workarounds, gotchas, best practices

**What Goes Here:**
- ✅ Terminal quirks and workarounds
- ✅ Testing tips
- ✅ Performance optimization tricks
- ✅ Common pitfalls and solutions

**Update Frequency:** When new tips discovered

**Lifecycle:** Living collection

---

## Document Types

### Type 1: Living Project Documents

**Examples:** TASKS.md, ROADMAP.md, PLAN.md, SPECIFICATION.md

**Characteristics:**
- Updated regularly as project evolves
- Single source of truth for their topic
- Never archived (always relevant)
- Located in `doc/project/`

**Update Rule:** ⚠️ MUST update when:
- Features are added/removed
- Tasks are completed
- Architecture changes
- Versions are released

---

### Type 2: Guide Documents

**Examples:** EMOJI_GUIDELINES.md, BORDER_GRADIENTS.md

**Characteristics:**
- Teach users how to use features
- Contain code examples
- Updated when feature APIs change
- Located in `doc/guides/`

**Update Rule:** ⚠️ MUST update when:
- Feature API changes
- New usage patterns emerge
- Breaking changes occur
- Best practices change

---

### Type 3: Reference Documents

**Examples:** CSS4-COLORS.md, GRADIENT_IMPLEMENTATION.md

**Characteristics:**
- Look-up material (not tutorials)
- Technical details and specs
- Growing documents (expand over time)
- Located in `doc/reference/`

**Update Rule:** ⚠️ MUST update when:
- New features added
- Algorithms change
- Performance characteristics change

---

### Type 4: Historical Documents

**Examples:** REFACTORING_SUMMARY.md, LEGACY_ANALYSIS_AND_IMPROVEMENTS.md

**Characteristics:**
- Describe completed work
- Archived for reference
- Never updated (frozen in time)
- Located in `doc/tasks/completed/`

**Update Rule:** ❌ NEVER update (historical record)

---

### Type 5: Notes & Changelogs

**Examples:** CHANGELOG_2025-10-18.md, VERIFICATION_REPORT.md

**Characteristics:**
- Date-stamped records
- Append-only (add new dates, don't edit old ones)
- Located in `doc/notes/`

**Update Rule:** ✅ Append new entries, don't edit old ones

---

## Naming Conventions

### File Naming Rules

**Format:** `TOPIC_NAME.md` (uppercase, underscores)

**Good Examples:**
- ✅ `EMOJI_GUIDELINES.md` - Clear, descriptive
- ✅ `BORDER_GRADIENTS.md` - Topic obvious
- ✅ `CSS4-COLORS.md` - Standard name (CSS4 uses hyphen)
- ✅ `THICK_STYLE.md` - Specific feature name

**Bad Examples:**
- ❌ `guide.md` - Too generic
- ❌ `emoji-guide-for-developers.md` - Too verbose
- ❌ `EmojiGuide.md` - Mixed case
- ❌ `emoji.md` - Too vague (which aspect of emoji?)

### Document Titles

**Format:** `# Document Title` (first line of file)

**Rules:**
- Match filename (EMOJI_GUIDELINES.md → "# Emoji Guidelines")
- Use Title Case
- Be descriptive but concise

---

## Update Rules

### When Code Changes, Update Docs

**Trigger:** Pull request or commit changes code

**Check:**
1. Does a guide cover this feature? → Update guide
2. Is this in SPECIFICATION.md? → Update specification
3. Are there code examples in docs? → Update examples
4. Is this a breaking change? → Update all affected docs

**Process:**
1. Identify affected documents
2. Update them in the same PR/commit
3. Run markdown linter
4. Update "Last Updated" date if document has one

---

### When Tasks Complete, Update TASKS.md

**Trigger:** Task is finished

**Actions:**
1. Mark task with ✅ in TASKS.md
2. Update completion date
3. Update milestone progress counter
4. If task had analysis doc → move to `tasks/completed/`

**Example:**
```markdown
### T-020: Icon Provider System ⏳
**Priority:** Medium
**Milestone:** M6 (v0.2.0)
**Status:** Planned

↓ becomes ↓

### T-020: Icon Provider System ✅
**Priority:** Medium
**Milestone:** M6 (v0.2.0)
**Status:** ✅ Completed (Oct 25, 2025)
```

---

### When Analysis Completes, Archive It

**Trigger:** Analysis leads to tasks or decision

**Actions:**
1. Create tasks in TASKS.md (if recommendations exist)
2. Move analysis doc to `tasks/completed/`
3. Update README.md index
4. Reference analysis from TASKS.md if needed

**Example:**
```bash
# Analysis complete, tasks created in TASKS.md
git mv doc/SOME_ANALYSIS.md doc/tasks/completed/

# Update TASKS.md to reference it
echo "See doc/tasks/completed/SOME_ANALYSIS.md for details" >> TASKS.md
```

---

### Prevent Document Drift

**Problem:** Code and docs get out of sync

**Solution:** Documentation Checklist

**Before Merging PR:**
- [ ] Code examples in docs still work?
- [ ] API signatures still match docs?
- [ ] Breaking changes documented?
- [ ] TASKS.md updated if task completed?
- [ ] README.md index updated if doc added/moved?

---

## Quality Standards

### Every Document MUST Have

1. **Title** (first line, H1)
   ```markdown
   # Emoji Guidelines
   ```

2. **Purpose** (what is this doc for?)
   ```markdown
   **Purpose:** Guide developers on correct emoji usage in StyledConsole
   ```

3. **Audience** (who should read this?)
   ```markdown
   **Audience:** Developers using emoji features
   ```

4. **Status** (is this complete or draft?)
   ```markdown
   **Status:** Complete (M1) / Active / Draft / Archived
   ```

5. **Table of Contents** (if > 200 lines)
   ```markdown
   ## Table of Contents
   - [Section 1](#section-1)
   - [Section 2](#section-2)
   ```

### Code Examples MUST

- ✅ Be runnable (test them!)
- ✅ Show imports
- ✅ Include output or expected behavior
- ✅ Use real project APIs (not pseudocode)

**Example:**
```python
from styledconsole import status_frame

# Create a status frame with emoji
status_frame(
    title="Server Status 🖥️",
    status="success",
    content=["✅ Database connected", "✅ API responding"]
)
```

### Markdown MUST

- ✅ Pass markdown linter (no MD022, MD032 errors)
- ✅ Use consistent heading levels (H2 → H3 → H4, no skipping)
- ✅ Have blank lines around headings and lists
- ✅ Use fenced code blocks with language specified

---

## Review Process

### When Creating New Document

**Before Creating:**
1. **Check:** Does a document for this topic already exist?
2. **Consider:** Should this be added to existing doc instead?
3. **Ask:** Will this be maintained or become stale?

**If Creating:**
1. Choose correct folder (`project/`, `guides/`, `reference/`)
2. Follow naming conventions
3. Include required sections (Title, Purpose, Audience, Status)
4. Add to README.md index
5. Run markdown linter

---

### When Updating Existing Document

**Process:**
1. Read current document first
2. Identify what's outdated
3. Update content
4. Test code examples
5. Update "Last Updated" date (if document has one)
6. Commit with descriptive message

**Commit Message Format:**
```
docs: Update EMOJI_GUIDELINES with Tier 2 examples

- Added skin tone modifier examples
- Updated supported emoji list
- Fixed broken code example in section 3
```

---

### When Archiving Document

**Checklist:**
1. ✅ Work described is actually completed?
2. ✅ Information extracted to active docs if needed?
3. ✅ Tasks created in TASKS.md for recommendations?
4. ✅ Document moved to `tasks/completed/`?
5. ✅ README.md updated?

**Command:**
```bash
git mv doc/DOCUMENT.md doc/tasks/completed/
git commit -m "docs: Archive DOCUMENT.md (work completed)"
```

---

## Special Cases

### When Refactoring Code

**Before Refactoring:**
1. Check if PLAN.md describes current architecture
2. Update PLAN.md with new architecture
3. Create refactoring plan doc if major (in `tasks/planned/`)

**During Refactoring:**
1. Update code examples in guides as you go
2. Update SPECIFICATION.md if behavior changes

**After Refactoring:**
1. Create refactoring summary (what changed, why)
2. Archive summary to `tasks/completed/`
3. Update affected guides with new examples

---

### When Adding New Feature

**Planning Phase:**
1. Update ROADMAP.md (which version?)
2. Add task to TASKS.md
3. Consider: Does this need a guide? (Y/N)

**Implementation Phase:**
1. Update PLAN.md if architecture changes
2. Update SPECIFICATION.md if new use cases

**Completion Phase:**
1. Mark task complete in TASKS.md ✅
2. Create guide if needed (in `guides/`)
3. Update README.md to reference guide
4. Add examples to existing docs if relevant

---

### When Deprecating Feature

**Process:**
1. Update ROADMAP.md (which version removes it?)
2. Update guide with deprecation warning
3. Update SPECIFICATION.md
4. Add migration guide if replacement exists

**Guide Deprecation Warning:**
```markdown
> ⚠️ **DEPRECATED:** This feature will be removed in v0.5.0
> Use `new_feature()` instead. See [Migration Guide](#migration).
```

---

## Summary: Quick Reference

### Document Placement Cheat Sheet

| Document Type | Location | Lifecycle | Update Frequency |
|--------------|----------|-----------|------------------|
| Requirements | `project/SPECIFICATION.md` | Living | When features change |
| Architecture | `project/PLAN.md` | Living | When design changes |
| Roadmap | `project/ROADMAP.md` | Living | When planning versions |
| Tasks | `project/TASKS.md` | Living | Daily/weekly |
| User Guides | `guides/*.md` | Active | When APIs change |
| Technical Guides | `guides/*.md` | Active | When implementations change |
| Reference | `reference/*.md` | Active | When features added |
| Completed Work | `tasks/completed/*.md` | Archived | Never |
| Planning (rare) | `tasks/planned/*.md` | Temporary | Until work starts |
| Notes | `notes/*.md` | Historical | Append-only |
| Tips | `tips_and_tricks/*.md` | Collection | Ad-hoc |

---

### When in Doubt

**Ask These Questions:**
1. Does this document already exist? (Check README.md index)
2. Should this be part of existing doc? (Prefer expanding over creating)
3. Will this be updated or become stale? (If stale → don't create)
4. Is this temporary or permanent? (Temporary → `notes/`, Permanent → proper location)

**Golden Rule:** When uncertain, ask in PR or create issue before creating new document.

---

## Enforcement

### Responsibility

**Everyone who commits:**
- Checks if docs need updating
- Updates docs in same PR as code
- Follows naming conventions
- Runs markdown linter

**Maintainers additionally:**
- Review doc changes in PRs
- Archive completed work
- Refactor docs when structure improves
- Enforce this policy

### Tools

**Markdown Linter:**
```bash
# Run before committing
pre-commit run --all-files
```

**Documentation Review:**
```bash
# Check for common issues
grep -r "TODO" doc/            # Unfinished sections
grep -r "FIXME" doc/           # Known problems
grep -r "Status: Draft" doc/   # Incomplete docs
```

---

## Policy Updates

**This policy itself is a living document.**

**Update when:**
- Documentation structure changes
- New document types emerge
- Better practices discovered

**Version History:**
- v1.0 (Oct 19, 2025): Initial policy created

---

**Questions or Suggestions?**

Open an issue with `[docs]` prefix to discuss documentation policy changes.
