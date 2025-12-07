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

from styledconsole.emoji_registry import EMOJI


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
    "CHECK_MARK_BUTTON": IconMapping(EMOJI.CHECK_MARK_BUTTON, "(OK)", "green"),
    "CROSS_MARK": IconMapping(EMOJI.CROSS_MARK, "(FAIL)", "red"),
    "WARNING": IconMapping(EMOJI.WARNING, "(WARN)", "yellow"),
    "INFORMATION": IconMapping(EMOJI.INFORMATION, "(INFO)", "cyan"),
    "RED_QUESTION_MARK": IconMapping(EMOJI.RED_QUESTION_MARK, "(?)", "magenta"),
    "COUNTERCLOCKWISE_ARROWS_BUTTON": IconMapping(
        EMOJI.COUNTERCLOCKWISE_ARROWS_BUTTON, "(~)", "cyan"
    ),
    # Colored circles -> colored bullets
    "RED_CIRCLE": IconMapping(EMOJI.RED_CIRCLE, "●", "red"),
    "YELLOW_CIRCLE": IconMapping(EMOJI.YELLOW_CIRCLE, "●", "yellow"),
    "GREEN_CIRCLE": IconMapping(EMOJI.GREEN_CIRCLE, "●", "green"),
    "BLUE_CIRCLE": IconMapping(EMOJI.BLUE_CIRCLE, "●", "blue"),
    "PURPLE_CIRCLE": IconMapping(EMOJI.PURPLE_CIRCLE, "●", "magenta"),
    "ORANGE_CIRCLE": IconMapping(EMOJI.ORANGE_CIRCLE, "●", "darkorange"),
    "WHITE_CIRCLE": IconMapping(EMOJI.WHITE_CIRCLE, "○", None),
    "BLACK_CIRCLE": IconMapping(EMOJI.BLACK_CIRCLE, "●", None),
}

# -----------------------------------------------------------------------------
# Stars & Sparkles - Celebrations, highlights
# -----------------------------------------------------------------------------
STARS_ICONS: Final[dict[str, IconMapping]] = {
    "STAR": IconMapping(EMOJI.STAR, "*", "yellow"),
    "SPARKLES": IconMapping(EMOJI.SPARKLES, "**", "yellow"),
    "DIZZY": IconMapping(EMOJI.DIZZY, "*~", "yellow"),
    "GLOWING_STAR": IconMapping(EMOJI.GLOWING_STAR, "(*)", "yellow"),
}

# -----------------------------------------------------------------------------
# Documents & Data - Files, charts, storage
# -----------------------------------------------------------------------------
DOCUMENT_ICONS: Final[dict[str, IconMapping]] = {
    # Charts
    "BAR_CHART": IconMapping(EMOJI.BAR_CHART, "(#)", "blue"),
    "CHART_INCREASING": IconMapping(EMOJI.CHART_INCREASING, "(^)", "green"),
    "CHART_DECREASING": IconMapping(EMOJI.CHART_DECREASING, "(v)", "red"),
    "PACKAGE": IconMapping(EMOJI.PACKAGE, "(P)", "saddlebrown"),
    # Folders
    "FILE_FOLDER": IconMapping(EMOJI.FILE_FOLDER, "(/)", "blue"),
    "OPEN_FILE_FOLDER": IconMapping(EMOJI.OPEN_FILE_FOLDER, "(+)", "blue"),
    "FILE_CABINET": IconMapping(EMOJI.FILE_CABINET, "(=)", "gray"),
    "CARD_FILE_BOX": IconMapping(EMOJI.CARD_FILE_BOX, "(=)", "gray"),
    "WASTEBASKET": IconMapping(EMOJI.WASTEBASKET, "(x)", "gray"),
    # Files
    "PAGE_FACING_UP": IconMapping(EMOJI.PAGE_FACING_UP, "(f)", None),
    "PAGE_WITH_CURL": IconMapping(EMOJI.PAGE_WITH_CURL, "(d)", None),
    "SCROLL": IconMapping(EMOJI.SCROLL, "(s)", "goldenrod"),
    "MEMO": IconMapping(EMOJI.MEMO, "(m)", None),
    "CLIPBOARD": IconMapping(EMOJI.CLIPBOARD, "(c)", None),
    "PUSHPIN": IconMapping(EMOJI.PUSHPIN, "(*)", "red"),
    "PAPERCLIP": IconMapping(EMOJI.PAPERCLIP, "(-)", "gray"),
    "BOOKMARK": IconMapping(EMOJI.BOOKMARK, "(>)", "tomato"),
    "LABEL": IconMapping(EMOJI.LABEL, "(t)", None),
    "CARD_INDEX": IconMapping(EMOJI.CARD_INDEX, "(i)", None),
    "CONSTRUCTION": IconMapping(EMOJI.CONSTRUCTION, "(!!)", "yellow"),
}

# -----------------------------------------------------------------------------
# Books & Reading
# -----------------------------------------------------------------------------
BOOK_ICONS: Final[dict[str, IconMapping]] = {
    "OPEN_BOOK": IconMapping(EMOJI.OPEN_BOOK, "(B)", None),
    "BOOKS": IconMapping(EMOJI.BOOKS, "(BB)", None),
    "NOTEBOOK": IconMapping(EMOJI.NOTEBOOK, "(N)", None),
    "LEDGER": IconMapping(EMOJI.LEDGER, "(L)", "yellow"),
    "CLOSED_BOOK": IconMapping(EMOJI.CLOSED_BOOK, "(B)", "red"),
    "GREEN_BOOK": IconMapping(EMOJI.GREEN_BOOK, "(B)", "green"),
    "BLUE_BOOK": IconMapping(EMOJI.BLUE_BOOK, "(B)", "blue"),
    "ORANGE_BOOK": IconMapping(EMOJI.ORANGE_BOOK, "(B)", "darkorange"),
    "NEWSPAPER": IconMapping(EMOJI.NEWSPAPER, "(N)", None),
    "ROLLED_UP_NEWSPAPER": IconMapping(EMOJI.ROLLED_UP_NEWSPAPER, "(N)", None),
}

# -----------------------------------------------------------------------------
# Technology - Computers, devices
# -----------------------------------------------------------------------------
TECH_ICONS: Final[dict[str, IconMapping]] = {
    "LAPTOP": IconMapping(EMOJI.LAPTOP, "(PC)", None),
    "DESKTOP": IconMapping(EMOJI.DESKTOP_COMPUTER, "(PC)", None),
    "KEYBOARD": IconMapping(EMOJI.KEYBOARD, "(kb)", None),
    "MOUSE": IconMapping(EMOJI.MOUSE, "(m)", None),
    "FLOPPY_DISK": IconMapping(EMOJI.FLOPPY_DISK, "(D)", None),
    "CD": IconMapping(EMOJI.OPTICAL_DISK, "(O)", None),
    "DVD": IconMapping(EMOJI.DVD, "(O)", "gold"),
    "DESKTOP_COMPUTER": IconMapping(EMOJI.DESKTOP_COMPUTER, "(C)", None),
    "SATELLITE_ANTENNA": IconMapping(EMOJI.SATELLITE_ANTENNA, "(A)", None),
    "GLOBE_WITH_MERIDIANS": IconMapping(EMOJI.GLOBE_WITH_MERIDIANS, "(@)", "blue"),
}

# -----------------------------------------------------------------------------
# Tools & Science - Development, testing
# -----------------------------------------------------------------------------
TOOLS_ICONS: Final[dict[str, IconMapping]] = {
    "TEST_TUBE": IconMapping(EMOJI.TEST_TUBE, "(T)", "mediumpurple"),
    "MICROSCOPE": IconMapping(EMOJI.MICROSCOPE, "(M)", None),
    "TRIANGULAR_RULER": IconMapping(EMOJI.TRIANGULAR_RULER, "(/)", None),
    "WRENCH": IconMapping(EMOJI.WRENCH, "(w)", "gray"),
    "HAMMER": IconMapping(EMOJI.HAMMER, "(h)", "gray"),
    "GEAR": IconMapping(EMOJI.GEAR, "(*)", "gray"),
    "NUT_BOLT": IconMapping(EMOJI.NUT_AND_BOLT, "(o)", "gray"),
}

# -----------------------------------------------------------------------------
# Activities & Celebrations
# -----------------------------------------------------------------------------
ACTIVITY_ICONS: Final[dict[str, IconMapping]] = {
    "BULLSEYE": IconMapping(EMOJI.BULLSEYE, "(o)", "red"),
    "ARTIST_PALETTE": IconMapping(EMOJI.ARTIST_PALETTE, "(~)", None),
    "PAINTBRUSH": IconMapping(EMOJI.PAINTBRUSH, "(/)", None),
    "PARTY_POPPER": IconMapping(EMOJI.PARTY_POPPER, "(!)", "gold"),
    "CONFETTI_BALL": IconMapping(EMOJI.CONFETTI_BALL, "(!)", "gold"),
    "WRAPPED_GIFT": IconMapping(EMOJI.WRAPPED_GIFT, "(G)", "red"),
    "BALLOON": IconMapping(EMOJI.BALLOON, "o", "red"),
    "TROPHY": IconMapping(EMOJI.TROPHY, "(#)", "gold"),
    "MEDAL": IconMapping(EMOJI.SPORTS_MEDAL, "(m)", "gold"),
    "FIREWORKS": IconMapping(EMOJI.FIREWORKS, "(*)", "gold"),
    "CIRCUS_TENT": IconMapping(EMOJI.CIRCUS_TENT, "(^)", "red"),
    "PERFORMING_ARTS": IconMapping(EMOJI.PERFORMING_ARTS, "(:))", None),
}

# -----------------------------------------------------------------------------
# Transportation & Speed
# -----------------------------------------------------------------------------
TRANSPORT_ICONS: Final[dict[str, IconMapping]] = {
    "ROCKET": IconMapping(EMOJI.ROCKET, ">>>", "cyan"),
    "AIRPLANE": IconMapping(EMOJI.AIRPLANE, "->", None),
    "AUTOMOBILE": IconMapping(EMOJI.AUTOMOBILE, "(>)", "red"),
    "BIKE": IconMapping(EMOJI.BICYCLE, "(o)", None),
    "LOCOMOTIVE": IconMapping(EMOJI.LOCOMOTIVE, "(=)", None),
    "SHIP": IconMapping(EMOJI.SHIP, "(~)", None),
}

# -----------------------------------------------------------------------------
# Nature & Weather
# -----------------------------------------------------------------------------
WEATHER_ICONS: Final[dict[str, IconMapping]] = {
    "RAINBOW": IconMapping(EMOJI.RAINBOW, "(~)", None),  # No single color fits
    "SUN": IconMapping(EMOJI.SUN, "(O)", "yellow"),
    "SUNRISE": IconMapping(EMOJI.SUNRISE, "(^)", "darkorange"),
    "MOON": IconMapping(EMOJI.CRESCENT_MOON, "(C)", "yellow"),
    "DROPLET": IconMapping(EMOJI.DROPLET, "o", "blue"),
    "WATER_WAVE": IconMapping(EMOJI.WATER_WAVE, "~~~", "blue"),
    "FIRE": IconMapping(EMOJI.FIRE, "~", "orangered"),
    "SNOWFLAKE": IconMapping(EMOJI.SNOWFLAKE, "*", "cyan"),
    "CLOUD": IconMapping(EMOJI.CLOUD, "(~)", None),
    "HIGH_VOLTAGE": IconMapping(EMOJI.HIGH_VOLTAGE, "/\\", "yellow"),
    "TORNADO": IconMapping(EMOJI.TORNADO, "@", "gray"),
    "MILKY_WAY": IconMapping(EMOJI.MILKY_WAY, "(*)", "mediumpurple"),
    "GLOBE_SHOWING_EUROPE_AFRICA": IconMapping(EMOJI.GLOBE_SHOWING_EUROPE_AFRICA, "(@)", "green"),
}

# -----------------------------------------------------------------------------
# Plants
# -----------------------------------------------------------------------------
PLANT_ICONS: Final[dict[str, IconMapping]] = {
    "EVERGREEN_TREE": IconMapping(EMOJI.EVERGREEN_TREE, "(T)", "green"),
    "PALM": IconMapping(EMOJI.PALM_TREE, "(Y)", "green"),
    "CACTUS": IconMapping(EMOJI.CACTUS, "(|)", "green"),
    "SEEDLING": IconMapping(EMOJI.SEEDLING, "(.)", "green"),
    "HERB": IconMapping(EMOJI.HERB, "(~)", "green"),
    "SHAMROCK": IconMapping(EMOJI.SHAMROCK, "(*)", "green"),
    "FOUR_LEAF_CLOVER": IconMapping(EMOJI.FOUR_LEAF_CLOVER, "(+)", "green"),
    "CHERRY_BLOSSOM": IconMapping(EMOJI.CHERRY_BLOSSOM, "(*)", "lightpink"),
    "LEAF_FLUTTERING_IN_WIND": IconMapping(EMOJI.LEAF_FLUTTERING_IN_WIND, "~~", "green"),
    "MAPLE_LEAF": IconMapping(EMOJI.MAPLE_LEAF, "(*)", "orangered"),  # autumn
}

# -----------------------------------------------------------------------------
# Food & Drink
# -----------------------------------------------------------------------------
FOOD_ICONS: Final[dict[str, IconMapping]] = {
    "PIZZA": IconMapping(EMOJI.PIZZA, "(>)", "darkorange"),
    "BURGER": IconMapping(EMOJI.HAMBURGER, "(=)", "saddlebrown"),
    "FRIES": IconMapping(EMOJI.FRENCH_FRIES, "(|)", "yellow"),
    "COFFEE": IconMapping(EMOJI.HOT_BEVERAGE, "(c)", "saddlebrown"),
    "BEER": IconMapping(EMOJI.BEER_MUG, "(U)", "gold"),
    "WINE": IconMapping(EMOJI.WINE_GLASS, "(Y)", "darkred"),
    "COCKTAIL": IconMapping(EMOJI.TROPICAL_DRINK, "(Y)", None),
    "CAKE": IconMapping(EMOJI.SHORTCAKE, "(^)", "lightpink"),
    "COOKIE": IconMapping(EMOJI.COOKIE, "(o)", "saddlebrown"),
    "TANGERINE": IconMapping(EMOJI.TANGERINE, "(o)", "darkorange"),
    "GRAPES": IconMapping(EMOJI.GRAPES, "oo", "purple"),
    "WATERMELON": IconMapping(EMOJI.WATERMELON, "[>", "green"),
    "CHESTNUT": IconMapping(EMOJI.CHESTNUT, "()", "saddlebrown"),
}

# -----------------------------------------------------------------------------
# People & Gestures
# -----------------------------------------------------------------------------
PEOPLE_ICONS: Final[dict[str, IconMapping]] = {
    "BUSTS_IN_SILHOUETTE": IconMapping(EMOJI.BUSTS_IN_SILHOUETTE, "(PP)", None),
    "PERSON": IconMapping(EMOJI.PERSON, "(P)", None),
    "THUMBS_UP": IconMapping(EMOJI.THUMBS_UP, "(+)", "green"),
    "THUMBS_DOWN": IconMapping(EMOJI.THUMBS_DOWN, "(-)", "red"),
    "WAVING_HAND": IconMapping(EMOJI.WAVING_HAND, "(/)", None),
    "HANDS_UP": IconMapping(EMOJI.RAISING_HANDS, "(^^)", None),
    "CLAP": IconMapping(EMOJI.CLAPPING_HANDS, "(*)", None),
    "MUSCLE": IconMapping(EMOJI.FLEXED_BICEPS, "(!)", None),
}

# -----------------------------------------------------------------------------
# Arrows - No colors (use terminal default)
# -----------------------------------------------------------------------------
ARROW_ICONS: Final[dict[str, IconMapping]] = {
    # Basic arrows
    "ARROW_RIGHT": IconMapping(EMOJI.ARROW_RIGHT, "->", None),
    "ARROW_LEFT": IconMapping(EMOJI.ARROW_LEFT, "<-", None),
    "ARROW_UP": IconMapping(EMOJI.ARROW_UP, "^", None),
    "ARROW_DOWN": IconMapping(EMOJI.ARROW_DOWN, "v", None),
    "UP_RIGHT_ARROW": IconMapping(EMOJI.UP_RIGHT_ARROW, "/^", None),
    "ARROW_DOWN_RIGHT": IconMapping(EMOJI.DOWN_RIGHT_ARROW, "\\v", None),
    "ARROW_DOWN_LEFT": IconMapping(EMOJI.DOWN_LEFT_ARROW, "/v", None),
    "ARROW_UP_LEFT": IconMapping(EMOJI.UP_LEFT_ARROW, "\\^", None),
    # Heavy arrows
    "HEAVY_RIGHT": IconMapping(EMOJI.RIGHT_ARROW, "==>", None),
    "HEAVY_LEFT": IconMapping(EMOJI.LEFT_ARROW, "<==", None),
    "HEAVY_UP": IconMapping(EMOJI.UP_ARROW, "^^", None),
    "HEAVY_DOWN": IconMapping(EMOJI.DOWN_ARROW, "vv", None),
}

# -----------------------------------------------------------------------------
# Symbols - Mixed utility icons
# -----------------------------------------------------------------------------
SYMBOL_ICONS: Final[dict[str, IconMapping]] = {
    "LIGHT_BULB": IconMapping(EMOJI.LIGHT_BULB, "(!)", "yellow"),
    "BELL": IconMapping(EMOJI.BELL, "(b)", "yellow"),
    "POLICE_CAR_LIGHT": IconMapping(EMOJI.POLICE_CAR_LIGHT, "(!)", "red"),
    "TRIANGULAR_RULER": IconMapping(EMOJI.TRIANGULAR_RULER, "(/)", None),
    "LOCKED": IconMapping(EMOJI.LOCKED, "(L)", "gray"),
    "UNLOCK": IconMapping(EMOJI.UNLOCKED, "(U)", "gray"),
    "KEY": IconMapping(EMOJI.KEY, "(k)", "gold"),
    "LINK": IconMapping(EMOJI.LINK, "(-)", "blue"),
    "CHAIN": IconMapping(EMOJI.CHAINS, "(-)", "gray"),
    "MAG": IconMapping(EMOJI.MAGNIFYING_GLASS_TILTED_LEFT, "(?)", None),
    "SHIELD": IconMapping(EMOJI.SHIELD, "(#)", "gray"),
    "CROWN": IconMapping(EMOJI.CROWN, "(^)", "gold"),
}

# -----------------------------------------------------------------------------
# Math & Logic
# -----------------------------------------------------------------------------
MATH_ICONS: Final[dict[str, IconMapping]] = {
    "PLUS": IconMapping(EMOJI.PLUS, "+", "green"),
    "MINUS": IconMapping(EMOJI.MINUS, "-", "red"),
    "MULTIPLY": IconMapping(EMOJI.MULTIPLY, "x", None),
    "DIVIDE": IconMapping(EMOJI.DIVIDE, "/", None),
    "EQUALS": IconMapping(EMOJI.HEAVY_EQUALS_SIGN, "=", None),
}

# -----------------------------------------------------------------------------
# Hearts - Use appropriate colors
# -----------------------------------------------------------------------------
HEART_ICONS: Final[dict[str, IconMapping]] = {
    "RED_HEART": IconMapping(EMOJI.RED_HEART, "<3", "red"),
    "ORANGE_HEART": IconMapping(EMOJI.ORANGE_HEART, "<3", "darkorange"),
    "YELLOW_HEART": IconMapping(EMOJI.YELLOW_HEART, "<3", "yellow"),
    "GREEN_HEART": IconMapping(EMOJI.GREEN_HEART, "<3", "green"),
    "BLUE_HEART": IconMapping(EMOJI.BLUE_HEART, "<3", "blue"),
    "PURPLE_HEART": IconMapping(EMOJI.PURPLE_HEART, "<3", "magenta"),
    "BROKEN_HEART": IconMapping(EMOJI.BROKEN_HEART, "</3", "red"),
    "SPARKLING_HEART": IconMapping(EMOJI.SPARKLING_HEART, "<*>", "hotpink"),
    "GROWING_HEART": IconMapping(EMOJI.GROWING_HEART, "<3>", "hotpink"),
}

# -----------------------------------------------------------------------------
# Currency & Money
# -----------------------------------------------------------------------------
MONEY_ICONS: Final[dict[str, IconMapping]] = {
    "DOLLAR_BANKNOTE": IconMapping(EMOJI.DOLLAR_BANKNOTE, "($)", "green"),
    "MONEY_BAG": IconMapping(EMOJI.MONEY_BAG, "($)", "gold"),
    "COIN": IconMapping(EMOJI.COIN, "(o)", "gold"),
    "CREDIT_CARD": IconMapping(EMOJI.CREDIT_CARD, "(=)", None),
    "GEM_STONE": IconMapping(EMOJI.GEM_STONE, "<>", "cyan"),
}

# -----------------------------------------------------------------------------
# Time & Calendar
# -----------------------------------------------------------------------------
TIME_ICONS: Final[dict[str, IconMapping]] = {
    "ONE_OCLOCK": IconMapping(EMOJI.ONE_OCLOCK, "(t)", None),
    "ALARM_CLOCK": IconMapping(EMOJI.ALARM_CLOCK, "(!)", "red"),
    "STOPWATCH": IconMapping(EMOJI.STOPWATCH, "(t)", "cyan"),
    "TIMER": IconMapping(EMOJI.TIMER_CLOCK, "(t)", "cyan"),
    "HOURGLASS_DONE": IconMapping(EMOJI.HOURGLASS_DONE, "(t)", None),
    "HOURGLASS_NOT_DONE": IconMapping(EMOJI.HOURGLASS_NOT_DONE, "(...)", "cyan"),
    "CALENDAR": IconMapping(EMOJI.CALENDAR, "(#)", None),
}

# -----------------------------------------------------------------------------
# Communication & Media
# -----------------------------------------------------------------------------
COMM_ICONS: Final[dict[str, IconMapping]] = {
    "MOBILE_PHONE": IconMapping(EMOJI.MOBILE_PHONE, "(p)", None),
    "TELEPHONE": IconMapping(EMOJI.TELEPHONE, "(p)", None),
    "E_MAIL": IconMapping(EMOJI.E_MAIL, "(@)", None),
    "ENVELOPE": IconMapping(EMOJI.ENVELOPE, "(_)", None),
    "MAILBOX": IconMapping(EMOJI.OPEN_MAILBOX_WITH_RAISED_FLAG, "(M)", None),
    "SPEAKER": IconMapping(EMOJI.SPEAKER_HIGH_VOLUME, "(>)", None),
    "MEGAPHONE": IconMapping(EMOJI.MEGAPHONE, "(>)", None),
    "LOUDSPEAKER": IconMapping(EMOJI.LOUDSPEAKER, "(>)", None),
    "GLOBE_WITH_MERIDIANS": IconMapping(EMOJI.GLOBE_WITH_MERIDIANS, "(@)", "blue"),
}

# -----------------------------------------------------------------------------
# Buildings & Places
# -----------------------------------------------------------------------------
BUILDING_ICONS: Final[dict[str, IconMapping]] = {
    "HOME": IconMapping(EMOJI.HOUSE, "(H)", None),
    "OFFICE": IconMapping(EMOJI.OFFICE_BUILDING, "(O)", None),
    "FACTORY": IconMapping(EMOJI.FACTORY, "(F)", "gray"),
    "HOSPITAL": IconMapping(EMOJI.HOSPITAL, "(+)", "red"),
    "SCHOOL": IconMapping(EMOJI.SCHOOL, "(S)", None),
    "BANK": IconMapping(EMOJI.BANK, "($)", None),
    "HOTEL": IconMapping(EMOJI.HOTEL, "(H)", None),
    "CASTLE": IconMapping(EMOJI.CASTLE, "(M)", None),
    "DESERT": IconMapping(EMOJI.DESERT, "(~)", "goldenrod"),
    "CLASSICAL_BUILDING": IconMapping(EMOJI.CLASSICAL_BUILDING, "(|)", None),
    "STADIUM": IconMapping(EMOJI.STADIUM, "(U)", None),
}

# -----------------------------------------------------------------------------
# Flags
# -----------------------------------------------------------------------------
FLAG_ICONS: Final[dict[str, IconMapping]] = {
    "FLAG_CHECKERED": IconMapping(EMOJI.CHEQUERED_FLAG, "(F)", None),
    "FLAG_TRIANGULAR": IconMapping(EMOJI.TRIANGULAR_FLAG, "[>", "red"),
    "WHITE_FLAG": IconMapping(EMOJI.WHITE_FLAG, "(F)", None),
}

# -----------------------------------------------------------------------------
# Animals & Insects
# -----------------------------------------------------------------------------
ANIMAL_ICONS: Final[dict[str, IconMapping]] = {
    "BUTTERFLY": IconMapping(EMOJI.BUTTERFLY, "(W)", "mediumpurple"),
    "BUG": IconMapping(EMOJI.BUG, "(b)", "green"),
    "BEE": IconMapping(EMOJI.HONEYBEE, "(b)", "yellow"),
    "LADY_BEETLE": IconMapping(EMOJI.LADY_BEETLE, "(b)", "red"),
    "SNAIL": IconMapping(EMOJI.SNAIL, "(@)", None),
    "TURTLE": IconMapping(EMOJI.TURTLE, "(T)", "green"),
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
