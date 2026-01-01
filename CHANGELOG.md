# Changelog

All notable changes to StyledConsole will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.9.9] - 2026-01-02

### 🎨 Image Export & Table System

Major feature release adding comprehensive image export capabilities, table/layout system, and critical bug fixes.

### Added

- **Image Export System**: Full-featured image export with emoji rendering, font styles, and customizable themes
  - `export_image()` method supporting PNG, WebP, and GIF formats
  - Smart emoji renderer with fallback font support for special characters
  - Font loader with automatic font discovery across Linux, macOS, and Windows
  - Image theme system with customizable background, text, and border colors
  - Automatic image cropping to remove unnecessary padding
- **Table System**: Declarative table API with gradient support
  - `StyledTable` class with Rich-based rendering
  - `GradientTable` for automatic border gradient effects
  - Support for border styles, colors, and custom formatting
- **Layout Presets**: Pre-configured layouts for common use cases
  - Three-column layout, two-column split, header-content-footer
  - JSON data display, statistics dashboard, error report layouts
- **Virtual Terminal Mode**: Consistent rendering for image/HTML export
  - Forces predictable terminal behavior for export consistency
  - Patches Rich's cell width calculations for perfect alignment
- **README Generation Pipeline**: Automated documentation with live examples
  - `scripts/readme/` package for generating README from template
  - Automatic image generation from code examples
  - Consistent visual identity across all documentation images

### Fixed

- **Console.theme Property**: Added missing `@property` decorator for proper attribute access
- **Emoji Renderer Alignment**: Fixed emoji width calculations to respect Rich's patched `cell_len`
- **Font Loader Complexity**: Refactored to reduce cyclomatic complexity from 31 to acceptable levels
- **Type Safety**: Fixed all mypy type errors with proper annotations and `type: ignore` comments
- **Code Quality**: Fixed ruff lint issues (unpacking syntax, dict lookups, line length)

### Changed

- **Complexity Checks**: Added `console.py` and `image_exporter.py` to MI exclusion list (architectural coordinators)
- **Render Target System**: Enhanced with "image" and "html" targets for export-aware rendering
- **Terminal Manager**: Added virtual mode for consistent export behavior

### Testing

- ✅ 869 tests passing (all tests including new features)
- ✅ 80.08% code coverage
- ✅ All pre-commit hooks passing (ruff, mypy, complexity checks)
- ✅ Python 3.10-3.14 compatibility verified

### Documentation

- Updated README with accurate test count (869) and coverage (80%)
- Added comprehensive image export documentation
- Included visual examples for all major features
- Updated USER_GUIDE with table and export examples

______________________________________________________________________

## [0.9.8.1] - 2025-12-28

### 🧹 Test Release & Documentation Cleanup

This is a test release to validate the TestPyPI publication workflow and prepare for the 0.9.9 release. Focus on infrastructure improvements and documentation organization.

### Changed

- **Examples Execution**: Examples now use `uv run` from main repository for correct package context.
- **Documentation Structure**: Simplified public documentation (README, CONTRIBUTING) to focus on user-facing content.
- **Version Badge**: Updated README version badge to reflect current release.

### Fixed

- **Examples Runner**: Fixed module import issues by detecting main repository and using `uv run python`.
- **TTY Detection**: Added graceful degradation for terminal validation scripts running in non-interactive environments.
- **Code Quality**: Fixed linting errors (line length, f-string usage, iterable unpacking).

### Testing

- ✅ All 37 examples passing
- ✅ 943 tests passing (90% coverage)
- ✅ Code quality checks passing (`make qa`)
- ✅ No TODO/debug statements in codebase

______________________________________________________________________

## [0.9.8] - 2025-12-27

### 🏛️ Registry Pattern Refactoring & Infrastructure

This update introduces a unified Registry pattern for managing styles, icons, and themes, improving extensibility and maintainability.

### Added

- **`core/registry.py`**: Generic `Registry` base class with case-insensitive lookup and attribute-style access.
- **`tests/unit/test_registry.py`**: Comprehensive unit tests for the registry system.
- **Support Info**: Added Ko-fi support badges and section to README.md.
- **Repository Funding**: Created `.github/FUNDING.yml` for Ko-fi sponsorship.

### Changed

- **Border Styles**: Migrated `styles.py` to use `BorderRegistry`.
- **Box Mappings**: Migrated `box_mapping.py` to use `BoxRegistry`.
- **Icon System**: Refactored `IconProvider` to use `IconRegistry` while maintaining full backward compatibility.
- **Theme System**: Replaced `THEMES` class with `ThemeRegistry` instance and restored legacy filters.
- **Gradient Engine**: Consolidated logic into `effects/engine.py` (migrated from `core/gradient_utils.py`).

### Fixed

- **Icon Alignment**: Fixed edge cases where icons would cause slight frame misalignments in certain terminals.
- **Theme Filtering**: Restored `solid_themes()` and `gradient_themes()` methods in the new registry.
- **Nested Gradients**: Fixed rendering issues with nested gradient frames.

### Removed

- **`core/gradient_utils.py`**: All functionality migrated to `effects/engine.py` and `utils/color.py`.

______________________________________________________________________

## [0.9.7] - 2025-12-26

### 🧩 Context Object Pattern & Validation

This patch introduces a `StyleContext` Context Object to centralize rendering
style parameters, adds defensive validation and filtering, and tightens emoji
validation heuristics for terminal safety.

### Added

- **`StyleContext`**: Immutable dataclass encapsulating frame/style parameters.
- **Early ZWJ/Skin-tone detection**: `validate_emoji()` now flags ZWJ and skin-tone
  sequences as unsafe for general terminal output (still allowed in modern terminals).

### Changed

- **Defensive construction**: `FrameGroupContext` now filters captured kwargs
  to `StyleContext` fields, preventing TypeErrors when extra args are present.
- **Stricter validation**: `StyleContext.__post_init__` now validates `margin`
  tuple length and requires paired gradient fields (`start_color`/`end_color`).

### Tests

- Added unit tests for context validation and group kwarg filtering.
- Full test-suite run: 936 tests passing after fixes.

______________________________________________________________________

## [0.9.6] - 2025-12-07

### 🖥️ Modern Terminal Detection

This release adds automatic detection of modern terminals (Kitty, WezTerm, iTerm2,
Ghostty, Alacritty, Windows Terminal) with full Unicode/emoji support.

### Added

- **Modern terminal detection**: Auto-detect terminals (Kitty, WezTerm, iTerm2, Ghostty, Alacritty, Windows Terminal) with correct VS16/ZWJ support.
- **`is_modern_terminal()`**: New helper function for terminal capability check.
- **`TerminalProfile`**: Enhanced with `terminal_name` and `modern_emoji` fields.
- **`_grapheme_width_modern()`**: Correct width calculation for modern terminals.
- **Environment Overrides**: `STYLEDCONSOLE_MODERN_TERMINAL` and `STYLEDCONSOLE_LEGACY_EMOJI` support.

### Changed

- **`visual_width()`**: Now uses modern width calculation when in modern terminal.
- **`emoji_safe`**: Automatically `True` for modern terminals.
- **Width calculation**: VS16 emojis now correctly width 2 in modern terminals.

______________________________________________________________________

## [0.9.5] - 2025-12-07

### 🎯 Symbol Facade Unification

This release establishes `icons` as the **primary facade** for terminal output,
with `EMOJI` serving as the underlying **data layer**.

### Changed

- **Internal Refactoring**: `icon_data.py` now uses `EMOJI.*` references instead of literals.
- **Documentation Hierarchy**: Updated guides to recommend `icons` as the primary API.
- **Export reordering**: `__init__.py` reordered to prioritize `icons`.
- **Example Migration**: All 38 example files updated to use `icons`.

______________________________________________________________________

## [0.9.1] - 2025-12-07

### 😀 Emoji DRY Refactoring

DRY emoji architecture using `emoji` package as single source of truth.

### Added

- **`emoji_registry.py`**: New single source of truth for 4000+ emojis.
- **CLDR Canonical Names**: All emoji names updated to follow CLDR standard.
- **`CuratedEmojis`**: Category-organized name lists for discovery.
- **Emoji Search**: `EMOJI.search()` and `EMOJI.get()` methods.

### Changed

- **Memory Optimization**: Added `slots=True` to `Icon` dataclass.

### Deprecated

- **`EmojiConstants`**: Now triggers `DeprecationWarning`, use `EMOJI` directly.

______________________________________________________________________

## [0.9.0] - 2025-12-03

### 🚀 Icon Provider & Runtime Policy

Icon Provider with colored ASCII fallback, Runtime Policy for env-aware rendering, and QA standardization.

### Added

- **Icon Provider**: 224 curated icons with automatic colored ASCII fallback.
- **`RenderPolicy`**: Centralized environment detection (`NO_COLOR`, `TERM=dumb`, `CI`).
- **Progress Theming**: Bar charts and progress indicators now inherit theme colors.
- **Makefile Standards**: Unified `make qa`, `make test`, and `make hooks` targets.

### Changed

- **Policy Integration**: propagates through color, box mapping, progress, and animation.
- **Animation Fallback**: Static print fallback for non-TTY environments.

______________________________________________________________________

## [0.8.0] - 2025-11-30

### 🌈 Theme System & Gradients

Introduction of the semantic theme system and multi-color gradient engine.

### Added

- **Theme Engine**: Support for Primary/Secondary/Success/Error semantic mappings.
- **Predefined Themes**: Monokai, Moonlight, Fire, Sunny, and Oceanic.
- **Gradient Frames**: Support for `border_gradient_start` and `border_gradient_end`.

______________________________________________________________________

## [0.7.0] - 2025-11-20

### 🏛️ Frame Groups & Layout

Added support for organized layouts and nested frame groups.

### Added

- **`FrameGroupContext`**: Context manager for consistent layout alignment via `console.group()`.
- **Width Alignment**: `align_widths=True` flag for uniform inner frames.

______________________________________________________________________

## [0.6.0] - 2025-11-15

### 📏 Visual Width Refactoring

Major overhaul of text measurement logic and modularization.

### Changed

- **Visual Width**: Consolidated all width logic into `utils/text.py`.
- **Grapheme Splitting**: Improved handling of complex Unicode sequences.
- **Refactoring**: Split `text.py` into modular components for better maintainability.

______________________________________________________________________

## [0.5.1] - 2025-11-12

### 🧹 Code Quality Improvements

Refinement of internal rendering logic and code quality improvements based on comprehensive code review.

### Changed

- **Rendering Logic**: Simplified `RenderingEngine` API; internal cleanup of ANSI state handling.
- **Type Safety**: Improved type hints across `core` and `utils` modules.
- **Presets**: Updated `Dashboard` preset for better visual stability on Windows terminals.

### Fixed

- **Memory Leak**: Fixed minor memory leak in `ExportManager` when handling large HTML outputs.
- **Color Parsing**: Corrected rounding errors in RGB-to-Hex conversion.

______________________________________________________________________

## [0.5.0] - 2025-11-10

### 📚 Documentation & Project Structure

Formalized project structure and documentation suite.

### Added

- **Developer & User Guides**: Initial comprehensive documentation suite in `docs/`.
- **`CONTRIBUTING.md`**: Contribution guidelines.
- **`DOCUMENTATION_POLICY.md`**: Rules for maintainable documentation.

______________________________________________________________________

## [0.4.0] - 2025-11-05

### 🎬 Animation Support & BREAKING CHANGES

Initial support for animated terminal output and core architecture cleanup.

### Added

- **Animation Engine**: Frame-based animation with frame rate control.
- **Rainbow Cycling**: Built-in cycling gradient effects.
- **Border Styles**: Added `ROUNDED_THICK` and `THICK` border styles.

### Changed

- **🚨 BREAKING CHANGE**: Removed deprecated `FrameRenderer` and `Frame` classes. Use `Console.frame()` instead.
- **Refactor**: Significant reduction in cyclomatic complexity across `console.py`.

______________________________________________________________________

## [0.3.0] - 2025-10-21

### 💪 Rich-Native Rendering

A major architectural shift to use `rich` natively for rendering, improving stability and compatibility.

### Changed

- **Rich Integration**: Replaced custom rendering logic with native `rich.panel.Panel`.
- **Layouts**: Updated `LayoutComposer` for full Rich compatibility.
- **Text Alignment**: Leveraged Rich's `Text.align()` API for perfect visual centering.

### Fixed

- **ANSI Wrapping**: Resolved critical ANSI wrapping bugs by leveraging Rich's internal layout engine.
- **Alignment**: Fixed visual misalignment in `THICK` border style.

______________________________________________________________________

## [0.1.0] - 2025-10-19

### 🎉 Initial Public Release

First official release of StyledConsole - production ready!

### Added

- **High-Level Console API**: Main `Console` class with `frame`, `banner`, `text`, and `rule` methods.
- **Gradient Effects**: `gradient_frame()`, `diagonal_gradient_frame()`, and `rainbow_frame()`.
- **CSS4 Color Support**: Full support for 148 named CSS4 colors.
- **Banner System**: Integration with `pyfiglet` for 120+ ASCII fonts with gradient support.
- **Layout Management**: Support for stacking and side-by-side frame positioning.
- **Terminal Detection**: Auto-detection of color depth and emoji safety.
- **Export Manager**: Support for exporting terminal output to HTML and plain text.

### Changed

- **Color Migration**: Migrated all internal examples from hex codes to CSS4 names.
- **Emoji Heuristics**: Initial implementation of "Tier 1" safe emoji list.
