"""Unit tests for Console.frame with style argument."""

from unittest.mock import MagicMock

import pytest

from styledconsole.console import Console
from styledconsole.core.context import StyleContext


class TestConsoleStyleArg:
    """Tests for Console.frame style argument precedence."""

    @pytest.fixture
    def console(self):
        """Create a Console instance with mocked renderer."""
        console = Console(detect_terminal=False)
        console._renderer = MagicMock()
        return console

    def test_style_arg_usage(self, console):
        """Verify passing a StyleContext object works."""
        style = StyleContext(border_style="double", padding=2, content_color="red")

        console.frame("Content", style=style)

        console._renderer.print_frame.assert_called_once()
        _, kwargs = console._renderer.print_frame.call_args
        ctx = kwargs["context"]

        assert ctx.border_style == "double"
        assert ctx.padding == 2
        # Colors need resolution check?
        # Console.frame logic resolves colors again.
        # But if style has "red", resolve("red") -> normalized hex.
        # We can't check normalized hex easily without knowing theme map.
        # But we verify it's NOT None.
        assert ctx.content_color is not None

    def test_style_arg_override(self, console):
        """Verify explicit kwargs override style."""
        style = StyleContext(border_style="double", padding=2)

        # Override border, keep padding
        console.frame("Content", style=style, border="heavy")

        _, kwargs = console._renderer.print_frame.call_args
        ctx = kwargs["context"]

        assert ctx.border_style == "heavy"
        assert ctx.padding == 2

    def test_style_arg_defaults(self, console):
        """Verify style fills in missing args."""
        style = StyleContext(align="center")

        console.frame("Content", style=style)

        _, kwargs = console._renderer.print_frame.call_args
        ctx = kwargs["context"]

        assert ctx.align == "center"
        # Implicit frame defaults should apply where style has None?
        # StyleContext default for border_style is "rounded" (or "solid" in context.py? check)
        # In context.py: border_style: str = "rounded".
        # In Console.frame fallback: if style.border_style if style else "solid".
        # If style has border_style="rounded", it uses "rounded".
        assert ctx.border_style == "rounded"
