# Documentation Split Plan - v0.9.8.1

**Strategy**: Option A - Public/Private Repository Split
**Target Version**: 0.9.8.1
**Date**: December 28, 2025

______________________________________________________________________

## Public Repository (StyledConsole)

### Documents to Keep Public

These documents are user-facing and essential for PyPI users:

| Document              | Purpose                                        | Action                                                        |
| --------------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| `README.md`           | Quick start, installation, basic examples      | **Simplify** - Remove strategic planning references           |
| `CHANGELOG.md`        | Version history, release notes                 | **Keep** - Essential for users tracking changes               |
| `LICENSE`             | Apache-2.0 license                             | **Keep** - Required                                           |
| `CONTRIBUTING.md`     | Contribution guidelines                        | **Simplify** - Keep basic workflow, remove strategic planning |
| `docs/USER_GUIDE.md`  | API reference, usage examples, troubleshooting | **Keep** - Core user documentation                            |
| `pyproject.toml`      | Package metadata and dependencies              | **Keep** - Required                                           |
| `.github/workflows/*` | CI/CD pipelines                                | **Keep** - Public automation                                  |

### Documents to Remove from Public

Move to private repository:

| Document                          | Reason                                        | Destination              |
| --------------------------------- | --------------------------------------------- | ------------------------ |
| `docs/STRATEGIC_PLAN.md`          | Internal roadmap, feature backlog             | Private repo root        |
| `docs/PROJECT_STATUS.md`          | Detailed status, ecosystem planning           | Private repo root        |
| `docs/DEVELOPER_GUIDE.md`         | Internal architecture, development philosophy | Private repo `/docs/`    |
| `docs/DOCUMENTATION_POLICY.md`    | Internal documentation standards              | Private repo `/docs/`    |
| `docs/BEST_PRACTICES.md`          | Internal coding standards                     | Private repo `/docs/`    |
| `.github/copilot-instructions.md` | AI agent instructions                         | Private repo `/.github/` |
| `DOCUMENTATION_SPLIT_PLAN.md`     | This file (temporary)                         | Delete after migration   |

______________________________________________________________________

## Private Repository (StyledConsole-Internal)

### Proposed Structure

```
StyledConsole-Internal/
├── README.md                    # Overview of private repo purpose
├── STRATEGIC_PLAN.md            # Long-term planning, feature backlog
├── PROJECT_STATUS.md            # Current status, roadmap, metrics
├── RELEASE_CHECKLIST.md         # Step-by-step release process
├── docs/
│   ├── DEVELOPER_GUIDE.md       # Architecture, development philosophy
│   ├── DOCUMENTATION_POLICY.md  # Documentation standards
│   ├── BEST_PRACTICES.md        # Coding standards
│   └── TESTING_STRATEGY.md      # Testing philosophy and practices
├── .github/
│   └── copilot-instructions.md  # AI agent instructions
└── planning/
    ├── feature-proposals/       # Detailed feature designs
    ├── architecture-decisions/  # ADRs (Architecture Decision Records)
    └── meeting-notes/           # Planning discussions
```

### New Documents for Private Repo

**`RELEASE_CHECKLIST.md`** - Comprehensive release process:

- Pre-release QA steps
- Version bumping procedure
- TestPyPI validation
- PyPI publication
- Post-release verification

**`docs/TESTING_STRATEGY.md`** - Testing philosophy:

- Test categories (unit, integration, snapshot)
- Coverage requirements
- Visual testing strategy
- Pre-commit hook rationale

______________________________________________________________________

## Public README.md Simplification

### Current Issues

- Too much strategic planning detail
- References to internal roadmap
- Developer-centric content

### Simplified Structure

```markdown
# StyledConsole

Elegant terminal output for Python applications.

## Features
- Beautiful frames and banners
- Gradient effects
- Emoji support with ASCII fallback
- Theme system
- Environment-aware rendering

## Installation
pip install styledconsole

## Quick Start
[Basic examples]

## Documentation
- User Guide: docs/USER_GUIDE.md
- Changelog: CHANGELOG.md
- Contributing: CONTRIBUTING.md

## Examples
[Link to StyledConsole-Examples repo]

## License
Apache-2.0
```

______________________________________________________________________

## Public CONTRIBUTING.md Simplification

### Remove These Sections

- Strategic planning references
- Long-term roadmap discussions
- Internal development philosophy

### Keep These Sections

- Setting up development environment
- Running tests
- Code quality requirements
- Git workflow
- Conventional commits
- Pre-commit hooks

______________________________________________________________________

## Migration Steps

1. **Create Private Repository**

   - Initialize `StyledConsole-Internal` on GitHub
   - Set as private repository
   - Add collaborators (you + AI agents)

1. **Copy Strategic Documents**

   - `STRATEGIC_PLAN.md` → Private repo root
   - `PROJECT_STATUS.md` → Private repo root
   - `docs/DEVELOPER_GUIDE.md` → Private repo `/docs/`
   - `docs/DOCUMENTATION_POLICY.md` → Private repo `/docs/`
   - `docs/BEST_PRACTICES.md` → Private repo `/docs/`
   - `.github/copilot-instructions.md` → Private repo `/.github/`

1. **Create New Private Repo Documents**

   - `RELEASE_CHECKLIST.md`
   - `docs/TESTING_STRATEGY.md`
   - Private repo `README.md`

1. **Simplify Public Repository**

   - Simplify `README.md`
   - Simplify `CONTRIBUTING.md`
   - Remove strategic documents
   - Update references

1. **Update Cross-References**

   - Public docs reference only public docs
   - Private docs reference both public and private

______________________________________________________________________

## Version 0.9.8.1 Release Notes

**Type**: Test release (TestPyPI)
**Focus**: Documentation cleanup, examples fixes, pre-release validation

### Changes

- Fixed examples execution context (use `uv run` from main repo)
- Fixed TTY detection in terminal validation scripts
- Code quality improvements (linting fixes)
- Documentation structure cleanup (public/private split)

### Testing Checklist

- [x] All 37 examples passing
- [x] Code quality checks passing (`make qa`)
- [ ] Version updated to 0.9.8.1
- [ ] CHANGELOG.md updated
- [ ] Build test (`uv build`)
- [ ] TestPyPI publication
- [ ] TestPyPI installation test

______________________________________________________________________

## Notes

- This is a **test release** to validate TestPyPI workflow
- No breaking changes or major features
- Focus on infrastructure and documentation
- Next release (0.9.9) will include VHS documentation
