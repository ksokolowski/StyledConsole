"""Icon mapping data for emoji to colored ASCII fallback.

This module contains the mapping from Unicode emojis to their ASCII
equivalents with associated colors. Used by the Icon Provider system
to provide consistent fallback rendering in terminals without emoji support.

Design Principles:
- ASCII symbols should preserve semantic meaning
- Colors should convey the same message (green=success, red=error)
- Symbols should be recognizable and distinct
- Width should be reasonable (1-6 characters)

Color Philosophy:
- Status indicators: green/red/yellow/cyan match their semantic meaning
- Colored emojis (circles, hearts): use the color they represent
- Neutral objects: gray or no color (terminal default)
- Actions/movement: cyan for active/running
- Celebrations: gold/yellow for positive
"""

from typing import Final, NamedTuple


class IconMapping(NamedTuple):
    """Mapping from emoji to ASCII with optional color.

    Attributes:
        emoji: The Unicode emoji character(s)
        ascii: ASCII fallback representation
        color: Rich-compatible color (CSS4 name, hex, or None for default)
    """

    emoji: str
    ascii: str
    color: str | None


# =============================================================================
# ICON MAPPINGS BY CATEGORY
# =============================================================================

# -----------------------------------------------------------------------------
# Status & Indicators - Most important for test/CI output
# NOTE: Avoid square brackets in ASCII - they conflict with Rich markup
# -----------------------------------------------------------------------------
STATUS_ICONS: Final[dict[str, IconMapping]] = {
    # Primary status - use parentheses or other symbols
    "CHECK_MARK_BUTTON": IconMapping("✅", "(OK)", "green"),
    "CROSS_MARK": IconMapping("❌", "(FAIL)", "red"),
    "WARNING": IconMapping("⚠️", "(WARN)", "yellow"),
    "INFORMATION": IconMapping("ℹ️", "(INFO)", "cyan"),
    "RED_QUESTION_MARK": IconMapping("❓", "(?)", "magenta"),
    "COUNTERCLOCKWISE_ARROWS_BUTTON": IconMapping("🔄", "(~)", "cyan"),
    # Colored circles -> colored bullets
    "RED_CIRCLE": IconMapping("🔴", "●", "red"),
    "YELLOW_CIRCLE": IconMapping("🟡", "●", "yellow"),
    "GREEN_CIRCLE": IconMapping("🟢", "●", "green"),
    "BLUE_CIRCLE": IconMapping("🔵", "●", "blue"),
    "PURPLE_CIRCLE": IconMapping("🟣", "●", "magenta"),
    "ORANGE_CIRCLE": IconMapping("🟠", "●", "darkorange"),
    "WHITE_CIRCLE": IconMapping("⚪", "○", None),
    "BLACK_CIRCLE": IconMapping("⚫", "●", None),
}

# -----------------------------------------------------------------------------
# Stars & Sparkles - Celebrations, highlights
# -----------------------------------------------------------------------------
STARS_ICONS: Final[dict[str, IconMapping]] = {
    "STAR": IconMapping("⭐", "*", "yellow"),
    "SPARKLES": IconMapping("✨", "**", "yellow"),
    "DIZZY": IconMapping("💫", "*~", "yellow"),
    "GLOWING_STAR": IconMapping("🌟", "(*)", "yellow"),
}

# -----------------------------------------------------------------------------
# Documents & Data - Files, charts, storage
# -----------------------------------------------------------------------------
DOCUMENT_ICONS: Final[dict[str, IconMapping]] = {
    # Charts
    "BAR_CHART": IconMapping("📊", "(#)", "blue"),
    "CHART_INCREASING": IconMapping("📈", "(^)", "green"),
    "CHART_DECREASING": IconMapping("📉", "(v)", "red"),
    "PACKAGE": IconMapping("📦", "(P)", "saddlebrown"),
    # Folders
    "FILE_FOLDER": IconMapping("📁", "(/)", "blue"),
    "OPEN_FILE_FOLDER": IconMapping("📂", "(+)", "blue"),
    "FILE_CABINET": IconMapping("🗄", "(=)", "gray"),
    "CARD_FILE_BOX": IconMapping("🗃", "(=)", "gray"),
    "WASTEBASKET": IconMapping("🗑", "(x)", "gray"),
    # Files
    "PAGE_FACING_UP": IconMapping("📄", "(f)", None),
    "PAGE_WITH_CURL": IconMapping("📃", "(d)", None),
    "SCROLL": IconMapping("📜", "(s)", "goldenrod"),
    "MEMO": IconMapping("📝", "(m)", None),
    "CLIPBOARD": IconMapping("📋", "(c)", None),
    "PUSHPIN": IconMapping("📌", "(*)", "red"),
    "PAPERCLIP": IconMapping("📎", "(-)", "gray"),
    "BOOKMARK": IconMapping("🔖", "(>)", "tomato"),
    "LABEL": IconMapping("🏷", "(t)", None),
    "CARD_INDEX": IconMapping("📇", "(i)", None),
    "CONSTRUCTION": IconMapping("🚧", "(!!)", "yellow"),
}

# -----------------------------------------------------------------------------
# Books & Reading
# -----------------------------------------------------------------------------
BOOK_ICONS: Final[dict[str, IconMapping]] = {
    "OPEN_BOOK": IconMapping("📖", "(B)", None),
    "BOOKS": IconMapping("📚", "(BB)", None),
    "NOTEBOOK": IconMapping("📓", "(N)", None),
    "LEDGER": IconMapping("📒", "(L)", "yellow"),
    "CLOSED_BOOK": IconMapping("📕", "(B)", "red"),
    "GREEN_BOOK": IconMapping("📗", "(B)", "green"),
    "BLUE_BOOK": IconMapping("📘", "(B)", "blue"),
    "ORANGE_BOOK": IconMapping("📙", "(B)", "darkorange"),
    "NEWSPAPER": IconMapping("📰", "(N)", None),
    "ROLLED_UP_NEWSPAPER": IconMapping("🗞", "(N)", None),
}

# -----------------------------------------------------------------------------
# Technology - Computers, devices
# -----------------------------------------------------------------------------
TECH_ICONS: Final[dict[str, IconMapping]] = {
    "LAPTOP": IconMapping("💻", "(PC)", None),
    "DESKTOP": IconMapping("🖥", "(PC)", None),
    "KEYBOARD": IconMapping("⌨", "(kb)", None),
    "MOUSE": IconMapping("🖱", "(m)", None),
    "FLOPPY_DISK": IconMapping("💾", "(D)", None),
    "CD": IconMapping("💿", "(O)", None),
    "DVD": IconMapping("📀", "(O)", "gold"),
    "DESKTOP_COMPUTER": IconMapping("🖥", "(C)", None),
    "SATELLITE_ANTENNA": IconMapping("📡", "(A)", None),
    "GLOBE_WITH_MERIDIANS": IconMapping("🌐", "(@)", "blue"),
}

# -----------------------------------------------------------------------------
# Tools & Science - Development, testing
# -----------------------------------------------------------------------------
TOOLS_ICONS: Final[dict[str, IconMapping]] = {
    "TEST_TUBE": IconMapping("🧪", "(T)", "mediumpurple"),
    "MICROSCOPE": IconMapping("🔬", "(M)", None),
    "TRIANGULAR_RULER": IconMapping("📐", "(/)", None),
    "WRENCH": IconMapping("🔧", "(w)", "gray"),
    "HAMMER": IconMapping("🔨", "(h)", "gray"),
    "GEAR": IconMapping("⚙️", "(*)", "gray"),
    "NUT_BOLT": IconMapping("🔩", "(o)", "gray"),
}

# -----------------------------------------------------------------------------
# Activities & Celebrations
# -----------------------------------------------------------------------------
ACTIVITY_ICONS: Final[dict[str, IconMapping]] = {
    "BULLSEYE": IconMapping("🎯", "(o)", "red"),
    "ARTIST_PALETTE": IconMapping("🎨", "(~)", None),
    "PAINTBRUSH": IconMapping("🖌️", "(/)", None),
    "PARTY_POPPER": IconMapping("🎉", "(!)", "gold"),
    "CONFETTI_BALL": IconMapping("🎊", "(!)", "gold"),
    "WRAPPED_GIFT": IconMapping("🎁", "(G)", "red"),
    "BALLOON": IconMapping("🎈", "o", "red"),
    "TROPHY": IconMapping("🏆", "(#)", "gold"),
    "MEDAL": IconMapping("🏅", "(m)", "gold"),
    "FIREWORKS": IconMapping("🎆", "(*)", "gold"),
    "CIRCUS_TENT": IconMapping("🎪", "(^)", "red"),
    "PERFORMING_ARTS": IconMapping("🎭", "(:))", None),
}

# -----------------------------------------------------------------------------
# Transportation & Speed
# -----------------------------------------------------------------------------
TRANSPORT_ICONS: Final[dict[str, IconMapping]] = {
    "ROCKET": IconMapping("🚀", ">>>", "cyan"),
    "AIRPLANE": IconMapping("✈️", "->", None),
    "AUTOMOBILE": IconMapping("🚗", "(>)", "red"),
    "BIKE": IconMapping("🚲", "(o)", None),
    "LOCOMOTIVE": IconMapping("🚂", "(=)", None),
    "SHIP": IconMapping("🚢", "(~)", None),
}

# -----------------------------------------------------------------------------
# Nature & Weather
# -----------------------------------------------------------------------------
WEATHER_ICONS: Final[dict[str, IconMapping]] = {
    "RAINBOW": IconMapping("🌈", "(~)", None),  # No single color fits
    "SUN": IconMapping("☀️", "(O)", "yellow"),
    "SUNRISE": IconMapping("🌅", "(^)", "darkorange"),
    "MOON": IconMapping("🌙", "(C)", "yellow"),
    "DROPLET": IconMapping("💧", "o", "blue"),
    "WATER_WAVE": IconMapping("🌊", "~~~", "blue"),
    "FIRE": IconMapping("🔥", "~", "orangered"),
    "SNOWFLAKE": IconMapping("❄️", "*", "cyan"),
    "CLOUD": IconMapping("☁️", "(~)", None),
    "HIGH_VOLTAGE": IconMapping("⚡", "/\\", "yellow"),
    "TORNADO": IconMapping("🌪", "@", "gray"),
    "MILKY_WAY": IconMapping("🌌", "(*)", "mediumpurple"),
    "GLOBE_SHOWING_EUROPE_AFRICA": IconMapping("🌍", "(@)", "green"),
}

# -----------------------------------------------------------------------------
# Plants
# -----------------------------------------------------------------------------
PLANT_ICONS: Final[dict[str, IconMapping]] = {
    "EVERGREEN_TREE": IconMapping("🌲", "(T)", "green"),
    "PALM": IconMapping("🌴", "(Y)", "green"),
    "CACTUS": IconMapping("🌵", "(|)", "green"),
    "SEEDLING": IconMapping("🌱", "(.)", "green"),
    "HERB": IconMapping("🌿", "(~)", "green"),
    "SHAMROCK": IconMapping("☘", "(*)", "green"),
    "FOUR_LEAF_CLOVER": IconMapping("🍀", "(+)", "green"),
    "CHERRY_BLOSSOM": IconMapping("🌸", "(*)", "lightpink"),
    "LEAF_FLUTTERING_IN_WIND": IconMapping("🍃", "~~", "green"),
    "MAPLE_LEAF": IconMapping("🍁", "(*)", "orangered"),  # autumn
}

# -----------------------------------------------------------------------------
# Food & Drink
# -----------------------------------------------------------------------------
FOOD_ICONS: Final[dict[str, IconMapping]] = {
    "PIZZA": IconMapping("🍕", "(>)", "darkorange"),
    "BURGER": IconMapping("🍔", "(=)", "saddlebrown"),
    "FRIES": IconMapping("🍟", "(|)", "yellow"),
    "COFFEE": IconMapping("☕", "(c)", "saddlebrown"),
    "BEER": IconMapping("🍺", "(U)", "gold"),
    "WINE": IconMapping("🍷", "(Y)", "darkred"),
    "COCKTAIL": IconMapping("🍹", "(Y)", None),
    "CAKE": IconMapping("🍰", "(^)", "lightpink"),
    "COOKIE": IconMapping("🍪", "(o)", "saddlebrown"),
    "TANGERINE": IconMapping("🍊", "(o)", "darkorange"),
    "GRAPES": IconMapping("🍇", "oo", "purple"),
    "WATERMELON": IconMapping("🍉", "[>", "green"),
    "CHESTNUT": IconMapping("🌰", "()", "saddlebrown"),
}

# -----------------------------------------------------------------------------
# People & Gestures
# -----------------------------------------------------------------------------
PEOPLE_ICONS: Final[dict[str, IconMapping]] = {
    "BUSTS_IN_SILHOUETTE": IconMapping("👥", "(PP)", None),
    "PERSON": IconMapping("👤", "(P)", None),
    "THUMBS_UP": IconMapping("👍", "(+)", "green"),
    "THUMBS_DOWN": IconMapping("👎", "(-)", "red"),
    "WAVING_HAND": IconMapping("👋", "(/)", None),
    "HANDS_UP": IconMapping("🙌", "(^^)", None),
    "CLAP": IconMapping("👏", "(*)", None),
    "MUSCLE": IconMapping("💪", "(!)", None),
}

# -----------------------------------------------------------------------------
# Arrows - No colors (use terminal default)
# -----------------------------------------------------------------------------
ARROW_ICONS: Final[dict[str, IconMapping]] = {
    # Basic arrows
    "ARROW_RIGHT": IconMapping("→", "->", None),
    "ARROW_LEFT": IconMapping("←", "<-", None),
    "ARROW_UP": IconMapping("↑", "^", None),
    "ARROW_DOWN": IconMapping("↓", "v", None),
    "UP_RIGHT_ARROW": IconMapping("↗", "/^", None),
    "ARROW_DOWN_RIGHT": IconMapping("↘", "\\v", None),
    "ARROW_DOWN_LEFT": IconMapping("↙", "/v", None),
    "ARROW_UP_LEFT": IconMapping("↖", "\\^", None),
    # Heavy arrows
    "HEAVY_RIGHT": IconMapping("➡", "==>", None),
    "HEAVY_LEFT": IconMapping("⬅", "<==", None),
    "HEAVY_UP": IconMapping("⬆", "^^", None),
    "HEAVY_DOWN": IconMapping("⬇", "vv", None),
}

# -----------------------------------------------------------------------------
# Symbols - Mixed utility icons
# -----------------------------------------------------------------------------
SYMBOL_ICONS: Final[dict[str, IconMapping]] = {
    "LIGHT_BULB": IconMapping("💡", "(!)", "yellow"),
    "BELL": IconMapping("🔔", "(b)", "yellow"),
    "POLICE_CAR_LIGHT": IconMapping("🚨", "(!)", "red"),
    "TRIANGULAR_RULER": IconMapping("📐", "(/)", None),
    "LOCKED": IconMapping("🔒", "(L)", "gray"),
    "UNLOCK": IconMapping("🔓", "(U)", "gray"),
    "KEY": IconMapping("🔑", "(k)", "gold"),
    "LINK": IconMapping("🔗", "(-)", "blue"),
    "CHAIN": IconMapping("⛓", "(-)", "gray"),
    "MAG": IconMapping("🔍", "(?)", None),
    "SHIELD": IconMapping("🛡", "(#)", "gray"),
    "CROWN": IconMapping("👑", "(^)", "gold"),
}

# -----------------------------------------------------------------------------
# Math & Logic
# -----------------------------------------------------------------------------
MATH_ICONS: Final[dict[str, IconMapping]] = {
    "PLUS": IconMapping("➕", "+", "green"),
    "MINUS": IconMapping("➖", "-", "red"),
    "MULTIPLY": IconMapping("✖️", "x", None),
    "DIVIDE": IconMapping("➗", "/", None),
    "EQUALS": IconMapping("🟰", "=", None),
}

# -----------------------------------------------------------------------------
# Hearts - Use appropriate colors
# -----------------------------------------------------------------------------
HEART_ICONS: Final[dict[str, IconMapping]] = {
    "RED_HEART": IconMapping("❤️", "<3", "red"),
    "ORANGE_HEART": IconMapping("🧡", "<3", "darkorange"),
    "YELLOW_HEART": IconMapping("💛", "<3", "yellow"),
    "GREEN_HEART": IconMapping("💚", "<3", "green"),
    "BLUE_HEART": IconMapping("💙", "<3", "blue"),
    "PURPLE_HEART": IconMapping("💜", "<3", "magenta"),
    "BROKEN_HEART": IconMapping("💔", "</3", "red"),
    "SPARKLING_HEART": IconMapping("💖", "<*>", "hotpink"),
    "GROWING_HEART": IconMapping("💗", "<3>", "hotpink"),
}

# -----------------------------------------------------------------------------
# Currency & Money
# -----------------------------------------------------------------------------
MONEY_ICONS: Final[dict[str, IconMapping]] = {
    "DOLLAR_BANKNOTE": IconMapping("💵", "($)", "green"),
    "MONEY_BAG": IconMapping("💰", "($)", "gold"),
    "COIN": IconMapping("🪙", "(o)", "gold"),
    "CREDIT_CARD": IconMapping("💳", "(=)", None),
    "GEM_STONE": IconMapping("💎", "<>", "cyan"),
}

# -----------------------------------------------------------------------------
# Time & Calendar
# -----------------------------------------------------------------------------
TIME_ICONS: Final[dict[str, IconMapping]] = {
    "ONE_OCLOCK": IconMapping("🕐", "(t)", None),
    "ALARM_CLOCK": IconMapping("⏰", "(!)", "red"),
    "STOPWATCH": IconMapping("⏱", "(t)", "cyan"),
    "TIMER": IconMapping("⏲", "(t)", "cyan"),
    "HOURGLASS_DONE": IconMapping("⌛", "(t)", None),
    "CALENDAR": IconMapping("📅", "(#)", None),
}

# -----------------------------------------------------------------------------
# Communication & Media
# -----------------------------------------------------------------------------
COMM_ICONS: Final[dict[str, IconMapping]] = {
    "MOBILE_PHONE": IconMapping("📱", "(p)", None),
    "TELEPHONE": IconMapping("☎️", "(p)", None),
    "E_MAIL": IconMapping("📧", "(@)", None),
    "ENVELOPE": IconMapping("✉️", "(_)", None),
    "MAILBOX": IconMapping("📬", "(M)", None),
    "SPEAKER": IconMapping("🔊", "(>)", None),
    "MEGAPHONE": IconMapping("📣", "(>)", None),
    "LOUDSPEAKER": IconMapping("📢", "(>)", None),
    "GLOBE_WITH_MERIDIANS": IconMapping("🌐", "(@)", "blue"),
}

# -----------------------------------------------------------------------------
# Buildings & Places
# -----------------------------------------------------------------------------
BUILDING_ICONS: Final[dict[str, IconMapping]] = {
    "HOME": IconMapping("🏠", "(H)", None),
    "OFFICE": IconMapping("🏢", "(O)", None),
    "FACTORY": IconMapping("🏭", "(F)", "gray"),
    "HOSPITAL": IconMapping("🏥", "(+)", "red"),
    "SCHOOL": IconMapping("🏫", "(S)", None),
    "BANK": IconMapping("🏦", "($)", None),
    "HOTEL": IconMapping("🏨", "(H)", None),
    "CASTLE": IconMapping("🏰", "(M)", None),
    "DESERT": IconMapping("🏜️", "(~)", "goldenrod"),
    "CLASSICAL_BUILDING": IconMapping("🏛", "(|)", None),
    "STADIUM": IconMapping("🏟", "(U)", None),
}

# -----------------------------------------------------------------------------
# Flags
# -----------------------------------------------------------------------------
FLAG_ICONS: Final[dict[str, IconMapping]] = {
    "FLAG_CHECKERED": IconMapping("🏁", "(F)", None),
    "FLAG_TRIANGULAR": IconMapping("🚩", "[>", "red"),
    "WHITE_FLAG": IconMapping("🏳", "(F)", None),
}

# -----------------------------------------------------------------------------
# Animals & Insects
# -----------------------------------------------------------------------------
ANIMAL_ICONS: Final[dict[str, IconMapping]] = {
    "BUTTERFLY": IconMapping("🦋", "(W)", "mediumpurple"),
    "BUG": IconMapping("🐛", "(b)", "green"),
    "BEE": IconMapping("🐝", "(b)", "yellow"),
    "LADY_BEETLE": IconMapping("🐞", "(b)", "red"),
    "SNAIL": IconMapping("🐌", "(@)", None),
    "TURTLE": IconMapping("🐢", "(T)", "green"),
}


# =============================================================================
# COMBINED REGISTRY - All icons in one place for lookup
# =============================================================================
def _build_icon_registry() -> dict[str, IconMapping]:
    """Build complete icon registry from all categories."""
    registry: dict[str, IconMapping] = {}

    # Add all category dictionaries
    categories = [
        STATUS_ICONS,
        STARS_ICONS,
        DOCUMENT_ICONS,
        BOOK_ICONS,
        TECH_ICONS,
        TOOLS_ICONS,
        ACTIVITY_ICONS,
        TRANSPORT_ICONS,
        WEATHER_ICONS,
        PLANT_ICONS,
        FOOD_ICONS,
        PEOPLE_ICONS,
        ARROW_ICONS,
        SYMBOL_ICONS,
        MATH_ICONS,
        HEART_ICONS,
        MONEY_ICONS,
        TIME_ICONS,
        COMM_ICONS,
        BUILDING_ICONS,
        FLAG_ICONS,
        ANIMAL_ICONS,
    ]

    for category in categories:
        registry.update(category)

    return registry


# Master registry - maps icon name to IconMapping
ICON_REGISTRY: Final[dict[str, IconMapping]] = _build_icon_registry()

# Reverse lookup - maps emoji to IconMapping (for runtime conversion)
EMOJI_TO_ICON: Final[dict[str, IconMapping]] = {
    mapping.emoji: mapping for mapping in ICON_REGISTRY.values()
}


__all__ = [
    "ACTIVITY_ICONS",
    "ANIMAL_ICONS",
    "ARROW_ICONS",
    "BOOK_ICONS",
    "BUILDING_ICONS",
    "COMM_ICONS",
    "DOCUMENT_ICONS",
    "EMOJI_TO_ICON",
    "FLAG_ICONS",
    "FOOD_ICONS",
    "HEART_ICONS",
    "ICON_REGISTRY",
    "MATH_ICONS",
    "MONEY_ICONS",
    "PEOPLE_ICONS",
    "PLANT_ICONS",
    "STARS_ICONS",
    # Category exports for reference
    "STATUS_ICONS",
    "SYMBOL_ICONS",
    "TECH_ICONS",
    "TIME_ICONS",
    "TOOLS_ICONS",
    "TRANSPORT_ICONS",
    "WEATHER_ICONS",
    "IconMapping",
]
