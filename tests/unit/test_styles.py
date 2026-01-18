"""Unit tests for border styles and rendering."""

import pytest

from styledconsole.core.styles import (
    ASCII,
    BORDERS,
    DOTS,
    DOUBLE,
    HEAVY,
    MINIMAL,
    ROUNDED,
    SOLID,
    THICK,
    BorderStyle,
    get_border_style,
    list_border_styles,
)


class TestBorderStyle:
    """Test BorderStyle dataclass."""

    def test_create_border_style(self):
        """Test creating a BorderStyle."""
        style = BorderStyle(
            name="test",
            top_left="A",
            top_right="B",
            bottom_left="C",
            bottom_right="D",
            horizontal="-",
            vertical="|",
            left_joint="E",
            right_joint="F",
            top_joint="G",
            bottom_joint="H",
            cross="X",
        )

        assert style.name == "test"
        assert style.top_left == "A"
        assert style.top_right == "B"
        assert style.bottom_left == "C"
        assert style.bottom_right == "D"
        assert style.horizontal == "-"
        assert style.vertical == "|"
        assert style.left_joint == "E"
        assert style.right_joint == "F"
        assert style.top_joint == "G"
        assert style.bottom_joint == "H"
        assert style.cross == "X"

    def test_border_style_is_frozen(self):
        """Test that BorderStyle is immutable (frozen)."""
        style = SOLID
        # Since we use frozen dataclass (or similar checks), it raises FrozenInstanceError
        from dataclasses import FrozenInstanceError

        with pytest.raises(FrozenInstanceError):
            style.name = "modified"  # type: ignore


class TestRenderHorizontal:
    """Test horizontal line rendering."""

    def test_render_horizontal_solid(self):
        """Test rendering horizontal line with solid style."""
        assert SOLID.render_horizontal(5) == "─────"
        assert SOLID.render_horizontal(10) == "──────────"

    def test_render_horizontal_double(self):
        """Test rendering horizontal line with double style."""
        assert DOUBLE.render_horizontal(5) == "═════"

    def test_render_horizontal_ascii(self):
        """Test rendering horizontal line with ASCII style."""
        assert ASCII.render_horizontal(5) == "-----"

    def test_render_horizontal_custom_char(self):
        """Test rendering horizontal line with custom character."""
        assert SOLID.render_horizontal(5, char="*") == "*****"
        assert DOUBLE.render_horizontal(3, char="#") == "###"

    def test_render_horizontal_zero_width(self):
        """Test rendering horizontal line with zero width."""
        assert SOLID.render_horizontal(0) == ""

    def test_render_horizontal_one_width(self):
        """Test rendering horizontal line with width of 1."""
        assert SOLID.render_horizontal(1) == "─"


class TestRenderVertical:
    """Test vertical line rendering."""

    def test_render_vertical_solid(self):
        """Test rendering vertical line with solid style."""
        result = SOLID.render_vertical(3)
        assert result == ["│", "│", "│"]
        assert len(result) == 3

    def test_render_vertical_double(self):
        """Test rendering vertical line with double style."""
        result = DOUBLE.render_vertical(2)
        assert result == ["║", "║"]

    def test_render_vertical_ascii(self):
        """Test rendering vertical line with ASCII style."""
        result = ASCII.render_vertical(4)
        assert result == ["|", "|", "|", "|"]

    def test_render_vertical_custom_char(self):
        """Test rendering vertical line with custom character."""
        result = SOLID.render_vertical(3, char="!")
        assert result == ["!", "!", "!"]

    def test_render_vertical_zero_height(self):
        """Test rendering vertical line with zero height."""
        assert SOLID.render_vertical(0) == []

    def test_render_vertical_one_height(self):
        """Test rendering vertical line with height of 1."""
        result = SOLID.render_vertical(1)
        assert result == ["│"]


class TestRenderTopBorder:
    """Test top border rendering."""

    def test_render_top_border_no_title(self):
        """Test rendering top border without title."""
        assert SOLID.render_top_border(10) == "┌────────┐"
        assert SOLID.render_top_border(5) == "┌───┐"

    def test_render_top_border_double(self):
        """Test rendering top border with double style."""
        assert DOUBLE.render_top_border(10) == "╔════════╗"

    def test_render_top_border_ascii(self):
        """Test rendering top border with ASCII style."""
        assert ASCII.render_top_border(10) == "+--------+"

    def test_render_top_border_with_title(self):
        """Test rendering top border with centered title."""
        result = SOLID.render_top_border(20, "Test")
        assert result == "┌────── Test ──────┐"
        assert len(result) == 20

    def test_render_top_border_title_even_width(self):
        """Test title centering with even remaining width."""
        result = SOLID.render_top_border(16, "Hi")
        assert result == "┌───── Hi ─────┐"
        assert len(result) == 16

    def test_render_top_border_title_odd_width(self):
        """Test title centering with odd remaining width."""
        result = SOLID.render_top_border(15, "Hi")
        assert result == "┌──── Hi ─────┐"
        assert len(result) == 15

    def test_render_top_border_long_title(self):
        """Test rendering with title longer than available width."""
        result = SOLID.render_top_border(10, "LongTitle")
        # Should truncate title
        assert len(result) == 10
        assert result.startswith("┌")
        assert result.endswith("┐")

    def test_render_top_border_title_exact_fit(self):
        """Test title that exactly fits the available space."""
        result = SOLID.render_top_border(12, "12345678")
        assert len(result) == 12

    def test_render_top_border_minimum_width(self):
        """Test top border with minimum width."""
        result = SOLID.render_top_border(2)
        assert result == "┌┐"

    def test_render_top_border_empty_string_title(self):
        """Test that empty string title is treated same as None."""
        width = 30
        result_none = SOLID.render_top_border(width, None)
        result_empty = SOLID.render_top_border(width, "")
        result_bottom = SOLID.render_bottom_border(width)

        # Empty string should produce solid border, same as None
        assert result_empty == result_none
        # Only corners differ between top and bottom
        assert result_none.replace("┌", "└").replace("┐", "┘") == result_bottom


class TestRenderTopBorderEmoji:
    """Test render_top_border with emoji titles."""

    def test_render_top_border_emoji_title(self):
        """Test top border with emoji in title."""
        from styledconsole import visual_width

        result = SOLID.render_top_border(40, "🚀 Launch")
        assert visual_width(result) == 40
        assert result.startswith("┌")
        assert result.endswith("┐")
        assert "🚀" in result
        assert "Launch" in result

    def test_render_top_border_emoji_only_title(self):
        """Test top border with emoji-only title."""
        from styledconsole import visual_width

        result = SOLID.render_top_border(30, "🎉")
        assert visual_width(result) == 30
        assert "🎉" in result

    def test_render_top_border_multiple_emojis(self):
        """Test top border with multiple emojis in title."""
        from styledconsole import visual_width

        result = SOLID.render_top_border(40, "🚀 Test 🎉")
        assert visual_width(result) == 40
        assert "🚀" in result
        assert "🎉" in result

    def test_render_top_border_emoji_truncation(self):
        """Test emoji title truncation when too long."""
        from styledconsole import visual_width

        long_title = "🚀 " * 10 + "Very long title"
        result = SOLID.render_top_border(20, long_title)
        assert visual_width(result) == 20
        assert result.startswith("┌")
        assert result.endswith("┐")

    def test_render_top_border_visual_alignment(self):
        """Test that emoji titles align perfectly with content lines."""
        from styledconsole import visual_width

        width = 45
        title_line = SOLID.render_top_border(width, "🚀 Emoji Support")
        content_line = SOLID.render_line(width, "Content")

        # Both should have same visual width for perfect alignment
        assert visual_width(title_line) == width
        assert visual_width(content_line) == width


class TestRenderLine:
    """Test content line rendering."""

    def test_render_line_left_align(self):
        """Test rendering content line with left alignment."""
        result = SOLID.render_line(20, "Hello")
        assert result == "│Hello             │"
        assert len(result) == 20

    def test_render_line_center_align(self):
        """Test rendering content line with center alignment."""
        result = SOLID.render_line(20, "Hello")
        assert len(result) == 20

        result = SOLID.render_line(20, "Hello", align="center")
        assert len(result) == 20
        # "Hello" is 5 chars, inner width is 18, so 13 padding total
        # Center: 6 left, 7 right (or 7 left, 6 right)
        assert "Hello" in result
        assert result.startswith("│")
        assert result.endswith("│")

    def test_render_line_right_align(self):
        """Test rendering content line with right alignment."""
        result = SOLID.render_line(20, "Hello", align="right")
        assert result == "│             Hello│"
        assert len(result) == 20

    def test_render_line_empty_content(self):
        """Test rendering empty content line."""
        result = SOLID.render_line(20)
        assert result == "│                  │"
        assert len(result) == 20

    def test_render_line_empty_string(self):
        """Test rendering with empty string content."""
        result = SOLID.render_line(20, "")
        assert result == "│                  │"
        assert len(result) == 20

    def test_render_line_long_content_truncated(self):
        """Test that long content is truncated properly."""
        long_text = "This is a very long text that should be truncated"
        result = SOLID.render_line(20, long_text)
        assert len(result) == 20
        assert result.startswith("│")
        assert result.endswith("│")
        # Content should be truncated (using truncate_to_width)

    def test_render_line_exact_fit(self):
        """Test content that exactly fits the inner width."""
        # Width 20, inner width 18
        content = "A" * 18
        result = SOLID.render_line(20, content)
        assert result == f"│{content}│"
        assert len(result) == 20

    def test_render_line_different_styles(self):
        """Test render_line with different border styles."""
        content = "Test"

        solid = SOLID.render_line(15, content)
        double = DOUBLE.render_line(15, content)
        ascii_line = ASCII.render_line(15, content)

        assert len(solid) == len(double) == len(ascii_line) == 15
        assert solid.startswith("│")
        assert double.startswith("║")
        assert ascii_line.startswith("|")

    def test_render_line_minimum_width(self):
        """Test render_line with minimum width."""
        result = SOLID.render_line(2, "X")
        assert len(result) == 2
        assert result == "││"  # No room for content

    def test_render_line_width_one(self):
        """Test render_line with width of 1."""
        result = SOLID.render_line(1, "X")
        assert result == "│"

    def test_render_line_align_variations(self):
        """Test all alignment variations produce correct width."""
        for align in ["left", "center", "right"]:
            result = SOLID.render_line(30, "Content", align=align)
            assert len(result) == 30
            assert result.startswith("│")
            assert result.endswith("│")
            assert "Content" in result


class TestRenderLineEmoji:
    """Test render_line with emoji and wide characters."""

    def test_render_line_emoji_left(self):
        """Test emoji content with left alignment."""
        from styledconsole import visual_width

        result = SOLID.render_line(30, "🚀 Rocket")
        # String length will be less than 30 due to emojis (multi-column chars)
        # But visual width should be exactly 30
        assert visual_width(result) == 30
        assert result.startswith("│")
        assert result.endswith("│")
        assert "🚀" in result
        assert "Rocket" in result

    def test_render_line_emoji_center(self):
        """Test emoji content with center alignment."""
        from styledconsole import visual_width

        result = SOLID.render_line(30, "🎉 Party", align="center")
        assert visual_width(result) == 30
        assert result.startswith("│")
        assert result.endswith("│")
        assert "🎉" in result
        assert "Party" in result

    def test_render_line_emoji_right(self):
        """Test emoji content with right alignment."""
        from styledconsole import visual_width

        result = SOLID.render_line(30, "Done ✅", align="right")
        assert visual_width(result) == 30
        assert result.startswith("│")
        assert result.endswith("│")
        assert "✅" in result
        assert "Done" in result

    def test_render_line_multiple_emojis(self):
        """Test content with multiple emojis."""
        from styledconsole import visual_width

        result = SOLID.render_line(40, "🚀 Launch 🎉 Success ✅")
        assert visual_width(result) == 40
        assert result.startswith("│")
        assert result.endswith("│")
        assert "🚀" in result
        assert "🎉" in result
        assert "✅" in result

    def test_render_line_emoji_truncation(self):
        """Test that long emoji content is truncated properly."""
        from styledconsole import visual_width

        long_text = "🚀 " * 20 + "Very long text"
        result = SOLID.render_line(20, long_text)
        # Visual width should be 20 (borders + truncated content)
        assert visual_width(result) == 20
        assert result.startswith("│")
        assert result.endswith("│")

    def test_render_line_visual_width_alignment(self):
        """Test that visual width calculations produce perfect alignment."""
        from styledconsole import visual_width

        width = 30

        # These should all have exactly 30 visual width (perfect alignment)
        line1 = SOLID.render_line(width, "No emoji")
        line2 = SOLID.render_line(width, "🚀 With emoji")
        line3 = SOLID.render_line(width, "Multiple 🎉 emojis ✅")

        # Visual widths should all be 30 (perfectly aligned visually)
        assert visual_width(line1) == width
        assert visual_width(line2) == width
        assert visual_width(line3) == width

        # String lengths may differ due to multi-column chars
        assert len(line1) == 30  # No emojis
        assert len(line2) < 30  # Has emoji (visual_width=2, len=1)
        assert len(line3) < 30  # Has multiple emojis

        # All should align perfectly
        assert line1.startswith("│") and line1.endswith("│")
        assert line2.startswith("│") and line2.endswith("│")
        assert line3.startswith("│") and line3.endswith("│")


class TestRenderBottomBorder:
    """Test bottom border rendering."""

    def test_render_bottom_border_solid(self):
        """Test rendering bottom border with solid style."""
        assert SOLID.render_bottom_border(10) == "└────────┘"
        assert SOLID.render_bottom_border(5) == "└───┘"

    def test_render_bottom_border_double(self):
        """Test rendering bottom border with double style."""
        assert DOUBLE.render_bottom_border(10) == "╚════════╝"

    def test_render_bottom_border_ascii(self):
        """Test rendering bottom border with ASCII style."""
        assert ASCII.render_bottom_border(10) == "+--------+"

    def test_render_bottom_border_rounded(self):
        """Test rendering bottom border with rounded style."""
        assert ROUNDED.render_bottom_border(10) == "╰────────╯"

    def test_render_bottom_border_minimum_width(self):
        """Test bottom border with minimum width."""
        result = SOLID.render_bottom_border(2)
        assert result == "└┘"


class TestRenderDivider:
    """Test divider rendering."""

    def test_render_divider_solid(self):
        """Test rendering divider with solid style."""
        assert SOLID.render_divider(10) == "├────────┤"
        assert SOLID.render_divider(5) == "├───┤"

    def test_render_divider_double(self):
        """Test rendering divider with double style."""
        assert DOUBLE.render_divider(10) == "╠════════╣"

    def test_render_divider_ascii(self):
        """Test rendering divider with ASCII style."""
        assert ASCII.render_divider(10) == "+--------+"

    def test_render_divider_heavy(self):
        """Test rendering divider with heavy style."""
        assert HEAVY.render_divider(10) == "┣━━━━━━━━┫"

    def test_render_divider_minimum_width(self):
        """Test divider with minimum width."""
        result = SOLID.render_divider(2)
        assert result == "├┤"


class TestPredefinedStyles:
    """Test all predefined border styles."""

    def test_solid_style(self):
        """Test SOLID border style characters."""
        assert SOLID.name == "solid"
        assert SOLID.top_left == "┌"
        assert SOLID.top_right == "┐"
        assert SOLID.bottom_left == "└"
        assert SOLID.bottom_right == "┘"
        assert SOLID.horizontal == "─"
        assert SOLID.vertical == "│"

    def test_double_style(self):
        """Test DOUBLE border style characters."""
        assert DOUBLE.name == "double"
        assert DOUBLE.top_left == "╔"
        assert DOUBLE.horizontal == "═"
        assert DOUBLE.vertical == "║"

    def test_rounded_style(self):
        """Test ROUNDED border style characters."""
        assert ROUNDED.name == "rounded"
        assert ROUNDED.top_left == "╭"
        assert ROUNDED.top_right == "╮"
        assert ROUNDED.bottom_left == "╰"
        assert ROUNDED.bottom_right == "╯"

    def test_heavy_style(self):
        """Test HEAVY border style characters."""
        assert HEAVY.name == "heavy"
        assert HEAVY.top_left == "┏"
        assert HEAVY.horizontal == "━"
        assert HEAVY.vertical == "┃"

    def test_thick_style(self):
        """Test THICK border style characters."""
        assert THICK.name == "thick"
        assert THICK.horizontal == "▀"
        assert THICK.vertical == "█"

    def test_ascii_style(self):
        """Test ASCII border style characters."""
        assert ASCII.name == "ascii"
        assert ASCII.top_left == "+"
        assert ASCII.horizontal == "-"
        assert ASCII.vertical == "|"
        assert ASCII.cross == "+"

    def test_minimal_style(self):
        """Test MINIMAL border style characters."""
        assert MINIMAL.name == "minimal"
        assert MINIMAL.top_left == " "
        assert MINIMAL.horizontal == "─"
        assert MINIMAL.vertical == " "

    def test_dots_style(self):
        """Test DOTS border style characters."""
        assert DOTS.name == "dots"
        assert DOTS.top_left == "·"
        assert DOTS.horizontal == "·"
        assert DOTS.vertical == "·"


class TestBordersDictionary:
    """Test BORDERS dictionary."""

    def test_borders_contains_all_styles(self):
        """Test that BORDERS dict contains all predefined styles."""
        assert "solid" in BORDERS
        assert "double" in BORDERS
        assert "rounded" in BORDERS
        assert "heavy" in BORDERS
        assert "thick" in BORDERS
        assert "ascii" in BORDERS
        assert "minimal" in BORDERS
        assert "dots" in BORDERS

    def test_borders_access(self):
        """Test accessing styles via BORDERS dictionary."""
        assert BORDERS["solid"] is SOLID
        assert BORDERS["double"] is DOUBLE
        assert BORDERS["rounded"] is ROUNDED
        assert BORDERS["heavy"] is HEAVY
        assert BORDERS["ascii"] is ASCII

    def test_borders_count(self):
        """Test number of predefined border styles."""
        assert len(BORDERS) == 9


class TestGetBorderStyle:
    """Test get_border_style function."""

    def test_get_border_style_lowercase(self):
        """Test getting border style with lowercase name."""
        style = get_border_style("solid")
        assert style is SOLID

    def test_get_border_style_uppercase(self):
        """Test getting border style with uppercase name."""
        style = get_border_style("DOUBLE")
        assert style is DOUBLE

    def test_get_border_style_mixed_case(self):
        """Test getting border style with mixed case name."""
        style = get_border_style("RoUnDeD")
        assert style is ROUNDED

    def test_get_border_style_invalid(self):
        """Test getting invalid border style raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            get_border_style("invalid")
        assert "Unknown border style: 'invalid'" in str(exc_info.value)
        assert "Available:" in str(exc_info.value)

    def test_get_border_style_error_message_lists_styles(self):
        """Test that error message lists available styles."""
        with pytest.raises(ValueError) as exc_info:
            get_border_style("nonexistent")
        error_msg = str(exc_info.value)
        assert "solid" in error_msg
        assert "double" in error_msg
        assert "ascii" in error_msg


class TestListBorderStyles:
    """Test list_border_styles function."""

    def test_list_border_styles_returns_all(self):
        """Test that list_border_styles returns all style names."""
        styles = list_border_styles()
        assert len(styles) == 9
        assert "solid" in styles
        assert "double" in styles
        assert "rounded" in styles
        assert "heavy" in styles
        assert "thick" in styles
        assert "rounded_thick" in styles
        assert "ascii" in styles
        assert "minimal" in styles
        assert "dots" in styles

    def test_list_border_styles_is_sorted(self):
        """Test that list_border_styles returns sorted list."""
        styles = list_border_styles()
        assert styles == sorted(styles)

    def test_list_border_styles_returns_copy(self):
        """Test that list_border_styles returns a new list."""
        styles1 = list_border_styles()
        styles2 = list_border_styles()
        assert styles1 == styles2
        assert styles1 is not styles2  # Different list objects


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_render_complete_frame(self):
        """Test rendering a complete frame with all components."""
        style = SOLID
        width = 20

        # Assemble a complete frame
        top = style.render_top_border(width, "Frame")
        bottom = style.render_bottom_border(width)
        divider = style.render_divider(width)

        assert len(top) == width
        assert len(bottom) == width
        assert len(divider) == width

        # Check structure
        assert top.startswith("┌")
        assert top.endswith("┐")
        assert bottom.startswith("└")
        assert bottom.endswith("┘")
        assert divider.startswith("├")
        assert divider.endswith("┤")

    def test_different_styles_different_characters(self):
        """Test that different styles use different characters."""
        solid_top = SOLID.render_top_border(10)
        double_top = DOUBLE.render_top_border(10)
        ascii_top = ASCII.render_top_border(10)

        # All should be same length
        assert len(solid_top) == len(double_top) == len(ascii_top) == 10

        # But use different characters
        assert solid_top != double_top
        assert double_top != ascii_top
        assert solid_top != ascii_top

    def test_unicode_characters_present(self):
        """Test that Unicode styles use actual Unicode characters."""
        # SOLID uses Unicode box drawing
        assert ord(SOLID.horizontal) > 127  # Non-ASCII
        assert ord(SOLID.vertical) > 127

        # ASCII uses only ASCII characters
        assert ord(ASCII.horizontal) < 128
        assert ord(ASCII.vertical) < 128

    def test_all_styles_have_complete_character_set(self):
        """Test that all predefined styles have all required characters."""
        for name, style in BORDERS.items():
            assert style.name == name
            assert len(style.top_left) == 1
            assert len(style.top_right) == 1
            assert len(style.bottom_left) == 1
            assert len(style.bottom_right) == 1
            assert len(style.horizontal) == 1
            assert len(style.vertical) == 1
            assert len(style.left_joint) == 1
            assert len(style.right_joint) == 1
            assert len(style.top_joint) == 1
            assert len(style.bottom_joint) == 1
            assert len(style.cross) == 1

    def test_rendering_with_very_large_dimensions(self):
        """Test rendering with very large dimensions."""
        style = SOLID
        horizontal = style.render_horizontal(1000)
        assert len(horizontal) == 1000
        assert horizontal == "─" * 1000

        vertical = style.render_vertical(500)
        assert len(vertical) == 500
        assert all(line == "│" for line in vertical)

    def test_title_with_special_characters(self):
        """Test rendering title with special characters."""
        from styledconsole import visual_width

        result = SOLID.render_top_border(20, "🚀 Test")
        # Emoji has visual_width=2 but len=1, so check visual width
        assert visual_width(result) == 20
        assert "🚀" in result or "Test" in result  # Either emoji or text visible
