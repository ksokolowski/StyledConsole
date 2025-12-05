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
