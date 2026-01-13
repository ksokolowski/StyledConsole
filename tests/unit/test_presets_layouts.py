"""Tests for presets/layouts.py - create_layout_from_config factory."""

import pytest

from styledconsole.presets.layouts import create_layout_from_config


class TestCreateLayoutFromConfig:
    """Tests for the create_layout_from_config factory function."""

    def test_text_element(self):
        """Text element creates Text renderable."""
        config = {"type": "text", "content": "Hello World"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_text_element_with_style(self):
        """Text element with style parameter."""
        config = {"type": "text", "content": "Styled", "style": "bold red"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_rule_element(self):
        """Rule element creates horizontal rule."""
        config = {"type": "rule"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_rule_element_with_title(self):
        """Rule element with title."""
        config = {"type": "rule", "title": "Section"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_rule_element_with_style(self):
        """Rule element with style."""
        config = {"type": "rule", "style": "cyan"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_panel_element(self):
        """Panel element creates bordered panel."""
        config = {"type": "panel", "content": "Panel content"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_panel_element_with_title(self):
        """Panel element with title."""
        config = {"type": "panel", "content": "Content", "title": "Title"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_frame_element(self):
        """Frame element creates StyledFrame."""
        config = {"type": "frame", "content": "Frame content"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_frame_element_with_title(self):
        """Frame element with title."""
        config = {"type": "frame", "content": "Content", "title": "Frame Title"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_group_element(self):
        """Group element creates nested Group."""
        config = {
            "type": "group",
            "items": [
                {"type": "text", "content": "Item 1"},
                {"type": "text", "content": "Item 2"},
            ],
        }
        result = create_layout_from_config(config)
        assert result is not None

    def test_vspacer_element(self):
        """Vspacer element creates vertical spacing."""
        config = {"type": "vspacer", "lines": 2}
        result = create_layout_from_config(config)
        assert result is not None

    def test_vspacer_default_lines(self):
        """Vspacer element with default lines (1)."""
        config = {"type": "vspacer"}
        result = create_layout_from_config(config)
        assert result is not None

    def test_table_element(self):
        """Table element creates table from config."""
        config = {
            "type": "table",
            "theme": {},
            "data": {
                "columns": [{"header": "Name"}, {"header": "Value"}],
                "rows": [["foo", "bar"], ["baz", "qux"]],
            },
        }
        result = create_layout_from_config(config)
        assert result is not None

    def test_unknown_element_type_raises(self):
        """Unknown element type raises ValueError."""
        config = {"type": "unknown_type", "content": "test"}
        with pytest.raises(ValueError, match="Unknown layout item type"):
            create_layout_from_config(config)

    def test_nested_groups(self):
        """Nested group elements."""
        config = {
            "type": "group",
            "items": [
                {"type": "text", "content": "Outer"},
                {
                    "type": "group",
                    "items": [{"type": "text", "content": "Inner"}],
                },
            ],
        }
        result = create_layout_from_config(config)
        assert result is not None
