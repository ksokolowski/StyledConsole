"""Text width calculation and grapheme handling utilities.

This module provides emoji-safe text width calculation and grapheme manipulation.
MVP (v0.1) focuses on Tier 1 emoji support (single-codepoint basic icons).
"""

import re

import wcwidth
from rich.text import Text as RichText

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


def render_markup_to_ansi(text: str) -> str:
    """Convert Rich markup to ANSI escape codes.

    This function takes a string containing Rich markup tags like [bold], [red],
    [italic], etc. and converts them to actual ANSI escape sequences.

    Args:
        text: String potentially containing Rich markup tags

    Returns:
        Text with markup converted to ANSI codes

    Example:
        >>> render_markup_to_ansi("[bold]Hello[/]")
        '\\x1b[1mHello\\x1b[0m'
    """
    from io import StringIO

    from rich.console import Console as RichConsole

    # Use a temporary console to render the markup
    buffer = StringIO()
    temp_console = RichConsole(file=buffer, force_terminal=True, no_color=False, width=10000)
    temp_console.print(text, end="", highlight=False)
    return buffer.getvalue()


def _is_legacy_emoji_mode() -> bool:
    """Check if legacy emoji mode is enabled via environment variable.

    Legacy mode supports terminals that do not correctly render ZWJ sequences
    or skin tone modifiers as single glyphs, but instead display them as
    separate characters (e.g. '👋' + '🏻').
    """
    import os

    val = os.getenv("STYLEDCONSOLE_LEGACY_EMOJI", "").lower()
    return val in ("1", "true", "yes", "on")


def visual_width(text: str, markup: bool = False) -> int:
    """Calculate the visual display width of text.

    This function:
    1. Strips ANSI escape sequences
    2. Splits text into graphemes using robust logic
    3. Calculates width for each grapheme:
       - ZWJ sequences -> Width 2 (or sum of parts in legacy mode)
       - VS16 sequences -> Width 1 (Terminal renders as 1, not wcwidth's 2)
       - Others -> wcwidth
    """
    # Strip ANSI codes first
    clean_text = strip_ansi(text)

    if markup:
        try:
            # Parse markup to get plain text for width calculation
            # We use Rich to strip tags and handle entities
            clean_text = RichText.from_markup(clean_text).plain
        except Exception:
            # Fallback if markup parsing fails
            pass

    # Split into graphemes to handle complex sequences correctly
    graphemes = split_graphemes(clean_text)

    legacy_mode = _is_legacy_emoji_mode()
    width = 0

    for g in graphemes:
        if legacy_mode and (len(g) > 1 or any(0x1F3FB <= ord(c) <= 0x1F3FF for c in g)):
            # Legacy Mode: Calculate width as sum of parts
            # This handles terminals that split ZWJ sequences and skin tones
            g_width = 0
            for char in g:
                # Force skin tone modifiers to width 2 in legacy mode
                # (wcwidth reports 0, but legacy terminals render as 2)
                if 0x1F3FB <= ord(char) <= 0x1F3FF:
                    g_width += 2
                # Ignore VS16 in legacy calculation (usually invisible or width 0)
                elif char == VARIATION_SELECTOR_16:
                    continue
                # Ignore ZWJ in legacy calculation (width 0)
                elif char == "\u200d":
                    continue
                else:
                    w = wcwidth.wcwidth(char)
                    g_width += w if w >= 0 else 1
            width += g_width

        elif "\u200d" in g:
            # Standard Mode: ZWJ sequences are always treated as width 2
            width += 2
        elif VARIATION_SELECTOR_16 in g:
            # VS16 emojis: Terminals render as width 1, not wcwidth's 2
            # This is a known terminal inconsistency we must account for
            width += 1
        else:
            # Standard path for single chars or simple sequences
            w = wcwidth.wcswidth(g)
            if w >= 0:
                width += w
            else:
                # Fallback if wcwidth fails (treat as 1)
                width += 1

    return width


def split_graphemes(text: str) -> list[str]:
    """Split text into grapheme clusters.

    Handles:
    - Regular ASCII characters
    - ANSI escape sequences (kept with preceding content or standalone)
    - ZWJ sequences (e.g. 👨‍💻)
    - VS16 sequences (e.g. ⚠️)
    - Skin tone modifiers (e.g. 👋🏻)
    """
    graphemes = []
    current_grapheme = ""
    i = 0
    n = len(text)

    while i < n:
        # Check for ANSI escape sequence
        if text[i] == "\x1b" and i + 1 < n and text[i + 1] == "[":
            # Find the end of the ANSI sequence
            end = i + 2
            while end < n and not text[end].isalpha():
                end += 1
            if end < n:
                end += 1

            ansi_code = text[i:end]

            # If we are building a grapheme, attach ANSI to it?
            # Or treat ANSI as zero-width non-breaking?
            # Existing logic attached it to previous.
            # Let's attach to current if exists, else start new.
            if current_grapheme:
                current_grapheme += ansi_code
            else:
                if graphemes:
                    graphemes[-1] += ansi_code
                else:
                    graphemes.append(ansi_code)

            i = end
            continue

        char = text[i]

        # Start of new grapheme
        if not current_grapheme:
            current_grapheme = char
            i += 1
            continue

        # Check if we should extend the current grapheme
        prev_char = current_grapheme[-1]

        # VS16 (Variation Selector-16) extends previous
        if char == VARIATION_SELECTOR_16:
            current_grapheme += char
            i += 1
            continue

        # ZWJ (Zero Width Joiner) extends previous
        if char == "\u200d":
            current_grapheme += char
            i += 1
            continue

        # If previous was ZWJ, this char extends it (emoji sequence)
        if prev_char == "\u200d":
            current_grapheme += char
            i += 1
            continue

        # Skin tone modifiers (U+1F3FB to U+1F3FF)
        if 0x1F3FB <= ord(char) <= 0x1F3FF:
            current_grapheme += char
            i += 1
            continue

        # Otherwise, start new grapheme
        graphemes.append(current_grapheme)
        current_grapheme = char
        i += 1

    if current_grapheme:
        graphemes.append(current_grapheme)

    return graphemes


def pad_to_width(
    text: str,
    width: int,
    align: AlignType = "left",
    fill_char: str = " ",
    markup: bool = False,
) -> str:
    """Pad text to a specific visual width.

    Takes into account the actual visual width of text (including emojis)
    and pads accordingly.

    Args:
        text: Text to pad
        width: Target visual width
        align: Alignment ("left", "center", or "right")
        fill_char: Character to use for padding (default: space)
        markup: Whether to handle Rich markup tags (default: False)

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
    current_width = visual_width(text, markup=markup)

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


def truncate_to_width(text: str, width: int, suffix: str = "...", markup: bool = False) -> str:
    """Truncate text to fit within a specific visual width.

    ANSI escape codes are preserved in the output.

    Args:
        text: Text to truncate (may contain ANSI codes)
        width: Maximum visual width
        suffix: Suffix to append when truncating (default: "...")
        markup: Whether to handle Rich markup tags (default: False)

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
    current_width = visual_width(text, markup=markup)
    if current_width <= width:
        return text

    if markup:
        try:
            # Use Rich for markup-aware truncation
            rt = RichText.from_markup(text)

            # Calculate target width for content
            suffix_width = visual_width(suffix, markup=markup)
            target_width = max(0, width - suffix_width)

            # Truncate using Rich (crop to make room for suffix)
            rt.truncate(target_width, overflow="crop", pad=False)
            return rt.markup + suffix
        except Exception:
            # Fallback to standard truncation if parsing fails
            pass

    suffix_width = visual_width(suffix, markup=markup)
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
        content: String or list of strings (items may contain newlines)

    Returns:
        List of lines (empty content becomes [""])

    Example:
        >>> normalize_content("Line 1\\nLine 2")
        ['Line 1', 'Line 2']
        >>> normalize_content(["Line 1", "Line 2"])
        ['Line 1', 'Line 2']
        >>> normalize_content(["Header", "Line 1\\nLine 2"])
        ['Header', 'Line 1', 'Line 2']
        >>> normalize_content("")
        ['']
        >>> normalize_content([])
        ['']
    """
    if isinstance(content, str):
        return content.splitlines() if content else [""]
    else:
        if not content:
            return [""]
        # Flatten list items that contain newlines
        result = []
        for item in content:
            if "\n" in item:
                result.extend(item.splitlines())
            else:
                result.append(item)
        return result


# Safe emoji list - tested and verified for reliable width calculation and rendering
# These are Tier 1 emojis (single codepoint) that work correctly across terminals
#
# VS16 EMOJIS WARNING:
# VS16 emojis (with variation selector U+FE0F) have TERMINAL RENDERING ISSUES.
# While visual_width() correctly returns 2, many terminals (including VS Code)
# render them as width 1, causing misalignment. Use non-VS16 alternatives when
# alignment is critical. VS16 emojis are included for completeness but marked
# with has_vs16=True and terminal_safe=False.
#
# ZWJ SEQUENCES WARNING:
# ZWJ (Zero Width Joiner) sequences like 👨‍💻 are NOT supported.
# Most terminals render them as multiple separate emojis instead of one
# combined glyph. These are explicitly excluded from SAFE_EMOJIS.
#
SAFE_EMOJIS = {
    # ========================================================================
    # VS16 Emojis (with Variation Selector-16 U+FE0F)
    # WARNING: These have inconsistent terminal rendering - use with caution!
    # Many terminals render these as width 1 instead of 2, causing misalignment.
    # ========================================================================
    "⚠️": {
        "name": "warning_sign",
        "width": 2,
        "category": "status",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "ℹ️": {
        "name": "information_source",
        "width": 2,
        "category": "status",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "❤️": {
        "name": "red_heart",
        "width": 2,
        "category": "symbols",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "⚙️": {"name": "gear", "width": 2, "category": "misc", "has_vs16": True, "terminal_safe": False},
    "☀️": {
        "name": "sun",
        "width": 2,
        "category": "nature",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "☁️": {
        "name": "cloud",
        "width": 2,
        "category": "nature",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "❄️": {
        "name": "snowflake",
        "width": 2,
        "category": "nature",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "✈️": {
        "name": "airplane",
        "width": 2,
        "category": "transport",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "✉️": {
        "name": "envelope",
        "width": 2,
        "category": "misc",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "✏️": {
        "name": "pencil",
        "width": 2,
        "category": "misc",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "✒️": {
        "name": "black_nib",
        "width": 2,
        "category": "misc",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "✔️": {
        "name": "heavy_check_mark",
        "width": 2,
        "category": "status",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "✖️": {
        "name": "heavy_multiplication_x",
        "width": 2,
        "category": "misc",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "☎️": {
        "name": "telephone",
        "width": 2,
        "category": "misc",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "🖌️": {
        "name": "paintbrush",
        "width": 2,
        "category": "misc",
        "has_vs16": True,
        "terminal_safe": False,
    },
    "🖍️": {
        "name": "crayon",
        "width": 2,
        "category": "misc",
        "has_vs16": True,
        "terminal_safe": False,
    },
    # ========================================================================
    # Standard single-codepoint emojis (no VS16) - TERMINAL SAFE
    # ========================================================================
    "⏰": {"name": "alarm_clock", "width": 2, "category": "misc", "has_vs16": False},
    "⌛": {"name": "hourglass", "width": 2, "category": "misc", "has_vs16": False},
    "⌚": {"name": "watch", "width": 2, "category": "misc", "has_vs16": False},
    "⭐": {"name": "white_medium_star", "width": 2, "category": "misc", "has_vs16": False},
    "☔": {"name": "umbrella_with_rain_drops", "width": 2, "category": "misc"},
    "☕": {"name": "hot_beverage", "width": 2, "category": "misc"},
    "☰": {"name": "trigram_for_heaven", "width": 2, "category": "misc"},
    "☱": {"name": "trigram_for_lake", "width": 2, "category": "misc"},
    "☲": {"name": "trigram_for_fire", "width": 2, "category": "misc"},
    "☳": {"name": "trigram_for_thunder", "width": 2, "category": "misc"},
    "☴": {"name": "trigram_for_wind", "width": 2, "category": "misc"},
    "☵": {"name": "trigram_for_water", "width": 2, "category": "misc"},
    "☶": {"name": "trigram_for_mountain", "width": 2, "category": "misc"},
    "☷": {"name": "trigram_for_earth", "width": 2, "category": "misc"},
    "♈": {"name": "aries", "width": 2, "category": "misc"},
    "♉": {"name": "taurus", "width": 2, "category": "misc"},
    "♊": {"name": "gemini", "width": 2, "category": "misc"},
    "♋": {"name": "cancer", "width": 2, "category": "misc"},
    "♌": {"name": "leo", "width": 2, "category": "misc"},
    "♍": {"name": "virgo", "width": 2, "category": "misc"},
    "♎": {"name": "libra", "width": 2, "category": "misc"},
    "♏": {"name": "scorpius", "width": 2, "category": "misc"},
    "♐": {"name": "sagittarius", "width": 2, "category": "misc"},
    "♑": {"name": "capricorn", "width": 2, "category": "misc"},
    "♒": {"name": "aquarius", "width": 2, "category": "misc"},
    "♓": {"name": "pisces", "width": 2, "category": "misc"},
    "♿": {"name": "wheelchair_symbol", "width": 2, "category": "misc"},
    "⚊": {"name": "monogram_for_yang", "width": 2, "category": "misc"},
    "⚋": {"name": "monogram_for_yin", "width": 2, "category": "misc"},
    "⚌": {"name": "digram_for_greater_yang", "width": 2, "category": "misc"},
    "⚍": {"name": "digram_for_lesser_yin", "width": 2, "category": "misc"},
    "⚎": {"name": "digram_for_lesser_yang", "width": 2, "category": "misc"},
    "⚏": {"name": "digram_for_greater_yin", "width": 2, "category": "misc"},
    "⚓": {"name": "anchor", "width": 2, "category": "misc"},
    "⚡": {"name": "high_voltage_sign", "width": 2, "category": "misc"},
    "⚪": {"name": "medium_white_circle", "width": 2, "category": "misc"},
    "⚫": {"name": "medium_black_circle", "width": 2, "category": "misc"},
    "⚽": {"name": "soccer_ball", "width": 2, "category": "misc"},
    "⚾": {"name": "baseball", "width": 2, "category": "misc"},
    "⛄": {"name": "snowman_without_snow", "width": 2, "category": "misc"},
    "⛅": {"name": "sun_behind_cloud", "width": 2, "category": "misc"},
    "⛎": {"name": "ophiuchus", "width": 2, "category": "misc"},
    "⛔": {"name": "no_entry", "width": 2, "category": "misc"},
    "⛪": {"name": "church", "width": 2, "category": "misc"},
    "⛲": {"name": "fountain", "width": 2, "category": "misc"},
    "⛳": {"name": "flag_in_hole", "width": 2, "category": "misc"},
    "⛵": {"name": "sailboat", "width": 2, "category": "misc"},
    "⛺": {"name": "tent", "width": 2, "category": "misc"},
    "⛽": {"name": "fuel_pump", "width": 2, "category": "misc"},
    "✅": {"name": "white_heavy_check_mark", "width": 2, "category": "dingbats"},
    "✊": {"name": "raised_fist", "width": 2, "category": "dingbats"},
    "✋": {"name": "raised_hand", "width": 2, "category": "dingbats"},
    "✨": {"name": "sparkles", "width": 2, "category": "dingbats"},
    "❌": {"name": "cross_mark", "width": 2, "category": "dingbats"},
    "❎": {"name": "negative_squared_cross_mark", "width": 2, "category": "dingbats"},
    "❓": {"name": "black_question_mark_ornament", "width": 2, "category": "dingbats"},
    "❔": {"name": "white_question_mark_ornament", "width": 2, "category": "dingbats"},
    "❕": {"name": "white_exclamation_mark_ornament", "width": 2, "category": "dingbats"},
    "❗": {"name": "heavy_exclamation_mark_symbol", "width": 2, "category": "dingbats"},
    "➕": {"name": "heavy_plus_sign", "width": 2, "category": "dingbats"},
    "➖": {"name": "heavy_minus_sign", "width": 2, "category": "dingbats"},
    "➗": {"name": "heavy_division_sign", "width": 2, "category": "dingbats"},
    "➰": {"name": "curly_loop", "width": 2, "category": "dingbats"},
    "➿": {"name": "double_curly_loop", "width": 2, "category": "dingbats"},
    "🌀": {"name": "cyclone", "width": 2, "category": "symbols"},
    "🌁": {"name": "foggy", "width": 2, "category": "symbols"},
    "🌂": {"name": "closed_umbrella", "width": 2, "category": "symbols"},
    "🌃": {"name": "night_with_stars", "width": 2, "category": "symbols"},
    "🌄": {"name": "sunrise_over_mountains", "width": 2, "category": "symbols"},
    "🌅": {"name": "sunrise", "width": 2, "category": "symbols"},
    "🌆": {"name": "cityscape_at_dusk", "width": 2, "category": "symbols"},
    "🌇": {"name": "sunset_over_buildings", "width": 2, "category": "symbols"},
    "🌈": {"name": "rainbow", "width": 2, "category": "symbols"},
    "🌉": {"name": "bridge_at_night", "width": 2, "category": "symbols"},
    "🌊": {"name": "water_wave", "width": 2, "category": "symbols"},
    "🌋": {"name": "volcano", "width": 2, "category": "symbols"},
    "🌌": {"name": "milky_way", "width": 2, "category": "symbols"},
    "🌍": {"name": "earth_globe_europe_africa", "width": 2, "category": "symbols"},
    "🌎": {"name": "earth_globe_americas", "width": 2, "category": "symbols"},
    "🌏": {"name": "earth_globe_asia_australia", "width": 2, "category": "symbols"},
    "🌐": {"name": "globe_with_meridians", "width": 2, "category": "symbols"},
    "🌑": {"name": "new_moon_symbol", "width": 2, "category": "symbols"},
    "🌒": {"name": "waxing_crescent_moon_symbol", "width": 2, "category": "symbols"},
    "🌓": {"name": "first_quarter_moon_symbol", "width": 2, "category": "symbols"},
    "🌔": {"name": "waxing_gibbous_moon_symbol", "width": 2, "category": "symbols"},
    "🌕": {"name": "full_moon_symbol", "width": 2, "category": "symbols"},
    "🌖": {"name": "waning_gibbous_moon_symbol", "width": 2, "category": "symbols"},
    "🌗": {"name": "last_quarter_moon_symbol", "width": 2, "category": "symbols"},
    "🌘": {"name": "waning_crescent_moon_symbol", "width": 2, "category": "symbols"},
    "🌙": {"name": "crescent_moon", "width": 2, "category": "symbols"},
    "🌚": {"name": "new_moon_with_face", "width": 2, "category": "symbols"},
    "🌛": {"name": "first_quarter_moon_with_face", "width": 2, "category": "symbols"},
    "🌜": {"name": "last_quarter_moon_with_face", "width": 2, "category": "symbols"},
    "🌝": {"name": "full_moon_with_face", "width": 2, "category": "symbols"},
    "🌞": {"name": "sun_with_face", "width": 2, "category": "symbols"},
    "🌟": {"name": "glowing_star", "width": 2, "category": "symbols"},
    "🌠": {"name": "shooting_star", "width": 2, "category": "symbols"},
    "🌭": {"name": "hot_dog", "width": 2, "category": "symbols"},
    "🌮": {"name": "taco", "width": 2, "category": "symbols"},
    "🌯": {"name": "burrito", "width": 2, "category": "symbols"},
    "🌰": {"name": "chestnut", "width": 2, "category": "symbols"},
    "🌱": {"name": "seedling", "width": 2, "category": "symbols"},
    "🌲": {"name": "evergreen_tree", "width": 2, "category": "symbols"},
    "🌳": {"name": "deciduous_tree", "width": 2, "category": "symbols"},
    "🌴": {"name": "palm_tree", "width": 2, "category": "symbols"},
    "🌵": {"name": "cactus", "width": 2, "category": "symbols"},
    "🌷": {"name": "tulip", "width": 2, "category": "symbols"},
    "🌸": {"name": "cherry_blossom", "width": 2, "category": "symbols"},
    "🌹": {"name": "rose", "width": 2, "category": "symbols"},
    "🌺": {"name": "hibiscus", "width": 2, "category": "symbols"},
    "🌻": {"name": "sunflower", "width": 2, "category": "symbols"},
    "🌼": {"name": "blossom", "width": 2, "category": "symbols"},
    "🌽": {"name": "ear_of_maize", "width": 2, "category": "symbols"},
    "🌾": {"name": "ear_of_rice", "width": 2, "category": "symbols"},
    "🌿": {"name": "herb", "width": 2, "category": "symbols"},
    "🍀": {"name": "four_leaf_clover", "width": 2, "category": "symbols"},
    "🍁": {"name": "maple_leaf", "width": 2, "category": "symbols"},
    "🍂": {"name": "fallen_leaf", "width": 2, "category": "symbols"},
    "🍃": {"name": "leaf_fluttering_in_wind", "width": 2, "category": "symbols"},
    "🍄": {"name": "mushroom", "width": 2, "category": "symbols"},
    "🍅": {"name": "tomato", "width": 2, "category": "symbols"},
    "🍆": {"name": "aubergine", "width": 2, "category": "symbols"},
    "🍇": {"name": "grapes", "width": 2, "category": "symbols"},
    "🍈": {"name": "melon", "width": 2, "category": "symbols"},
    "🍉": {"name": "watermelon", "width": 2, "category": "symbols"},
    "🍊": {"name": "tangerine", "width": 2, "category": "symbols"},
    "🍋": {"name": "lemon", "width": 2, "category": "symbols"},
    "🍌": {"name": "banana", "width": 2, "category": "symbols"},
    "🍍": {"name": "pineapple", "width": 2, "category": "symbols"},
    "🍎": {"name": "red_apple", "width": 2, "category": "symbols"},
    "🍏": {"name": "green_apple", "width": 2, "category": "symbols"},
    "🍐": {"name": "pear", "width": 2, "category": "symbols"},
    "🍑": {"name": "peach", "width": 2, "category": "symbols"},
    "🍒": {"name": "cherries", "width": 2, "category": "symbols"},
    "🍓": {"name": "strawberry", "width": 2, "category": "symbols"},
    "🍔": {"name": "hamburger", "width": 2, "category": "symbols"},
    "🍕": {"name": "slice_of_pizza", "width": 2, "category": "symbols"},
    "🍖": {"name": "meat_on_bone", "width": 2, "category": "symbols"},
    "🍗": {"name": "poultry_leg", "width": 2, "category": "symbols"},
    "🍘": {"name": "rice_cracker", "width": 2, "category": "symbols"},
    "🍙": {"name": "rice_ball", "width": 2, "category": "symbols"},
    "🍚": {"name": "cooked_rice", "width": 2, "category": "symbols"},
    "🍛": {"name": "curry_and_rice", "width": 2, "category": "symbols"},
    "🍜": {"name": "steaming_bowl", "width": 2, "category": "symbols"},
    "🍝": {"name": "spaghetti", "width": 2, "category": "symbols"},
    "🍞": {"name": "bread", "width": 2, "category": "symbols"},
    "🍟": {"name": "french_fries", "width": 2, "category": "symbols"},
    "🍠": {"name": "roasted_sweet_potato", "width": 2, "category": "symbols"},
    "🍡": {"name": "dango", "width": 2, "category": "symbols"},
    "🍢": {"name": "oden", "width": 2, "category": "symbols"},
    "🍣": {"name": "sushi", "width": 2, "category": "symbols"},
    "🍤": {"name": "fried_shrimp", "width": 2, "category": "symbols"},
    "🍥": {"name": "fish_cake_with_swirl_design", "width": 2, "category": "symbols"},
    "🍦": {"name": "soft_ice_cream", "width": 2, "category": "symbols"},
    "🍧": {"name": "shaved_ice", "width": 2, "category": "symbols"},
    "🍨": {"name": "ice_cream", "width": 2, "category": "symbols"},
    "🍩": {"name": "doughnut", "width": 2, "category": "symbols"},
    "🍪": {"name": "cookie", "width": 2, "category": "symbols"},
    "🍫": {"name": "chocolate_bar", "width": 2, "category": "symbols"},
    "🍬": {"name": "candy", "width": 2, "category": "symbols"},
    "🍭": {"name": "lollipop", "width": 2, "category": "symbols"},
    "🍮": {"name": "custard", "width": 2, "category": "symbols"},
    "🍯": {"name": "honey_pot", "width": 2, "category": "symbols"},
    "🍰": {"name": "shortcake", "width": 2, "category": "symbols"},
    "🍱": {"name": "bento_box", "width": 2, "category": "symbols"},
    "🍲": {"name": "pot_of_food", "width": 2, "category": "symbols"},
    "🍳": {"name": "cooking", "width": 2, "category": "symbols"},
    "🍴": {"name": "fork_and_knife", "width": 2, "category": "symbols"},
    "🍵": {"name": "teacup_without_handle", "width": 2, "category": "symbols"},
    "🍶": {"name": "sake_bottle_and_cup", "width": 2, "category": "symbols"},
    "🍷": {"name": "wine_glass", "width": 2, "category": "symbols"},
    "🍸": {"name": "cocktail_glass", "width": 2, "category": "symbols"},
    "🍹": {"name": "tropical_drink", "width": 2, "category": "symbols"},
    "🍺": {"name": "beer_mug", "width": 2, "category": "symbols"},
    "🍻": {"name": "clinking_beer_mugs", "width": 2, "category": "symbols"},
    "🍼": {"name": "baby_bottle", "width": 2, "category": "symbols"},
    "🍾": {"name": "bottle_with_popping_cork", "width": 2, "category": "symbols"},
    "🍿": {"name": "popcorn", "width": 2, "category": "symbols"},
    "🎀": {"name": "ribbon", "width": 2, "category": "symbols"},
    "🎁": {"name": "wrapped_present", "width": 2, "category": "symbols"},
    "🎂": {"name": "birthday_cake", "width": 2, "category": "symbols"},
    "🎃": {"name": "jack_o_lantern", "width": 2, "category": "symbols"},
    "🎄": {"name": "christmas_tree", "width": 2, "category": "symbols"},
    "🎅": {"name": "father_christmas", "width": 2, "category": "symbols"},
    "🎆": {"name": "fireworks", "width": 2, "category": "symbols"},
    "🎇": {"name": "firework_sparkler", "width": 2, "category": "symbols"},
    "🎈": {"name": "balloon", "width": 2, "category": "symbols"},
    "🎉": {"name": "party_popper", "width": 2, "category": "symbols"},
    "🎊": {"name": "confetti_ball", "width": 2, "category": "symbols"},
    "🎋": {"name": "tanabata_tree", "width": 2, "category": "symbols"},
    "🎌": {"name": "crossed_flags", "width": 2, "category": "symbols"},
    "🎍": {"name": "pine_decoration", "width": 2, "category": "symbols"},
    "🎎": {"name": "japanese_dolls", "width": 2, "category": "symbols"},
    "🎏": {"name": "carp_streamer", "width": 2, "category": "symbols"},
    "🎐": {"name": "wind_chime", "width": 2, "category": "symbols"},
    "🎑": {"name": "moon_viewing_ceremony", "width": 2, "category": "symbols"},
    "🎒": {"name": "school_satchel", "width": 2, "category": "symbols"},
    "🎓": {"name": "graduation_cap", "width": 2, "category": "symbols"},
    "🎠": {"name": "carousel_horse", "width": 2, "category": "symbols"},
    "🎡": {"name": "ferris_wheel", "width": 2, "category": "symbols"},
    "🎢": {"name": "roller_coaster", "width": 2, "category": "symbols"},
    "🎣": {"name": "fishing_pole_and_fish", "width": 2, "category": "symbols"},
    "🎤": {"name": "microphone", "width": 2, "category": "symbols"},
    "🎥": {"name": "movie_camera", "width": 2, "category": "symbols"},
    "🎦": {"name": "cinema", "width": 2, "category": "symbols"},
    "🎧": {"name": "headphone", "width": 2, "category": "symbols"},
    "🎨": {"name": "artist_palette", "width": 2, "category": "symbols"},
    "🎩": {"name": "top_hat", "width": 2, "category": "symbols"},
    "🎪": {"name": "circus_tent", "width": 2, "category": "symbols"},
    "🎫": {"name": "ticket", "width": 2, "category": "symbols"},
    "🎬": {"name": "clapper_board", "width": 2, "category": "symbols"},
    "🎭": {"name": "performing_arts", "width": 2, "category": "symbols"},
    "🎮": {"name": "video_game", "width": 2, "category": "symbols"},
    "🎯": {"name": "direct_hit", "width": 2, "category": "symbols"},
    "🎰": {"name": "slot_machine", "width": 2, "category": "symbols"},
    "🎱": {"name": "billiards", "width": 2, "category": "symbols"},
    "🎲": {"name": "game_die", "width": 2, "category": "symbols"},
    "🎳": {"name": "bowling", "width": 2, "category": "symbols"},
    "🎴": {"name": "flower_playing_cards", "width": 2, "category": "symbols"},
    "🎵": {"name": "musical_note", "width": 2, "category": "symbols"},
    "🎶": {"name": "multiple_musical_notes", "width": 2, "category": "symbols"},
    "🎷": {"name": "saxophone", "width": 2, "category": "symbols"},
    "🎸": {"name": "guitar", "width": 2, "category": "symbols"},
    "🎹": {"name": "musical_keyboard", "width": 2, "category": "symbols"},
    "🎺": {"name": "trumpet", "width": 2, "category": "symbols"},
    "🎻": {"name": "violin", "width": 2, "category": "symbols"},
    "🎼": {"name": "musical_score", "width": 2, "category": "symbols"},
    "🎽": {"name": "running_shirt_with_sash", "width": 2, "category": "symbols"},
    "🎾": {"name": "tennis_racquet_and_ball", "width": 2, "category": "symbols"},
    "🎿": {"name": "ski_and_ski_boot", "width": 2, "category": "symbols"},
    "🏀": {"name": "basketball_and_hoop", "width": 2, "category": "symbols"},
    "🏁": {"name": "chequered_flag", "width": 2, "category": "symbols"},
    "🏂": {"name": "snowboarder", "width": 2, "category": "symbols"},
    "🏃": {"name": "runner", "width": 2, "category": "symbols"},
    "🏄": {"name": "surfer", "width": 2, "category": "symbols"},
    "🏅": {"name": "sports_medal", "width": 2, "category": "symbols"},
    "🏆": {"name": "trophy", "width": 2, "category": "symbols"},
    "🏇": {"name": "horse_racing", "width": 2, "category": "symbols"},
    "🏈": {"name": "american_football", "width": 2, "category": "symbols"},
    "🏉": {"name": "rugby_football", "width": 2, "category": "symbols"},
    "🏊": {"name": "swimmer", "width": 2, "category": "symbols"},
    "🏏": {"name": "cricket_bat_and_ball", "width": 2, "category": "symbols"},
    "🏐": {"name": "volleyball", "width": 2, "category": "symbols"},
    "🏑": {"name": "field_hockey_stick_and_ball", "width": 2, "category": "symbols"},
    "🏒": {"name": "ice_hockey_stick_and_puck", "width": 2, "category": "symbols"},
    "🏓": {"name": "table_tennis_paddle_and_ball", "width": 2, "category": "symbols"},
    "🏠": {"name": "house_building", "width": 2, "category": "symbols"},
    "🏡": {"name": "house_with_garden", "width": 2, "category": "symbols"},
    "🏢": {"name": "office_building", "width": 2, "category": "symbols"},
    "🏣": {"name": "japanese_post_office", "width": 2, "category": "symbols"},
    "🏤": {"name": "european_post_office", "width": 2, "category": "symbols"},
    "🏥": {"name": "hospital", "width": 2, "category": "symbols"},
    "🏦": {"name": "bank", "width": 2, "category": "symbols"},
    "🏧": {"name": "automated_teller_machine", "width": 2, "category": "symbols"},
    "🏨": {"name": "hotel", "width": 2, "category": "symbols"},
    "🏩": {"name": "love_hotel", "width": 2, "category": "symbols"},
    "🏪": {"name": "convenience_store", "width": 2, "category": "symbols"},
    "🏫": {"name": "school", "width": 2, "category": "symbols"},
    "🏬": {"name": "department_store", "width": 2, "category": "symbols"},
    "🏭": {"name": "factory", "width": 2, "category": "symbols"},
    "🏮": {"name": "izakaya_lantern", "width": 2, "category": "symbols"},
    "🏯": {"name": "japanese_castle", "width": 2, "category": "symbols"},
    "🏰": {"name": "european_castle", "width": 2, "category": "symbols"},
    "🏴": {"name": "waving_black_flag", "width": 2, "category": "symbols"},
    "🏸": {"name": "badminton_racquet_and_shuttlecock", "width": 2, "category": "symbols"},
    "🏹": {"name": "bow_and_arrow", "width": 2, "category": "symbols"},
    "🏺": {"name": "amphora", "width": 2, "category": "symbols"},
    "🐀": {"name": "rat", "width": 2, "category": "symbols"},
    "🐁": {"name": "mouse", "width": 2, "category": "symbols"},
    "🐂": {"name": "ox", "width": 2, "category": "symbols"},
    "🐃": {"name": "water_buffalo", "width": 2, "category": "symbols"},
    "🐄": {"name": "cow", "width": 2, "category": "symbols"},
    "🐅": {"name": "tiger", "width": 2, "category": "symbols"},
    "🐆": {"name": "leopard", "width": 2, "category": "symbols"},
    "🐇": {"name": "rabbit", "width": 2, "category": "symbols"},
    "🐈": {"name": "cat", "width": 2, "category": "symbols"},
    "🐉": {"name": "dragon", "width": 2, "category": "symbols"},
    "🐊": {"name": "crocodile", "width": 2, "category": "symbols"},
    "🐋": {"name": "whale", "width": 2, "category": "symbols"},
    "🐌": {"name": "snail", "width": 2, "category": "symbols"},
    "🐍": {"name": "snake", "width": 2, "category": "symbols"},
    "🐎": {"name": "horse", "width": 2, "category": "symbols"},
    "🐏": {"name": "ram", "width": 2, "category": "symbols"},
    "🐐": {"name": "goat", "width": 2, "category": "symbols"},
    "🐑": {"name": "sheep", "width": 2, "category": "symbols"},
    "🐒": {"name": "monkey", "width": 2, "category": "symbols"},
    "🐓": {"name": "rooster", "width": 2, "category": "symbols"},
    "🐔": {"name": "chicken", "width": 2, "category": "symbols"},
    "🐕": {"name": "dog", "width": 2, "category": "symbols"},
    "🐖": {"name": "pig", "width": 2, "category": "symbols"},
    "🐗": {"name": "boar", "width": 2, "category": "symbols"},
    "🐘": {"name": "elephant", "width": 2, "category": "symbols"},
    "🐙": {"name": "octopus", "width": 2, "category": "symbols"},
    "🐚": {"name": "spiral_shell", "width": 2, "category": "symbols"},
    "🐛": {"name": "bug", "width": 2, "category": "symbols"},
    "🐜": {"name": "ant", "width": 2, "category": "symbols"},
    "🐝": {"name": "honeybee", "width": 2, "category": "symbols"},
    "🐞": {"name": "lady_beetle", "width": 2, "category": "symbols"},
    "🐟": {"name": "fish", "width": 2, "category": "symbols"},
    "🐠": {"name": "tropical_fish", "width": 2, "category": "symbols"},
    "🐡": {"name": "blowfish", "width": 2, "category": "symbols"},
    "🐢": {"name": "turtle", "width": 2, "category": "symbols"},
    "🐣": {"name": "hatching_chick", "width": 2, "category": "symbols"},
    "🐤": {"name": "baby_chick", "width": 2, "category": "symbols"},
    "🐥": {"name": "front_facing_baby_chick", "width": 2, "category": "symbols"},
    "🐦": {"name": "bird", "width": 2, "category": "symbols"},
    "🐧": {"name": "penguin", "width": 2, "category": "symbols"},
    "🐨": {"name": "koala", "width": 2, "category": "symbols"},
    "🐩": {"name": "poodle", "width": 2, "category": "symbols"},
    "🐪": {"name": "dromedary_camel", "width": 2, "category": "symbols"},
    "🐫": {"name": "bactrian_camel", "width": 2, "category": "symbols"},
    "🐬": {"name": "dolphin", "width": 2, "category": "symbols"},
    "🐭": {"name": "mouse_face", "width": 2, "category": "symbols"},
    "🐮": {"name": "cow_face", "width": 2, "category": "symbols"},
    "🐯": {"name": "tiger_face", "width": 2, "category": "symbols"},
    "🐰": {"name": "rabbit_face", "width": 2, "category": "symbols"},
    "🐱": {"name": "cat_face", "width": 2, "category": "symbols"},
    "🐲": {"name": "dragon_face", "width": 2, "category": "symbols"},
    "🐳": {"name": "spouting_whale", "width": 2, "category": "symbols"},
    "🐴": {"name": "horse_face", "width": 2, "category": "symbols"},
    "🐵": {"name": "monkey_face", "width": 2, "category": "symbols"},
    "🐶": {"name": "dog_face", "width": 2, "category": "symbols"},
    "🐷": {"name": "pig_face", "width": 2, "category": "symbols"},
    "🐸": {"name": "frog_face", "width": 2, "category": "symbols"},
    "🐹": {"name": "hamster_face", "width": 2, "category": "symbols"},
    "🐺": {"name": "wolf_face", "width": 2, "category": "symbols"},
    "🐻": {"name": "bear_face", "width": 2, "category": "symbols"},
    "🐼": {"name": "panda_face", "width": 2, "category": "symbols"},
    "🐽": {"name": "pig_nose", "width": 2, "category": "symbols"},
    "🐾": {"name": "paw_prints", "width": 2, "category": "symbols"},
    "👀": {"name": "eyes", "width": 2, "category": "symbols"},
    "👂": {"name": "ear", "width": 2, "category": "symbols"},
    "👃": {"name": "nose", "width": 2, "category": "symbols"},
    "👄": {"name": "mouth", "width": 2, "category": "symbols"},
    "👅": {"name": "tongue", "width": 2, "category": "symbols"},
    "👆": {"name": "white_up_pointing_backhand_index", "width": 2, "category": "symbols"},
    "👇": {"name": "white_down_pointing_backhand_index", "width": 2, "category": "symbols"},
    "👈": {"name": "white_left_pointing_backhand_index", "width": 2, "category": "symbols"},
    "👉": {"name": "white_right_pointing_backhand_index", "width": 2, "category": "symbols"},
    "👊": {"name": "fisted_hand_sign", "width": 2, "category": "symbols"},
    "👋": {"name": "waving_hand_sign", "width": 2, "category": "symbols"},
    "👌": {"name": "ok_hand_sign", "width": 2, "category": "symbols"},
    "👍": {"name": "thumbs_up_sign", "width": 2, "category": "symbols"},
    "👎": {"name": "thumbs_down_sign", "width": 2, "category": "symbols"},
    "👏": {"name": "clapping_hands_sign", "width": 2, "category": "symbols"},
    "👐": {"name": "open_hands_sign", "width": 2, "category": "symbols"},
    "👑": {"name": "crown", "width": 2, "category": "symbols"},
    "👒": {"name": "womans_hat", "width": 2, "category": "symbols"},
    "👓": {"name": "eyeglasses", "width": 2, "category": "symbols"},
    "👔": {"name": "necktie", "width": 2, "category": "symbols"},
    "👕": {"name": "t_shirt", "width": 2, "category": "symbols"},
    "👖": {"name": "jeans", "width": 2, "category": "symbols"},
    "👗": {"name": "dress", "width": 2, "category": "symbols"},
    "👘": {"name": "kimono", "width": 2, "category": "symbols"},
    "👙": {"name": "bikini", "width": 2, "category": "symbols"},
    "👚": {"name": "womans_clothes", "width": 2, "category": "symbols"},
    "👛": {"name": "purse", "width": 2, "category": "symbols"},
    "👜": {"name": "handbag", "width": 2, "category": "symbols"},
    "👝": {"name": "pouch", "width": 2, "category": "symbols"},
    "👞": {"name": "mans_shoe", "width": 2, "category": "symbols"},
    "👟": {"name": "athletic_shoe", "width": 2, "category": "symbols"},
    "👠": {"name": "high_heeled_shoe", "width": 2, "category": "symbols"},
    "👡": {"name": "womans_sandal", "width": 2, "category": "symbols"},
    "👢": {"name": "womans_boots", "width": 2, "category": "symbols"},
    "👣": {"name": "footprints", "width": 2, "category": "symbols"},
    "👤": {"name": "bust_in_silhouette", "width": 2, "category": "symbols"},
    "👥": {"name": "busts_in_silhouette", "width": 2, "category": "symbols"},
    "👦": {"name": "boy", "width": 2, "category": "symbols"},
    "👧": {"name": "girl", "width": 2, "category": "symbols"},
    "👨": {"name": "man", "width": 2, "category": "symbols"},
    "👩": {"name": "woman", "width": 2, "category": "symbols"},
    "👪": {"name": "family", "width": 2, "category": "symbols"},
    "👫": {"name": "man_and_woman_holding_hands", "width": 2, "category": "symbols"},
    "👬": {"name": "two_men_holding_hands", "width": 2, "category": "symbols"},
    "👭": {"name": "two_women_holding_hands", "width": 2, "category": "symbols"},
    "👮": {"name": "police_officer", "width": 2, "category": "symbols"},
    "👯": {"name": "woman_with_bunny_ears", "width": 2, "category": "symbols"},
    "👰": {"name": "bride_with_veil", "width": 2, "category": "symbols"},
    "👱": {"name": "person_with_blond_hair", "width": 2, "category": "symbols"},
    "👲": {"name": "man_with_gua_pi_mao", "width": 2, "category": "symbols"},
    "👳": {"name": "man_with_turban", "width": 2, "category": "symbols"},
    "👴": {"name": "older_man", "width": 2, "category": "symbols"},
    "👵": {"name": "older_woman", "width": 2, "category": "symbols"},
    "👶": {"name": "baby", "width": 2, "category": "symbols"},
    "👷": {"name": "construction_worker", "width": 2, "category": "symbols"},
    "👸": {"name": "princess", "width": 2, "category": "symbols"},
    "👹": {"name": "japanese_ogre", "width": 2, "category": "symbols"},
    "👺": {"name": "japanese_goblin", "width": 2, "category": "symbols"},
    "👻": {"name": "ghost", "width": 2, "category": "symbols"},
    "👼": {"name": "baby_angel", "width": 2, "category": "symbols"},
    "👽": {"name": "extraterrestrial_alien", "width": 2, "category": "symbols"},
    "👾": {"name": "alien_monster", "width": 2, "category": "symbols"},
    "👿": {"name": "imp", "width": 2, "category": "symbols"},
    "💀": {"name": "skull", "width": 2, "category": "symbols"},
    "💁": {"name": "information_desk_person", "width": 2, "category": "symbols"},
    "💂": {"name": "guardsman", "width": 2, "category": "symbols"},
    "💃": {"name": "dancer", "width": 2, "category": "symbols"},
    "💄": {"name": "lipstick", "width": 2, "category": "symbols"},
    "💅": {"name": "nail_polish", "width": 2, "category": "symbols"},
    "💆": {"name": "face_massage", "width": 2, "category": "symbols"},
    "💇": {"name": "haircut", "width": 2, "category": "symbols"},
    "💈": {"name": "barber_pole", "width": 2, "category": "symbols"},
    "💉": {"name": "syringe", "width": 2, "category": "symbols"},
    "💊": {"name": "pill", "width": 2, "category": "symbols"},
    "💋": {"name": "kiss_mark", "width": 2, "category": "symbols"},
    "💌": {"name": "love_letter", "width": 2, "category": "symbols"},
    "💍": {"name": "ring", "width": 2, "category": "symbols"},
    "💎": {"name": "gem_stone", "width": 2, "category": "symbols"},
    "💏": {"name": "kiss", "width": 2, "category": "symbols"},
    "💐": {"name": "bouquet", "width": 2, "category": "symbols"},
    "💑": {"name": "couple_with_heart", "width": 2, "category": "symbols"},
    "💒": {"name": "wedding", "width": 2, "category": "symbols"},
    "💓": {"name": "beating_heart", "width": 2, "category": "symbols"},
    "💔": {"name": "broken_heart", "width": 2, "category": "symbols"},
    "💕": {"name": "two_hearts", "width": 2, "category": "symbols"},
    "💖": {"name": "sparkling_heart", "width": 2, "category": "symbols"},
    "💗": {"name": "growing_heart", "width": 2, "category": "symbols"},
    "💘": {"name": "heart_with_arrow", "width": 2, "category": "symbols"},
    "💙": {"name": "blue_heart", "width": 2, "category": "symbols"},
    "💚": {"name": "green_heart", "width": 2, "category": "symbols"},
    "💛": {"name": "yellow_heart", "width": 2, "category": "symbols"},
    "💜": {"name": "purple_heart", "width": 2, "category": "symbols"},
    "💝": {"name": "heart_with_ribbon", "width": 2, "category": "symbols"},
    "💞": {"name": "revolving_hearts", "width": 2, "category": "symbols"},
    "💟": {"name": "heart_decoration", "width": 2, "category": "symbols"},
    "💠": {"name": "diamond_shape_with_a_dot_inside", "width": 2, "category": "symbols"},
    "💡": {"name": "electric_light_bulb", "width": 2, "category": "symbols"},
    "💢": {"name": "anger_symbol", "width": 2, "category": "symbols"},
    "💣": {"name": "bomb", "width": 2, "category": "symbols"},
    "💤": {"name": "sleeping_symbol", "width": 2, "category": "symbols"},
    "💥": {"name": "collision_symbol", "width": 2, "category": "symbols"},
    "💦": {"name": "splashing_sweat_symbol", "width": 2, "category": "symbols"},
    "💧": {"name": "droplet", "width": 2, "category": "symbols"},
    "💨": {"name": "dash_symbol", "width": 2, "category": "symbols"},
    "💩": {"name": "pile_of_poo", "width": 2, "category": "symbols"},
    "💪": {"name": "flexed_biceps", "width": 2, "category": "symbols"},
    "💫": {"name": "dizzy_symbol", "width": 2, "category": "symbols"},
    "💬": {"name": "speech_balloon", "width": 2, "category": "symbols"},
    "💭": {"name": "thought_balloon", "width": 2, "category": "symbols"},
    "💮": {"name": "white_flower", "width": 2, "category": "symbols"},
    "💯": {"name": "hundred_points_symbol", "width": 2, "category": "symbols"},
    "💰": {"name": "money_bag", "width": 2, "category": "symbols"},
    "💱": {"name": "currency_exchange", "width": 2, "category": "symbols"},
    "💲": {"name": "heavy_dollar_sign", "width": 2, "category": "symbols"},
    "💳": {"name": "credit_card", "width": 2, "category": "symbols"},
    "💴": {"name": "banknote_with_yen_sign", "width": 2, "category": "symbols"},
    "💵": {"name": "banknote_with_dollar_sign", "width": 2, "category": "symbols"},
    "💶": {"name": "banknote_with_euro_sign", "width": 2, "category": "symbols"},
    "💷": {"name": "banknote_with_pound_sign", "width": 2, "category": "symbols"},
    "💸": {"name": "money_with_wings", "width": 2, "category": "symbols"},
    "💹": {"name": "chart_with_upwards_trend_and_yen_sign", "width": 2, "category": "symbols"},
    "💺": {"name": "seat", "width": 2, "category": "symbols"},
    "💻": {"name": "personal_computer", "width": 2, "category": "symbols"},
    "💼": {"name": "briefcase", "width": 2, "category": "symbols"},
    "💽": {"name": "minidisc", "width": 2, "category": "symbols"},
    "💾": {"name": "floppy_disk", "width": 2, "category": "symbols"},
    "💿": {"name": "optical_disc", "width": 2, "category": "symbols"},
    "📀": {"name": "dvd", "width": 2, "category": "symbols"},
    "📁": {"name": "file_folder", "width": 2, "category": "symbols"},
    "📂": {"name": "open_file_folder", "width": 2, "category": "symbols"},
    "📃": {"name": "page_with_curl", "width": 2, "category": "symbols"},
    "📄": {"name": "page_facing_up", "width": 2, "category": "symbols"},
    "📅": {"name": "calendar", "width": 2, "category": "symbols"},
    "📆": {"name": "tear_off_calendar", "width": 2, "category": "symbols"},
    "📇": {"name": "card_index", "width": 2, "category": "symbols"},
    "📈": {"name": "chart_with_upwards_trend", "width": 2, "category": "symbols"},
    "📉": {"name": "chart_with_downwards_trend", "width": 2, "category": "symbols"},
    "📊": {"name": "bar_chart", "width": 2, "category": "symbols"},
    "📋": {"name": "clipboard", "width": 2, "category": "symbols"},
    "📌": {"name": "pushpin", "width": 2, "category": "symbols"},
    "📍": {"name": "round_pushpin", "width": 2, "category": "symbols"},
    "📎": {"name": "paperclip", "width": 2, "category": "symbols"},
    "📏": {"name": "straight_ruler", "width": 2, "category": "symbols"},
    "📐": {"name": "triangular_ruler", "width": 2, "category": "symbols"},
    "📑": {"name": "bookmark_tabs", "width": 2, "category": "symbols"},
    "📒": {"name": "ledger", "width": 2, "category": "symbols"},
    "📓": {"name": "notebook", "width": 2, "category": "symbols"},
    "📔": {"name": "notebook_with_decorative_cover", "width": 2, "category": "symbols"},
    "📕": {"name": "closed_book", "width": 2, "category": "symbols"},
    "📖": {"name": "open_book", "width": 2, "category": "symbols"},
    "📗": {"name": "green_book", "width": 2, "category": "symbols"},
    "📘": {"name": "blue_book", "width": 2, "category": "symbols"},
    "📙": {"name": "orange_book", "width": 2, "category": "symbols"},
    "📚": {"name": "books", "width": 2, "category": "symbols"},
    "📛": {"name": "name_badge", "width": 2, "category": "symbols"},
    "📜": {"name": "scroll", "width": 2, "category": "symbols"},
    "📝": {"name": "memo", "width": 2, "category": "symbols"},
    "📞": {"name": "telephone_receiver", "width": 2, "category": "symbols"},
    "📟": {"name": "pager", "width": 2, "category": "symbols"},
    "📠": {"name": "fax_machine", "width": 2, "category": "symbols"},
    "📡": {"name": "satellite_antenna", "width": 2, "category": "symbols"},
    "📢": {"name": "public_address_loudspeaker", "width": 2, "category": "symbols"},
    "📣": {"name": "cheering_megaphone", "width": 2, "category": "symbols"},
    "📤": {"name": "outbox_tray", "width": 2, "category": "symbols"},
    "📥": {"name": "inbox_tray", "width": 2, "category": "symbols"},
    "📦": {"name": "package", "width": 2, "category": "symbols"},
    "📧": {"name": "e_mail_symbol", "width": 2, "category": "symbols"},
    "📨": {"name": "incoming_envelope", "width": 2, "category": "symbols"},
    "📩": {"name": "envelope_with_downwards_arrow_above", "width": 2, "category": "symbols"},
    "📪": {"name": "closed_mailbox_with_lowered_flag", "width": 2, "category": "symbols"},
    "📫": {"name": "closed_mailbox_with_raised_flag", "width": 2, "category": "symbols"},
    "📬": {"name": "open_mailbox_with_raised_flag", "width": 2, "category": "symbols"},
    "📭": {"name": "open_mailbox_with_lowered_flag", "width": 2, "category": "symbols"},
    "📮": {"name": "postbox", "width": 2, "category": "symbols"},
    "📯": {"name": "postal_horn", "width": 2, "category": "symbols"},
    "📰": {"name": "newspaper", "width": 2, "category": "symbols"},
    "📱": {"name": "mobile_phone", "width": 2, "category": "symbols"},
    "📲": {"name": "mobile_phone_with_rightwards_arrow_at_left", "width": 2, "category": "symbols"},
    "📳": {"name": "vibration_mode", "width": 2, "category": "symbols"},
    "📴": {"name": "mobile_phone_off", "width": 2, "category": "symbols"},
    "📵": {"name": "no_mobile_phones", "width": 2, "category": "symbols"},
    "📶": {"name": "antenna_with_bars", "width": 2, "category": "symbols"},
    "📷": {"name": "camera", "width": 2, "category": "symbols"},
    "📸": {"name": "camera_with_flash", "width": 2, "category": "symbols"},
    "📹": {"name": "video_camera", "width": 2, "category": "symbols"},
    "📺": {"name": "television", "width": 2, "category": "symbols"},
    "📻": {"name": "radio", "width": 2, "category": "symbols"},
    "📼": {"name": "videocassette", "width": 2, "category": "symbols"},
    "📿": {"name": "prayer_beads", "width": 2, "category": "symbols"},
    "🔀": {"name": "twisted_rightwards_arrows", "width": 2, "category": "symbols"},
    "🔁": {
        "name": "clockwise_rightwards_and_leftwards_open_circle_arrows",
        "width": 2,
        "category": "symbols",
    },
    "🔂": {
        "name": "clockwise_rightwards_and_leftwards_open_circle_arrows_with_circled_one_overlay",
        "width": 2,
        "category": "symbols",
    },
    "🔃": {
        "name": "clockwise_downwards_and_upwards_open_circle_arrows",
        "width": 2,
        "category": "symbols",
    },
    "🔄": {
        "name": "anticlockwise_downwards_and_upwards_open_circle_arrows",
        "width": 2,
        "category": "symbols",
    },
    "🔅": {"name": "low_brightness_symbol", "width": 2, "category": "symbols"},
    "🔆": {"name": "high_brightness_symbol", "width": 2, "category": "symbols"},
    "🔇": {"name": "speaker_with_cancellation_stroke", "width": 2, "category": "symbols"},
    "🔈": {"name": "speaker", "width": 2, "category": "symbols"},
    "🔉": {"name": "speaker_with_one_sound_wave", "width": 2, "category": "symbols"},
    "🔊": {"name": "speaker_with_three_sound_waves", "width": 2, "category": "symbols"},
    "🔋": {"name": "battery", "width": 2, "category": "symbols"},
    "🔌": {"name": "electric_plug", "width": 2, "category": "symbols"},
    "🔍": {"name": "left_pointing_magnifying_glass", "width": 2, "category": "symbols"},
    "🔎": {"name": "right_pointing_magnifying_glass", "width": 2, "category": "symbols"},
    "🔏": {"name": "lock_with_ink_pen", "width": 2, "category": "symbols"},
    "🔐": {"name": "closed_lock_with_key", "width": 2, "category": "symbols"},
    "🔑": {"name": "key", "width": 2, "category": "symbols"},
    "🔒": {"name": "lock", "width": 2, "category": "symbols"},
    "🔓": {"name": "open_lock", "width": 2, "category": "symbols"},
    "🔔": {"name": "bell", "width": 2, "category": "symbols"},
    "🔕": {"name": "bell_with_cancellation_stroke", "width": 2, "category": "symbols"},
    "🔖": {"name": "bookmark", "width": 2, "category": "symbols"},
    "🔗": {"name": "link_symbol", "width": 2, "category": "symbols"},
    "🔘": {"name": "radio_button", "width": 2, "category": "symbols"},
    "🔙": {"name": "back_with_leftwards_arrow_above", "width": 2, "category": "symbols"},
    "🔚": {"name": "end_with_leftwards_arrow_above", "width": 2, "category": "symbols"},
    "🔛": {
        "name": "on_with_exclamation_mark_with_left_right_arrow_above",
        "width": 2,
        "category": "symbols",
    },
    "🔜": {"name": "soon_with_rightwards_arrow_above", "width": 2, "category": "symbols"},
    "🔝": {"name": "top_with_upwards_arrow_above", "width": 2, "category": "symbols"},
    "🔞": {"name": "no_one_under_eighteen_symbol", "width": 2, "category": "symbols"},
    "🔟": {"name": "keycap_ten", "width": 2, "category": "symbols"},
    "🔠": {"name": "input_symbol_for_latin_capital_letters", "width": 2, "category": "symbols"},
    "🔡": {"name": "input_symbol_for_latin_small_letters", "width": 2, "category": "symbols"},
    "🔢": {"name": "input_symbol_for_numbers", "width": 2, "category": "symbols"},
    "🔣": {"name": "input_symbol_for_symbols", "width": 2, "category": "symbols"},
    "🔤": {"name": "input_symbol_for_latin_letters", "width": 2, "category": "symbols"},
    "🔥": {"name": "fire", "width": 2, "category": "symbols"},
    "🔦": {"name": "electric_torch", "width": 2, "category": "symbols"},
    "🔧": {"name": "wrench", "width": 2, "category": "symbols"},
    "🔨": {"name": "hammer", "width": 2, "category": "symbols"},
    "🔩": {"name": "nut_and_bolt", "width": 2, "category": "symbols"},
    "🔪": {"name": "hocho", "width": 2, "category": "symbols"},
    "🔫": {"name": "pistol", "width": 2, "category": "symbols"},
    "🔬": {"name": "microscope", "width": 2, "category": "symbols"},
    "🔭": {"name": "telescope", "width": 2, "category": "symbols"},
    "🔮": {"name": "crystal_ball", "width": 2, "category": "symbols"},
    "🔯": {"name": "six_pointed_star_with_middle_dot", "width": 2, "category": "symbols"},
    "🔰": {"name": "japanese_symbol_for_beginner", "width": 2, "category": "symbols"},
    "🔱": {"name": "trident_emblem", "width": 2, "category": "symbols"},
    "🔲": {"name": "black_square_button", "width": 2, "category": "symbols"},
    "🔳": {"name": "white_square_button", "width": 2, "category": "symbols"},
    "🔴": {"name": "large_red_circle", "width": 2, "category": "symbols"},
    "🔵": {"name": "large_blue_circle", "width": 2, "category": "symbols"},
    "🔶": {"name": "large_orange_diamond", "width": 2, "category": "symbols"},
    "🔷": {"name": "large_blue_diamond", "width": 2, "category": "symbols"},
    "🔸": {"name": "small_orange_diamond", "width": 2, "category": "symbols"},
    "🔹": {"name": "small_blue_diamond", "width": 2, "category": "symbols"},
    "🔺": {"name": "up_pointing_red_triangle", "width": 2, "category": "symbols"},
    "🔻": {"name": "down_pointing_red_triangle", "width": 2, "category": "symbols"},
    "🔼": {"name": "up_pointing_small_red_triangle", "width": 2, "category": "symbols"},
    "🔽": {"name": "down_pointing_small_red_triangle", "width": 2, "category": "symbols"},
    "🕋": {"name": "kaaba", "width": 2, "category": "symbols"},
    "🕌": {"name": "mosque", "width": 2, "category": "symbols"},
    "🕍": {"name": "synagogue", "width": 2, "category": "symbols"},
    "🕎": {"name": "menorah_with_nine_branches", "width": 2, "category": "symbols"},
    "🕐": {"name": "clock_face_one_oclock", "width": 2, "category": "symbols"},
    "🕑": {"name": "clock_face_two_oclock", "width": 2, "category": "symbols"},
    "🕒": {"name": "clock_face_three_oclock", "width": 2, "category": "symbols"},
    "🕓": {"name": "clock_face_four_oclock", "width": 2, "category": "symbols"},
    "🕔": {"name": "clock_face_five_oclock", "width": 2, "category": "symbols"},
    "🕕": {"name": "clock_face_six_oclock", "width": 2, "category": "symbols"},
    "🕖": {"name": "clock_face_seven_oclock", "width": 2, "category": "symbols"},
    "🕗": {"name": "clock_face_eight_oclock", "width": 2, "category": "symbols"},
    "🕘": {"name": "clock_face_nine_oclock", "width": 2, "category": "symbols"},
    "🕙": {"name": "clock_face_ten_oclock", "width": 2, "category": "symbols"},
    "🕚": {"name": "clock_face_eleven_oclock", "width": 2, "category": "symbols"},
    "🕛": {"name": "clock_face_twelve_oclock", "width": 2, "category": "symbols"},
    "🕜": {"name": "clock_face_one_thirty", "width": 2, "category": "symbols"},
    "🕝": {"name": "clock_face_two_thirty", "width": 2, "category": "symbols"},
    "🕞": {"name": "clock_face_three_thirty", "width": 2, "category": "symbols"},
    "🕟": {"name": "clock_face_four_thirty", "width": 2, "category": "symbols"},
    "🕠": {"name": "clock_face_five_thirty", "width": 2, "category": "symbols"},
    "🕡": {"name": "clock_face_six_thirty", "width": 2, "category": "symbols"},
    "🕢": {"name": "clock_face_seven_thirty", "width": 2, "category": "symbols"},
    "🕣": {"name": "clock_face_eight_thirty", "width": 2, "category": "symbols"},
    "🕤": {"name": "clock_face_nine_thirty", "width": 2, "category": "symbols"},
    "🕥": {"name": "clock_face_ten_thirty", "width": 2, "category": "symbols"},
    "🕦": {"name": "clock_face_eleven_thirty", "width": 2, "category": "symbols"},
    "🕧": {"name": "clock_face_twelve_thirty", "width": 2, "category": "symbols"},
    "🕺": {"name": "man_dancing", "width": 2, "category": "symbols"},
    "🖕": {"name": "reversed_hand_with_middle_finger_extended", "width": 2, "category": "symbols"},
    "🖖": {
        "name": "raised_hand_with_part_between_middle_and_ring_fingers",
        "width": 2,
        "category": "symbols",
    },
    "🖤": {"name": "black_heart", "width": 2, "category": "symbols"},
    "🗻": {"name": "mount_fuji", "width": 2, "category": "symbols"},
    "🗼": {"name": "tokyo_tower", "width": 2, "category": "symbols"},
    "🗽": {"name": "statue_of_liberty", "width": 2, "category": "symbols"},
    "🗾": {"name": "silhouette_of_japan", "width": 2, "category": "symbols"},
    "🗿": {"name": "moyai", "width": 2, "category": "symbols"},
    "😀": {"name": "grinning_face", "width": 2, "category": "people"},
    "😁": {"name": "grinning_face_with_smiling_eyes", "width": 2, "category": "people"},
    "😂": {"name": "face_with_tears_of_joy", "width": 2, "category": "people"},
    "😃": {"name": "smiling_face_with_open_mouth", "width": 2, "category": "people"},
    "😄": {
        "name": "smiling_face_with_open_mouth_and_smiling_eyes",
        "width": 2,
        "category": "people",
    },
    "😅": {"name": "smiling_face_with_open_mouth_and_cold_sweat", "width": 2, "category": "people"},
    "😆": {
        "name": "smiling_face_with_open_mouth_and_tightly_closed_eyes",
        "width": 2,
        "category": "people",
    },
    "😇": {"name": "smiling_face_with_halo", "width": 2, "category": "people"},
    "😈": {"name": "smiling_face_with_horns", "width": 2, "category": "people"},
    "😉": {"name": "winking_face", "width": 2, "category": "people"},
    "😊": {"name": "smiling_face_with_smiling_eyes", "width": 2, "category": "people"},
    "😋": {"name": "face_savouring_delicious_food", "width": 2, "category": "people"},
    "😌": {"name": "relieved_face", "width": 2, "category": "people"},
    "😍": {"name": "smiling_face_with_heart_shaped_eyes", "width": 2, "category": "people"},
    "😎": {"name": "smiling_face_with_sunglasses", "width": 2, "category": "people"},
    "😏": {"name": "smirking_face", "width": 2, "category": "people"},
    "😐": {"name": "neutral_face", "width": 2, "category": "people"},
    "😑": {"name": "expressionless_face", "width": 2, "category": "people"},
    "😒": {"name": "unamused_face", "width": 2, "category": "people"},
    "😓": {"name": "face_with_cold_sweat", "width": 2, "category": "people"},
    "😔": {"name": "pensive_face", "width": 2, "category": "people"},
    "😕": {"name": "confused_face", "width": 2, "category": "people"},
    "😖": {"name": "confounded_face", "width": 2, "category": "people"},
    "😗": {"name": "kissing_face", "width": 2, "category": "people"},
    "😘": {"name": "face_throwing_a_kiss", "width": 2, "category": "people"},
    "😙": {"name": "kissing_face_with_smiling_eyes", "width": 2, "category": "people"},
    "😚": {"name": "kissing_face_with_closed_eyes", "width": 2, "category": "people"},
    "😛": {"name": "face_with_stuck_out_tongue", "width": 2, "category": "people"},
    "😜": {"name": "face_with_stuck_out_tongue_and_winking_eye", "width": 2, "category": "people"},
    "😝": {
        "name": "face_with_stuck_out_tongue_and_tightly_closed_eyes",
        "width": 2,
        "category": "people",
    },
    "😞": {"name": "disappointed_face", "width": 2, "category": "people"},
    "😟": {"name": "worried_face", "width": 2, "category": "people"},
    "😠": {"name": "angry_face", "width": 2, "category": "people"},
    "😡": {"name": "pouting_face", "width": 2, "category": "people"},
    "😢": {"name": "crying_face", "width": 2, "category": "people"},
    "😣": {"name": "persevering_face", "width": 2, "category": "people"},
    "😤": {"name": "face_with_look_of_triumph", "width": 2, "category": "people"},
    "😥": {"name": "disappointed_but_relieved_face", "width": 2, "category": "people"},
    "😦": {"name": "frowning_face_with_open_mouth", "width": 2, "category": "people"},
    "😧": {"name": "anguished_face", "width": 2, "category": "people"},
    "😨": {"name": "fearful_face", "width": 2, "category": "people"},
    "😩": {"name": "weary_face", "width": 2, "category": "people"},
    "😪": {"name": "sleepy_face", "width": 2, "category": "people"},
    "😫": {"name": "tired_face", "width": 2, "category": "people"},
    "😬": {"name": "grimacing_face", "width": 2, "category": "people"},
    "😭": {"name": "loudly_crying_face", "width": 2, "category": "people"},
    "😮": {"name": "face_with_open_mouth", "width": 2, "category": "people"},
    "😯": {"name": "hushed_face", "width": 2, "category": "people"},
    "😰": {"name": "face_with_open_mouth_and_cold_sweat", "width": 2, "category": "people"},
    "😱": {"name": "face_screaming_in_fear", "width": 2, "category": "people"},
    "😲": {"name": "astonished_face", "width": 2, "category": "people"},
    "😳": {"name": "flushed_face", "width": 2, "category": "people"},
    "😴": {"name": "sleeping_face", "width": 2, "category": "people"},
    "😵": {"name": "dizzy_face", "width": 2, "category": "people"},
    "😶": {"name": "face_without_mouth", "width": 2, "category": "people"},
    "😷": {"name": "face_with_medical_mask", "width": 2, "category": "people"},
    "😸": {"name": "grinning_cat_face_with_smiling_eyes", "width": 2, "category": "people"},
    "😹": {"name": "cat_face_with_tears_of_joy", "width": 2, "category": "people"},
    "😺": {"name": "smiling_cat_face_with_open_mouth", "width": 2, "category": "people"},
    "😻": {"name": "smiling_cat_face_with_heart_shaped_eyes", "width": 2, "category": "people"},
    "😼": {"name": "cat_face_with_wry_smile", "width": 2, "category": "people"},
    "😽": {"name": "kissing_cat_face_with_closed_eyes", "width": 2, "category": "people"},
    "😾": {"name": "pouting_cat_face", "width": 2, "category": "people"},
    "😿": {"name": "crying_cat_face", "width": 2, "category": "people"},
    "🙀": {"name": "weary_cat_face", "width": 2, "category": "people"},
    "🙁": {"name": "slightly_frowning_face", "width": 2, "category": "people"},
    "🙂": {"name": "slightly_smiling_face", "width": 2, "category": "people"},
    "🙃": {"name": "upside_down_face", "width": 2, "category": "people"},
    "🙄": {"name": "face_with_rolling_eyes", "width": 2, "category": "people"},
    "🙅": {"name": "face_with_no_good_gesture", "width": 2, "category": "people"},
    "🙆": {"name": "face_with_ok_gesture", "width": 2, "category": "people"},
    "🙇": {"name": "person_bowing_deeply", "width": 2, "category": "people"},
    "🙈": {"name": "see_no_evil_monkey", "width": 2, "category": "people"},
    "🙉": {"name": "hear_no_evil_monkey", "width": 2, "category": "people"},
    "🙊": {"name": "speak_no_evil_monkey", "width": 2, "category": "people"},
    "🙋": {"name": "happy_person_raising_one_hand", "width": 2, "category": "people"},
    "🙌": {"name": "person_raising_both_hands_in_celebration", "width": 2, "category": "people"},
    "🙍": {"name": "person_frowning", "width": 2, "category": "people"},
    "🙎": {"name": "person_with_pouting_face", "width": 2, "category": "people"},
    "🙏": {"name": "person_with_folded_hands", "width": 2, "category": "people"},
    "🚀": {"name": "rocket", "width": 2, "category": "transport"},
    "🚁": {"name": "helicopter", "width": 2, "category": "transport"},
    "🚂": {"name": "steam_locomotive", "width": 2, "category": "transport"},
    "🚃": {"name": "railway_car", "width": 2, "category": "transport"},
    "🚄": {"name": "high_speed_train", "width": 2, "category": "transport"},
    "🚅": {"name": "high_speed_train_with_bullet_nose", "width": 2, "category": "transport"},
    "🚆": {"name": "train", "width": 2, "category": "transport"},
    "🚇": {"name": "metro", "width": 2, "category": "transport"},
    "🚈": {"name": "light_rail", "width": 2, "category": "transport"},
    "🚉": {"name": "station", "width": 2, "category": "transport"},
    "🚊": {"name": "tram", "width": 2, "category": "transport"},
    "🚋": {"name": "tram_car", "width": 2, "category": "transport"},
    "🚌": {"name": "bus", "width": 2, "category": "transport"},
    "🚍": {"name": "oncoming_bus", "width": 2, "category": "transport"},
    "🚎": {"name": "trolleybus", "width": 2, "category": "transport"},
    "🚏": {"name": "bus_stop", "width": 2, "category": "transport"},
    "🚐": {"name": "minibus", "width": 2, "category": "transport"},
    "🚑": {"name": "ambulance", "width": 2, "category": "transport"},
    "🚒": {"name": "fire_engine", "width": 2, "category": "transport"},
    "🚓": {"name": "police_car", "width": 2, "category": "transport"},
    "🚔": {"name": "oncoming_police_car", "width": 2, "category": "transport"},
    "🚕": {"name": "taxi", "width": 2, "category": "transport"},
    "🚖": {"name": "oncoming_taxi", "width": 2, "category": "transport"},
    "🚗": {"name": "automobile", "width": 2, "category": "transport"},
    "🚘": {"name": "oncoming_automobile", "width": 2, "category": "transport"},
    "🚙": {"name": "recreational_vehicle", "width": 2, "category": "transport"},
    "🚚": {"name": "delivery_truck", "width": 2, "category": "transport"},
    "🚛": {"name": "articulated_lorry", "width": 2, "category": "transport"},
    "🚜": {"name": "tractor", "width": 2, "category": "transport"},
    "🚝": {"name": "monorail", "width": 2, "category": "transport"},
    "🚞": {"name": "mountain_railway", "width": 2, "category": "transport"},
    "🚟": {"name": "suspension_railway", "width": 2, "category": "transport"},
    "🚠": {"name": "mountain_cableway", "width": 2, "category": "transport"},
    "🚡": {"name": "aerial_tramway", "width": 2, "category": "transport"},
    "🚢": {"name": "ship", "width": 2, "category": "transport"},
    "🚣": {"name": "rowboat", "width": 2, "category": "transport"},
    "🚤": {"name": "speedboat", "width": 2, "category": "transport"},
    "🚥": {"name": "horizontal_traffic_light", "width": 2, "category": "transport"},
    "🚦": {"name": "vertical_traffic_light", "width": 2, "category": "transport"},
    "🚧": {"name": "construction_sign", "width": 2, "category": "transport"},
    "🚨": {"name": "police_cars_revolving_light", "width": 2, "category": "transport"},
    "🚩": {"name": "triangular_flag_on_post", "width": 2, "category": "transport"},
    "🚪": {"name": "door", "width": 2, "category": "transport"},
    "🚫": {"name": "no_entry_sign", "width": 2, "category": "transport"},
    "🚬": {"name": "smoking_symbol", "width": 2, "category": "transport"},
    "🚭": {"name": "no_smoking_symbol", "width": 2, "category": "transport"},
    "🚮": {"name": "put_litter_in_its_place_symbol", "width": 2, "category": "transport"},
    "🚯": {"name": "do_not_litter_symbol", "width": 2, "category": "transport"},
    "🚰": {"name": "potable_water_symbol", "width": 2, "category": "transport"},
    "🚱": {"name": "non_potable_water_symbol", "width": 2, "category": "transport"},
    "🚲": {"name": "bicycle", "width": 2, "category": "transport"},
    "🚳": {"name": "no_bicycles", "width": 2, "category": "transport"},
    "🚴": {"name": "bicyclist", "width": 2, "category": "transport"},
    "🚵": {"name": "mountain_bicyclist", "width": 2, "category": "transport"},
    "🚶": {"name": "pedestrian", "width": 2, "category": "transport"},
    "🚷": {"name": "no_pedestrians", "width": 2, "category": "transport"},
    "🚸": {"name": "children_crossing", "width": 2, "category": "transport"},
    "🚹": {"name": "mens_symbol", "width": 2, "category": "transport"},
    "🚺": {"name": "womens_symbol", "width": 2, "category": "transport"},
    "🚻": {"name": "restroom", "width": 2, "category": "transport"},
    "🚼": {"name": "baby_symbol", "width": 2, "category": "transport"},
    "🚽": {"name": "toilet", "width": 2, "category": "transport"},
    "🚾": {"name": "water_closet", "width": 2, "category": "transport"},
    "🚿": {"name": "shower", "width": 2, "category": "transport"},
    "🛀": {"name": "bath", "width": 2, "category": "transport"},
    "🛁": {"name": "bathtub", "width": 2, "category": "transport"},
    "🛂": {"name": "passport_control", "width": 2, "category": "transport"},
    "🛃": {"name": "customs", "width": 2, "category": "transport"},
    "🛄": {"name": "baggage_claim", "width": 2, "category": "transport"},
    "🛅": {"name": "left_luggage", "width": 2, "category": "transport"},
    "🛌": {"name": "sleeping_accommodation", "width": 2, "category": "transport"},
    "🛐": {"name": "place_of_worship", "width": 2, "category": "transport"},
    "🛑": {"name": "octagonal_sign", "width": 2, "category": "transport"},
    "🛒": {"name": "shopping_trolley", "width": 2, "category": "transport"},
    "🛕": {"name": "hindu_temple", "width": 2, "category": "transport"},
    "🛖": {"name": "hut", "width": 2, "category": "transport"},
    "🛗": {"name": "elevator", "width": 2, "category": "transport"},
    "🛜": {"name": "wireless", "width": 2, "category": "transport"},
    "🛝": {"name": "playground_slide", "width": 2, "category": "transport"},
    "🛞": {"name": "wheel", "width": 2, "category": "transport"},
    "🛟": {"name": "ring_buoy", "width": 2, "category": "transport"},
    "🛫": {"name": "airplane_departure", "width": 2, "category": "transport"},
    "🛬": {"name": "airplane_arriving", "width": 2, "category": "transport"},
    "🛴": {"name": "scooter", "width": 2, "category": "transport"},
    "🛵": {"name": "motor_scooter", "width": 2, "category": "transport"},
    "🛶": {"name": "canoe", "width": 2, "category": "transport"},
    "🛷": {"name": "sled", "width": 2, "category": "transport"},
    "🛸": {"name": "flying_saucer", "width": 2, "category": "transport"},
    "🛹": {"name": "skateboard", "width": 2, "category": "transport"},
    "🛺": {"name": "auto_rickshaw", "width": 2, "category": "transport"},
    "🛻": {"name": "pickup_truck", "width": 2, "category": "transport"},
    "🛼": {"name": "roller_skate", "width": 2, "category": "transport"},
    "🤌": {"name": "pinched_fingers", "width": 2, "category": "supplemental"},
    "🤍": {"name": "white_heart", "width": 2, "category": "supplemental"},
    "🤎": {"name": "brown_heart", "width": 2, "category": "supplemental"},
    "🤏": {"name": "pinching_hand", "width": 2, "category": "supplemental"},
    "🤐": {"name": "zipper_mouth_face", "width": 2, "category": "supplemental"},
    "🤑": {"name": "money_mouth_face", "width": 2, "category": "supplemental"},
    "🤒": {"name": "face_with_thermometer", "width": 2, "category": "supplemental"},
    "🤓": {"name": "nerd_face", "width": 2, "category": "supplemental"},
    "🤔": {"name": "thinking_face", "width": 2, "category": "supplemental"},
    "🤕": {"name": "face_with_head_bandage", "width": 2, "category": "supplemental"},
    "🤖": {"name": "robot_face", "width": 2, "category": "supplemental"},
    "🤗": {"name": "hugging_face", "width": 2, "category": "supplemental"},
    "🤘": {"name": "sign_of_the_horns", "width": 2, "category": "supplemental"},
    "🤙": {"name": "call_me_hand", "width": 2, "category": "supplemental"},
    "🤚": {"name": "raised_back_of_hand", "width": 2, "category": "supplemental"},
    "🤛": {"name": "left_facing_fist", "width": 2, "category": "supplemental"},
    "🤜": {"name": "right_facing_fist", "width": 2, "category": "supplemental"},
    "🤝": {"name": "handshake", "width": 2, "category": "supplemental"},
    "🤞": {
        "name": "hand_with_index_and_middle_fingers_crossed",
        "width": 2,
        "category": "supplemental",
    },
    "🤟": {"name": "i_love_you_hand_sign", "width": 2, "category": "supplemental"},
    "🤠": {"name": "face_with_cowboy_hat", "width": 2, "category": "supplemental"},
    "🤡": {"name": "clown_face", "width": 2, "category": "supplemental"},
    "🤢": {"name": "nauseated_face", "width": 2, "category": "supplemental"},
    "🤣": {"name": "rolling_on_the_floor_laughing", "width": 2, "category": "supplemental"},
    "🤤": {"name": "drooling_face", "width": 2, "category": "supplemental"},
    "🤥": {"name": "lying_face", "width": 2, "category": "supplemental"},
    "🤦": {"name": "face_palm", "width": 2, "category": "supplemental"},
    "🤧": {"name": "sneezing_face", "width": 2, "category": "supplemental"},
    "🤨": {"name": "face_with_one_eyebrow_raised", "width": 2, "category": "supplemental"},
    "🤩": {"name": "grinning_face_with_star_eyes", "width": 2, "category": "supplemental"},
    "🤪": {
        "name": "grinning_face_with_one_large_and_one_small_eye",
        "width": 2,
        "category": "supplemental",
    },
    "🤫": {"name": "face_with_finger_covering_closed_lips", "width": 2, "category": "supplemental"},
    "🤬": {
        "name": "serious_face_with_symbols_covering_mouth",
        "width": 2,
        "category": "supplemental",
    },
    "🤭": {
        "name": "smiling_face_with_smiling_eyes_and_hand_covering_mouth",
        "width": 2,
        "category": "supplemental",
    },
    "🤮": {"name": "face_with_open_mouth_vomiting", "width": 2, "category": "supplemental"},
    "🤯": {"name": "shocked_face_with_exploding_head", "width": 2, "category": "supplemental"},
    "🤰": {"name": "pregnant_woman", "width": 2, "category": "supplemental"},
    "🤱": {"name": "breast_feeding", "width": 2, "category": "supplemental"},
    "🤲": {"name": "palms_up_together", "width": 2, "category": "supplemental"},
    "🤳": {"name": "selfie", "width": 2, "category": "supplemental"},
    "🤴": {"name": "prince", "width": 2, "category": "supplemental"},
    "🤵": {"name": "man_in_tuxedo", "width": 2, "category": "supplemental"},
    "🤶": {"name": "mother_christmas", "width": 2, "category": "supplemental"},
    "🤷": {"name": "shrug", "width": 2, "category": "supplemental"},
    "🤸": {"name": "person_doing_cartwheel", "width": 2, "category": "supplemental"},
    "🤹": {"name": "juggling", "width": 2, "category": "supplemental"},
    "🤺": {"name": "fencer", "width": 2, "category": "supplemental"},
    "🤼": {"name": "wrestlers", "width": 2, "category": "supplemental"},
    "🤽": {"name": "water_polo", "width": 2, "category": "supplemental"},
    "🤾": {"name": "handball", "width": 2, "category": "supplemental"},
    "🤿": {"name": "diving_mask", "width": 2, "category": "supplemental"},
    "🥀": {"name": "wilted_flower", "width": 2, "category": "supplemental"},
    "🥁": {"name": "drum_with_drumsticks", "width": 2, "category": "supplemental"},
    "🥂": {"name": "clinking_glasses", "width": 2, "category": "supplemental"},
    "🥃": {"name": "tumbler_glass", "width": 2, "category": "supplemental"},
    "🥄": {"name": "spoon", "width": 2, "category": "supplemental"},
    "🥅": {"name": "goal_net", "width": 2, "category": "supplemental"},
    "🥇": {"name": "first_place_medal", "width": 2, "category": "supplemental"},
    "🥈": {"name": "second_place_medal", "width": 2, "category": "supplemental"},
    "🥉": {"name": "third_place_medal", "width": 2, "category": "supplemental"},
    "🥊": {"name": "boxing_glove", "width": 2, "category": "supplemental"},
    "🥋": {"name": "martial_arts_uniform", "width": 2, "category": "supplemental"},
    "🥌": {"name": "curling_stone", "width": 2, "category": "supplemental"},
    "🥍": {"name": "lacrosse_stick_and_ball", "width": 2, "category": "supplemental"},
    "🥎": {"name": "softball", "width": 2, "category": "supplemental"},
    "🥏": {"name": "flying_disc", "width": 2, "category": "supplemental"},
    "🥐": {"name": "croissant", "width": 2, "category": "supplemental"},
    "🥑": {"name": "avocado", "width": 2, "category": "supplemental"},
    "🥒": {"name": "cucumber", "width": 2, "category": "supplemental"},
    "🥓": {"name": "bacon", "width": 2, "category": "supplemental"},
    "🥔": {"name": "potato", "width": 2, "category": "supplemental"},
    "🥕": {"name": "carrot", "width": 2, "category": "supplemental"},
    "🥖": {"name": "baguette_bread", "width": 2, "category": "supplemental"},
    "🥗": {"name": "green_salad", "width": 2, "category": "supplemental"},
    "🥘": {"name": "shallow_pan_of_food", "width": 2, "category": "supplemental"},
    "🥙": {"name": "stuffed_flatbread", "width": 2, "category": "supplemental"},
    "🥚": {"name": "egg", "width": 2, "category": "supplemental"},
    "🥛": {"name": "glass_of_milk", "width": 2, "category": "supplemental"},
    "🥜": {"name": "peanuts", "width": 2, "category": "supplemental"},
    "🥝": {"name": "kiwifruit", "width": 2, "category": "supplemental"},
    "🥞": {"name": "pancakes", "width": 2, "category": "supplemental"},
    "🥟": {"name": "dumpling", "width": 2, "category": "supplemental"},
    "🥠": {"name": "fortune_cookie", "width": 2, "category": "supplemental"},
    "🥡": {"name": "takeout_box", "width": 2, "category": "supplemental"},
    "🥢": {"name": "chopsticks", "width": 2, "category": "supplemental"},
    "🥣": {"name": "bowl_with_spoon", "width": 2, "category": "supplemental"},
    "🥤": {"name": "cup_with_straw", "width": 2, "category": "supplemental"},
    "🥥": {"name": "coconut", "width": 2, "category": "supplemental"},
    "🥦": {"name": "broccoli", "width": 2, "category": "supplemental"},
    "🥧": {"name": "pie", "width": 2, "category": "supplemental"},
    "🥨": {"name": "pretzel", "width": 2, "category": "supplemental"},
    "🥩": {"name": "cut_of_meat", "width": 2, "category": "supplemental"},
    "🥪": {"name": "sandwich", "width": 2, "category": "supplemental"},
    "🥫": {"name": "canned_food", "width": 2, "category": "supplemental"},
    "🥬": {"name": "leafy_green", "width": 2, "category": "supplemental"},
    "🥭": {"name": "mango", "width": 2, "category": "supplemental"},
    "🥮": {"name": "moon_cake", "width": 2, "category": "supplemental"},
    "🥯": {"name": "bagel", "width": 2, "category": "supplemental"},
    "🥰": {
        "name": "smiling_face_with_smiling_eyes_and_three_hearts",
        "width": 2,
        "category": "supplemental",
    },
    "🥱": {"name": "yawning_face", "width": 2, "category": "supplemental"},
    "🥲": {"name": "smiling_face_with_tear", "width": 2, "category": "supplemental"},
    "🥳": {"name": "face_with_party_horn_and_party_hat", "width": 2, "category": "supplemental"},
    "🥴": {"name": "face_with_uneven_eyes_and_wavy_mouth", "width": 2, "category": "supplemental"},
    "🥵": {"name": "overheated_face", "width": 2, "category": "supplemental"},
    "🥶": {"name": "freezing_face", "width": 2, "category": "supplemental"},
    "🥷": {"name": "ninja", "width": 2, "category": "supplemental"},
    "🥸": {"name": "disguised_face", "width": 2, "category": "supplemental"},
    "🥹": {"name": "face_holding_back_tears", "width": 2, "category": "supplemental"},
    "🥺": {"name": "face_with_pleading_eyes", "width": 2, "category": "supplemental"},
    "🥻": {"name": "sari", "width": 2, "category": "supplemental"},
    "🥼": {"name": "lab_coat", "width": 2, "category": "supplemental"},
    "🥽": {"name": "goggles", "width": 2, "category": "supplemental"},
    "🥾": {"name": "hiking_boot", "width": 2, "category": "supplemental"},
    "🥿": {"name": "flat_shoe", "width": 2, "category": "supplemental"},
    "🦀": {"name": "crab", "width": 2, "category": "supplemental"},
    "🦁": {"name": "lion_face", "width": 2, "category": "supplemental"},
    "🦂": {"name": "scorpion", "width": 2, "category": "supplemental"},
    "🦃": {"name": "turkey", "width": 2, "category": "supplemental"},
    "🦄": {"name": "unicorn_face", "width": 2, "category": "supplemental"},
    "🦅": {"name": "eagle", "width": 2, "category": "supplemental"},
    "🦆": {"name": "duck", "width": 2, "category": "supplemental"},
    "🦇": {"name": "bat", "width": 2, "category": "supplemental"},
    "🦈": {"name": "shark", "width": 2, "category": "supplemental"},
    "🦉": {"name": "owl", "width": 2, "category": "supplemental"},
    "🦊": {"name": "fox_face", "width": 2, "category": "supplemental"},
    "🦋": {"name": "butterfly", "width": 2, "category": "supplemental"},
    "🦌": {"name": "deer", "width": 2, "category": "supplemental"},
    "🦍": {"name": "gorilla", "width": 2, "category": "supplemental"},
    "🦎": {"name": "lizard", "width": 2, "category": "supplemental"},
    "🦏": {"name": "rhinoceros", "width": 2, "category": "supplemental"},
    "🦐": {"name": "shrimp", "width": 2, "category": "supplemental"},
    "🦑": {"name": "squid", "width": 2, "category": "supplemental"},
    "🦒": {"name": "giraffe_face", "width": 2, "category": "supplemental"},
    "🦓": {"name": "zebra_face", "width": 2, "category": "supplemental"},
    "🦔": {"name": "hedgehog", "width": 2, "category": "supplemental"},
    "🦕": {"name": "sauropod", "width": 2, "category": "supplemental"},
    "🦖": {"name": "t_rex", "width": 2, "category": "supplemental"},
    "🦗": {"name": "cricket", "width": 2, "category": "supplemental"},
    "🦘": {"name": "kangaroo", "width": 2, "category": "supplemental"},
    "🦙": {"name": "llama", "width": 2, "category": "supplemental"},
    "🦚": {"name": "peacock", "width": 2, "category": "supplemental"},
    "🦛": {"name": "hippopotamus", "width": 2, "category": "supplemental"},
    "🦜": {"name": "parrot", "width": 2, "category": "supplemental"},
    "🦝": {"name": "raccoon", "width": 2, "category": "supplemental"},
    "🦞": {"name": "lobster", "width": 2, "category": "supplemental"},
    "🦟": {"name": "mosquito", "width": 2, "category": "supplemental"},
    "🦠": {"name": "microbe", "width": 2, "category": "supplemental"},
    "🦡": {"name": "badger", "width": 2, "category": "supplemental"},
    "🦢": {"name": "swan", "width": 2, "category": "supplemental"},
    "🦣": {"name": "mammoth", "width": 2, "category": "supplemental"},
    "🦤": {"name": "dodo", "width": 2, "category": "supplemental"},
    "🦥": {"name": "sloth", "width": 2, "category": "supplemental"},
    "🦦": {"name": "otter", "width": 2, "category": "supplemental"},
    "🦧": {"name": "orangutan", "width": 2, "category": "supplemental"},
    "🦨": {"name": "skunk", "width": 2, "category": "supplemental"},
    "🦩": {"name": "flamingo", "width": 2, "category": "supplemental"},
    "🦪": {"name": "oyster", "width": 2, "category": "supplemental"},
    "🦫": {"name": "beaver", "width": 2, "category": "supplemental"},
    "🦬": {"name": "bison", "width": 2, "category": "supplemental"},
    "🦭": {"name": "seal", "width": 2, "category": "supplemental"},
    "🦮": {"name": "guide_dog", "width": 2, "category": "supplemental"},
    "🦯": {"name": "probing_cane", "width": 2, "category": "supplemental"},
    "🦰": {"name": "emoji_component_red_hair", "width": 2, "category": "supplemental"},
    "🦱": {"name": "emoji_component_curly_hair", "width": 2, "category": "supplemental"},
    "🦲": {"name": "emoji_component_bald", "width": 2, "category": "supplemental"},
    "🦳": {"name": "emoji_component_white_hair", "width": 2, "category": "supplemental"},
    "🦴": {"name": "bone", "width": 2, "category": "supplemental"},
    "🦵": {"name": "leg", "width": 2, "category": "supplemental"},
    "🦶": {"name": "foot", "width": 2, "category": "supplemental"},
    "🦷": {"name": "tooth", "width": 2, "category": "supplemental"},
    "🦸": {"name": "superhero", "width": 2, "category": "supplemental"},
    "🦹": {"name": "supervillain", "width": 2, "category": "supplemental"},
    "🦺": {"name": "safety_vest", "width": 2, "category": "supplemental"},
    "🦻": {"name": "ear_with_hearing_aid", "width": 2, "category": "supplemental"},
    "🦼": {"name": "motorized_wheelchair", "width": 2, "category": "supplemental"},
    "🦽": {"name": "manual_wheelchair", "width": 2, "category": "supplemental"},
    "🦾": {"name": "mechanical_arm", "width": 2, "category": "supplemental"},
    "🦿": {"name": "mechanical_leg", "width": 2, "category": "supplemental"},
    "🧀": {"name": "cheese_wedge", "width": 2, "category": "supplemental"},
    "🧁": {"name": "cupcake", "width": 2, "category": "supplemental"},
    "🧂": {"name": "salt_shaker", "width": 2, "category": "supplemental"},
    "🧃": {"name": "beverage_box", "width": 2, "category": "supplemental"},
    "🧄": {"name": "garlic", "width": 2, "category": "supplemental"},
    "🧅": {"name": "onion", "width": 2, "category": "supplemental"},
    "🧆": {"name": "falafel", "width": 2, "category": "supplemental"},
    "🧇": {"name": "waffle", "width": 2, "category": "supplemental"},
    "🧈": {"name": "butter", "width": 2, "category": "supplemental"},
    "🧉": {"name": "mate_drink", "width": 2, "category": "supplemental"},
    "🧊": {"name": "ice_cube", "width": 2, "category": "supplemental"},
    "🧋": {"name": "bubble_tea", "width": 2, "category": "supplemental"},
    "🧌": {"name": "troll", "width": 2, "category": "supplemental"},
    "🧍": {"name": "standing_person", "width": 2, "category": "supplemental"},
    "🧎": {"name": "kneeling_person", "width": 2, "category": "supplemental"},
    "🧏": {"name": "deaf_person", "width": 2, "category": "supplemental"},
    "🧐": {"name": "face_with_monocle", "width": 2, "category": "supplemental"},
    "🧑": {"name": "adult", "width": 2, "category": "supplemental"},
    "🧒": {"name": "child", "width": 2, "category": "supplemental"},
    "🧓": {"name": "older_adult", "width": 2, "category": "supplemental"},
    "🧔": {"name": "bearded_person", "width": 2, "category": "supplemental"},
    "🧕": {"name": "person_with_headscarf", "width": 2, "category": "supplemental"},
    "🧖": {"name": "person_in_steamy_room", "width": 2, "category": "supplemental"},
    "🧗": {"name": "person_climbing", "width": 2, "category": "supplemental"},
    "🧘": {"name": "person_in_lotus_position", "width": 2, "category": "supplemental"},
    "🧙": {"name": "mage", "width": 2, "category": "supplemental"},
    "🧚": {"name": "fairy", "width": 2, "category": "supplemental"},
    "🧛": {"name": "vampire", "width": 2, "category": "supplemental"},
    "🧜": {"name": "merperson", "width": 2, "category": "supplemental"},
    "🧝": {"name": "elf", "width": 2, "category": "supplemental"},
    "🧞": {"name": "genie", "width": 2, "category": "supplemental"},
    "🧟": {"name": "zombie", "width": 2, "category": "supplemental"},
    "🧠": {"name": "brain", "width": 2, "category": "supplemental"},
    "🧡": {"name": "orange_heart", "width": 2, "category": "supplemental"},
    "🧢": {"name": "billed_cap", "width": 2, "category": "supplemental"},
    "🧣": {"name": "scarf", "width": 2, "category": "supplemental"},
    "🧤": {"name": "gloves", "width": 2, "category": "supplemental"},
    "🧥": {"name": "coat", "width": 2, "category": "supplemental"},
    "🧦": {"name": "socks", "width": 2, "category": "supplemental"},
    "🧧": {"name": "red_gift_envelope", "width": 2, "category": "supplemental"},
    "🧨": {"name": "firecracker", "width": 2, "category": "supplemental"},
    "🧩": {"name": "jigsaw_puzzle_piece", "width": 2, "category": "supplemental"},
    "🧪": {"name": "test_tube", "width": 2, "category": "supplemental"},
    "🧫": {"name": "petri_dish", "width": 2, "category": "supplemental"},
    "🧬": {"name": "dna_double_helix", "width": 2, "category": "supplemental"},
    "🧭": {"name": "compass", "width": 2, "category": "supplemental"},
    "🧮": {"name": "abacus", "width": 2, "category": "supplemental"},
    "🧯": {"name": "fire_extinguisher", "width": 2, "category": "supplemental"},
    "🧰": {"name": "toolbox", "width": 2, "category": "supplemental"},
    "🧱": {"name": "brick", "width": 2, "category": "supplemental"},
    "🧲": {"name": "magnet", "width": 2, "category": "supplemental"},
    "🧳": {"name": "luggage", "width": 2, "category": "supplemental"},
    "🧴": {"name": "lotion_bottle", "width": 2, "category": "supplemental"},
    "🧵": {"name": "spool_of_thread", "width": 2, "category": "supplemental"},
    "🧶": {"name": "ball_of_yarn", "width": 2, "category": "supplemental"},
    "🧷": {"name": "safety_pin", "width": 2, "category": "supplemental"},
    "🧸": {"name": "teddy_bear", "width": 2, "category": "supplemental"},
    "🧹": {"name": "broom", "width": 2, "category": "supplemental"},
    "🧺": {"name": "basket", "width": 2, "category": "supplemental"},
    "🧻": {"name": "roll_of_paper", "width": 2, "category": "supplemental"},
    "🧼": {"name": "bar_of_soap", "width": 2, "category": "supplemental"},
    "🧽": {"name": "sponge", "width": 2, "category": "supplemental"},
    "🧾": {"name": "receipt", "width": 2, "category": "supplemental"},
    "🧿": {"name": "nazar_amulet", "width": 2, "category": "supplemental"},
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
        "terminal_safe": False,
        "recommendation": "Unknown emoji",
    }

    # Check if in safe list
    if emoji in SAFE_EMOJIS:
        info = SAFE_EMOJIS[emoji]
        terminal_safe = info.get("terminal_safe", True)  # Default True for non-VS16
        result.update(
            {
                "safe": True,
                "name": info.get("name", "unknown"),
                "width": info.get("width", 2),
                "category": info.get("category", "other"),
                "has_vs16": info.get("has_vs16", False),
                "terminal_safe": terminal_safe,
                "recommendation": "✅ Safe to use",
            }
        )
        if result["has_vs16"] and not terminal_safe:
            result["recommendation"] = (
                "✅ Safe to use (VS16 - automatic spacing adjustment applied)"
            )
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


def get_safe_emojis(category: str | None = None, terminal_safe_only: bool = False) -> dict:
    """Get safe emojis, optionally filtered by category and terminal safety.

    Args:
        category: Optional category name to filter by
                 (e.g., 'status', 'tech', 'nature', 'food', 'activity')
                 If None, returns all safe emojis.
        terminal_safe_only: If True, excludes VS16 emojis that have terminal
                           rendering issues (render as width 1 in some terminals).
                           Default False returns all safe emojis.

    Returns:
        Dictionary of emoji -> info mappings

    Example:
        >>> status_emojis = get_safe_emojis("status")
        >>> "✅" in status_emojis
        True
        >>> # Get only terminal-safe emojis (excludes VS16)
        >>> safe_emojis = get_safe_emojis(terminal_safe_only=True)
        >>> "⚠️" in safe_emojis  # VS16 emoji excluded
        False
        >>> len(get_safe_emojis())
        > 80
    """
    result = SAFE_EMOJIS.copy()

    if terminal_safe_only:
        result = {
            emoji: info
            for emoji, info in result.items()
            if info.get("terminal_safe", True)  # Default True for non-VS16
        }

    if category is not None:
        result = {emoji: info for emoji, info in result.items() if info.get("category") == category}

    return result


def get_emoji_spacing_adjustment(emoji: str) -> int:
    """Get the number of extra spaces needed after an emoji for proper alignment.

    This function detects when an emoji's reported visual width doesn't match
    its actual terminal display width (due to grapheme cluster compositions
    and terminal rendering inconsistencies) and returns the adjustment needed.

    The detection logic:
    1. Checks if emoji is in safe list
    2. For VS16 emojis (terminal_safe=False, has_vs16=True): always returns 1
       because terminals render them as width 1 despite wcwidth reporting 2
    3. For other emojis: compares visual_width with metadata width

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

    # VS16 emojis need adjustment: terminals render them as width 1
    # despite wcwidth reporting width 2. This is the key fix.
    if info.get("has_vs16") and not info.get("terminal_safe", True):
        # VS16 emojis render as width 1 in terminals, but we want width 2
        # So we need 1 extra space to compensate
        return 1

    # Calculate visual width reported by wcwidth
    actual_visual_width = visual_width(emoji)

    # Determine if spacing adjustment is needed
    # If visual_width is less than metadata width, there's a mismatch that needs compensation.
    if actual_visual_width < metadata_width:
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
