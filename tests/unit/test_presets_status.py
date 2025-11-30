from unittest.mock import Mock, patch

import pytest

from styledconsole.console import Console
from styledconsole.presets.status import status_frame


@pytest.fixture
def mock_console():
    return Mock(spec=Console)


def test_status_frame_pass(mock_console):
    status_frame("Test Case 1", "PASS", console=mock_console)

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    assert kwargs["title"] == " PASS "
    assert kwargs["border_color"] == "green"
    assert kwargs["title_color"] == "green"
    assert "✅  [bold]Test Case 1[/]" in kwargs["content"][0]


def test_status_frame_fail(mock_console):
    status_frame("Test Case 2", "FAIL", message="AssertionError: 1 != 2", console=mock_console)

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    assert kwargs["title"] == " FAIL "
    assert kwargs["border_color"] == "red"
    assert kwargs["title_color"] == "red"
    assert "❌  [bold]Test Case 2[/]" in kwargs["content"][0]
    assert "AssertionError: 1 != 2" in kwargs["content"]


def test_status_frame_skip(mock_console):
    status_frame("Test Case 3", "SKIP", console=mock_console)

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    assert kwargs["title"] == " SKIP "
    assert kwargs["border_color"] == "yellow"
    assert kwargs["title_color"] == "yellow"
    # Uses ⚠️ (VS16 emoji) - auto-spacing adjustment handles terminal rendering
    assert "⚠️  [bold]Test Case 3[/]" in kwargs["content"][0]


def test_status_frame_error(mock_console):
    status_frame("Test Case 4", "ERROR", console=mock_console)

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    assert kwargs["title"] == " ERROR "
    assert kwargs["border_color"] == "crimson"
    assert kwargs["title_color"] == "crimson"
    assert "💥  [bold]Test Case 4[/]" in kwargs["content"][0]


def test_status_frame_with_duration(mock_console):
    status_frame("Test Case 5", "PASS", duration=1.234, console=mock_console)

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    # Check if duration is present in the content
    # It might be in the second line if duration is the only detail
    content_str = "".join(kwargs["content"])
    assert "Duration: 1.23s" in content_str


@patch("styledconsole.presets.status.Console")
def test_status_frame_default_console(mock_console_cls):
    # Mock Console constructor to verify it's called when no console is provided
    mock_instance = mock_console_cls.return_value

    status_frame("Test Default", "PASS")

    mock_console_cls.assert_called_once()
    mock_instance.frame.assert_called_once()


def test_status_frame_markup_escaping(mock_console):
    """Test that markup in inputs is escaped."""
    status_frame("[red]Malicious[/red]", "PASS", message="[bold]Break[/bold]", console=mock_console)

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    # The content should contain the escaped version, not the raw tags
    # rich.markup.escape replaces [ with \[
    content_lines = kwargs["content"]
    assert any("\\[red]Malicious\\[/red]" in line for line in content_lines)
    assert any("\\[bold]Break\\[/bold]" in line for line in content_lines)


def test_status_frame_kwargs_override(mock_console):
    """Test that kwargs can override defaults."""
    status_frame(
        "Test Override", "PASS", console=mock_console, border="double", padding=2, width=100
    )

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    assert kwargs["border"] == "double"
    assert kwargs["padding"] == 2
    assert kwargs["width"] == 100
    # Defaults that weren't overridden should remain
    assert kwargs["border_color"] == "green"
