"""Ensure rule with emoji title adjusts spacing without crashing."""

from styledconsole.console import Console


def test_rule_with_emoji_title():
    console = Console(record=True)
    console.rule(title="Config ⚙️")
    text = console.export_text()
    assert "Config" in text
