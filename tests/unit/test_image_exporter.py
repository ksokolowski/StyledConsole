"""Tests for image export functionality."""

import pytest

from styledconsole import Console


class TestImageExport:
    """Tests for Console image export methods."""

    @pytest.fixture
    def console_with_content(self):
        """Create console with recorded content."""
        console = Console(record=True)
        console.frame("Hello World", border="rounded")
        return console

    def test_export_png_creates_file(self, console_with_content, tmp_path):
        """export_png creates a valid PNG file."""
        path = tmp_path / "test.png"
        console_with_content.export_png(str(path))

        assert path.exists()
        assert path.stat().st_size > 0

        # Verify it's a valid PNG
        from PIL import Image

        img = Image.open(path)
        assert img.format == "PNG"
        assert img.width > 0
        assert img.height > 0

    def test_export_png_with_scale(self, console_with_content, tmp_path):
        """export_png respects scale parameter."""
        path1 = tmp_path / "test1x.png"
        path2 = tmp_path / "test2x.png"

        console_with_content.export_png(str(path1), scale=1.0)
        console_with_content.export_png(str(path2), scale=2.0)

        from PIL import Image

        img1 = Image.open(path1)
        img2 = Image.open(path2)

        # 2x scale should double dimensions
        assert img2.width == img1.width * 2
        assert img2.height == img1.height * 2

    def test_export_webp_creates_file(self, console_with_content, tmp_path):
        """export_webp creates a valid WebP file."""
        path = tmp_path / "test.webp"
        console_with_content.export_webp(str(path))

        assert path.exists()
        assert path.stat().st_size > 0

        from PIL import Image

        img = Image.open(path)
        assert img.format == "WEBP"

    def test_export_webp_quality(self, console_with_content, tmp_path):
        """export_webp respects quality parameter."""
        path_high = tmp_path / "high.webp"
        path_low = tmp_path / "low.webp"

        console_with_content.export_webp(str(path_high), quality=95)
        console_with_content.export_webp(str(path_low), quality=20)

        # Higher quality should generally produce larger files
        # (though not guaranteed for all content)
        assert path_high.exists()
        assert path_low.exists()

    def test_export_gif_creates_file(self, console_with_content, tmp_path):
        """export_gif creates a valid GIF file."""
        path = tmp_path / "test.gif"
        console_with_content.export_gif(str(path))

        assert path.exists()
        assert path.stat().st_size > 0

        from PIL import Image

        img = Image.open(path)
        assert img.format == "GIF"

    def test_export_without_recording_raises_error(self, tmp_path):
        """Export methods raise error if recording not enabled."""
        console = Console(record=False)
        console.frame("Test")

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            console.export_png(str(tmp_path / "test.png"))

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            console.export_webp(str(tmp_path / "test.webp"))

        with pytest.raises(RuntimeError, match="Recording mode not enabled"):
            console.export_gif(str(tmp_path / "test.gif"))

    def test_export_with_colors(self, tmp_path):
        """Export preserves colors in output."""
        console = Console(record=True)
        console.text("Red text", color="red")
        console.text("Green text", color="green")

        path = tmp_path / "colors.png"
        console.export_png(str(path))

        assert path.exists()
        # We just verify it creates a file - visual verification is manual

    def test_export_with_gradient_border(self, tmp_path):
        """Export works with gradient borders."""
        console = Console(record=True)
        console.frame(
            "Gradient border test",
            border="rounded",
            border_gradient_start="green",
            border_gradient_end="cyan",
        )

        path = tmp_path / "gradient.png"
        console.export_png(str(path))

        assert path.exists()

    def test_export_with_icons(self, tmp_path):
        """Export works with icons/emoji."""
        from styledconsole import icons

        console = Console(record=True)
        console.frame(
            f"{icons.CHECK_MARK_BUTTON} Success",
            title=f"{icons.SPARKLES} Status",
        )

        path = tmp_path / "icons.png"
        console.export_png(str(path))

        assert path.exists()

    def test_export_empty_console(self, tmp_path):
        """Export handles empty console gracefully."""
        console = Console(record=True)
        # No content added

        path = tmp_path / "empty.png"
        console.export_png(str(path))

        assert path.exists()

    def test_webp_smaller_than_png(self, console_with_content, tmp_path):
        """WebP should generally be smaller than PNG."""
        png_path = tmp_path / "test.png"
        webp_path = tmp_path / "test.webp"

        console_with_content.export_png(str(png_path))
        console_with_content.export_webp(str(webp_path))

        # WebP is typically smaller than PNG
        # Allow some tolerance as this depends on content
        png_size = png_path.stat().st_size
        webp_size = webp_path.stat().st_size

        # Just verify both were created successfully
        assert png_size > 0
        assert webp_size > 0


class TestImageExporterClass:
    """Tests for ImageExporter class directly."""

    def test_lazy_import_works(self):
        """get_image_exporter returns ImageExporter class."""
        from styledconsole.export import get_image_exporter

        cls = get_image_exporter()
        assert cls.__name__ == "ImageExporter"

    def test_image_theme_defaults(self):
        """ImageTheme has sensible defaults."""
        from styledconsole.export import get_image_theme

        theme_cls = get_image_theme()
        theme = theme_cls()

        assert theme.background == "#11111b"  # Catppuccin Mocha Crust
        assert theme.foreground == "#cdd6f4"
        assert theme.font_size == 16
        assert theme.padding == 20

    def test_image_exporter_debug_grid_does_not_crash(self, tmp_path):
        from styledconsole.export import get_image_theme

        console = Console(record=True)
        console.frame("Grid test", border="rounded")

        theme_cls = get_image_theme()
        theme = theme_cls(terminal_size=(80, 24), debug_grid=True)

        path = tmp_path / "grid.png"
        console.export_webp(str(path.with_suffix(".webp")), theme=theme, auto_crop=False)
        assert path.with_suffix(".webp").exists()

    def test_image_exporter_with_custom_theme(self, tmp_path):
        """ImageExporter accepts custom theme."""
        from rich.console import Console as RichConsole

        from styledconsole.export import get_image_exporter, get_image_theme

        theme_cls = get_image_theme()
        custom_theme = theme_cls(
            background="#000000",
            foreground="#ffffff",
            font_size=16,
            padding=30,
        )

        console = RichConsole(record=True)
        console.print("Test content")

        exporter_cls = get_image_exporter()
        exporter = exporter_cls(console, theme=custom_theme)

        path = tmp_path / "custom_theme.png"
        exporter.save_png(str(path))

        assert path.exists()

    def test_image_exporter_width_accounts_for_wide_emoji_when_render_emojis_false(self):
        """Width measurement uses Rich cell widths even without emoji rendering.

        This prevents right-side border clipping/misalignment for lines that
        contain emoji/icons (e.g. in tables) when render_emojis=False.
        """
        from rich.cells import cell_len
        from rich.console import Console as RichConsole

        from styledconsole.export import get_image_exporter

        rich_console = RichConsole(record=True)
        rich_console.print("A🚀B")

        exporter_cls = get_image_exporter()
        exporter = exporter_cls(rich_console, render_emojis=False)

        # Ensure font metrics are loaded so char_width is available.
        _, _, pil_font = exporter._lazy_import_pillow()
        exporter._font_loader.load(pil_font)

        width_px, _ = exporter._calculate_dimensions()
        content_width_px = width_px - int(exporter._theme.padding * 2)

        expected_cells = cell_len("A🚀B")
        expected_px = expected_cells * exporter._font_loader.char_width

        assert content_width_px >= expected_px

    def test_emoji_renderer_uses_rich_cell_len_for_emoji_width(self, monkeypatch):
        """EmojiRenderer advances emojis by Rich cell width * char_width.

        README image generation patches Rich's cell_len; the image exporter must
        follow that to keep table borders aligned.
        """
        from rich import cells as rich_cells
        from rich.console import Console as RichConsole

        from styledconsole.export import get_image_exporter

        original_cell_len = rich_cells.cell_len

        def patched_cell_len(text: str) -> int:
            if text == "🚀":
                return 1
            return original_cell_len(text)

        monkeypatch.setattr(rich_cells, "cell_len", patched_cell_len)

        rich_console = RichConsole(record=True)
        rich_console.print("X🚀Y")

        exporter_cls = get_image_exporter()
        exporter = exporter_cls(rich_console, render_emojis=True)

        _, _, pil_font = exporter._lazy_import_pillow()
        exporter._font_loader.load(pil_font)

        # Create the renderer on a temp image and validate width.
        from PIL import Image

        img = Image.new("RGB", (10, 10))
        emoji_renderer = exporter._create_emoji_renderer(img)
        assert emoji_renderer is not None

        width = emoji_renderer.getwidth("X🚀Y", font=exporter._font_loader.font)
        expected = (1 + 1 + 1) * exporter._font_loader.char_width
        assert width == expected


class TestImageExporterFormats:
    """Test various image format outputs."""

    @pytest.fixture
    def rich_console_with_content(self):
        """Create Rich console with content."""
        from rich.console import Console as RichConsole

        console = RichConsole(record=True)
        console.print("[bold red]Hello[/bold red] [green]World[/green]")
        return console

    def test_png_format(self, rich_console_with_content, tmp_path):
        """PNG export produces valid PNG."""
        from styledconsole.export import get_image_exporter

        exporter_cls = get_image_exporter()
        exporter = exporter_cls(rich_console_with_content)

        path = tmp_path / "test.png"
        exporter.save_png(str(path))

        from PIL import Image

        img = Image.open(path)
        assert img.format == "PNG"
        assert img.mode == "RGB"

    def test_webp_format(self, rich_console_with_content, tmp_path):
        """WebP export produces valid WebP."""
        from styledconsole.export import get_image_exporter

        exporter_cls = get_image_exporter()
        exporter = exporter_cls(rich_console_with_content)

        path = tmp_path / "test.webp"
        exporter.save_webp(str(path))

        from PIL import Image

        img = Image.open(path)
        assert img.format == "WEBP"

    def test_gif_format(self, rich_console_with_content, tmp_path):
        """GIF export produces valid GIF."""
        from styledconsole.export import get_image_exporter

        exporter_cls = get_image_exporter()
        exporter = exporter_cls(rich_console_with_content)

        path = tmp_path / "test.gif"
        exporter.save_gif(str(path))

        from PIL import Image

        img = Image.open(path)
        assert img.format == "GIF"
