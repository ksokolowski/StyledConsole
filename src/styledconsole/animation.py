"""Animation utilities for StyledConsole.

Provides capabilities to render animated frames in the terminal.
Supports policy-aware rendering with fallback for limited terminals.
"""

from __future__ import annotations

import sys
import time
from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from styledconsole.policy import RenderPolicy


def _supports_cursor_control(policy: RenderPolicy | None = None) -> bool:
    """Check if terminal supports cursor control for animations.

    Args:
        policy: Optional RenderPolicy to check. If None, auto-detects.

    Returns:
        True if cursor control (ANSI escape codes) is supported.
    """
    # Not a TTY = no cursor control
    if not sys.stdout.isatty():
        return False

    # If policy provided, check unicode support (implies ANSI support)
    if policy is not None:
        return policy.unicode

    # Auto-detect from environment
    import os

    # TERM=dumb means no cursor control
    if os.environ.get("TERM", "") == "dumb":
        return False

    # NO_COLOR doesn't disable cursor control, but let's be safe
    # and check for explicit terminal capability indicators
    return True


class Animation:
    """Handles rendering of animated frames.

    Supports two rendering modes:
    - **Animated mode**: Uses ANSI cursor control to redraw frames in place.
      Requires a TTY with ANSI support.
    - **Fallback mode**: Prints each frame on new lines with separators.
      Used when terminal doesn't support cursor control.

    The mode is automatically selected based on terminal capabilities
    and the provided RenderPolicy.

    Example:
        >>> from styledconsole.animation import Animation
        >>> def spinner():
        ...     chars = ['|', '/', '-', '\\\\']
        ...     for i in range(20):
        ...         yield f"{chars[i % 4]} Loading...\\n"
        >>> Animation.run(spinner(), fps=10, duration=2)
    """

    @staticmethod
    def run(
        frames: Iterator[str],
        fps: int = 10,
        duration: float | None = None,
        *,
        policy: RenderPolicy | None = None,
        fallback_separator: str | None = None,
    ) -> None:
        """Run an animation loop.

        Automatically detects terminal capabilities and uses cursor control
        when available, or falls back to simple line-by-line output.

        Args:
            frames: Iterator yielding frame strings. Each frame should end
                with a newline for proper rendering.
            fps: Frames per second. Defaults to 10.
            duration: Optional duration in seconds. If None, runs until
                the iterator is exhausted or interrupted with Ctrl+C.
            policy: Optional RenderPolicy to determine animation mode.
                If None, auto-detects from environment.
            fallback_separator: Separator between frames in fallback mode.
                If None, uses "---" for multi-line frames or no separator
                for single-line frames. Set to "" to disable separators.

        Example:
            >>> # With explicit policy
            >>> from styledconsole import RenderPolicy
            >>> Animation.run(frames, policy=RenderPolicy.minimal())

            >>> # Auto-detect (default)
            >>> Animation.run(frames, fps=5, duration=10)
        """
        use_cursor_control = _supports_cursor_control(policy)

        if use_cursor_control:
            Animation._run_animated(frames, fps, duration)
        else:
            Animation._run_fallback(frames, fps, duration, fallback_separator)

    @staticmethod
    def _run_animated(
        frames: Iterator[str],
        fps: int,
        duration: float | None,
    ) -> None:
        """Run animation with cursor control (ANSI escape codes)."""
        delay = 1.0 / fps
        first_frame = True
        lines_to_clear = 0
        start_time = time.time()

        try:
            # Hide cursor
            sys.stdout.write("\033[?25l")

            for frame in frames:
                if duration and (time.time() - start_time > duration):
                    break

                if not first_frame:
                    # Move cursor up to overwrite previous frame
                    if lines_to_clear > 0:
                        sys.stdout.write(f"\033[{lines_to_clear}A")
                    sys.stdout.write("\r")

                sys.stdout.write(frame)
                sys.stdout.flush()

                # Calculate lines for next clear
                lines_to_clear = frame.count("\n")
                first_frame = False

                time.sleep(delay)

        except KeyboardInterrupt:
            # Graceful exit on Ctrl+C
            pass
        finally:
            # Show cursor again and move down past the last frame
            sys.stdout.write("\033[?25h")
            sys.stdout.write("\n")

    @staticmethod
    def _run_fallback(
        frames: Iterator[str],
        fps: int,
        duration: float | None,
        separator: str | None,
    ) -> None:
        """Run animation in fallback mode (no cursor control).

        Prints each frame on new lines. For single-line frames, uses
        carriage return to update in place if possible.
        """
        delay = 1.0 / fps
        start_time = time.time()
        first_frame = True
        is_single_line = None

        try:
            for frame in frames:
                if duration and (time.time() - start_time > duration):
                    break

                # Detect if frames are single-line or multi-line
                if is_single_line is None:
                    # Count newlines (excluding trailing)
                    stripped = frame.rstrip("\n")
                    is_single_line = "\n" not in stripped

                if is_single_line:
                    # Single-line: use carriage return (works on most terminals)
                    sys.stdout.write("\r" + frame.rstrip("\n"))
                    sys.stdout.flush()
                else:
                    # Multi-line: print with separator
                    if not first_frame and separator != "":
                        sep = separator if separator is not None else "---"
                        sys.stdout.write(sep + "\n")
                    sys.stdout.write(frame)
                    sys.stdout.flush()

                first_frame = False
                time.sleep(delay)

        except KeyboardInterrupt:
            pass
        finally:
            # Ensure we end on a new line
            sys.stdout.write("\n")
            sys.stdout.flush()
