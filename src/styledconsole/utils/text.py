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

    Args:
        text: Text to truncate
        width: Maximum visual width
        suffix: Suffix to append when truncating (default: "...")

    Returns:
        Truncated text with suffix if needed

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

    # Build truncated string character by character
    clean_text = strip_ansi(text)
    result = []
    accumulated_width = 0

    for char in clean_text:
        char_width = wcwidth.wcwidth(char)
        if char_width == -1:
            char_width = 1

        if accumulated_width + char_width > target_width:
            break

        result.append(char)
        accumulated_width += char_width

    return "".join(result) + suffix


__all__ = [
    "visual_width",
    "strip_ansi",
    "split_graphemes",
    "pad_to_width",
    "truncate_to_width",
    "AlignType",
]
