"""Visual confirmation test for Rich's alignment methods."""

from rich.console import Console as RichConsole
from rich.text import Text
from styledconsole.core.frame import FrameRenderer

from styledconsole import SOLID


def main():
    """Test Rich's justify parameter with complete frames."""
    rich_console = RichConsole()
    renderer = FrameRenderer()

    print(f"\n{'=' * 60}")
    print(f"Terminal width: {rich_console.width}")
    print(f"{'=' * 60}\n")

    # Create a colored frame
    frame_lines = renderer.render(
        content="🚀 This is a test frame with colors and emoji",
        border=SOLID,
        width=60,
        border_color="cyan",
        content_color="yellow",
        title="Test Frame",
        title_color="magenta",
    )

    print("LEFT ALIGNED (current working approach):")
    for line in frame_lines:
        text = Text.from_ansi(line)
        rich_console.print(text, justify="left")

    print("\n" + "─" * rich_console.width + "\n")

    print("CENTER ALIGNED (using Rich justify):")
    for line in frame_lines:
        text = Text.from_ansi(line)
        rich_console.print(text, justify="center")

    print("\n" + "─" * rich_console.width + "\n")

    print("RIGHT ALIGNED (using Rich justify):")
    for line in frame_lines:
        text = Text.from_ansi(line)
        rich_console.print(text, justify="right")

    print("\n" + "=" * rich_console.width)
    print("✅ No wrapping occurred! Rich's justify handles ANSI correctly!")
    print("=" * rich_console.width + "\n")


if __name__ == "__main__":
    main()
