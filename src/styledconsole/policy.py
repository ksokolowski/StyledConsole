"""Runtime policy system for environment-aware rendering.

This module provides a centralized way to control rendering behavior
based on environment detection or explicit configuration. It respects
standard environment variables like NO_COLOR and handles CI/CD contexts.

Environment Variables Detected:
- NO_COLOR: Disables color output (https://no-color.org/)
- FORCE_COLOR: Forces color output even if not detected
- TERM=dumb: Disables unicode and emoji
- CI: Conservative mode (disables emoji by default)
- GITHUB_ACTIONS, GITLAB_CI, JENKINS_URL: CI detection

Example:
    >>> from styledconsole import Console, RenderPolicy
    >>>
    >>> # Auto-detect from environment
    >>> policy = RenderPolicy.from_env()
    >>> console = Console(policy=policy)
    >>>
    >>> # Manual configuration
    >>> policy = RenderPolicy(unicode=True, color=False, emoji=False)
    >>> console = Console(policy=policy)
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class RenderPolicy:
    """Immutable rendering policy configuration.

    Controls how the Console renders output based on terminal capabilities
    and user preferences. Can be auto-detected from environment or manually
    configured.

    Attributes:
        unicode: Allow Unicode box-drawing characters and symbols.
        color: Allow ANSI color codes in output.
        emoji: Allow emoji characters (implies unicode=True if emoji=True).
        force_ascii_icons: Force Icon Provider to use ASCII mode.

    Example:
        >>> # Minimal ASCII-only output for logs
        >>> policy = RenderPolicy(unicode=False, color=False, emoji=False)
        >>>
        >>> # Full-featured terminal
        >>> policy = RenderPolicy(unicode=True, color=True, emoji=True)
        >>>
        >>> # CI-friendly: colors but no emoji
        >>> policy = RenderPolicy(unicode=True, color=True, emoji=False)
    """

    unicode: bool = True
    color: bool = True
    emoji: bool = True
    force_ascii_icons: bool = False

    def __post_init__(self) -> None:
        """Validate policy constraints."""
        # If emoji is enabled, unicode must also be enabled
        if self.emoji and not self.unicode:
            object.__setattr__(self, "unicode", True)

    @classmethod
    def from_env(cls) -> RenderPolicy:
        """Create a RenderPolicy by detecting environment variables.

        Detection priority (highest to lowest):
        1. FORCE_COLOR=1 → color=True (override)
        2. NO_COLOR (any value) → color=False
        3. TERM=dumb → unicode=False, emoji=False, color=False
        4. CI environments → emoji=False (conservative)
        5. TTY detection → color based on isatty()

        Returns:
            RenderPolicy configured for the current environment.

        Example:
            >>> import os
            >>> os.environ["NO_COLOR"] = "1"
            >>> policy = RenderPolicy.from_env()
            >>> policy.color
            False
        """
        # Start with defaults
        unicode = True
        color = True
        emoji = True
        force_ascii_icons = False

        # Check TERM=dumb (very limited terminal)
        term = os.environ.get("TERM", "").lower()
        if term == "dumb":
            unicode = False
            color = False
            emoji = False
            force_ascii_icons = True

        # Check for CI environments (conservative: disable emoji)
        ci_vars = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "JENKINS_URL", "TRAVIS"]
        is_ci = any(os.environ.get(var) for var in ci_vars)
        if is_ci:
            emoji = False
            force_ascii_icons = True

        # TTY detection for color
        if not sys.stdout.isatty():
            # Not a TTY, probably piped or redirected
            color = False

        # NO_COLOR standard (https://no-color.org/)
        # Any value means disable color
        if "NO_COLOR" in os.environ:
            color = False

        # FORCE_COLOR override (highest priority for color)
        force_color = os.environ.get("FORCE_COLOR", "").lower()
        if force_color in ("1", "true", "yes"):
            color = True

        return cls(
            unicode=unicode,
            color=color,
            emoji=emoji,
            force_ascii_icons=force_ascii_icons,
        )

    @classmethod
    def full(cls) -> RenderPolicy:
        """Create a policy with all features enabled.

        Returns:
            RenderPolicy with unicode, color, and emoji all enabled.
        """
        return cls(unicode=True, color=True, emoji=True, force_ascii_icons=False)

    @classmethod
    def minimal(cls) -> RenderPolicy:
        """Create a minimal ASCII-only policy.

        Useful for log files or very basic terminals.

        Returns:
            RenderPolicy with everything disabled.
        """
        return cls(unicode=False, color=False, emoji=False, force_ascii_icons=True)

    @classmethod
    def ci_friendly(cls) -> RenderPolicy:
        """Create a CI-friendly policy.

        Enables colors and unicode but disables emoji for
        better compatibility with CI log viewers.

        Returns:
            RenderPolicy suitable for CI environments.
        """
        return cls(unicode=True, color=True, emoji=False, force_ascii_icons=True)

    @classmethod
    def no_color(cls) -> RenderPolicy:
        """Create a policy that respects NO_COLOR.

        Enables unicode and emoji but disables color output.

        Returns:
            RenderPolicy with color disabled.
        """
        return cls(unicode=True, color=False, emoji=True, force_ascii_icons=False)

    def with_override(
        self,
        *,
        unicode: bool | None = None,
        color: bool | None = None,
        emoji: bool | None = None,
        force_ascii_icons: bool | None = None,
    ) -> RenderPolicy:
        """Create a new policy with selective overrides.

        Args:
            unicode: Override unicode setting (or None to keep current).
            color: Override color setting (or None to keep current).
            emoji: Override emoji setting (or None to keep current).
            force_ascii_icons: Override icon mode (or None to keep current).

        Returns:
            New RenderPolicy with the specified overrides.

        Example:
            >>> policy = RenderPolicy.from_env()
            >>> no_emoji = policy.with_override(emoji=False)
        """
        return RenderPolicy(
            unicode=unicode if unicode is not None else self.unicode,
            color=color if color is not None else self.color,
            emoji=emoji if emoji is not None else self.emoji,
            force_ascii_icons=(
                force_ascii_icons if force_ascii_icons is not None else self.force_ascii_icons
            ),
        )

    @property
    def border_style_fallback(self) -> Literal["ascii", "unicode"]:
        """Get the appropriate border style based on unicode setting.

        Returns:
            "ascii" if unicode is disabled, "unicode" otherwise.
        """
        return "unicode" if self.unicode else "ascii"

    @property
    def icon_mode(self) -> Literal["emoji", "ascii", "auto"]:
        """Get the appropriate icon mode based on policy.

        Returns:
            "ascii" if force_ascii_icons or emoji disabled,
            "emoji" if emoji enabled, "auto" otherwise.
        """
        if self.force_ascii_icons or not self.emoji:
            return "ascii"
        return "emoji" if self.emoji else "auto"

    def apply_to_icons(self) -> None:
        """Apply this policy to the global Icon Provider.

        Sets the icon mode based on policy settings.
        """
        from styledconsole.icons import set_icon_mode

        set_icon_mode(self.icon_mode)

    def __repr__(self) -> str:
        """Return a readable representation."""
        return (
            f"RenderPolicy(unicode={self.unicode}, color={self.color}, "
            f"emoji={self.emoji}, force_ascii_icons={self.force_ascii_icons})"
        )


# Module-level default policy (auto-detected on first access)
_default_policy: RenderPolicy | None = None


def get_default_policy() -> RenderPolicy:
    """Get the default policy, auto-detecting from environment on first call.

    Returns:
        The default RenderPolicy for this process.
    """
    global _default_policy
    if _default_policy is None:
        _default_policy = RenderPolicy.from_env()
    return _default_policy


def set_default_policy(policy: RenderPolicy) -> None:
    """Set the default policy for the process.

    Args:
        policy: The RenderPolicy to use as default.
    """
    global _default_policy
    _default_policy = policy


def reset_default_policy() -> None:
    """Reset the default policy to be re-detected from environment."""
    global _default_policy
    _default_policy = None


__all__ = [
    "RenderPolicy",
    "get_default_policy",
    "reset_default_policy",
    "set_default_policy",
]
