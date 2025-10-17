# StyledConsole Package Manager: UV

**Decision Date:** October 17, 2025  
**Status:** ✅ Implemented in all documentation  
**Package Manager:** UV (Astral)

---

## TL;DR

StyledConsole uses **UV** instead of Poetry or pip because:

✅ **10-100x faster** - Matters in dev and CI/CD  
✅ **Standard format** - PEP 621 pyproject.toml (works with pip too)  
✅ **Same team as Ruff** - Perfect ecosystem fit (Astral)  
✅ **Python version management** - Test 3.10, 3.11, 3.12 easily  
✅ **Modern best practice** - 2025 industry standard for Python ≥3.10  

---

## Quick Start

```bash
# Install UV (one-time)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone project
git clone https://github.com/user/styledconsole.git
cd styledconsole

# Install all dependencies (~1 second)
uv sync

# Start coding!
uv run pytest           # Run tests
uv run ruff check .     # Lint
uv run ruff format .    # Format
```

---

## Key Commands

```bash
# Add dependency
uv add "rich>=13.7"

# Add dev dependency
uv add --dev "pytest>=8.0"

# Run tests
uv run pytest

# Build package
uv build

# Publish to PyPI
uv publish
```

---

## For End Users

**No change!** Users can still install with:

```bash
pip install styledconsole        # Works
poetry add styledconsole         # Works
uv add styledconsole             # Works
```

UV is only used by StyledConsole **developers**, not library users.

---

## Files Updated

- ✅ **TASKS.md** - T-001 uses UV commands
- ✅ **PLAN.md** - PEP 621 format, UV references
- ✅ **SDD-UPDATES-SUMMARY.md** - Updated references
- ✅ **UV-MIGRATION.md** - Complete migration guide (new)

---

## pyproject.toml Format

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "styledconsole"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "rich>=13.7",
    "pyfiglet>=1.0.2",
    "wcwidth>=0.2.13",
    "ansi2html>=1.8.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "ruff>=0.3",
]
```

**Standard PEP 621** - works with pip, poetry, and uv!

---

## Speed Comparison

| Operation | UV | Poetry | Pip |
|-----------|-----|--------|-----|
| Install 4 deps | ~1s | ~8s | ~4s |
| Full setup | ~2s | ~12s | ~8s |
| Lock generation | ~0.5s | ~5s | N/A |

**Result:** 5-10x faster development workflow

---

## Resources

- **Migration Guide:** See `UV-MIGRATION.md`
- **UV Docs:** https://docs.astral.sh/uv/
- **UV GitHub:** https://github.com/astral-sh/uv

---

**Ready for T-001 implementation with UV! 🚀**
