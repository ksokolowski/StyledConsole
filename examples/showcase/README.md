# StyledConsole Showcase Examples

This directory contains comprehensive showcase examples demonstrating advanced features and real-world use cases of StyledConsole.

## Examples

### `cicd_dashboard.py` - CI/CD Pipeline Dashboards

Comprehensive CI/CD monitoring dashboards demonstrating:

- **3x3 Grid Layouts**: Multi-stage pipeline visualization
- **Banner Headers**: Eye-catching titles with ASCII art and gradients
- **Color-Coded Status**: Visual indicators using colors and emojis
- **Multiple Dashboard Types**:
  - Failed Pipeline Dashboard (with warnings and errors)
  - Success Dashboard (all stages passed)
  - Monitoring Dashboard (system metrics)

**Features Demonstrated:**
- `BannerRenderer` with gradient colors
- `FrameRenderer` with content colors, border colors, and title colors
- `LayoutComposer` with grid layouts (3x3, 2x2)
- Status emojis (✅ ❌ ⚠️ 🔴 🟢)
- Per-line gradient interpolation
- Mixed frame styles and colors

**Run It:**
```bash
uv run python examples/showcase/cicd_dashboard.py
```

### `banner_showcase.py` - Banner Renderer Gallery

Visual showcase of banner capabilities:

- Different ASCII art fonts (slant, banner, standard, etc.)
- Gradient color effects
- Border integration
- Application launch banners

**Run It:**
```bash
uv run python examples/showcase/banner_showcase.py
```

## Requirements

All showcase examples require:
- Python 3.10+
- StyledConsole library installed
- Terminal with 24-bit color support (most modern terminals)

## Color Support

The dashboards use 24-bit RGB ANSI color codes. If your terminal doesn't support these, the output will still be readable but without colors. Most modern terminals support this:
- iTerm2 (macOS)
- Terminal.app (macOS)
- Windows Terminal
- GNOME Terminal
- Konsole
- VS Code integrated terminal

## Creating Your Own Dashboards

Use these examples as templates for creating:
- Application status dashboards
- System monitoring displays
- Build/deployment reports
- Test result summaries
- Log viewers with color-coded severity
- Multi-panel terminal UIs
