from unittest.mock import Mock, patch

import pytest

from styledconsole.console import Console
from styledconsole.presets.summary import TestResult
from styledconsole.presets.summary import test_summary as render_test_summary


@pytest.fixture
def mock_console():
    return Mock(spec=Console)


def test_summary_all_pass(mock_console):
    results: list[TestResult] = [
        {"name": "Test 1", "status": "PASS", "duration": 0.1},
        {"name": "Test 2", "status": "PASS", "duration": 0.2},
    ]

    render_test_summary(results, total_duration=0.3, console=mock_console)

    mock_console.frame.assert_called_once()
    args, kwargs = mock_console.frame.call_args

    assert kwargs["title"] == " PASSED "
    assert kwargs["border_color"] == "success"  # Semantic color name
    assert "Total:   [bold]2[/]" in kwargs["content"]
    assert "Passed:  2" in kwargs["content"]  # No longer uses Rich markup
    assert "Duration: 0.30s" in kwargs["content"]


def test_summary_mixed_results(mock_console):
    results: list[TestResult] = [
        {"name": "Test 1", "status": "PASS", "duration": 0.1},
        {"name": "Test 2", "status": "FAIL", "duration": 0.2, "message": "Error details"},
    ]

    render_test_summary(results, total_duration=0.3, console=mock_console)

    # Should call frame twice: once for summary, once for failure details
    assert mock_console.frame.call_count == 2

    # Check summary frame
    summary_call = mock_console.frame.call_args_list[0]
    _, summary_kwargs = summary_call
    assert summary_kwargs["title"] == " FAILED "
    assert summary_kwargs["border_color"] == "error"  # Semantic color name
    assert "Failed:  1" in summary_kwargs["content"]  # No longer uses Rich markup

    # Check failure details frame
    fail_call = mock_console.frame.call_args_list[1]
    _, fail_kwargs = fail_call
    assert fail_kwargs["border_color"] == "error"  # Semantic color name
    assert "❌ [bold]Test 2[/]" in fail_kwargs["content"][0]
    assert "Error details" in fail_kwargs["content"][2]  # No longer uses Rich markup


def test_summary_empty(mock_console):
    render_test_summary([], total_duration=0.0, console=mock_console)

    mock_console.frame.assert_called_once()
    _, kwargs = mock_console.frame.call_args

    assert kwargs["title"] == " NO TESTS "
    assert kwargs["border_color"] == "warning"  # Semantic color name
    assert "Total:   [bold]0[/]" in kwargs["content"]


@patch("styledconsole.presets.summary.Console")
def test_summary_default_console(mock_console_cls):
    mock_instance = mock_console_cls.return_value
    results: list[TestResult] = [{"name": "Test 1", "status": "PASS", "duration": 0.1}]

    render_test_summary(results)

    mock_console_cls.assert_called_once()
    mock_instance.frame.assert_called_once()
