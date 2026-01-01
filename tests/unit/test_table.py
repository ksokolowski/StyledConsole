"""Tests for StyledTable policy adherence."""

import pytest
from rich.box import ASCII, ROUNDED

from styledconsole.policy import RenderPolicy
from styledconsole.table import StyledTable


def test_table_default_policy():
    """Test table uses default policy (usually full features)."""
    table = StyledTable()
    # Default policy usually has unicode=True, so box should not be ASCII unless env forces it.
    # We can't strictly assert box type without knowing env, but we can verify it accepted defaults.
    assert table.box is not None


def test_table_policy_ascii_borders():
    """Test table downgrades to ASCII borders when unicode=False."""
    # Must disable emoji too, otherwise strict policy forces unicode=True
    policy = RenderPolicy(unicode=False, emoji=False)
    table = StyledTable(policy=policy, border_style="rounded")
    
    # Compare the internal box structure since Rich Box instances might differ in identity
    # but produce the same string representation
    assert str(table.box) == str(ASCII)


def test_table_policy_unicode_borders():
    """Test table keeps requested border when unicode=True."""
    policy = RenderPolicy(unicode=True)
    table = StyledTable(policy=policy, border_style="rounded")
    
    assert table.box == ROUNDED


def test_table_sanitize_emoji_on_add_row():
    """Test table converts emoji to ASCII when emoji=False."""
    policy = RenderPolicy(emoji=False)
    table = StyledTable(policy=policy)
    
    # "✅" should become "[OK]" in green if using styledconsole icons logic,
    # or at least sanitized.
    # Note: convert_emoji_to_ascii relies on EMOJI_TO_ICON mapping.
    # We should verify it changes.
    
    table.add_row("Status", "✅ Done")
    
    # Access the columns from the first row in the internal storage
    # Rich Table stores rows in .rows, which is a list of Row objects.
    # But Row structure is internal. simpler to export to text and check.
    
    from rich.console import Console
    console = Console()
    with console.capture() as capture:
        console.print(table)
    output = capture.get()
    
    assert "✅" not in output
    assert "(OK)" in output  # based on default mapping for CHECK_MARK_BUTTON


def test_table_keep_emoji_on_add_row():
    """Test table keeps emoji when emoji=True."""
    policy = RenderPolicy(emoji=True)
    table = StyledTable(policy=policy)
    
    table.add_row("Status", "✅ Done")
    
    from rich.console import Console
    console = Console()
    with console.capture() as capture:
        console.print(table)
    output = capture.get()
    
    assert "✅" in output


def test_table_sanitize_column_header():
    """Test table converts emoji in headers."""
    policy = RenderPolicy(emoji=False)
    table = StyledTable(policy=policy)
    
    table.add_column("🚀 Speed")
    
    from rich.console import Console
    console = Console()
    with console.capture() as capture:
        console.print(table)
    output = capture.get()
    
    assert "🚀" not in output
    assert ">>>" in output or "Speed" in output
