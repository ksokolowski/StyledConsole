"""DRY Emoji Registry - Single source of truth from emoji package.

This module provides emoji constants generated from the `emoji` package,
ensuring consistent naming with the Unicode CLDR standard.

The emoji package is the single source of truth for:
- Emoji characters
- Canonical names (e.g., CHECK_MARK_BUTTON, not CHECK)
- Validation and metadata

Usage:
    from styledconsole import EMOJI

    # Canonical names from emoji package
    console.frame("Done!", title=f"{EMOJI.CHECK_MARK_BUTTON} Complete")
    console.frame("Error!", title=f"{EMOJI.CROSS_MARK} Failed")

    # All 4000+ emojis available
    print(EMOJI.ROCKET)           # 🚀
    print(EMOJI.FIRE)             # 🔥
    print(EMOJI.PARTY_POPPER)     # 🎉

Design:
    - Primary names come from emoji package (CLDR standard)
    - ~4000 emojis available, curated subset highlighted
    - Arrows (↑↓←→) handled separately (not Unicode emojis)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

# Import emoji package (required dependency for v0.10+)
import emoji as _emoji_pkg

if TYPE_CHECKING:
    pass


def _normalize_name(shortcode: str) -> str:
    """Convert emoji package shortcode to valid Python identifier.

    Examples:
        :rocket: -> ROCKET
        :check_mark_button: -> CHECK_MARK_BUTTON
        :1st_place_medal: -> E_1ST_PLACE_MEDAL
        :ON!_arrow: -> ON_ARROW
    """
    name = shortcode.strip(":").upper()
    name = name.replace("-", "_").replace(" ", "_").replace("!", "").replace("'", "")
    # Handle names starting with numbers
    if name and not name[0].isalpha() and name[0] != "_":
        name = "E_" + name
    return name


class _EmojiRegistry:
    """Dynamic emoji registry backed by emoji package.

    Provides attribute access to all emojis in the emoji package.
    Names are normalized to valid Python identifiers.
    """

    # Cache for emoji lookups
    _cache: dict[str, str]
    _initialized: bool = False

    # Unicode arrows (not in emoji package, kept for compatibility)
    _UNICODE_ARROWS: Final[dict[str, str]] = {
        "ARROW_UP": "↑",
        "ARROW_DOWN": "↓",
        "ARROW_LEFT": "←",
        "ARROW_RIGHT": "→",
    }

    def __init__(self) -> None:
        self._cache = {}
        self._initialized = False

    def _ensure_initialized(self) -> None:
        """Lazy initialization of emoji cache."""
        if self._initialized:
            return

        # Build cache from emoji package
        for char, data in _emoji_pkg.EMOJI_DATA.items():
            if "en" not in data:
                continue
            name = _normalize_name(data["en"])
            if name and name not in self._cache:
                self._cache[name] = char

        # Add Unicode arrows
        self._cache.update(self._UNICODE_ARROWS)

        self._initialized = True

    def __getattr__(self, name: str) -> str:
        """Get emoji by canonical name.

        Args:
            name: Canonical emoji name (e.g., ROCKET, CHECK_MARK_BUTTON)

        Returns:
            The emoji character

        Raises:
            AttributeError: If emoji name not found
        """
        # Skip private attributes
        if name.startswith("_"):
            raise AttributeError(name)

        self._ensure_initialized()

        if name in self._cache:
            return self._cache[name]

        raise AttributeError(
            f"Unknown emoji: {name}. Use EMOJI.search('{name.lower()}') to find similar emojis."
        )

    def __dir__(self) -> list[str]:
        """List available emoji names for autocomplete."""
        self._ensure_initialized()
        return sorted(self._cache.keys())

    def search(self, query: str, limit: int = 10) -> list[tuple[str, str]]:
        """Search for emojis by partial name.

        Args:
            query: Partial name to search for (case-insensitive)
            limit: Maximum results to return

        Returns:
            List of (name, emoji) tuples

        Example:
            >>> EMOJI.search("check")
            [('CHECK_MARK', '✔️'), ('CHECK_MARK_BUTTON', '✅'), ...]
        """
        self._ensure_initialized()
        query_upper = query.upper()
        results = [(name, char) for name, char in self._cache.items() if query_upper in name]
        return sorted(results)[:limit]

    def get(self, name: str, default: str = "") -> str:
        """Get emoji by name with default fallback.

        Args:
            name: Emoji name
            default: Default value if not found

        Returns:
            Emoji character or default
        """
        self._ensure_initialized()
        return self._cache.get(name, default)

    def __contains__(self, name: str) -> bool:
        """Check if emoji name exists."""
        self._ensure_initialized()
        return name in self._cache

    def __len__(self) -> int:
        """Return count of available emojis."""
        self._ensure_initialized()
        return len(self._cache)

    def all_names(self) -> list[str]:
        """Return all available emoji names."""
        self._ensure_initialized()
        return sorted(self._cache.keys())


# Singleton instance
EMOJI = _EmojiRegistry()

# Shorthand alias
E = EMOJI


# =============================================================================
# Curated emoji sets for common use cases
# =============================================================================


class CuratedEmojis:
    """Curated sets of emojis for common CLI/terminal use cases.

    These are the most commonly used emojis, organized by category.
    All names are canonical (from emoji package).
    """

    # Status indicators
    STATUS: Final[list[str]] = [
        "CHECK_MARK_BUTTON",  # ✅
        "CROSS_MARK",  # ❌
        "WARNING",  # ⚠️
        "INFORMATION",  # ℹ️
        "RED_QUESTION_MARK",  # ❓
        "COUNTERCLOCKWISE_ARROWS_BUTTON",  # 🔄
    ]

    # Colored circles (great for status)
    CIRCLES: Final[list[str]] = [
        "RED_CIRCLE",  # 🔴
        "YELLOW_CIRCLE",  # 🟡
        "GREEN_CIRCLE",  # 🟢
        "BLUE_CIRCLE",  # 🔵
        "PURPLE_CIRCLE",  # 🟣
        "ORANGE_CIRCLE",  # 🟠
        "WHITE_CIRCLE",  # ⚪
        "BLACK_CIRCLE",  # ⚫
    ]

    # File/folder related
    FILES: Final[list[str]] = [
        "FILE_FOLDER",  # 📁
        "OPEN_FILE_FOLDER",  # 📂
        "PAGE_FACING_UP",  # 📄
        "PAGE_WITH_CURL",  # 📃
        "MEMO",  # 📝
        "CLIPBOARD",  # 📋
        "PACKAGE",  # 📦
    ]

    # Development
    DEV: Final[list[str]] = [
        "ROCKET",  # 🚀
        "FIRE",  # 🔥
        "STAR",  # ⭐
        "SPARKLES",  # ✨
        "LIGHT_BULB",  # 💡
        "GEAR",  # ⚙️
        "WRENCH",  # 🔧
        "LAPTOP",  # 💻
        "BUG",  # 🐛
        "TEST_TUBE",  # 🧪
    ]


__all__ = [
    "EMOJI",
    "CuratedEmojis",
    "E",
]
