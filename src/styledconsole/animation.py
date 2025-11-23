"""Animation utilities for StyledConsole.

Provides capabilities to render animated frames in the terminal.
"""

import sys
import time
from collections.abc import Iterator


class Animation:
    """Handles rendering of animated frames."""

    @staticmethod
    def run(frames: Iterator[str], fps: int = 10, duration: float | None = None):
        """Run an animation loop.

        Args:
            frames: Iterator yielding frame strings.
            fps: Frames per second.
            duration: Optional duration in seconds. If None, runs until interrupted.
        """
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
