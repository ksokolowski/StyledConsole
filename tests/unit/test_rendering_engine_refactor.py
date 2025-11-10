"""Regression test for refactored RenderingEngine.print_frame helpers.

Ensures frame rendering still succeeds with gradients, colors, title after
refactor extracting _normalize_colors and _build_content_renderable.
"""

from styledconsole.console import Console


def test_frame_gradient_renders_without_error():
    console = Console(record=True)
    console.frame(
        ["Line A", "Line B", "Line C"],
        title="Refactor Test 🚀",
        border="rounded",
        start_color="red",
        end_color="blue",
        content_color=None,
    )
    exported = console.export_text()
    # Basic regression assertions: all lines appear in plain text export
    assert "Line A" in exported
    assert "Line B" in exported
    assert "Line C" in exported
