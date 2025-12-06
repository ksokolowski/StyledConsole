"""
Emoji Constants for StyledConsole.

This module re-exports from emoji_registry for backward compatibility.
The emoji_registry module is the single source of truth (DRY principle),
using the `emoji` package as the authoritative source for:
- Emoji characters
- Canonical names (CLDR standard)
- Validation and metadata

Usage:
    from styledconsole.emojis import EMOJI, E

    # Canonical names from emoji package
    console.frame("Success!", title=f"{EMOJI.CHECK_MARK_BUTTON} Complete")
    console.frame("Error!", title=f"{EMOJI.CROSS_MARK} Failed")

    # All 4000+ emojis available
    print(EMOJI.ROCKET)           # 🚀
    print(EMOJI.FIRE)             # 🔥
    print(EMOJI.PARTY_POPPER)     # 🎉

See: docs/USER_GUIDE.md for full emoji support details.
"""

# Re-export from the DRY source of truth
from styledconsole.emoji_registry import EMOJI, CuratedEmojis, E

# Alias for backward compatibility with tests that import EmojiConstants
EmojiConstants = type(EMOJI)

__all__ = [
    "EMOJI",
    "CuratedEmojis",
    "E",
    "EmojiConstants",
]
