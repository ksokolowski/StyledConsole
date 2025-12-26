# Python Library Development: Best Practices & Template

Version: 1.0.0
Author: StyledConsole Project Analysis

______________________________________________________________________

## 🏗️ Project Foundation & Setup

### 1. Modern Dependency Management (`uv`)

Use [uv](https://github.com/astral-sh/uv) for lightning-fast, deterministic dependency management.

- **Locking:** Always commit `uv.lock` to ensure identical environments across dev and CI.
- **Syncing:** Use `uv sync --all-extras` for a complete dev environment setup.

### 2. Standardized Configuration (`pyproject.toml`)

Keep all tool configurations in a single `pyproject.toml` file.

- **PEP 621:** Use standard metadata fields.
- **Build Backend:** Use `hatchling` for a robust, standard-compliant build process.
- **Typing:** Include `py.typed` and declare it in `[tool.hatch.build.targets.wheel]`.

### 3. The "One Command" Rule (`Makefile`)

Abstract complex commands into a `Makefile` to maximize Developer Experience (DX). Standard targets should include:

- `make setup`: Bootstrap the environment.
- `make qa`: Run full Quality Assurance (linting, type-checking, tests with coverage).
- `make lint-fix`: Automatically resolve style issues.
- `make demo`: Run example scripts to verify functionality visually.

______________________________________________________________________

## 🏛️ Architecture & Design Patterns

### 1. The Facade Pattern

Expose a single, intuitive entry point (e.g., a `Console` or `Client` class).

- **Hide Complexity:** Subsystems like `RenderingEngine` or `ExportManager` should be internal details.
- **API Surface:** Keep the public API minimal and well-documented in `__init__.py`.

### 2. The Strategy Pattern

Use strategies for interchangeable logic (e.g., gradient types, positioning).

- **Extensibility:** Allows adding new features without modifying core logic.
- **Testability:** Strategies can be tested in isolation.

### 3. Graceful Degradation (Policy-Awareness)

Design for varied environments (CI, legacy terminals, no-color modes).

- **Policy Object:** Centralize environment detection in a `RenderPolicy`.
- **Fallbacks:** Ensure functional, text-only fallbacks for visual features (e.g., ASCII borders for Unicode-incapable terminals).

### 4. Shared Data Layer (DRY Emojis/Icons)

Centralize symbols and constants.

- **Registry:** Use a singleton registry for large datasets (e.g., EMOJI).
- **Mappings:** Map complex symbols to safe ASCII fallbacks with colors.

______________________________________________________________________

## ✨ Code Excellence

### 1. Strict Static Analysis (`ruff`)

Enforce modern Python standards automatically.

- **Rulesets:** Enable `UP` (pyupgrade), `SIM` (simplify), `C4` (comprehensions), and `B` (bugbear).
- **Formatting:** Use `ruff format` for a consistent, Zero-Config style.

### 2. Bulletproof Typing (`mypy`)

Full type hints are mandatory for modern libraries.

- **Future Annotations:** Use `from __future__ import annotations`.
- **Strict Mode:** Aim for `check_untyped_defs = true`.

### 3. Visual Width & Unicode Safety

If your library handles text, respect visual width.

- Use `wcwidth` or custom grapheme-splitting for emoji-heavy layouts.
- Account for VS16 (Variation Selector-16) and ZWJ (Zero Width Joiner) sequences.

______________________________________________________________________

## 📚 Documentation Strategy (The "5-Doc" Rule)

Don't scatter information. Maintain exactly five core documents:

1. **`USER_GUIDE.md`**: Tutorials and high-level API usage with runnable examples.
1. **`DEVELOPER_GUIDE.md`**: Architecture, Mermaid diagrams, and internal module structure.
1. **`PROJECT_STATUS.md`**: The living roadmap, current task list, and metrics.
1. **`CHANGELOG.md`**: Human-readable history of changes (Keep A Changelog format).
1. **`CONTRIBUTING.md`**: Onboarding instructions and PR standards.

### Core Doc Principles:

- **Decision-Based:** Document *why* a choice was made, not just the process.
- **Live Examples:** Every code snippet must be runnable and tested.
- **Visuals:** Use Mermaid diagrams for architecture and sequence flows.
- **Aggressive Archiving:** Move completed analysis/exploration to an `archive/` folder.

______________________________________________________________________

## 🧪 Testing & Verification

### 1. Layered Testing

- **Unit Tests:** High coverage for utility functions and core logic.
- **Integration Tests:** Verify complex interactions (e.g., Rendering + Policy).
- **Visual/Snapshot Testing:** Use `pytest-snapshot` for terminal output to prevent regression in layouts.

### 2. Quality Gates

- **Coverage:** Aim for 90%+. Require `PRAGMA: NO COVER` only for unreachable/environment-specific code.
- **Pre-Commit:** Use `pre-commit` hooks to run fast checks locally before pushing.

______________________________________________________________________

## 🚀 Developer Onboarding

- **Quick Start:** Provide a "One Minute" example in `README.md`.
- **Visual Gallery:** Create an `examples/gallery/` folder where scripts produce instant, impressive results.
- **Functional Demos:** Use `examples/usecases/` to show the library solving real-world problems.
