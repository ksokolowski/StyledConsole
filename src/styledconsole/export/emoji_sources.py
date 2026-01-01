"""Emoji image sources for image export.

This module provides various sources for fetching emoji images,
including CDN-based sources and local font-based rendering.

Inspired by the pilmoji project (https://github.com/jay3332/pilmoji),
but rewritten from scratch to support emoji v2.x library.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from io import BytesIO
from typing import TYPE_CHECKING
from urllib.error import HTTPError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

if TYPE_CHECKING:
    from PIL import ImageFont as PILImageFont

__all__ = [
    "AppleEmojiSource",
    "BaseEmojiSource",
    "CDNEmojiSource",
    "GoogleEmojiSource",
    "MicrosoftEmojiSource",
    "NotoColorEmojiSource",
    "OpenmojiSource",
    "TwemojiSource",
]


# =============================================================================
# CDN Configuration
# =============================================================================

CDN_BASE_URL = "https://emojicdn.elk.sh"
"""Base URL for the emoji CDN service.

emojicdn.elk.sh provides emoji images in multiple styles.
It's a free service that serves PNG images of emojis.
"""

CDN_REQUEST_TIMEOUT_SECONDS = 10
"""HTTP request timeout for CDN requests in seconds.

10 seconds provides a reasonable balance between:
- Allowing slow connections to complete
- Not blocking too long on failed requests
"""

CDN_USER_AGENT = "Mozilla/5.0"
"""User-Agent header for CDN requests.

Some CDNs require a browser-like User-Agent to serve content.
"""


# =============================================================================
# NotoColorEmoji Font Configuration
# =============================================================================

NOTO_COLOR_EMOJI_FONT_SIZE = 109
"""Fixed font size for NotoColorEmoji rendering.

NotoColorEmoji is a bitmap font that only renders correctly
at specific sizes. 109px is the native size for the font.
Attempting to use other sizes may result in blurry or
incorrectly rendered emojis.
"""

NOTO_COLOR_EMOJI_PADDING = 40
"""Padding around emoji when rendering from font.

Extra space around the emoji ensures:
- No clipping of emoji edges
- Room for emoji variations (skin tones, etc.)
"""

NOTO_COLOR_EMOJI_CROP_MARGIN = 2
"""Margin to preserve when cropping rendered emoji.

Small margin prevents edge artifacts from cropping
too close to the rendered content.
"""

NOTO_COLOR_EMOJI_FONT_NAME = "NotoColorEmoji.ttf"
"""Filename of the NotoColorEmoji font.

This font should be placed in the 'fonts' subdirectory
of the export module.
"""


# =============================================================================
# Base Classes
# =============================================================================


class BaseEmojiSource(ABC):
    """Abstract base class for emoji image sources.

    Subclasses must implement get_emoji() to provide emoji images
    from their specific source (CDN, local font, etc.).
    """

    @abstractmethod
    def get_emoji(self, emoji: str) -> BytesIO | None:
        """Get emoji image as BytesIO stream.

        Args:
            emoji: The emoji character to fetch.

        Returns:
            BytesIO stream with image data, or None if not found.
        """
        raise NotImplementedError


class CDNEmojiSource(BaseEmojiSource):
    """Emoji source that fetches images from a CDN.

    Uses emojicdn.elk.sh as the default CDN which supports multiple
    emoji styles (Twitter, Apple, Google, Microsoft, OpenMoji).

    Subclasses should set the STYLE class attribute to specify which
    emoji style to use.
    """

    BASE_URL: str = ""
    STYLE: str = ""

    def __init__(self) -> None:
        """Initialize the CDN source with an empty cache."""
        self._cache: dict[str, BytesIO] = {}

    def _request(self, url: str) -> bytes | None:
        """Make HTTP request to fetch emoji image.

        Args:
            url: URL to fetch.

        Returns:
            Response bytes, or None on error.
        """
        try:
            req = Request(url, headers={"User-Agent": CDN_USER_AGENT})
            with urlopen(req, timeout=CDN_REQUEST_TIMEOUT_SECONDS) as response:
                return response.read()
        except (HTTPError, TimeoutError, OSError):
            return None

    def get_emoji(self, emoji: str) -> BytesIO | None:
        """Fetch emoji image from CDN.

        Results are cached to avoid repeated network requests.

        Args:
            emoji: The emoji character to fetch.

        Returns:
            BytesIO stream with PNG image data, or None if not found.
        """
        if emoji in self._cache:
            stream = self._cache[emoji]
            stream.seek(0)
            return stream

        url = self._build_url(emoji)
        data = self._request(url)

        if data:
            stream = BytesIO(data)
            self._cache[emoji] = stream
            stream.seek(0)
            return stream
        return None

    def _build_url(self, emoji: str) -> str:
        """Build URL for emoji image.

        Args:
            emoji: The emoji character.

        Returns:
            Full URL to fetch the emoji image.
        """
        return f"{CDN_BASE_URL}/{quote_plus(emoji)}?style={quote_plus(self.STYLE)}"


# =============================================================================
# CDN Source Implementations
# =============================================================================


class TwemojiSource(CDNEmojiSource):
    """Twitter/Twemoji style emojis.

    Twemoji is an open-source emoji set used by Twitter and Discord.
    Clean, flat design with good cross-platform consistency.
    """

    STYLE = "twitter"


class AppleEmojiSource(CDNEmojiSource):
    """Apple style emojis.

    The classic Apple emoji design, known for its detailed
    3D-style rendering and expressive faces.
    """

    STYLE = "apple"


class GoogleEmojiSource(CDNEmojiSource):
    """Google/Noto style emojis.

    Google's Noto Emoji design, featuring a blob-like style
    for older versions and more realistic for newer.
    """

    STYLE = "google"


class MicrosoftEmojiSource(CDNEmojiSource):
    """Microsoft/Fluent style emojis.

    Microsoft's Fluent emoji design with 3D-style rendering
    and vibrant colors.
    """

    STYLE = "microsoft"


class OpenmojiSource(CDNEmojiSource):
    """OpenMoji style emojis.

    OpenMoji is an open-source emoji project with a consistent,
    accessible design. Good choice for open-source projects.
    """

    STYLE = "openmoji"


# =============================================================================
# Local Font Source
# =============================================================================


class NotoColorEmojiSource(BaseEmojiSource):
    """Local Noto Color Emoji font source.

    Uses the bundled NotoColorEmoji.ttf font for high-quality,
    offline emoji rendering. This is faster than CDN sources
    and works without internet connection.

    The NotoColorEmoji font is from Google's Noto fonts project:
    https://github.com/googlefonts/noto-emoji

    License: SIL Open Font License 1.1

    Note:
        NotoColorEmoji is a bitmap font that only works correctly
        at the specific size defined in NOTO_COLOR_EMOJI_FONT_SIZE.
    """

    def __init__(self) -> None:
        """Initialize the local font source."""
        self._cache: dict[str, BytesIO] = {}
        self._font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
        self._font_loaded: bool = False

    def _load_font(self) -> bool:
        """Load the NotoColorEmoji font.

        Returns:
            True if font loaded successfully, False otherwise.
        """
        if self._font_loaded:
            return self._font is not None

        self._font_loaded = True
        try:
            from pathlib import Path

            from PIL import ImageFont

            font_path = Path(__file__).parent / "fonts" / NOTO_COLOR_EMOJI_FONT_NAME
            if font_path.exists():
                self._font = ImageFont.truetype(str(font_path), size=NOTO_COLOR_EMOJI_FONT_SIZE)
                return True
        except Exception:
            pass
        return False

    def get_emoji(self, emoji: str) -> BytesIO | None:
        """Render emoji from font and return as image stream.

        Args:
            emoji: The emoji character to render.

        Returns:
            BytesIO stream with PNG image data, or None on error.
        """
        if emoji in self._cache:
            stream = self._cache[emoji]
            stream.seek(0)
            return stream

        if not self._load_font():
            return None

        try:
            from PIL import Image, ImageDraw

            # Create transparent canvas with padding
            padding = NOTO_COLOR_EMOJI_PADDING
            img_size = NOTO_COLOR_EMOJI_FONT_SIZE + padding * 2
            img = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Render emoji with embedded color
            draw.text((padding, padding), emoji, font=self._font, embedded_color=True)

            # Crop to content with margin
            bbox = img.getbbox()
            if bbox:
                margin = NOTO_COLOR_EMOJI_CROP_MARGIN
                x1, y1, x2, y2 = bbox
                x1 = max(0, x1 - margin)
                y1 = max(0, y1 - margin)
                x2 = min(img_size, x2 + margin)
                y2 = min(img_size, y2 + margin)
                img = img.crop((x1, y1, x2, y2))

            # Save to BytesIO
            stream = BytesIO()
            img.save(stream, format="PNG")
            stream.seek(0)

            # Cache the result
            self._cache[emoji] = BytesIO(stream.read())
            stream.seek(0)
            return stream

        except Exception:
            return None
