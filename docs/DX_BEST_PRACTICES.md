# Developer Experience (DX) Best Practices

This document synthesizes the best practices observed in both `styledconsole` and `robotframework-suds`. It serves as a unified standard for Python project development, aiming to maximize developer efficiency, code quality, and maintainability.

## 1. Project Automation (The "One Command" Rule)

**Goal:** Reduce cognitive load by abstracting complex commands into simple, memorable targets.

- **Tool:** `Makefile` (or `Justfile`)
- **Best Practice (Shared):**
  - Do not require developers to memorize flags for `pytest`, `ruff`, or `uv`.
  - Provide standard targets:
    - `make setup`: Install dependencies (handling venv/uv automatically).
    - `make test`: Run standard test suite.
    - `make lint` / `make fix`: Check and auto-fix code style.
    - `make qa`: Run full quality assurance (lint + coverage + formatting).
    - `make qa-quick`: Run quick checks (lint + fast tests).
    - `make hooks`: Run pre-commit hooks on staged files.
    - `make hooks-all`: Run pre-commit hooks on all files.
  - **Anti-Pattern:** Documenting "Run `uv run pytest --cov=...`" in README instructions.

## 2. Code Quality & Static Analysis

**Goal:** Catch bugs early and enforce consistency without human code review effort.

- **Tool:** `ruff`

- **Best Practice (Shared):**

  - **Strict Rules:** Enable modern rulesets in `pyproject.toml`:
    - `UP` (pyupgrade): Enforce modern Python syntax (e.g., `list[str]` over `List[str]`).
    - `SIM` (flake8-simplify): Simplify complex logic.
    - `C4` (flake8-comprehensions): Optimize list/dict comprehensions.
  - **Auto-Fix:** configure linting tasks to automatically fix trivial issues (`ruff check --fix`).

- **Tool:** `mypy` / `pyright`

- **Best Practice (from `styledconsole`):**

  - **Strict Typing:** Use `from __future__ import annotations` and full type hints.
  - **Library Marker:** Include an empty `py.typed` file in the package root to allow consumers to use your type hints.

## 3. Architecture & API Design

**Goal:** Make the library intuitive to use and easy to extend.

- **Pattern:** The Facade Pattern

- **Best Practice (from `styledconsole`):**

  - **Single Entry Point:** Expose a single high-level class (e.g., `Console`) that wraps complex subsystems.
  - **Hiding Complexity:** Users shouldn't need to import internal utility classes (`GradientEngine`, `BorderMapper`) to do basic tasks.

- **Feature:** Runtime degradation (Graceful Failure)

- **Best Practice (from `styledconsole`):**

  - **Policy-Awareness:** Centralize environment detection (CI, No-Color, Legacy Terminal) in a `Policy` object.
  - **Fallbacks:** Ensure every fancy feature (Emoji, Color, Animation) has a functional, readable text-only fallback.

## 4. Documentation Strategy

**Goal:** documentation should answer "What?", "How?", and "Why?".

- **Artifacts (from `styledconsole`):**
  - `CONTRIBUTING.md`: Entry point for new developers.
  - `USER_GUIDE.md`: For end-users. Tutorials and API usage.
  - `DEVELOPER_GUIDE.md`: For contributors. Contains **Architecture Diagrams** (Mermaid), sequence flows, and file structure explanation.
  - `PROJECT_STATUS.md`: High-level roadmap and current version goals.
  - `CHANGELOG.md`: Human-readable history of changes (Keep A Changelog format).

## 5. Developer Onboarding

**Goal:** Enable a new developer to understand the library's capabilities quickly.

- **Visual Libraries (e.g., `styledconsole`):**

  - **Structure:** `examples/gallery/` scripts.
  - **Why:** Visual feedback is instant.

- **Functional/Test Libraries (e.g., `robotframework-suds`):**

  - **Structure:** Acceptance Tests (ATDD).
  - **Why:** Executable specifications (`.robot` files) demonstrate exactly how keywords are used in real scenarios.
  - **Best Practice:** Ensure tests are readable and serve as documentation.

## 6. Dependency Management

**Goal:** Fast, deterministic builds.

- **Tool:** `uv`
- **Best Practice (Shared):**
  - **Lockfiles:** Commit `uv.lock` or `pdm.lock` to ensure CI runs exactly what developers run.
  - **Dev Dependencies:** explicit `[project.optional-dependencies] dev = [...]` in `pyproject.toml`.

## 7. Git Workflow & Best Practices

**Goal:** Maintain a clean history and avoid frustration with CI/pre-commit failures.

- **Best Practice (Shared):**
  - **Pre-Commit Strategy:**
    - Always run `make hooks` (or `make qa-quick`) *before* running `git commit`.
    - **Workflow:** `make hooks` -> `git add .` -> `git commit`.
  - **Intentional Commits:**
    - **Anti-Pattern:** Auto-committing and pushing every local file save or minor change.
    - **Best Practice:** Commit logically related changes ("Atomic Commits").
    - **Pushing:** Push to remote only when the feature/fix is stable or ready for backup. Avoid triggering CI pipelines for micro-changes.
  - **Conventional Commits:**
    - Use structured messages: `feat: add fire theme`, `fix: resolve crash`, `docs: update readme`.
    - This allows automated changelog generation and version bumping.

## Summary of Recommendations

| Feature          | StyledConsole     | RobotFramework-Suds     | Recommendation to Both      |
| :--------------- | :---------------- | :---------------------- | :-------------------------- |
| **Automation**   | ✅ `Makefile`     | ✅ `Makefile`           | Adopt `Makefile` standard   |
| **Linting**      | ✅ Strict         | ✅ Strict (`UP`, `SIM`) | Adopt Strict `ruff` rules   |
| **Docs**         | ✅ Comprehensive  | ⚠️ Basic                | Create `DEVELOPER_GUIDE.md` |
| **Architecture** | ✅ Facade, Policy | ✅ Wrapped Facade       | Use Facade for public API   |
| **Onboarding**   | ✅ Visual Gallery | ✅ Acceptance Tests     | Maintain Executable Docs    |
| **Typing**       | ✅ `py.typed`     | ❌ Missing `py.typed`   | Add `py.typed`              |
