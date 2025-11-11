# Documentation Management Policy

**Project:** StyledConsole
**Version:** 1.0
**Date:** October 19, 2025
**Status:** Active Policy

______________________________________________________________________

## 📋 Table of Contents

1. [Purpose](#purpose)
1. [Learning from Past Failures](#learning-from-past-failures)
1. [Documentation Structure](#documentation-structure)
1. [Document Lifecycle](#document-lifecycle)
1. [Folder Organization](#folder-organization)
1. [Document Types](#document-types)
1. [Naming Conventions](#naming-conventions)
1. [Update Rules](#update-rules)
1. [Quality Standards](#quality-standards)
1. [Review Process](#review-process)

______________________________________________________________________

## Purpose

### Why This Policy Exists

**Problem:** Documentation can quickly become:

- ❌ Outdated (describes features no longer existing)
- ❌ Redundant (multiple docs covering same topic)
- ❌ Scattered (no clear organization)
- ❌ Inconsistent (different formats, styles, depths)
- ❌ **Over-engineered** (documenting everything = documenting nothing)**Solution:** This policy ensures:
- ✅ Single Source of Truth (no duplicate docs)
- ✅ Living Documents (updated when code changes)
- ✅ Clear Organization (easy to find information)
- ✅ Consistent Quality (uniform format and depth)
- ✅ **Focus on What Matters** (document decisions, not every thought)

### Guiding Principles

1. **Less is More**: Document what users need, not what we can write
1. **DRY (Don't Repeat Yourself)**: One topic, one document
1. **Living Documentation**: Update docs when code changes
1. **Progressive Archival**: Move completed work to history
1. **Discoverable**: Clear naming and folder structure
1. **Anti-Over-Engineering**: If it doesn't help users/contributors, don't document it

______________________________________________________________________

## Learning from Past Failures

### Why This Project Has Strict Documentation Rules

**Context:** This is a **rewrite** of a previous StyledConsole library that failed due to over-engineering.

**Legacy Project Analysis:**

- **111 files, 19,022 lines of code** (vs current 21 files, 4,696 lines)
- **Over-documented, under-focused** - lots of analysis, little clarity
- **Documentation drift** - docs described features that didn't exist or were broken
- **Complexity spiral** - more docs → more maintenance → more complexity → more docs
- **Lost focus** - spent time documenting hypotheticals instead of building core features

### Critical Lessons Applied

#### 1. **Code Simplicity = Documentation Simplicity**

**Legacy mistake:**

- 248-line `frame_alignment.py` to fix emoji rendering
- Required extensive documentation explaining the workaround
- Documentation became maintenance burden

**Current approach:**

- Tier 1 emojis only (no alignment hacks needed)
- Simple = less to document = less to maintain
- **Document the design decision, not the workaround**

#### 2. **Not Everything Deserves a Document**

**❌ Don't document:**

- Work-in-progress thoughts (use notes/ if needed, then delete)
- Every analysis step (document the conclusion only)
- Temporary decisions (wait until permanent)
- "Nice to have" features not yet planned
- Process minutiae (how we organized files = notes/, not doc/)

**✅ Do document:**

- Architecture decisions (PLAN.md)
- User-facing features (guides/)
- API references (reference/)
- Active tasks (TASKS.md)
- Design rationale for non-obvious choices

#### 3. **Over-Engineering Starts with Documentation**

**Warning signs:**

- Creating documents about documents (meta-documentation)
- Documenting hypothetical features
- Writing summaries of summaries
- Excessive process documentation
- Documentation taking more time than coding

**Prevention:**

- Ask: "Will this help a user or contributor right now?"
- If NO → Don't document it
- If MAYBE → Put in notes/ and revisit later
- If YES → Document concisely in appropriate folder

#### 4. **Legacy Had 18 Colors, Current Has 148 - But Less Docs**

**Counterintuitive but true:**

- More features ≠ more documentation
- Better design = simpler documentation
- CSS4 standard colors = one reference doc (CSS4-COLORS.md)
- Legacy custom colors = complex explanations needed

**Lesson:** Good design reduces documentation burden

### The Iron Rules (To Prevent Repeat Failure)

#### Rule 1: Document Decisions, Not Process

**❌ Bad:**

```markdown
# How We Decided On Emoji Strategy

First we analyzed legacy code...
Then we discussed Tier 1 vs Tier 2...
Then we created comparison matrix...
Then we decided...
```

**✅ Good:**

```markdown
# Emoji Strategy

**Decision:** Support Tier 1 emojis only (basic pictographs).

**Rationale:** Legacy project had 248-line fix for complex emojis.
Supporting only Tier 1 = zero alignment issues = simpler codebase.

**See:** EMOJI-STRATEGY.md for tier definitions.
```

#### Rule 2: Archive Aggressively

**The moment work completes:**

1. Extract decision → update active docs
1. Move analysis → tasks/completed/
1. Delete if it was just exploration (notes/ is not a dumping ground)

**Don't let completed work clutter active docs.**

#### Rule 3: Quality Over Quantity

**One great guide > ten mediocre docs**

- EMOJI_GUIDELINES.md (complete usage guide)
- Better than: emoji-basic.md, emoji-advanced.md, emoji-tips.md, emoji-faq.md, emoji-troubleshooting.md

#### Rule 4: Code is Documentation

**If you need extensive docs to explain code, the code is too complex.**

- Legacy: 248 lines + docs explaining why
- Current: 0 lines (avoided the problem)

**Write clear code first, then minimal docs.**

#### Rule 5: User Focus

**Documentation exists for users, not for us.**

Ask before documenting:

- "Does this help someone use the library?" → guides/
- "Does this help someone contribute?" → project/
- "Does this help someone understand an API?" → reference/
- "Is this just for our own reference?" → notes/ (then delete when done)

### What We Avoid

**Based on legacy project failure:**

1. **❌ Analysis paralysis** - Don't document 10 approaches, document the chosen one
1. **❌ Premature documentation** - Don't document v2.0 features in v0.1.0
1. **❌ Process over-documentation** - Don't document how we organize docs (ironic, but this section is the exception)
1. **❌ Hypothetical features** - If it's not in ROADMAP.md, don't document it
1. **❌ Architecture astronomy** - Don't document every possible design pattern
1. **❌ Documentation for documentation's sake** - Every doc must serve users or contributors

### Success Metrics

**How we know we're doing it right:**

- ✅ **Can find information in \< 30 seconds** (README.md index works)
- ✅ **Code/docs ratio stays healthy** (more code than docs is good)
- ✅ **No duplicate information** (one source of truth)
- ✅ **New contributors understand quickly** (clear guides/)
- ✅ **Documentation doesn't slow development** (update in same PR as code)
- ✅ **No "documenting the documentation"** (this policy is the exception)

### When In Doubt

**Apply the "Legacy Test":**

Ask: "Would this document have saved the legacy project from over-engineering?"

- If NO → Don't create it
- If YES → Document the decision that prevents the mistake

**Remember:**

- Legacy failed because it was too complex
- Complexity started with over-documentation
- This policy exists to prevent history from repeating

______________________________________________________________________

**Bottom line:** We document to help users and contributors, not to create more work for ourselves. The legacy project drowned in its own complexity. We won't make the same mistake.

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

### `/doc/reference/` - Technical Reference

**Purpose:** Reference material users look up (not tutorials)

**What Goes Here:**

- ✅ Color palettes (CSS4-COLORS.md)
- ✅ Algorithm details (GRADIENT_IMPLEMENTATION.md)
- ✅ API references (future: API_REFERENCE.md)
- ✅ Configuration options (future: CONFIGURATION.md)

**Update Frequency:** When APIs change or new features added

**Lifecycle:** Living documents, grow over time

______________________________________________________________________

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

______________________________________________________________________

### `/doc/tasks/planned/` - Future Planning (Rarely Used)

**Purpose:** Detailed technical planning for complex future features

**What Goes Here:**

- ✅ Major feature RFCs (Request for Comments)
- ✅ Detailed implementation plans for complex features
- ✅ Research and technical analysis before implementation
- ✅ Architecture proposals for large changes

**When to Use:**

- Feature is confirmed feasible (in ROADMAP.md)
- Implementation requires detailed technical planning
- Complexity justifies separate document (vs simple task in TASKS.md)

**Important:** Most future work should be tracked in TASKS.md only, not separate docs

**Workflow:**

1. **Create:** Feature confirmed feasible → Create detailed plan in `tasks/planned/`
1. **Track:** Reference from TASKS.md: "See tasks/planned/FEATURE_NAME.md for details"
1. **Implement:** Work in progress → Keep plan in tasks/planned/
1. **Complete:** Implementation done and tested → Move to `tasks/completed/`
1. **Update:** Mark task complete in TASKS.md ✅

**Example:**

```text
tasks/planned/
├── ANIMATION_FRAMEWORK.md      # Detailed animation system design
└── ICON_PROVIDER_SYSTEM.md     # Icon provider implementation plan

# Referenced from TASKS.md:
### T-020: Icon Provider System ⏳
**Status:** In Progress
**Details:** See tasks/planned/ICON_PROVIDER_SYSTEM.md

# After completion:
### T-020: Icon Provider System ✅
**Status:** ✅ Completed (Nov 5, 2025)
**Implementation:** See tasks/completed/ICON_PROVIDER_SYSTEM.md
```

**Benefits:**

- ✅ TASKS.md stays high-level and scannable
- ✅ Technical details don't clutter project docs
- ✅ Completed plans preserved for reference
- ✅ Clear workflow: planned → in progress → completed

______________________________________________________________________

### `/doc/notes/` - Development Notes

**Purpose:** Changelogs, verification reports, meeting notes

**What Goes Here:**

- ✅ Changelogs by date (CHANGELOG_2025-10-18.md)
- ✅ Verification reports (VERIFICATION_REPORT.md)
- ✅ Ad-hoc analysis (not formal docs)
- ✅ Debugging notes

**Update Frequency:** Ad-hoc (as needed)

**Lifecycle:** Keep as historical record

______________________________________________________________________

### `/doc/tips_and_tricks/` - Development Tips

**Purpose:** Useful workarounds, gotchas, best practices

**What Goes Here:**

- ✅ Terminal quirks and workarounds
- ✅ Testing tips
- ✅ Performance optimization tricks
- ✅ Common pitfalls and solutions

**Update Frequency:** When new tips discovered

**Lifecycle:** Living collection

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

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

______________________________________________________________________

### Type 4: Historical Documents

**Examples:** REFACTORING_SUMMARY.md, LEGACY_ANALYSIS_AND_IMPROVEMENTS.md

**Characteristics:**

- Describe completed work
- Archived for reference
- Never updated (frozen in time)
- Located in `doc/tasks/completed/`

**Update Rule:** ❌ NEVER update (historical record)

______________________________________________________________________

### Type 5: Notes & Changelogs

**Examples:** CHANGELOG_2025-10-18.md, VERIFICATION_REPORT.md

**Characteristics:**

- Date-stamped records
- Append-only (add new dates, don't edit old ones)
- Located in `doc/notes/`

**Update Rule:** ✅ Append new entries, don't edit old ones

______________________________________________________________________

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

______________________________________________________________________

## Update Rules

### When Code Changes, Update Docs

**Trigger:** Pull request or commit changes code

**Check:**

1. Does a guide cover this feature? → Update guide
1. Is this in SPECIFICATION.md? → Update specification
1. Are there code examples in docs? → Update examples
1. Is this a breaking change? → Update all affected docs

**Process:**

1. Identify affected documents
1. Update them in the same PR/commit
1. Run markdown linter
1. Update "Last Updated" date if document has one

______________________________________________________________________

### When Tasks Complete, Update TASKS.md

**Trigger:** Task is finished

**Actions:**

1. Mark task with ✅ in TASKS.md
1. Update completion date
1. Update milestone progress counter
1. If task had analysis doc → move to `tasks/completed/`

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

______________________________________________________________________

### When Analysis Completes, Archive It

**Trigger:** Analysis leads to tasks or decision

**Actions:**

1. Create tasks in TASKS.md (if recommendations exist)
1. Move analysis doc to `tasks/completed/`
1. Update README.md index
1. Reference analysis from TASKS.md if needed

**Example:**

```bash
# Analysis complete, tasks created in TASKS.md
git mv doc/SOME_ANALYSIS.md doc/tasks/completed/

# Update TASKS.md to reference it
echo "See doc/tasks/completed/SOME_ANALYSIS.md for details" >> TASKS.md
```

______________________________________________________________________

### Prevent Document Drift

**Problem:** Code and docs get out of sync

**Solution:** Documentation Checklist

**Before Merging PR:**

- [ ] Code examples in docs still work?
- [ ] API signatures still match docs?
- [ ] Breaking changes documented?
- [ ] TASKS.md updated if task completed?
- [ ] README.md index updated if doc added/moved?

______________________________________________________________________

## Quality Standards

### Every Document MUST Have

1. **Title** (first line, H1)

   ```markdown
   # Emoji Guidelines
   ```

1. **Purpose** (what is this doc for?)

   ```markdown
   **Purpose:** Guide developers on correct emoji usage in StyledConsole
   ```

1. **Audience** (who should read this?)

   ```markdown
   **Audience:** Developers using emoji features
   ```

1. **Status** (is this complete or draft?)

   ```markdown
   **Status:** Complete (M1) / Active / Draft / Archived
   ```

1. **Table of Contents** (if > 200 lines)

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

______________________________________________________________________

## Review Process

### When Creating New Document

**Before Creating:**

1. **Check:** Does a document for this topic already exist?
1. **Consider:** Should this be added to existing doc instead?
1. **Ask:** Will this be maintained or become stale?

**If Creating:**

1. Choose correct folder (`project/`, `guides/`, `reference/`)
1. Follow naming conventions
1. Include required sections (Title, Purpose, Audience, Status)
1. Add to README.md index
1. Run markdown linter

______________________________________________________________________

### When Updating Existing Document

**Process:**

1. Read current document first
1. Identify what's outdated
1. Update content
1. Test code examples
1. Update "Last Updated" date (if document has one)
1. Commit with descriptive message

**Commit Message Format:**

```
docs: Update EMOJI_GUIDELINES with Tier 2 examples

- Added skin tone modifier examples
- Updated supported emoji list
- Fixed broken code example in section 3
```

______________________________________________________________________

### When Archiving Document

**Checklist:**

1. ✅ Work described is actually completed?
1. ✅ Information extracted to active docs if needed?
1. ✅ Tasks created in TASKS.md for recommendations?
1. ✅ Document moved to `tasks/completed/`?
1. ✅ README.md updated?

**Command:**

```bash
git mv doc/DOCUMENT.md doc/tasks/completed/
git commit -m "docs: Archive DOCUMENT.md (work completed)"
```

______________________________________________________________________

## Special Cases

### When Refactoring Code

**Before Refactoring:**

1. Check if PLAN.md describes current architecture
1. Update PLAN.md with new architecture
1. Create refactoring plan doc if major (in `tasks/planned/`)

**During Refactoring:**

1. Update code examples in guides as you go
1. Update SPECIFICATION.md if behavior changes

**After Refactoring:**

1. Create refactoring summary (what changed, why)
1. Archive summary to `tasks/completed/`
1. Update affected guides with new examples

______________________________________________________________________

### When Adding New Feature

**Planning Phase:**

1. Update ROADMAP.md (which version?)
1. Add task to TASKS.md
1. Consider: Does this need a guide? (Y/N)

**Implementation Phase:**

1. Update PLAN.md if architecture changes
1. Update SPECIFICATION.md if new use cases

**Completion Phase:**

1. Mark task complete in TASKS.md ✅
1. Create guide if needed (in `guides/`)
1. Update README.md to reference guide
1. Add examples to existing docs if relevant

______________________________________________________________________

### When Deprecating Feature

**Process:**

1. Update ROADMAP.md (which version removes it?)
1. Update guide with deprecation warning
1. Update SPECIFICATION.md
1. Add migration guide if replacement exists

**Guide Deprecation Warning:**

```markdown
> ⚠️ **DEPRECATED:** This feature will be removed in v0.5.0
> Use `new_feature()` instead. See [Migration Guide](#migration).
```

______________________________________________________________________

## Summary: Quick Reference

### Document Placement Cheat Sheet

| Document Type    | Location                   | Lifecycle  | Update Frequency            |
| ---------------- | -------------------------- | ---------- | --------------------------- |
| Requirements     | `project/SPECIFICATION.md` | Living     | When features change        |
| Architecture     | `project/PLAN.md`          | Living     | When design changes         |
| Roadmap          | `project/ROADMAP.md`       | Living     | When planning versions      |
| Tasks            | `project/TASKS.md`         | Living     | Daily/weekly                |
| User Guides      | `guides/*.md`              | Active     | When APIs change            |
| Technical Guides | `guides/*.md`              | Active     | When implementations change |
| Reference        | `reference/*.md`           | Active     | When features added         |
| Completed Work   | `tasks/completed/*.md`     | Archived   | Never                       |
| Planning (rare)  | `tasks/planned/*.md`       | Temporary  | Until work starts           |
| Notes            | `notes/*.md`               | Historical | Append-only                 |
| Tips             | `tips_and_tricks/*.md`     | Collection | Ad-hoc                      |

______________________________________________________________________

### When in Doubt

**Ask These Questions:**

1. Does this document already exist? (Check README.md index)
1. Should this be part of existing doc? (Prefer expanding over creating)
1. Will this be updated or become stale? (If stale → don't create)
1. Is this temporary or permanent? (Temporary → `notes/`, Permanent → proper location)

**Golden Rule:** When uncertain, ask in PR or create issue before creating new document.

______________________________________________________________________

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

______________________________________________________________________

## Policy Updates

**This policy itself is a living document.**

**Update when:**

- Documentation structure changes
- New document types emerge
- Better practices discovered

**Version History:**

- v1.0 (Oct 19, 2025): Initial policy created

______________________________________________________________________

**Questions or Suggestions?**

Open an issue with `[docs]` prefix to discuss documentation policy changes.
