"""Tests for the RenderPolicy system."""

from __future__ import annotations

import os
from collections.abc import Iterator
from unittest.mock import patch

import pytest

from styledconsole.policy import (
    RenderPolicy,
    get_default_policy,
    reset_default_policy,
    set_default_policy,
)


class TestRenderPolicyCreation:
    """Tests for RenderPolicy instantiation."""

    def test_default_values(self) -> None:
        """Default policy has everything enabled."""
        policy = RenderPolicy()
        assert policy.unicode is True
        assert policy.color is True
        assert policy.emoji is True
        assert policy.force_ascii_icons is False

    def test_all_disabled(self) -> None:
        """Can create policy with all features disabled."""
        policy = RenderPolicy(unicode=False, color=False, emoji=False)
        assert policy.unicode is False
        assert policy.color is False
        assert policy.emoji is False

    def test_emoji_implies_unicode(self) -> None:
        """Enabling emoji automatically enables unicode."""
        policy = RenderPolicy(unicode=False, emoji=True)
        assert policy.unicode is True
        assert policy.emoji is True

    def test_is_frozen(self) -> None:
        """Policy is immutable (frozen dataclass)."""
        policy = RenderPolicy()
        with pytest.raises(AttributeError):
            policy.color = False  # type: ignore[misc]


class TestRenderPolicyFactories:
    """Tests for factory methods."""

    def test_full_policy(self) -> None:
        """full() creates policy with all features enabled."""
        policy = RenderPolicy.full()
        assert policy.unicode is True
        assert policy.color is True
        assert policy.emoji is True
        assert policy.force_ascii_icons is False

    def test_minimal_policy(self) -> None:
        """minimal() creates ASCII-only policy."""
        policy = RenderPolicy.minimal()
        assert policy.unicode is False
        assert policy.color is False
        assert policy.emoji is False
        assert policy.force_ascii_icons is True

    def test_ci_friendly_policy(self) -> None:
        """ci_friendly() creates policy suitable for CI."""
        policy = RenderPolicy.ci_friendly()
        assert policy.unicode is True
        assert policy.color is True
        assert policy.emoji is False
        assert policy.force_ascii_icons is True

    def test_no_color_policy(self) -> None:
        """no_color() creates policy without color."""
        policy = RenderPolicy.no_color()
        assert policy.unicode is True
        assert policy.color is False
        assert policy.emoji is True
        assert policy.force_ascii_icons is False


class TestRenderPolicyFromEnv:
    """Tests for from_env() environment detection."""

    @pytest.fixture(autouse=True)
    def clean_env(self) -> Iterator[None]:
        """Ensure clean environment for each test and restore after."""
        env_vars = [
            "NO_COLOR",
            "FORCE_COLOR",
            "TERM",
            "CI",
            "GITHUB_ACTIONS",
            "GITLAB_CI",
            "JENKINS_URL",
            "TRAVIS",
        ]
        # Save original values
        original = {var: os.environ.get(var) for var in env_vars}

        # Clear env vars for test
        for var in env_vars:
            if var in os.environ:
                del os.environ[var]

        yield  # Run the test

        # Restore original values
        for var, value in original.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

    def test_default_tty(self) -> None:
        """With TTY and no env vars, everything is enabled."""
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.unicode is True
            assert policy.color is True
            assert policy.emoji is True

    def test_no_tty_disables_color(self) -> None:
        """Without TTY, color is disabled."""
        with patch("sys.stdout.isatty", return_value=False):
            policy = RenderPolicy.from_env()
            assert policy.color is False

    def test_no_color_env(self) -> None:
        """NO_COLOR environment variable disables color."""
        os.environ["NO_COLOR"] = "1"
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.color is False
            assert policy.unicode is True  # unicode still enabled
            assert policy.emoji is True  # emoji still enabled

    def test_no_color_any_value(self) -> None:
        """NO_COLOR with any value disables color."""
        os.environ["NO_COLOR"] = ""  # Empty string still counts
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.color is False

    def test_force_color_overrides(self) -> None:
        """FORCE_COLOR=1 overrides NO_COLOR and TTY detection."""
        os.environ["NO_COLOR"] = "1"
        os.environ["FORCE_COLOR"] = "1"
        with patch("sys.stdout.isatty", return_value=False):
            policy = RenderPolicy.from_env()
            assert policy.color is True

    def test_force_color_true_value(self) -> None:
        """FORCE_COLOR accepts 'true' and 'yes'."""
        for value in ["1", "true", "yes", "TRUE", "YES"]:
            os.environ["FORCE_COLOR"] = value
            with patch("sys.stdout.isatty", return_value=False):
                policy = RenderPolicy.from_env()
                assert policy.color is True, f"Failed for FORCE_COLOR={value}"

    def test_term_dumb(self) -> None:
        """TERM=dumb disables unicode, color, and emoji."""
        os.environ["TERM"] = "dumb"
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.unicode is False
            assert policy.color is False
            assert policy.emoji is False
            assert policy.force_ascii_icons is True

    def test_ci_env(self) -> None:
        """CI=true disables emoji but keeps color."""
        os.environ["CI"] = "true"
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.unicode is True
            assert policy.color is True
            assert policy.emoji is False
            assert policy.force_ascii_icons is True

    def test_github_actions(self) -> None:
        """GITHUB_ACTIONS triggers CI mode."""
        os.environ["GITHUB_ACTIONS"] = "true"
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.emoji is False
            assert policy.force_ascii_icons is True

    def test_gitlab_ci(self) -> None:
        """GITLAB_CI triggers CI mode."""
        os.environ["GITLAB_CI"] = "true"
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.emoji is False

    def test_jenkins(self) -> None:
        """JENKINS_URL triggers CI mode."""
        os.environ["JENKINS_URL"] = "http://jenkins.example.com"
        with patch("sys.stdout.isatty", return_value=True):
            policy = RenderPolicy.from_env()
            assert policy.emoji is False


class TestRenderPolicyWithOverride:
    """Tests for with_override() method."""

    def test_override_single_field(self) -> None:
        """Can override a single field."""
        policy = RenderPolicy.full()
        new_policy = policy.with_override(emoji=False)
        assert new_policy.emoji is False
        assert new_policy.color is True
        assert new_policy.unicode is True

    def test_override_multiple_fields(self) -> None:
        """Can override multiple fields."""
        policy = RenderPolicy.full()
        new_policy = policy.with_override(color=False, emoji=False)
        assert new_policy.color is False
        assert new_policy.emoji is False
        assert new_policy.unicode is True

    def test_override_preserves_original(self) -> None:
        """with_override returns new instance, doesn't modify original."""
        policy = RenderPolicy.full()
        _ = policy.with_override(color=False)
        assert policy.color is True  # Original unchanged

    def test_override_none_keeps_value(self) -> None:
        """None values keep original value."""
        policy = RenderPolicy(unicode=True, color=False, emoji=True)
        new_policy = policy.with_override(unicode=None, color=True)
        assert new_policy.unicode is True
        assert new_policy.color is True
        assert new_policy.emoji is True


class TestRenderPolicyProperties:
    """Tests for computed properties."""

    def test_border_style_fallback_unicode(self) -> None:
        """border_style_fallback returns 'unicode' when enabled."""
        policy = RenderPolicy(unicode=True)
        assert policy.border_style_fallback == "unicode"

    def test_border_style_fallback_ascii(self) -> None:
        """border_style_fallback returns 'ascii' when unicode disabled."""
        policy = RenderPolicy(unicode=False, emoji=False)
        assert policy.border_style_fallback == "ascii"

    def test_icon_mode_emoji(self) -> None:
        """icon_mode returns 'emoji' when emoji enabled."""
        policy = RenderPolicy(emoji=True, force_ascii_icons=False)
        assert policy.icon_mode == "emoji"

    def test_icon_mode_ascii_forced(self) -> None:
        """icon_mode returns 'ascii' when force_ascii_icons is True."""
        policy = RenderPolicy(emoji=True, force_ascii_icons=True)
        assert policy.icon_mode == "ascii"

    def test_icon_mode_ascii_no_emoji(self) -> None:
        """icon_mode returns 'ascii' when emoji disabled."""
        policy = RenderPolicy(emoji=False)
        assert policy.icon_mode == "ascii"


class TestRenderPolicyRepr:
    """Tests for string representation."""

    def test_repr(self) -> None:
        """__repr__ shows all fields."""
        policy = RenderPolicy(unicode=True, color=False, emoji=True)
        repr_str = repr(policy)
        assert "unicode=True" in repr_str
        assert "color=False" in repr_str
        assert "emoji=True" in repr_str


class TestDefaultPolicyFunctions:
    """Tests for module-level policy functions."""

    def setup_method(self) -> None:
        """Reset default policy before each test."""
        reset_default_policy()

    def teardown_method(self) -> None:
        """Clean up after each test."""
        reset_default_policy()

    def test_get_default_policy_auto_detects(self) -> None:
        """get_default_policy auto-detects on first call."""
        with patch("sys.stdout.isatty", return_value=True):
            policy = get_default_policy()
            assert isinstance(policy, RenderPolicy)

    def test_get_default_policy_cached(self) -> None:
        """get_default_policy returns same instance on subsequent calls."""
        with patch("sys.stdout.isatty", return_value=True):
            policy1 = get_default_policy()
            policy2 = get_default_policy()
            assert policy1 is policy2

    def test_set_default_policy(self) -> None:
        """set_default_policy sets the default."""
        custom = RenderPolicy.minimal()
        set_default_policy(custom)
        assert get_default_policy() is custom

    def test_reset_default_policy(self) -> None:
        """reset_default_policy clears cached policy."""
        custom = RenderPolicy.minimal()
        set_default_policy(custom)
        reset_default_policy()
        with patch("sys.stdout.isatty", return_value=True):
            new_policy = get_default_policy()
            assert new_policy is not custom


class TestRenderPolicyIntegration:
    """Integration tests for policy with icons."""

    def test_apply_to_icons(self) -> None:
        """apply_to_icons sets the global icon mode."""
        from styledconsole.icons import get_icon_mode, reset_icon_mode

        try:
            policy = RenderPolicy(emoji=False, force_ascii_icons=True)
            policy.apply_to_icons()
            assert get_icon_mode() == "ascii"
        finally:
            reset_icon_mode()

    def test_policy_emoji_mode_applies(self) -> None:
        """Policy with emoji applies emoji mode."""
        from styledconsole.icons import get_icon_mode, reset_icon_mode

        try:
            policy = RenderPolicy(emoji=True, force_ascii_icons=False)
            policy.apply_to_icons()
            assert get_icon_mode() == "emoji"
        finally:
            reset_icon_mode()
