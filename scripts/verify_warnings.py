"""Verification script for deprecation warnings."""

import warnings

from rich.console import Console

from styledconsole.core.rendering_engine import RenderingEngine


def test_warnings():
    engine = RenderingEngine(Console())

    print("Testing render_frame_to_string legacy usage...")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # Trigger warning by passing legacy arg (border="double") without context
        engine.render_frame_to_string("Test", border="double")

        assert len(w) > 0
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "render_frame_to_string" in str(w[-1].message)
        print("✅ Warning caught for render_frame_to_string")

    print("Testing print_frame legacy usage...")
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # Trigger warning
        engine.print_frame("Test", border="double")

        assert len(w) > 0
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "print_frame" in str(w[-1].message)
        print("✅ Warning caught for print_frame")


if __name__ == "__main__":
    test_warnings()
