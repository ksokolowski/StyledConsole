"""Tests for the Effects System (v0.9.9.2+).

Tests cover:
- EffectSpec dataclass and factory methods
- EffectRegistry and EFFECTS presets
- MultiStopGradient and EnhancedRainbow strategies
- resolve_effect() bridge function
"""

import pytest

from styledconsole.effects import (
    EFFECTS,
    EffectRegistry,
    EffectSpec,
    EnhancedRainbow,
    LinearGradient,
    MultiStopGradient,
    RainbowSpectrum,
    ReversedColorSource,
    resolve_effect,
)

# =============================================================================
# EffectSpec Tests
# =============================================================================


class TestEffectSpec:
    """Tests for EffectSpec dataclass."""

    def test_gradient_factory(self):
        """Test EffectSpec.gradient() factory method."""
        spec = EffectSpec.gradient("red", "blue")

        assert spec.name == "gradient"
        assert spec.colors == ("red", "blue")
        assert spec.direction == "vertical"
        assert spec.target == "both"
        assert spec.layer == "foreground"
        assert spec.reverse is False

    def test_gradient_with_options(self):
        """Test gradient factory with custom options."""
        spec = EffectSpec.gradient(
            "cyan",
            "magenta",
            direction="horizontal",
            target="border",
            reverse=True,
        )

        assert spec.direction == "horizontal"
        assert spec.target == "border"
        assert spec.reverse is True

    def test_multi_stop_factory(self):
        """Test EffectSpec.multi_stop() factory method."""
        spec = EffectSpec.multi_stop(["red", "yellow", "green"])

        assert spec.name == "multi_stop"
        assert spec.colors == ("red", "yellow", "green")
        assert spec.is_multi_stop() is True
        assert spec.is_gradient() is True

    def test_multi_stop_requires_two_colors(self):
        """Test that multi_stop requires at least 2 colors."""
        with pytest.raises(ValueError, match="at least 2 colors"):
            EffectSpec.multi_stop(["red"])

    def test_rainbow_factory(self):
        """Test EffectSpec.rainbow() factory method."""
        spec = EffectSpec.rainbow()

        assert spec.name == "rainbow"
        assert spec.colors == ()
        assert spec.saturation == 1.0
        assert spec.brightness == 1.0
        assert spec.reverse is False
        assert spec.is_rainbow() is True

    def test_rainbow_with_options(self):
        """Test rainbow factory with custom options."""
        spec = EffectSpec.rainbow(
            saturation=0.5,
            brightness=1.2,
            reverse=True,
            direction="diagonal",
        )

        assert spec.saturation == 0.5
        assert spec.brightness == 1.2
        assert spec.reverse is True
        assert spec.direction == "diagonal"

    def test_is_gradient(self):
        """Test is_gradient() method."""
        gradient = EffectSpec.gradient("red", "blue")
        multi = EffectSpec.multi_stop(["red", "yellow", "blue"])
        rainbow = EffectSpec.rainbow()

        assert gradient.is_gradient() is True
        assert multi.is_gradient() is True
        assert rainbow.is_gradient() is False

    def test_is_rainbow(self):
        """Test is_rainbow() method."""
        gradient = EffectSpec.gradient("red", "blue")
        rainbow = EffectSpec.rainbow()

        assert gradient.is_rainbow() is False
        assert rainbow.is_rainbow() is True

    def test_with_direction(self):
        """Test with_direction() returns new spec."""
        original = EffectSpec.gradient("red", "blue")
        modified = original.with_direction("horizontal")

        assert original.direction == "vertical"
        assert modified.direction == "horizontal"
        assert original is not modified

    def test_with_target(self):
        """Test with_target() returns new spec."""
        original = EffectSpec.gradient("red", "blue")
        modified = original.with_target("border")

        assert original.target == "both"
        assert modified.target == "border"
        assert original is not modified

    def test_reversed(self):
        """Test reversed() returns new spec with reverse toggled."""
        original = EffectSpec.gradient("red", "blue")
        reversed_spec = original.reversed()

        assert original.reverse is False
        assert reversed_spec.reverse is True

    def test_frozen_immutable(self):
        """Test that EffectSpec is immutable."""
        spec = EffectSpec.gradient("red", "blue")

        with pytest.raises(AttributeError):
            spec.name = "other"  # type: ignore


# =============================================================================
# EffectRegistry Tests
# =============================================================================


class TestEffectRegistry:
    """Tests for EffectRegistry and EFFECTS global."""

    def test_effects_has_presets(self):
        """Test that EFFECTS contains registered presets."""
        assert len(EFFECTS) > 0
        assert "fire" in EFFECTS
        assert "rainbow" in EFFECTS
        assert "ocean" in EFFECTS

    def test_attribute_access(self):
        """Test attribute-style access to effects."""
        fire = EFFECTS.fire

        assert isinstance(fire, EffectSpec)
        assert fire.name == "multi_stop"

    def test_dict_access(self):
        """Test dict-style access to effects."""
        ocean = EFFECTS["ocean"]

        assert isinstance(ocean, EffectSpec)

    def test_get_method(self):
        """Test get() method."""
        rainbow = EFFECTS.get("rainbow")

        assert isinstance(rainbow, EffectSpec)
        assert rainbow.is_rainbow() is True

    def test_unknown_preset_raises(self):
        """Test that unknown preset raises KeyError."""
        with pytest.raises(KeyError):
            EFFECTS.get("nonexistent_preset")

    def test_list_all(self):
        """Test list_all() returns sorted list."""
        all_effects = EFFECTS.list_all()

        assert isinstance(all_effects, list)
        assert len(all_effects) > 20  # We registered 30+ presets
        assert all_effects == sorted(all_effects)

    def test_gradients_filter(self):
        """Test gradients() returns only gradient effects."""
        gradients = EFFECTS.gradients()

        assert len(gradients) > 0
        for effect in gradients:
            assert effect.is_gradient() is True

    def test_rainbows_filter(self):
        """Test rainbows() returns only rainbow effects."""
        rainbows = EFFECTS.rainbows()

        assert len(rainbows) > 0
        for effect in rainbows:
            assert effect.is_rainbow() is True

    def test_custom_registry(self):
        """Test creating a custom EffectRegistry."""
        registry = EffectRegistry()
        registry.register("custom", EffectSpec.gradient("pink", "purple"))

        assert "custom" in registry
        assert registry.custom.colors == ("pink", "purple")


# =============================================================================
# Strategy Tests
# =============================================================================


class TestMultiStopGradient:
    """Tests for MultiStopGradient strategy."""

    def test_three_colors(self):
        """Test gradient with three colors."""
        gradient = MultiStopGradient(["#ff0000", "#00ff00", "#0000ff"])

        # Start (red)
        color_0 = gradient.get_color(0.0)
        assert color_0.lower() == "#ff0000"

        # Middle (green)
        color_50 = gradient.get_color(0.5)
        assert color_50.lower() == "#00ff00"

        # End (blue)
        color_100 = gradient.get_color(1.0)
        assert color_100.lower() == "#0000ff"

    def test_interpolation_between_stops(self):
        """Test color interpolation between stops."""
        gradient = MultiStopGradient(["#000000", "#ffffff"])

        # 50% should be gray
        color = gradient.get_color(0.5)
        # Should be approximately #808080 (may vary slightly)
        assert color.startswith("#")

    def test_requires_two_colors(self):
        """Test that at least 2 colors are required."""
        with pytest.raises(ValueError, match="at least 2 colors"):
            MultiStopGradient(["red"])

    def test_custom_positions(self):
        """Test gradient with custom positions."""
        gradient = MultiStopGradient(
            ["#ff0000", "#00ff00", "#0000ff"],
            positions=[0.0, 0.2, 1.0],  # Green appears early
        )

        # At 0.2, should be green
        color = gradient.get_color(0.2)
        assert color.lower() == "#00ff00"

    def test_position_clamping(self):
        """Test that positions outside 0-1 are clamped."""
        gradient = MultiStopGradient(["#ff0000", "#0000ff"])

        # Below 0 should return start color
        color_neg = gradient.get_color(-0.5)
        assert color_neg.lower() == "#ff0000"

        # Above 1 should return end color
        color_over = gradient.get_color(1.5)
        assert color_over.lower() == "#0000ff"


class TestEnhancedRainbow:
    """Tests for EnhancedRainbow strategy."""

    def test_default_returns_rainbow_colors(self):
        """Test default rainbow returns ROYGBIV colors."""
        rainbow = EnhancedRainbow()

        color_0 = rainbow.get_color(0.0)
        color_100 = rainbow.get_color(1.0)

        # Should return hex colors
        assert color_0.startswith("#")
        assert color_100.startswith("#")

    def test_reverse_option(self):
        """Test that reverse reverses the rainbow."""
        normal = EnhancedRainbow()
        reversed_rainbow = EnhancedRainbow(reverse=True)

        normal_start = normal.get_color(0.0)
        reversed_end = reversed_rainbow.get_color(1.0)

        # Reversed end should match normal start
        assert normal_start == reversed_end

    def test_saturation_adjustment(self):
        """Test saturation adjustment produces different colors."""
        normal = EnhancedRainbow()
        desaturated = EnhancedRainbow(saturation=0.5)

        normal_color = normal.get_color(0.5)
        desat_color = desaturated.get_color(0.5)

        # Colors should be different
        assert normal_color != desat_color

    def test_no_adjustment_uses_base_rainbow(self):
        """Test that default params use simple RainbowSpectrum."""
        enhanced = EnhancedRainbow()
        simple = RainbowSpectrum()

        # Should produce same colors when no adjustments
        for pos in [0.0, 0.25, 0.5, 0.75, 1.0]:
            assert enhanced.get_color(pos) == simple.get_color(pos)


class TestReversedColorSource:
    """Tests for ReversedColorSource wrapper."""

    def test_reverses_gradient(self):
        """Test that ReversedColorSource reverses a gradient."""
        original = LinearGradient("#ff0000", "#0000ff")
        reversed_source = ReversedColorSource(original)

        # Original: 0.0 = red, 1.0 = blue
        # Reversed: 0.0 = blue, 1.0 = red
        assert reversed_source.get_color(0.0).lower() == "#0000ff"
        assert reversed_source.get_color(1.0).lower() == "#ff0000"


# =============================================================================
# Resolver Tests
# =============================================================================


class TestResolveEffect:
    """Tests for resolve_effect() bridge function."""

    def test_resolve_from_string(self):
        """Test resolving effect from preset name."""
        position, color, target, layer = resolve_effect("fire")

        assert position is not None
        assert color is not None
        assert target is not None
        assert layer in ("foreground", "background")

    def test_resolve_from_spec(self):
        """Test resolving effect from EffectSpec."""
        spec = EffectSpec.gradient("cyan", "magenta")
        _position, color, _target, _layer = resolve_effect(spec)

        assert isinstance(color, LinearGradient)

    def test_resolve_rainbow(self):
        """Test resolving rainbow effect."""
        spec = EffectSpec.rainbow(saturation=0.5)
        _position, color, _target, _layer = resolve_effect(spec)

        assert isinstance(color, EnhancedRainbow)

    def test_resolve_multi_stop(self):
        """Test resolving multi-stop gradient."""
        spec = EffectSpec.multi_stop(["red", "yellow", "green"])
        _position, color, _target, _layer = resolve_effect(spec)

        assert isinstance(color, MultiStopGradient)

    def test_unknown_preset_raises(self):
        """Test that unknown preset raises KeyError."""
        with pytest.raises(KeyError):
            resolve_effect("nonexistent")

    def test_invalid_type_raises(self):
        """Test that invalid type raises TypeError."""
        with pytest.raises(TypeError):
            resolve_effect(123)  # type: ignore

    def test_direction_mapping(self):
        """Test that direction is correctly mapped."""
        from styledconsole.effects import DiagonalPosition, HorizontalPosition, VerticalPosition

        spec_v = EffectSpec.gradient("a", "b", direction="vertical")
        spec_h = EffectSpec.gradient("a", "b", direction="horizontal")
        spec_d = EffectSpec.gradient("a", "b", direction="diagonal")

        pos_v, _, _, _ = resolve_effect(spec_v)
        pos_h, _, _, _ = resolve_effect(spec_h)
        pos_d, _, _, _ = resolve_effect(spec_d)

        assert isinstance(pos_v, VerticalPosition)
        assert isinstance(pos_h, HorizontalPosition)
        assert isinstance(pos_d, DiagonalPosition)

    def test_target_mapping(self):
        """Test that target is correctly mapped."""
        from styledconsole.effects import BorderOnly, Both, ContentOnly

        spec_c = EffectSpec.gradient("a", "b", target="content")
        spec_b = EffectSpec.gradient("a", "b", target="border")
        spec_both = EffectSpec.gradient("a", "b", target="both")

        _, _, target_c, _ = resolve_effect(spec_c)
        _, _, target_b, _ = resolve_effect(spec_b)
        _, _, target_both, _ = resolve_effect(spec_both)

        assert isinstance(target_c, ContentOnly)
        assert isinstance(target_b, BorderOnly)
        assert isinstance(target_both, Both)


# =============================================================================
# Integration Tests
# =============================================================================


class TestEffectsIntegration:
    """Integration tests for the effects system."""

    def test_preset_to_strategies(self):
        """Test full flow from preset to strategies."""
        # Get a preset
        fire = EFFECTS.fire

        # Resolve to strategies
        _position, color, _target, _layer = resolve_effect(fire)

        # Use the color source
        start_color = color.get_color(0.0)
        end_color = color.get_color(1.0)

        # Should produce valid hex colors
        assert start_color.startswith("#")
        assert end_color.startswith("#")

    def test_custom_spec_to_strategies(self):
        """Test custom EffectSpec through resolver."""
        spec = EffectSpec.multi_stop(
            ["#ff0000", "#ffff00", "#00ff00"],
            direction="horizontal",
            target="border",
        )

        position, color, target, layer = resolve_effect(spec)

        # Verify correct types
        from styledconsole.effects import BorderOnly, HorizontalPosition

        assert isinstance(position, HorizontalPosition)
        assert isinstance(color, MultiStopGradient)
        assert isinstance(target, BorderOnly)
        assert layer == "foreground"

    def test_layer_resolution(self):
        """Test that layer is correctly resolved."""
        spec_fg = EffectSpec.gradient("a", "b", layer="foreground")
        spec_bg = EffectSpec.gradient("a", "b", layer="background")

        _, _, _, layer_fg = resolve_effect(spec_fg)
        _, _, _, layer_bg = resolve_effect(spec_bg)

        assert layer_fg == "foreground"
        assert layer_bg == "background"
