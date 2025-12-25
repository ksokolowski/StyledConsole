"""Unit tests for group margins and frame alignment."""

from unittest.mock import MagicMock

import pytest

from styledconsole.console import Console


class TestGroupMargins:
    """Tests for margin and frame_align in Console.group and frame_group."""

    @pytest.fixture
    def console(self):
        """Create a Console instance with mocked renderer."""
        console = Console(detect_terminal=False)
        console._renderer = MagicMock()
        return console

    def test_frame_group_passes_margin(self, console):
        """Verify frame_group method passes margin and frame_align."""
        console.frame_group([{"content": "Item"}], margin=(1, 2, 3, 4), frame_align="center")

        console._renderer.print_frame_group.assert_called_once()
        _, kwargs = console._renderer.print_frame_group.call_args

        assert kwargs["margin"] == (1, 2, 3, 4)
        assert kwargs["frame_align"] == "center"

    def test_group_context_stores_margin(self, console):
        """Verify group context manager stores margin and frame_align."""
        with console.group(margin=5, frame_align="right") as group:
            assert group.margin == 5
            assert group.frame_align == "right"

            # Simulate exit to trigger render
            # We mock _render_group to avoid full rendering logic dependency in this unit test?
            # Or we mock console._renderer.render_frame_group_to_string?
            # FrameGroupContext._render_group uses console._renderer.render_frame_to_string for inner frames
            # and OUTER frame.

            pass

        # After exit, _render_group is called.
        # But _render_group calls console._renderer.render_frame_to_string for the outer frame.
        # Let's verify that call.

        # However, _render_group logic is complex.
        # Let's inspect what calls were made to renderer.

        # FrameGroupContext._render_group calls:
        # 1. render_frame_to_string for each inner item
        # 2. render_frame_to_string for outer frame (if title/border etc present)
        # 3. print_ansi_output (via _output_to_parent_or_print)

        # In this test, we have empty group (no inner frames), so _render_group might do nothing?
        # Let's check _render_group code.
        # "if not self._captured_frames: ... if self.title: ..."
        # Our group has no title, no frames. So it might return early.

    def test_group_context_renders_with_margin(self, console):
        """Verify group rendering passes margin to outer frame via StyleContext."""
        # Mock connection to return a string, otherwise join() fails
        console._renderer.render_frame_to_string.return_value = "RenderedFrame"

        # We need captured frames to force rendering
        with console.group(margin=5, frame_align="right", title="Group"):
            console.frame("Inner")

        # Check calls to render_frame_to_string
        # First call is Inner frame
        # Second call is Outer frame (combining inner)

        assert console._renderer.render_frame_to_string.call_count >= 2

        # Get the call for the outer frame
        # It's likely the last one
        _args, kwargs = console._renderer.render_frame_to_string.call_args

        # Now we pass a StyleContext instead of individual kwargs
        # Verify the context contains the expected values
        ctx = kwargs["context"]
        assert ctx.margin == (5, 5, 5, 5)  # StyleContext normalizes int to tuple
        assert ctx.frame_align == "right"
        assert ctx.title == "Group"
