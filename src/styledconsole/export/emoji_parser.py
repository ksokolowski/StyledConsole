"""Text parsing utilities for emoji detection.

This module provides text parsing capabilities to identify and separate
emoji characters from regular text content for image rendering.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import NamedTuple

__all__ = [
    "EMOJI_REGEX",
    "Node",
    "NodeType",
    "parse_text_with_emojis",
]


def _build_emoji_regex() -> re.Pattern[str]:
    """Build regex pattern to match emoji characters.

    Uses the central EMOJI registry as the source of truth.
    """
    try:
        from styledconsole.emoji_registry import EMOJI

        return re.compile(EMOJI.get_emoji_regex())
    except ImportError:
        # Fallback: empty pattern if something goes wrong
        return re.compile(r"(\x00)")  # Won't match anything useful


EMOJI_REGEX = _build_emoji_regex()


class NodeType(Enum):
    """Type of parsed text node."""

    TEXT = 0
    EMOJI = 1


class Node(NamedTuple):
    """A parsed text node containing either text or emoji content."""

    type: NodeType
    content: str


def parse_text_with_emojis(text: str) -> list[list[Node]]:
    """Parse text into nodes, separating emojis from regular text.

    Splits text by lines and identifies emoji vs text segments within each line.

    Args:
        text: Text to parse, may contain emoji characters.

    Returns:
        List of lines, each containing a list of Node objects.
        Each node is either TEXT or EMOJI type with its content.

    Example:
        >>> nodes = parse_text_with_emojis("Hello 🌍 World")
        >>> len(nodes)  # One line
        1
        >>> len(nodes[0])  # Three nodes: "Hello ", "🌍", " World"
        3
    """
    result = []
    for line in text.splitlines():
        nodes = []
        for i, chunk in enumerate(EMOJI_REGEX.split(line)):
            if not chunk:
                continue
            if i % 2 == 0:
                # Regular text (even indices after split)
                nodes.append(Node(NodeType.TEXT, chunk))
            else:
                # Emoji (odd indices - captured groups)
                nodes.append(Node(NodeType.EMOJI, chunk))
        result.append(nodes)
    return result
