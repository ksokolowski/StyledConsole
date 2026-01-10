"""Tests for Theme system."""

import pytest

from styledconsole import DEFAULT_THEME, THEMES, Console, GradientSpec, Theme


class TestGradientSpec:
    """Tests for GradientSpec dataclass."""

    def test_gradient_spec_defaults(self):
        """Test GradientSpec default values."""
        spec = GradientSpec(start="red", end="blue")
        assert spec.start == "red"
        assert spec.end == "blue"
        assert spec.direction == "vertical"

    def test_gradient_spec_custom_direction(self):
        """Test GradientSpec with custom direction."""
        spec = GradientSpec(start="red", end="blue", direction="horizontal")
        assert spec.direction == "horizontal"

    def test_gradient_spec_is_frozen(self):
        """Test GradientSpec is immutable."""
        spec = GradientSpec(start="red", end="blue")
        from dataclasses import FrozenInstanceError

        with pytest.raises(FrozenInstanceError):
            spec.start = "green"


class TestTheme:
    """Tests for Theme dataclass."""

    def test_default_theme_values(self):
        """Test default theme has expected values."""
        theme = Theme()
        assert theme.name == "default"
        assert theme.primary == "cyan"
        assert theme.success == "green"
        assert theme.warning == "yellow"
        assert theme.error == "red"
        assert theme.info == "blue"
        assert theme.border == "white"

    def test_custom_theme(self):
        """Test creating custom theme."""
        theme = Theme(
            name="custom",
            primary="dodgerblue",
            success="lime",
            warning="gold",
            error="crimson",
        )
        assert theme.name == "custom"
        assert theme.primary == "dodgerblue"
        assert theme.success == "lime"
        assert theme.warning == "gold"
        assert theme.error == "crimson"

    def test_theme_is_frozen(self):
        """Test that Theme is immutable."""
        theme = Theme()
        with pytest.raises(AttributeError):
            theme.primary = "red"

    def test_get_color(self):
        """Test get_color method."""
        theme = Theme(primary="cyan", success="lime")
        assert theme.get_color("primary") == "cyan"
        assert theme.get_color("success") == "lime"
        assert theme.get_color("nonexistent") is None

    def test_resolve_color_semantic(self):
        """Test resolve_color with semantic names."""
        theme = Theme(success="lime", error="crimson")
        assert theme.resolve_color("success") == "lime"
        assert theme.resolve_color("error") == "crimson"

    def test_resolve_color_literal(self):
        """Test resolve_color with literal colors."""
        theme = Theme()
        assert theme.resolve_color("red") == "red"
        assert theme.resolve_color("#ff0000") == "#ff0000"
        assert theme.resolve_color("dodgerblue") == "dodgerblue"

    def test_resolve_color_none(self):
        """Test resolve_color with None."""
        theme = Theme()
        assert theme.resolve_color(None) is None

    def test_to_rich_theme(self):
        """Test conversion to Rich Theme."""
        theme = Theme(
            name="test",
            success="green",
            warning="yellow",
            error="red",
            primary="blue",
        )
        rich_theme = theme.to_rich_theme()

        from rich.theme import Theme as RichTheme

        assert isinstance(rich_theme, RichTheme)

        # Verify styles are generated correctly
        styles = rich_theme.styles
        assert str(styles["success"]) == "bold green"
        assert str(styles["warning"]) == "bold yellow"
        assert str(styles["error"]) == "bold red"
        assert str(styles["primary"]) == "blue"  # No modifier for primary


class TestThemesCollection:
    """Tests for THEMES predefined collection."""

    def test_dark_theme_exists(self):
        """Test DARK theme is available."""
        assert THEMES.DARK is not None
        assert THEMES.DARK.name == "dark"
        assert THEMES.DARK.primary == "cyan"

    def test_light_theme_exists(self):
        """Test LIGHT theme is available."""
        assert THEMES.LIGHT is not None
        assert THEMES.LIGHT.name == "light"
        assert THEMES.LIGHT.primary == "blue"

    def test_solarized_theme_exists(self):
        """Test SOLARIZED theme is available."""
        assert THEMES.SOLARIZED is not None
        assert THEMES.SOLARIZED.name == "solarized"

    def test_monokai_theme_exists(self):
        """Test MONOKAI theme is available."""
        assert THEMES.MONOKAI is not None
        assert THEMES.MONOKAI.name == "monokai"

    def test_nord_theme_exists(self):
        """Test NORD theme is available."""
        assert THEMES.NORD is not None
        assert THEMES.NORD.name == "nord"

    def test_dracula_theme_exists(self):
        """Test DRACULA theme is available."""
        assert THEMES.DRACULA is not None
        assert THEMES.DRACULA.name == "dracula"

    def test_all_themes(self):
        """Test THEMES.all() returns all themes."""
        all_themes = THEMES.all()
        assert len(all_themes) == 10  # 6 solid + 4 gradient themes
        names = {t.name for t in all_themes}
        expected = {
            "dark",
            "light",
            "solarized",
            "monokai",
            "nord",
            "dracula",
            "rainbow",
            "ocean",
            "sunset",
            "neon",
        }
        assert names == expected

    def test_solid_themes(self):
        """Test THEMES.solid_themes() returns only non-gradient themes."""
        solid = THEMES.solid_themes()
        assert len(solid) == 6
        for theme in solid:
            assert not theme.has_gradients()

    def test_gradient_themes(self):
        """Test THEMES.gradient_themes() returns only gradient themes."""
        gradient = THEMES.gradient_themes()
        assert len(gradient) == 4
        names = {t.name for t in gradient}
        assert names == {"rainbow", "ocean", "sunset", "neon"}
        for theme in gradient:
            assert theme.has_gradients()

    def test_get_theme_by_name(self):
        """Test THEMES.get() lookup."""
        assert THEMES.get("dark") == THEMES.DARK
        assert THEMES.get("DARK") == THEMES.DARK  # Case insensitive
        assert THEMES.get("monokai") == THEMES.MONOKAI
        assert THEMES.get("nonexistent") is None


class TestConsoleTheme:
    """Tests for Console theme integration."""

    def test_console_default_theme(self):
        """Test Console uses default theme when none specified."""
        console = Console()
        assert console.theme == DEFAULT_THEME

    def test_console_with_theme_instance(self):
        """Test Console with Theme instance."""
        console = Console(theme=THEMES.DARK)
        assert console.theme == THEMES.DARK

    def test_console_with_theme_string(self):
        """Test Console with theme name string."""
        console = Console(theme="monokai")
        assert console.theme == THEMES.MONOKAI

    def test_console_with_invalid_theme_string(self):
        """Test Console with invalid theme name falls back to default."""
        console = Console(theme="nonexistent")
        assert console.theme == DEFAULT_THEME

    def test_console_with_custom_theme(self):
        """Test Console with custom Theme instance."""
        custom = Theme(name="custom", primary="purple")
        console = Console(theme=custom)
        assert console.theme == custom
        assert console.theme.primary == "purple"

    def test_console_resolve_color(self):
        """Test Console.resolve_color() method."""
        console = Console(theme=THEMES.DARK)
        assert console.resolve_color("success") == "bright_green"
        assert console.resolve_color("red") == "red"
        assert console.resolve_color(None) is None

    def test_console_theme_markup(self):
        """Test Console properly configures Rich with theme styles."""
        console = Console(theme=THEMES.DARK)

        # Verify it has our styles using get_style()
        # This confirms the theme was loaded into the Console
        success_style = console._rich_console.get_style("success")
        assert str(success_style) == "bold bright_green"

        error_style = console._rich_console.get_style("error")
        assert str(error_style) == "bold red"


class TestThemeColors:
    """Tests for theme color values."""

    def test_dark_theme_colors(self):
        """Test DARK theme has appropriate colors."""
        theme = THEMES.DARK
        assert theme.success == "bright_green"
        assert theme.warning == "yellow"
        assert theme.error == "red"
        assert theme.border == "white"

    def test_light_theme_colors(self):
        """Test LIGHT theme has appropriate colors."""
        theme = THEMES.LIGHT
        assert theme.success == "green"
        assert theme.warning == "yellow"
        assert theme.error == "red"
        assert theme.border == "bright_black"

    def test_themes_have_all_semantic_colors(self):
        """Test all themes define all semantic colors."""
        required = ["primary", "secondary", "success", "warning", "error", "info", "border"]
        for theme in THEMES.all():
            for color_name in required:
                value = theme.get_color(color_name)
                assert value is not None, f"{theme.name} missing {color_name}"


class TestThemeGradients:
    """Tests for theme gradient support."""

    def test_theme_with_gradients(self):
        """Test creating theme with gradient specifications."""
        theme = Theme(
            name="custom_gradient",
            border_gradient=GradientSpec("red", "blue"),
            banner_gradient=GradientSpec("green", "yellow"),
            text_gradient=GradientSpec("cyan", "magenta"),
        )
        assert theme.border_gradient is not None
        assert theme.border_gradient.start == "red"
        assert theme.border_gradient.end == "blue"
        assert theme.banner_gradient.start == "green"
        assert theme.text_gradient.start == "cyan"

    def test_theme_has_gradients(self):
        """Test has_gradients() method."""
        theme_no_gradient = Theme(name="plain")
        assert not theme_no_gradient.has_gradients()

        theme_with_gradient = Theme(
            name="gradient",
            border_gradient=GradientSpec("red", "blue"),
        )
        assert theme_with_gradient.has_gradients()

    def test_rainbow_theme_has_all_gradients(self):
        """Test RAINBOW theme has all gradient types."""
        theme = THEMES.RAINBOW
        assert theme.border_gradient is not None
        assert theme.banner_gradient is not None
        assert theme.text_gradient is not None

    def test_gradient_themes_have_gradients(self):
        """Test all gradient themes have at least one gradient."""
        for theme in [THEMES.RAINBOW, THEMES.OCEAN, THEMES.SUNSET, THEMES.NEON]:
            assert theme.has_gradients(), f"{theme.name} should have gradients"
            assert theme.border_gradient is not None
            assert theme.banner_gradient is not None

    def test_solid_themes_no_gradients(self):
        """Test solid themes don't have gradients."""
        for theme in [
            THEMES.DARK,
            THEMES.LIGHT,
            THEMES.SOLARIZED,
            THEMES.MONOKAI,
            THEMES.NORD,
            THEMES.DRACULA,
        ]:
            assert not theme.has_gradients(), f"{theme.name} should not have gradients"
