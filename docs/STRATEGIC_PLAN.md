# StyledConsole Strategic Plan

**Version:** 1.0
**Last Updated:** December 28, 2025
**Planning Horizon:** Q1-Q2 2026

______________________________________________________________________

## Purpose

This document outlines the **strategic priorities** for the StyledConsole ecosystem. It focuses on **infrastructure, tooling, and project organization** rather than feature development. This plan integrates with existing roadmap (PROJECT_STATUS.md) and follows the 5-Doc Rule.

**Key Principle:** Test locally, merge to main when complete and working. Avoid excessive remote commits.

______________________________________________________________________

## Strategic Pillars

### 1. Documentation & Visibility

**Goal:** Make StyledConsole discoverable and understandable

### 2. Ecosystem Infrastructure

**Goal:** Build supporting repositories and tooling

### 3. Quality & Testing

**Goal:** Ensure reliability across platforms and terminals

### 4. Developer Experience

**Goal:** Make contributing easy and enjoyable

______________________________________________________________________

## Current State (v0.9.8b1)

| Area           | Status              | Notes                     |
| -------------- | ------------------- | ------------------------- |
| Core Library   | ✅ Production-ready | 943 tests, 90% coverage   |
| Documentation  | ✅ Excellent        | 5-Doc Rule established    |
| Examples       | ✅ Organized        | Separate repo with runner |
| Visibility     | ⚠️ Low              | 0 stars, needs promotion  |
| Testing Tools  | ❌ Missing          | No visual regression yet  |
| RF Integration | ❌ Missing          | Planned as separate repo  |

______________________________________________________________________

## Ecosystem Repositories

### Repository Matrix

| Repository                       | Status        | Purpose             | Priority | Version      |
| -------------------------------- | ------------- | ------------------- | -------- | ------------ |
| **StyledConsole**                | ✅ Active     | Core library        | P0       | v0.9.8b1     |
| **StyledConsole-Examples**       | ✅ Active     | Educational content | P1       | v0.1.0       |
| **RobotFramework-StyledConsole** | 🔧 Initialize | RF keyword library  | P2       | v0.1.0-alpha |
| **StyledConsole-VisualTests**    | 📋 Planned    | Visual regression   | P3       | Future       |

**Legend:**

- ✅ Active: Currently maintained
- 🔧 Initialize: Ready to create, mark as Alpha
- 📋 Planned: Documented, wait for prerequisites

______________________________________________________________________

## Feature Backlog

### High-Priority Features (Post-Infrastructure)

Based on current gaps and user needs, these features should be prioritized after infrastructure work completes:

#### Enhanced Gradient System (v0.10.0)

**Current State**: Only vertical gradients implemented
**Limitation**: Documented in PROJECT_STATUS.md line 64
**Scope**: Complete gradient directions + rainbow effects

##### Horizontal Gradients

- **Use Cases**: Progress bars, horizontal separators, table columns, status bars
- **Implementation**:
  - Add `direction="horizontal"` parameter to gradient functions
  - Extend `LinearGradient` class with horizontal interpolation
  - Ensure compatibility with existing vertical gradient API

##### Diagonal Gradients

- **Use Cases**: Decorative headers, dynamic backgrounds, visual effects
- **Directions**: Top-left to bottom-right, bottom-left to top-right
- **Implementation**:
  - Add `direction="diagonal_down"` and `direction="diagonal_up"` parameters
  - 2D color interpolation across both axes
  - Handle edge cases for non-square text blocks

##### Rainbow/Spectrum Effects

- **Current State**: Users must manually define multi-color gradients
- **Use Cases**: Visual highlights, celebratory messages, attention-grabbing headers
- **Features**:
  - `rainbow()` preset using full RGB spectrum (ROYGBIV)
  - `rainbow_text()` helper function for quick application
  - Smooth color transitions across 7 spectral colors
  - Configurable saturation and brightness
- **Integration**: Works with all gradient directions (vertical, horizontal, diagonal)

##### Implementation Notes

- All gradient types share common API: `gradient(text, colors, direction="...")`
- Rainbow preset: `gradient(text, colors="rainbow", direction="horizontal")`
- Examples for each gradient type in visual gallery
- Performance testing for large text blocks with complex gradients
- Terminal compatibility validation (fallback to simpler gradients in limited terminals)

#### Table/Grid System (v0.11.x)

- **Current State**: Users build tables manually with frames
- **Need**: First-class table support with automatic column width, headers, sorting
- **Features**:
  - Automatic column width calculation
  - Header styling with separators
  - Row striping (alternating colors)
  - Cell alignment (left/center/right)
  - Nested frame support for complex layouts
- **Integration**: Works with gradients, themes, and export system

#### Spinner/Loading Animations (v0.11.x)

- **Current State**: Basic progress bar exists, no spinners
- **Use Cases**: Long-running operations, API calls, background tasks
- **Features**:
  - Multiple spinner styles (dots, line, arc, bouncing)
  - Customizable speed and colors
  - Text alongside spinner
  - Context manager support (`with spinner():`)
  - Integration with existing progress tracking

#### Interactive Prompts (v0.12.x)

- **Current State**: Library is output-only
- **Need**: Match Rich's prompt capabilities for complete CLI toolkit
- **Features**:
  - Text input with validation
  - Yes/no confirmations
  - Single/multi-select menus
  - Password input (masked)
  - Type coercion and error handling
- **Note**: Major API expansion, deserves dedicated version

#### Tree/Hierarchy Visualization (v0.12.x)

- **Current State**: No built-in tree rendering
- **Use Cases**: File system display, nested data structures, test results
- **Features**:
  - Expandable/collapsible nodes
  - Custom branch characters
  - Icon integration
  - Styled nodes (colors, bold, etc.)

#### Markdown Rendering (v0.13.x)

- **Current State**: No markdown support
- **Use Cases**: Help text, documentation, formatted messages
- **Features**:
  - Basic markdown syntax (headers, bold, italic, code)
  - Lists (ordered/unordered)
  - Links (rendered as styled text)
  - Code blocks with syntax highlighting (via Pygments)

### Medium-Priority Features (Post-v1.0.0)

#### Layout Containers

- Horizontal/vertical stacking
- Percentage-based widths
- Responsive layouts based on terminal size

#### Advanced Export

- PDF export (via terminal-to-image conversion)
- SVG export for web embedding
- JSON export for programmatic processing

#### Plugin API for Custom Styles

- User-defined border styles
- Custom gradient algorithms
- Theme marketplace/sharing

### Feature Integration Strategy

1. **Each feature gets its own minor version** (0.x.0)
1. **Feature development follows this workflow**:
   - Branch: `feature/<name>`
   - Implementation with tests (95%+ coverage)
   - Examples in StyledConsole-Examples
   - Documentation in USER_GUIDE.md
   - Visual testing (if applicable)
   - Merge when complete and tested
1. **No feature creep**: Stick to planned feature, defer enhancements to next version
1. **User feedback loop**: Release alpha → gather feedback → iterate → stable

______________________________________________________________________

## Phase 1: Foundation Cleanup (v0.9.9 → v0.10.0)

**Timeline:** Weeks 1-4
**Focus:** Documentation, visibility, infrastructure setup
**Note:** No feature development in this phase

### Week 1-2: Documentation Enhancement

**Branch:** `docs/visual-identity`

- [ ] Add "Why StyledConsole?" section to README (content from previous planning)
- [ ] Set up VHS infrastructure for automated GIF generation
  - Create `docs/tapes/` directory structure
  - Write 5-8 basic tape files for core features
  - Create `scripts/generate_gifs.py` helper
  - Add `make gifs` target to Makefile
- [ ] Generate initial GIFs for README
- [ ] Update main README with visual examples
- [ ] Test GIF rendering on GitHub (light/dark themes)

**Deliverables:**

- Updated README.md with visual section
- VHS tape infrastructure (local only, no CI yet)
- 5-8 GIFs demonstrating core features
- Documentation in CONTRIBUTING.md about GIF generation

**Merge Criteria:**

- [ ] All GIFs render correctly on GitHub
- [ ] README is visually compelling
- [ ] VHS tapes are documented and runnable
- [ ] `make gifs` works reliably

### Week 3-4: Project Hygiene

**Branch:** `refactor/project-cleanup`

- [ ] Audit all documentation for 5-Doc Rule compliance
- [ ] Move completed work to `archive/` if needed
- [ ] Review and update PROJECT_STATUS.md with current metrics
- [ ] Update CHANGELOG.md for v0.9.9 (if releasing)
- [ ] Review GitHub settings:
  - Topics/tags
  - Issue templates
  - Discussion categories
  - Branch protection rules
- [ ] Prepare PyPI release checklist

**Deliverables:**

- Clean, organized documentation structure
- Updated PROJECT_STATUS.md
- PyPI release preparation

**Merge Criteria:**

- [ ] All 5 master docs are up-to-date
- [ ] No documentation debt
- [ ] Ready for potential v0.9.9 release

______________________________________________________________________

## Phase 2: Ecosystem Expansion (v0.10.0 → v0.10.5)

**Timeline:** Weeks 5-12
**Focus:** RobotFramework integration, examples enhancement

### Weeks 5-8: RobotFramework-StyledConsole (Alpha)

**Repository:** `RobotFramework-StyledConsole` (NEW)
**Branch:** `main` (new repo, work directly until stable)
**Version:** v0.1.0-alpha

**Setup:**

- [ ] Create repository with `uv init --lib`

- [ ] Set up project structure:

  ```text
  RobotFramework-StyledConsole/
  ├── src/StyledConsoleLibrary/
  │   └── __init__.py           # Main library
  ├── examples/
  │   ├── basic_usage.robot     # Simple examples
  │   └── comprehensive.robot   # Full feature demo
  ├── tests/
  │   └── test_keywords.robot   # Self-tests
  ├── docs/
  │   └── keywords.html         # Generated libdoc
  ├── pyproject.toml
  ├── Makefile
  └── README.md
  ```

- [ ] Implement 40+ keywords (from previous planning)

- [ ] Create comprehensive example suites

- [ ] Write README with installation and usage

- [ ] Generate keyword documentation with `robot.libdoc`

**Features (from previous discussion):**

- Print Styled Text
- Create Frame (8 border styles)
- Print With Gradient
- Create Banner
- Print With Icon
- Environment detection helpers
- Progress bar keywords
- Export keywords (HTML/text)

**Testing:**

- Test locally with `uv run robot examples/`
- Verify HTML reports look good
- Test on Ubuntu (primary)
- Test on Windows 11 (if accessible)

**Mark as Alpha:**

- Add prominent ALPHA notice in README
- Set version to 0.1.0-alpha in pyproject.toml
- Tag as "alpha" in GitHub topics
- Note in README: "API may change without notice"

**Deliverables:**

- Working RF library with 40+ keywords
- Example test suites
- Complete README
- Generated keyword documentation

**Publish Criteria (when ready):**

- [ ] All keywords tested and working
- [ ] Examples run successfully
- [ ] Documentation is complete
- [ ] README has clear Alpha disclaimer
- [ ] Ready for PyPI as alpha release

### Weeks 9-12: Examples Enhancement

**Repository:** StyledConsole-Examples
**Branch:** `feature/visual-gallery`

- [ ] Add screenshots/GIFs to README
- [ ] Create visual gallery section
- [ ] Organize examples by complexity (beginner/intermediate/advanced)
- [ ] Add README to each category directory
- [ ] Test runner enhancements (if needed)

**Deliverables:**

- Visual gallery in README
- Category-specific documentation
- Enhanced discoverability

**Merge Criteria:**

- [ ] All examples have visual previews
- [ ] README is compelling
- [ ] Examples are well-organized

______________________________________________________________________

## Phase 3: Visual Testing Infrastructure (v0.11.0+)

**Timeline:** Weeks 13-20
**Focus:** Automated visual regression testing

**Prerequisites:**

- RobotFramework-StyledConsole must be stable (not alpha)
- VHS tape infrastructure must be proven
- Multi-terminal testing research complete

### Research Phase (Weeks 13-14)

**Branch:** `research/visual-testing` (local only)

- [ ] Test VHS on different terminals:
  - GNOME Terminal
  - Kitty
  - Ghostty
  - xterm
  - Windows Terminal (if accessible)
- [ ] Prototype snapshot comparison logic
- [ ] Design terminal capability profiles
- [ ] Document findings in `archive/visual-testing-research.md`

**Decision Point:**

- If VHS works well: Proceed with full implementation
- If VHS has issues: Research alternatives (Terminalizer, custom solution)

### Implementation Phase (Weeks 15-20)

**Repository:** `StyledConsole-VisualTests` (NEW)
**Only create if research phase succeeds**

Structure:

```text
StyledConsole-VisualTests/
├── tapes/
│   ├── features/          # Feature-specific tapes
│   └── regression/        # Regression test tapes
├── libraries/
│   └── VisualTestLib.py   # Python helper
├── tests/
│   ├── basic_rendering/   # Basic tests
│   └── advanced/          # Complex tests
├── snapshots/             # Expected outputs (git-lfs?)
├── scripts/
│   └── run_visual_tests.py
├── Makefile
└── README.md
```

**Deliverables:**

- VHS-based visual testing framework
- RF test suites
- Terminal profiles
- CI/CD configuration (GitHub Actions)
- Snapshot management strategy

______________________________________________________________________

## Phase 4: Promotion & Community (Ongoing)

**Timeline:** Start after Phase 1 complete
**Focus:** Visibility and adoption

### Promotion Checklist

**Before promoting:**

- [ ] v0.9.9+ released to PyPI
- [ ] README has visual examples
- [ ] "Why StyledConsole?" section exists
- [ ] Examples repository is polished
- [ ] GitHub topics/tags are optimized

**Promotion Activities:**

- [ ] Post on r/Python
- [ ] Post on r/programming
- [ ] Write dev.to article
- [ ] Submit Show HN post
- [ ] Add to awesome-python lists
- [ ] Create Twitter/X thread
- [ ] Set up GitHub Discussions

**Defer until ready:**

- Conference talks (wait for v1.0.0)
- Blog tour (wait for adoption)
- Sponsorship campaigns (wait for users)

______________________________________________________________________

## Version Planning

### Version Semantics (0.x.y)

Following your preference to avoid 1.0.0 prematurely:

- **0.x.0** = Minor release (new features, infrastructure)
- **0.x.y** = Patch release (bugs, docs, small improvements)

### Tentative Version Roadmap

| Version   | Focus                          | Type           | Estimated  |
| --------- | ------------------------------ | -------------- | ---------- |
| v0.9.9    | Documentation + VHS            | Infrastructure | Week 4     |
| v0.10.0   | Enhanced Gradient System       | Feature        | Week 6     |
| v0.10.1   | RF Library Alpha               | Ecosystem      | Week 8     |
| v0.10.2-5 | Examples Enhancement           | Infrastructure | Weeks 9-12 |
| v0.11.0   | Table/Grid System              | Feature        | Week 14    |
| v0.11.1   | Spinner/Loading Animations     | Feature        | Week 16    |
| v0.11.2   | Visual Testing (if ready)      | Infrastructure | Week 20    |
| v0.12.0   | Interactive Prompts            | Feature        | Week 24    |
| v0.12.1   | Tree/Hierarchy Visualization   | Feature        | Week 28    |
| v0.13.0   | Markdown Rendering             | Feature        | Week 32    |
| v0.14.0   | Test Automation Presets - Core | Feature        | Q2 2026    |
| v0.15.0+  | Additional presets & polish    | Feature        | Q3 2026    |
| v1.0.0    | API freeze & Production        | Milestone      | Q4 2026    |

**Note:** Version numbers may shift based on feature complexity and priorities. This roadmap integrates both infrastructure work (Phases 1-3) and feature development (Feature Backlog).

**Key Principle:** Don't rush to 1.0.0. It will happen when:

- API is stable and proven
- All major features are complete
- Test coverage is excellent
- Documentation is comprehensive
- Community adoption is established

______________________________________________________________________

## Decision Framework

### When to Create a New Branch

**Create branch when:**

- Change spans multiple work sessions
- Change affects multiple files/areas
- Want to test before committing to main

**Work on main when:**

- Quick documentation fixes
- Single-file changes
- Emergency hotfixes

### When to Merge to Main

**Criteria for merge:**

- [ ] All tests pass (`make qa`)
- [ ] Documentation updated
- [ ] Changes are complete and working
- [ ] Tested locally
- [ ] Atomic commit(s) with clear messages

**Do not merge:**

- Work in progress
- Broken tests
- Incomplete features
- Experimental code

### When to Push to Remote

**Push when:**

- Branch is ready for review
- Feature is complete
- Need backup of work
- Collaborating with others

**Avoid pushing:**

- Every local commit
- Experimental code
- Broken builds

______________________________________________________________________

## Integration with Existing Documents

### This Plan Updates

**PROJECT_STATUS.md:**

- Add ecosystem repository status
- Update roadmap with infrastructure focus
- Track strategic initiatives

**CONTRIBUTING.md:**

- Reference this plan for contributors
- Link to branch strategy
- Explain ecosystem structure

**CHANGELOG.md:**

- Track infrastructure releases
- Document ecosystem additions
- Note strategic milestones

### This Plan Does NOT Replace

- Feature roadmap (stays in PROJECT_STATUS.md)
- API documentation (stays in USER_GUIDE.md)
- Architecture details (stays in DEVELOPER_GUIDE.md)
- Release notes (stays in CHANGELOG.md)

______________________________________________________________________

## Success Metrics

### Phase 1 Success (Weeks 1-4)

- [ ] README has 5+ visual examples
- [ ] VHS infrastructure is working
- [ ] Project feels "polished"
- [ ] Ready for promotion

### Phase 2 Success (Weeks 5-12)

- [ ] RF library is usable (alpha)
- [ ] Examples repository is visually appealing
- [ ] At least 3-5 GitHub stars (early adopters)
- [ ] Community feedback received

### Phase 3 Success (Weeks 13-20)

- [ ] Visual testing is automated
- [ ] Tests run on multiple terminals
- [ ] Regression catching works
- [ ] CI/CD integration complete

______________________________________________________________________

## Risk Management

| Risk                   | Impact | Mitigation                                        |
| ---------------------- | ------ | ------------------------------------------------- |
| VHS doesn't work well  | High   | Research phase first, have fallback               |
| RF library too complex | Medium | Start with core keywords, expand later            |
| No community interest  | Medium | Focus on quality, promotion timing                |
| Time constraints       | Medium | Prioritize ruthlessly, defer non-critical         |
| Scope creep            | High   | Stick to strategic plan, resist feature additions |

______________________________________________________________________

## Review Schedule

**This document should be reviewed:**

- After each phase completion
- Quarterly (even if phases aren't done)
- When major blockers appear
- When community feedback requires pivot

**Update triggers:**

- Completed phases
- Changed priorities
- New learnings
- External factors (new tools, community needs)

______________________________________________________________________

## Archive Policy

**When to archive this document:**

- When all phases are complete
- When a new strategic plan is created
- When the roadmap fundamentally changes

**Archive location:** `docs/archive/STRATEGIC_PLAN_2026Q1Q2.md`

______________________________________________________________________

## Notes

- This plan prioritizes **infrastructure** over features
- Features are tracked in PROJECT_STATUS.md roadmap (v0.10-0.14)
- This plan enables future feature development
- All timelines are estimates, quality over speed
- Local testing and incremental progress are valued

______________________________________________________________________

**Next Review:** After Phase 1 completion (est. Week 4)
