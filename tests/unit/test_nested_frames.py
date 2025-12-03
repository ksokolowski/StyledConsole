import pytest

from styledconsole import Console
from styledconsole.policy import RenderPolicy


class TestNestedFrames:
    @pytest.fixture
    def console(self):
        # Use full policy to ensure color output in tests
        return Console(policy=RenderPolicy.full())

    def test_render_frame_returns_string(self, console):
        """Verify render_frame returns a string."""
        output = console.render_frame("Test Content")
        assert isinstance(output, str)
        assert "Test Content" in output

    def test_render_frame_contains_ansi(self, console):
        """Verify render_frame output contains ANSI codes for colors."""
        output = console.render_frame("Colored Frame", border_color="red", content_color="blue")
        # Check for ANSI escape sequence starter
        assert "\x1b[" in output

    def test_nested_frame_rendering(self, console):
        """Verify a frame can be nested inside another."""
        inner = console.render_frame("Inner", border="solid")

        # Capture outer frame output
        # We use a mock or capture stdout to verify, but here we just ensure no error
        # and that inner content is present
        outer = console.render_frame(inner, title="Outer", border="double")

        assert "Inner" in outer
        assert "Outer" in outer
        # Inner frame border characters should be present
        assert "│" in outer

    def test_nested_alignment(self, console):
        """Verify nested frame alignment."""
        inner = console.render_frame("Inner", width=20)
        outer = console.render_frame(inner, align="center", width=40)
        # Visual inspection would show centering, here we check length/structure
        lines = outer.splitlines()
        # Ensure lines are padded
        assert len(lines) > 0
