"""Unit tests for the declarative layer."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from styledconsole.declarative import (
    BUILTIN_TEMPLATES,
    Declarative,
    Template,
    TemplateRegistry,
    TemplateVariable,
    create,
    from_template,
    get_builtin_registry,
    load_dict,
    load_file,
    load_json,
    load_yaml,
    normalize,
    parse_data,
)
from styledconsole.model import Banner, Frame, Layout, Rule, Spacer, Table, Text

# =============================================================================
# Shorthand Normalization Tests
# =============================================================================


class TestNormalize:
    """Tests for shorthand normalization."""

    def test_normalize_string(self) -> None:
        """Test string normalizes to text."""
        result = normalize("Hello")
        assert result == {"type": "text", "content": "Hello"}

    def test_normalize_empty_string(self) -> None:
        """Test empty string normalizes to text."""
        result = normalize("")
        assert result == {"type": "text", "content": ""}

    def test_normalize_list(self) -> None:
        """Test list normalizes to vertical layout."""
        result = normalize(["a", "b", "c"])
        assert result["type"] == "vertical"
        assert len(result["children"]) == 3
        assert result["children"][0] == {"type": "text", "content": "a"}

    def test_normalize_empty_list(self) -> None:
        """Test empty list normalizes to empty layout."""
        result = normalize([])
        assert result == {"type": "vertical", "children": []}

    def test_normalize_nested_list(self) -> None:
        """Test nested lists normalize correctly."""
        result = normalize([["a", "b"], "c"])
        assert result["type"] == "vertical"
        assert result["children"][0]["type"] == "vertical"
        assert result["children"][1] == {"type": "text", "content": "c"}

    def test_normalize_frame_shorthand(self) -> None:
        """Test frame shorthand."""
        result = normalize({"frame": "Content", "title": "Title"})
        assert result["type"] == "frame"
        assert result["content"] == {"type": "text", "content": "Content"}
        assert result["title"] == "Title"

    def test_normalize_banner_shorthand(self) -> None:
        """Test banner shorthand."""
        result = normalize({"banner": "TEST", "font": "slant"})
        assert result["type"] == "banner"
        assert result["text"] == "TEST"
        assert result["font"] == "slant"

    def test_normalize_row_shorthand(self) -> None:
        """Test row shorthand for horizontal layout."""
        result = normalize({"row": ["a", "b"], "gap": 2})
        assert result["type"] == "horizontal"
        assert len(result["children"]) == 2
        assert result["gap"] == 2

    def test_normalize_column_shorthand(self) -> None:
        """Test column shorthand for vertical layout."""
        result = normalize({"column": ["a", "b"], "gap": 1})
        assert result["type"] == "vertical"
        assert len(result["children"]) == 2
        assert result["gap"] == 1

    def test_normalize_grid_shorthand(self) -> None:
        """Test grid shorthand."""
        result = normalize({"grid": ["a", "b", "c", "d"], "columns": 2})
        assert result["type"] == "grid"
        assert len(result["children"]) == 4
        assert result["columns"] == 2

    def test_normalize_typed_dict(self) -> None:
        """Test dict with type key passes through."""
        result = normalize({"type": "text", "content": "Hello"})
        assert result == {"type": "text", "content": "Hello"}

    def test_normalize_typed_dict_with_nested_content(self) -> None:
        """Test typed dict normalizes nested content."""
        result = normalize(
            {
                "type": "frame",
                "content": "Hello",  # String should normalize to text
                "title": "Title",
            }
        )
        assert result["type"] == "frame"
        assert result["content"] == {"type": "text", "content": "Hello"}

    def test_normalize_inferred_frame(self) -> None:
        """Test frame inference from keys."""
        result = normalize({"content": "Hello", "title": "Title"})
        assert result["type"] == "frame"

    def test_normalize_inferred_banner(self) -> None:
        """Test banner inference from keys."""
        result = normalize({"text": "HELLO", "font": "standard"})
        assert result["type"] == "banner"

    def test_normalize_inferred_table(self) -> None:
        """Test table inference from keys."""
        result = normalize(
            {
                "columns": ["A", "B"],
                "rows": [["1", "2"]],
            }
        )
        assert result["type"] == "table"

    def test_normalize_inferred_layout(self) -> None:
        """Test layout inference from children."""
        result = normalize(
            {
                "children": ["a", "b"],
                "direction": "horizontal",
            }
        )
        assert result["type"] == "horizontal"

    def test_normalize_invalid_type(self) -> None:
        """Test error on invalid type."""
        with pytest.raises(TypeError, match="Cannot normalize type"):
            normalize(123)

    def test_normalize_ambiguous_dict(self) -> None:
        """Test error on ambiguous dict."""
        with pytest.raises(ValueError, match="Cannot infer type"):
            normalize({"unknown_key": "value"})


# =============================================================================
# Template Tests
# =============================================================================


class TestTemplate:
    """Tests for Template class."""

    def test_render_simple(self) -> None:
        """Test simple variable substitution."""
        tmpl = Template({"type": "text", "content": "${msg}"})
        result = tmpl.render(msg="Hello")
        assert result == {"type": "text", "content": "Hello"}

    def test_render_with_default(self) -> None:
        """Test variable with default value."""
        tmpl = Template({"type": "text", "content": "${msg:Default}"})
        result = tmpl.render()
        assert result == {"type": "text", "content": "Default"}

    def test_render_override_default(self) -> None:
        """Test overriding default value."""
        tmpl = Template({"type": "text", "content": "${msg:Default}"})
        result = tmpl.render(msg="Custom")
        assert result == {"type": "text", "content": "Custom"}

    def test_render_nested(self) -> None:
        """Test nested variable substitution."""
        tmpl = Template(
            {
                "type": "frame",
                "title": "${title}",
                "content": {"type": "text", "content": "${msg}"},
            }
        )
        result = tmpl.render(title="Title", msg="Content")
        assert result["title"] == "Title"
        assert result["content"]["content"] == "Content"

    def test_render_missing_required(self) -> None:
        """Test error on missing required variable."""
        tmpl = Template({"type": "text", "content": "${msg}"})
        with pytest.raises(ValueError, match="Missing required variable"):
            tmpl.render()

    def test_render_non_string_value(self) -> None:
        """Test substituting non-string values."""
        tmpl = Template({"type": "table", "rows": "${rows}"})
        result = tmpl.render(rows=[["a", "b"]])
        assert result["rows"] == [["a", "b"]]

    def test_get_variables(self) -> None:
        """Test extracting variables from template."""
        tmpl = Template(
            {
                "type": "frame",
                "title": "${title}",
                "content": "${msg:Default}",
            }
        )
        variables = tmpl.get_variables()
        names = {v.name for v in variables}
        assert names == {"title", "msg"}

    def test_get_variables_with_defaults(self) -> None:
        """Test extracting variables with defaults."""
        tmpl = Template({"content": "${a}", "title": "${b:default}"})
        variables = {v.name: v.default for v in tmpl.get_variables()}
        assert variables["a"] is None
        assert variables["b"] == "default"

    def test_validate_all_provided(self) -> None:
        """Test validation with all variables provided."""
        tmpl = Template({"content": "${a}", "title": "${b}"})
        missing = tmpl.validate(a="x", b="y")
        assert missing == []

    def test_validate_missing_required(self) -> None:
        """Test validation catches missing required."""
        tmpl = Template({"content": "${a}", "title": "${b}"})
        missing = tmpl.validate(a="x")
        assert missing == ["b"]

    def test_validate_ignores_defaults(self) -> None:
        """Test validation ignores variables with defaults."""
        tmpl = Template({"content": "${a}", "title": "${b:default}"})
        missing = tmpl.validate()
        assert missing == ["a"]


class TestTemplateVariable:
    """Tests for TemplateVariable class."""

    def test_required_no_default(self) -> None:
        """Test required when no default."""
        var = TemplateVariable(name="x")
        assert var.required is True

    def test_not_required_with_default(self) -> None:
        """Test not required with default."""
        var = TemplateVariable(name="x", default="value")
        assert var.required is False


class TestTemplateRegistry:
    """Tests for TemplateRegistry class."""

    def test_register_and_get(self) -> None:
        """Test registering and retrieving template."""
        registry = TemplateRegistry()
        registry.register("test", {"type": "text", "content": "Hello"})
        tmpl = registry.get("test")
        assert tmpl is not None
        assert tmpl.definition == {"type": "text", "content": "Hello"}

    def test_register_template_instance(self) -> None:
        """Test registering Template instance."""
        registry = TemplateRegistry()
        tmpl = Template({"type": "text", "content": "Hello"})
        registry.register("test", tmpl)
        assert registry.get("test") is not None

    def test_get_missing(self) -> None:
        """Test getting missing template returns None."""
        registry = TemplateRegistry()
        assert registry.get("missing") is None

    def test_render(self) -> None:
        """Test rendering from registry."""
        registry = TemplateRegistry()
        registry.register("greet", {"type": "text", "content": "${msg}"})
        result = registry.render("greet", msg="World")
        assert result == {"type": "text", "content": "World"}

    def test_render_missing(self) -> None:
        """Test rendering missing template raises."""
        registry = TemplateRegistry()
        with pytest.raises(KeyError, match="not found"):
            registry.render("missing")

    def test_list_templates(self) -> None:
        """Test listing registered templates."""
        registry = TemplateRegistry()
        registry.register("a", {"type": "text", "content": "a"})
        registry.register("b", {"type": "text", "content": "b"})
        templates = registry.list_templates()
        assert set(templates) == {"a", "b"}

    def test_unregister(self) -> None:
        """Test unregistering template."""
        registry = TemplateRegistry()
        registry.register("test", {"type": "text", "content": "x"})
        assert registry.unregister("test") is True
        assert registry.get("test") is None
        assert registry.unregister("test") is False


class TestBuiltinTemplates:
    """Tests for built-in templates."""

    def test_builtin_templates_exist(self) -> None:
        """Test built-in templates are defined."""
        assert "info_box" in BUILTIN_TEMPLATES
        assert "warning_box" in BUILTIN_TEMPLATES
        assert "error_box" in BUILTIN_TEMPLATES
        assert "success_box" in BUILTIN_TEMPLATES

    def test_get_builtin_registry(self) -> None:
        """Test getting pre-populated registry."""
        registry = get_builtin_registry()
        assert registry.get("info_box") is not None
        assert len(registry.list_templates()) == len(BUILTIN_TEMPLATES)


# =============================================================================
# Loader Tests
# =============================================================================


class TestLoader:
    """Tests for file loading utilities."""

    def test_load_json(self) -> None:
        """Test loading from JSON string."""
        obj = load_json('{"type": "text", "content": "Hello"}')
        assert isinstance(obj, Text)
        assert obj.content == "Hello"

    def test_load_json_shorthand(self) -> None:
        """Test JSON with shorthand."""
        obj = load_json('"Hello"')
        assert isinstance(obj, Text)
        assert obj.content == "Hello"

    def test_load_json_with_variables(self) -> None:
        """Test JSON with template variables."""
        obj = load_json(
            '{"type": "text", "content": "${msg}"}',
            variables={"msg": "Hello"},
        )
        assert obj.content == "Hello"

    def test_load_dict(self) -> None:
        """Test loading from dict."""
        obj = load_dict({"type": "text", "content": "Hello"})
        assert isinstance(obj, Text)

    def test_load_dict_shorthand(self) -> None:
        """Test loading dict with shorthand."""
        obj = load_dict({"frame": "Content", "title": "Title"})
        assert isinstance(obj, Frame)

    def test_parse_data(self) -> None:
        """Test parsing without creating object."""
        result = parse_data("Hello")
        assert result == {"type": "text", "content": "Hello"}

    def test_load_file_json(self) -> None:
        """Test loading from JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"type": "text", "content": "From file"}, f)
            f.flush()
            obj = load_file(f.name)
            assert isinstance(obj, Text)
            assert obj.content == "From file"
            Path(f.name).unlink()

    def test_load_file_yaml(self) -> None:
        """Test loading from YAML file."""
        pytest.importorskip("yaml")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("type: text\ncontent: From YAML\n")
            f.flush()
            obj = load_file(f.name)
            assert isinstance(obj, Text)
            assert obj.content == "From YAML"
            Path(f.name).unlink()

    def test_load_file_not_found(self) -> None:
        """Test loading non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_file("/nonexistent/path.json")

    def test_load_file_unsupported_format(self) -> None:
        """Test loading unsupported format."""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            f.write(b"content")
            f.flush()
            with pytest.raises(ValueError, match="Unsupported file format"):
                load_file(f.name)
            Path(f.name).unlink()


class TestLoadYaml:
    """Tests for YAML loading."""

    def test_load_yaml(self) -> None:
        """Test loading from YAML string."""
        pytest.importorskip("yaml")
        obj = load_yaml("type: text\ncontent: Hello")
        assert isinstance(obj, Text)
        assert obj.content == "Hello"

    def test_load_yaml_shorthand(self) -> None:
        """Test YAML with shorthand."""
        pytest.importorskip("yaml")
        obj = load_yaml("frame: Content\ntitle: Title")
        assert isinstance(obj, Frame)

    def test_load_yaml_complex(self) -> None:
        """Test complex YAML structure."""
        pytest.importorskip("yaml")
        yaml_content = """
type: vertical
gap: 1
children:
  - type: text
    content: Item 1
  - type: text
    content: Item 2
"""
        obj = load_yaml(yaml_content)
        assert isinstance(obj, Layout)
        assert len(obj.children) == 2


# =============================================================================
# Declarative Facade Tests
# =============================================================================


class TestDeclarative:
    """Tests for Declarative facade."""

    @pytest.fixture
    def decl(self) -> Declarative:
        """Create Declarative instance."""
        return Declarative()

    def test_create_string(self, decl: Declarative) -> None:
        """Test creating from string."""
        obj = decl.create("Hello")
        assert isinstance(obj, Text)
        assert obj.content == "Hello"

    def test_create_list(self, decl: Declarative) -> None:
        """Test creating from list."""
        obj = decl.create(["a", "b"])
        assert isinstance(obj, Layout)
        assert obj.direction == "vertical"

    def test_create_frame_shorthand(self, decl: Declarative) -> None:
        """Test creating frame from shorthand."""
        obj = decl.create({"frame": "Content", "title": "Title"})
        assert isinstance(obj, Frame)
        assert obj.title == "Title"

    def test_create_with_variables(self, decl: Declarative) -> None:
        """Test creating with template variables."""
        obj = decl.create(
            {"type": "text", "content": "${msg}"},
            variables={"msg": "Hello"},
        )
        assert obj.content == "Hello"

    def test_parse(self, decl: Declarative) -> None:
        """Test parsing to dict."""
        result = decl.parse("Hello")
        assert result == {"type": "text", "content": "Hello"}

    def test_from_template(self, decl: Declarative) -> None:
        """Test creating from template."""
        obj = decl.from_template("info_box", message="Test")
        assert isinstance(obj, Frame)
        assert obj.effect == "ocean"

    def test_from_template_missing(self, decl: Declarative) -> None:
        """Test error on missing template."""
        with pytest.raises(KeyError, match="not found"):
            decl.from_template("nonexistent")

    def test_register_template(self, decl: Declarative) -> None:
        """Test registering custom template."""
        decl.register_template(
            "custom",
            {
                "type": "text",
                "content": "${msg}",
            },
        )
        obj = decl.from_template("custom", msg="Hello")
        assert obj.content == "Hello"

    def test_list_templates(self, decl: Declarative) -> None:
        """Test listing templates."""
        templates = decl.list_templates()
        assert "info_box" in templates
        assert len(templates) >= len(BUILTIN_TEMPLATES)

    def test_without_builtins(self) -> None:
        """Test creating without built-in templates."""
        decl = Declarative(include_builtins=False)
        assert decl.list_templates() == []


class TestConvenienceFunctions:
    """Tests for module-level convenience functions."""

    def test_create_function(self) -> None:
        """Test create() convenience function."""
        obj = create("Hello")
        assert isinstance(obj, Text)

    def test_from_template_function(self) -> None:
        """Test from_template() convenience function."""
        obj = from_template("info_box", message="Test")
        assert isinstance(obj, Frame)


# =============================================================================
# Integration Tests
# =============================================================================


class TestDeclarativeIntegration:
    """Integration tests for declarative layer."""

    def test_complex_layout(self) -> None:
        """Test creating complex nested layout."""
        data = {
            "column": [
                {"banner": "APP", "font": "slant"},
                {
                    "row": [
                        {"frame": "Panel 1", "title": "Left"},
                        {"frame": "Panel 2", "title": "Right"},
                    ],
                    "gap": 2,
                },
                {
                    "columns": ["Key", "Value"],
                    "rows": [["a", "1"], ["b", "2"]],
                },
            ],
            "gap": 1,
        }
        decl = Declarative()
        obj = decl.create(data)
        assert isinstance(obj, Layout)
        assert obj.direction == "vertical"
        assert len(obj.children) == 3
        assert isinstance(obj.children[0], Banner)
        assert isinstance(obj.children[1], Layout)
        assert isinstance(obj.children[2], Table)

    def test_template_with_nested_shorthand(self) -> None:
        """Test template that produces shorthand output."""
        decl = Declarative()
        decl.register_template(
            "panel_pair",
            {
                "row": [
                    {"frame": "${left}", "title": "${left_title:Left}"},
                    {"frame": "${right}", "title": "${right_title:Right}"},
                ],
            },
        )
        obj = decl.from_template(
            "panel_pair",
            left="Content 1",
            right="Content 2",
        )
        assert isinstance(obj, Layout)
        assert obj.direction == "horizontal"

    def test_all_object_types(self) -> None:
        """Test creating all supported object types."""
        decl = Declarative()

        # Text
        assert isinstance(decl.create("text"), Text)

        # Frame
        assert isinstance(decl.create({"frame": "x"}), Frame)

        # Banner
        assert isinstance(decl.create({"banner": "X"}), Banner)

        # Table
        assert isinstance(
            decl.create({"columns": ["A"], "rows": [["1"]]}),
            Table,
        )

        # Layout
        assert isinstance(decl.create(["a", "b"]), Layout)

        # Rule
        assert isinstance(
            decl.create({"type": "rule", "title": "Section"}),
            Rule,
        )

        # Spacer
        assert isinstance(
            decl.create({"type": "spacer", "lines": 2}),
            Spacer,
        )
