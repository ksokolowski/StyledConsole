"""Text width calculation and grapheme handling utilities.

This module provides emoji-safe text width calculation and grapheme manipulation.
MVP (v0.1) focuses on Tier 1 emoji support (single-codepoint basic icons).
"""

import re

import emoji
import wcwidth
from rich.errors import MarkupError
from rich.text import Text as RichText

from styledconsole.types import AlignType

# Emoji Variation Selector-16 (U+FE0F) forces emoji presentation
VARIATION_SELECTOR_16 = "\ufe0f"

# ANSI escape sequence pattern (CSI sequences)
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


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


def _is_skin_tone_modifier(char: str) -> bool:
    """Check if character is a skin tone modifier (U+1F3FB to U+1F3FF)."""
    return 0x1F3FB <= ord(char) <= 0x1F3FF


def _grapheme_width_legacy(grapheme: str) -> int:
    """Calculate width in legacy mode (sum of parts)."""
    g_width = 0
    for char in grapheme:
        if _is_skin_tone_modifier(char):
            g_width += 2
        elif char == VARIATION_SELECTOR_16 or char == "\u200d":
            continue
        else:
            w = wcwidth.wcwidth(char)
            g_width += w if w >= 0 else 1
    return g_width


def _grapheme_width_standard(grapheme: str) -> int:
    """Calculate width in standard mode."""
    if "\u200d" in grapheme:
        return 2  # ZWJ sequences are always width 2
    if VARIATION_SELECTOR_16 in grapheme:
        return 1  # VS16 emojis render as width 1 in terminals
    w = wcwidth.wcswidth(grapheme)
    return w if w >= 0 else 1


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
        import contextlib

        with contextlib.suppress(MarkupError):
            # Parse markup to get plain text for width calculation
            # We use Rich to strip tags and handle entities
            clean_text = RichText.from_markup(clean_text).plain

    # Split into graphemes to handle complex sequences correctly
    graphemes = split_graphemes(clean_text)
    legacy_mode = _is_legacy_emoji_mode()

    width = 0
    for g in graphemes:
        if legacy_mode and (len(g) > 1 or any(_is_skin_tone_modifier(c) for c in g)):
            width += _grapheme_width_legacy(g)
        else:
            width += _grapheme_width_standard(g)

    return width


def _parse_ansi_sequence(text: str, start: int) -> tuple[str, int]:
    """Parse ANSI escape sequence starting at position start.

    Returns:
        Tuple of (ansi_code, end_position)
    """
    end = start + 2
    n = len(text)
    while end < n and not text[end].isalpha():
        end += 1
    if end < n:
        end += 1
    return text[start:end], end


def _should_extend_grapheme(current: str, char: str) -> bool:
    """Check if char should extend the current grapheme cluster."""
    if not current:
        return False
    prev_char = current[-1]

    # VS16 (Variation Selector-16) extends previous
    if char == VARIATION_SELECTOR_16:
        return True
    # ZWJ (Zero Width Joiner) extends previous
    if char == "\u200d":
        return True
    # If previous was ZWJ, this char extends it (emoji sequence)
    if prev_char == "\u200d":
        return True
    # Skin tone modifiers extend previous
    return bool(_is_skin_tone_modifier(char))


def split_graphemes(text: str) -> list[str]:
    """Split text into grapheme clusters.

    Handles:
    - Regular ASCII characters
    - ANSI escape sequences (kept with preceding content or standalone)
    - ZWJ sequences (e.g. 👨‍💻)
    - VS16 sequences (e.g. ⚠️)
    - Skin tone modifiers (e.g. 👋🏻)
    """
    graphemes: list[str] = []
    current_grapheme = ""
    i = 0
    n = len(text)

    while i < n:
        # Check for ANSI escape sequence
        if text[i] == "\x1b" and i + 1 < n and text[i + 1] == "[":
            ansi_code, i = _parse_ansi_sequence(text, i)
            # Attach ANSI to current grapheme or previous
            if current_grapheme:
                current_grapheme += ansi_code
            elif graphemes:
                graphemes[-1] += ansi_code
            else:
                graphemes.append(ansi_code)
            continue

        char = text[i]

        if _should_extend_grapheme(current_grapheme, char):
            current_grapheme += char
        elif not current_grapheme:
            current_grapheme = char
        else:
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
        except MarkupError:
            # Invalid markup syntax - fall through to standard truncation
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
    """Normalize content to list of lines."""
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


def validate_emoji(emoji_char: str) -> dict:
    """Validate an emoji for safe usage in StyledConsole.

    Checks if emoji is a valid Unicode emoji and returns detailed information
    about its properties and potential rendering issues.

    Args:
        emoji_char: Single emoji character or emoji+variation selector sequence

    Returns:
        Dictionary with keys:
        - 'safe': bool - Whether emoji is considered safe
        - 'name': str - Human-readable name
        - 'width': int - Display width (usually 2)
        - 'category': str - Always "unknown" (category data not available in dynamic mode)
        - 'has_vs16': bool - Whether emoji includes variation selector
        - 'recommendation': str - Any warnings or recommendations
    """
    result: dict[str, str | bool | int | None] = {
        "safe": False,
        "name": None,
        "width": None,
        "category": "unknown",
        "has_vs16": False,
        "terminal_safe": False,
        "recommendation": "Unknown emoji",
    }

    if not emoji.is_emoji(emoji_char):
        result["recommendation"] = "❓ Unknown/Invalid emoji. Use at your own risk."
        return result

    # Identify metadata using emoji package
    data = emoji.EMOJI_DATA.get(emoji_char, {})
    name = data.get("en", "").strip(":").replace("_", " ")

    has_vs16 = VARIATION_SELECTOR_16 in emoji_char
    is_zwj = "\u200d" in emoji_char
    # Check for skin tone modifiers
    has_skin_tone = any(0x1F3FB <= ord(c) <= 0x1F3FF for c in emoji_char)
    width = 2  # Standard emoji width

    # Determine safety
    terminal_safe = True
    safe = True
    recommendation = "✅ Safe to use"

    if is_zwj:
        terminal_safe = False
        result["recommendation"] = (
            "❌ ZWJ sequence detected. These are not supported in v0.1. "
            "Use simple single-codepoint emojis instead."
        )
        # We consider ZWJ unsafe for now in this validation
        safe = False

    elif has_skin_tone:
        terminal_safe = False
        result["recommendation"] = (
            "❌ Skin tone modifier detected. "
            "Tier 2 emojis are not supported in v0.1. "
            "Use base emoji without skin tone."
        )
        safe = False

    elif has_vs16:
        terminal_safe = False  # VS16 often renders width 1
        result["recommendation"] = (
            "⚠️ Variation selector (U+FE0F) detected. "
            "This emoji may render with width 1 in some terminals. "
            "Automatic adjustment will apply."
        )
        recommendation = str(result["recommendation"])

    # If it passed ZWJ/Skin tone checks, it's generally "safe" in our dict sense
    # but VS16 is a special case of "safe but needs adjustment"
    if safe:
        result.update(
            {
                "safe": True,
                "name": name,
                "width": width,
                "category": "unknown",
                "has_vs16": has_vs16,
                "terminal_safe": terminal_safe,
                "recommendation": recommendation,
            }
        )

    return result


def get_safe_emojis(category: str | None = None, terminal_safe_only: bool = False) -> dict:
    """Get safe emojis, explicitly constructed from emoji package.

    Approximates the old Tier 1 list by filtering for single-codepoint emojis.
    Note: 'category' filtering is not supported in dynamic mode and will return empty if set.
    """
    if category is not None:
        # We don't have category data in dynamic emoji package easily mapped to our old categories
        return {}

    result = {}
    # Iterate all emojis - this might be slow, so we limit to short sequences
    for char, data in emoji.EMOJI_DATA.items():
        if "en" not in data:
            continue

        # Filter for Tier 1 approximation:
        # - No ZWJ
        # - No modifiers/skin tones (checking length of codepoints helps, but isn't perfect)
        # Simple heuristic: len(char) <= 2 (some have VS16 so length 2)
        if len(char) > 2:
            continue

        # Or better check explicit forbidden chars
        if "\u200d" in char:
            continue

        has_skin_tone = any(0x1F3FB <= ord(c) <= 0x1F3FF for c in char)
        if has_skin_tone:
            continue

        has_vs16 = VARIATION_SELECTOR_16 in char
        terminal_safe = not has_vs16

        if terminal_safe_only and not terminal_safe:
            continue

        name = data["en"].strip(":").replace("_", " ")

        result[char] = {
            "name": name,
            "width": 2,
            "category": "unknown",
            "has_vs16": has_vs16,
            "terminal_safe": terminal_safe,
        }

    return result


def get_emoji_spacing_adjustment(emoji_char: str) -> int:
    """Get the number of extra spaces needed after an emoji for proper alignment.

    Args:
        emoji_char: Single emoji or emoji+modifiers sequence

    Returns:
        Number of extra spaces to add after emoji (0, 1, or 2)
    """
    # Simply use visual_width logic vs expected width (2)
    # Plus explicit VS16 check

    if not emoji.is_emoji(emoji_char):
        raise ValueError(f"Invalid emoji: {emoji_char!r}")

    # VS16 emojis need adjustment: terminals render them as width 1
    # despite wcwidth reporting width 2.
    if VARIATION_SELECTOR_16 in emoji_char:
        return 1

    metadata_width = 2
    actual_visual_width = visual_width(emoji_char)

    if actual_visual_width < metadata_width:
        adjustment = metadata_width - actual_visual_width
        return min(adjustment, 2)

    return 0


def format_emoji_with_spacing(emoji: str, text: str = "", sep: str = " ") -> str:
    """Format emoji with automatic spacing adjustment."""
    if not text:
        return emoji

    adjustment = get_emoji_spacing_adjustment(emoji)
    total_spaces = len(sep) + adjustment

    return emoji + (" " * total_spaces) + text


def _collect_vs16_emojis() -> set[str]:
    """Collect likely VS16 emojis dynamically."""
    # This is expensive to scan all emojis every time.
    # Use a cached set or just minimal common ones?
    # For dynamic approach, we can't easily pre-compute.
    # We return an empty set here because we rely on dynamic check in adjust_emoji_spacing_in_text pattern
    # actually, adjust_emoji_spacing_in_text USES this set to build a regex.
    # So we MUST return something useful or change the regex strategy.

    # If we return ALL VS16 emojis from the 4000+ list, the regex will be huge.
    # Maybe we only care about emojis actually IN the text?
    # adjust_emoji_spacing_in_text logic needs to be inverted: scan text, find emojis, check if VS16.
    return set()


def _assume_vs16_enabled() -> bool:
    """Determine if we should assume VS16 emojis glue by default."""
    import os as _os

    val = _os.getenv("STYLEDCONSOLE_ASSUME_VS16")
    if val is None:
        return True
    val_lower = str(val).lower().strip()
    return val_lower not in ("", "0", "false", "no")


def default_gluing_emojis() -> set[str]:
    """Default set of emojis to adjust when gluing_emojis is not provided."""
    return _collect_vs16_emojis() if _assume_vs16_enabled() else set()


def adjust_emoji_spacing_in_text(
    text: str,
    separator: str = " ",
    *,
    gluing_emojis: set[str] | None = None,
) -> str:
    """Adjust spacing after emojis inside arbitrary text.

    Modified to work dynamically without a pre-computed safe list.
    """
    if not text or separator == "":
        return text

    # New implementation pattern:
    # 1. Detect all emojis in text
    # 2. Iterate and replace if they need adjustment

    # Using emoji package to find locations
    emoji_list = emoji.emoji_list(text)
    if not emoji_list:
        return text

    # Process from end to start to maintain indices
    # Or just use replace? Replace all occurrences of specific emojis found?
    # Text might contain SAME emoji multiple times.

    # Let's use a robust approach: find unique emojis in text, check adjustment, replace.
    unique_emojis = {match["emoji"] for match in emoji_list}

    # Filter for those that need adjustment
    to_adjust = set()
    for char in unique_emojis:
        if gluing_emojis and char not in gluing_emojis:
            continue

        # Check if needs adjustment
        # Warning: get_emoji_spacing_adjustment uses visual_width which calls split_graphemes...
        try:
            adj = get_emoji_spacing_adjustment(char)
            if adj > 0:
                to_adjust.add(char)
        except ValueError:
            pass

    if not to_adjust:
        return text

    import re as _re

    alt = "|".join(_re.escape(e) for e in sorted(to_adjust, key=len, reverse=True))
    pattern = _re.compile(rf"(?P<emo>{alt}){_re.escape(separator)}(?=\S)")

    def _repl(m: "_re.Match[str]") -> str:
        emo = m.group("emo")
        # We know adjustment > 0
        try:
            adj = get_emoji_spacing_adjustment(emo)
            return emo + (separator * (1 + adj))
        except ValueError:
            return m.group(0)

    return pattern.sub(_repl, text)


__all__ = [
    "AlignType",
    "adjust_emoji_spacing_in_text",
    "default_gluing_emojis",
    "format_emoji_with_spacing",
    "get_emoji_spacing_adjustment",
    "get_safe_emojis",
    "normalize_content",
    "pad_to_width",
    "split_graphemes",
    "strip_ansi",
    "truncate_to_width",
    "validate_emoji",
    "visual_width",
]
