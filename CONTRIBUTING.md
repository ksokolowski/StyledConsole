# Contributing to StyledConsole

Thank you for your interest in contributing! This guide helps you get started with our development workflow.

## 🚀 Setting Up

We use `make` to automate common tasks. You don't need to memorize complex flags.

```bash
# Install dependencies (creates .venv)
make setup
```

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

## 🧪 Testing

Run almost all tests with:

```bash
make test
```

## 🎨 Adding New Features

1. **Themes**: If adding a theme, registered it in `src/styledconsole/core/theme.py`.
1. **Examples**: Add a script in `examples/demos/` if your feature is visual.
1. **Documentation**: Update `docs/USER_GUIDE.md` if you change public APIs.

## 📝 Code Style

- **Type Hints**: We use `from __future__ import annotations` and strict type hints.
- **Docstrings**: All public classes/functions must have Google-style docstrings.
- **Conventional Commits**: Please use conventional commit messages (e.g., `feat: add fire theme`, `fix: progress bar crash`).
