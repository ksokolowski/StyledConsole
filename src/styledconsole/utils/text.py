"""Text width calculation and grapheme handling utilities.

This module provides emoji-safe text width calculation and grapheme manipulation.
MVP (v0.1) focuses on Tier 1 emoji support (single-codepoint basic icons).
"""

import re

import wcwidth

from styledconsole.types import AlignType

# ANSI escape sequence pattern (CSI sequences)
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")

# Emoji Variation Selector-16 (U+FE0F) forces emoji presentation
# Some terminals render these as width=1 instead of wcwidth's reported width=2
# This is a known terminal inconsistency
VARIATION_SELECTOR_16 = "\ufe0f"

# Tier 1 MVP: Basic single-codepoint emojis that are well-supported
# These are the 200+ common icons from EMOJI-STRATEGY.md Tier 1
TIER1_EMOJI_RANGES = [
    (0x2600, 0x26FF),  # Miscellaneous Symbols (☀️ ☁️ ⛄ ⚡ etc.)
    (0x2700, 0x27BF),  # Dingbats (✂️ ✅ ✈️ ✉️ ✏️ ✒️ etc.)
    (0x1F300, 0x1F5FF),  # Miscellaneous Symbols and Pictographs
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F680, 0x1F6FF),  # Transport and Map Symbols
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
]


def strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from text.

    Args:
        text: String potentially containing ANSI codes

    Returns:
        Text with ANSI codes removed

    Example:
        >>> strip_ansi("\\033[31mRed\\033[0m")
        'Red'
    """
    return ANSI_PATTERN.sub("", text)


def visual_width(text: str) -> int:
    """Calculate the visual display width of text.

    This function:
    1. Strips ANSI escape sequences
    2. Uses wcwidth for accurate Unicode width calculation
    3. Handles Tier 1 emojis correctly (width=2)
    4. Applies terminal-specific workarounds for variation selectors

    Known Issues:
    - Emoji Variation Selector-16 (U+FE0F) has inconsistent terminal support
    - Some terminals render "⚠️" (warning + VS16) as width=1, not width=2
    - wcwidth reports width=2 but actual display may be width=1
    - This affects: ⚠️ ℹ️ and other symbol+VS16 combinations

    Workaround: We detect character+VS16 patterns and calculate width based
    on the base character only, since many terminals ignore the VS16 width.

    Note: Tier 2 (skin tones) and Tier 3 (ZWJ sequences) will be
    addressed in future versions (v0.2+).

    Args:
        text: String to measure (may contain ANSI codes, emojis, etc.)

    Returns:
        Visual width in terminal columns

    Example:
        >>> visual_width("Hello")
        5
        >>> visual_width("🚀")
        2
        >>> visual_width("Test 🚀 🎉")
        11
        >>> visual_width("\\033[31mRed\\033[0m")
        3
        >>> visual_width("⚠️")  # Warning sign + variation selector
        1
        >>> visual_width("⚠️  Warning")
        11
    """
    # Strip ANSI codes first
    clean_text = strip_ansi(text)

    # Workaround for variation selector emoji rendering inconsistency
    # Many terminals render base_char + VS16 with the width of base_char only
    # This fixes alignment for ⚠️, ℹ️, etc.
    if VARIATION_SELECTOR_16 in clean_text:
        # Calculate width character by character, treating VS16 sequences specially
        width = 0
        i = 0
        while i < len(clean_text):
            # Check if next character is VS16
            if i + 1 < len(clean_text) and clean_text[i + 1] == VARIATION_SELECTOR_16:
                # This is a char + VS16 combination
                # Use only the base character's width (many terminals ignore VS16)
                base_char = clean_text[i]
                char_width = wcwidth.wcwidth(base_char)
                width += char_width if char_width > 0 else 1
                i += 2  # Skip both base char and VS16
            else:
                # Regular character
                char_width = wcwidth.wcwidth(clean_text[i])
                width += char_width if char_width > 0 else 1
                i += 1
        return width

    # Standard path: use wcwidth for accurate width calculation
    # wcwidth handles emojis, wide characters, zero-width, etc.
    width = wcwidth.wcswidth(clean_text)

    # wcswidth returns -1 if string contains non-printable characters
    # Fall back to character count in that case
    if width == -1:
        # Count characters, treating common emojis as width=2
        width = 0
        for char in clean_text:
            char_width = wcwidth.wcwidth(char)
            if char_width == -1:
                # Unknown character, assume width=1
                width += 1
            else:
                width += char_width

    return width


def split_graphemes(text: str) -> list[str]:
    """Split text into grapheme clusters.

    For MVP (v0.1), this is a simplified implementation that handles:
    - Regular ASCII characters
    - Tier 1 single-codepoint emojis
    - ANSI codes are preserved with adjacent characters

    Future versions will handle grapheme clusters properly using
    unicode segmentation rules.

    Args:
        text: Text to split into graphemes

    Returns:
        List of grapheme strings

    Example:
        >>> split_graphemes("Hello")
        ['H', 'e', 'l', 'l', 'o']
        >>> split_graphemes("Hi 🚀")
        ['H', 'i', ' ', '🚀']
    """
    graphemes = []
    i = 0
    text_len = len(text)

    while i < text_len:
        # Check for ANSI escape sequence
        if text[i] == "\x1b" and i + 1 < text_len and text[i + 1] == "[":
            # Find the end of the ANSI sequence
            end = i + 2
            while end < text_len and not text[end].isalpha():
                end += 1
            if end < text_len:
                end += 1
            # ANSI sequence found, attach to previous grapheme if exists
            ansi_code = text[i:end]
            if graphemes:
                graphemes[-1] += ansi_code
            else:
                graphemes.append(ansi_code)
            i = end
            continue

        # Regular character or emoji
        graphemes.append(text[i])
        i += 1

    return graphemes


def pad_to_width(
    text: str,
    width: int,
    align: AlignType = "left",
    fill_char: str = " ",
) -> str:
    """Pad text to a specific visual width.

    Takes into account the actual visual width of text (including emojis)
    and pads accordingly.

    Args:
        text: Text to pad
        width: Target visual width
        align: Alignment ("left", "center", or "right")
        fill_char: Character to use for padding (default: space)

    Returns:
        Padded text with exact visual width

    Example:
        >>> pad_to_width("Hi", 5, "left")
        'Hi   '
        >>> pad_to_width("🚀", 4, "left")
        '🚀  '
        >>> pad_to_width("X", 5, "center")
        '  X  '
        >>> pad_to_width("✅", 6, "center")
        '  ✅  '

    Raises:
        ValueError: If text is already wider than target width
    """
    current_width = visual_width(text)

    if current_width > width:
        raise ValueError(f"Text width ({current_width}) exceeds target width ({width})")

    padding_needed = width - current_width

    if align == "left":
        return text + (fill_char * padding_needed)
    elif align == "right":
        return (fill_char * padding_needed) + text
    elif align == "center":
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        return (fill_char * left_pad) + text + (fill_char * right_pad)
    else:
        raise ValueError(f"Invalid align value: {align}")


def truncate_to_width(text: str, width: int, suffix: str = "...") -> str:
    """Truncate text to fit within a specific visual width.

    ANSI escape codes are preserved in the output.

    Args:
        text: Text to truncate (may contain ANSI codes)
        width: Maximum visual width
        suffix: Suffix to append when truncating (default: "...")

    Returns:
        Truncated text with suffix if needed, preserving ANSI codes

    Example:
        >>> truncate_to_width("Hello World", 8)
        'Hello...'
        >>> truncate_to_width("Hi", 10)
        'Hi'
        >>> truncate_to_width("🚀 Rocket", 5)
        '🚀...'
    """
    current_width = visual_width(text)

    if current_width <= width:
        return text

    suffix_width = visual_width(suffix)
    target_width = width - suffix_width

    if target_width <= 0:
        # Not enough space for suffix, just truncate
        return suffix[:width] if len(suffix) > 0 else ""

    # If text has no ANSI codes, use simple truncation
    if "\x1b" not in text:
        # Build truncated string character by character
        result = []
        accumulated_width = 0

        for char in text:
            char_width = wcwidth.wcwidth(char)
            if char_width == -1:
                char_width = 1

            if accumulated_width + char_width > target_width:
                break

            result.append(char)
            accumulated_width += char_width

        return "".join(result) + suffix

    # Text has ANSI codes - need to preserve them
    # Split text into ANSI codes and visible characters
    parts = ANSI_PATTERN.split(text)
    ansi_codes = ANSI_PATTERN.findall(text)

    # Reconstruct text while tracking visible width
    result = []
    accumulated_width = 0
    part_idx = 0
    ansi_idx = 0

    while part_idx < len(parts):
        # Add visible text from this part
        part = parts[part_idx]
        for char in part:
            char_width = wcwidth.wcwidth(char)
            if char_width == -1:
                char_width = 1

            if accumulated_width + char_width > target_width:
                # Add suffix and any trailing ANSI reset codes
                result.append(suffix)
                # Add reset code if text had any ANSI codes
                if ansi_codes:
                    result.append("\x1b[0m")
                return "".join(result)

            result.append(char)
            accumulated_width += char_width

        part_idx += 1

        # Add ANSI code if there is one after this part
        if ansi_idx < len(ansi_codes):
            result.append(ansi_codes[ansi_idx])
            ansi_idx += 1

    # Shouldn't reach here, but just in case
    return "".join(result) + suffix


def normalize_content(content: str | list[str]) -> list[str]:
    """Normalize content to list of lines.

    Args:
        content: String or list of strings

    Returns:
        List of lines (empty content becomes [""])

    Example:
        >>> normalize_content("Line 1\\nLine 2")
        ['Line 1', 'Line 2']
        >>> normalize_content(["Line 1", "Line 2"])
        ['Line 1', 'Line 2']
        >>> normalize_content("")
        ['']
        >>> normalize_content([])
        ['']
    """
    if isinstance(content, str):
        return content.splitlines() if content else [""]
    else:
        return content if content else [""]


# Safe emoji list - tested and verified for reliable width calculation and rendering
# These are Tier 1 emojis (single codepoint) that work correctly across terminals
SAFE_EMOJIS = {
    # Status & Indicators
    "✅": {"name": "check_mark", "width": 2, "category": "status"},
    "❌": {"name": "cross_mark", "width": 2, "category": "status"},
    "⚠️": {"name": "warning", "width": 2, "category": "status", "has_vs16": True},
    "ℹ️": {"name": "info", "width": 2, "category": "status", "has_vs16": True},
    "🔴": {"name": "red_circle", "width": 2, "category": "status"},
    "🟡": {"name": "yellow_circle", "width": 2, "category": "status"},
    "🟢": {"name": "green_circle", "width": 2, "category": "status"},
    "🔵": {"name": "blue_circle", "width": 2, "category": "status"},
    # Progress & Activity
    "⏭️": {"name": "next_track", "width": 2, "category": "progress"},
    "⏸️": {"name": "pause", "width": 2, "category": "progress"},
    "⏹️": {"name": "stop", "width": 2, "category": "progress"},
    "▶️": {"name": "play", "width": 2, "category": "progress"},
    "⏩": {"name": "fast_forward", "width": 2, "category": "progress"},
    "⏪": {"name": "rewind", "width": 2, "category": "progress"},
    # Arrows & Direction
    "➡️": {"name": "right_arrow", "width": 2, "category": "direction", "has_vs16": True},
    "⬅️": {"name": "left_arrow", "width": 2, "category": "direction"},
    "⬆️": {"name": "up_arrow", "width": 2, "category": "direction"},
    "⬇️": {"name": "down_arrow", "width": 2, "category": "direction"},
    "↗️": {"name": "northeast_arrow", "width": 2, "category": "direction"},
    "↘️": {"name": "southeast_arrow", "width": 2, "category": "direction"},
    "↙️": {"name": "southwest_arrow", "width": 2, "category": "direction"},
    "↖️": {"name": "northwest_arrow", "width": 2, "category": "direction"},
    "🔃": {"name": "repeat", "width": 2, "category": "direction"},
    "🔄": {"name": "refresh", "width": 2, "category": "direction"},
    # Tech & Objects
    "💻": {"name": "laptop", "width": 2, "category": "tech"},
    "🖥️": {"name": "desktop", "width": 2, "category": "tech", "has_vs16": True},
    "⌨️": {"name": "keyboard", "width": 2, "category": "tech"},
    "🖱️": {"name": "mouse", "width": 2, "category": "tech", "has_vs16": True},
    "💾": {"name": "floppy_disk", "width": 2, "category": "tech"},
    "💿": {"name": "cd", "width": 2, "category": "tech"},
    "🔧": {"name": "wrench", "width": 2, "category": "tech"},
    "🔨": {"name": "hammer", "width": 2, "category": "tech"},
    "⚙️": {"name": "gear", "width": 2, "category": "tech"},
    "🚀": {"name": "rocket", "width": 2, "category": "tech"},
    "📦": {"name": "package", "width": 2, "category": "tech"},
    "📁": {"name": "folder", "width": 2, "category": "tech"},
    "📂": {"name": "open_folder", "width": 2, "category": "tech"},
    "📄": {"name": "page", "width": 2, "category": "tech"},
    "📝": {"name": "memo", "width": 2, "category": "tech"},
    "📋": {"name": "clipboard", "width": 2, "category": "tech"},
    # Data & Charts
    "📊": {"name": "bar_chart", "width": 2, "category": "data"},
    "📈": {"name": "chart_up", "width": 2, "category": "data"},
    "📉": {"name": "chart_down", "width": 2, "category": "data"},
    # Nature & Weather
    "🌈": {"name": "rainbow", "width": 2, "category": "nature"},
    "☀️": {"name": "sun", "width": 2, "category": "nature"},
    "🌙": {"name": "moon", "width": 2, "category": "nature"},
    "⭐": {"name": "star", "width": 2, "category": "nature"},
    "✨": {"name": "sparkles", "width": 2, "category": "nature"},
    "💫": {"name": "dizzy", "width": 2, "category": "nature"},
    "🌟": {"name": "glowing_star", "width": 2, "category": "nature"},
    "💧": {"name": "droplet", "width": 2, "category": "nature"},
    "❄️": {"name": "snowflake", "width": 2, "category": "nature"},
    "☔": {"name": "umbrella", "width": 2, "category": "nature"},
    "⚡": {"name": "lightning", "width": 2, "category": "nature"},
    "🔥": {"name": "fire", "width": 2, "category": "nature"},
    # Food & Drink
    "🍕": {"name": "pizza", "width": 2, "category": "food"},
    "🍔": {"name": "hamburger", "width": 2, "category": "food"},
    "🍟": {"name": "fries", "width": 2, "category": "food"},
    "☕": {"name": "coffee", "width": 2, "category": "food"},
    "🍺": {"name": "beer", "width": 2, "category": "food"},
    "🍪": {"name": "cookie", "width": 2, "category": "food"},
    # Fun & Activities
    "🎉": {"name": "party", "width": 2, "category": "activity"},
    "🎊": {"name": "confetti", "width": 2, "category": "activity"},
    "🎁": {"name": "gift", "width": 2, "category": "activity"},
    "🎯": {"name": "target", "width": 2, "category": "activity"},
    "🎨": {"name": "artist", "width": 2, "category": "activity"},
    "🎭": {"name": "theater", "width": 2, "category": "activity"},
    "🎮": {"name": "game", "width": 2, "category": "activity"},
    "🏆": {"name": "trophy", "width": 2, "category": "activity"},
    # Hand Gestures (Simple)
    "👍": {"name": "thumbs_up", "width": 2, "category": "hand"},
    "👎": {"name": "thumbs_down", "width": 2, "category": "hand"},
    "👋": {"name": "wave", "width": 2, "category": "hand"},
    "🙌": {"name": "raising_hands", "width": 2, "category": "hand"},
    "🤝": {"name": "handshake", "width": 2, "category": "hand"},
    "✋": {"name": "raised_hand", "width": 2, "category": "hand"},
    "✌️": {"name": "peace", "width": 2, "category": "hand"},
    # Others
    "❤️": {"name": "heart", "width": 2, "category": "other"},
    "💡": {"name": "lightbulb", "width": 2, "category": "other"},
    "💎": {"name": "gem", "width": 2, "category": "other"},
    "🔑": {"name": "key", "width": 2, "category": "other"},
    "🎓": {"name": "graduation", "width": 2, "category": "other"},
    "🚗": {"name": "car", "width": 2, "category": "other"},
    "✏️": {"name": "pencil", "width": 2, "category": "other"},
}


def validate_emoji(emoji: str) -> dict:
    """Validate an emoji for safe usage in StyledConsole.

    Checks if emoji is in the safe list and returns detailed information
    about its properties and any known issues.

    Args:
        emoji: Single emoji character or emoji+variation selector sequence

    Returns:
        Dictionary with keys:
        - 'safe': bool - Whether emoji is in safe list
        - 'name': str - Human-readable name if safe
        - 'width': int - Display width (1 or 2)
        - 'category': str - Category if safe
        - 'has_vs16': bool - Whether emoji includes variation selector
        - 'recommendation': str - Any warnings or recommendations

    Example:
        >>> result = validate_emoji("✅")
        >>> result['safe']
        True
        >>> result['width']
        2

        >>> result = validate_emoji("👨‍💻")
        >>> result['safe']
        False
        >>> "ZWJ" in result['recommendation']
        True

        >>> result = validate_emoji("🖥️")
        >>> result['has_vs16']
        True
    """
    result = {
        "safe": False,
        "name": None,
        "width": None,
        "category": None,
        "has_vs16": False,
        "recommendation": "Unknown emoji",
    }

    # Check if in safe list
    if emoji in SAFE_EMOJIS:
        info = SAFE_EMOJIS[emoji]
        result.update(
            {
                "safe": True,
                "name": info.get("name", "unknown"),
                "width": info.get("width", 2),
                "category": info.get("category", "other"),
                "has_vs16": info.get("has_vs16", False),
                "recommendation": "✅ Safe to use",
            }
        )
        if result["has_vs16"]:
            result["recommendation"] += " (includes variation selector)"
        return result

    # Check for ZWJ sequences
    if "\u200d" in emoji:  # Zero-Width Joiner
        result["recommendation"] = (
            "❌ ZWJ sequence detected. These are not supported in v0.1. "
            "Use simple single-codepoint emojis instead."
        )
        return result

    # Check for variation selectors
    if VARIATION_SELECTOR_16 in emoji:
        result["recommendation"] = (
            "⚠️ Variation selector (U+FE0F) detected. "
            "This emoji may not be in the tested safe list. "
            "Try removing the variation selector if alignment issues occur."
        )
        return result

    # Check for skin tone modifiers (Tier 2)
    if any(0x1F3FB <= ord(c) <= 0x1F3FF for c in emoji):
        result["recommendation"] = (
            "❌ Skin tone modifier detected. "
            "Tier 2 emojis are not supported in v0.1. "
            "Use base emoji without skin tone."
        )
        return result

    # Fallback
    result["recommendation"] = (
        "❓ Unknown emoji. Not in safe list. Use at your own risk - may have alignment issues."
    )
    return result


def get_safe_emojis(category: str | None = None) -> dict:
    """Get safe emojis, optionally filtered by category.

    Args:
        category: Optional category name to filter by
                 (e.g., 'status', 'tech', 'nature', 'food', 'activity')
                 If None, returns all safe emojis.

    Returns:
        Dictionary of emoji -> info mappings

    Example:
        >>> status_emojis = get_safe_emojis("status")
        >>> "✅" in status_emojis
        True
        >>> len(get_safe_emojis())
        > 80
    """
    if category is None:
        return SAFE_EMOJIS.copy()

    return {emoji: info for emoji, info in SAFE_EMOJIS.items() if info.get("category") == category}


def get_emoji_spacing_adjustment(emoji: str) -> int:
    """Get the number of extra spaces needed after an emoji for proper alignment.

    This function detects when an emoji's reported visual width doesn't match
    its actual terminal display width (due to grapheme cluster compositions
    and terminal rendering inconsistencies) and returns the adjustment needed.

    The detection logic:
    1. Checks if emoji is in safe list
    2. Compares emoji's grapheme_count with visual_width() result
    3. Returns adjustment if: grapheme_count > 1 AND visual_width < metadata width

    This handles both explicit VS16 cases and other multi-part emoji sequences.

    Args:
        emoji: Single emoji or emoji+modifiers sequence

    Returns:
        Number of extra spaces to add after emoji:
        - 0: No adjustment needed (emoji width calculated correctly)
        - 1: Add 1 extra space (common for VS16 emojis)
        - 2: Add 2 extra spaces (edge cases)

    Example:
        >>> get_emoji_spacing_adjustment("✅")  # Standard emoji
        0
        >>> get_emoji_spacing_adjustment("⚠️")  # VS16 emoji (warning)
        1
        >>> get_emoji_spacing_adjustment("➡️")  # Variation selector arrow
        1
        >>> get_emoji_spacing_adjustment("↖️")  # Multi-grapheme no VS16
        1

    Raises:
        ValueError: If emoji is not in safe list
    """
    if emoji not in SAFE_EMOJIS:
        raise ValueError(
            f"Emoji {repr(emoji)} not in safe list. "
            f"Use validate_emoji() to check unsupported emojis."
        )

    # Get emoji metadata
    info = SAFE_EMOJIS[emoji]
    metadata_width = info.get("width", 2)

    # Calculate actual grapheme count
    grapheme_count = len(split_graphemes(emoji))

    # Calculate visual width reported by wcwidth
    actual_visual_width = visual_width(emoji)

    # Determine if spacing adjustment is needed
    # If emoji has multiple graphemes but visual_width is less than metadata width,
    # there's a mismatch that needs compensation
    if grapheme_count > 1 and actual_visual_width < metadata_width:
        # Calculate how much adjustment is needed
        adjustment = metadata_width - actual_visual_width
        return min(adjustment, 2)  # Cap at 2 extra spaces

    return 0


def format_emoji_with_spacing(emoji: str, text: str = "", sep: str = " ") -> str:
    """Format emoji with automatic spacing adjustment.

    This is a convenience function that combines emoji with text, automatically
    adding the correct number of spaces between them to prevent visual gluing.

    Args:
        emoji: Emoji character(s) from safe list
        text: Optional text to append after emoji
        sep: Base separator between emoji and text (default: single space)

    Returns:
        Formatted string with emoji and text, properly spaced

    Example:
        >>> format_emoji_with_spacing("✅", "Success")
        '✅ Success'
        >>> format_emoji_with_spacing("⚠️", "Warning")
        '⚠️  Warning'  # Extra space for VS16
        >>> format_emoji_with_spacing("➡️", "Next")
        '➡️  Next'
        >>> format_emoji_with_spacing("↖️", "Back")
        '↖️  Back'

    Raises:
        ValueError: If emoji not in safe list
    """
    if not text:
        return emoji

    adjustment = get_emoji_spacing_adjustment(emoji)
    total_spaces = len(sep) + adjustment

    return emoji + (" " * total_spaces) + text


__all__ = [
    "visual_width",
    "strip_ansi",
    "split_graphemes",
    "pad_to_width",
    "truncate_to_width",
    "normalize_content",
    "validate_emoji",
    "get_safe_emojis",
    "get_emoji_spacing_adjustment",
    "format_emoji_with_spacing",
    "SAFE_EMOJIS",
    "AlignType",
]
