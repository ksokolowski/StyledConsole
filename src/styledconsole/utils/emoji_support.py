"""Optional emoji package integration for enhanced emoji handling.

This module provides a wrapper around the PyPI `emoji` package (>=2.15.0) with
fallback behavior when the package is not installed. It enhances StyledConsole's
emoji capabilities without breaking existing functionality.

Key Features:
- Comprehensive emoji validation (4,000+ emojis vs 200 in SAFE_EMOJIS)
- Proper ZWJ sequence detection using Unicode standard
- Emoji version filtering for terminal compatibility
- Shortcode conversion (:rocket: → 🚀)

Usage:
    from styledconsole.utils.emoji_support import (
        is_valid_emoji,
        is_zwj_sequence,
        get_emoji_info,
        EMOJI_PACKAGE_AVAILABLE,
    )

Installation:
    pip install styledconsole[emoji]
    # or
    pip install emoji>=2.15.0
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

# Try to import the emoji package
try:
    import emoji as _emoji_pkg
except ImportError as err:
    # This should technically not happen if installed with dependencies
    # but we handle it gracefully just in case
    raise ImportError(
        "The 'emoji' package is required but not installed. "
        "Please install styledconsole with dependencies."
    ) from err

EMOJI_PACKAGE_AVAILABLE = True

if TYPE_CHECKING:
    from typing import Any


@dataclass
class EmojiInfo:
    """Emoji information container.

    Attributes:
        emoji: The emoji character itself
        name: Human-readable name (e.g., "rocket")
        is_valid: Whether this is a valid emoji
        is_zwj: Whether this is a ZWJ sequence
        is_zwj_non_rgi: Whether this is a non-RGI ZWJ sequence
        version: Emoji Unicode version (e.g., 0.6 for 🚀)
        terminal_safe: Whether this emoji renders safely in terminals
    """

    emoji: str
    name: str
    is_valid: bool
    is_zwj: bool = False
    is_zwj_non_rgi: bool = False
    version: float | None = None
    terminal_safe: bool = True


def is_valid_emoji(char: str) -> bool:
    """Check if a character is a valid emoji.

    Uses the `emoji` package for comprehensive Unicode coverage.

    Args:
        char: Character to check

    Returns:
        True if the character is a valid emoji

    Example:
        >>> is_valid_emoji("🚀")
        True
        >>> is_valid_emoji("👨‍👩‍👧")  # ZWJ sequence
        True
        >>> is_valid_emoji("A")
        False
    """
    return _emoji_pkg.is_emoji(char)


def is_zwj_sequence(text: str) -> bool:
    """Check if text contains a ZWJ (Zero Width Joiner) sequence.

    ZWJ sequences combine multiple emojis into one glyph (e.g., 👨‍👩‍👧 family).
    These are often problematic in terminals due to inconsistent rendering.

    Args:
        text: Text to check for ZWJ sequences

    Returns:
        True if text contains ZWJ sequences

    Example:
        >>> is_zwj_sequence("👨‍👩‍👧")
        True
        >>> is_zwj_sequence("🚀")
        False
    """
    for token in _emoji_pkg.analyze(text, join_emoji=True):
        if hasattr(token.value, "emoji"):
            # Check if the matched emoji contains ZWJ character
            emoji_str = token.value.emoji
            if "\u200d" in emoji_str:
                return True
            # Also check for ZWJ/non-RGI match types
            if isinstance(
                token.value,
                (_emoji_pkg.EmojiMatchZWJ, _emoji_pkg.EmojiMatchZWJNonRGI),
            ):
                return True
    return False


def analyze_emoji_safety(text: str) -> dict[str, Any]:
    """Analyze text for emoji safety in terminals.

    Returns detailed information about emojis in the text, categorized
    by their terminal rendering safety.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with emoji analysis results:
        - emoji_count: Total number of emojis
        - safe_emojis: List of terminal-safe emojis
        - zwj_sequences: List of ZWJ sequences (potentially problematic)
        - non_rgi: List of non-RGI ZWJ sequences (likely problematic)
        - all_safe: Boolean indicating if all emojis are terminal-safe

    Example:
        >>> result = analyze_emoji_safety("Hello 🚀 and 👨‍👩‍👧")
        >>> result["emoji_count"]
        2
        >>> result["all_safe"]
        False
    """
    results: dict[str, Any] = {
        "emoji_count": _emoji_pkg.emoji_count(text),
        "safe_emojis": [],
        "zwj_sequences": [],
        "non_rgi": [],
        "all_safe": True,
    }

    for token in _emoji_pkg.analyze(text, join_emoji=True):
        if hasattr(token.value, "emoji"):
            match = token.value
            emoji_char = match.emoji

            # Check for non-RGI ZWJ sequences first
            if isinstance(match, _emoji_pkg.EmojiMatchZWJNonRGI):
                results["non_rgi"].append(emoji_char)
                results["all_safe"] = False
            # Check for ZWJ match type or ZWJ character in emoji
            elif isinstance(match, _emoji_pkg.EmojiMatchZWJ) or "\u200d" in emoji_char:
                results["zwj_sequences"].append(emoji_char)
                results["all_safe"] = False
            else:
                results["safe_emojis"].append(emoji_char)

    return results


def get_emoji_info(char: str) -> EmojiInfo:
    """Get detailed information about an emoji.

    Uses the `emoji` package for comprehensive metadata.

    Args:
        char: Emoji character to get info for

    Returns:
        EmojiInfo dataclass with emoji metadata

    Example:
        >>> info = get_emoji_info("🚀")
        >>> info.name
        'rocket'
        >>> info.is_valid
        True
        >>> info.version
        0.6
    """
    if not _emoji_pkg.is_emoji(char):
        return EmojiInfo(emoji=char, name="", is_valid=False, terminal_safe=False)

    # Check if ZWJ sequence - either by match type or presence of ZWJ character
    is_zwj = "\u200d" in char  # Direct check for ZWJ character
    is_zwj_non_rgi = False
    for token in _emoji_pkg.analyze(char, join_emoji=True):
        if hasattr(token.value, "emoji"):
            if isinstance(token.value, _emoji_pkg.EmojiMatchZWJNonRGI):
                is_zwj_non_rgi = True
                is_zwj = True
            elif isinstance(token.value, _emoji_pkg.EmojiMatchZWJ):
                is_zwj = True

    # Get metadata from EMOJI_DATA
    data = _emoji_pkg.EMOJI_DATA.get(char, {})
    name = data.get("en", "").strip(":").replace("_", " ")
    version = data.get("E")

    # ZWJ sequences are not terminal-safe
    terminal_safe = not is_zwj

    return EmojiInfo(
        emoji=char,
        name=name,
        is_valid=True,
        is_zwj=is_zwj,
        is_zwj_non_rgi=is_zwj_non_rgi,
        version=version,
        terminal_safe=terminal_safe,
    )


def get_emoji_version(char: str) -> float | None:
    """Get the Unicode/Emoji version of an emoji.

    Useful for determining if an emoji is supported on older terminals.

    Args:
        char: Emoji character

    Returns:
        Emoji version (e.g., 0.6, 5.0, 15.0) or None if unknown

    Example:
        >>> get_emoji_version("🚀")  # Emoji 0.6
        0.6
        >>> get_emoji_version("🦖")  # Emoji 5.0
        5.0
        >>> get_emoji_version("A")  # Not an emoji
        None
    """
    if not _emoji_pkg.is_emoji(char):
        return None

    return _emoji_pkg.version(char)


def filter_by_version(text: str, max_version: float = 5.0, replacement: str = "□") -> str:
    """Replace emojis newer than max_version with a placeholder.

    Useful for ensuring emoji compatibility with older terminals.

    Args:
        text: Text containing emojis
        max_version: Maximum emoji version to allow (default 5.0)
        replacement: Replacement character for unsupported emojis

    Returns:
        Text with newer emojis replaced

    Example:
        >>> filter_by_version("Hello 🚀 World", max_version=0.5)
        'Hello □ World'
    """

    def replacer(chars: str, _data: dict) -> str:
        version = _emoji_pkg.version(chars)
        if version is not None and version <= max_version:
            return chars
        return replacement

    return _emoji_pkg.replace_emoji(text, replace=replacer)


def emojize(text: str, language: str = "alias") -> str:
    """Convert shortcodes to emoji characters.

    Args:
        text: Text with emoji shortcodes like :rocket:
        language: Language for shortcodes (default "alias" for GitHub-style)

    Returns:
        Text with shortcodes converted to emojis

    Example:
        >>> emojize(":rocket: Launch!")
        '🚀 Launch!'
        >>> emojize(":check_mark: Done")
        '✔️ Done'
    """
    return _emoji_pkg.emojize(text, language=language)


def demojize(text: str, language: str = "alias") -> str:
    """Convert emoji characters to shortcodes.

    Args:
        text: Text with emoji characters
        language: Language for shortcodes (default "alias" for GitHub-style)

    Returns:
        Text with emojis converted to shortcodes

    Example:
        >>> demojize("🚀 Launch!")
        ':rocket: Launch!'
    """
    return _emoji_pkg.demojize(text, language=language)


def get_all_emojis() -> set[str]:
    """Get a set of all valid emoji characters.

    Returns the complete Unicode emoji set from the `emoji` package.

    Returns:
        Set of emoji characters

    Example:
        >>> "🚀" in get_all_emojis()
        True
        >>> len(get_all_emojis())  # ~4000+ with emoji package
        ...
    """
    return set(_emoji_pkg.EMOJI_DATA.keys())


def emoji_list(text: str) -> list[dict[str, Any]]:
    """Find all emojis in text with their positions.

    Args:
        text: Text to search for emojis

    Returns:
        List of dicts with 'emoji', 'match_start', 'match_end' keys

    Example:
        >>> emoji_list("Hello 👋 World 🌍")
        [{'emoji': '👋', 'match_start': 6, 'match_end': 7},
         {'emoji': '🌍', 'match_start': 14, 'match_end': 15}]
    """
    return list(_emoji_pkg.emoji_list(text))  # type: ignore[arg-type]


__all__ = [
    "EMOJI_PACKAGE_AVAILABLE",
    "EmojiInfo",
    "analyze_emoji_safety",
    "demojize",
    "emoji_list",
    "emojize",
    "filter_by_version",
    "get_all_emojis",
    "get_emoji_info",
    "get_emoji_version",
    "is_valid_emoji",
    "is_zwj_sequence",
]
