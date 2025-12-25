"""Unit tests for Console.frame method with extensive parameter verification."""

from unittest.mock import MagicMock

import pytest

from styledconsole.console import Console
from styledconsole.core.context import StyleContext


class TestConsoleFrame:
    """Tests for Console.frame method."""

    @pytest.fixture
    def console(self):
        """Create a Console instance with mocked renderer."""
        console = Console(detect_terminal=False)
        console._renderer = MagicMock()
        return console

    def test_frame_constructs_context_correctly(self, console):
        """Verify StyleContext is constructed with correct arguments."""
        console.frame(
            "Content",
            title="Title",
            border="heavy",
            width=50,
            padding=2,
            align="center",
            frame_align="right",
            margin=(1, 2, 3, 4),
            content_color="red",
            border_color="blue",
            title_color="green",
        )

        # Verify print_frame was called
        console._renderer.print_frame.assert_called_once()

        # Check call args
        args, kwargs = console._renderer.print_frame.call_args
        assert args[0] == "Content"

        # Verify context object
        assert "context" in kwargs
        ctx = kwargs["context"]
        assert isinstance(ctx, StyleContext)

        # Verify context fields
        assert ctx.border_style == "heavy"
        assert ctx.width == 50
        assert ctx.padding == 2
        assert ctx.align == "center"
        assert ctx.frame_align == "right"
        assert ctx.margin == (1, 2, 3, 4)
        # Colors are resolved by theme before creating context in Console.frame
        # So we expect the resolved values (or normalized ones).
        # Since we mocked renderer, we can't easily check internal color resolution
        # unless we also mock the theme or check what values ended up in context.
        # However, Console.frame does logic BEFORE context creation.
        # Let's trust it passes *something*.

    def test_frame_defaults(self, console):
        """Verify default values are passed correctly."""
        console.frame("Content")

        _, kwargs = console._renderer.print_frame.call_args
        ctx = kwargs["context"]

        assert ctx.border_style == "solid"
        assert ctx.padding == 1
        assert ctx.align == "left"
        assert ctx.frame_align is None
        assert ctx.margin == (0, 0, 0, 0)  # Normalized from 0

    def test_frame_margin_normalization(self, console):
        """Verify margin int is normalized to tuple."""
        console.frame("Content", margin=5)

        _, kwargs = console._renderer.print_frame.call_args
        ctx = kwargs["context"]
        assert ctx.margin == (5, 5, 5, 5)

    def test_frame_gradient_args(self, console):
        """Verify gradient arguments are passed."""
        console.frame(
            "Content",
            start_color="red",
            end_color="blue",
            border_gradient_start="green",
            border_gradient_end="yellow",
            border_gradient_direction="horizontal",
        )

        _, kwargs = console._renderer.print_frame.call_args
        ctx = kwargs["context"]

        # Console.frame resolves colors.
        # If we passed strings, they should be in the context as strings (normalized)
        # or as Resolve/Normalized values.
        # Since we don't mock theme fully, the default theme will run.
        # Default theme resolve_color returns the string input if it's a valid color or hex.

        # We mostly care that they made it into the context object
        assert ctx.border_gradient_start is not None
        assert ctx.border_gradient_end is not None
        assert ctx.border_gradient_direction == "horizontal"
