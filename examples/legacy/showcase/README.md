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

### `rainbow_fat_alignment.py` - Rainbow Fat Alignment Showcase

Advanced example showcasing layout alignment with vibrant styling:

- **Three Alignment Demonstrations**: Left, Center, and Right aligned sections
- **Rainbow Gradient Banners**: Large colorful ASCII art banners with gradients
- **Mixed Alignment Layouts**: Dynamic visual hierarchy with multiple alignment types
- **Emoji-Rich Dashboard**: Performance, storage, and user metrics cards (all centered)
- **Border Style Gallery**: All 8 border styles with rotating alignments
- **Multiple Color Schemes**: CSS4 color names throughout (lime, cyan, yellow, magenta, hotpink, orange)

**Features Demonstrated:**

- `LayoutComposer.stack()` with `align="left"`, `align="center"`, `align="right"`
- `BannerRenderer` with red→magenta, green→cyan, and blue→magenta gradients
- `FrameRenderer` with all 8 border styles
- Emoji-safe width calculations with `visual_width()`
- `format_emoji_with_spacing()` for perfect emoji alignment
- Fixed and auto-width layouts
- Complex multi-section compositions

**Run It:**

```bash
uv run python examples/showcase/rainbow_fat_alignment.py
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
