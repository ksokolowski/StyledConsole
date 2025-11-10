"""Test that Console.text with dim=True uses Rich directly and still prints."""

from styledconsole.console import Console


def test_console_text_dim_prints():
    console = Console(record=True)
    console.text("dim text", dim=True)
    out = console.export_text()
    assert "dim text" in out
