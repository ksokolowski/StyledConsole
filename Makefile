# StyledConsole Makefile
# Unified task runner for consistent Developer Experience
# Requires: uv (https://github.com/astral-sh/uv)

.PHONY: help setup test lint lint-fix format format-check qa clean coverage type-check demo

# Configuration
PYTHON := uv run python
PYTEST := uv run pytest
RUF := uv run ruff

# Default target
help:
	@echo "🎨 StyledConsole Developer Tasks"
	@echo "================================"
	@echo "Setup:"
	@echo "  make setup         Install dependencies and dev tools"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run all unit tests"
	@echo "  make coverage      Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Check code style (ruff)"
	@echo "  make lint-fix      Fix code style issues automatically"
	@echo "  make format        Format code (ruff)"
	@echo "  make type-check    Run static type checking (mypy)"
	@echo "  make qa            Run full quality assurance (lint + format + coverage)"
	@echo "  make qa-quick      Run quick quality checks (lint + test)"
	@echo ""
	@echo "Demos:"
	@echo "  make demo          Run all example scripts"
	@echo ""
	@echo "Git Hooks:"
	@echo "  make install-hooks Install pre-commit hooks"
	@echo "  make hooks         Run hooks on staged files"
	@echo "  make hooks-all     Run hooks on ALL files"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean         Remove build artifacts and cache"

# Setup
setup:
	@echo "🚀 Setting up development environment..."
	@uv sync --all-extras
	@echo "✅ Setup complete!"

# Testing
test:
	@echo "🧪 Running unit tests..."
	@$(PYTEST) tests/unit

coverage:
	@echo "📊 Running coverage analysis..."
	@$(PYTEST) tests/unit --cov=styledconsole --cov-report=term-missing --cov-report=html:htmlcov

# Code Quality
lint:
	@echo "🔍 Checking code style..."
	@$(RUF) check src tests examples

lint-fix:
	@echo "🔧 Fixing code style issues..."
	@$(RUF) check --fix src tests examples

format:
	@echo "✨ Formatting code..."
	@$(RUF) format src tests examples

format-check:
	@echo "📝 Checking code formatting..."
	@$(RUF) format --check src tests examples

type-check:
	@echo "types check..."
	@$(PYTHON) -m mypy src/styledconsole || echo "⚠️  Mypy checks failed (non-blocking for now)"

qa: lint format-check coverage
	@echo "✅ QA Pipeline Passed!"

qa-quick: lint test
	@echo "✅ Quick QA Passed!"

# Demos
demo:
	@echo "🎬 Running examples..."
	@$(PYTHON) examples/run_examples.py

# Git Hooks
install-hooks:
	@echo "🪝 Installing git hooks..."
	@uv run pre-commit install

hooks:
	@echo "🪝 Running git hooks on staged files..."
	@uv run pre-commit run

hooks-all:
	@echo "🪝 Running git hooks on ALL files..."
	@uv run pre-commit run --all-files

# Cleanup
clean:
	@echo "🧹 Cleaning artifacts..."
	@rm -rf dist/ build/ *.egg-info .pytest_cache .coverage htmlcov .ruff_cache
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✅ Clean complete!"
