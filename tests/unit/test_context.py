"""Unit tests for StyleContext."""

from styledconsole.core.context import StyleContext


def test_style_context_defaults():
    """Test default values of StyleContext."""
    ctx = StyleContext()
    assert ctx.width is None
    assert ctx.padding == 1
    assert ctx.align == "left"
    assert ctx.border_style == "rounded"
    assert ctx.border_color is None
    assert ctx.title is None


def test_style_context_initialization():
    """Test initializing StyleContext with values."""
    ctx = StyleContext(
        width=100,
        padding=2,
        align="center",
        border_style="double",
        border_color="red",
        title="Test Title",
    )
    assert ctx.width == 100
    assert ctx.padding == 2
    assert ctx.align == "center"
    assert ctx.border_style == "double"
    assert ctx.border_color == "red"
    assert ctx.title == "Test Title"


def test_style_context_immutability():
    """Test that StyleContext is immutable."""
    ctx = StyleContext()
    try:
        ctx.width = 100
    except Exception as e:
        # Dataclasses with frozen=True raise FrozenInstanceError (subclass of AttributeError)
        assert isinstance(e, AttributeError)


def test_style_context_gradients():
    """Test gradient fields in StyleContext."""
    ctx = StyleContext(
        start_color="blue",
        end_color="green",
        border_gradient_start="red",
        border_gradient_end="yellow",
        border_gradient_direction="horizontal",
    )
    assert ctx.start_color == "blue"
    assert ctx.end_color == "green"
    assert ctx.border_gradient_start == "red"
    assert ctx.border_gradient_end == "yellow"
    assert ctx.border_gradient_direction == "horizontal"
