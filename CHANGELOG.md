# Changelog

All notable changes to StyledConsole will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2025-11-30

### 🛠️ Code Refactoring

This release focuses on improving code maintainability through refactoring of `text.py`.

### Changed

#### text.py Refactoring

- **Extracted `emoji_data.py`**: Moved `SAFE_EMOJIS` dictionary (~1200 lines) to dedicated `utils/emoji_data.py` module. Reduces `text.py` from 2048 to 815 lines (60% reduction).
- **Refactored `visual_width()`**: Extracted helper functions `_grapheme_width_legacy()` and `_grapheme_width_standard()`. Cyclomatic complexity reduced from 16 (grade C) to 8 (grade B).
- **Refactored `split_graphemes()`**: Extracted helper functions `_parse_ansi_sequence()` and `_should_extend_grapheme()`. Cyclomatic complexity reduced from 16 (grade C) to 10 (grade B).
- **Improved maintainability**: Average cyclomatic complexity improved from 5.72 to 4.78. Maintainability index improved from 34.13 to 37.47.

### Added

- **New module `utils/emoji_data.py`**: Contains `SAFE_EMOJIS`, `TIER1_EMOJI_RANGES`, and `VARIATION_SELECTOR_16` constants with MI score of 100.

### Backward Compatibility

- All existing imports continue to work unchanged
- `SAFE_EMOJIS` remains accessible from both `styledconsole` and `styledconsole.utils.text`

______________________________________________________________________

## [0.5.1] - 2025-11-30

### 🔧 Code Quality Improvements

This patch release addresses issues identified during comprehensive code review.

### Fixed

- **Duplicate `__all__` entries**: Removed duplicate `prepare_frame_content` and `auto_size_content` entries from `__init__.py`
- **Consistent exception types**: `get_border_style()` now raises `ValueError` instead of `KeyError` for unknown border styles, matching `box_mapping.get_box_style()` for consistency
- **Specific exception handling**: Replaced bare `except Exception` with specific `MarkupError` catches in `text.py` markup parsing to avoid hiding real bugs

### Changed

- **Dashboard refactored to use Console API**: `dashboard()` preset now uses `Console.frame()` and `Console.render_frame()` instead of directly importing Rich's `Panel`. This maintains architectural consistency with the facade pattern where Console is the public API and Rich is the backend infrastructure.
- **Improved color cache efficiency**: `parse_color()` now normalizes input (lowercase, strip whitespace) before caching, so `"RED"`, `"red"`, and `" red "` all hit the same cache entry
- **Pre-compiled regex pattern**: VS16 emoji HTML wrapping regex in `export_manager.py` moved to module level for better performance
- **Added missing type hints**: Added return type hints to private methods in `rendering_engine.py` (`_build_content_renderable`, `_get_figlet`) and parameter/return types in `gradient_utils.py` (`get_border_chars`, `apply_diagonal_gradient`, `apply_diagonal_rainbow`, `_colorize_line_with_ansi`)

### Removed

- **Legacy code cleanup**: Removed unused `_render_frame_legacy()` method from `RenderingEngine` (~100 lines). This legacy Rich Panel fallback was kept for reference but never called.

______________________________________________________________________

## [0.5.0] - 2025-11-30

### 📚 Documentation & Project Structure

This release focuses on documentation consolidation, project cleanup, and improved developer experience.

### Changed

#### Documentation Consolidation

- **4 Master Documents**: Consolidated 27+ scattered docs into clean structure:
  - `docs/USER_GUIDE.md` - Complete user documentation with Presets section
  - `docs/DEVELOPER_GUIDE.md` - Architecture and contribution guide
  - `docs/PROJECT_STATUS.md` - Current status and metrics
  - `docs/DOCUMENTATION_POLICY.md` - Standards and rules
- **Folder Rename**: Renamed `doc/` to `docs/` for consistency

#### Examples Reorganization

- **4 Categories**: Reorganized 27 examples into logical folders:
  - `gallery/` - Visual showcases (colors, borders, emojis, gradients)
  - `usecases/` - Real-world scenarios (alerts, progress, reports)
  - `demos/` - Feature demonstrations (animation, nested frames)
  - `validation/` - Testing and validation scripts
- **Unified Runner**: Single `run_examples.py` with `--all` and `--auto` flags
- **Standardized Naming**: Removed prefixes (`demo_`, `test_`, `_showcase`)

#### Gallery Improvements

- **Emoji Standardization**: All gallery examples now use `EMOJI` constants
- **Console API Only**: Examples use public API, not internal Rich access

### Removed

- **Root Cleanup**: Deleted 24 exploratory test files from project root
- **Empty Folders**: Removed unused `recipes/` folder
- **Redundant Runners**: Removed duplicate `test_examples.py`

______________________________________________________________________

## [0.4.0] - 2025-11-23

### 🚀 Animated Gradients & Unified Engine

This release introduces dynamic, animated gradients, a completely refactored gradient engine, and significant improvements to the emoji and example systems.

### Added

#### Animated Gradients & Engine

- **Animation Class**: New `Animation` class for handling render loops, cursor management, and FPS control.
- **OffsetPositionStrategy**: New strategy that allows gradients to be shifted dynamically, enabling cycling animations.
- **Unified Gradient Engine**: Replaced hardcoded gradient functions with a modular Strategy pattern (`PositionStrategy`, `ColorSource`, `TargetFilter`).
- **New Documentation**: Added `ANIMATED_GRADIENTS.md` guide and `GRADIENT_ENGINE.md` reference.

#### Emojis & Assets

- **Tier 1 Emojis**: Added 20+ new Tier 1 emoji constants (Nov 12).
- **Emoji Constants**: Added `SIREN`, `TRIANGLE_RULER`, `GLOBE` and file/document emojis (Nov 11).
- **Reference**: Added emoji constants reference documentation.

#### Examples

- **Use Cases**: Added 6 comprehensive use case examples (Nov 11).
- **Demo**: New `examples/demo_animation.py` showcasing the animated rainbow effect.

### Changed

- **Breaking Change**: Removed deprecated `FrameRenderer` and `Frame` classes (Nov 02).
- **Border Styles**: Improved `ROUNDED_THICK` border style with quadrant block characters (Nov 11).
- **Refactor**: Reduced cyclomatic complexity across codebase (Nov 11).
- **Documentation**: Comprehensive update to project documentation and policy.

### Fixed

- **Animation Glitch**: Fixed off-by-one error in animation cursor clearing.
- **Diagonal Alignment**: Fixed test failure related to centered frame alignment.

______________________________________________________________________

## [0.3.0] - 2025-10-21

### 🏗️ Rich-Native Migration

A major architectural shift to use `rich` natively for rendering, improving stability and compatibility.

### Changed

- **Rich Integration**: Replaced custom `FrameRenderer` with native `rich.panel.Panel`.
- **Layouts**: Updated `LayoutComposer` for full Rich compatibility.
- **Text Alignment**: Fixed decorative box headers/footers and ANSI wrapping bugs using Rich's `Text.align()` API.

### Fixed

- **ANSI Wrapping**: Resolved critical ANSI wrapping bugs by leveraging Rich's layout engine.
- **Alignment**: Fixed visual illusions in `THICK` style and empty string title handling.

______________________________________________________________________

## [0.1.0] - 2025-10-19

### 🎉 Initial Public Release

First official release of StyledConsole - production ready!

### Added

#### Gradient & Rainbow Effects (2025-10-19)

- **Gradient Effects System**: Three powerful gradient functions for stunning visual output
  - `gradient_frame()`: Vertical gradients with custom start/end colors
  - `diagonal_gradient_frame()`: Diagonal gradients (top-left to bottom-right)
  - `rainbow_frame()`: Full ROYGBIV rainbow spectrum with vertical/diagonal direction
- **Rainbow Direction Control**: Added `direction` parameter ("vertical" or "diagonal") to `rainbow_frame()`
- **CSS4 Color Support**: Full support for 148 CSS4 color names throughout the library
  - Human-readable color names like "red", "lime", "blue" instead of hex codes
  - Backward compatible with hex codes and RGB tuples
  - Consistent color naming across all examples and tests
- **ROYGBIV Rainbow**: Proper 7-color rainbow interpolation (Red, Orange, Yellow, Green, Blue, Indigo, Violet)
  - Fixed rainbow to cycle through all 7 spectrum colors instead of simple red-violet gradient
  - Uses CSS4 colors: red, orange, yellow, lime, blue, indigo, darkviolet
- **Emoji Guidelines**: Comprehensive documentation of 100+ tested safe emojis
  - `doc/EMOJI_GUIDELINES.md` with categorized emoji lists
  - Variation selector warnings and safe alternatives
  - Best practices for emoji usage in terminal output

#### Core Features (2025-10-17 to 2025-10-18)

- **High-Level Console API**: Main `Console` class with frame, banner, text, rule methods
- **Frame Rendering System**: Beautiful bordered frames with 8 border styles
  - Border styles: solid, double, rounded, heavy, thick, ascii, minimal, dots
  - Auto-width calculation and emoji-safe rendering
  - Color support for content, borders, and titles
  - Gradient effects integration
- **Banner Rendering**: Large ASCII art text with 120+ fonts via pyfiglet
  - Gradient support for banners
  - Border frames for banners
  - Width and alignment controls
- **Layout System**: Stack, side-by-side, and grid layouts for complex compositions
- **Text Utilities**: ANSI-aware text processing
  - Visual width calculation (emoji-safe)
  - Text wrapping and truncation
  - ANSI code stripping
- **Color System**: Advanced color parsing and manipulation
  - CSS4 color names (148 colors)
  - Hex color codes (#RRGGBB, #RGB)
  - RGB tuples (r, g, b)
  - Color interpolation for gradients
  - Color distance calculation
- **Terminal Detection**: Auto-detect terminal capabilities
  - Color depth detection (truecolor, 256-color, basic, none)
  - Emoji safety detection
  - Terminal size detection
- **Export System**: Save console output to HTML or plain text
  - HTML export with optional inline styles
  - ANSI-to-HTML conversion
  - Plain text export with ANSI codes stripped

### Changed

#### CSS4 Color Migration (2025-10-19)

- **Migrated all examples to CSS4 color names** (27 files updated)
  - `examples/basic/08_console_api.py`: 5 color replacements
  - `examples/basic/06_banner_renderer.py`: 6 color replacements
  - `examples/showcase/banner_showcase.py`: 3 color replacements
  - `examples/showcase/cicd_dashboard.py`: 7 color replacements
  - `examples/prototype/rainbow_gradient_prototype.py`: Updated RAINBOW_COLORS
- **Updated all test files to CSS4 colors** (20+ replacements)
  - `tests/unit/test_frame_colors.py`: All color tests
  - `tests/unit/test_console.py`: Color test cases
  - `tests/integration/test_console_integration.py`: Integration tests
  - `tests/test_effects.py`: Gradient tests
- **Updated documentation examples** to use CSS4 color names
  - `src/styledconsole/console.py`: Docstring examples
  - `src/styledconsole/core/banner.py`: Docstring examples
- **Improved code readability**: Color names are self-documenting (e.g., "red" instead of "#ff0000")

#### Bug Fixes (2025-10-19)

- **Fixed content gradient coloring borders**: Content gradients no longer affect border colors
- **Fixed emoji alignment**: Resolved variation selector issues causing misalignment
- **Fixed border coloring in "both" mode**: Vertical borders now properly colored when target="both"
- **Fixed rainbow color spectrum**: Now displays full ROYGBIV instead of red-purple gradient

### Technical Details

#### Test Coverage (2025-10-19)

- **612 tests** across all test modules (100% passing)
- **96.30% overall coverage** (1066/1107 statements)
- **100% coverage** on all manager classes (TerminalManager, ExportManager, RenderingEngine)
- **83.42% effects.py coverage** (166/199 statements)
- **Zero regressions** - all examples working perfectly

#### Refactoring Complete (Phase 4)

- **Console refactored to Facade pattern** (609 lines → 54 statements, 91% reduction)
- **TerminalManager created** (41 statements, 97.56% coverage)
- **ExportManager created** (38 statements, 100% coverage)
- **RenderingEngine created** (81 statements, 100% coverage)
- **63 new tests added** for manager classes
- **Clean architecture** with Single Responsibility Principle
- **Full documentation** with research validation

#### Color Mappings

Common hex-to-CSS4 conversions:

- `#ff0000` → `red`
- `#00ff00` → `lime` (bright green)
- `#0000ff` → `blue`
- `#00ffff` → `cyan`
- `#ff00ff` → `magenta`
- `#ffff00` → `yellow`
- `#ffffff` → `white`
- `#00aa00` → `darkgreen`
- `#aa0000` → `darkred`
- `#ffaa00` → `orange`
- `#ff6600` → `orangered`
- `#9400d3` → `darkviolet`
- `#4b0082` → `indigo`

### Quality Metrics

- **Tests**: 612 passing (100% success rate)
- **Coverage**: 96.30% overall
- **Python**: 3.10, 3.11, 3.12, 3.13
- **Zero known bugs**
- **Production ready** ✅

### Known Limitations

- Tier 2/3 emoji (skin tones, ZWJ sequences) not yet supported
- Horizontal gradients not implemented (only vertical and diagonal)

### Future Plans (v0.2.0)

- Additional border styles
- Theme presets
- Animation support
- Enhanced emoji support (Tier 2/3)
- Horizontal gradients

______________________________________________________________________

## Release Schedule

- **v0.1.0**: Core functionality (frames, banners, text, layouts)
- **v0.2.0**: Advanced effects (gradients, rainbows)
- **v0.3.0**: Preset functions and dashboards
- **v1.0.0**: Stable release with full documentation

______________________________________________________________________

[0.1.0]: https://github.com/yourusername/styledconsole/releases/tag/v0.1.0
