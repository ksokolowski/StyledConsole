# Documentation Policy

**Version:** 2.0
**Last Updated:** November 30, 2025

______________________________________________________________________

## Master Documents

All documentation lives in **4 files**:

| Document             | Purpose                         |
| -------------------- | ------------------------------- |
| `USER_GUIDE.md`      | All user-facing documentation   |
| `DEVELOPER_GUIDE.md` | Architecture, API, contributing |
| `PROJECT_STATUS.md`  | Roadmap, tasks, changelog       |
| `archive/`           | Historical reference            |

______________________________________________________________________

## Why This Policy Exists

**Context:** This is a rewrite of a legacy project that failed due to over-engineering.

**Legacy mistakes:**

- 111 files, 19,000+ lines (vs current 21 files, ~4,200 lines)
- Over-documented, under-focused
- Documentation drift (docs described non-existent features)
- Complexity spiral (more docs → more maintenance → more complexity)

**This policy prevents repeating those mistakes.**

______________________________________________________________________

## Core Principles

1. **Less is More** - 4 great docs > 30 scattered files
1. **DRY** - One source of truth per topic
1. **Living Docs** - Update when code changes
1. **Archive Aggressively** - Move completed work to `archive/`
1. **User Focus** - Document for users, not for ourselves

______________________________________________________________________

## The Iron Rules

### Rule 1: Document Decisions, Not Process

**❌ Bad:**

```markdown
First we analyzed legacy code...
Then we discussed options...
Then we decided...
```

**✅ Good:**

```markdown
**Decision:** Support Tier 1 emojis only.
**Rationale:** Complex emojis required 248-line fix in legacy.
```

### Rule 2: Archive Aggressively

The moment work completes:

1. Extract decision → update master docs
1. Move analysis → `archive/`
1. Delete if it was just exploration

### Rule 3: Quality Over Quantity

One great guide > ten mediocre docs.

### Rule 4: Code is Documentation

If you need extensive docs to explain code, the code is too complex.

### Rule 5: User Focus

Ask before documenting:

- "Does this help someone use the library?" → USER_GUIDE.md
- "Does this help someone contribute?" → DEVELOPER_GUIDE.md
- "Is this just for our reference?" → Maybe don't document it

______________________________________________________________________

## What NOT to Document

Based on legacy failures:

- ❌ Work-in-progress thoughts
- ❌ Every analysis step (document conclusion only)
- ❌ Temporary decisions
- ❌ Hypothetical features not in roadmap
- ❌ Process minutiae

______________________________________________________________________

## When to Update

| Event            | Action                    |
| ---------------- | ------------------------- |
| New feature      | Update USER_GUIDE.md      |
| API change       | Update DEVELOPER_GUIDE.md |
| Version release  | Update PROJECT_STATUS.md  |
| Task complete    | Update PROJECT_STATUS.md  |
| Old doc obsolete | Move to archive/          |

______________________________________________________________________

## Quality Standards

### Every Document Must Have

1. **Title** - H1, first line
1. **Version/Date** - Current status
1. **Table of Contents** - If > 200 lines

### Code Examples Must

- ✅ Be runnable (test them!)
- ✅ Show imports
- ✅ Include expected output
- ✅ Use real APIs (not pseudocode)

______________________________________________________________________

## Formatting Standards

### Headers

```markdown
# Document Title

**Version:** X.Y.Z
**Last Updated:** Month Day, Year

---

## Section (H2)

### Subsection (H3)
```

### Horizontal Rules

Use `---` (three hyphens) between major sections.

### Code Blocks

Always specify language:

```python
from styledconsole import Console
```

### Tables

```markdown
| Column | Column |
|--------|--------|
| Data   | Data   |
```

### Lists

- Use `-` for bullets
- Use status emojis: ✅ ⚠️ ❌
- Blank line before list

### Inline Formatting

| Element       | Format      |
| ------------- | ----------- |
| Code/commands | `backticks` |
| File paths    | `backticks` |
| Emphasis      | **bold**    |
| Terms         | *italic*    |

______________________________________________________________________

## Anti-Patterns

| ❌ Don't                  | ✅ Do Instead             |
| ------------------------- | ------------------------- |
| Skip heading levels       | Use H2 → H3 → H4 in order |
| Generic examples (`foo`)  | Real-world examples       |
| Code without language tag | Always specify language   |
| Dense paragraphs          | Break into lists/tables   |
| Undated documents         | Include actual date       |

______________________________________________________________________

## Commit Messages

```text
docs: Update USER_GUIDE with new feature
docs: Archive completed task
docs: Fix code example in DEVELOPER_GUIDE
```

______________________________________________________________________

## Before Committing Checklist

- [ ] Version matches `__init__.py`
- [ ] All code blocks have language
- [ ] All code examples tested
- [ ] No skipped heading levels
- [ ] Tables have header rows

______________________________________________________________________

## Historical Reference

Full original policy (750 lines): `archive/DOCUMENTATION_POLICY_FULL.md`
