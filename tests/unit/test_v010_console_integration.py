"""Integration tests for Console with new v0.10.0 API layers."""

from __future__ import annotations

import pytest

from styledconsole import (
    BannerBuilder,
    BannerModel,
    Column,
    Console,
    ConsoleObject,
    Declarative,
    FrameBuilder,
    FrameModel,
    Group,
    HTMLRenderer,
    Layout,
    LayoutBuilder,
    RenderContext,
    RuleModel,
    Spacer,
    Style,
    TableBuilder,
    TableModel,
    Template,
    TemplateRegistry,
    TerminalRenderer,
    Text,
    create_object,
    from_template,
    load_dict,
    normalize,
)

# =============================================================================
# Console Builder Factory Tests
# =============================================================================


class TestConsoleBuilderFactories:
    """Tests for Console.build_*() factory methods."""

    @pytest.fixture
    def console(self) -> Console:
        """Create test console."""
        return Console()

    def test_build_frame_returns_builder(self, console: Console) -> None:
        """Test build_frame() returns FrameBuilder."""
        builder = console.build_frame()
        assert isinstance(builder, FrameBuilder)
        assert builder._console is console

    def test_build_banner_returns_builder(self, console: Console) -> None:
        """Test build_banner() returns BannerBuilder."""
        builder = console.build_banner()
        assert isinstance(builder, BannerBuilder)
        assert builder._console is console

    def test_build_table_returns_builder(self, console: Console) -> None:
        """Test build_table() returns TableBuilder."""
        builder = console.build_table()
        assert isinstance(builder, TableBuilder)
        assert builder._console is console

    def test_build_layout_returns_builder(self, console: Console) -> None:
        """Test build_layout() returns LayoutBuilder."""
        builder = console.build_layout()
        assert isinstance(builder, LayoutBuilder)
        assert builder._console is console

    def test_builder_can_build(self, console: Console) -> None:
        """Test builder can build object."""
        frame = console.build_frame().content("Test").title("Title").build()
        assert isinstance(frame, FrameModel)
        assert frame.title == "Title"

    def test_builder_can_render(self, console: Console) -> None:
        """Test builder can render directly."""
        # Just verify no exception - output goes to stdout
        console.build_frame().content("Render test").render()


# =============================================================================
# Console render_object Tests
# =============================================================================


class TestConsoleRenderObject:
    """Tests for Console.render_object() method."""

    @pytest.fixture
    def console(self) -> Console:
        """Create test console with buffer."""
        return Console()

    def test_render_text(self, console: Console) -> None:
        """Test rendering Text object."""
        text = Text(content="Hello World")
        console.render_object(text)  # Should not raise

    def test_render_frame(self, console: Console) -> None:
        """Test rendering Frame object."""
        frame = FrameModel(content=Text(content="Content"), title="Title")
        console.render_object(frame)

    def test_render_layout(self, console: Console) -> None:
        """Test rendering Layout object."""
        layout = Layout(
            direction="vertical",
            children=(Text(content="A"), Text(content="B")),
        )
        console.render_object(layout)

    def test_render_with_context(self, console: Console) -> None:
        """Test rendering with custom context."""
        text = Text(content="Custom context")
        ctx = RenderContext(width=40, color=True)
        console.render_object(text, context=ctx)


# =============================================================================
# Console Declarative Methods Tests
# =============================================================================


class TestConsoleDeclarative:
    """Tests for Console declarative methods."""

    @pytest.fixture
    def console(self) -> Console:
        """Create test console."""
        return Console()

    def test_render_dict_string(self, console: Console) -> None:
        """Test render_dict with string."""
        console.render_dict("Hello")

    def test_render_dict_list(self, console: Console) -> None:
        """Test render_dict with list."""
        console.render_dict(["Item 1", "Item 2"])

    def test_render_dict_frame_shorthand(self, console: Console) -> None:
        """Test render_dict with frame shorthand."""
        console.render_dict({"frame": "Content", "title": "Title"})

    def test_render_dict_with_variables(self, console: Console) -> None:
        """Test render_dict with template variables."""
        console.render_dict(
            {"type": "text", "content": "${msg}"},
            variables={"msg": "Variable test"},
        )

    def test_render_template(self, console: Console) -> None:
        """Test render_template with built-in template."""
        console.render_template("info_box", message="Test message")

    def test_render_template_error_box(self, console: Console) -> None:
        """Test render_template with error_box."""
        console.render_template("error_box", message="Error!")


# =============================================================================
# Package Export Tests
# =============================================================================


class TestPackageExports:
    """Tests for package-level exports."""

    def test_model_exports(self) -> None:
        """Test model layer exports."""
        assert Text is not None
        assert FrameModel is not None
        assert BannerModel is not None
        assert TableModel is not None
        assert Layout is not None
        assert Group is not None
        assert Spacer is not None
        assert RuleModel is not None
        assert Style is not None
        assert Column is not None
        assert ConsoleObject is not None

    def test_builder_exports(self) -> None:
        """Test builder layer exports."""
        assert FrameBuilder is not None
        assert BannerBuilder is not None
        assert TableBuilder is not None
        assert LayoutBuilder is not None

    def test_renderer_exports(self) -> None:
        """Test renderer layer exports."""
        assert TerminalRenderer is not None
        assert HTMLRenderer is not None
        assert RenderContext is not None

    def test_declarative_exports(self) -> None:
        """Test declarative layer exports."""
        assert Declarative is not None
        assert Template is not None
        assert TemplateRegistry is not None
        assert create_object is not None
        assert from_template is not None
        assert load_dict is not None
        assert normalize is not None


# =============================================================================
# End-to-End Integration Tests
# =============================================================================


class TestEndToEndIntegration:
    """End-to-end integration tests."""

    def test_full_workflow_builder(self) -> None:
        """Test complete workflow using builders."""
        console = Console()

        # Build frame
        frame = (
            console.build_frame()
            .content("Builder workflow test")
            .title("Test")
            .effect("ocean")
            .build()
        )

        assert isinstance(frame, FrameModel)
        assert frame.effect == "ocean"

    def test_full_workflow_declarative(self) -> None:
        """Test complete workflow using declarative API."""
        console = Console()

        # Create complex layout declaratively
        data = {
            "column": [
                {"banner": "APP", "font": "slant"},
                {
                    "row": [
                        {"frame": "Left", "title": "Panel 1"},
                        {"frame": "Right", "title": "Panel 2"},
                    ]
                },
            ]
        }

        # Should render without error
        console.render_dict(data)

    def test_full_workflow_model(self) -> None:
        """Test complete workflow using model directly."""
        console = Console()

        # Build model directly
        layout = Layout(
            direction="vertical",
            gap=1,
            children=(
                Text(content="Header", style=Style(bold=True)),
                FrameModel(
                    content=Text(content="Content"),
                    title="Frame",
                    effect="fire",
                ),
            ),
        )

        console.render_object(layout)

    def test_mixed_workflow(self) -> None:
        """Test mixing different APIs."""
        console = Console()

        # Use builder for frame
        frame = console.build_frame().content("From builder").build()

        # Use declarative for text
        text = load_dict("From declarative")

        # Combine in layout
        layout = Layout(
            direction="vertical",
            children=(text, frame),
        )

        console.render_object(layout)

    def test_template_customization(self) -> None:
        """Test customizing templates."""
        decl = Declarative()

        # Register custom template
        decl.register_template(
            "custom_panel",
            {
                "type": "frame",
                "title": "${title:Custom}",
                "content": {"type": "text", "content": "${msg}"},
                "effect": "${effect:steel}",
            },
        )

        # Use custom template
        obj = decl.from_template("custom_panel", msg="Custom content")
        assert isinstance(obj, FrameModel)

        # Render it
        console = Console()
        console.render_object(obj)

    def test_html_export_with_model(self) -> None:
        """Test HTML export with model objects."""
        renderer = HTMLRenderer()
        frame = FrameModel(
            content=Text(content="Export test"),
            title="Export",
            effect="ocean",
        )

        html = renderer.render_fragment(frame)
        assert "<div" in html
        assert "Export test" in html

    def test_render_context_propagation(self) -> None:
        """Test render context affects output."""
        renderer = TerminalRenderer()
        text = Text(content="Context test")

        # Narrow context
        ctx_narrow = RenderContext(width=40)
        result_narrow = renderer.render_to_string(text, context=ctx_narrow)

        # Wide context
        ctx_wide = RenderContext(width=120)
        result_wide = renderer.render_to_string(text, context=ctx_wide)

        # Both should contain content
        assert "Context test" in result_narrow
        assert "Context test" in result_wide
