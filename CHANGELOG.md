# Changelog

All notable changes to StyledConsole will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- **502 tests** across 18 test modules (all passing)
- **93.42% overall coverage** (980/1049 statements)
- **83.42% effects.py coverage** (166/199 statements)
- **36 gradient effect tests** with comprehensive edge cases
- **Zero regressions** after CSS4 migration

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

## [0.1.0] - 2025-10-17

### Added
- Initial project setup with UV package manager
- Core package structure: `styledconsole/{core,utils,presets,export}`
- Test structure: `tests/{unit,integration}`
- Apache 2.0 License
- Basic README and documentation

---

## Release Schedule

- **v0.1.0**: Core functionality (frames, banners, text, layouts)
- **v0.2.0**: Advanced effects (gradients, rainbows)
- **v0.3.0**: Preset functions and dashboards
- **v1.0.0**: Stable release with full documentation

---

[Unreleased]: https://github.com/yourusername/styledconsole/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/styledconsole/releases/tag/v0.1.0
