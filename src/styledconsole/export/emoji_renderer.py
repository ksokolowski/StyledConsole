"""Emoji rendering support for image export.

This module provides emoji rendering capabilities for Pillow images,
fetching emoji images from CDN sources and compositing them with text.

Inspired by the pilmoji project (https://github.com/jay3332/pilmoji),
but rewritten from scratch to support emoji v2.x library.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING, NamedTuple
from urllib.error import HTTPError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

if TYPE_CHECKING:
    from PIL import Image as PILImage
    from PIL import ImageFont as PILImageFont

    from .image_exporter import FontFamily, TextStyle

__all__ = [
    "AppleEmojiSource",
    "BaseEmojiSource",
    "EmojiRenderer",
    "GoogleEmojiSource",
    "MicrosoftEmojiSource",
    "NotoColorEmojiSource",
    "OpenmojiSource",
    "TwemojiSource",
]


# Build emoji regex from emoji library (v2.x compatible)
def _build_emoji_regex() -> re.Pattern[str]:
    """Build regex pattern to match emoji characters.

    Uses emoji.EMOJI_DATA which is available in emoji v2.x.
    """
    try:
        from emoji import EMOJI_DATA

        # Get all emoji characters, sorted by length (longest first for proper matching)
        emoji_chars = sorted(EMOJI_DATA.keys(), key=len, reverse=True)
        pattern = "|".join(map(re.escape, emoji_chars))
        return re.compile(f"({pattern})")
    except ImportError:
        # Fallback: empty pattern if emoji not available
        return re.compile(r"(\x00)")  # Won't match anything useful


EMOJI_REGEX = _build_emoji_regex()


class NodeType(Enum):
    """Type of parsed text node."""

    TEXT = 0
    EMOJI = 1


class Node(NamedTuple):
    """A parsed text node."""

    type: NodeType
    content: str


def parse_text_with_emojis(text: str) -> list[list[Node]]:
    """Parse text into nodes, separating emojis from regular text.

    Args:
        text: Text to parse.

    Returns:
        List of lines, each containing a list of Node objects.
    """
    result = []
    for line in text.splitlines():
        nodes = []
        for i, chunk in enumerate(EMOJI_REGEX.split(line)):
            if not chunk:
                continue
            if i % 2 == 0:
                # Regular text
                nodes.append(Node(NodeType.TEXT, chunk))
            else:
                # Emoji
                nodes.append(Node(NodeType.EMOJI, chunk))
        result.append(nodes)
    return result


class BaseEmojiSource(ABC):
    """Base class for emoji image sources."""

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
    """Emoji source that fetches from a CDN."""

    BASE_URL: str = ""
    STYLE: str = ""

    def __init__(self) -> None:
        self._cache: dict[str, BytesIO] = {}

    def _request(self, url: str) -> bytes | None:
        """Make HTTP request to fetch emoji image."""
        try:
            req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urlopen(req, timeout=10) as response:
                return response.read()
        except (HTTPError, TimeoutError, OSError):
            return None

    def get_emoji(self, emoji: str) -> BytesIO | None:
        """Fetch emoji image from CDN."""
        # Check cache first
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
        """Build URL for emoji image."""
        # Default: use emojicdn.elk.sh
        return f"https://emojicdn.elk.sh/{quote_plus(emoji)}?style={quote_plus(self.STYLE)}"


class TwemojiSource(CDNEmojiSource):
    """Twitter/Twemoji style emojis (used by Discord)."""

    STYLE = "twitter"


class AppleEmojiSource(CDNEmojiSource):
    """Apple style emojis."""

    STYLE = "apple"


class GoogleEmojiSource(CDNEmojiSource):
    """Google/Noto style emojis."""

    STYLE = "google"


class MicrosoftEmojiSource(CDNEmojiSource):
    """Microsoft/Fluent style emojis."""

    STYLE = "microsoft"


class OpenmojiSource(CDNEmojiSource):
    """OpenMoji style emojis (open source)."""

    STYLE = "openmoji"


class NotoColorEmojiSource(BaseEmojiSource):
    """Local Noto Color Emoji font source.

    Uses the bundled NotoColorEmoji.ttf font for high-quality, offline emoji rendering.
    This is faster than CDN sources and works without internet connection.

    The NotoColorEmoji font is from Google's Noto fonts project:
    https://github.com/googlefonts/noto-emoji

    License: SIL Open Font License 1.1
    """

    # NotoColorEmoji only works at this specific size (bitmap font)
    FONT_SIZE = 109

    def __init__(self) -> None:
        self._cache: dict[str, BytesIO] = {}
        # Typed as Optional FreeTypeFont or ImageFont (annotation evaluated later)
        self._font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
        self._font_loaded: bool = False

    def _load_font(self) -> bool:
        """Load the NotoColorEmoji font."""
        if self._font_loaded:
            return self._font is not None

        self._font_loaded = True
        try:
            from pathlib import Path

            from PIL import ImageFont

            # Try to find the bundled font
            font_path = Path(__file__).parent / "fonts" / "NotoColorEmoji.ttf"
            if font_path.exists():
                self._font = ImageFont.truetype(str(font_path), size=self.FONT_SIZE)
                return True
        except Exception:
            pass
        return False

    def get_emoji(self, emoji: str) -> BytesIO | None:
        """Render emoji from font and return as image stream."""
        # Check cache first
        if emoji in self._cache:
            stream = self._cache[emoji]
            stream.seek(0)
            return stream

        if not self._load_font():
            return None

        try:
            from PIL import Image, ImageDraw

            # Create transparent image for rendering
            # Use generous padding to ensure emoji is not clipped
            padding = 40
            img_size = self.FONT_SIZE + padding * 2
            img = Image.new("RGBA", (img_size, img_size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # Render emoji centered in canvas with color
            draw.text((padding, padding), emoji, font=self._font, embedded_color=True)

            # Crop to content with small margin to avoid clipping
            bbox = img.getbbox()
            if bbox:
                # Add 2px margin around the bbox to prevent edge clipping
                x1, y1, x2, y2 = bbox
                x1 = max(0, x1 - 2)
                y1 = max(0, y1 - 2)
                x2 = min(img_size, x2 + 2)
                y2 = min(img_size, y2 + 2)
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


@dataclass
class EmojiRenderer:
    """Renders text with emoji support onto PIL images.

    This class handles the complexity of rendering mixed text and emoji
    content by:
    1. Parsing text to identify emoji characters
    2. Fetching emoji images from a CDN source
    3. Compositing emoji images with regular text

    Example:
        >>> from PIL import Image, ImageFont
        >>> from styledconsole.export.emoji_renderer import EmojiRenderer, TwemojiSource
        >>>
        >>> image = Image.new('RGB', (400, 100), '#1e1e2e')
        >>> renderer = EmojiRenderer(image, source=TwemojiSource())
        >>> font = ImageFont.truetype('DejaVuSansMono.ttf', 16)
        >>> renderer.text((10, 10), '✅ Success!', fill='#00ff00', font=font)
        >>> image.save('output.png')
    """

    image: PILImage.Image
    source: BaseEmojiSource | None = None
    emoji_scale_factor: float = 1.0
    emoji_position_offset: tuple[int, int] = (0, -2)
    # Width of one character in pixels (for calculating emoji width as 2 chars)
    char_width: int | None = None
    # Line height in pixels - emojis are scaled to fit within this height
    line_height: int | None = None

    def __post_init__(self) -> None:
        """Initialize the renderer."""
        from PIL import ImageDraw

        self._draw = ImageDraw.Draw(self.image)
        if self.source is None:
            self.source = TwemojiSource()

    def _get_emoji_size(self, font_size: int) -> int:
        """Get the size (width and height) of an emoji in pixels.

        Emoji size is scaled to be slightly larger than text height for visual
        prominence while still fitting within line_height boundaries.

        Args:
            font_size: The font size in pixels.

        Returns:
            Size in pixels for rendering emoji (square).
        """
        if self.line_height is not None:
            # Use 75% of line_height for slightly larger emojis
            # With line_height=24, this gives 18px emoji (larger than 16px text)
            return max(int(self.line_height * 0.75), 12)
        if self.char_width is not None:
            # Fallback: Terminal emojis are 2 columns wide and square
            return 2 * self.char_width
        return int(font_size * self.emoji_scale_factor)

    def _get_emoji_width(self, font_size: int) -> int:
        """Get the width of an emoji in pixels for positioning.

        This is used for advancing the x position after drawing an emoji.
        Always returns 2 * char_width for proper text alignment.
        """
        if self.char_width is not None:
            return 2 * self.char_width
        return self._get_emoji_size(font_size)

    def text(
        self,
        xy: tuple[int, int],
        text: str,
        fill: str | tuple[int, int, int] | None = None,
        font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None,
        spacing: int = 4,
        fallback_font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None,
        is_braille_func: Callable[[str], bool] | None = None,
        text_style: TextStyle | None = None,
        font_family: FontFamily | None = None,
        **kwargs,
    ) -> None:
        """Draw text with emoji support.

        Args:
            xy: Position (x, y) to start drawing.
            text: Text to render (may contain emojis).
            fill: Text color.
            font: Font to use for text.
            spacing: Line spacing in pixels.
            fallback_font: Fallback font for characters not in primary font (e.g., Braille).
            is_braille_func: Function to check if a character is Braille.
            text_style: TextStyle object with bold, italic, underline, etc. properties.
            font_family: FontFamily object for selecting styled font variants.
            **kwargs: Additional arguments passed to ImageDraw.text().
        """
        from PIL import ImageFont

        if font is None:
            font = ImageFont.load_default()

        x, y = xy
        original_x = x
        lines = parse_text_with_emojis(text)

        # Get font size for emoji scaling
        font_size = self._get_font_size(font)

        # Apply dim effect to fill color if needed
        actual_fill = self._apply_dim(fill) if text_style and text_style.dim else fill

        # Select base font based on style (bold/italic)
        base_font = self._select_styled_font(font, font_family, text_style)

        for line_nodes in lines:
            x = original_x
            for node in line_nodes:
                if node.type == NodeType.TEXT:
                    x = self._render_text_node(
                        x, y, node, base_font, actual_fill, text_style,
                        fallback_font, is_braille_func, **kwargs
                    )
                elif node.type == NodeType.EMOJI:
                    x = self._render_emoji_node(x, y, node, font_size, font, fill)

            # Move to next line
            y += int(font_size + spacing)

    def _get_font_size(self, font) -> int:
        """Extract font size from font object."""
        try:
            return int(getattr(font, "size", 14))
        except Exception:
            return 14

    def _select_styled_font(self, font, font_family, text_style):
        """Select appropriate font based on style (bold/italic)."""
        if font_family and text_style:
            styled = font_family.get_font(text_style.bold, text_style.italic)
            if styled is not None:
                return styled
        return font

    def _render_text_node(
        self,
        x: int,
        y: int,
        node,
        base_font,
        actual_fill,
        text_style,
        fallback_font,
        is_braille_func,
        **kwargs,
    ) -> int:
        """Render a text node and return the new x position."""
        if self.char_width is not None:
            return self._render_text_char_by_char(
                x, y, node.content, base_font, actual_fill, text_style,
                fallback_font, is_braille_func, **kwargs
            )
        return self._render_text_chunk(
            x, y, node.content, base_font, actual_fill, text_style, **kwargs
        )

    def _render_text_char_by_char(
        self,
        x: int,
        y: int,
        content: str,
        base_font,
        actual_fill,
        text_style,
        fallback_font,
        is_braille_func,
        **kwargs,
    ) -> int:
        """Draw text character by character at fixed positions."""
        from styledconsole.utils.text import _grapheme_width_export, split_graphemes

        for grapheme in split_graphemes(content):
            char_font = self._select_char_font(
                grapheme, base_font, fallback_font, is_braille_func
            )
            self._draw.text((x, y), grapheme, fill=actual_fill, font=char_font, **kwargs)

            grapheme_width = int(_grapheme_width_export(grapheme) * self.char_width)
            if text_style:
                self._draw_decorations(x, y, grapheme_width, text_style, actual_fill)
            x += grapheme_width
        return x

    def _select_char_font(self, grapheme, base_font, fallback_font, is_braille_func):
        """Select font for a character, using fallback for Braille."""
        if (
            fallback_font is not None
            and is_braille_func is not None
            and len(grapheme) == 1
            and is_braille_func(grapheme)
        ):
            return fallback_font
        return base_font

    def _render_text_chunk(
        self, x: int, y: int, content: str, base_font, actual_fill, text_style, **kwargs
    ) -> int:
        """Draw text as a single chunk using font metrics."""
        self._draw.text((x, y), content, fill=actual_fill, font=base_font, **kwargs)
        text_width = self._get_text_width(content, base_font)
        if text_style:
            self._draw_decorations(x, y, text_width, text_style, actual_fill)
        return x + text_width

    def _get_text_width(self, content: str, font) -> int:
        """Get width of text using font metrics."""
        try:
            _getlen = getattr(font, "getlength", None)
            if callable(_getlen):
                return int(_getlen(content) or 0)
        except Exception:
            pass
        try:
            bbox = font.getbbox(content)
            if bbox:
                return int(bbox[2] - bbox[0])
        except Exception:
            pass
        return len(content) * 8

    def _render_emoji_node(
        self, x: int, y: int, node, font_size: int, font, fill
    ) -> int:
        """Render an emoji node and return the new x position."""
        from PIL import Image

        emoji_stream = self.source.get_emoji(node.content) if self.source else None
        emoji_size = int(self._get_emoji_size(font_size))
        emoji_width = int(self._get_emoji_width(font_size))

        if emoji_stream:
            try:
                x = self._paste_emoji_image(
                    x, y, emoji_stream, emoji_size, emoji_width, font
                )
                return x
            except Exception:
                pass

        # Fallback: draw placeholder
        self._draw.text((x, y), "□", fill=fill, font=font)
        return x + emoji_width

    def _paste_emoji_image(
        self, x: int, y: int, emoji_stream, emoji_size: int, emoji_width: int, font
    ) -> int:
        """Paste emoji image at position and return new x position."""
        from PIL import Image

        with Image.open(emoji_stream) as emoji_img:
            emoji_img = emoji_img.convert("RGBA")
            emoji_img = emoji_img.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)

            # Center emoji horizontally within its 2-char width
            ox = (emoji_width - emoji_size) // 2
            oy = self._calculate_emoji_y_offset(emoji_size, font)

            self.image.paste(emoji_img, (int(x + ox), int(y + oy)), emoji_img)
            return x + emoji_width

    def _calculate_emoji_y_offset(self, emoji_size: int, font) -> int:
        """Calculate vertical offset for emoji alignment with text."""
        if self.line_height is not None:
            try:
                text_bbox = getattr(font, "getbbox", lambda s: None)("M")
                if text_bbox:
                    return int(text_bbox[3]) - emoji_size
                return int((self.line_height - emoji_size) // 2)
            except Exception:
                return int((self.line_height - emoji_size) // 2)
        return int(self.emoji_position_offset[1])

    def _apply_dim(
        self, color: str | tuple[int, int, int] | None
    ) -> str | tuple[int, int, int] | None:
        """Apply dim effect by reducing color brightness to 50%.

        Args:
            color: Color as hex string or RGB tuple.

        Returns:
            Dimmed color (darkened by 50%).
        """
        if color is None:
            return None

        if isinstance(color, str):
            # Handle hex color string
            if not color.startswith("#") or len(color) != 7:
                return color
            try:
                r = int(color[1:3], 16) // 2
                g = int(color[3:5], 16) // 2
                b = int(color[5:7], 16) // 2
                return f"#{r:02x}{g:02x}{b:02x}"
            except ValueError:
                return color
        elif isinstance(color, tuple) and len(color) >= 3:
            # Handle RGB tuple - return same type
            return (color[0] // 2, color[1] // 2, color[2] // 2)
        return color

    def _draw_decorations(
        self,
        x: int,
        y: int,
        width: int,
        text_style: TextStyle,
        color: str | tuple | None,
    ) -> None:
        """Draw text decorations (underline, strikethrough, overline).

        Args:
            x: Starting x position.
            y: Starting y position.
            width: Width of the text/character to decorate.
            text_style: TextStyle object with decoration flags.
            color: Color for the decoration lines.
        """
        if not self.line_height or color is None:
            return

        line_thickness = max(1, self.line_height // 12)

        if text_style.underline:
            underline_y = y + self.line_height - 3
            self._draw.line(
                [(x, underline_y), (x + width, underline_y)],
                fill=color,
                width=line_thickness,
            )

        if text_style.strike:
            strike_y = y + self.line_height // 2
            self._draw.line(
                [(x, strike_y), (x + width, strike_y)],
                fill=color,
                width=line_thickness,
            )

        if text_style.overline:
            overline_y = y + 2
            self._draw.line(
                [(x, overline_y), (x + width, overline_y)],
                fill=color,
                width=line_thickness,
            )

    def getwidth(
        self,
        text: str,
        font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None,
    ) -> int:
        """Calculate the width needed to render a single line of text with emojis.

        Args:
            text: Text to measure (should be single line, no newlines).
            font: Font to use.

        Returns:
            Width in pixels.
        """
        from PIL import ImageFont

        if font is None:
            font = ImageFont.load_default()

        try:
            font_size = int(getattr(font, "size", 14))
        except Exception:
            font_size = 14

        # Parse text into nodes
        nodes = []
        for i, chunk in enumerate(EMOJI_REGEX.split(text)):
            if not chunk:
                continue
            if i % 2 == 0:
                nodes.append(Node(NodeType.TEXT, chunk))
            else:
                nodes.append(Node(NodeType.EMOJI, chunk))

        # Calculate total width
        # When char_width is set, use visual_width for consistency
        # with frame layout calculations
        total_width = 0
        for node in nodes:
            if node.type == NodeType.TEXT:
                if self.char_width is not None:
                    # Use visual_width for proper grapheme handling
                    from styledconsole.utils.text import _grapheme_width_export, split_graphemes

                    graphemes = split_graphemes(node.content)
                    for grapheme in graphemes:
                        total_width += int(_grapheme_width_export(grapheme) * self.char_width)
                else:
                    # Fallback to font metrics
                    try:
                        _getlen = getattr(font, "getlength", None)
                        if callable(_getlen):
                            total_width += int(_getlen(node.content) or 0)
                        else:
                            raise AttributeError
                    except Exception:
                        try:
                            bbox = font.getbbox(node.content)
                            total_width += int(bbox[2] - bbox[0]) if bbox else len(node.content) * 8
                        except Exception:
                            total_width += len(node.content) * 8
            else:
                # Emoji width - use 2 char widths if set, otherwise font_size * scale
                total_width += int(self._get_emoji_width(font_size))

        return total_width

    def getsize(
        self,
        text: str,
        font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None,
        spacing: int = 4,
    ) -> tuple[int, int]:
        """Calculate the size needed to render text with emojis.

        Args:
            text: Text to measure.
            font: Font to use.
            spacing: Line spacing.

        Returns:
            Tuple of (width, height).
        """
        from PIL import ImageFont

        if font is None:
            font = ImageFont.load_default()

        try:
            font_size = int(getattr(font, "size", 14))
        except Exception:
            font_size = 14

        lines = parse_text_with_emojis(text)
        max_width = 0
        total_height = 0

        for line_nodes in lines:
            line_width = 0
            for node in line_nodes:
                if node.type == NodeType.TEXT:
                    if self.char_width is not None:
                        # Use visual_width for proper grapheme handling
                        from styledconsole.utils.text import _grapheme_width_export, split_graphemes

                        graphemes = split_graphemes(node.content)
                        for grapheme in graphemes:
                            line_width += int(_grapheme_width_export(grapheme) * self.char_width)
                    else:
                        # Fallback to font metrics
                        try:
                            _getlen = getattr(font, "getlength", None)
                            if callable(_getlen):
                                line_width += int(_getlen(node.content) or 0)
                            else:
                                raise AttributeError
                        except Exception:
                            try:
                                bbox = font.getbbox(node.content)
                                if bbox:
                                    line_width += int(bbox[2] - bbox[0])
                                else:
                                    line_width += len(node.content) * 8
                            except Exception:
                                line_width += len(node.content) * 8
                else:
                    # Emoji width - use 2 char widths if set, otherwise font_size * scale
                    line_width += int(self._get_emoji_width(font_size))

            max_width = max(max_width, line_width)
            total_height += font_size + spacing

        # Remove last spacing
        if total_height > 0:
            total_height -= spacing

        return max_width, total_height
