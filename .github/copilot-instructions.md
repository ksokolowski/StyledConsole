# AI Coding Agent Instructions for StyledConsole

**Project:** StyledConsole v0.9.8.1
**Last Updated:** December 28, 2025
**Python:** ≥3.10 | **License:** Apache-2.0

______________________________________________________________________

## 🛠️ Development Tooling (MUST USE)

### Package Manager: uv (preferred)

```bash
# Environment setup
uv sync --group dev              # Install all dependencies
uv run pytest                    # Run tests
uv run python examples/run_examples.py  # Run examples

# Fallback only if uv unavailable
pip install -e ".[dev]"
```

### Pre-commit Hooks (REQUIRED before commits)

```bash
# Install hooks (one-time)
uv run pre-commit install

# Run all hooks manually
uv run pre-commit run --all-files
```

**Active hooks:**

- `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-toml`
- `check-ast` - Catches Python syntax errors
- `debug-statements` - Catches forgotten print/breakpoint
- `ruff` - Linting with auto-fix
- `ruff-format` - Code formatting
- `mdformat` - Markdown formatting
- `complexity-metrics` - Radon CC/MI gate (blocks if CC > C or MI < 40)

### Testing

```bash
# Full test suite with coverage
uv run pytest                    # 700+ tests, 95%+ coverage

# Quick targeted test
uv run pytest tests/unit/test_frame.py -v

# Update snapshots after intentional changes
uv run pytest --snapshot-update
```

### Visual Examples (Quality Validation)

```bash
# Run all examples (validates library works correctly)
uv run python examples/run_examples.py --all

# Auto-run with delays (for visual inspection)
uv run python examples/run_examples.py --auto
```

______________________________________________________________________

## 🚨 Critical Working Principles

### Tool Usage

- **NEVER use sed/grep for code modifications** - Use `read_file()`, `replace_string_in_file()`, `grep_search()` tools. Mass edits with terminal tools (sed, awk, perl -i) have corrupted complex code in this project.
- **NEVER pipe output through head/tail/grep** - Commands like `uv run pytest | head`, `uv run pytest 2>&1 | tail -20`, or `grep -v` hide valuable output and mask errors. Always capture full output.
- **Always run pre-commit before suggesting commits** - `uv run pre-commit run --all-files`
- **Prefer uv over pip** - All commands should use `uv run` prefix
- **Non-interactive example runs** - Use `--auto` flag: `uv run python examples/run_examples.py --auto`

### Console API Usage

- **Use Console API exclusively in examples** - Never access `console._rich_console` or import Rich directly
- **Rich is infrastructure, not interface** - Console is the facade; Rich is the backend
- **Explicit Gradient Arguments** - Use `border_gradient_start`/`border_gradient_end`, NEVER tuples to `border_color`

### Anti-Patterns to Avoid

- ❌ Using `console._rich_console.print()` in examples
- ❌ Importing Rich Panel/Text/Group directly in example files
- ❌ Passing tuples to `border_color` (crashes API)
- ❌ Running `pip install` instead of `uv sync`
- ❌ Skipping pre-commit hooks
- ❌ Committing without running tests
- ❌ Piping command output through `| head`, `| tail`, `| grep` (hides errors)
- ❌ Using `sed`, `awk`, `perl -i` for code edits (corrupts complex code)

______________________________________________________________________

## 📁 Project Structure (v0.9.0)

```
styledconsole/
├── src/styledconsole/           # Library source
│   ├── console.py               # Main facade API
│   ├── policy.py                # RenderPolicy (environment-aware rendering)
│   ├── icons.py                 # IconProvider (emoji/ASCII auto-switching)
│   ├── emoji_registry.py        # EMOJI constants (4000+ from emoji package)
│   ├── emojis.py                # Re-exports from emoji_registry (backward compat)
│   ├── core/                    # Rendering engine
│   │   ├── rendering_engine.py  # Rich-native coordinator (policy-aware)
│   │   ├── box_mapping.py       # Border → Rich Box
│   │   ├── theme.py             # Theme system (semantic colors, gradients)
│   │   └── styles.py            # Border definitions
│   ├── effects/                 # Strategy-based gradients
│   │   ├── engine.py            # apply_gradient()
│   │   └── strategies.py        # Position/Color/Target strategies
│   ├── presets/                 # High-level components
│   │   ├── status.py            # status_frame()
│   │   ├── summary.py           # test_summary()
│   │   └── dashboard.py         # dashboard()
│   └── utils/                   # Utilities
│       ├── text.py              # Emoji-safe width (CRITICAL)
│       ├── color.py             # CSS4 colors, gradients
│       └── icon_data.py         # Icon registry data
├── tests/                       # 700+ tests
│   ├── unit/                    # Component tests
│   ├── integration/             # Cross-component tests
│   └── snapshots/               # Visual regression
├── examples/                    # Visual examples
│   ├── gallery/                 # Visual showcases
│   ├── usecases/                # Real-world scenarios
│   ├── demos/                   # Feature demos
│   ├── validation/              # Testing scripts
│   └── run_examples.py          # Unified runner
├── docs/                        # Documentation
│   ├── USER_GUIDE.md            # API usage, examples, troubleshooting
│   ├── DEVELOPER_GUIDE.md       # Architecture and development guide
│   └── README.md                # Documentation overview
├── scripts/
│   └── complexity_check.py      # Radon CC/MI gate
├── pyproject.toml               # Dependencies & config
└── .pre-commit-config.yaml      # Pre-commit hooks
```

______________________________________________________________________

## 🎯 Core Concepts

### Console Facade Pattern

```python
from styledconsole import Console, EMOJI, icons

console = Console()
console.frame("Content", title="Title", border="rounded")
console.banner("SUCCESS", start_color="green", end_color="blue")
console.text("Status: OK", color="lime", bold=True)
```

### Data Flow

```
Console(policy=..., theme=...)
  → RenderingEngine (policy-aware rendering)
  → box_mapping.get_box_style_for_policy() → Rich Box
  → Rich Panel → rich_console.print()
  → ExportManager.export_html() (if record=True)
```

### RenderPolicy (Environment-Aware Rendering)

RenderPolicy controls output based on terminal capabilities and environment variables:

```python
from styledconsole import Console, RenderPolicy

# Auto-detect from environment (NO_COLOR, CI, TERM=dumb)
console = Console()  # Uses RenderPolicy.from_env() by default

# CI-friendly: colors but no emoji
console = Console(policy=RenderPolicy.ci_friendly())

# ASCII-only for logs/pipes
console = Console(policy=RenderPolicy(unicode=False, color=False, emoji=False))

# Check policy settings
if console.policy.emoji:
    print("Emoji enabled")
```

**Environment Variables Detected:**

- `NO_COLOR` → Disables color output
- `FORCE_COLOR` → Forces color output
- `TERM=dumb` → Disables unicode, emoji, color
- `CI`, `GITHUB_ACTIONS`, `GITLAB_CI` → Conservative mode (no emoji)

### IconProvider (Emoji/ASCII Auto-Switching)

Icons automatically render as emoji or colored ASCII based on terminal capabilities:

```python
from styledconsole import icons, set_icon_mode

# Auto-detects terminal capability (default)
print(f"{icons.CHECK_MARK_BUTTON} Tests passed")  # ✅ or [OK] (green)
print(f"{icons.CROSS_MARK} Build failed")         # ❌ or [FAIL] (red)
print(f"{icons.WARNING} Deprecation")             # ⚠️ or [WARN] (yellow)

# Force specific mode globally
set_icon_mode("ascii")   # Force ASCII everywhere
set_icon_mode("emoji")   # Force emoji everywhere
set_icon_mode("auto")    # Auto-detect (default)
```

### Themes (Semantic Colors)

```python
from styledconsole import Console, THEMES

# Use built-in theme
console = Console(theme="monokai")  # or THEMES.MONOKAI

# Semantic colors resolve through theme
console.frame("OK!", border_color="success")   # Uses theme.success color
console.frame("Oops", border_color="error")    # Uses theme.error color
```

### Emoji Handling (CRITICAL)

```python
from styledconsole.utils.text import visual_width, pad_to_width

# ALWAYS use visual_width, NEVER len()
width = visual_width("🚀 Title")  # Returns 9, not 8

# Use EMOJI constants in examples (4000+ available from emoji package)
from styledconsole import EMOJI
console.frame(f"{EMOJI.CHECK_MARK_BUTTON} Done", title=f"{EMOJI.ROCKET} Status")

# Common emoji names (CLDR standard from emoji package):
# EMOJI.CHECK_MARK_BUTTON (✅), EMOJI.CROSS_MARK (❌), EMOJI.WARNING (⚠️)
# EMOJI.ROCKET (🚀), EMOJI.FIRE (🔥), EMOJI.SPARKLES (✨), EMOJI.PARTY_POPPER (🎉)
```

### API Signatures

```python
# Frame
console.frame(
    content,
    title="Title",
    border="rounded",          # solid|rounded|double|heavy|thick|ascii|minimal|dashed
    border_color="cyan",
    border_gradient_start="red",  # NOT border_color=("red", "blue")
    border_gradient_end="blue",
)

# Banner
console.banner(
    "TEXT",
    font="slant",
    start_color="red",
    end_color="blue",
)

# Text
console.text("Hello", color="cyan", bold=True, italic=True)
```

______________________________________________________________________

## 🧪 Quality Gates

### Before Every Commit

1. **Pre-commit hooks**: `uv run pre-commit run --all-files`
1. **Tests**: `uv run pytest` (must pass 700+ tests)
1. **Examples**: `uv run python examples/run_examples.py --all`

### Complexity Thresholds

- **Cyclomatic Complexity**: Grade C or better (≤10)
- **Maintainability Index**: ≥40 per file
- Excluded from MI: `text.py` (data), `rendering_engine.py` (coordinator)

### Coverage Target

- Overall: 95%+
- New code: 100% coverage expected

______________________________________________________________________

## 📝 Key Conventions

### Colors

```python
# CSS4 names (preferred)
console.frame("...", border_color="dodgerblue")

# Hex codes
console.frame("...", border_color="#1E90FF")

# RGB tuples
console.frame("...", border_color=(30, 144, 255))
```

### Border Styles

8 built-in: `solid`, `rounded`, `double`, `heavy`, `thick`, `ascii`, `minimal`, `dashed`

### Example Categories

| Folder        | Purpose                                    |
| ------------- | ------------------------------------------ |
| `gallery/`    | Visual showcases (borders, colors, emojis) |
| `usecases/`   | Real-world scenarios (alerts, reports)     |
| `demos/`      | Feature demonstrations (animation)         |
| `validation/` | Testing and validation                     |

______________________________________________________________________

## 🔄 Common Workflows

### Adding a Feature

1. Write tests first in `tests/unit/`
1. Implement in appropriate module
1. Add example in `examples/`
1. Run: `uv run pre-commit run --all-files && uv run pytest`

### Fixing a Bug

1. Write failing test
1. Fix the bug
1. Verify: `uv run pytest tests/unit/test_<module>.py -v`
1. Run full suite: `uv run pytest`

### Updating Examples

1. Use Console API only (no Rich imports)
1. Use EMOJI constants (no raw emojis)
1. Test: `uv run python examples/<folder>/<example>.py`
1. Validate all: `uv run python examples/run_examples.py --all`

______________________________________________________________________

## 📚 Documentation

| Document                  | Purpose                              |
| ------------------------- | ------------------------------------ |
| `docs/USER_GUIDE.md`      | API usage, examples, troubleshooting |
| `docs/DEVELOPER_GUIDE.md` | Architecture and development guide   |
| `CONTRIBUTING.md`         | Development workflow and standards   |
| `CHANGELOG.md`            | Version history                      |
| `README.md`               | Quick start and project overview     |

______________________________________________________________________

## ⚠️ Gotchas

1. **Emoji width**: Always `visual_width()`, never `len()`
1. **Gradient args**: Use `border_gradient_start`/`end`, not tuple to `border_color`
1. **Rich access**: Avoid `console._rich_console` in examples
1. **Folder name**: It's `docs/` not `doc/`
1. **Package manager**: Use `uv run`, not bare `python` or `pip`
1. **Pre-commit**: Run before every commit suggestion

______________________________________________________________________

## 🏃 Quick Reference

```bash
# Setup
uv sync --group dev

# Daily workflow
uv run pytest                              # Tests
uv run pre-commit run --all-files          # Lint/format
uv run python examples/run_examples.py     # Examples

# Before commit
uv run pre-commit run --all-files && uv run pytest
```
