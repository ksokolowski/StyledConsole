"""Text width calculation and grapheme handling utilities.

This module provides emoji-safe text width calculation and grapheme manipulation.
MVP (v0.1) focuses on Tier 1 emoji support (single-codepoint basic icons).
"""

import re

import wcwidth
from rich.errors import MarkupError
from rich.text import Text as RichText

from styledconsole.types import AlignType
from styledconsole.utils.emoji_data import (
    SAFE_EMOJIS,
    VARIATION_SELECTOR_16,
)

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
        elif char == VARIATION_SELECTOR_16:
            continue
        elif char == "\u200d":
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
        try:
            # Parse markup to get plain text for width calculation
            # We use Rich to strip tags and handle entities
            clean_text = RichText.from_markup(clean_text).plain
        except MarkupError:
            # Invalid markup syntax - fall through with original text
            pass

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
    if _is_skin_tone_modifier(char):
        return True
    return False


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
            except ValueError:
                # Invalid emoji - use default spacing
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
