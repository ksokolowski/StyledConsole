"""Tests for effect= parameter integration in Console API.

v0.9.9.3: Effect system integration into Console.frame() and Console.banner().
"""

from __future__ import annotations

import warnings

import pytest

from styledconsole import EFFECTS, Console, EffectSpec


class TestFrameEffectParameter:
    """Tests for Console.frame() effect= parameter."""

    def test_frame_with_effect_preset_name(self) -> None:
        """Frame accepts effect preset by name."""
        console = Console(record=True)
        console.frame("Hello", effect="fire")
        output = console.export_text()
        assert "Hello" in output

    def test_frame_with_effect_spec(self) -> None:
        """Frame accepts EffectSpec directly."""
        console = Console(record=True)
        spec = EffectSpec.gradient("red", "blue")
        console.frame("Hello", effect=spec)
        output = console.export_text()
        assert "Hello" in output

    def test_frame_with_effects_registry(self) -> None:
        """Frame accepts EFFECTS registry item."""
        console = Console(record=True)
        console.frame("Hello", effect=EFFECTS.ocean)
        output = console.export_text()
        assert "Hello" in output

    def test_frame_with_rainbow_effect(self) -> None:
        """Frame accepts rainbow effect presets."""
        console = Console(record=True)
        console.frame("Rainbow", effect="rainbow")
        output = console.export_text()
        assert "Rainbow" in output

    def test_frame_with_rainbow_variations(self) -> None:
        """Frame accepts rainbow variation presets."""
        console = Console(record=True)
        for preset in ["rainbow_pastel", "rainbow_neon", "rainbow_muted"]:
            console.frame(f"Test {preset}", effect=preset)
        output = console.export_text()
        assert "Test rainbow_pastel" in output

    def test_frame_with_multi_stop_effect(self) -> None:
        """Frame accepts multi-stop gradient effects."""
        console = Console(record=True)
        console.frame("Multi-stop", effect="vaporwave")
        output = console.export_text()
        assert "Multi-stop" in output

    def test_frame_with_border_only_effect(self) -> None:
        """Frame accepts border-only effect presets."""
        console = Console(record=True)
        console.frame("Border only", effect="border_fire")
        output = console.export_text()
        assert "Border only" in output

    def test_frame_with_custom_horizontal_effect(self) -> None:
        """Frame accepts custom horizontal gradient."""
        console = Console(record=True)
        spec = EffectSpec.gradient("cyan", "magenta", direction="horizontal")
        console.frame("Horizontal", effect=spec)
        output = console.export_text()
        assert "Horizontal" in output

    def test_frame_with_invalid_effect_raises(self) -> None:
        """Frame raises KeyError for unknown effect preset."""
        console = Console(record=True)
        with pytest.raises(KeyError, match="Unknown effect"):
            console.frame("Test", effect="nonexistent_effect")

    def test_frame_effect_overrides_legacy_params(self) -> None:
        """Effect parameter takes precedence over legacy gradient params."""
        console = Console(record=True)
        # Even if legacy params are provided, effect= should be used
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            console.frame(
                "Test",
                effect="fire",
                start_color="green",  # Should be ignored
                end_color="yellow",  # Should be ignored
            )
        output = console.export_text()
        assert "Test" in output


class TestFrameDeprecationWarnings:
    """Tests for deprecation warnings on legacy gradient params."""

    def test_start_end_color_deprecation(self) -> None:
        """start_color/end_color emit deprecation warning."""
        console = Console(record=True)
        with pytest.warns(DeprecationWarning, match="start_color/end_color are deprecated"):
            console.frame("Test", start_color="red", end_color="blue")

    def test_border_gradient_deprecation(self) -> None:
        """border_gradient_start/end emit deprecation warning."""
        console = Console(record=True)
        with pytest.warns(DeprecationWarning, match="border_gradient_start/end are deprecated"):
            console.frame("Test", border_gradient_start="cyan", border_gradient_end="magenta")

    def test_legacy_params_still_work(self) -> None:
        """Legacy gradient params still produce output."""
        console = Console(record=True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            console.frame("Legacy", start_color="red", end_color="blue")
        output = console.export_text()
        assert "Legacy" in output


class TestBannerEffectParameter:
    """Tests for Console.banner() effect= parameter."""

    def test_banner_with_effect_preset_name(self) -> None:
        """Banner accepts effect preset by name."""
        console = Console(record=True)
        console.banner("TEST", effect="fire")
        output = console.export_text()
        assert len(output) > 0

    def test_banner_with_rainbow_effect(self) -> None:
        """Banner accepts rainbow effect preset."""
        console = Console(record=True)
        console.banner("RAINBOW", effect="rainbow")
        output = console.export_text()
        assert len(output) > 0

    def test_banner_with_rainbow_neon(self) -> None:
        """Banner accepts rainbow_neon effect preset."""
        console = Console(record=True)
        console.banner("NEON", effect="rainbow_neon")
        output = console.export_text()
        assert len(output) > 0

    def test_banner_with_effect_spec(self) -> None:
        """Banner accepts EffectSpec directly."""
        console = Console(record=True)
        spec = EffectSpec.gradient("cyan", "magenta")
        console.banner("SPEC", effect=spec)
        output = console.export_text()
        assert len(output) > 0

    def test_banner_with_effects_registry(self) -> None:
        """Banner accepts EFFECTS registry item."""
        console = Console(record=True)
        console.banner("OCEAN", effect=EFFECTS.ocean)
        output = console.export_text()
        assert len(output) > 0

    def test_banner_with_invalid_effect_raises(self) -> None:
        """Banner raises KeyError for unknown effect preset."""
        console = Console(record=True)
        with pytest.raises(KeyError, match="Unknown effect"):
            console.banner("TEST", effect="nonexistent_effect")


class TestBannerDeprecationWarnings:
    """Tests for deprecation warnings on legacy banner params."""

    def test_rainbow_bool_deprecation(self) -> None:
        """rainbow=True emits deprecation warning."""
        console = Console(record=True)
        with pytest.warns(DeprecationWarning, match="rainbow=True is deprecated"):
            console.banner("TEST", rainbow=True)

    def test_start_end_color_deprecation(self) -> None:
        """start_color/end_color emit deprecation warning."""
        console = Console(record=True)
        with pytest.warns(DeprecationWarning, match="start_color/end_color are deprecated"):
            console.banner("TEST", start_color="red", end_color="blue")

    def test_legacy_rainbow_still_works(self) -> None:
        """Legacy rainbow=True still produces output."""
        console = Console(record=True)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            console.banner("LEGACY", rainbow=True)
        output = console.export_text()
        assert len(output) > 0


class TestEffectImports:
    """Tests for effect system public API imports."""

    def test_effects_import_from_main(self) -> None:
        """EFFECTS can be imported from styledconsole."""
        from styledconsole import EFFECTS

        assert hasattr(EFFECTS, "fire")
        assert hasattr(EFFECTS, "ocean")
        assert hasattr(EFFECTS, "rainbow")

    def test_effectspec_import_from_main(self) -> None:
        """EffectSpec can be imported from styledconsole."""
        from styledconsole import EffectSpec

        spec = EffectSpec.gradient("red", "blue")
        assert spec.colors == ("red", "blue")

    def test_effects_import_from_effects_module(self) -> None:
        """EFFECTS can be imported from styledconsole.effects."""
        from styledconsole.effects import EFFECTS

        assert len(EFFECTS.list_all()) >= 30

    def test_effectspec_import_from_effects_module(self) -> None:
        """EffectSpec can be imported from styledconsole.effects."""
        from styledconsole.effects import EffectSpec

        spec = EffectSpec.rainbow()
        assert spec.is_rainbow()


class TestAllEffectPresets:
    """Tests that all registered effect presets work with frame()."""

    def test_all_gradient_presets(self) -> None:
        """All gradient presets work with frame()."""
        console = Console(record=True)
        gradient_presets = [
            "fire",
            "ocean",
            "sunset",
            "forest",
            "aurora",
            "lavender",
            "peach",
            "mint",
            "steel",
            "gold",
        ]
        for preset in gradient_presets:
            console.frame(f"Test {preset}", effect=preset)
        output = console.export_text()
        assert "Test fire" in output

    def test_all_rainbow_presets(self) -> None:
        """All rainbow presets work with frame()."""
        console = Console(record=True)
        rainbow_presets = [
            "rainbow",
            "rainbow_pastel",
            "rainbow_neon",
            "rainbow_muted",
            "rainbow_reverse",
            "rainbow_horizontal",
            "rainbow_diagonal",
        ]
        for preset in rainbow_presets:
            console.frame(f"Test {preset}", effect=preset)
        output = console.export_text()
        assert "Test rainbow" in output

    def test_all_themed_presets(self) -> None:
        """All themed presets work with frame()."""
        console = Console(record=True)
        themed_presets = [
            "matrix",
            "cyberpunk",
            "retro",
            "vaporwave",
            "dracula",
            "nord_aurora",
        ]
        for preset in themed_presets:
            console.frame(f"Test {preset}", effect=preset)
        output = console.export_text()
        assert "Test matrix" in output

    def test_all_semantic_presets(self) -> None:
        """All semantic presets work with frame()."""
        console = Console(record=True)
        semantic_presets = ["success", "warning", "error", "info", "neutral"]
        for preset in semantic_presets:
            console.frame(f"Test {preset}", effect=preset)
        output = console.export_text()
        assert "Test success" in output

    def test_all_border_presets(self) -> None:
        """All border-only presets work with frame()."""
        console = Console(record=True)
        border_presets = ["border_fire", "border_ocean", "border_rainbow", "border_gold"]
        for preset in border_presets:
            console.frame(f"Test {preset}", effect=preset)
        output = console.export_text()
        assert "Test border_fire" in output
