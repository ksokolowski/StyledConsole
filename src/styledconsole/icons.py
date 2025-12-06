"""Icon Provider for terminal-adaptive emoji/ASCII rendering.

This module provides a smart icon system that automatically switches between
Unicode emojis and colored ASCII fallbacks based on terminal capabilities.

Features:
- Auto-detection: Uses terminal profile to choose emoji vs ASCII
- Colored ASCII: Fallbacks include semantic colors (green=success, red=error)
- Mode switching: Global or per-icon mode override
- Rich integration: ASCII colors use Rich markup

Usage:
    from styledconsole import icons

    # Auto-detects terminal capability
    print(f"{icons.CHECK_MARK_BUTTON} Tests passed")     # ✅ or [OK] (green)
    print(f"{icons.CROSS_MARK} Build failed")     # ❌ or [FAIL] (red)
    print(f"{icons.WARNING} Deprecation")    # ⚠️ or [WARN] (yellow)

    # Force specific mode globally
    from styledconsole import set_icon_mode
    set_icon_mode("ascii")   # Force ASCII everywhere
    set_icon_mode("emoji")   # Force emoji everywhere
    set_icon_mode("auto")    # Auto-detect (default)

    # Access icon properties
    icon = icons.get("CHECK")
    print(icon.emoji)    # "✅"
    print(icon.ascii)    # "[OK]"
    print(icon.color)    # "green"
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from styledconsole.utils.icon_data import EMOJI_TO_ICON, ICON_REGISTRY
from styledconsole.utils.terminal import detect_terminal_capabilities

if TYPE_CHECKING:
    from styledconsole.utils.terminal import TerminalProfile


# Type alias for icon rendering mode
IconMode = Literal["auto", "emoji", "ascii"]


# =============================================================================
# Module-level state
# =============================================================================
_current_mode: IconMode = "auto"
_terminal_profile: TerminalProfile | None = None


def _get_emoji_safe() -> bool:
    """Get cached terminal emoji safety status."""
    global _terminal_profile
    if _terminal_profile is None:
        _terminal_profile = detect_terminal_capabilities()
    return _terminal_profile.emoji_safe


# =============================================================================
# Icon class
# =============================================================================
@dataclass(frozen=True, slots=True)
class Icon:
    """A single icon with emoji and colored ASCII variants.

    Icons automatically render as emoji or colored ASCII based on
    the current mode and terminal capabilities.

    Attributes:
        name: Icon identifier (e.g., "CHECK", "WARNING")
        emoji: Unicode emoji representation
        ascii: ASCII fallback representation
        color: Rich-compatible color for ASCII mode (or None)

    Example:
        >>> icon = Icon("CHECK", "✅", "[OK]", "green")
        >>> str(icon)  # Returns emoji or colored ASCII based on mode
        '✅'
        >>> icon.as_ascii()
        '[green][OK][/]'
        >>> icon.as_emoji()
        '✅'
    """

    name: str
    emoji: str
    ascii: str
    color: str | None = None

    def __str__(self) -> str:
        """Return appropriate representation based on current mode.

        Returns:
            - In "emoji" mode: Always returns emoji
            - In "ascii" mode: Always returns colored ASCII
            - In "auto" mode: Returns emoji if terminal supports it, else ASCII
        """
        if _current_mode == "emoji":
            return self.emoji
        if _current_mode == "ascii":
            return self.as_ascii()
        # Auto mode - check terminal capability
        if _get_emoji_safe():
            return self.emoji
        return self.as_ascii()

    def as_emoji(self) -> str:
        """Return emoji representation regardless of mode."""
        return self.emoji

    def as_ascii(self) -> str:
        """Return colored ASCII representation with ANSI escape codes.

        Uses ANSI escape codes directly for coloring, which works universally
        in both Rich-rendered contexts and plain terminal output.

        Returns:
            ASCII string with ANSI color codes if color is defined,
            otherwise plain ASCII string.
        """
        if self.color:
            from styledconsole.utils.color import color_to_ansi

            return color_to_ansi(self.ascii, self.color)
        return self.ascii

    def as_plain_ascii(self) -> str:
        """Return plain ASCII without color markup."""
        return self.ascii


# =============================================================================
# IconProvider class
# =============================================================================
class IconProvider:
    """Central registry of icons with attribute-style access.

    Provides access to all icons via attribute names matching
    the constants in emojis.py (e.g., icons.CHECK_MARK_BUTTON, icons.WARNING).

    The provider is a singleton-like object that should be accessed
    via the module-level `icons` instance.

    Example:
        >>> from styledconsole import icons
        >>> print(icons.CHECK_MARK_BUTTON)           # ✅ or [OK]
        >>> print(icons.ROCKET)          # 🚀 or >>>
        >>> icon = icons.get("WARNING")  # Get Icon object
        >>> print(icon.color)            # "yellow"
    """

    def __init__(self) -> None:
        """Initialize the icon provider with all registered icons."""
        self._icons: dict[str, Icon] = {}
        self._load_icons()

    def _load_icons(self) -> None:
        """Load all icons from the registry."""
        for name, mapping in ICON_REGISTRY.items():
            self._icons[name] = Icon(
                name=name,
                emoji=mapping.emoji,
                ascii=mapping.ascii,
                color=mapping.color,
            )

    def __getattr__(self, name: str) -> Icon:
        """Get icon by attribute name.

        Args:
            name: Icon name (e.g., "CHECK", "WARNING", "ROCKET")

        Returns:
            Icon object for the requested name

        Raises:
            AttributeError: If icon name is not found
        """
        # Skip private attributes
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        if name in self._icons:
            return self._icons[name]

        raise AttributeError(
            f"Icon '{name}' not found. "
            f"Available icons: {', '.join(sorted(self._icons.keys())[:10])}..."
        )

    def get(self, name: str) -> Icon | None:
        """Get icon by name, returning None if not found.

        Args:
            name: Icon name (e.g., "CHECK", "WARNING")

        Returns:
            Icon object or None if not found
        """
        return self._icons.get(name)

    def get_by_emoji(self, emoji: str) -> Icon | None:
        """Get icon by its emoji character.

        Args:
            emoji: Unicode emoji to look up

        Returns:
            Icon object or None if not found
        """
        mapping = EMOJI_TO_ICON.get(emoji)
        if mapping:
            # Find the name by matching emoji
            for _name, icon in self._icons.items():
                if icon.emoji == emoji:
                    return icon
        return None

    def list_icons(self) -> list[str]:
        """Return list of all available icon names."""
        return sorted(self._icons.keys())

    def list_by_category(self) -> dict[str, list[str]]:
        """Return icons organized by category.

        Returns:
            Dictionary mapping category name to list of icon names
        """
        # Import category dicts to build the mapping
        from styledconsole.utils.icon_data import (
            ACTIVITY_ICONS,
            ANIMAL_ICONS,
            ARROW_ICONS,
            BOOK_ICONS,
            BUILDING_ICONS,
            COMM_ICONS,
            DOCUMENT_ICONS,
            FLAG_ICONS,
            FOOD_ICONS,
            HEART_ICONS,
            MATH_ICONS,
            MONEY_ICONS,
            PEOPLE_ICONS,
            PLANT_ICONS,
            STARS_ICONS,
            STATUS_ICONS,
            SYMBOL_ICONS,
            TECH_ICONS,
            TIME_ICONS,
            TOOLS_ICONS,
            TRANSPORT_ICONS,
            WEATHER_ICONS,
        )

        return {
            "status": list(STATUS_ICONS.keys()),
            "stars": list(STARS_ICONS.keys()),
            "documents": list(DOCUMENT_ICONS.keys()),
            "books": list(BOOK_ICONS.keys()),
            "technology": list(TECH_ICONS.keys()),
            "tools": list(TOOLS_ICONS.keys()),
            "activities": list(ACTIVITY_ICONS.keys()),
            "transport": list(TRANSPORT_ICONS.keys()),
            "weather": list(WEATHER_ICONS.keys()),
            "plants": list(PLANT_ICONS.keys()),
            "food": list(FOOD_ICONS.keys()),
            "people": list(PEOPLE_ICONS.keys()),
            "arrows": list(ARROW_ICONS.keys()),
            "symbols": list(SYMBOL_ICONS.keys()),
            "math": list(MATH_ICONS.keys()),
            "hearts": list(HEART_ICONS.keys()),
            "money": list(MONEY_ICONS.keys()),
            "time": list(TIME_ICONS.keys()),
            "communication": list(COMM_ICONS.keys()),
            "buildings": list(BUILDING_ICONS.keys()),
            "flags": list(FLAG_ICONS.keys()),
            "animals": list(ANIMAL_ICONS.keys()),
        }

    def __len__(self) -> int:
        """Return number of available icons."""
        return len(self._icons)

    def __iter__(self):
        """Iterate over icon names."""
        return iter(self._icons)

    def __contains__(self, name: str) -> bool:
        """Check if icon name exists."""
        return name in self._icons


# =============================================================================
# Module-level API
# =============================================================================

# Singleton icon provider instance
icons = IconProvider()


def set_icon_mode(mode: IconMode) -> None:
    """Set global icon rendering mode.

    Args:
        mode: One of:
            - "auto": Auto-detect based on terminal capabilities (default)
            - "emoji": Always use Unicode emojis
            - "ascii": Always use colored ASCII fallbacks

    Example:
        >>> from styledconsole import set_icon_mode, icons
        >>> set_icon_mode("ascii")
        >>> print(icons.CHECK_MARK_BUTTON)  # Always prints [OK] in green
        >>> set_icon_mode("emoji")
        >>> print(icons.CHECK_MARK_BUTTON)  # Always prints ✅
        >>> set_icon_mode("auto")
        >>> print(icons.CHECK_MARK_BUTTON)  # Depends on terminal
    """
    global _current_mode
    if mode not in ("auto", "emoji", "ascii"):
        raise ValueError(f"Invalid mode '{mode}'. Must be 'auto', 'emoji', or 'ascii'")
    _current_mode = mode


def get_icon_mode() -> IconMode:
    """Get current icon rendering mode.

    Returns:
        Current mode: "auto", "emoji", or "ascii"
    """
    return _current_mode


def reset_icon_mode() -> None:
    """Reset icon mode to default ("auto")."""
    global _current_mode
    _current_mode = "auto"


def convert_emoji_to_ascii(text: str) -> str:
    """Convert all emojis in text to their colored ASCII equivalents.

    This function scans text for known emojis and replaces them with
    their ASCII + ANSI color code equivalents. Useful for processing
    strings that may contain emojis.

    Args:
        text: Text potentially containing emojis

    Returns:
        Text with emojis replaced by colored ASCII

    Example:
        >>> result = convert_emoji_to_ascii("Status: ✅ Done")
        >>> # Returns: 'Status: \\033[38;2;0;255;0m[OK]\\033[0m Done'
    """
    from styledconsole.utils.color import color_to_ansi

    result = text
    for emoji, mapping in EMOJI_TO_ICON.items():
        if emoji in result:
            if mapping.color:
                replacement = color_to_ansi(mapping.ascii, mapping.color)
            else:
                replacement = mapping.ascii
            result = result.replace(emoji, replacement)
    return result


__all__ = [
    # Core classes
    "Icon",
    "IconMode",
    "IconProvider",
    # Utility functions
    "convert_emoji_to_ascii",
    "get_icon_mode",
    # Singleton instance
    "icons",
    "reset_icon_mode",
    # Mode control functions
    "set_icon_mode",
]
