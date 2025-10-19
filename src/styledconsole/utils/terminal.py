"""Terminal capability detection utilities.

This module provides functions to detect terminal capabilities such as ANSI support,
color depth, emoji safety, and terminal dimensions.
"""

import os
import sys
from dataclasses import dataclass


@dataclass
class TerminalProfile:
    """Represents terminal capabilities and settings.

    Attributes:
        ansi_support: Whether the terminal supports ANSI escape codes
        color_depth: Number of colors supported (8, 256, or 16777216 for truecolor)
        emoji_safe: Whether emoji rendering is likely safe
        width: Terminal width in characters
        height: Terminal height in characters
        term: Value of the TERM environment variable
        colorterm: Value of the COLORTERM environment variable
    """

    ansi_support: bool
    color_depth: int
    emoji_safe: bool
    width: int
    height: int
    term: str | None
    colorterm: str | None


def detect_terminal_capabilities() -> TerminalProfile:
    """Detect current terminal capabilities.

    Detects:
    - ANSI support via isatty() and TERM environment variable
    - Color depth via COLORTERM and TERM variables
    - Emoji safety heuristically (UTF-8 locale + color support)
    - Terminal dimensions via os.get_terminal_size()

    Returns:
        TerminalProfile with detected capabilities

    Example:
        >>> profile = detect_terminal_capabilities()
        >>> if profile.ansi_support:
        ...     print("\\033[32mGreen text\\033[0m")
        >>> if profile.emoji_safe:
        ...     print("🚀 Emoji supported!")
    """
    # Check if stdout is a TTY
    is_tty = sys.stdout.isatty()

    # Get environment variables
    term = os.environ.get("TERM", "")
    colorterm = os.environ.get("COLORTERM", "")

    # Detect ANSI support
    # Supported if:
    # 1. stdout is a TTY
    # 2. TERM is not empty or "dumb"
    # 3. Not explicitly disabled via NO_COLOR or TERM=dumb
    ansi_support = (
        is_tty
        and term not in ("", "dumb")
        and "NO_COLOR" not in os.environ
        and "ANSI_COLORS_DISABLED" not in os.environ
    )

    # Detect color depth
    color_depth = _detect_color_depth(term, colorterm, ansi_support)

    # Detect emoji safety
    # Heuristic: UTF-8 locale + color support + not in CI
    emoji_safe = _detect_emoji_safety(is_tty, color_depth)

    # Get terminal dimensions
    width, height = _get_terminal_size()

    return TerminalProfile(
        ansi_support=ansi_support,
        color_depth=color_depth,
        emoji_safe=emoji_safe,
        width=width,
        height=height,
        term=term if term else None,
        colorterm=colorterm if colorterm else None,
    )


def _detect_color_depth(term: str, colorterm: str, ansi_support: bool) -> int:
    """Detect terminal color depth.

    Args:
        term: Value of TERM environment variable
        colorterm: Value of COLORTERM environment variable
        ansi_support: Whether ANSI is supported

    Returns:
        Number of colors: 8, 256, or 16777216 (truecolor), or 0 if no color
    """
    if not ansi_support:
        return 0

    # Check for truecolor support
    if colorterm in ("truecolor", "24bit"):
        return 16777216  # 2^24 colors

    # Check TERM for color hints
    term_lower = term.lower()

    # 256 color terminals
    if "256color" in term_lower or "256" in term_lower:
        return 256

    # Basic color terminals
    if any(hint in term_lower for hint in ["color", "ansi", "xterm", "screen", "tmux", "linux"]):
        return 8

    # Default to basic ANSI colors if supported
    return 8 if ansi_support else 0


def _detect_emoji_safety(is_tty: bool, color_depth: int) -> bool:
    """Detect if emoji rendering is likely safe.

    Uses heuristics:
    - Requires TTY output
    - Requires color support (emoji often rely on color)
    - UTF-8 locale (check LANG, LC_ALL, LC_CTYPE)
    - Not in CI environment (GitHub Actions, Jenkins, etc.)

    Args:
        is_tty: Whether output is to a TTY
        color_depth: Detected color depth

    Returns:
        True if emoji rendering is likely safe
    """
    if not is_tty or color_depth == 0:
        return False

    # Check for CI environments where emoji might not render well
    ci_vars = ["CI", "GITHUB_ACTIONS", "JENKINS_URL", "GITLAB_CI", "CIRCLECI"]
    if any(var in os.environ for var in ci_vars):
        return False

    # Check for UTF-8 locale
    locale_vars = ["LANG", "LC_ALL", "LC_CTYPE"]
    for var in locale_vars:
        value = os.environ.get(var, "")
        if value and "UTF-8" in value.upper():
            return True

    # Default to False if we can't confirm UTF-8
    return False


def _get_terminal_size() -> tuple[int, int]:
    """Get terminal dimensions.

    Returns:
        Tuple of (width, height) in characters. Returns (80, 24) as fallback.
    """
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except (OSError, ValueError):
        # Fallback to standard terminal size
        return 80, 24


__all__ = [
    "TerminalProfile",
    "detect_terminal_capabilities",
]
