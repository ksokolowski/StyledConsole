# Changelog

All notable changes to StyledConsole will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🔧 Unified Gradient Engine Consolidation

This update consolidates all gradient logic into a single unified engine using the Strategy Pattern.

### Changed

- **Gradient Engine Consolidation**: Removed `core/gradient_utils.py` (614 lines) in favor of unified `effects/engine.py`
- **Rendering Engine**: Now uses `apply_gradient()` from `effects.engine` with strategy pattern
- **Color Utilities**: Added `get_rainbow_color()`, `colorize` alias, and `RAINBOW_COLORS` constant to `utils/color.py`
- **Styles Module**: Added `get_border_chars()` function for efficient border character lookup
- **Nested Gradient Fix**: Fixed rendering issues with nested gradient frames

### Removed

- **`core/gradient_utils.py`**: All functionality migrated to `effects/engine.py` and `utils/color.py`

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
