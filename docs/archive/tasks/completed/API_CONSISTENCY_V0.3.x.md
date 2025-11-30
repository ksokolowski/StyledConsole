# API Consistency & Unification - Detailed Implementation Plan

**Task ID:** API_CONSISTENCY_V0.3.x
**Priority:** High
**Phase:** v0.3.x (near-term) / v1.0 (future)
**Date Created:** November 15, 2025
**Status:** ⏳ Planned
**Tracked in:** `doc/project/TASKS.md` (main task list)

**Related Documents:**

- `doc/notes/CONSOLE_API_IMPROVEMENTS.md` (source analysis)
- `doc/project/SPECIFICATION.md` (user journeys)
- `doc/project/PLAN.md` (architecture)

______________________________________________________________________

## Progress Tracking

### Phase 1: Gallery Example Cleanup (v0.3.x - Immediate)

- [ ] Task 1.2.1: Fix `colors_showcase.py` - remove legacy patterns, use gradient helpers
- [ ] Task 1.2.2: Fix `gradients_showcase.py` - convert `style="gradient"` to `start_color`/`end_color`
- [ ] Task 1.2.3: Fix `emojis_showcase.py` - replace raw emojis with `EMOJI[...]` constants
- [ ] Task 1.2.4: Fix `banners_showcase.py` - eliminate `style="rainbow"`, use modern API
- [ ] Task 1.2.5: Verify all 4 gallery files execute without errors

### Phase 2: Documentation & Clarification (v0.3.x - Near-term)

- [x] Task 1.3: Document color parameter naming conventions in user docs
- [x] Task 4.1-4.2: Update docstrings and examples for alignment semantics
- [x] Task 5.3: Document error handling principles
- [x] Task 6.3: Update emoji guide with examples reference

### Phase 3: Optional API Extensions (v0.3.x - Optional)

- [x] Task 1.1: Extend `Console.frame()` to support `start_color`/`end_color` gradients
- [x] Add gradient frame tests
- [x] Add gradient frame examples

### Phase 4: Advanced Features (v1.0 - Future)

- [ ] Task 2.1-2.4: Region-specific style parameters (`title_style`, `content_style`)
- [ ] Task 3.1-3.4: Preprocessed content API (`console.prepare_content`)
- [ ] Task 5.1-5.2: Standardize validation behavior

### Phase 5: Breaking Cleanup (v1.0 - Future)

- [ ] Deprecate/remove `style`/`colors` on banner
- [ ] Tighten `ColorType` to exclude `tuple[str, ...]`
- [ ] Publish migration guide

______________________________________________________________________

## Problem Statement

The current StyledConsole API (v0.3.0) has evolved organically, resulting in:

1. **Inconsistent gradient/color parameter names** across methods (`style`/`colors` vs `start_color`/`end_color`)
1. **Overloaded semantics** (`border_color` used for both solid colors and implicit gradients via tuples)
1. **Missing style capabilities** (no way to apply bold/italic to frame titles or banner text)
1. **Unclear region naming** (confusion between `color` vs `content_color` vs `border_color`)
1. **No preprocessed content API** for large, styled text blocks with auto-sized frames

This creates friction for users and makes the codebase harder to evolve.

______________________________________________________________________

## Goals

### v0.3.x (Incremental Improvements)

- [ ] **Audit and fix all gallery examples** to use modern API patterns
- [ ] **Document parameter naming conventions** in user-facing docs
- [ ] **Extend Console.frame()** to support gradients via `start_color`/`end_color` (optional)
- [ ] **Stop encouraging legacy patterns** (`style="gradient"`, tuple-of-names in `border_color`)

### v1.0 (Breaking Cleanup)

- [ ] **Deprecate/remove** `style` and `colors` parameters on `Console.banner()`
- [ ] **Add region-specific style knobs** (`title_style`, `content_style`) to enable bold/italic on titles
- [ ] **Implement preprocessed content API** (`console.prepare_content(...)`) for Rich-native styled blocks
- [ ] **Tighten ColorType** to exclude `tuple[str, ...]` for gradients

______________________________________________________________________

## Specification

### 1. Color & Gradient Parameter Unification

#### Current State

```python
# Console.banner - modern (v0.3.0)
console.banner("Deploy", start_color="cyan", end_color="purple")

# Console.banner - legacy (examples still use)
console.banner("Deploy", style="gradient", colors=["cyan", "purple"])
console.banner("Rainbow", style="rainbow")

# Console.frame - solid only
console.frame("content", border_color="blue", content_color="white")

# Examples overload border_color with tuples:
console.frame("...", border_color=("red", "orange", "yellow"))  # implies gradient
```

#### Desired State (v0.3.x)

```python
# Solid colors - single region
console.text("Hello", color="cyan", bold=True)
console.banner("Title", color="green")

# Solid colors - multi-region
console.frame("content", content_color="white", border_color="blue", title_color="cyan")

# Gradients - always via start_color/end_color
console.banner("Deploy", start_color="cyan", end_color="purple")
console.frame("content", start_color="cyan", end_color="purple")  # NEW in v0.3.x

# Advanced gradients - via effects helpers
from styledconsole.effects import gradient_frame, diagonal_gradient_frame, rainbow_frame

gradient_frame("content", start_color="red", end_color="blue", border="rounded")
diagonal_gradient_frame("content", start_color="coral", end_color="orange")
rainbow_frame("Rainbow text", border="double")
```

#### Implementation Tasks

**Task 1.1: Extend Console.frame() for gradients**

- Add optional `start_color`/`end_color` parameters to `Console.frame()` signature
- When both are set, apply gradient to content (via RenderingEngine)
- Document in docstring that gradient applies to content, not border (border gradients remain in effects)
- Test: gradient frames render correctly, interact properly with `content_color` (gradient wins)

**Task 1.2: Audit and fix gallery examples**

- `colors_showcase.py`: Remove tuple-of-names in `border_color`, use gradient helpers
- `gradients_showcase.py`: Convert all `style="gradient"` → `start_color`/`end_color`
- `banners_showcase.py`: Eliminate `style="rainbow"`, use `start_color`/`end_color` or note as future feature
- `emojis_showcase.py`: Ensure consistent color parameters

**Task 1.3: Document naming conventions**

- Add "Color Parameter Conventions" section to user docs (or README)
- State rules:
  - `color` for single-region APIs (text, banner text)
  - `content_color`, `border_color`, `title_color` for multi-region APIs (frame)
  - `start_color`/`end_color` for 2-stop gradients
  - Effects helpers for advanced gradients (diagonal, rainbow, multi-stop)

**Acceptance Criteria:**

- All gallery examples execute without errors
- No examples use `style`/`colors` or tuple-of-names in `border_color`
- `Console.frame()` supports gradient via `start_color`/`end_color` (optional feature)
- User docs clearly state parameter naming rules

______________________________________________________________________

### 2. Text Style Knobs for Titles and Content

#### Current State

```python
# Console.text - full style support
console.text("Warning", color="yellow", bold=True, italic=True)

# Console.frame - only colors, no styles for title or content
console.frame("content", title="Title", title_color="cyan")
# No way to make title bold or italic
```

#### Desired State (v1.0)

```python
# Option A: Region-specific style flags
console.frame(
    "content",
    title="Status Report",
    title_color="cyan",
    title_bold=True,
    content_color="white",
    content_italic=True,
)

# Option B: Region-specific style string (following Rich)
console.frame(
    "content",
    title="Status Report",
    title_style="bold cyan",
    content_style="italic white",
)
```

#### Implementation Tasks

**Task 2.1: Design style parameter approach**

- Decide: individual flags (`title_bold`, `title_italic`) vs style string (`title_style="bold italic cyan"`)
- Document rationale in PLAN.md or CONSOLE_API_IMPROVEMENTS.md
- Pros/cons:
  - Flags: consistent with `Console.text()`, but many parameters
  - Style string: more compact, follows Rich pattern, but less discoverable

**Task 2.2: Implement for Console.frame()**

- Add chosen style parameters to `Console.frame()` signature
- Update `RenderingEngine.print_frame()` to build Rich `Text` objects for title/content using style parameters
- Ensure compatibility with existing `title_color`/`content_color` (style overrides or merges)

**Task 2.3: Extend to Console.banner() if needed**

- Evaluate if banner text needs style flags (currently uses pyfiglet ASCII art, style may not apply meaningfully)
- If yes, add `text_style` or `bold`/`italic` flags

**Task 2.4: Update gallery examples**

- Add examples showing styled titles in frames
- Demonstrate bold/italic content in dashboards

**Acceptance Criteria:**

- Frame titles can be bold, italic, underlined via new parameters
- Frame content can be styled independently of title
- All changes backward-compatible (new parameters optional, default to current behavior)
- Examples demonstrate new capabilities

______________________________________________________________________

### 3. Preprocessed Content API for Large Text Blocks

#### Current State

```python
# Users must manually wrap and calculate widths
from styledconsole.utils.wrap import wrap_text
from styledconsole.utils.text import visual_width

text = "Long paragraph with emojis 🚀..."
wrapped = wrap_text(text, max_width=70)
max_line_width = max(visual_width(line) for line in wrapped)

console.frame(wrapped, title="Details", width=max_line_width + 4)
```

#### Desired State (v1.0)

```python
# Option A: Console helper
content = console.prepare_content(
    text="Long paragraph with emojis 🚀...",
    max_width=80,
    color="cyan",
    bold=True,
    preserve_paragraphs=True,
)
console.frame(content, title="Details")  # Width auto-determined

# Option B: Utility function
from styledconsole.utils import prepare_content_block

content = prepare_content_block(
    text="Long paragraph...",
    max_width=80,
    color="cyan",
    bold=True,
)
console.frame(content, title="Details")
```

#### Implementation Tasks

**Task 3.1: Design API surface**

- Decide: method on `Console` vs standalone utility function
- Parameters:
  - `text: str` (input text, potentially multi-paragraph)
  - `max_width: int | None` (optional width hint)
  - Style knobs: `color`, `bold`, `italic`, `underline`, `dim` (reuse from `Console.text`)
  - `preserve_paragraphs: bool` (default True)
- Return type: Rich `Text` or list of strings compatible with `Console.frame()`

**Task 3.2: Implement core logic**

- Use `utils.wrap.wrap_text()` for emoji-safe wrapping
- Build Rich `Text` object with requested styles
- Optionally compute suggested `width` based on max line visual width
- Ensure content can be passed directly to `Console.frame()` without re-wrapping

**Task 3.3: Update RenderingEngine if needed**

- Ensure `print_frame()` can accept Rich `Text`/renderables as content (may already work)
- If not, extend to handle Rich renderables alongside plain strings

**Task 3.4: Create gallery examples**

- `large_text_showcase.py`: demonstrate multi-paragraph help text in auto-sized frame
- `log_excerpt_showcase.py`: show log output in frame with auto-width
- Include emoji-rich content to validate width calculations

**Acceptance Criteria:**

- Users can prepare large text blocks with styles + wrapping in one call
- Prepared content integrates seamlessly with `Console.frame()`
- Frame width auto-determined from content when `width` not specified
- Examples demonstrate real-world use cases (help text, logs)

______________________________________________________________________

### 4. Alignment & Layout Semantics Clarification

#### Current State

- `Console.frame(..., align=...)` controls content alignment inside frame
- `Console.banner(..., align=...)` controls ASCII art alignment inside banner
- `Console.text(...)` has no `align` (user must wrap in frame for alignment)
- Examples sometimes rely on terminal width implicitly

#### Desired State (v0.3.x - documentation only)

- **Document clearly** what `align` controls for each API
- **Update examples** to use explicit `width` with `align` for deterministic behavior
- **Note future work**: nested frames / higher-level layout (section 1 of CONSOLE_API_IMPROVEMENTS.md)

#### Implementation Tasks

**Task 4.1: Update docstrings**

- `Console.frame()`: clarify `align` controls content alignment inside the frame box
- `Console.banner()`: clarify `align` controls ASCII art alignment inside banner area
- `Console.text()`: note alignment should be handled via wrapping in frame or layout

**Task 4.2: Audit gallery examples**

- Ensure examples using `align="center"` also specify `width` explicitly
- Remove reliance on implicit terminal width for centering

**Task 4.3: Add alignment section to user docs**

- Short "Alignment & Layout" guide explaining:
  - When to use `align` on frame vs banner
  - How to center output deterministically (explicit width)
  - Future layout helpers (columns/grid) as placeholder

**Acceptance Criteria:**

- Docstrings clearly state what `align` controls
- Gallery examples use `align` with explicit `width`
- User docs explain alignment behavior

______________________________________________________________________

### 5. Error Handling & Validation Expectations

#### Current State

- Unknown color names may silently fall back or raise unclear errors
- Ambiguous gradient config (`start_color` without `end_color`) behavior undefined
- Invalid border/font names fall back to defaults without user visibility

#### Desired State (v0.3.x)

- **Document validation principles** in user docs or PLAN.md
- **Make ambiguous cases explicit**:
  - `start_color` without `end_color` → documented fallback to solid or clear error
  - Unknown color/border/font → documented default + optional warning in debug mode
- **Improve error messages** to mention parameter names and expected types

#### Implementation Tasks

**Task 5.1: Audit validation paths**

- Review `console.py`, `effects.py`, `utils/color.py` for validation logic
- Identify ambiguous cases (partial gradient params, unknown names)

**Task 5.2: Standardize error handling**

- Decide policy:
  - Recoverable issues (unknown color) → fallback + debug log
  - Ambiguous issues (partial gradient) → error or documented fallback
- Implement consistently across all APIs

**Task 5.3: Document validation behavior**

- Add "Error Handling" section to user docs
- List common validation scenarios and expected behavior
- Include 1-2 code examples

**Acceptance Criteria:**

- Ambiguous gradient configs have documented, predictable behavior
- Unknown color/border/font names fall back gracefully with clear defaults
- Error messages are actionable (mention parameter names, expected types)
- User docs explain validation principles

______________________________________________________________________

### 6. Emoji Usage & Examples Consistency

#### Current State

- Some examples use raw emoji literals (`"🚀"`) instead of `EMOJI["rocket"]`
- Emoji categories not consistently demonstrated across examples

#### Desired State (v0.3.x)

- **All examples** use `from styledconsole import EMOJI` and named constants
- **Emoji showcase** groups emojis by category (status, faces, objects, etc.)
- **User docs** mention emoji safety and that emojis are optional

#### Implementation Tasks

**Task 6.1: Refactor emojis_showcase.py**

- Replace all raw emoji literals with `EMOJI[...]` constants
- Organize demo functions by category (status indicators, weather, transport, etc.)
- Add comments/section titles for each category

**Task 6.2: Audit other gallery examples**

- Scan `colors_showcase.py`, `gradients_showcase.py`, `banners_showcase.py` for raw emojis
- Replace with `EMOJI` constants

**Task 6.3: Update emoji guide**

- Add note in `doc/guides/EMOJI_GUIDELINES.md` linking to examples
- State that emojis are optional and rendering is stable without them

**Acceptance Criteria:**

- No raw emoji literals in gallery examples
- `emojis_showcase.py` demonstrates all emoji categories
- Emoji guide references examples and states optional nature

______________________________________________________________________

## Implementation Phases

### Phase 1: Gallery Example Cleanup (v0.3.x - immediate)

**Duration:** 1-2 days
**Goal:** Make existing examples canonical references for the documented API

- Task 1.2: Fix colors, gradients, banners, emojis showcases
- Task 4.2: Audit alignment usage in examples
- Task 6.1, 6.2: Replace raw emojis with EMOJI constants

**Deliverables:**

- 4 fixed gallery files committed
- All examples execute without errors
- Examples demonstrate modern API patterns

### Phase 2: Documentation & Clarification (v0.3.x - near-term)

**Duration:** 1-2 days
**Goal:** Make API conventions explicit in user-facing docs

- Task 1.3: Document color parameter naming conventions
- Task 4.3: Add alignment/layout section to user docs
- Task 5.3: Document error handling principles
- Task 6.3: Update emoji guide

**Deliverables:**

- User docs expanded with conventions and guides
- README or docs site updated (if applicable)

### Phase 3: Optional API Extensions (v0.3.x - near-term)

**Duration:** 2-3 days
**Goal:** Add gradient support to Console.frame() if prioritized

- Task 1.1: Extend Console.frame() for start_color/end_color
- Tests for frame gradients
- Examples demonstrating feature

**Deliverables:**

- Console.frame() supports gradients (optional)
- Test coverage for gradient frames
- Example in gradients_showcase.py

### Phase 4: Advanced Features (v1.0 - future)

**Duration:** 1-2 weeks
**Goal:** Implement text style knobs and preprocessed content API

- Task 2.1-2.4: Region-specific style parameters (title_style, content_style)
- Task 3.1-3.4: Preprocessed content API (console.prepare_content)
- Task 5.1-5.2: Standardize validation behavior

**Deliverables:**

- Console.frame() supports styled titles/content
- Preprocessed content API available
- Gallery examples demonstrate new features
- All tests pass

### Phase 5: Breaking Cleanup (v1.0 - future)

**Duration:** 1 day
**Goal:** Remove deprecated patterns and tighten types

- Deprecate/remove `style`/`colors` on banner
- Tighten `ColorType` to exclude `tuple[str, ...]`
- Migration guide for users

**Deliverables:**

- Deprecated parameters removed
- Migration guide published
- All tests updated

______________________________________________________________________

## Testing Strategy

### Existing Tests

- 654 tests already pass (95.96% coverage)
- Snapshot tests validate visual output
- Unit tests cover core utilities

### New Tests Needed

**For v0.3.x:**

- Gradient frames (if Task 1.1 implemented): snapshot tests for various color combos
- Example execution tests: ensure all gallery files run without errors
- Parameter validation tests: verify error messages for ambiguous cases

**For v1.0:**

- Styled title/content tests: verify Rich Text styling applied correctly
- Preprocessed content tests: validate wrapping, width calculation, emoji safety
- Backward compatibility tests: ensure optional parameters don't break existing code

### Test Commands

```bash
# Run all tests with coverage
uv run pytest --cov=src/styledconsole --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_frame.py -v

# Update snapshots after intentional changes
uv run pytest --snapshot-update

# Run examples (validates UX)
uv run python examples/run_all.py
```

______________________________________________________________________

## Success Metrics

### Quantitative

- [ ] All 4 gallery showcase files execute without errors
- [ ] No linter warnings (ruff) on gallery files
- [ ] Test coverage remains ≥95%
- [ ] All snapshot tests pass
- [ ] Code complexity remains grade A/B (radon)

### Qualitative

- [ ] API naming is predictable and self-documenting
- [ ] Examples serve as clear reference for users
- [ ] User docs explain conventions without over-documenting
- [ ] No "magic" overloading of parameters (border_color, style)
- [ ] Future API extensions follow established patterns from matrices

______________________________________________________________________

## Risks & Mitigations

### Risk 1: Breaking Changes in v0.3.x

**Mitigation:** All v0.3.x work is **additive or example-level only**. No existing public API parameters removed.

### Risk 2: Over-Engineering Documentation

**Mitigation:** Follow DOCUMENTATION_POLICY.md: document decisions, not process. Keep user docs focused on journeys and conventions.

### Risk 3: Feature Creep (v1.0 scope)

**Mitigation:** Stick to planned tasks. Defer nested frames (section 1 of CONSOLE_API_IMPROVEMENTS.md) to v1.1+.

### Risk 4: Rich API Changes

**Mitigation:** StyledConsole facade isolates users from Rich changes. Internal adjustments may be needed but public API stable.

______________________________________________________________________

## References

- **Source Analysis:** `doc/notes/CONSOLE_API_IMPROVEMENTS.md` (7 sections with matrices)
- **Architecture:** `doc/project/PLAN.md` (Rich-native rendering, facade pattern)
- **User Journeys:** `doc/project/SPECIFICATION.md` (what users need to accomplish)
- **Documentation Policy:** `doc/DOCUMENTATION_POLICY.md` (anti-over-engineering)
- **Copilot Instructions:** `.github/copilot-instructions.md` (critical working principles)

______________________________________________________________________

## Next Steps

1. **Review this plan** with project stakeholders (if applicable)
1. **Start Phase 1** (gallery example cleanup) immediately
1. **Commit plan to** `doc/tasks/planned/API_CONSISTENCY_V0.3.x.md`
1. **Track progress** via todo list and git commits
1. **Update status** in this document as phases complete

______________________________________________________________________

**Last Updated:** November 25, 2025
**Author:** Specification-Driven Development Process
**Status:** Ready for Implementation
