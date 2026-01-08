"""Tests for StyledColumns functionality and policy adherence."""

from rich.console import Console

from styledconsole.columns import StyledColumns
from styledconsole.policy import RenderPolicy


def test_columns_policy_assignment():
    """Test that StyledColumns correctly assigns policy."""
    policy = RenderPolicy(emoji=False)
    columns = StyledColumns(policy=policy)
    assert columns._policy == policy


def test_columns_sanitize_on_init():
    """Test that StyledColumns sanitizes emojis in constructor."""
    policy = RenderPolicy(emoji=False)
    # Using ⚠️ which has a mapping in ICON_REGISTRY
    items = ["⚠️ Warning", "Nominal"]
    columns = StyledColumns(items, policy=policy)

    # Check internal renderables
    # Rich Columns stores them in self.renderables
    assert "⚠️" not in columns.renderables[0]
    assert "[WARN]" in columns.renderables[0] or "Warning" in columns.renderables[0]


def test_columns_sanitize_on_add_renderable():
    """Test that StyledColumns sanitizes emojis when adding items."""
    policy = RenderPolicy(emoji=False)
    columns = StyledColumns(policy=policy)
    columns.add_renderable("🚀 Speed")

    assert "🚀" not in columns.renderables[0]
    assert ">>>" in columns.renderables[0] or "Speed" in columns.renderables[0]


def test_columns_keep_emoji_when_allowed():
    """Test that StyledColumns preserves emojis when policy allows them."""
    policy = RenderPolicy(emoji=True)
    items = ["🚀 High Speed", "✅ Success"]
    columns = StyledColumns(items, policy=policy)

    assert "🚀" in columns.renderables[0]
    assert "✅" in columns.renderables[1]


def test_console_columns_facade():
    """Test that Console.columns() works without error."""
    from styledconsole import Console as StyledConsole

    console = StyledConsole()
    items = ["A", "B", "C"]

    # Just verify it doesn't crash and prints something
    with console._rich_console.capture() as capture:
        console.columns(items)
    output = capture.get()

    assert "A" in output
    assert "B" in output
    assert "C" in output


def test_columns_rendering_output():
    """Test basic rendering output of StyledColumns."""
    console = Console(width=20)
    items = ["Item 1", "Item 2", "Item 3"]
    columns = StyledColumns(items, padding=0)

    with console.capture() as capture:
        console.print(columns)
    output = capture.get()

    for item in items:
        assert item in output


def test_columns_vs16_alignment_context():
    """Verifies that _patched_cell_len is used during rendering.

    Since we can't easily spy on the context manager in a clean way,
    we test that the code runs without error and correctly handles
    VS16 emojis in the output.
    """
    console = Console()
    # ⚙️ is a VS16 emoji (width 2 in modern terminals)
    items = ["⚙️ Settings", "Info"]
    columns = StyledColumns(items, policy=RenderPolicy(emoji=True))

    with console.capture() as capture:
        console.print(columns)
    output = capture.get()

    assert "⚙️" in output
    assert "Settings" in output
    assert "Info" in output
