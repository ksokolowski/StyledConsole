# Examples Catalog Redesign Plan

**Date:** November 11, 2025
**Version:** v0.3.0
**Status:** Planning Phase

---

## 🎯 Vision

Transform StyledConsole examples from scattered demonstrations into a **curated visual catalog** that:
1. **Showcases real-world use cases** (not toy examples)
2. **Demonstrates best practices** with visually appealing designs
3. **Reveals patterns** that justify high-level convenience APIs
4. **Inspires developers** with beautiful terminal UI possibilities

---

## 📊 Current State Analysis

### Existing Examples Audit

#### `/examples/basic/` (10 files)
- **01_simple_frame.py** - Basic frame rendering (too simple)
- **02_emoji_support.py** - Emoji alignment demo (technical, not visual)
- **03_alignments.py** - Left/center/right alignment (basic)
- **04_border_styles.py** - Shows all 8 borders (reference, not use case)
- **05_console_frames.py** - Console API demo (redundant with 01)
- **06_banner_renderer.py** - Banner basics (superseded by 08)
- **07_rich_layouts.py** - Direct Rich API usage (advanced, confusing)
- **08_console_api.py** - Console.banner() demo (good!)
- **09_emoji_validation.py** - Emoji safety check (technical)
- **09_variable_content.py** - Dynamic content (duplicate naming!)
- **10_color_system.py** - CSS4 colors reference (good)

**Assessment:** Too many "hello world" examples. Need use-case driven approach.

#### `/examples/showcase/` (7 files)
- **banner_showcase.py** ✅ - Great visual demo of banners
- **cicd_dashboard.py** ✅ - Excellent real-world use case (414 lines)
- **digital_poetry.py** ✅ - Creative use case
- **gradient_effects.py** ✅ - Beautiful gradient catalog (387 lines)
- **rainbow_fat_alignment.py** - Specific rainbow alignment test
- **02_nested_multiframe.py** - Multi-frame layouts
- **ADVANCED_DASHBOARD.md** - Documentation, not example

**Assessment:** Best examples are here. These inspire! cicd_dashboard & gradient_effects are gold.

#### `/examples/gallery/` (1 file)
- **border_gallery.py** - All border styles showcase

**Assessment:** Good reference, but overlaps with basic/04.

#### `/examples/testing/` (11 files)
- All technical validation/diagnostic scripts
- Not user-facing examples

**Assessment:** Keep in testing/, not part of example catalog.

#### `/examples/prototype/` (2 markdown files)
- Planning documents, not examples

---

## 🎨 Proposed New Structure

### Vision: Use-Case Driven + Visual Gallery

```
examples/
├── README.md                          # Catalog index with screenshots
├── run_all.py                         # Run all examples (updated)
│
├── usecases/                          # Real-world scenarios
│   ├── README.md                      # Use case catalog
│   ├── alerts.py                      # ✨ Success/error/warning alerts
│   ├── notifications.py               # ✨ System notifications
│   ├── progress_dashboard.py          # ✨ Build/deploy progress
│   ├── status_panels.py               # ✨ Service health monitoring
│   ├── cli_menus.py                   # ✨ Interactive menu interfaces
│   ├── data_tables.py                 # ✨ Formatted data display
│   ├── logs_viewer.py                 # ✨ Log output formatting
│   └── welcome_screens.py             # ✨ Application launch screens
│
├── gallery/                           # Visual showcases
│   ├── README.md                      # Gallery index
│   ├── borders_showcase.py            # All border styles (visual)
│   ├── colors_showcase.py             # CSS4 color palette demo
│   ├── gradients_showcase.py          # Gradient effects catalog
│   ├── emojis_showcase.py             # Emoji-rich designs
│   └── banners_showcase.py            # ASCII art banners
│
├── recipes/                           # ✨ NEW: Common patterns
│   ├── README.md                      # Recipe book index
│   ├── multi_column_layout.py         # Side-by-side panels
│   ├── nested_frames.py               # Frames within frames
│   ├── animated_progress.py           # Progress indicators
│   └── custom_themes.py               # Color scheme patterns
│
├── legacy/                            # Archived examples (reference)
│   ├── README.md                      # "Old examples - kept for reference"
│   ├── basic/                         # Moved from examples/basic/
│   ├── showcase/                      # Moved from examples/showcase/
│   └── gallery/                       # Moved from examples/gallery/
│
└── testing/                           # Keep as-is (not user-facing)
```

---

## 🚀 High-Level API Opportunities

### Patterns Identified from Existing Examples

Based on `cicd_dashboard.py`, `banner_showcase.py`, and common use cases:

#### 1. **Alerts & Notifications**

**Pattern observed:** Repetitive success/error/warning messages with:
- Specific emojis (✅ ❌ ⚠️)
- Color conventions (green=success, red=error, yellow=warning)
- Consistent styling

**Proposed API:**
```python
console.alert(
    "Deployment successful!",
    type="success",  # success|error|warning|info
    title="✅ Success",
    width=60
)
# Renders: Green gradient frame, success emoji, appropriate styling
```

#### 2. **Status Panels**

**Pattern observed:** Service health, build status panels with:
- Title + status indicator
- Color-coded content
- Emojis for quick scanning

**Proposed API:**
```python
console.status_panel(
    title="Database Connection",
    status="healthy",  # healthy|degraded|down
    details="PostgreSQL 15.3 • 42 connections",
    width=40
)
# Renders: Green border + ✅ for healthy, red + ❌ for down
```

#### 3. **Progress Dashboards**

**Pattern observed:** CI/CD pipelines, build steps with:
- Step name + status
- Progress indicators
- Time/duration display

**Proposed API:**
```python
console.progress_dashboard(
    title="🚀 Deployment Pipeline",
    steps=[
        {"name": "Build", "status": "complete", "duration": "2m 34s"},
        {"name": "Test", "status": "running", "progress": 67},
        {"name": "Deploy", "status": "pending"},
    ],
    width=80
)
```

#### 4. **CLI Menus**

**Pattern observed:** Selection menus with:
- Numbered options
- Emojis for visual grouping
- Highlighted selection

**Proposed API:**
```python
console.menu(
    title="Main Menu",
    options=[
        "🚀 Deploy Application",
        "📊 View Metrics",
        "⚙️  Settings",
        "🚪 Exit"
    ],
    selected=0,  # Highlight first option
    width=50
)
```

#### 5. **Data Tables**

**Pattern observed:** Key-value pairs, metrics display:
- Aligned columns
- Color-coded values
- Header styling

**Proposed API:**
```python
console.data_table(
    title="System Metrics",
    headers=["Metric", "Value", "Status"],
    rows=[
        ["CPU Usage", "45%", "✅ Normal"],
        ["Memory", "12.5 GB", "⚠️  High"],
        ["Disk I/O", "523 MB/s", "✅ Normal"],
    ],
    align=["left", "right", "center"],
    width=60
)
```

---

## 📋 Implementation Phases

### Phase 1: Archive & Audit ✅ (Immediate)
- [ ] Create `examples/legacy/` structure
- [ ] Move existing `basic/`, `showcase/`, `gallery/` → `legacy/`
- [ ] Keep `testing/` as-is (developer tools)
- [ ] Document in `legacy/README.md`: "Reference material, may have redundancy"

### Phase 2: Use Cases Catalog (Priority)
- [ ] Create `examples/usecases/` with 8 use-case examples
- [ ] Each example must be:
  - ✅ Visually appealing (no "Hello World")
  - ✅ Real-world scenario
  - ✅ Self-contained (runnable without dependencies)
  - ✅ Well-commented with "Why" not just "How"
- [ ] Examples to create:
  1. `alerts.py` - Success/error/warning messages
  2. `notifications.py` - System notifications
  3. `progress_dashboard.py` - Build/deploy progress
  4. `status_panels.py` - Service monitoring
  5. `cli_menus.py` - Interactive menus
  6. `data_tables.py` - Metrics display
  7. `logs_viewer.py` - Log formatting
  8. `welcome_screens.py` - App launch screens

### Phase 3: Visual Gallery (Quick Wins)
- [ ] Consolidate best visual showcases:
  - `borders_showcase.py` ← from legacy/gallery/border_gallery.py
  - `colors_showcase.py` ← from legacy/basic/10_color_system.py
  - `gradients_showcase.py` ← from legacy/showcase/gradient_effects.py
  - `banners_showcase.py` ← from legacy/showcase/banner_showcase.py
  - `emojis_showcase.py` ← NEW (Tier 1 emoji catalog)

### Phase 4: High-Level API Design
- [ ] Create `doc/project/HIGH_LEVEL_API.md` specification
- [ ] For each proposed API:
  - Function signature
  - Parameters with defaults
  - Behavior specification
  - Visual design rules (colors, emojis, borders)
  - Example usage
- [ ] Review against use case examples (do they simplify?)

### Phase 5: High-Level API Implementation (Future)
- [ ] Create `src/styledconsole/presets.py` (or similar)
- [ ] Implement functions:
  - `alert()`
  - `status_panel()`
  - `progress_dashboard()`
  - `menu()`
  - `data_table()`
- [ ] Add tests in `tests/unit/test_presets.py`
- [ ] Update use case examples to show both:
  - "Using low-level API" (current)
  - "Using high-level API" (new convenience functions)

### Phase 6: Documentation & Polish
- [ ] Update main `README.md` with link to examples catalog
- [ ] Add screenshots to `examples/README.md`
- [ ] Create visual index (maybe ASCII art grid?)
- [ ] Update `run_all.py` to run only `usecases/` + `gallery/`

---

## 🎯 Success Criteria

### Examples Quality
- ✅ **No toy examples** - Every example solves a real problem
- ✅ **Visually stunning** - Users say "I want that in my CLI!"
- ✅ **Copy-pasteable** - Developers can adapt directly
- ✅ **Well-documented** - Comments explain design decisions

### High-Level API Validation
- ✅ **Reduces boilerplate** - Compare before/after for common tasks
- ✅ **Intuitive naming** - Function names match intent
- ✅ **Consistent conventions** - Colors, emojis, borders follow patterns
- ✅ **Justified by use cases** - Every function has 3+ examples using it

### Catalog Organization
- ✅ **Easy navigation** - Find example for use case in < 30 seconds
- ✅ **Clear separation** - Use cases vs visual gallery vs recipes
- ✅ **Maintainable** - Adding new example is straightforward

---

## 💡 Creative Extensions

### Potential Additional Use Cases
1. **Configuration Wizard** - Step-by-step setup with frames
2. **Error Reports** - Beautiful stack traces / error formatting
3. **CLI Dashboard** - Live updating status (using Rich Live)
4. **Git-style Output** - Commit messages, diffs with styling
5. **Package Manager UI** - Install progress, dependency trees
6. **Test Results** - Pytest-style test summary with colors
7. **API Response Viewer** - JSON/XML formatted display
8. **File Browser** - Directory tree with icons

### Inspiration Sources
- **Rich library examples** - See what resonates
- **GitHub CLI** (`gh`) - Clean, emoji-rich output
- **Modern CLIs** - Docker, npm, cargo output styles
- **Terminal dashboards** - htop, btop++ aesthetics

---

## 🚧 Migration Strategy

### For Users
- ✅ **No breaking changes** - All examples stay runnable
- ✅ **Legacy remains** - Old examples in `legacy/` with deprecation notice
- ✅ **Smooth transition** - New catalog points to legacy for deprecated patterns

### For Contributors
- ✅ **Clear guidelines** - Template for new examples
- ✅ **Review checklist** - Quality bar for accepting examples
- ✅ **Testing required** - All examples run in CI via `test_examples.py`

---

## 📝 Next Steps

1. **Get feedback** on this plan (validate vision alignment)
2. **Execute Phase 1** - Archive existing examples to `legacy/`
3. **Create 1-2 use case examples** - Validate approach (e.g., `alerts.py`)
4. **Review & iterate** - Adjust plan based on learnings
5. **Continue Phases 2-3** - Build out catalog
6. **Design high-level API** - Once patterns are clear (Phase 4)

---

## 📖 References

- **DOCUMENTATION_POLICY.md** - "Less is More" principle applies to examples too
- **Existing showcase examples** - `cicd_dashboard.py`, `gradient_effects.py` (gold standard)
- **Rich library** - Inspiration for beautiful terminal output
- **User feedback** - What do users try to build first?

---

**Bottom line:** Transform examples from "feature demos" to "solution templates". Users should leave inspired and equipped to build beautiful CLIs.
