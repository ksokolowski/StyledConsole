"""Emoji sanitization utilities for Rich wrappers.

This module provides shared functions for sanitizing emoji content
when rendering in terminals that don't support emoji display.

The sanitization converts emoji characters to their ASCII equivalents
with optional color markup for visual consistency.
"""

from __future__ import annotations

from typing import Any

from rich.markup import escape

from styledconsole.utils.icon_data import EMOJI_TO_ICON


def sanitize_emoji_content(content: Any, with_color: bool = True) -> Any:
    """Sanitize content by replacing emoji with ASCII equivalents.

    This function converts known emoji characters to their ASCII fallback
    representations, optionally applying Rich markup for color styling.

    Args:
        content: String content to sanitize. Non-string values are returned unchanged.
        with_color: Whether to apply color markup to ASCII replacements.
            When True, uses the color defined in EMOJI_TO_ICON mapping.
            When False, uses plain ASCII text.

    Returns:
        Sanitized content with emoji replaced by ASCII equivalents,
        or the original content if not a string.

    Example:
        >>> sanitize_emoji_content("Status: ✅ Done")
        'Status: [green][OK][/] Done'
        >>> sanitize_emoji_content("Status: ✅ Done", with_color=False)
        'Status: [OK] Done'
    """
    if not isinstance(content, str):
        return content

    result = content
    for emoji, mapping in EMOJI_TO_ICON.items():
        if emoji in result:
            if with_color and mapping.color:
                # Use Rich markup for color
                replacement = f"[{mapping.color}]{escape(mapping.ascii)}[/]"
            else:
                replacement = escape(mapping.ascii)
            result = result.replace(emoji, replacement)
    return result


__all__ = ["sanitize_emoji_content"]
