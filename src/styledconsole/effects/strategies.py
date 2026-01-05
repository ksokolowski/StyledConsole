"""Gradient strategy implementations for effects module.

Separates position calculation, color generation, and target filtering
into pluggable strategies following the Strategy pattern.
"""

from typing import Protocol

from styledconsole.utils.color import get_rainbow_color, interpolate_color

# ============================================================================
# Position Strategies (How to calculate gradient position for each character)
# ============================================================================


class PositionStrategy(Protocol):
    """Calculate gradient position (0.0-1.0) for a character."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        """Return position from 0.0 (start) to 1.0 (end)."""
        ...


class VerticalPosition:
    """Vertical gradient: Top (0.0) → Bottom (1.0)."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        return row / max(total_rows - 1, 1)


class DiagonalPosition:
    """Diagonal gradient: Top-left (0.0) → Bottom-right (1.0)."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        row_progress = row / max(total_rows - 1, 1)
        col_progress = col / max(total_cols - 1, 1)
        return (row_progress + col_progress) / 2.0


class HorizontalPosition:
    """Horizontal gradient: Left (0.0) → Right (1.0)."""

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        return col / max(total_cols - 1, 1)


class OffsetPositionStrategy:
    """Wraps a position strategy and adds an offset (for animation)."""

    def __init__(self, base_strategy: PositionStrategy, offset: float = 0.0):
        self.base_strategy = base_strategy
        self.offset = offset

    def calculate(self, row: int, col: int, total_rows: int, total_cols: int) -> float:
        base_pos = self.base_strategy.calculate(row, col, total_rows, total_cols)
        # Wrap around 0.0-1.0
        return (base_pos + self.offset) % 1.0


# ============================================================================
# Color Source Strategies (What color to use at each position)
# ============================================================================


class ColorSource(Protocol):
    """Provide color for gradient position."""

    def get_color(self, position: float) -> str:
        """Return hex color for position (0.0-1.0)."""
        ...


class LinearGradient:
    """Two-color linear gradient interpolation."""

    def __init__(self, start_color: str, end_color: str):
        self.start_color = start_color
        self.end_color = end_color

    def get_color(self, position: float) -> str:
        return interpolate_color(self.start_color, self.end_color, position)


class RainbowSpectrum:
    """7-color ROYGBIV rainbow spectrum."""

    def get_color(self, position: float) -> str:
        return get_rainbow_color(position)


class MultiStopGradient:
    """Multi-color gradient with 3+ color stops.

    Interpolates between multiple colors based on position.
    Colors are evenly distributed unless custom positions are provided.

    Example:
        >>> gradient = MultiStopGradient(["red", "yellow", "green"])
        >>> gradient.get_color(0.0)   # red
        >>> gradient.get_color(0.5)   # yellow
        >>> gradient.get_color(1.0)   # green
        >>> gradient.get_color(0.25)  # interpolated red-yellow
    """

    def __init__(
        self,
        colors: tuple[str, ...] | list[str],
        positions: tuple[float, ...] | list[float] | None = None,
    ):
        """Initialize multi-stop gradient.

        Args:
            colors: Sequence of colors (minimum 2).
            positions: Optional custom positions (0.0-1.0) for each color.
                      If None, colors are evenly distributed.

        Raises:
            ValueError: If fewer than 2 colors provided.
            ValueError: If positions count doesn't match colors count.
        """
        self.colors = tuple(colors)
        if len(self.colors) < 2:
            raise ValueError("MultiStopGradient requires at least 2 colors")

        if positions is None:
            # Evenly distribute colors
            n = len(self.colors)
            self.positions = tuple(i / (n - 1) for i in range(n))
        else:
            if len(positions) != len(self.colors):
                raise ValueError("positions count must match colors count")
            self.positions = tuple(positions)

    def get_color(self, position: float) -> str:
        """Get interpolated color at position.

        Args:
            position: Position from 0.0 to 1.0.

        Returns:
            Interpolated hex color.
        """
        # Clamp position to valid range
        position = max(0.0, min(1.0, position))

        # Find the two colors to interpolate between
        for i in range(len(self.positions) - 1):
            if position <= self.positions[i + 1]:
                # Found the segment
                start_pos = self.positions[i]
                end_pos = self.positions[i + 1]
                start_color = self.colors[i]
                end_color = self.colors[i + 1]

                # Calculate local position within segment
                segment_length = end_pos - start_pos
                local_pos = 0.0 if segment_length == 0 else (position - start_pos) / segment_length

                return interpolate_color(start_color, end_color, local_pos)

        # Position is at or beyond the last stop
        return interpolate_color(self.colors[-2], self.colors[-1], 1.0)


class EnhancedRainbow:
    """Rainbow spectrum with saturation and brightness controls.

    Extends RainbowSpectrum with adjustable saturation, brightness,
    and optional direction reversal.

    Example:
        >>> pastel = EnhancedRainbow(saturation=0.5, brightness=1.2)
        >>> neon = EnhancedRainbow(saturation=1.2, brightness=1.1)
        >>> reversed_rainbow = EnhancedRainbow(reverse=True)
    """

    def __init__(
        self,
        saturation: float = 1.0,
        brightness: float = 1.0,
        reverse: bool = False,
    ):
        """Initialize enhanced rainbow.

        Args:
            saturation: Saturation multiplier (0.0-2.0, 1.0 = normal).
            brightness: Brightness multiplier (0.0-2.0, 1.0 = normal).
            reverse: If True, reverses rainbow direction (violet to red).
        """
        self.saturation = saturation
        self.brightness = brightness
        self.reverse = reverse

    def get_color(self, position: float) -> str:
        """Get rainbow color at position with adjustments.

        Args:
            position: Position from 0.0 to 1.0.

        Returns:
            Adjusted hex color.
        """
        if self.reverse:
            position = 1.0 - position

        # Get base rainbow color
        base_color = get_rainbow_color(position)

        # If no adjustments needed, return base color
        if self.saturation == 1.0 and self.brightness == 1.0:
            return base_color

        # Apply saturation and brightness adjustments
        return self._adjust_color(base_color)

    def _adjust_color(self, hex_color: str) -> str:
        """Apply saturation and brightness adjustments to a color.

        Args:
            hex_color: Input color in hex format.

        Returns:
            Adjusted hex color.
        """
        from styledconsole.utils.color import hex_to_rgb

        r, g, b = hex_to_rgb(hex_color)

        # Convert to HSL-like adjustment (simplified)
        # Calculate luminance
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        lum = (max_c + min_c) / 2

        if max_c == min_c:
            # Achromatic
            h = s = 0.0
        else:
            d = max_c - min_c
            s = d / (2 - max_c - min_c) if lum > 0.5 else d / (max_c + min_c)

            if max_c == r:
                h = (g - b) / d + (6 if g < b else 0)
            elif max_c == g:
                h = (b - r) / d + 2
            else:
                h = (r - g) / d + 4
            h /= 6

        # Apply adjustments
        s = min(1.0, s * self.saturation)
        lum = min(1.0, lum * self.brightness)

        # Convert back to RGB
        if s == 0:
            r = g = b = int(lum * 255)
        else:

            def hue_to_rgb(p: float, q: float, t: float) -> float:
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p

            q = lum * (1 + s) if lum < 0.5 else lum + s - lum * s
            p = 2 * lum - q
            r = int(hue_to_rgb(p, q, h + 1 / 3) * 255)
            g = int(hue_to_rgb(p, q, h) * 255)
            b = int(hue_to_rgb(p, q, h - 1 / 3) * 255)

        # Clamp values
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        return f"#{r:02x}{g:02x}{b:02x}"


class ReversedColorSource:
    """Wrapper that reverses any color source.

    Example:
        >>> gradient = LinearGradient("red", "blue")
        >>> reversed_gradient = ReversedColorSource(gradient)
        >>> reversed_gradient.get_color(0.0)  # Returns blue
        >>> reversed_gradient.get_color(1.0)  # Returns red
    """

    def __init__(self, source: ColorSource):
        """Initialize with a color source to reverse.

        Args:
            source: The color source to reverse.
        """
        self.source = source

    def get_color(self, position: float) -> str:
        """Get color at reversed position.

        Args:
            position: Position from 0.0 to 1.0.

        Returns:
            Color from the reversed position.
        """
        return self.source.get_color(1.0 - position)


# ============================================================================
# Target Filter Strategies (Which characters to color)
# ============================================================================


class TargetFilter(Protocol):
    """Determine if character should be colored."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        """Return True if character should be colored."""
        ...


class ContentOnly:
    """Color content characters only (skip borders)."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        return not is_border


class BorderOnly:
    """Color border characters only (skip content)."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        return is_border


class Both:
    """Color all characters (content and borders)."""

    def should_color(self, char: str, is_border: bool, row: int, col: int) -> bool:
        return True
