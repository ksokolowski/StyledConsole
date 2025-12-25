#!/usr/bin/env python3
"""Demo of animated gradients using the new Unified Gradient Engine."""

from io import StringIO

from styledconsole import Console, StyleContext
from styledconsole.animation import Animation
from styledconsole.core.styles import get_border_style
from styledconsole.effects.engine import apply_gradient
from styledconsole.effects.strategies import (
    Both,
    DiagonalPosition,
    OffsetPositionStrategy,
    RainbowSpectrum,
)


def create_animated_frame_generator():
    """Yields frames with cycling gradient offsets."""

    # Pre-render the base content (no colors)
    buffer = StringIO()
    temp_console = Console(file=buffer, detect_terminal=False)

    content = [
        "✨ Animated Gradients ✨",
        "",
        "Using Unified Gradient Engine",
        "with OffsetPositionStrategy",
        "",
        "Press Ctrl+C to stop",
    ]

    style = StyleContext(
        border_style="double",
        width=40,
        align="center",
        padding=1,
    )
    temp_console.frame(content, title="🚀 Animation Demo", style=style)
    base_lines = buffer.getvalue().splitlines()

    # Setup strategies
    # We'll use a diagonal rainbow that shifts
    base_pos_strategy = DiagonalPosition()
    color_source = RainbowSpectrum()
    target_filter = Both()

    # Get border chars for detection
    style = get_border_style("double")
    border_chars = {
        style.top_left,
        style.top_right,
        style.bottom_left,
        style.bottom_right,
        style.horizontal,
        style.vertical,
        style.left_joint,
        style.right_joint,
        style.top_joint,
        style.bottom_joint,
        style.cross,
    }

    offset = 0.0

    while True:
        # Create strategy with current offset
        pos_strategy = OffsetPositionStrategy(base_pos_strategy, offset=offset)

        # Apply gradient
        colored_lines = apply_gradient(
            base_lines, pos_strategy, color_source, target_filter, border_chars
        )

        yield "\n".join(colored_lines)

        # Increment offset
        offset += 0.02  # Speed of animation


def main():
    print("Starting animation... (Runs for 10s or Ctrl+C to stop)")
    try:
        frames = create_animated_frame_generator()
        Animation.run(frames, fps=20, duration=10)
    except KeyboardInterrupt:
        print("\nAnimation stopped.")


if __name__ == "__main__":
    main()
