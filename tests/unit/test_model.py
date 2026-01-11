"""Unit tests for the model layer.

Tests cover:
- Style creation and serialization
- All ConsoleObject types
- Nested object structures
- Serialization round-trips (JSON, YAML)
- Registry and factory functions
"""

from __future__ import annotations

import json

import pytest

from styledconsole.model import (
    Banner,
    Column,
    Frame,
    Group,
    Layout,
    Rule,
    Spacer,
    Style,
    Table,
    Text,
    create_object,
    from_json,
)


class TestStyle:
    """Tests for Style dataclass."""

    def test_default_style(self):
        """Style with no args has all defaults."""
        style = Style()
        assert style.color is None
        assert style.background is None
        assert style.bold is False
        assert style.italic is False

    def test_style_with_color(self):
        """Style can be created with color."""
        style = Style(color="cyan")
        assert style.color == "cyan"

    def test_style_with_modifiers(self):
        """Style can be created with text modifiers."""
        style = Style(bold=True, italic=True, underline=True)
        assert style.bold is True
        assert style.italic is True
        assert style.underline is True

    def test_style_to_dict_minimal(self):
        """Empty style serializes to empty dict."""
        style = Style()
        assert style.to_dict() == {}

    def test_style_to_dict_with_values(self):
        """Style serializes only non-default values."""
        style = Style(color="red", bold=True)
        result = style.to_dict()
        assert result == {"color": "red", "bold": True}

    def test_style_from_dict(self):
        """Style can be deserialized from dict."""
        data = {"color": "green", "italic": True}
        style = Style.from_dict(data)
        assert style.color == "green"
        assert style.italic is True
        assert style.bold is False

    def test_style_merge_with(self):
        """Style.merge_with combines two styles."""
        base = Style(color="blue", bold=True)
        override = Style(color="red")
        merged = base.merge_with(override)
        assert merged.color == "red"  # Overridden
        assert merged.bold is True  # Kept from base

    def test_style_immutable(self):
        """Style is immutable (frozen)."""
        style = Style(color="cyan")
        with pytest.raises(AttributeError):
            style.color = "red"  # type: ignore


class TestText:
    """Tests for Text object."""

    def test_text_creation(self):
        """Text can be created with content."""
        text = Text(content="Hello World")
        assert text.content == "Hello World"

    def test_text_with_style(self):
        """Text can have style."""
        style = Style(color="cyan")
        text = Text(content="Styled", style=style)
        assert text.style == style

    def test_text_to_dict(self):
        """Text serializes correctly."""
        text = Text(content="Test")
        result = text.to_dict()
        assert result == {"type": "text", "content": "Test"}

    def test_text_to_dict_with_style(self):
        """Text with style serializes both."""
        text = Text(content="Test", style=Style(color="red"))
        result = text.to_dict()
        assert result == {
            "type": "text",
            "style": {"color": "red"},
            "content": "Test",
        }

    def test_text_to_json(self):
        """Text can serialize to JSON."""
        text = Text(content="Hello")
        json_str = text.to_json()
        data = json.loads(json_str)
        assert data["type"] == "text"
        assert data["content"] == "Hello"


class TestFrame:
    """Tests for Frame object."""

    def test_frame_creation(self):
        """Frame can be created with content."""
        content = Text(content="Hello")
        frame = Frame(content=content, title="Greeting")
        assert frame.title == "Greeting"
        assert frame.content == content

    def test_frame_defaults(self):
        """Frame has sensible defaults."""
        frame = Frame()
        assert frame.border == "solid"
        assert frame.padding == 1
        assert frame.align == "left"

    def test_frame_with_effect(self):
        """Frame can have an effect."""
        frame = Frame(content=Text(content="Test"), effect="ocean")
        assert frame.effect == "ocean"

    def test_frame_to_dict(self):
        """Frame serializes correctly."""
        frame = Frame(
            content=Text(content="Test"),
            title="Title",
            effect="fire",
        )
        result = frame.to_dict()
        assert result["type"] == "frame"
        assert result["title"] == "Title"
        assert result["effect"] == "fire"
        assert result["content"]["type"] == "text"

    def test_frame_to_dict_minimal(self):
        """Frame only serializes non-default values."""
        frame = Frame(content=Text(content="X"))
        result = frame.to_dict()
        # Should not include default values
        assert "border" not in result  # "solid" is default
        assert "padding" not in result  # 1 is default
        assert "align" not in result  # "left" is default


class TestBanner:
    """Tests for Banner object."""

    def test_banner_creation(self):
        """Banner can be created with text."""
        banner = Banner(text="HELLO")
        assert banner.text == "HELLO"
        assert banner.font == "standard"

    def test_banner_with_font(self):
        """Banner can specify a font."""
        banner = Banner(text="TEST", font="slant")
        assert banner.font == "slant"

    def test_banner_to_dict(self):
        """Banner serializes correctly."""
        banner = Banner(text="DEMO", effect="fire")
        result = banner.to_dict()
        assert result == {
            "type": "banner",
            "text": "DEMO",
            "effect": "fire",
        }


class TestTable:
    """Tests for Table object."""

    def test_table_creation(self):
        """Table can be created with columns and rows."""
        table = Table(
            columns=(Column(header="Name"), Column(header="Age")),
            rows=(("Alice", 30), ("Bob", 25)),
        )
        assert len(table.columns) == 2
        assert len(table.rows) == 2

    def test_column_defaults(self):
        """Column has sensible defaults."""
        col = Column(header="Test")
        assert col.align == "left"
        assert col.width is None

    def test_table_to_dict(self):
        """Table serializes correctly."""
        table = Table(
            columns=(Column(header="Name"),),
            rows=(("Test",),),
            title="My Table",
        )
        result = table.to_dict()
        assert result["type"] == "table"
        assert result["title"] == "My Table"
        assert len(result["columns"]) == 1
        assert result["columns"][0]["header"] == "Name"


class TestLayout:
    """Tests for Layout object."""

    def test_layout_vertical(self):
        """Vertical layout is default."""
        layout = Layout(children=(Text(content="A"), Text(content="B")))
        assert layout.direction == "vertical"

    def test_layout_horizontal(self):
        """Horizontal layout can be specified."""
        layout = Layout(children=(), direction="horizontal")
        assert layout.direction == "horizontal"

    def test_layout_grid(self):
        """Grid layout with columns."""
        layout = Layout(children=(), direction="grid", columns=3)
        assert layout.direction == "grid"
        assert layout.columns == 3

    def test_layout_to_dict(self):
        """Layout serializes children correctly."""
        layout = Layout(
            children=(Text(content="A"), Text(content="B")),
            direction="horizontal",
            gap=2,
        )
        result = layout.to_dict()
        assert result["type"] == "layout"
        assert result["direction"] == "horizontal"
        assert result["gap"] == 2
        assert len(result["children"]) == 2


class TestGroup:
    """Tests for Group object."""

    def test_group_creation(self):
        """Group can hold multiple objects."""
        group = Group(children=(Text(content="A"), Text(content="B")))
        assert len(group.children) == 2

    def test_group_to_dict(self):
        """Group serializes correctly."""
        group = Group(children=(Text(content="X"),))
        result = group.to_dict()
        assert result["type"] == "group"
        assert len(result["children"]) == 1


class TestSpacer:
    """Tests for Spacer object."""

    def test_spacer_default(self):
        """Default spacer has 1 line."""
        spacer = Spacer()
        assert spacer.lines == 1

    def test_spacer_custom(self):
        """Spacer can have custom lines."""
        spacer = Spacer(lines=3)
        assert spacer.lines == 3

    def test_spacer_to_dict_default(self):
        """Default spacer serializes minimally."""
        spacer = Spacer()
        result = spacer.to_dict()
        assert result == {"type": "spacer"}

    def test_spacer_to_dict_custom(self):
        """Custom spacer includes lines."""
        spacer = Spacer(lines=5)
        result = spacer.to_dict()
        assert result == {"type": "spacer", "lines": 5}


class TestRule:
    """Tests for Rule object."""

    def test_rule_simple(self):
        """Simple rule with no title."""
        rule = Rule()
        assert rule.title is None

    def test_rule_with_title(self):
        """Rule can have a title."""
        rule = Rule(title="Section")
        assert rule.title == "Section"

    def test_rule_to_dict(self):
        """Rule serializes correctly."""
        rule = Rule(title="Divider")
        result = rule.to_dict()
        assert result == {"type": "rule", "title": "Divider"}


class TestCreateObject:
    """Tests for create_object factory function."""

    def test_create_text(self):
        """Create Text from dict."""
        obj = create_object({"type": "text", "content": "Hello"})
        assert isinstance(obj, Text)
        assert obj.content == "Hello"

    def test_create_frame(self):
        """Create Frame from dict."""
        obj = create_object(
            {
                "type": "frame",
                "title": "Test",
                "content": {"type": "text", "content": "Body"},
            }
        )
        assert isinstance(obj, Frame)
        assert obj.title == "Test"
        assert isinstance(obj.content, Text)

    def test_create_layout_alias(self):
        """Layout type aliases work."""
        h = create_object({"type": "horizontal", "children": []})
        assert isinstance(h, Layout)
        assert h.direction == "horizontal"

        v = create_object({"type": "vertical", "children": []})
        assert v.direction == "vertical"

        g = create_object({"type": "grid", "children": [], "columns": 2})
        assert g.direction == "grid"

    def test_create_with_style(self):
        """Objects can be created with style."""
        obj = create_object(
            {
                "type": "text",
                "content": "Styled",
                "style": {"color": "cyan", "bold": True},
            }
        )
        assert obj.style is not None
        assert obj.style.color == "cyan"
        assert obj.style.bold is True

    def test_unknown_type_raises(self):
        """Unknown type raises ValueError."""
        with pytest.raises(ValueError, match="Unknown object type"):
            create_object({"type": "nonexistent"})

    def test_missing_type_raises(self):
        """Missing type raises ValueError."""
        with pytest.raises(ValueError, match="Missing 'type' key"):
            create_object({"content": "no type"})


class TestFromJson:
    """Tests for from_json function."""

    def test_from_json_text(self):
        """Parse Text from JSON."""
        obj = from_json('{"type": "text", "content": "Hello"}')
        assert isinstance(obj, Text)
        assert obj.content == "Hello"

    def test_from_json_nested(self):
        """Parse nested structure from JSON."""
        json_str = json.dumps(
            {
                "type": "layout",
                "direction": "vertical",
                "children": [
                    {"type": "text", "content": "A"},
                    {"type": "text", "content": "B"},
                ],
            }
        )
        obj = from_json(json_str)
        assert isinstance(obj, Layout)
        assert len(obj.children) == 2


class TestRoundTrip:
    """Tests for serialization round-trips."""

    def test_text_roundtrip(self):
        """Text survives JSON round-trip."""
        original = Text(content="Test", style=Style(color="red"))
        json_str = original.to_json()
        restored = from_json(json_str)
        assert restored.content == original.content
        assert restored.style.color == original.style.color

    def test_frame_roundtrip(self):
        """Frame survives JSON round-trip."""
        original = Frame(
            content=Text(content="Body"),
            title="Title",
            effect="ocean",
            border="rounded",
        )
        json_str = original.to_json()
        restored = from_json(json_str)
        assert restored.title == original.title
        assert restored.effect == original.effect
        assert restored.border == original.border

    def test_complex_layout_roundtrip(self):
        """Complex layout survives JSON round-trip."""
        original = Layout(
            children=(
                Banner(text="HEADER", effect="fire"),
                Layout(
                    children=(
                        Frame(content=Text(content="Left"), title="L"),
                        Frame(content=Text(content="Right"), title="R"),
                    ),
                    direction="horizontal",
                    gap=2,
                ),
                Rule(title="Footer"),
            ),
            direction="vertical",
            gap=1,
        )
        json_str = original.to_json()
        restored = from_json(json_str)

        assert len(restored.children) == 3
        assert isinstance(restored.children[0], Banner)
        assert isinstance(restored.children[1], Layout)
        assert isinstance(restored.children[2], Rule)


class TestImmutability:
    """Tests for object immutability."""

    def test_text_immutable(self):
        """Text objects are immutable."""
        text = Text(content="Original")
        with pytest.raises(AttributeError):
            text.content = "Modified"  # type: ignore

    def test_frame_immutable(self):
        """Frame objects are immutable."""
        frame = Frame(title="Original")
        with pytest.raises(AttributeError):
            frame.title = "Modified"  # type: ignore

    def test_layout_immutable(self):
        """Layout objects are immutable."""
        layout = Layout(gap=1)
        with pytest.raises(AttributeError):
            layout.gap = 2  # type: ignore
