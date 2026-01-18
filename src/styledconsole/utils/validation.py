"""Centralized validation for StyledConsole.

This module provides shared validation functions used across the codebase
to ensure consistent error handling and reduce code duplication.
"""

from styledconsole.types import AlignType

VALID_ALIGNMENTS = {"left", "center", "right"}


def validate_align(align: AlignType) -> None:
    """Validate alignment parameter.

    Args:
        align: Alignment value to validate

    Raises:
        ValueError: If alignment is not valid

    Example:
        >>> validate_align("left")  # OK
        >>> validate_align("middle")  # Raises ValueError
    """
    if align not in VALID_ALIGNMENTS:
        from styledconsole.utils.suggestions import suggest_similar

        # Common aliases that might be used
        common_aliases = {"middle": "center", "centre": "center", "justify": None}

        # Check for common aliases first
        if align in common_aliases:
            correct = common_aliases[align]
            if correct:
                raise ValueError(
                    f"align must be one of {VALID_ALIGNMENTS}, got: {align!r}. "
                    f"Did you mean '{correct}'?"
                )
            else:
                raise ValueError(
                    f"align must be one of {VALID_ALIGNMENTS}, got: {align!r}. "
                    "Note: 'justify' is not supported."
                )

        # Try fuzzy matching
        suggestion = suggest_similar(align, list(VALID_ALIGNMENTS), max_distance=2)
        if suggestion:
            raise ValueError(
                f"align must be one of {VALID_ALIGNMENTS}, got: {align!r}. {suggestion}"
            )

        raise ValueError(f"align must be one of {VALID_ALIGNMENTS}, got: {align!r}")


def validate_color_pair(
    start: str | None,
    end: str | None,
    *,
    param_name: str = "color",
) -> None:
    """Validate color pair (both or neither required).

    Args:
        start: Starting color
        end: Ending color
        param_name: Parameter name for error messages (default: "color")

    Raises:
        ValueError: If only one color is provided

    Example:
        >>> validate_color_pair("red", "blue")  # OK
        >>> validate_color_pair(None, None)  # OK
        >>> validate_color_pair("red", None)  # Raises ValueError
    """
    if (start is None) != (end is None):
        raise ValueError(
            f"start_{param_name} and end_{param_name} must both be provided or both be None. "
            f"Got start_{param_name}={start!r}, end_{param_name}={end!r}"
        )


def _validate_nonnegative(value: int | None, name: str) -> None:
    """Validate that a value is non-negative."""
    if value is not None and value < 0:
        raise ValueError(f"{name} must be >= 0, got: {value}")


def _validate_positive(value: int | None, name: str) -> None:
    """Validate that a value is positive."""
    if value is not None and value < 1:
        raise ValueError(f"{name} must be >= 1, got: {value}")


def _validate_width_constraints(
    width: int | None,
    min_width: int | None,
    max_width: int | None,
) -> None:
    """Validate width relationships (min <= width, min <= max)."""
    if min_width is not None and max_width is not None and min_width > max_width:
        raise ValueError(f"min_width ({min_width}) must be <= max_width ({max_width})")

    if width is not None and min_width is not None and width < min_width:
        raise ValueError(f"width ({width}) must be >= min_width ({min_width})")


def validate_dimensions(
    width: int | None = None,
    padding: int | None = None,
    min_width: int | None = None,
    max_width: int | None = None,
) -> None:
    """Validate dimensional parameters.

    Args:
        width: Frame width
        padding: Padding amount
        min_width: Minimum width
        max_width: Maximum width

    Raises:
        ValueError: If any dimension is invalid

    Example:
        >>> validate_dimensions(width=80, padding=2)  # OK
        >>> validate_dimensions(padding=-1)  # Raises ValueError
    """
    _validate_nonnegative(padding, "padding")
    _validate_positive(width, "width")
    _validate_positive(min_width, "min_width")
    _validate_positive(max_width, "max_width")
    _validate_width_constraints(width, min_width, max_width)


__all__ = [
    "VALID_ALIGNMENTS",
    "validate_align",
    "validate_color_pair",
    "validate_dimensions",
]
