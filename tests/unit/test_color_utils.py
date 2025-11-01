"""Unit tests for color utilities."""

import pytest

from styledconsole.utils.color import (
    apply_line_gradient,
    color_distance,
    colorize_text,
    get_color_names,
    hex_to_rgb,
    interpolate_color,
    normalize_color_for_rich,
    parse_color,
    rgb_to_hex,
)


class TestHexToRgb:
    """Test hex to RGB conversion."""

    def test_full_hex_with_hash(self):
        """Convert full hex with # prefix."""
        assert hex_to_rgb("#FF0000") == (255, 0, 0)
        assert hex_to_rgb("#00FF00") == (0, 255, 0)
        assert hex_to_rgb("#0000FF") == (0, 0, 255)

    def test_full_hex_without_hash(self):
        """Convert full hex without # prefix."""
        assert hex_to_rgb("FF0000") == (255, 0, 0)
        assert hex_to_rgb("00FF00") == (0, 255, 0)

    def test_shorthand_hex(self):
        """Convert shorthand hex (3 characters)."""
        assert hex_to_rgb("#f00") == (255, 0, 0)
        assert hex_to_rgb("#0f0") == (0, 255, 0)
        assert hex_to_rgb("#00f") == (0, 0, 255)
        assert hex_to_rgb("abc") == (170, 187, 204)

    def test_case_insensitive(self):
        """Hex codes are case-insensitive."""
        assert hex_to_rgb("#FfAa00") == hex_to_rgb("#ffaa00")
        assert hex_to_rgb("#ABC") == hex_to_rgb("#abc")

    def test_invalid_hex_raises(self):
        """Invalid hex strings raise ValueError."""
        with pytest.raises(ValueError, match="Invalid hex color"):
            hex_to_rgb("GGGGGG")
        with pytest.raises(ValueError, match="Invalid hex color"):
            hex_to_rgb("#12")
        with pytest.raises(ValueError, match="Invalid hex color"):
            hex_to_rgb("#1234567")


class TestRgbToHex:
    """Test RGB to hex conversion."""

    def test_basic_colors(self):
        """Convert basic RGB colors to hex."""
        assert rgb_to_hex(255, 0, 0) == "#FF0000"
        assert rgb_to_hex(0, 255, 0) == "#00FF00"
        assert rgb_to_hex(0, 0, 255) == "#0000FF"
        assert rgb_to_hex(0, 0, 0) == "#000000"
        assert rgb_to_hex(255, 255, 255) == "#FFFFFF"

    def test_mixed_values(self):
        """Convert mixed RGB values."""
        assert rgb_to_hex(30, 144, 255) == "#1E90FF"  # dodgerblue
        assert rgb_to_hex(255, 127, 80) == "#FF7F50"  # coral

    def test_out_of_range_raises(self):
        """Values outside 0-255 raise ValueError."""
        with pytest.raises(ValueError, match="must be 0-255"):
            rgb_to_hex(256, 0, 0)
        with pytest.raises(ValueError, match="must be 0-255"):
            rgb_to_hex(0, -1, 0)
        with pytest.raises(ValueError, match="must be 0-255"):
            rgb_to_hex(0, 0, 300)


class TestParseColor:
    """Test color parsing from various formats."""

    def test_parse_hex_format(self):
        """Parse hex format colors."""
        assert parse_color("#FF0000") == (255, 0, 0)
        assert parse_color("#f00") == (255, 0, 0)
        assert parse_color("00FF00") == (0, 255, 0)

    def test_parse_rgb_format(self):
        """Parse rgb() format."""
        assert parse_color("rgb(255, 0, 0)") == (255, 0, 0)
        assert parse_color("rgb(0,255,0)") == (0, 255, 0)
        assert parse_color("rgb( 0 , 0 , 255 )") == (0, 0, 255)

    def test_parse_tuple_format(self):
        """Parse tuple format (r, g, b)."""
        assert parse_color("(255, 0, 0)") == (255, 0, 0)
        assert parse_color("(0,255,0)") == (0, 255, 0)
        assert parse_color("( 0 , 0 , 255 )") == (0, 0, 255)

    def test_parse_css4_named_colors(self):
        """Parse CSS4 named colors."""
        assert parse_color("red") == (255, 0, 0)
        assert parse_color("green") == (0, 128, 0)
        assert parse_color("blue") == (0, 0, 255)
        assert parse_color("dodgerblue") == (30, 144, 255)
        assert parse_color("coral") == (255, 127, 80)
        assert parse_color("lightseagreen") == (32, 178, 170)
        assert parse_color("tomato") == (255, 99, 71)
        assert parse_color("gold") == (255, 215, 0)

    def test_parse_case_insensitive(self):
        """Color names are case-insensitive."""
        assert parse_color("RED") == parse_color("red")
        assert parse_color("DodgerBlue") == parse_color("dodgerblue")
        assert parse_color("CORAL") == parse_color("coral")

    def test_parse_gray_grey_spelling(self):
        """Both gray and grey spellings work."""
        assert parse_color("gray") == parse_color("grey")
        assert parse_color("darkgray") == parse_color("darkgrey")
        assert parse_color("lightgray") == parse_color("lightgrey")
        assert parse_color("slategray") == parse_color("slategrey")

    def test_parse_invalid_format_raises(self):
        """Invalid color format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid color format"):
            parse_color("notacolor")
        with pytest.raises(ValueError, match="RGB values must be 0-255"):
            parse_color("rgb(256, 0, 0)")  # Out of range
        with pytest.raises(ValueError, match="Invalid color format"):
            parse_color("")


class TestInterpolateColor:
    """Test color interpolation."""

    def test_interpolate_hex_colors(self):
        """Interpolate between hex colors."""
        assert interpolate_color("#000000", "#FFFFFF", 0.0) == "#000000"
        assert interpolate_color("#000000", "#FFFFFF", 0.5) == "#7F7F7F"
        assert interpolate_color("#000000", "#FFFFFF", 1.0) == "#FFFFFF"

    def test_interpolate_named_colors(self):
        """Interpolate between named colors."""
        result = interpolate_color("red", "blue", 0.5)
        # Red (255,0,0) + Blue (0,0,255) at 0.5 = (127,0,127) = purple
        assert result == "#7F007F"

        result = interpolate_color("black", "white", 0.5)
        assert result == "#7F7F7F"  # gray

    def test_interpolate_mixed_formats(self):
        """Interpolate between different color formats."""
        result1 = interpolate_color("#FF0000", "blue", 0.5)
        result2 = interpolate_color("red", "#0000FF", 0.5)
        assert result1 == result2 == "#7F007F"

    def test_interpolate_with_rgb_tuples(self):
        """Interpolate with RGB tuples."""
        result = interpolate_color((255, 0, 0), (0, 0, 255), 0.5)
        assert result == "#7F007F"

        result = interpolate_color((0, 0, 0), (255, 255, 255), 0.5)
        assert result == "#7F7F7F"

    def test_interpolate_boundary_values(self):
        """Interpolation at boundaries (0.0 and 1.0)."""
        start, end = "#FF0000", "#0000FF"
        assert interpolate_color(start, end, 0.0) == "#FF0000"
        assert interpolate_color(start, end, 1.0) == "#0000FF"

    def test_interpolate_clamps_t(self):
        """Interpolation factor is clamped to [0, 1]."""
        # t < 0 should be treated as 0
        assert interpolate_color("#000000", "#FFFFFF", -0.5) == "#000000"
        # t > 1 should be treated as 1
        assert interpolate_color("#000000", "#FFFFFF", 1.5) == "#FFFFFF"

    def test_interpolate_gradient_examples(self):
        """Real-world gradient examples."""
        # Coral to dodgerblue gradient
        result = interpolate_color("coral", "dodgerblue", 0.3)
        # Coral: (255, 127, 80), Dodgerblue: (30, 144, 255)
        # At 0.3: (187, 132, 133) approximately
        rgb = parse_color(result)
        assert 180 <= rgb[0] <= 195
        assert 125 <= rgb[1] <= 140
        assert 125 <= rgb[2] <= 140


class TestColorDistance:
    """Test color distance calculation."""

    def test_distance_identical_colors(self):
        """Distance between identical colors is 0."""
        assert color_distance("red", "red") == 0.0
        assert color_distance("#FF0000", "#FF0000") == 0.0
        assert color_distance((255, 0, 0), (255, 0, 0)) == 0.0

    def test_distance_black_white(self):
        """Distance between black and white (maximum)."""
        distance = color_distance("#000000", "#FFFFFF")
        # sqrt(255^2 + 255^2 + 255^2) = sqrt(195075) ≈ 441.67
        assert 441.0 < distance < 442.0

    def test_distance_similar_colors(self):
        """Similar colors have smaller distance."""
        # red vs darkred should be closer than red vs blue
        dist_similar = color_distance("red", "darkred")
        dist_different = color_distance("red", "blue")
        assert dist_similar < dist_different

    def test_distance_with_named_colors(self):
        """Distance works with named colors."""
        # Coral and salmon are similar (both orange-ish)
        dist1 = color_distance("coral", "salmon")
        # Coral and blue are very different
        dist2 = color_distance("coral", "blue")
        assert dist1 < dist2

    def test_distance_with_mixed_formats(self):
        """Distance works with mixed formats."""
        dist1 = color_distance("#FF0000", "red")
        dist2 = color_distance((255, 0, 0), "red")
        assert dist1 == dist2 == 0.0


class TestGetColorNames:
    """Test getting list of color names."""

    def test_color_names_count(self):
        """Should return 148 CSS4 color names."""
        names = get_color_names()
        assert len(names) == 148

    def test_color_names_sorted(self):
        """Color names should be sorted alphabetically."""
        names = get_color_names()
        assert names == sorted(names)

    def test_color_names_content(self):
        """Verify some expected color names are present."""
        names = get_color_names()
        assert "red" in names
        assert "blue" in names
        assert "green" in names
        assert "dodgerblue" in names
        assert "coral" in names
        assert "lightseagreen" in names
        assert "tomato" in names
        assert "gold" in names

    def test_both_gray_spellings(self):
        """Both gray and grey spellings are in the list."""
        names = get_color_names()
        assert "gray" in names
        assert "grey" in names
        assert "darkgray" in names
        assert "darkgrey" in names


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_white_color(self):
        """Test white color in various formats."""
        assert parse_color("#FFFFFF") == (255, 255, 255)
        assert parse_color("white") == (255, 255, 255)
        assert parse_color("rgb(255, 255, 255)") == (255, 255, 255)

    def test_black_color(self):
        """Test black color in various formats."""
        assert parse_color("#000000") == (0, 0, 0)
        assert parse_color("black") == (0, 0, 0)
        assert parse_color("rgb(0, 0, 0)") == (0, 0, 0)

    def test_whitespace_handling(self):
        """Color parsing handles extra whitespace."""
        assert parse_color("  red  ") == (255, 0, 0)
        assert parse_color("  #FF0000  ") == (255, 0, 0)

    def test_rebeccapurple(self):
        """Test rebeccapurple (added in CSS4 in honor of Eric Meyer's daughter)."""
        # This color has historical significance in CSS
        assert parse_color("rebeccapurple") == (102, 51, 153)


class TestApplyLineGradient:
    """Tests for apply_line_gradient()."""

    def test_basic_gradient(self):
        """Test basic gradient application."""
        lines = ["Line 1", "Line 2", "Line 3"]
        colored = apply_line_gradient(lines, "red", "blue")

        assert len(colored) == 3
        # All lines should have ANSI codes
        assert all("\033[38;2;" in line for line in colored)
        # All lines should have reset codes
        assert all("\033[0m" in line for line in colored)
        # Original text preserved
        assert "Line 1" in colored[0]
        assert "Line 2" in colored[1]
        assert "Line 3" in colored[2]

    def test_single_line(self):
        """Test gradient with single line."""
        lines = ["Single"]
        colored = apply_line_gradient(lines, "red", "blue")
        assert len(colored) == 1
        assert "\033[38;2;" in colored[0]
        assert "Single" in colored[0]

    def test_empty_list(self):
        """Test gradient with empty list."""
        lines = []
        colored = apply_line_gradient(lines, "red", "blue")
        assert colored == []

    def test_two_lines(self):
        """Test gradient with two lines (start and end colors)."""
        lines = ["First", "Last"]
        colored = apply_line_gradient(lines, "#FF0000", "#0000FF")

        # First line should be red (255, 0, 0)
        assert "255;0;0" in colored[0]
        # Last line should be blue (0, 0, 255)
        assert "0;0;255" in colored[1]

    def test_gradient_with_hex_colors(self):
        """Test gradient with hex color format."""
        lines = ["A", "B", "C"]
        colored = apply_line_gradient(lines, "#FF0000", "#00FF00")
        assert len(colored) == 3

    def test_gradient_with_named_colors(self):
        """Test gradient with CSS4 color names."""
        lines = ["A", "B"]
        colored = apply_line_gradient(lines, "cyan", "magenta")
        assert len(colored) == 2

    def test_preserves_original_lines(self):
        """Test that original lines list is not modified."""
        lines = ["Test 1", "Test 2"]
        original = lines.copy()
        apply_line_gradient(lines, "red", "blue")
        assert lines == original


class TestColorizeText:
    """Tests for colorize_text()."""

    def test_basic_colorization(self):
        """Test basic text colorization."""
        colored = colorize_text("Hello", "red")
        assert "\033[38;2;255;0;0m" in colored  # Red
        assert "Hello" in colored
        assert "\033[0m" in colored  # Reset

    def test_with_hex_color(self):
        """Test colorization with hex color."""
        colored = colorize_text("World", "#00FF00")
        assert "\033[38;2;0;255;0m" in colored  # Green
        assert "World" in colored

    def test_with_css4_color(self):
        """Test colorization with CSS4 color name."""
        colored = colorize_text("Test", "lime")
        assert "\033[38;2;0;255;0m" in colored  # Lime
        assert "Test" in colored

    def test_empty_string(self):
        """Test colorization of empty string."""
        colored = colorize_text("", "red")
        assert "\033[38;2;255;0;0m" in colored
        assert "\033[0m" in colored

    def test_multiline_text(self):
        """Test colorization preserves newlines."""
        colored = colorize_text("Line 1\nLine 2", "blue")
        assert "Line 1\nLine 2" in colored
        assert "\033[38;2;0;0;255m" in colored  # Blue

    def test_text_with_special_chars(self):
        """Test colorization with special characters."""
        colored = colorize_text("!@#$%^&*()", "red")
        assert "!@#$%^&*()" in colored
        assert "\033[38;2;255;0;0m" in colored


class TestNormalizeColorForRich:
    """Test color normalization for Rich compatibility."""

    def test_none_returns_none(self):
        """None input returns None."""
        assert normalize_color_for_rich(None) is None

    def test_hex_passthrough(self):
        """Hex colors are returned unchanged."""
        assert normalize_color_for_rich("#FF0000") == "#FF0000"
        assert normalize_color_for_rich("#00FF00") == "#00FF00"
        assert normalize_color_for_rich("#0000FF") == "#0000FF"

    def test_hex_lowercase(self):
        """Lowercase hex colors work."""
        assert normalize_color_for_rich("#ff0000") == "#ff0000"
        assert normalize_color_for_rich("#abc123") == "#abc123"

    def test_css4_color_names(self):
        """CSS4 color names are normalized to hex."""
        assert normalize_color_for_rich("red") == "#FF0000"
        assert normalize_color_for_rich("lime") == "#00FF00"
        assert normalize_color_for_rich("blue") == "#0000FF"
        assert normalize_color_for_rich("white") == "#FFFFFF"
        assert normalize_color_for_rich("black") == "#000000"

    def test_css4_case_insensitive(self):
        """CSS4 names are case-insensitive."""
        assert normalize_color_for_rich("RED") == "#FF0000"
        assert normalize_color_for_rich("Red") == "#FF0000"
        assert normalize_color_for_rich("rEd") == "#FF0000"

    def test_rich_color_names(self):
        """Rich color names map to CSS4 equivalents."""
        # Rich's bright_green should map to lime
        assert normalize_color_for_rich("bright_green") == "#00FF00"
        # Rich's bright_red maps to its own value
        result = normalize_color_for_rich("bright_red")
        assert result.startswith("#")  # Should return a hex color

    def test_invalid_color_returns_original(self):
        """Invalid color names return original string."""
        # Let Rich handle unknown colors
        assert normalize_color_for_rich("invalid_color") == "invalid_color"
        assert normalize_color_for_rich("not_a_color") == "not_a_color"
        # Empty string returns None (treated as no color)
        assert normalize_color_for_rich("") is None

    def test_whitespace_stripped(self):
        """Whitespace is stripped from input."""
        assert normalize_color_for_rich("  red  ") == "#FF0000"
        assert normalize_color_for_rich("\t#FF0000\n") == "#FF0000"

    def test_gray_grey_variants(self):
        """Both gray and grey spellings work."""
        assert normalize_color_for_rich("gray") == "#808080"
        assert normalize_color_for_rich("grey") == "#808080"
        assert normalize_color_for_rich("darkgray") == "#A9A9A9"
        assert normalize_color_for_rich("darkgrey") == "#A9A9A9"

    def test_cache_behavior(self):
        """Function uses LRU cache correctly."""
        # Clear cache first
        normalize_color_for_rich.cache_clear()

        # First call - cache miss
        result1 = normalize_color_for_rich("red")
        cache_info1 = normalize_color_for_rich.cache_info()
        assert cache_info1.hits == 0
        assert cache_info1.misses == 1

        # Second call - cache hit
        result2 = normalize_color_for_rich("red")
        cache_info2 = normalize_color_for_rich.cache_info()
        assert cache_info2.hits == 1
        assert cache_info2.misses == 1

        # Results are identical
        assert result1 == result2 == "#FF0000"

    def test_cache_size_limit(self):
        """Cache respects maxsize=256."""
        normalize_color_for_rich.cache_clear()

        # Cache has maxsize=256
        cache_info = normalize_color_for_rich.cache_info()
        assert cache_info.maxsize == 256

    def test_complex_css4_colors(self):
        """Test various CSS4 color names."""
        assert normalize_color_for_rich("coral") == "#FF7F50"
        assert normalize_color_for_rich("skyblue") == "#87CEEB"
        assert normalize_color_for_rich("gold") == "#FFD700"
        assert normalize_color_for_rich("purple") == "#800080"
        assert normalize_color_for_rich("orange") == "#FFA500"

    def test_edge_cases(self):
        """Test edge case inputs."""
        # Empty string after strip returns None
        assert normalize_color_for_rich("   ") is None

        # Hex-like but invalid (would fail parse_color)
        result = normalize_color_for_rich("#GGGGGG")
        assert result == "#GGGGGG"  # Returns original
