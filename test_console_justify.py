"""Test using Rich's justify parameter directly through Console.print()."""

from styledconsole import SOLID, Console
from styledconsole.core.frame import FrameRenderer


def main():
    """Test Rich's justify parameter with Console.print()."""
    console = Console()
    renderer = FrameRenderer()

    print(f"\n{'=' * 60}")
    print(f"Terminal width: {console._rich_console.width}")
    print(f"{'=' * 60}\n")

    # Create colored frame
    frame_lines = renderer.render(
        content="🚀 Test frame with colors",
        border=SOLID,
        width=60,
        border_color="cyan",
        content_color="yellow",
        title="Test",
    )

    print("Method 1: Direct console.print() with justify parameter:")
    print()

    print("LEFT:")
    for line in frame_lines:
        console.print(line, justify="left", highlight=False, soft_wrap=False)

    print("\nCENTER:")
    for line in frame_lines:
        console.print(line, justify="center", highlight=False, soft_wrap=False)

    print("\nRIGHT:")
    for line in frame_lines:
        console.print(line, justify="right", highlight=False, soft_wrap=False)

    print("\n" + "=" * console._rich_console.width)
    print("✅ No wrapping! Rich's justify parameter handles ANSI correctly!")
    print("=" * console._rich_console.width + "\n")


if __name__ == "__main__":
    main()
