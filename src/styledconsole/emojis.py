"""
Emoji Constants for StyledConsole

Provides named constants for Tier 1 emojis (safe, single-codepoint emojis)
that work perfectly with StyledConsole's rendering engine.

Usage:
    from styledconsole.emojis import EMOJI, E

    # Use full names
    console.frame("Success!", title=f"{EMOJI.CHECK} Complete")

    # Or shorthand
    console.frame("Error!", title=f"{E.X} Failed")

All emojis in this module are guaranteed to:
- Be single codepoint (no ZWJ sequences)
- Have correct visual width calculation
- Work in all StyledConsole features (frames, gradients, banners)
- Be supported across major terminals

See: doc/guides/EMOJI_GUIDELINES.md for full emoji support details
"""

from typing import Final


class EmojiConstants:
    """Named constants for supported emojis.

    Organized by category for easy discovery.
    All emojis are Tier 1 (safe, single-codepoint).
    """

    # ============================================================================
    # Status & Indicators
    # ============================================================================
    CHECK: Final[str] = "✅"
    CROSS: Final[str] = "❌"
    WARNING: Final[str] = "⚠️"
    INFO: Final[str] = "ℹ️"

    # Colored Circles
    RED_CIRCLE: Final[str] = "🔴"
    YELLOW_CIRCLE: Final[str] = "🟡"
    GREEN_CIRCLE: Final[str] = "🟢"
    BLUE_CIRCLE: Final[str] = "🔵"
    PURPLE_CIRCLE: Final[str] = "🟣"
    ORANGE_CIRCLE: Final[str] = "🟠"

    # Stars & Sparkles
    STAR: Final[str] = "⭐"
    SPARKLES: Final[str] = "✨"
    DIZZY: Final[str] = "💫"
    GLOWING_STAR: Final[str] = "🌟"

    # ============================================================================
    # Objects & Tools
    # ============================================================================

    # Documents & Files
    CHART_BAR: Final[str] = "📊"
    CHART_INCREASING: Final[str] = "📈"
    CHART_DECREASING: Final[str] = "📉"
    PACKAGE: Final[str] = "📦"
    FOLDER: Final[str] = "📁"
    OPEN_FOLDER: Final[str] = "📂"
    PAGE: Final[str] = "📄"
    MEMO: Final[str] = "📝"
    CLIPBOARD: Final[str] = "📋"

    # Technology
    COMPUTER: Final[str] = "💻"
    LAPTOP: Final[str] = "💻"  # Alias
    DESKTOP: Final[str] = "🖥"  # Note: No variation selector version
    KEYBOARD: Final[str] = "⌨"  # Note: No variation selector version
    MOUSE: Final[str] = "🖱"  # Note: No variation selector version
    FLOPPY: Final[str] = "💾"
    CD: Final[str] = "💿"
    DVD: Final[str] = "📀"

    # Tools & Science
    TEST_TUBE: Final[str] = "🧪"
    MICROSCOPE: Final[str] = "🔬"
    WRENCH: Final[str] = "🔧"
    HAMMER: Final[str] = "🔨"
    GEAR: Final[str] = "⚙️"
    NUT_BOLT: Final[str] = "🔩"

    # ============================================================================
    # Activities & Celebrations
    # ============================================================================
    TARGET: Final[str] = "🎯"
    ART: Final[str] = "🎨"
    PALETTE: Final[str] = "🎨"  # Alias
    PARTY: Final[str] = "🎉"
    CONFETTI: Final[str] = "🎊"
    GIFT: Final[str] = "🎁"
    BALLOON: Final[str] = "🎈"
    TROPHY: Final[str] = "🏆"
    MEDAL: Final[str] = "🏅"

    # ============================================================================
    # Transportation & Speed
    # ============================================================================
    ROCKET: Final[str] = "🚀"
    AIRPLANE: Final[str] = "✈️"
    CAR: Final[str] = "🚗"
    BIKE: Final[str] = "🚲"
    TRAIN: Final[str] = "🚂"
    SHIP: Final[str] = "🚢"

    # ============================================================================
    # Nature & Weather
    # ============================================================================
    RAINBOW: Final[str] = "🌈"
    SUN: Final[str] = "☀️"
    MOON: Final[str] = "🌙"
    STAR_SIMPLE: Final[str] = "⭐"  # Alias
    DROPLET: Final[str] = "💧"
    FIRE: Final[str] = "🔥"
    SNOWFLAKE: Final[str] = "❄️"
    CLOUD: Final[str] = "☁️"
    LIGHTNING: Final[str] = "⚡"
    TORNADO: Final[str] = "🌪"  # Note: No variation selector version

    # Plants
    TREE: Final[str] = "🌲"
    EVERGREEN: Final[str] = "🌲"  # Alias
    PALM: Final[str] = "🌴"
    CACTUS: Final[str] = "🌵"
    SEEDLING: Final[str] = "🌱"
    HERB: Final[str] = "🌿"
    SHAMROCK: Final[str] = "☘"  # Note: No variation selector version
    FOUR_LEAF_CLOVER: Final[str] = "🍀"

    # ============================================================================
    # Food & Drink
    # ============================================================================
    PIZZA: Final[str] = "🍕"
    BURGER: Final[str] = "🍔"
    FRIES: Final[str] = "🍟"
    COFFEE: Final[str] = "☕"
    BEER: Final[str] = "🍺"
    WINE: Final[str] = "🍷"
    COCKTAIL: Final[str] = "🍹"
    CAKE: Final[str] = "🍰"
    COOKIE: Final[str] = "🍪"

    # ============================================================================
    # People & Gestures (Simple Only)
    # ============================================================================
    PEOPLE: Final[str] = "👥"
    PERSON: Final[str] = "👤"
    THUMBS_UP: Final[str] = "👍"
    THUMBS_DOWN: Final[str] = "👎"
    WAVE: Final[str] = "👋"
    HANDS_UP: Final[str] = "🙌"
    CLAP: Final[str] = "👏"
    MUSCLE: Final[str] = "💪"

    # ============================================================================
    # Symbols & Arrows
    # ============================================================================

    # Directional Arrows (base versions, no variation selectors)
    ARROW_RIGHT: Final[str] = "→"
    ARROW_LEFT: Final[str] = "←"
    ARROW_UP: Final[str] = "↑"
    ARROW_DOWN: Final[str] = "↓"
    ARROW_UP_RIGHT: Final[str] = "↗"
    ARROW_DOWN_RIGHT: Final[str] = "↘"
    ARROW_DOWN_LEFT: Final[str] = "↙"
    ARROW_UP_LEFT: Final[str] = "↖"

    # Heavy Arrows (thick versions)
    HEAVY_RIGHT: Final[str] = "➡"  # Note: No variation selector version
    HEAVY_LEFT: Final[str] = "⬅"  # Note: No variation selector version
    HEAVY_UP: Final[str] = "⬆"  # Note: No variation selector version
    HEAVY_DOWN: Final[str] = "⬇"  # Note: No variation selector version

    # Symbols
    LIGHTBULB: Final[str] = "💡"
    BELL: Final[str] = "🔔"
    SIREN: Final[str] = "🚨"
    TRIANGLE_RULER: Final[str] = "📐"
    LOCK: Final[str] = "🔒"
    UNLOCK: Final[str] = "🔓"
    KEY: Final[str] = "🔑"
    LINK: Final[str] = "🔗"
    CHAIN: Final[str] = "⛓"  # Note: No variation selector version
    MAG: Final[str] = "🔍"
    MAGNIFYING_GLASS: Final[str] = "🔍"  # Alias

    # Math & Logic
    PLUS: Final[str] = "➕"
    MINUS: Final[str] = "➖"
    MULTIPLY: Final[str] = "✖️"
    DIVIDE: Final[str] = "➗"
    EQUALS: Final[str] = "🟰"

    # ============================================================================
    # Hearts & Emotions
    # ============================================================================
    HEART: Final[str] = "❤️"
    ORANGE_HEART: Final[str] = "🧡"
    YELLOW_HEART: Final[str] = "💛"
    GREEN_HEART: Final[str] = "💚"
    BLUE_HEART: Final[str] = "💙"
    PURPLE_HEART: Final[str] = "💜"
    BROKEN_HEART: Final[str] = "💔"
    SPARKLING_HEART: Final[str] = "💖"

    # ============================================================================
    # Currency & Money
    # ============================================================================
    DOLLAR: Final[str] = "💵"
    MONEY_BAG: Final[str] = "💰"
    COIN: Final[str] = "🪙"
    CREDIT_CARD: Final[str] = "💳"
    GEM: Final[str] = "💎"
    DIAMOND: Final[str] = "💎"  # Alias

    # ============================================================================
    # Time & Calendar
    # ============================================================================
    CLOCK: Final[str] = "🕐"
    ALARM: Final[str] = "⏰"
    STOPWATCH: Final[str] = "⏱"  # Note: No variation selector version
    TIMER: Final[str] = "⏲"  # Note: No variation selector version
    HOURGLASS: Final[str] = "⌛"
    CALENDAR: Final[str] = "📅"

    # ============================================================================
    # Communication & Media
    # ============================================================================
    PHONE: Final[str] = "📱"
    TELEPHONE: Final[str] = "☎️"
    EMAIL: Final[str] = "📧"
    ENVELOPE: Final[str] = "✉️"
    MAILBOX: Final[str] = "📬"
    SPEAKER: Final[str] = "🔊"
    MEGAPHONE: Final[str] = "📣"
    LOUDSPEAKER: Final[str] = "📢"
    GLOBE: Final[str] = "🌐"
    GLOBE_MERIDIANS: Final[str] = "🌐"  # Alias

    # ============================================================================
    # Buildings & Places
    # ============================================================================
    HOME: Final[str] = "🏠"
    HOUSE: Final[str] = "🏠"  # Alias
    OFFICE: Final[str] = "🏢"
    FACTORY: Final[str] = "🏭"
    HOSPITAL: Final[str] = "🏥"
    SCHOOL: Final[str] = "🏫"
    BANK: Final[str] = "🏦"
    HOTEL: Final[str] = "🏨"

    # ============================================================================
    # Flags & Symbols (Simple)
    # ============================================================================
    FLAG_CHECKERED: Final[str] = "🏁"
    FLAG_TRIANGULAR: Final[str] = "🚩"
    WHITE_FLAG: Final[str] = "🏳"  # Note: No variation selector version

    # ============================================================================
    # Common Combinations (for convenience)
    # ============================================================================

    @staticmethod
    def success(text: str = "") -> str:
        """Return check mark with optional text."""
        return f"{EmojiConstants.CHECK} {text}".strip()

    @staticmethod
    def error(text: str = "") -> str:
        """Return cross mark with optional text."""
        return f"{EmojiConstants.CROSS} {text}".strip()

    @staticmethod
    def warning(text: str = "") -> str:
        """Return warning sign with optional text."""
        return f"{EmojiConstants.WARNING} {text}".strip()

    @staticmethod
    def info(text: str = "") -> str:
        """Return info symbol with optional text."""
        return f"{EmojiConstants.INFO} {text}".strip()


# Convenience aliases for shorter code
EMOJI = EmojiConstants
E = EmojiConstants  # Ultra-short alias for quick usage


# Export all constants for `from styledconsole.emojis import *`
__all__ = [
    "EMOJI",
    "E",
    "EmojiConstants",
]
