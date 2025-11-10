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
    4. Applies a VS16 workaround: many terminals render base_char+VS16 with the
       width of the base character only.

    Args:
        text: String to measure (may contain ANSI codes, emojis, etc.)

    Returns:
        Visual width in terminal columns
    """
    # Strip ANSI codes first
    clean_text = strip_ansi(text)

    # Special-case VS16 sequences: treat base+VS16 as width of base char
    if VARIATION_SELECTOR_16 in clean_text:
        width = 0
        i = 0
        n = len(clean_text)
        while i < n:
            # If next codepoint is VS16, measure base only and skip VS16
            if i + 1 < n and clean_text[i + 1] == VARIATION_SELECTOR_16:
                base = clean_text[i]
                w = wcwidth.wcwidth(base)
                width += w if w > 0 else 1
                i += 2
            else:
                w = wcwidth.wcwidth(clean_text[i])
                width += w if w > 0 else 1
                i += 1
        return width

    # Standard path
    width = wcwidth.wcswidth(clean_text)
    if width == -1:
        # Fallback to per-char accumulation
        width = 0
        for ch in clean_text:
            w = wcwidth.wcwidth(ch)
            width += w if w >= 0 else 1
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


def _truncate_plain_text(text: str, target_width: int, suffix: str) -> str:
    """Truncate text without ANSI codes."""
    result = []
    accumulated_width = 0

    for char in text:
        char_width = wcwidth.wcwidth(char) if wcwidth.wcwidth(char) != -1 else 1

        if accumulated_width + char_width > target_width:
            break

        result.append(char)
        accumulated_width += char_width

    return "".join(result) + suffix


def _truncate_ansi_text(text: str, target_width: int, suffix: str) -> str:
    """Truncate text with ANSI codes, preserving them."""
    parts = ANSI_PATTERN.split(text)
    ansi_codes = ANSI_PATTERN.findall(text)

    result = []
    accumulated_width = 0
    part_idx = 0
    ansi_idx = 0

    while part_idx < len(parts):
        part = parts[part_idx]

        for char in part:
            char_width = wcwidth.wcwidth(char) if wcwidth.wcwidth(char) != -1 else 1

            if accumulated_width + char_width > target_width:
                result.append(suffix)
                if ansi_codes:
                    result.append("\x1b[0m")  # Reset code
                return "".join(result)

            result.append(char)
            accumulated_width += char_width

        part_idx += 1

        # Add ANSI code if there is one after this part
        if ansi_idx < len(ansi_codes):
            result.append(ansi_codes[ansi_idx])
            ansi_idx += 1

    return "".join(result) + suffix


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
        return suffix[:width] if len(suffix) > 0 else ""

    # Dispatch to appropriate truncation strategy
    if "\x1b" not in text:
        return _truncate_plain_text(text, target_width, suffix)
    else:
        return _truncate_ansi_text(text, target_width, suffix)


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


def _collect_vs16_emojis() -> set[str]:
    """Collect SAFE_EMOJIS that use VS16 (variation selector).

    Returns:
        Set of emojis considered likely to glue in some terminals.
    """
    vs16_set: set[str] = set()
    for e, info in SAFE_EMOJIS.items():
        if info.get("has_vs16") or VARIATION_SELECTOR_16 in e:
            vs16_set.add(e)
    return vs16_set


def _assume_vs16_enabled() -> bool:
    """Determine if we should assume VS16 emojis glue by default.

    Controlled via env var STYLEDCONSOLE_ASSUME_VS16:
      - "0"/"false" (any case) disables the assumption
      - "1"/"true" enables the assumption
      - unset: defaults to enabled (pragmatic default for VS Code terminals)
    """
    import os as _os

    val = _os.getenv("STYLEDCONSOLE_ASSUME_VS16")
    if val is None:
        return True
    val_lower = str(val).lower().strip()
    if val_lower in ("", "0", "false", "no"):  # explicit off
        return False
    return True


def default_gluing_emojis() -> set[str]:
    """Default set of emojis to adjust when gluing_emojis is not provided.

    By default (and unless explicitly disabled via STYLEDCONSOLE_ASSUME_VS16=0),
    we assume VS16 emojis may glue in common terminals and return that set.
    """
    return _collect_vs16_emojis() if _assume_vs16_enabled() else set()


def adjust_emoji_spacing_in_text(
    text: str,
    separator: str = " ",
    *,
    gluing_emojis: set[str] | None = None,
) -> str:
    """Adjust spacing after emojis inside arbitrary text.

    Scans the string for occurrences of SAFE_EMOJIS and ensures the number of
    spaces after each emoji matches what :func:`get_emoji_spacing_adjustment`
    recommends. This makes the function:
      - Idempotent: running it multiple times won't add extra spaces
      - Conservative: only adjusts when exactly one separator is found and
        an adjustment > 0 is required

    Limitations:
      - Only handles simple patterns: ``<emoji><separator><non-space>``
      - Does not attempt to cross ANSI sequences inserted between emoji and
        the following text (rare in practice for titles)

    Args:
        text: Arbitrary string (may contain multiple emojis)
        separator: The base separator to normalize (default: single space)
        gluing_emojis: Optional set of emojis to adjust. When provided, only
            emojis in this set will be adjusted. If None, no adjustments are
            applied by default. This prevents over-adjusting VS16 emojis that
            don't glue in the current terminal/font.

    Returns:
        Text with spacing after emojis adjusted where needed.

    Examples:
        >>> adjust_emoji_spacing_in_text("⚙️ Services")
        '⚙️  Services'
        >>> adjust_emoji_spacing_in_text("⚠️ Warning")
        '⚠️ Warning'
        >>> adjust_emoji_spacing_in_text("✅ Done")
        '✅ Done'
    """
    if not text or separator == "":
        return text

    # Determine which emojis to consider
    targets: set[str]
    if gluing_emojis is None:
        # Use library default assumption (can be disabled via env)
        targets = default_gluing_emojis()
    else:
        targets = set(gluing_emojis)

    if not targets:
        return text

    # Quick path: if none of the target emojis are present, return early
    if not any(e in text for e in targets):
        return text

    # Regex-based replacement: match any target emoji followed by exactly one
    # separator and then a non-space (lookahead). This avoids over-adjusting
    # already-correct double-spacing and is resilient to multiple emojis.
    import re as _re

    alt = "|".join(_re.escape(e) for e in sorted(targets, key=len, reverse=True))
    pattern = _re.compile(rf"(?P<emo>{alt}){_re.escape(separator)}(?=\S)")

    def _compute_adjustment(emo: str) -> int:
        if emo in SAFE_EMOJIS:
            try:
                return max(0, min(2, get_emoji_spacing_adjustment(emo)))
            except Exception:
                return 0
        return 1 if VARIATION_SELECTOR_16 in emo else 0

    def _repl(m: "_re.Match[str]") -> str:
        emo = m.group("emo")
        adj = _compute_adjustment(emo)
        if adj <= 0:
            return m.group(0)
        return emo + (separator * (1 + adj))

    return pattern.sub(_repl, text)


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
    "adjust_emoji_spacing_in_text",
    "default_gluing_emojis",
    "SAFE_EMOJIS",
    "AlignType",
]
