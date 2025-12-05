"""Tests for validation utilities."""

import pytest

from styledconsole.utils.validation import (
    VALID_ALIGNMENTS,
    validate_align,
    validate_color_pair,
    validate_dimensions,
)


class TestValidateAlign:
    """Tests for validate_align()."""

    def test_valid_alignments(self):
        """Test all valid alignment values."""
        validate_align("left")
        validate_align("center")
        validate_align("right")

    def test_invalid_alignment(self):
        """Test invalid alignment raises ValueError."""
        with pytest.raises(ValueError, match="align must be one of"):
            validate_align("middle")

        with pytest.raises(ValueError, match="align must be one of"):
            validate_align("top")

        with pytest.raises(ValueError, match="align must be one of"):
            validate_align("justify")

    def test_error_message_format(self):
        """Test error message includes expected values."""
        with pytest.raises(ValueError) as exc_info:
            validate_align("invalid")

        error_msg = str(exc_info.value)
        assert "left" in error_msg
        assert "center" in error_msg
        assert "right" in error_msg
        assert "'invalid'" in error_msg


class TestValidateColorPair:
    """Tests for validate_color_pair()."""

    def test_both_provided(self):
        """Test with both colors provided."""
        validate_color_pair("red", "blue")
        validate_color_pair("#FF0000", "#0000FF")
        validate_color_pair("rgb(255,0,0)", "rgb(0,0,255)")

    def test_both_none(self):
        """Test with both colors None."""
        validate_color_pair(None, None)

    def test_only_start_provided(self):
        """Test with only start color raises ValueError."""
        with pytest.raises(ValueError, match="must both be provided or both be None"):
            validate_color_pair("red", None)

    def test_only_end_provided(self):
        """Test with only end color raises ValueError."""
        with pytest.raises(ValueError, match="must both be provided or both be None"):
            validate_color_pair(None, "blue")

    def test_custom_param_name(self):
        """Test custom parameter name in error message."""
        with pytest.raises(ValueError) as exc_info:
            validate_color_pair("red", None, param_name="gradient")

        error_msg = str(exc_info.value)
        assert "start_gradient" in error_msg
        assert "end_gradient" in error_msg

    def test_error_message_includes_values(self):
        """Test error message includes actual values."""
        with pytest.raises(ValueError) as exc_info:
            validate_color_pair("red", None)

        error_msg = str(exc_info.value)
        assert "'red'" in error_msg
        assert "None" in error_msg


class TestValidateDimensions:
    """Tests for validate_dimensions()."""

    def test_valid_dimensions(self):
        """Test with all valid dimensions."""
        validate_dimensions(width=80, padding=2, min_width=20, max_width=100)

    def test_all_none(self):
        """Test with all parameters None."""
        validate_dimensions()

    def test_negative_padding(self):
        """Test negative padding raises ValueError."""
        with pytest.raises(ValueError, match="padding must be >= 0"):
            validate_dimensions(padding=-1)

    def test_zero_padding(self):
        """Test zero padding is allowed."""
        validate_dimensions(padding=0)

    def test_invalid_width(self):
        """Test width < 1 raises ValueError."""
        with pytest.raises(ValueError, match="width must be >= 1"):
            validate_dimensions(width=0)

        with pytest.raises(ValueError, match="width must be >= 1"):
            validate_dimensions(width=-5)

    def test_invalid_min_width(self):
        """Test min_width < 1 raises ValueError."""
        with pytest.raises(ValueError, match="min_width must be >= 1"):
            validate_dimensions(min_width=0)

    def test_invalid_max_width(self):
        """Test max_width < 1 raises ValueError."""
        with pytest.raises(ValueError, match="max_width must be >= 1"):
            validate_dimensions(max_width=0)

    def test_min_greater_than_max(self):
        """Test min_width > max_width raises ValueError."""
        with pytest.raises(ValueError, match=r"min_width.*must be <= max_width"):
            validate_dimensions(min_width=100, max_width=50)

    def test_min_equal_max(self):
        """Test min_width == max_width is allowed."""
        validate_dimensions(min_width=50, max_width=50)

    def test_width_less_than_min(self):
        """Test width < min_width raises ValueError."""
        with pytest.raises(ValueError, match=r"width.*must be >= min_width"):
            validate_dimensions(width=30, min_width=50)

    def test_width_equal_min(self):
        """Test width == min_width is allowed."""
        validate_dimensions(width=50, min_width=50)

    def test_complex_valid_scenario(self):
        """Test complex but valid dimension combination."""
        validate_dimensions(
            width=80,
            padding=3,
            min_width=50,
            max_width=120,
        )

    def test_error_message_includes_values(self):
        """Test error messages include actual values."""
        with pytest.raises(ValueError) as exc_info:
            validate_dimensions(padding=-5)

        assert "-5" in str(exc_info.value)


class TestValidationConstants:
    """Tests for validation constants."""

    def test_valid_alignments_constant(self):
        """Test VALID_ALIGNMENTS contains expected values."""
        assert {"left", "center", "right"} == VALID_ALIGNMENTS
        assert len(VALID_ALIGNMENTS) == 3
