"""Test proper Rich integration - treating frame as a unit."""

from rich.console import Console as RichConsole
from rich.console import Group
from rich.text import Text
from styledconsole.core.frame import FrameRenderer

from styledconsole import SOLID


def test_group_approach():
    """Use Rich's Group to keep frame lines together."""
    print("\n=== Rich Group Approach ===\n")

    rich_console = RichConsole()
    renderer = FrameRenderer()

    frame_lines = renderer.render(
        content="🚀 Test content with colors",
        border=SOLID,
        width=60,
        border_color="cyan",
        content_color="yellow",
        title="Test Frame",
    )

    # Convert each line to Rich Text
    text_objects = [Text.from_ansi(line) for line in frame_lines]

    # Create a Group (keeps lines together)
    frame_group = Group(*text_objects)

    print("LEFT:")
    rich_console.print(frame_group, justify="left")

    print("\nCENTER:")
    rich_console.print(frame_group, justify="center")

    print("\nRIGHT:")
    rich_console.print(frame_group, justify="right")

    print("\n" + "=" * rich_console.width)


def test_text_align_approach():
    """Use Text.align() method."""
    print("\n\n=== Rich Text.align() Approach ===\n")

    rich_console = RichConsole()
    renderer = FrameRenderer()

    frame_lines = renderer.render(
        content="🚀 Test content with colors",
        border=SOLID,
        width=60,
        border_color="cyan",
        content_color="yellow",
        title="Test Frame",
    )

    terminal_width = rich_console.width

    print("CENTER with Text.align():")
    for line in frame_lines:
        text = Text.from_ansi(line)
        # Align the text object itself to terminal width
        text.align("center", width=terminal_width)
        rich_console.print(text)

    print("\n" + "=" * rich_console.width)


if __name__ == "__main__":
    test_group_approach()
    test_text_align_approach()
