"""Export functionality for Console output.

This module provides export capabilities for recorded console output:
- HTML export (built-in)
- Plain text export (built-in)
- Image export (requires Pillow - install with styledconsole[image])
- Emoji rendering for images (requires Pillow)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .emoji_renderer import BaseEmojiSource, EmojiRenderer
    from .image_exporter import ImageExporter, ImageTheme


def get_image_exporter() -> type[ImageExporter]:
    """Get the ImageExporter class (lazy load).

    Returns:
        ImageExporter class.

    Raises:
        ImportError: If Pillow is not installed.

    Example:
        >>> ImageExporter = get_image_exporter()
        >>> exporter = ImageExporter(rich_console)
        >>> exporter.save_png("output.png")
    """
    try:
        from .image_exporter import ImageExporter

        return ImageExporter
    except ImportError as e:
        raise ImportError(
            "Image export requires Pillow. Install with: pip install styledconsole[image]"
        ) from e


def get_image_theme() -> type[ImageTheme]:
    """Get the ImageTheme class (lazy load).

    Returns:
        ImageTheme class.

    Raises:
        ImportError: If Pillow is not installed.
    """
    try:
        from .image_exporter import ImageTheme

        return ImageTheme
    except ImportError as e:
        raise ImportError(
            "Image export requires Pillow. Install with: pip install styledconsole[image]"
        ) from e


def get_emoji_renderer() -> type[EmojiRenderer]:
    """Get the EmojiRenderer class (lazy load).

    Returns:
        EmojiRenderer class.

    Raises:
        ImportError: If Pillow is not installed.
    """
    try:
        from .emoji_renderer import EmojiRenderer

        return EmojiRenderer
    except ImportError as e:
        raise ImportError(
            "Emoji rendering requires Pillow. Install with: pip install styledconsole[image]"
        ) from e


def get_emoji_source(style: str = "twemoji") -> BaseEmojiSource:
    """Get an emoji source by style name.

    Args:
        style: Emoji style - "twemoji", "apple", "google", "microsoft", "openmoji".

    Returns:
        BaseEmojiSource instance.

    Raises:
        ImportError: If Pillow is not installed.
        ValueError: If style is not recognized.
    """
    try:
        from .emoji_renderer import (
            AppleEmojiSource,
            GoogleEmojiSource,
            MicrosoftEmojiSource,
            OpenmojiSource,
            TwemojiSource,
        )

        sources = {
            "twemoji": TwemojiSource,
            "twitter": TwemojiSource,
            "apple": AppleEmojiSource,
            "google": GoogleEmojiSource,
            "microsoft": MicrosoftEmojiSource,
            "openmoji": OpenmojiSource,
        }

        if style.lower() not in sources:
            raise ValueError(
                f"Unknown emoji style: {style}. Available: {', '.join(sources.keys())}"
            )

        return sources[style.lower()]()
    except ImportError as e:
        raise ImportError(
            "Emoji rendering requires Pillow. Install with: pip install styledconsole[image]"
        ) from e


__all__ = [
    "get_emoji_renderer",
    "get_emoji_source",
    "get_image_exporter",
    "get_image_theme",
]
