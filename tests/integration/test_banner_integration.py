"""Integration tests for BannerRenderer.

Tests real-world usage patterns and visual output correctness.
"""

from styledconsole import Banner, BannerRenderer
from styledconsole.utils.text import strip_ansi, visual_width


def test_basic_banner_workflow():
    """Test typical user workflow with BannerRenderer."""
    renderer = BannerRenderer()

    # Simple banner
    lines = renderer.render("TEST")
    assert len(lines) > 0
    assert isinstance(lines, list)
    assert all(isinstance(line, str) for line in lines)


def test_banner_with_all_features():
    """Test banner with gradient, border, and custom settings."""
    renderer = BannerRenderer()

    lines = renderer.render(
        "DEMO",
        font="banner",
        gradient_start="#ff0000",
        gradient_end="#0000ff",
        border="double",
        width=60,
        align="center",
        padding=2,
    )

    # Should have border
    assert len(lines) >= 3
    assert "═" in lines[0]
    assert "═" in lines[-1]

    # Should have gradient colors
    content_lines = lines[1:-1]
    assert any("\033[38;2;" in line for line in content_lines)

    # All lines should have consistent width
    widths = [visual_width(line) for line in lines]
    assert len(set(widths)) == 1
    assert widths[0] == 60


def test_banner_dataclass_workflow():
    """Test using Banner dataclass directly."""
    renderer = BannerRenderer()

    banner = Banner(
        text="BANNER",
        font="standard",
        gradient_start="red",
        gradient_end="blue",
        border="solid",
        width=50,
    )

    lines = renderer.render_banner(banner)
    assert len(lines) > 0
    assert visual_width(lines[0]) == 50


def test_multiple_fonts():
    """Test rendering with multiple different fonts."""
    renderer = BannerRenderer()
    fonts = ["standard", "slant", "banner", "big"]

    outputs = {}
    for font in fonts:
        lines = renderer.render("X", font=font)
        outputs[font] = lines
        assert len(lines) > 0

    # Different fonts should produce different output
    assert len(set(tuple(lines) for lines in outputs.values())) == len(fonts)


def test_gradient_variations():
    """Test different gradient color combinations."""
    renderer = BannerRenderer()

    test_cases = [
        ("#ff0000", "#0000ff"),  # Red to blue (hex)
        ("red", "blue"),  # Named colors
        ("rgb(0,255,0)", "rgb(0,0,255)"),  # RGB format
        ("#00ff00", "yellow"),  # Mix of hex and named
    ]

    for start, end in test_cases:
        lines = renderer.render("X", gradient_start=start, gradient_end=end)
        assert len(lines) > 0
        # Should contain ANSI color codes
        assert any("\033[38;2;" in line for line in lines)


def test_border_consistency():
    """Test that all borders render with consistent width."""
    renderer = BannerRenderer()
    borders = ["solid", "double", "rounded", "heavy", "ascii"]

    for border_style in borders:
        lines = renderer.render("X", border=border_style, width=50)

        # All lines should have same visual width
        widths = [visual_width(line) for line in lines]
        assert len(set(widths)) == 1, f"Inconsistent widths for {border_style}"
        assert widths[0] == 50


def test_alignment_variations():
    """Test different alignment options."""
    renderer = BannerRenderer()

    for align in ["left", "center", "right"]:
        lines = renderer.render("TEST", border="solid", width=60, align=align)

        assert len(lines) > 0
        # All lines should have consistent width
        widths = [visual_width(line) for line in lines]
        assert len(set(widths)) == 1
        assert widths[0] == 60


def test_emoji_handling():
    """Test emoji text falls back gracefully."""
    renderer = BannerRenderer()

    # Emoji text
    emoji_lines = renderer.render("🚀")
    assert len(emoji_lines) == 1  # Should fallback to single line
    assert "🚀" in emoji_lines[0]

    # Emoji with gradient
    gradient_lines = renderer.render("🎉", gradient_start="red", gradient_end="blue")
    assert len(gradient_lines) == 1
    assert "🎉" in gradient_lines[0]
    assert "\033[38;2;" in gradient_lines[0]  # Should still have color

    # Emoji with border
    border_lines = renderer.render("✨", border="rounded")
    assert len(border_lines) == 3  # Top, content, bottom
    assert "✨" in border_lines[1]


def test_realistic_application_title():
    """Test realistic application title banner."""
    renderer = BannerRenderer()

    lines = renderer.render(
        "MyApp",
        font="slant",
        gradient_start="dodgerblue",
        gradient_end="purple",
        border="double",
        width=70,
    )

    # Should have proper structure
    assert len(lines) >= 3
    assert "═" in lines[0]  # Top border
    assert "═" in lines[-1]  # Bottom border

    # Should have gradient
    content = lines[1:-1]
    assert any("\033[38;2;" in line for line in content)

    # Consistent width
    assert all(visual_width(line) == 70 for line in lines)


def test_status_message_banners():
    """Test status message banners (success, error, warning)."""
    renderer = BannerRenderer()

    status_configs = [
        ("SUCCESS", "#00ff00", "#00aa00"),  # Green gradient
        ("ERROR", "#ff0000", "#aa0000"),  # Red gradient
        ("WARNING", "#ffaa00", "#ff6600"),  # Orange gradient
    ]

    for text, start, end in status_configs:
        lines = renderer.render(
            text,
            font="banner",
            gradient_start=start,
            gradient_end=end,
            border="heavy",
        )

        assert len(lines) >= 3
        assert "━" in lines[0]  # Heavy border
        assert any("\033[38;2;" in line for line in lines[1:-1])


def test_font_discovery():
    """Test font listing and preview utilities."""
    renderer = BannerRenderer()

    # List fonts
    all_fonts = renderer.list_fonts()
    assert len(all_fonts) > 0
    assert "standard" in all_fonts
    assert "slant" in all_fonts

    # Limited list
    limited = renderer.list_fonts(limit=10)
    assert len(limited) == 10

    # Preview font
    preview = renderer.preview_font("standard", "Test")
    assert isinstance(preview, str)
    assert len(preview) > 0


def test_long_text_handling():
    """Test handling of longer text strings."""
    renderer = BannerRenderer()

    long_text = "Hello World"
    lines = renderer.render(long_text, font="standard")

    assert len(lines) > 0
    # Should produce ASCII art
    max_width = max(len(strip_ansi(line)) for line in lines)
    assert max_width > len(long_text)  # ASCII art is wider than text


def test_special_characters():
    """Test rendering special characters."""
    renderer = BannerRenderer()

    test_strings = ["123", "ABC", "@#$", "v1.0"]

    for text in test_strings:
        lines = renderer.render(text, font="standard")
        assert len(lines) > 0


def test_padding_variations():
    """Test different padding values."""
    renderer = BannerRenderer()

    for padding in [1, 2, 3, 4]:
        lines = renderer.render(
            "X",
            font="standard",
            border="solid",
            width=50,
            padding=padding,
        )

        assert len(lines) >= 3
        assert all(visual_width(line) == 50 for line in lines)


def test_width_variations():
    """Test different width values."""
    renderer = BannerRenderer()

    widths = [40, 60, 80, 100]

    for width in widths:
        lines = renderer.render("X", border="solid", width=width)

        # All lines should match specified width
        assert all(visual_width(line) == width for line in lines)


def test_no_border_pure_ascii():
    """Test banner without border returns pure ASCII art."""
    renderer = BannerRenderer()

    lines = renderer.render("TEST", font="banner")

    # Should not have border characters
    assert not any("─" in line or "│" in line for line in lines)
    assert not any("═" in line or "║" in line for line in lines)
    assert not any("┌" in line or "└" in line for line in lines)


def test_gradient_interpolation_accuracy():
    """Test that gradient correctly interpolates across lines."""
    renderer = BannerRenderer()

    lines = renderer.render(
        "GRADIENT",
        font="banner",
        gradient_start="#ff0000",  # Pure red
        gradient_end="#0000ff",  # Pure blue
    )

    # Extract RGB values from ANSI codes
    rgb_values = []
    for line in lines:
        if "\033[38;2;" in line:
            parts = line.split("\033[38;2;")[1].split("m")[0].split(";")
            if len(parts) == 3:
                rgb_values.append(tuple(map(int, parts)))

    if len(rgb_values) > 1:
        # First line should be more red
        assert rgb_values[0][0] > rgb_values[0][2]  # R > B
        # Last line should be more blue
        assert rgb_values[-1][2] > rgb_values[-1][0]  # B > R


def test_combined_features():
    """Test combining multiple features together."""
    renderer = BannerRenderer()

    # Everything enabled
    lines = renderer.render(
        "FULL",
        font="slant",
        gradient_start="coral",
        gradient_end="dodgerblue",
        border="thick",
        width=65,
        align="center",
        padding=2,
    )

    # Should have all features
    assert len(lines) >= 3  # Border present
    assert any("\033[38;2;" in line for line in lines)  # Gradient present
    assert all(visual_width(line) == 65 for line in lines)  # Width correct
    # ASCII art should be visible (after stripping ANSI codes)
    clean_content = [strip_ansi(line) for line in lines[1:-1]]
    assert any(len(line.strip()) > 0 for line in clean_content)
