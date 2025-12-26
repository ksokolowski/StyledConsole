# Documentation Policy

**Version:** 2.1
**Last Updated:** December 26, 2025

______________________________________________________________________

## Master Documents

All documentation lives in **exactly five master documents**:

| Document             | Purpose                       | Source of Truth For...       |
| -------------------- | ----------------------------- | ---------------------------- |
| `USER_GUIDE.md`      | Tutorials & visual galleries  | Library usage & examples     |
| `DEVELOPER_GUIDE.md` | Architecture & internal logic | Design decisions & internals |
| `CHANGELOG.md`       | Release history               | Project history & versions   |
| `PROJECT_STATUS.md`  | Roadmap & metrics             | Current health & future      |
| `CONTRIBUTING.md`    | Dev workflow & PR standards   | Contribution process         |

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

1. **The 5-Doc Rule** - Maintain exactly 5 core documents to prevent information rot.
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

| Event               | Action                                      |
| ------------------- | ------------------------------------------- |
| New feature         | Update `USER_GUIDE.md`                      |
| Architecture change | Update `DEVELOPER_GUIDE.md`                 |
| Version release     | Update `CHANGELOG.md` & `PROJECT_STATUS.md` |
| Task complete       | Update `PROJECT_STATUS.md`                  |
| Workflow change     | Update `CONTRIBUTING.md`                    |
| Doc obsolete        | Move to `archive/`                          |

______________________________________________________________________

## The 5-Doc Architecture

Each document has a strictly defined boundary to prevent redundancy:

- **[`USER_GUIDE.md`](USER_GUIDE.md)**: The "How-To". Contains tutorials, copy-paste examples, and the visual gallery. If it doesn't help a user *use* the library, it doesn't belong here.
- **[`DEVELOPER_GUIDE.md`](DEVELOPER_GUIDE.md)**: The "How-it-Works". Contains architecture diagrams, module relationships, and internal logic explanations.
- **[`CHANGELOG.md`](../CHANGELOG.md)**: The "What-Changed". Chronological history of all releases. No roadmap or usage info here.
- **[`PROJECT_STATUS.md`](PROJECT_STATUS.md)**: The "Where-We-Are". Current metrics, roadmap, and active task lists.
- **[`CONTRIBUTING.md`](../CONTRIBUTING.md)**: The "How-to-Help". Dev environment setup, `make` commands, and PR standards.

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

### ASCII Art / Box-Drawing Visualizations

When documenting preset output or frame visualizations:

**Rules:**

1. **Verify character-by-character** - Every line in a box must have identical width
1. **Count emoji width correctly** - Emojis like ⏱️, ⚠️, ⭐ may display as 1 or 2 columns
1. **Test in monospace** - Render in a fixed-width font before committing
1. **Align borders precisely** - Top border (`╭─...─╮`) must match bottom (`╰─...─╯`) exactly

**❌ Bad (misaligned):**

```text
╭────────────────────────────────────╮
│ ⏱️  Duration: 2.45s                    │
╰────────────────────────────────────╯
```

**✅ Good (aligned):**

```text
╭────────────────────────────────────╮
│ ⏱️  Duration: 2.45s                │
╰────────────────────────────────────╯
```

**Why this matters:** This library is specifically about terminal rendering and visual
width calculation. Misaligned ASCII art in documentation undermines the project's
credibility and creates confusion about expected output.

**Verification tip:** Use `visual_width()` from the library itself to verify line lengths:

```python
from styledconsole.utils.text import visual_width
assert visual_width("│ ⏱️  Duration: 2.45s                │") == 38
```

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

## Before Committing Checklist

- [ ] Version matches `__init__.py`
- [ ] All code blocks have language
- [ ] All code examples tested
- [ ] No skipped heading levels
- [ ] Tables have header rows

______________________________________________________________________

## Historical Reference

Full original policy (750 lines): `archive/DOCUMENTATION_POLICY_FULL.md`
