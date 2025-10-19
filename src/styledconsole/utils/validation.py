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
    if padding is not None and padding < 0:
        raise ValueError(f"padding must be >= 0, got: {padding}")

    if width is not None and width < 1:
        raise ValueError(f"width must be >= 1, got: {width}")

    if min_width is not None and min_width < 1:
        raise ValueError(f"min_width must be >= 1, got: {min_width}")

    if max_width is not None and max_width < 1:
        raise ValueError(f"max_width must be >= 1, got: {max_width}")

    if min_width is not None and max_width is not None and min_width > max_width:
        raise ValueError(f"min_width ({min_width}) must be <= max_width ({max_width})")

    if width is not None and min_width is not None and width < min_width:
        raise ValueError(f"width ({width}) must be >= min_width ({min_width})")


__all__ = [
    "VALID_ALIGNMENTS",
    "validate_align",
    "validate_color_pair",
    "validate_dimensions",
]
