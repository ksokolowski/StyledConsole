# StyledConsole Makefile
# Unified task runner for consistent Developer Experience
# Requires: uv (https://github.com/astral-sh/uv)

.PHONY: help setup test lint lint-fix format format-check qa clean coverage type-check demo

# Windows compatibility: use PowerShell and .venv paths
ifeq ($(OS),Windows_NT)
    SHELL := powershell.exe
    .SHELLFLAGS := -NoProfile -Command
    UV := .\.venv\Scripts\uv.exe
    PYTHON := $(UV) run python
    PYTEST := $(UV) run pytest
    RUF := $(UV) run ruff
    RM_RF := Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    FIND_PYCACHE := Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
else
    UV := uv
    PYTHON := $(UV) run python
    PYTEST := $(UV) run pytest
    RUF := $(UV) run ruff
    RM_RF := rm -rf
    FIND_PYCACHE := find . -type d -name "__pycache__" -exec rm -rf {} +
endif

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
	@echo "Setting up development environment..."
	$(UV) sync --all-extras
	@echo "Setup complete!"

# Testing
test:
	@echo "Running unit tests..."
	$(PYTEST) tests/unit

coverage:
	@echo "Running coverage analysis..."
	$(PYTEST) tests/unit --cov=styledconsole --cov-report=term-missing --cov-report=html:htmlcov

# Code Quality
lint:
	@echo "Checking code style..."
	$(RUF) check src tests examples

lint-fix:
	@echo "Fixing code style issues..."
	$(RUF) check --fix src tests examples

format:
	@echo "Formatting code..."
	$(RUF) format src tests examples

format-check:
	@echo "Checking code formatting..."
	$(RUF) format --check src tests examples

type-check:
	@echo "Running type check..."
	$(PYTHON) -m mypy src/styledconsole

qa: lint format-check coverage
	@echo "QA Pipeline Passed!"

qa-quick: lint test
	@echo "Quick QA Passed!"

# Demos
demo:
	@echo "Running examples..."
	$(PYTHON) examples/run_examples.py

# Git Hooks
install-hooks:
	@echo "Installing git hooks..."
	$(UV) run pre-commit install

hooks:
	@echo "Running git hooks on staged files..."
	$(UV) run pre-commit run

hooks-all:
	@echo "Running git hooks on ALL files..."
	$(UV) run pre-commit run --all-files

# Cleanup
clean:
	@echo "Cleaning artifacts..."
	-$(RM_RF) dist/
	-$(RM_RF) build/
	-$(RM_RF) *.egg-info
	-$(RM_RF) .pytest_cache
	-$(RM_RF) .coverage
	-$(RM_RF) htmlcov
	-$(RM_RF) .ruff_cache
	-$(FIND_PYCACHE)
	@echo "Clean complete!"
