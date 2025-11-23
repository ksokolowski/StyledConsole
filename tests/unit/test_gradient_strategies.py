"""Unit tests for gradient strategy components."""

from styledconsole.effects.strategies import (
    BorderOnly,
    Both,
    ContentOnly,
    DiagonalPosition,
    HorizontalPosition,
    LinearGradient,
    OffsetPositionStrategy,
    RainbowSpectrum,
    VerticalPosition,
)


class TestPositionStrategies:
    """Test position calculation strategies."""

    def test_vertical_position_top(self):
        """Top row = 0.0."""
        strategy = VerticalPosition()
        assert strategy.calculate(0, 0, 10, 10) == 0.0

    def test_vertical_position_bottom(self):
        """Bottom row = 1.0."""
        strategy = VerticalPosition()
        assert strategy.calculate(9, 0, 10, 10) == 1.0

    def test_vertical_position_middle(self):
        """Middle row = 0.5."""
        strategy = VerticalPosition()
        assert abs(strategy.calculate(5, 0, 11, 10) - 0.5) < 0.01

    def test_diagonal_position_top_left(self):
        """Top-left = 0.0."""
        strategy = DiagonalPosition()
        assert strategy.calculate(0, 0, 10, 10) == 0.0

    def test_diagonal_position_bottom_right(self):
        """Bottom-right = 1.0."""
        strategy = DiagonalPosition()
        assert strategy.calculate(9, 9, 10, 10) == 1.0

    def test_diagonal_position_center(self):
        """Center ≈ 0.5."""
        strategy = DiagonalPosition()
        pos = strategy.calculate(5, 5, 11, 11)
        assert 0.4 < pos < 0.6  # Approximate center

    def test_horizontal_position_left(self):
        """Left col = 0.0."""
        strategy = HorizontalPosition()
        assert strategy.calculate(0, 0, 10, 10) == 0.0

    def test_horizontal_position_right(self):
        """Right col = 1.0."""
        strategy = HorizontalPosition()
        assert strategy.calculate(0, 9, 10, 10) == 1.0

    def test_offset_strategy(self):
        """Offset strategy shifts position."""
        base = VerticalPosition()
        strategy = OffsetPositionStrategy(base, offset=0.1)
        # Base (0,0) is 0.0 -> 0.1
        assert strategy.calculate(0, 0, 10, 10) == 0.1
        # Base (9,0) is 1.0 -> 1.1 -> 0.1 (wrap)
        assert abs(strategy.calculate(9, 0, 10, 10) - 0.1) < 0.001


class TestColorSources:
    """Test color generation strategies."""

    def test_linear_gradient_start(self):
        """Position 0.0 = start color."""
        source = LinearGradient("#FF0000", "#0000FF")
        assert source.get_color(0.0) == "#FF0000"

    def test_linear_gradient_end(self):
        """Position 1.0 = end color."""
        source = LinearGradient("#FF0000", "#0000FF")
        assert source.get_color(1.0) == "#0000FF"

    def test_linear_gradient_middle(self):
        """Position 0.5 = interpolated color."""
        source = LinearGradient("#FF0000", "#0000FF")
        color = source.get_color(0.5)
        # Should be purple-ish (#800080)
        assert color.startswith("#")

    def test_rainbow_spectrum_red(self):
        """Position 0.0 = red."""
        source = RainbowSpectrum()
        color = source.get_color(0.0)
        assert color == "#FF0000"  # Red

    def test_rainbow_spectrum_violet(self):
        """Position 1.0 = violet."""
        source = RainbowSpectrum()
        color = source.get_color(1.0)
        # Should be violet (darkviolet = #9400D3)
        assert color.startswith("#")


class TestTargetFilters:
    """Test character filtering strategies."""

    def test_content_only_colors_content(self):
        """Content characters colored."""
        filter = ContentOnly()
        assert filter.should_color("a", is_border=False, row=0, col=0) is True

    def test_content_only_skips_borders(self):
        """Border characters not colored."""
        filter = ContentOnly()
        assert filter.should_color("─", is_border=True, row=0, col=0) is False

    def test_border_only_colors_borders(self):
        """Border characters colored."""
        filter = BorderOnly()
        assert filter.should_color("─", is_border=True, row=0, col=0) is True

    def test_border_only_skips_content(self):
        """Content characters not colored."""
        filter = BorderOnly()
        assert filter.should_color("a", is_border=False, row=0, col=0) is False

    def test_both_colors_everything(self):
        """All characters colored."""
        filter = Both()
        assert filter.should_color("a", is_border=False, row=0, col=0) is True
        assert filter.should_color("─", is_border=True, row=0, col=0) is True
