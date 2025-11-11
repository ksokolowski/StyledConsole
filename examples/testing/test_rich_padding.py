"""Test Rich's Padding API for ANSI alignment bug."""

from rich.console import Console as RichConsole
from rich.padding import Padding
from rich.text import Text

from styledconsole import SOLID, Console
from styledconsole.utils.text import strip_ansi, visual_width


def test_current_approach():
    """Show current broken behavior."""
    print("\n=== CURRENT APPROACH (String-based padding) ===")

    from styledconsole.core.frame import FrameRenderer

    # Create a colored frame directly
    renderer = FrameRenderer()
    frame_lines = renderer.render(
        content="Test Content", border=SOLID, width=60, border_color="cyan", content_color="white"
    )

    console = Console(detect_terminal=True)

    terminal_width = console._rich_console.width
    print(f"Terminal width: {terminal_width}")

    # Try right-align with current approach (string padding)
    for line in frame_lines:
        visual = visual_width(line)
        total_bytes = len(line)
        ansi_overhead = total_bytes - len(strip_ansi(line))

        print(f"Visual: {visual}, Total bytes: {total_bytes}, ANSI overhead: {ansi_overhead}")

        # Current approach: pad with spaces
        padding = terminal_width - visual
        aligned = (" " * padding) + line

        print(f"Aligned string length: {len(aligned)}")
        print(f"Output: {repr(aligned[:80])}...")  # Show first 80 chars
        break  # Just show first line


def test_rich_padding_api():
    """Test Rich's Padding API approach."""
    print("\n\n=== RICH PADDING API APPROACH ===")

    from styledconsole.core.frame import FrameRenderer

    rich_console = RichConsole()
    terminal_width = rich_console.width
    print(f"Terminal width: {terminal_width}")

    # Create a colored frame line
    renderer = FrameRenderer()
    frame_lines = renderer.render(
        content="Test Content", border=SOLID, width=60, border_color="cyan", content_color="white"
    )

    line = frame_lines[0]
    visual = visual_width(line)

    print(f"Frame visual width: {visual}")
    print(f"Frame byte length: {len(line)}")

    # Convert ANSI string to Rich Text object
    text = Text.from_ansi(line)
    print(f"Rich Text object created: {text}")
    print(f"Rich Text cell_len: {text.cell_len}")

    # Calculate padding needed
    padding_needed = terminal_width - visual
    print(f"Padding needed: {padding_needed}")

    # Try Rich's Padding for right-align
    # Padding(renderable, pad=(top, right, bottom, left))
    padded = Padding(text, (0, 0, 0, padding_needed))

    print("\nRendering with Rich Padding:")
    rich_console.print(padded)

    # Check if it wraps
    print("\nDoes it wrap? Let's check with a border:")
    rich_console.print("=" * terminal_width)


def test_rich_text_justify():
    """Test Rich's Text.justify() method."""
    print("\n\n=== RICH TEXT JUSTIFY METHOD ===")

    from styledconsole.core.frame import FrameRenderer

    rich_console = RichConsole()
    terminal_width = rich_console.width
    print(f"Terminal width: {terminal_width}")

    # Create a colored frame line
    renderer = FrameRenderer()
    frame_lines = renderer.render(
        content="Test Content", border=SOLID, width=60, border_color="cyan", content_color="white"
    )

    line = frame_lines[0]
    visual = visual_width(line)

    print(f"Frame visual width: {visual}")

    # Convert to Rich Text and use justify
    text = Text.from_ansi(line)

    # Right-justify (Rich should handle ANSI properly)
    print("\nRight-justified with Rich Text.justify():")
    rich_console.print(text, justify="right")

    print("\nCenter-justified with Rich Text.justify():")
    rich_console.print(text, justify="center")

    print("\nCheck wrapping with border:")
    rich_console.print("=" * terminal_width)


if __name__ == "__main__":
    test_current_approach()
    test_rich_padding_api()
    test_rich_text_justify()
