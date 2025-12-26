# Contributing to StyledConsole

Thank you for your interest in contributing! This guide helps you get started with our development workflow.

## 🚀 Setting Up

We use `uv` for dependency management and `make` to automate common tasks.

### 🛠️ Toolchain Strategy

- **Development**: We exclusively use [uv](https://github.com/astral-sh/uv) for its speed and deterministic resolution. `uv.lock` is our source of truth.
- **End-Users**: We maintain strict compatibility with `pip` and standard wheel installation. No features or build steps should depend on `uv` being present in a user's environment.

### 🛠️ The "One Command" Rule

Do not run complex `pytest` or `ruff` commands manually. Use these standard targets:

- `make setup`: Bootstrap the entire environment.
- `make test`: Run the standard test suite.
- `make qa`: Full Quality Assurance (lint + type-check + coverage).
- `make fix`: Automatically resolve style and lint issues.
- `make hooks`: Run pre-commit checks on staged files.

## 🛠️ Development Workflow

We strictly enforce code quality. Please run these commands before submitting a PR:

### Quality Assurance (QA)

- **Full QA**: Runs linting, formatting check, and coverage.
  ```bash
  make qa
  ```
- **Quick QA**: Runs linting and fast tests (skips slow coverage).
  ```bash
  make qa-quick
  ```

### Code Formatting & Linting

We use `ruff` and `mypy`.

- **Auto-fix Style**:
  ```bash
  make fix
  ```
- **Lint Check**:
  ```bash
  make lint
  ```
- **Type Checking**:
  ```bash
  make type-check
  ```

### Git Hooks

Install pre-commit hooks to catch issues automatically:

```bash
make install-hooks
```

To run hooks manually on staged files:

```bash
make hooks
```

To run hooks on all files:

```bash
make hooks-all
```

## 🌳 Git Workflow

**Goal:** Maintain a clean, atomic history and avoid broken builds.

### 1. The Pre-Commit Habit

Always run `make hooks` (or `make qa-quick`) **before** running `git commit`.

- **Workflow:** `make fix` → `make hooks` → `git add .` → `git commit`.

### 2. Atomic Commits

Avoid "massive" commits that fix 5 different things. Commit logically related changes together. This makes reverts and reviews significantly easier.

### 3. Intentional Pushing

Avoid triggering CI pipelines for every minor local change. Push to remote only when the feature or fix is stable and ready for a PR review.

## 🧪 Testing

Run almost all tests with:

```bash
make test
```

## 🎨 Adding New Features

1. **Themes**: If adding a theme, registered it in `src/styledconsole/core/theme.py`.
1. **Examples**: Add a script in `examples/demos/` if your feature is visual.
1. **Documentation**: Update `docs/USER_GUIDE.md` if you change public APIs.

### 📝 Conventional Commits

We strictly follow [Conventional Commits](https://www.conventionalcommits.org/). This allows for automated versioning and changelog generation.

**Format:** `<type>(<scope>): <description>`

- `feat`: A new feature (e.g., `feat(frame): add gradient support`)
- `fix`: A bug fix (e.g., `fix(emoji): correct width calculation`)
- `docs`: Documentation changes (e.g., `docs: update user guide`)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Maintenance tasks (deps, tools, etc.)

**Example:**

```text
feat(icons): add rocket icon with ascii fallback
docs: update CHANGELOG for v0.9.7 release
```
