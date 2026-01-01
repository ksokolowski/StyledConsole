# Image Exporter Specification (v0.9.9)

**Status:** ✅ Implemented
**Released:** v0.9.9
**Created:** December 28, 2025
**Updated:** January 2, 2026

______________________________________________________________________

## Overview

Add native image export capabilities to StyledConsole using Pillow. This enables:

- Static screenshots (PNG, WebP)
- Animated recordings (GIF, WebP, AVIF)
- No external tools required (unlike VHS)
- Lazy loading - zero impact on users who don't use image export

______________________________________________________________________

## API Design

### Console Methods

```python
from styledconsole import Console

console = Console(record=True)
console.frame("Hello World", border="rounded", border_gradient_start="green")

# Static exports
console.export_png("output.png")                    # Lossless PNG
console.export_png("output.png", scale=2.0)         # 2x resolution (retina)
console.export_webp("output.webp")                  # Smaller WebP
console.export_webp("output.webp", quality=90)      # Quality 0-100

# Animated exports (multi-frame recording)
console.export_gif("output.gif", fps=10)            # Animated GIF
console.export_gif("output.gif", fps=10, loop=0)    # Loop forever (default)
console.export_webp("output.webp", animated=True)   # Animated WebP
```

### Multi-Frame Recording

```python
console = Console(record=True)

# Record multiple frames for animation
for i in range(10):
    console.clear_recording()
    console.frame(f"Progress: {i*10}%", border="rounded")
    console.capture_frame()  # Save current output as frame

# Export as animation
console.export_gif("progress.gif", fps=5)
```

______________________________________________________________________

## Architecture

### File Structure

```
src/styledconsole/
├── export/
│   ├── __init__.py              # Lazy loading exports
│   └── image_exporter.py        # NEW: ImageExporter class
├── core/
│   ├── export_manager.py        # Existing: HTML/text export
│   └── ansi_parser.py           # NEW: ANSI to styled segments
└── console.py                   # Add export_png, export_webp, export_gif
```

### Lazy Loading Pattern

```python
# src/styledconsole/export/__init__.py

def get_image_exporter():
    """Lazy load ImageExporter (requires Pillow)."""
    try:
        from .image_exporter import ImageExporter
        return ImageExporter
    except ImportError as e:
        raise ImportError(
            "Image export requires Pillow. Install with: "
            "pip install styledconsole[image]"
        ) from e

# Re-export for convenience
__all__ = ["get_image_exporter"]
```

### Console Integration

```python
# In Console class

def export_png(self, path: str, *, scale: float = 1.0) -> None:
    """Export recorded output as PNG image."""
    self._validate_recording_enabled()

    # Lazy load - only import Pillow when needed
    from styledconsole.export import get_image_exporter
    ImageExporter = get_image_exporter()

    exporter = ImageExporter(
        recorded_text=self._rich_console.export_text(),
        recorded_html=self._rich_console.export_html(),
        theme=self._theme,
    )
    exporter.save_png(path, scale=scale)
```

______________________________________________________________________

## Implementation Details

### 1. ANSI Parser

Convert ANSI escape sequences to styled segments:

```python
@dataclass
class StyledSegment:
    """A segment of text with styling information."""
    text: str
    foreground: str | None = None     # Hex color "#RRGGBB"
    background: str | None = None     # Hex color "#RRGGBB"
    bold: bool = False
    italic: bool = False
    underline: bool = False
    x: int = 0                        # Column position
    y: int = 0                        # Row position

class ANSIParser:
    """Parse ANSI escape codes into styled segments."""

    def parse(self, text: str) -> list[StyledSegment]:
        """Parse ANSI text into styled segments with positions."""
        ...
```

### 2. ImageExporter Class

```python
class ImageExporter:
    """Export console output to image formats using Pillow."""

    DEFAULT_FONT_SIZE = 14
    DEFAULT_PADDING = 20
    DEFAULT_BG_COLOR = "#1e1e2e"      # Dark background
    DEFAULT_FG_COLOR = "#cdd6f4"      # Light text

    def __init__(
        self,
        recorded_text: str,
        recorded_html: str,
        theme: TerminalTheme | None = None,
        font_path: str | None = None,
        font_size: int = DEFAULT_FONT_SIZE,
    ):
        self._text = recorded_text
        self._html = recorded_html
        self._theme = theme
        self._font = self._load_font(font_path, font_size)
        self._segments = self._parse_ansi()

    def _load_font(self, path: str | None, size: int) -> ImageFont:
        """Load monospace font for rendering."""
        from PIL import ImageFont

        if path:
            return ImageFont.truetype(path, size)

        # Try common monospace fonts
        for font_name in ["JetBrainsMono-Regular.ttf", "DejaVuSansMono.ttf"]:
            try:
                return ImageFont.truetype(font_name, size)
            except OSError:
                continue

        # Fallback to default
        return ImageFont.load_default()

    def _calculate_dimensions(self) -> tuple[int, int]:
        """Calculate image dimensions based on text content."""
        lines = self._text.split("\n")
        char_width, char_height = self._get_char_dimensions()

        width = max(len(line) for line in lines) * char_width + 2 * self.DEFAULT_PADDING
        height = len(lines) * char_height + 2 * self.DEFAULT_PADDING

        return width, height

    def _render_frame(self) -> Image:
        """Render text to PIL Image."""
        from PIL import Image, ImageDraw

        width, height = self._calculate_dimensions()
        img = Image.new("RGB", (width, height), self._theme.background or self.DEFAULT_BG_COLOR)
        draw = ImageDraw.Draw(img)

        for segment in self._segments:
            x = self.DEFAULT_PADDING + segment.x * self._char_width
            y = self.DEFAULT_PADDING + segment.y * self._char_height

            draw.text(
                (x, y),
                segment.text,
                font=self._font,
                fill=segment.foreground or self.DEFAULT_FG_COLOR,
            )

        return img

    def save_png(self, path: str, *, scale: float = 1.0) -> None:
        """Save as PNG image."""
        img = self._render_frame()
        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.LANCZOS)
        img.save(path, "PNG")

    def save_webp(self, path: str, *, quality: int = 90, animated: bool = False) -> None:
        """Save as WebP image (static or animated)."""
        if animated:
            self._save_animated_webp(path, quality)
        else:
            img = self._render_frame()
            img.save(path, "WEBP", quality=quality)

    def save_gif(self, path: str, *, fps: int = 10, loop: int = 0) -> None:
        """Save as animated GIF."""
        frames = self._frames if self._frames else [self._render_frame()]

        frames[0].save(
            path,
            save_all=True,
            append_images=frames[1:],
            duration=1000 // fps,
            loop=loop,
        )
```

______________________________________________________________________

## Optional Dependencies

### pyproject.toml Changes

```toml
[project.optional-dependencies]
image = ["Pillow>=10.0.0"]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.1",
    "pytest-snapshot>=0.9",
    "ruff>=0.3",
    "pre-commit>=3.6",
    "radon>=6.0",
    "mypy>=1.0",
    "Pillow>=10.0.0",  # For testing image export
]
```

### Installation

```bash
# Without image support (default)
pip install styledconsole

# With image support
pip install styledconsole[image]

# Development (includes Pillow)
uv sync
```

______________________________________________________________________

## Theme Integration

Use existing Rich terminal themes for consistent colors:

```python
from rich.terminal_theme import MONOKAI, DIMMED_MONOKAI

# Export with specific theme
console.export_png("output.png", theme=MONOKAI)
```

Default theme colors (Catppuccin Mocha-like):

- Background: `#1e1e2e`
- Foreground: `#cdd6f4`
- Colors mapped from ANSI codes

______________________________________________________________________

## Font Handling

### Strategy: System Fonts with Fallback

1. Try user-specified font path
1. Try common monospace fonts (JetBrains Mono, DejaVu Sans Mono, Consolas)
1. Fall back to Pillow default font

### Future: Bundled Font (Optional)

Could bundle a small monospace font (e.g., JetBrains Mono subset) for consistent rendering across systems.

______________________________________________________________________

## Testing Strategy

```python
# tests/unit/export/test_image_exporter.py

class TestImageExporter:
    """Tests for image export functionality."""

    @pytest.fixture
    def console_with_content(self):
        console = Console(record=True)
        console.frame("Test", border="rounded")
        return console

    def test_export_png_creates_file(self, console_with_content, tmp_path):
        """PNG export creates valid image file."""
        path = tmp_path / "test.png"
        console_with_content.export_png(str(path))
        assert path.exists()

        from PIL import Image
        img = Image.open(path)
        assert img.format == "PNG"
        assert img.width > 0
        assert img.height > 0

    def test_export_without_pillow_raises_import_error(self, monkeypatch):
        """Clear error when Pillow not installed."""
        # Mock Pillow import to fail
        ...

    def test_export_without_recording_raises_error(self):
        """Export requires record=True."""
        console = Console(record=False)
        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            console.export_png("test.png")
```

______________________________________________________________________

## Implementation Phases

### Phase 1: Core Static Export

- [ ] Create `ANSIParser` class
- [ ] Create `ImageExporter` class
- [ ] Add `export_png()` to Console
- [ ] Add `export_webp()` to Console
- [ ] Update pyproject.toml with optional dependency
- [ ] Write unit tests

### Phase 2: Animation Support

- [ ] Add `capture_frame()` to Console
- [ ] Add multi-frame rendering
- [ ] Add `export_gif()` to Console
- [ ] Add animated WebP support

### Phase 3: Documentation & Polish

- [ ] Update USER_GUIDE.md
- [ ] Add examples to Examples repo
- [ ] Generate README visuals
- [ ] Update CHANGELOG.md

______________________________________________________________________

## Questions Resolved

1. **Scope for v0.9.9**: Full implementation (static + animated)
1. **Font handling**: System fonts with fallback, no bundling for now
1. **Theme integration**: Reuse Rich terminal themes

______________________________________________________________________

## Related Files

- [console.py](../src/styledconsole/console.py) - Add export methods
- [export_manager.py](../src/styledconsole/core/export_manager.py) - Existing export logic
- [pyproject.toml](../pyproject.toml) - Add optional dependency
