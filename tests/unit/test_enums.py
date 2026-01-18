"""Tests for styledconsole.enums module."""

import pytest

from styledconsole import (
    Align,
    Border,
    Console,
    Direction,
    Effect,
    ExportFormat,
    LayoutMode,
    Target,
)
from styledconsole.core.styles import BORDERS
from styledconsole.effects import EFFECTS


class TestBorderEnum:
    """Tests for Border enum."""

    def test_border_values_match_registry(self):
        """Border enum values should match BORDERS registry keys."""
        registry_keys = set(BORDERS.list_all())
        enum_values = {b.value for b in Border}
        assert enum_values == registry_keys

    def test_border_is_str(self):
        """Border enum values should be usable as strings."""
        assert Border.ROUNDED == "rounded"
        assert Border.DOUBLE == "double"
        assert isinstance(Border.SOLID, str)

    def test_border_with_console(self, capsys):
        """Border enum should work with Console.frame()."""
        console = Console()
        # Should not raise - output goes to stdout
        console.frame("Test", border=Border.ROUNDED)
        console.frame("Test", border=Border.DOUBLE)
        console.frame("Test", border=Border.ASCII)
        captured = capsys.readouterr()
        assert "Test" in captured.out

    @pytest.mark.parametrize("border", list(Border))
    def test_all_borders_valid(self, border: Border, capsys):
        """All Border enum values should work with Console."""
        console = Console()
        console.frame("Test", border=border)
        captured = capsys.readouterr()
        assert "Test" in captured.out


class TestEffectEnum:
    """Tests for Effect enum."""

    def test_effect_values_match_registry(self):
        """Effect enum values should match EFFECTS registry keys."""
        registry_keys = set(EFFECTS.list_all())
        enum_values = {e.value for e in Effect}
        # Enum should be subset of registry (registry may have more)
        assert enum_values.issubset(registry_keys), (
            f"Missing from registry: {enum_values - registry_keys}"
        )

    def test_effect_is_str(self):
        """Effect enum values should be usable as strings."""
        assert Effect.FIRE == "fire"
        assert Effect.OCEAN == "ocean"
        assert isinstance(Effect.RAINBOW, str)

    def test_effect_with_console(self, capsys):
        """Effect enum should work with Console.frame()."""
        console = Console()
        # Should not raise
        console.frame("Test", effect=Effect.FIRE)
        console.frame("Test", effect=Effect.OCEAN)
        console.frame("Test", effect=Effect.RAINBOW)
        captured = capsys.readouterr()
        assert "Test" in captured.out

    def test_effect_categories(self):
        """Effect enum should have all expected categories."""
        # Gradients
        assert Effect.FIRE.value == "fire"
        assert Effect.OCEAN.value == "ocean"

        # Rainbows
        assert Effect.RAINBOW.value == "rainbow"
        assert Effect.RAINBOW_NEON.value == "rainbow_neon"

        # Themed
        assert Effect.MATRIX.value == "matrix"
        assert Effect.CYBERPUNK.value == "cyberpunk"

        # Semantic
        assert Effect.SUCCESS.value == "success"
        assert Effect.ERROR.value == "error"

        # Border-only
        assert Effect.BORDER_FIRE.value == "border_fire"


class TestAlignEnum:
    """Tests for Align enum."""

    def test_align_values(self):
        """Align enum should have expected values."""
        assert Align.LEFT == "left"
        assert Align.CENTER == "center"
        assert Align.RIGHT == "right"

    def test_align_is_str(self):
        """Align enum values should be usable as strings."""
        assert isinstance(Align.LEFT, str)
        assert isinstance(Align.CENTER, str)

    def test_align_count(self):
        """Align enum should have exactly 3 values."""
        assert len(Align) == 3


class TestDirectionEnum:
    """Tests for Direction enum."""

    def test_direction_values(self):
        """Direction enum should have expected values."""
        assert Direction.VERTICAL == "vertical"
        assert Direction.HORIZONTAL == "horizontal"
        assert Direction.DIAGONAL == "diagonal"

    def test_direction_count(self):
        """Direction enum should have exactly 3 values."""
        assert len(Direction) == 3


class TestTargetEnum:
    """Tests for Target enum."""

    def test_target_values(self):
        """Target enum should have expected values."""
        assert Target.CONTENT == "content"
        assert Target.BORDER == "border"
        assert Target.BOTH == "both"

    def test_target_count(self):
        """Target enum should have exactly 3 values."""
        assert len(Target) == 3


class TestLayoutModeEnum:
    """Tests for LayoutMode enum."""

    def test_layout_mode_values(self):
        """LayoutMode enum should have expected values."""
        assert LayoutMode.VERTICAL == "vertical"
        assert LayoutMode.HORIZONTAL == "horizontal"
        assert LayoutMode.GRID == "grid"

    def test_layout_mode_count(self):
        """LayoutMode enum should have exactly 3 values."""
        assert len(LayoutMode) == 3


class TestExportFormatEnum:
    """Tests for ExportFormat enum."""

    def test_export_format_values(self):
        """ExportFormat enum should have expected values."""
        assert ExportFormat.HTML == "html"
        assert ExportFormat.TEXT == "text"
        assert ExportFormat.PNG == "png"
        assert ExportFormat.WEBP == "webp"
        assert ExportFormat.GIF == "gif"

    def test_export_format_count(self):
        """ExportFormat enum should have exactly 5 values."""
        assert len(ExportFormat) == 5


class TestEnumBackwardCompatibility:
    """Tests for backward compatibility with string values."""

    def test_string_border_still_works(self, capsys):
        """String border values should still work."""
        console = Console()
        console.frame("Test", border="rounded")
        console.frame("Test", border="double")
        captured = capsys.readouterr()
        assert "Test" in captured.out

    def test_string_effect_still_works(self, capsys):
        """String effect values should still work."""
        console = Console()
        console.frame("Test", effect="fire")
        console.frame("Test", effect="ocean")
        captured = capsys.readouterr()
        assert "Test" in captured.out

    def test_enum_equals_string(self):
        """Enum values should equal their string counterparts."""
        assert Border.ROUNDED == "rounded"
        assert Effect.FIRE == "fire"
        assert Align.CENTER == "center"

    def test_string_in_enum(self):
        """String values should be found in enum."""
        assert "rounded" in [b.value for b in Border]
        assert "fire" in [e.value for e in Effect]
