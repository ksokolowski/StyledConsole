"""Unit tests for the rendering layer."""

from __future__ import annotations

import io

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
)
from styledconsole.rendering import HTMLRenderer, RenderContext, TerminalRenderer

# =============================================================================
# RenderContext Tests
# =============================================================================


class TestRenderContext:
    """Tests for RenderContext dataclass."""

    def test_default_values(self) -> None:
        """Test default context values."""
        ctx = RenderContext()
        assert ctx.color is True
        assert ctx.emoji is True
        assert ctx.color_depth == 256
        assert ctx.width == 80
        assert ctx.height == 24
        assert ctx.theme is None

    def test_custom_values(self) -> None:
        """Test context with custom values."""
        ctx = RenderContext(
            color=False,
            emoji=False,
            color_depth=16,
            width=120,
            height=40,
        )
        assert ctx.color is False
        assert ctx.emoji is False
        assert ctx.color_depth == 16
        assert ctx.width == 120
        assert ctx.height == 40

    def test_auto_detect(self) -> None:
        """Test auto-detection creates valid context."""
        ctx = RenderContext.auto_detect()
        assert isinstance(ctx.color, bool)
        assert isinstance(ctx.emoji, bool)
        assert ctx.color_depth in (1, 4, 8, 256, 16777216)
        assert ctx.width > 0
        assert ctx.height > 0

    def test_for_html(self) -> None:
        """Test HTML-optimized context."""
        ctx = RenderContext.for_html()
        assert ctx.color is True
        assert ctx.emoji is True
        assert ctx.color_depth == 16777216  # True color
        assert ctx.width == 120

    def test_for_html_custom_width(self) -> None:
        """Test HTML context with custom width."""
        ctx = RenderContext.for_html(width=200)
        assert ctx.width == 200

    def test_minimal(self) -> None:
        """Test minimal context (no colors/emoji)."""
        ctx = RenderContext.minimal()
        assert ctx.color is False
        assert ctx.emoji is False
        assert ctx.color_depth == 16
        assert ctx.width == 80

    def test_for_image(self) -> None:
        """Test image context."""
        ctx = RenderContext.for_image(width=100, dpi=200)
        assert ctx.color is True
        assert ctx.emoji is True
        assert ctx.color_depth == 16777216
        assert ctx.width == 100
        assert ctx.dpi == 200


# =============================================================================
# TerminalRenderer Tests
# =============================================================================


class TestTerminalRenderer:
    """Tests for TerminalRenderer."""

    @pytest.fixture
    def renderer(self) -> TerminalRenderer:
        """Create a terminal renderer."""
        return TerminalRenderer()

    @pytest.fixture
    def context(self) -> RenderContext:
        """Create a test context."""
        return RenderContext(width=80)

    # -------------------------------------------------------------------------
    # Basic Object Rendering
    # -------------------------------------------------------------------------

    def test_render_text(self, renderer: TerminalRenderer) -> None:
        """Test rendering Text object."""
        text = Text(content="Hello World")
        result = renderer.render_to_string(text)
        assert "Hello World" in result

    def test_render_text_with_style(self, renderer: TerminalRenderer) -> None:
        """Test rendering styled Text."""
        text = Text(content="Bold Text", style=Style(bold=True))
        result = renderer.render_to_string(text)
        assert "Bold Text" in result

    def test_render_frame(self, renderer: TerminalRenderer) -> None:
        """Test rendering Frame object."""
        frame = Frame(content=Text(content="Content"), title="Title")
        result = renderer.render_to_string(frame)
        assert "Title" in result
        assert "Content" in result

    def test_render_frame_with_effect(self, renderer: TerminalRenderer) -> None:
        """Test rendering Frame with effect."""
        frame = Frame(
            content=Text(content="Ocean frame"),
            title="Ocean",
            effect="ocean",
        )
        result = renderer.render_to_string(frame)
        assert "Ocean" in result
        # Should contain ANSI escape codes for color
        assert "\x1b[" in result

    def test_render_frame_with_style(self, renderer: TerminalRenderer) -> None:
        """Test rendering Frame with style."""
        frame = Frame(
            content=Text(content="Styled"),
            title="Styled",
            style=Style(color="red", bold=True),
        )
        result = renderer.render_to_string(frame)
        assert "Styled" in result

    def test_render_frame_no_title(self, renderer: TerminalRenderer) -> None:
        """Test rendering Frame without title."""
        frame = Frame(content=Text(content="No title"))
        result = renderer.render_to_string(frame)
        assert "No title" in result

    def test_render_banner(self, renderer: TerminalRenderer) -> None:
        """Test rendering Banner object."""
        banner = Banner(text="TEST", font="slant")
        result = renderer.render_to_string(banner)
        # Figlet output contains ASCII art
        assert len(result) > len("TEST")

    def test_render_banner_with_effect(self, renderer: TerminalRenderer) -> None:
        """Test rendering Banner with effect."""
        banner = Banner(text="HI", font="slant", effect="fire")
        result = renderer.render_to_string(banner)
        # Should contain ANSI escape codes
        assert "\x1b[" in result

    def test_render_table(self, renderer: TerminalRenderer) -> None:
        """Test rendering Table object."""
        table = Table(
            columns=[Column(header="Name"), Column(header="Value")],
            rows=[["foo", "1"], ["bar", "2"]],
        )
        result = renderer.render_to_string(table)
        assert "Name" in result
        assert "Value" in result
        assert "foo" in result
        assert "bar" in result

    def test_render_table_with_title(self, renderer: TerminalRenderer) -> None:
        """Test rendering Table with title."""
        table = Table(
            title="My Table",
            columns=[Column(header="A"), Column(header="B")],
            rows=[["1", "2"]],
        )
        result = renderer.render_to_string(table)
        assert "My Table" in result

    def test_render_layout_vertical(self, renderer: TerminalRenderer) -> None:
        """Test rendering vertical Layout."""
        layout = Layout(
            direction="vertical",
            children=[Text(content="Item 1"), Text(content="Item 2")],
        )
        result = renderer.render_to_string(layout)
        assert "Item 1" in result
        assert "Item 2" in result

    def test_render_layout_horizontal(self, renderer: TerminalRenderer) -> None:
        """Test rendering horizontal Layout."""
        layout = Layout(
            direction="horizontal",
            children=[Text(content="Left"), Text(content="Right")],
        )
        result = renderer.render_to_string(layout)
        assert "Left" in result
        assert "Right" in result

    def test_render_group(self, renderer: TerminalRenderer) -> None:
        """Test rendering Group object."""
        group = Group(
            children=[Text(content="Child 1"), Text(content="Child 2")],
        )
        result = renderer.render_to_string(group)
        assert "Child 1" in result
        assert "Child 2" in result

    def test_render_spacer(self, renderer: TerminalRenderer) -> None:
        """Test rendering Spacer object."""
        spacer = Spacer(lines=3)
        result = renderer.render_to_string(spacer)
        # Should have 3 newlines plus trailing
        assert result.count("\n") >= 3

    def test_render_rule(self, renderer: TerminalRenderer) -> None:
        """Test rendering Rule object."""
        rule = Rule(title="Section")
        result = renderer.render_to_string(rule)
        assert "Section" in result
        assert "─" in result  # Contains horizontal line chars

    def test_render_rule_no_title(self, renderer: TerminalRenderer) -> None:
        """Test rendering Rule without title."""
        rule = Rule()
        result = renderer.render_to_string(rule)
        assert "─" in result

    # -------------------------------------------------------------------------
    # Render to Stream
    # -------------------------------------------------------------------------

    def test_render_to_stream(self, renderer: TerminalRenderer) -> None:
        """Test rendering to a stream."""
        text = Text(content="Stream test")
        stream = io.StringIO()
        renderer.render(text, target=stream)
        stream.seek(0)
        assert "Stream test" in stream.read()

    # -------------------------------------------------------------------------
    # Context Handling
    # -------------------------------------------------------------------------

    def test_render_with_context(self, renderer: TerminalRenderer) -> None:
        """Test rendering with custom context."""
        ctx = RenderContext(width=40)
        frame = Frame(content=Text(content="Narrow"), title="Test")
        result = renderer.render_to_string(frame, context=ctx)
        # Result should be narrower
        assert "Narrow" in result

    # -------------------------------------------------------------------------
    # Edge Cases
    # -------------------------------------------------------------------------

    def test_render_empty_text(self, renderer: TerminalRenderer) -> None:
        """Test rendering empty Text."""
        text = Text(content="")
        result = renderer.render_to_string(text)
        assert result == "\n"

    def test_render_nested_frame(self, renderer: TerminalRenderer) -> None:
        """Test rendering nested Frame."""
        inner = Frame(content=Text(content="Inner"), title="Inner Frame")
        outer = Frame(content=inner, title="Outer Frame")
        result = renderer.render_to_string(outer)
        assert "Inner Frame" in result
        assert "Outer Frame" in result

    def test_render_text_multiline(self, renderer: TerminalRenderer) -> None:
        """Test rendering multiline Text."""
        text = Text(content="Line 1\nLine 2\nLine 3")
        result = renderer.render_to_string(text)
        assert "Line 1" in result
        assert "Line 2" in result


# =============================================================================
# HTMLRenderer Tests
# =============================================================================


class TestHTMLRenderer:
    """Tests for HTMLRenderer."""

    @pytest.fixture
    def renderer(self) -> HTMLRenderer:
        """Create an HTML renderer."""
        return HTMLRenderer()

    # -------------------------------------------------------------------------
    # Fragment Rendering
    # -------------------------------------------------------------------------

    def test_render_fragment_text(self, renderer: HTMLRenderer) -> None:
        """Test rendering Text as HTML fragment."""
        text = Text(content="Hello World")
        result = renderer.render_fragment(text)
        assert "<span>" in result
        assert "Hello World" in result
        assert "</span>" in result

    def test_render_fragment_text_with_style(self, renderer: HTMLRenderer) -> None:
        """Test rendering styled Text as HTML."""
        text = Text(content="Bold", style=Style(bold=True, color="red"))
        result = renderer.render_fragment(text)
        assert "font-weight: bold" in result
        assert "color: red" in result

    def test_render_fragment_frame(self, renderer: HTMLRenderer) -> None:
        """Test rendering Frame as HTML fragment."""
        frame = Frame(content=Text(content="Content"), title="Title")
        result = renderer.render_fragment(frame)
        assert "<div" in result
        assert "border:" in result
        assert "Content" in result

    def test_render_fragment_frame_with_effect(self, renderer: HTMLRenderer) -> None:
        """Test rendering Frame with effect as HTML."""
        frame = Frame(
            content=Text(content="Ocean"),
            title="Ocean",
            effect="ocean",
        )
        result = renderer.render_fragment(frame)
        assert "<div" in result
        assert "#" in result  # Should have color code

    def test_render_fragment_banner(self, renderer: HTMLRenderer) -> None:
        """Test rendering Banner as HTML fragment."""
        banner = Banner(text="HI", font="slant")
        result = renderer.render_fragment(banner)
        assert "<pre" in result
        assert "</pre>" in result

    def test_render_fragment_table(self, renderer: HTMLRenderer) -> None:
        """Test rendering Table as HTML fragment."""
        table = Table(
            columns=[Column(header="A"), Column(header="B")],
            rows=[["1", "2"]],
        )
        result = renderer.render_fragment(table)
        assert "<table" in result
        assert "<th>" in result or "<th " in result
        assert "<td>" in result or "<td " in result

    def test_render_fragment_layout(self, renderer: HTMLRenderer) -> None:
        """Test rendering Layout as HTML fragment."""
        layout = Layout(
            direction="vertical",
            children=[Text(content="Item 1"), Text(content="Item 2")],
        )
        result = renderer.render_fragment(layout)
        assert "<div" in result
        assert "Item 1" in result
        assert "Item 2" in result

    def test_render_fragment_group(self, renderer: HTMLRenderer) -> None:
        """Test rendering Group as HTML fragment."""
        group = Group(
            children=[Text(content="A"), Text(content="B")],
        )
        result = renderer.render_fragment(group)
        assert "<div" in result
        assert "A" in result
        assert "B" in result

    def test_render_fragment_spacer(self, renderer: HTMLRenderer) -> None:
        """Test rendering Spacer as HTML fragment."""
        spacer = Spacer(lines=2)
        result = renderer.render_fragment(spacer)
        # Should be div with height
        assert "<div" in result
        assert "height:" in result

    def test_render_fragment_rule(self, renderer: HTMLRenderer) -> None:
        """Test rendering Rule as HTML fragment."""
        rule = Rule(title="Section")
        result = renderer.render_fragment(rule)
        assert "<hr" in result

    # -------------------------------------------------------------------------
    # Document Rendering
    # -------------------------------------------------------------------------

    def test_render_document(self, renderer: HTMLRenderer) -> None:
        """Test rendering full HTML document."""
        text = Text(content="Hello")
        result = renderer.render_document(text)
        assert "<!DOCTYPE html>" in result
        assert "<html>" in result
        assert "<head>" in result
        assert "<body>" in result
        assert "Hello" in result

    def test_render_document_with_title(self, renderer: HTMLRenderer) -> None:
        """Test document with custom title."""
        text = Text(content="Content")
        result = renderer.render_document(text, title="My Page")
        assert "<title>My Page</title>" in result

    def test_render_document_with_context(self, renderer: HTMLRenderer) -> None:
        """Test document with custom context."""
        text = Text(content="Custom")
        ctx = RenderContext(width=100, background_color="#2d2d2d")
        result = renderer.render_document(text, context=ctx)
        assert "background" in result
        assert "#2d2d2d" in result

    def test_render_document_to_stream(self, renderer: HTMLRenderer) -> None:
        """Test rendering document to stream."""
        text = Text(content="Stream")
        stream = io.StringIO()
        renderer.render_document(text, target=stream)
        stream.seek(0)
        content = stream.read()
        assert "<!DOCTYPE html>" in content
        assert "Stream" in content

    # -------------------------------------------------------------------------
    # render Method (Convenience)
    # -------------------------------------------------------------------------

    def test_render_returns_fragment_when_no_target(self, renderer: HTMLRenderer) -> None:
        """Test render() returns fragment when no target given."""
        text = Text(content="Test")
        result = renderer.render(text)
        assert "<span>" in result
        assert "Test" in result

    # -------------------------------------------------------------------------
    # Edge Cases
    # -------------------------------------------------------------------------

    def test_render_empty_text(self, renderer: HTMLRenderer) -> None:
        """Test rendering empty Text as HTML."""
        text = Text(content="")
        result = renderer.render_fragment(text)
        assert "<span>" in result

    def test_render_nested_frame(self, renderer: HTMLRenderer) -> None:
        """Test rendering nested Frame as HTML."""
        inner = Frame(content=Text(content="Inner"), title="Inner")
        outer = Frame(content=inner, title="Outer")
        result = renderer.render_fragment(outer)
        assert "Inner" in result
        assert "Outer" in result

    def test_render_text_multiline(self, renderer: HTMLRenderer) -> None:
        """Test rendering multiline Text as HTML."""
        text = Text(content="Line 1\nLine 2")
        result = renderer.render_fragment(text)
        assert "Line 1" in result
        assert "Line 2" in result


# =============================================================================
# Integration Tests
# =============================================================================


class TestRendererIntegration:
    """Integration tests for renderers."""

    @pytest.fixture
    def complex_layout(self) -> Layout:
        """Create a complex layout for testing."""
        return Layout(
            direction="vertical",
            gap=1,
            children=[
                Banner(text="APP", font="slant"),
                Frame(
                    content=Text(content="Welcome message"),
                    title="Welcome",
                    effect="ocean",
                ),
                Layout(
                    direction="horizontal",
                    gap=2,
                    children=[
                        Frame(content=Text(content="Panel 1"), title="Left"),
                        Frame(content=Text(content="Panel 2"), title="Right"),
                    ],
                ),
                Table(
                    title="Data",
                    columns=[Column(header="Key"), Column(header="Value")],
                    rows=[["a", "1"], ["b", "2"], ["c", "3"]],
                ),
                Rule(title="End"),
            ],
        )

    def test_terminal_complex_layout(self, complex_layout: Layout) -> None:
        """Test terminal rendering of complex layout."""
        renderer = TerminalRenderer()
        result = renderer.render_to_string(complex_layout)
        assert "Welcome" in result
        assert "Panel 1" in result
        assert "Panel 2" in result
        assert "Key" in result
        assert "End" in result

    def test_html_complex_layout(self, complex_layout: Layout) -> None:
        """Test HTML rendering of complex layout."""
        renderer = HTMLRenderer()
        result = renderer.render_fragment(complex_layout)
        assert "<div" in result
        assert "Welcome" in result
        assert "Panel 1" in result

    def test_both_renderers_same_content(self) -> None:
        """Test both renderers handle same content."""
        frame = Frame(
            content=Text(content="Test content"),
            title="Test",
            effect="fire",
        )

        terminal = TerminalRenderer()
        html = HTMLRenderer()

        terminal_result = terminal.render_to_string(frame)
        html_result = html.render_fragment(frame)

        # Both should contain the content
        assert "Test content" in terminal_result
        assert "Test content" in html_result

        # Terminal should have ANSI codes
        assert "\x1b[" in terminal_result

        # HTML should have tags
        assert "<div" in html_result
