"""Emoji rendering for image export.

This module provides the EmojiRenderer class that handles compositing
emoji images with regular text on PIL images.

The emoji parsing and source classes are in separate modules:
- emoji_parser: Text parsing to identify emoji characters
- emoji_sources: CDN and local font sources for emoji images
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

# Re-export commonly used classes for convenience
from .emoji_parser import EMOJI_REGEX, Node, NodeType, parse_text_with_emojis
from .emoji_sources import (
    AppleEmojiSource,
    BaseEmojiSource,
    GoogleEmojiSource,
    MicrosoftEmojiSource,
    NotoColorEmojiSource,
    OpenmojiSource,
    TwemojiSource,
)

if TYPE_CHECKING:
    from PIL import Image as PILImage
    from PIL import ImageFont as PILImageFont

    from .image_exporter import FontFamily, TextStyle

from .config import (
    EMOJI_LINE_HEIGHT_FACTOR,
    EMOJI_MIN_SIZE_PX,
    EMOJI_POSITION_OFFSET,
    EMOJI_SCALE_FACTOR,
)

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


@dataclass
class EmojiRenderer:
    """Renders text with emoji support onto PIL images.

    This class handles the complexity of rendering mixed text and emoji
    content by:
    1. Parsing text to identify emoji characters
    2. Fetching emoji images from a source (CDN or local font)
    3. Compositing emoji images with regular text

    Attributes:
        image: The PIL Image to draw on.
        source: Emoji image source (defaults to TwemojiSource).
        emoji_scale_factor: Scale factor for emoji size relative to font.
        emoji_position_offset: Pixel offset for emoji positioning.
        char_width: Fixed character width for monospace alignment.
        line_height: Line height for proper emoji vertical alignment.

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
    emoji_scale_factor: float = EMOJI_SCALE_FACTOR
    emoji_position_offset: tuple[int, int] = EMOJI_POSITION_OFFSET
    char_width: int | None = None
    line_height: int | None = None

    def __post_init__(self) -> None:
        """Initialize the renderer with ImageDraw and default source."""
        from PIL import ImageDraw

        self._draw = ImageDraw.Draw(self.image)
        if self.source is None:
            self.source = TwemojiSource()

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

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
            fill: Text color as hex string or RGB tuple.
            font: Font to use for text.
            spacing: Line spacing in pixels.
            fallback_font: Fallback font for special chars (e.g., Braille).
            is_braille_func: Function to check if a character is Braille.
            text_style: TextStyle with bold, italic, underline, etc.
            font_family: FontFamily for selecting styled font variants.
            **kwargs: Additional arguments passed to ImageDraw.text().
        """
        from PIL import ImageFont

        if font is None:
            font = ImageFont.load_default()

        x, y = xy
        original_x = x
        lines = parse_text_with_emojis(text)
        font_size = self._get_font_size(font)

        # Apply dim effect if needed
        # Apply dim effect if needed
        actual_fill = fill
        if text_style and text_style.dim:
            from styledconsole.utils.color import apply_dim

            actual_fill = apply_dim(fill)

        # Select font variant based on style
        base_font = self._select_styled_font(font, font_family, text_style)

        for line_nodes in lines:
            x = original_x
            for node in line_nodes:
                if node.type == NodeType.TEXT:
                    x = self._render_text_node(
                        x,
                        y,
                        node,
                        base_font,
                        actual_fill,
                        text_style,
                        fallback_font,
                        is_braille_func,
                        **kwargs,
                    )
                elif node.type == NodeType.EMOJI:
                    x = self._render_emoji_node(x, y, node, font_size, font, fill)
            y += int(font_size + spacing)

    def getwidth(
        self,
        text: str,
        font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None,
    ) -> int:
        """Calculate width needed to render a single line of text.

        Args:
            text: Text to measure (should be single line).
            font: Font to use for measurement.

        Returns:
            Width in pixels.
        """
        from PIL import ImageFont

        if font is None:
            font = ImageFont.load_default()

        font_size = self._get_font_size(font)
        nodes = self._parse_single_line(text)

        total_width = 0
        for node in nodes:
            if node.type == NodeType.TEXT:
                total_width += self._measure_text_width(node.content, font)
            else:
                total_width += self._measure_emoji_width(node.content, font_size)
        return total_width

    def getsize(
        self,
        text: str,
        font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None,
        spacing: int = 4,
    ) -> tuple[int, int]:
        """Calculate size needed to render multi-line text.

        Args:
            text: Text to measure (may contain newlines).
            font: Font to use for measurement.
            spacing: Line spacing in pixels.

        Returns:
            Tuple of (width, height) in pixels.
        """
        from PIL import ImageFont

        if font is None:
            font = ImageFont.load_default()

        font_size = self._get_font_size(font)
        lines = parse_text_with_emojis(text)

        max_width = 0
        total_height = 0

        for line_nodes in lines:
            line_width = 0
            for node in line_nodes:
                if node.type == NodeType.TEXT:
                    line_width += self._measure_text_width(node.content, font)
                else:
                    line_width += self._measure_emoji_width(node.content, font_size)
            max_width = max(max_width, line_width)
            total_height += font_size + spacing

        if total_height > 0:
            total_height -= spacing

        return max_width, total_height

    # -------------------------------------------------------------------------
    # Emoji sizing
    # -------------------------------------------------------------------------

    def _get_emoji_size(self, font_size: int) -> int:
        """Get emoji size (square) in pixels for rendering."""
        if self.line_height is not None:
            return max(int(self.line_height * EMOJI_LINE_HEIGHT_FACTOR), EMOJI_MIN_SIZE_PX)
        if self.char_width is not None:
            return 2 * self.char_width
        return int(font_size * self.emoji_scale_factor)

    def _get_emoji_width(self, font_size: int) -> int:
        """Get emoji width for x-position advancement."""
        if self.char_width is not None:
            return 2 * self.char_width
        return self._get_emoji_size(font_size)

    def _measure_emoji_width(self, emoji_text: str, font_size: int) -> int:
        """Measure emoji width in pixels.

        When char_width is provided we must match the layout engine's width
        calculations. Try to use Rich's cell_len first (respects patches),
        then fall back to visual_width for consistent export behavior.
        """
        if self.char_width is not None:
            # Try to use Rich's cell_len if available (respects patches for README generation)
            try:
                from rich import cells as rich_cells

                cell_width = rich_cells.cell_len(emoji_text)
                return cell_width * self.char_width
            except Exception:
                # Fallback to visual_width for consistent export behavior
                from styledconsole.utils.text import visual_width

                return visual_width(emoji_text) * self.char_width
        return int(self._get_emoji_width(font_size))

    # -------------------------------------------------------------------------
    # Font helpers
    # -------------------------------------------------------------------------

    def _get_font_size(self, font) -> int:
        """Extract font size from font object."""
        try:
            return int(getattr(font, "size", 14))
        except Exception:
            return 14

    def _select_styled_font(self, font, font_family, text_style):
        """Select font variant based on bold/italic style."""
        if font_family and text_style:
            styled = font_family.get_font(text_style.bold, text_style.italic)
            if styled is not None:
                return styled
        return font

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

    # -------------------------------------------------------------------------
    # Text rendering
    # -------------------------------------------------------------------------

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
        """Render a text node and return new x position."""
        if self.char_width is not None:
            return self._render_char_by_char(
                x,
                y,
                node.content,
                base_font,
                actual_fill,
                text_style,
                fallback_font,
                is_braille_func,
                **kwargs,
            )
        return self._render_text_chunk(
            x, y, node.content, base_font, actual_fill, text_style, **kwargs
        )

    def _render_char_by_char(
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
        """Draw text character by character at fixed positions.

        Uses Rich's cell_len for width calculation to ensure alignment
        with Rich's table/panel border positioning.
        """
        from rich.cells import cell_len

        from styledconsole.utils.text import split_graphemes

        assert self.char_width is not None  # Caller verifies this
        char_width = self.char_width

        for grapheme in split_graphemes(content):
            char_font = self._select_char_font(grapheme, base_font, fallback_font, is_braille_func)
            self._draw.text((x, y), grapheme, fill=actual_fill, font=char_font, **kwargs)
            # Use Rich's cell_len for width to match Rich's table/panel rendering
            # Rich uses cell_len to position borders, so we must use the same
            grapheme_width = cell_len(grapheme) * char_width
            if text_style:
                self._draw_decorations(x, y, grapheme_width, text_style, actual_fill)
            x += grapheme_width
        return x

    def _render_text_chunk(
        self, x: int, y: int, content: str, base_font, actual_fill, text_style, **kwargs
    ) -> int:
        """Draw text as a single chunk using font metrics."""
        self._draw.text((x, y), content, fill=actual_fill, font=base_font, **kwargs)
        text_width = self._measure_text_width(content, base_font)
        if text_style:
            self._draw_decorations(x, y, text_width, text_style, actual_fill)
        return x + text_width

    # -------------------------------------------------------------------------
    # Emoji rendering
    # -------------------------------------------------------------------------

    def _render_emoji_node(self, x: int, y: int, node, font_size: int, font, fill) -> int:
        """Render an emoji node and return new x position."""
        emoji_stream = self.source.get_emoji(node.content) if self.source else None
        emoji_width = int(self._measure_emoji_width(node.content, font_size))
        emoji_size = int(self._get_emoji_size(font_size))
        if emoji_size > emoji_width:
            emoji_size = emoji_width

        if emoji_stream:
            try:
                return self._paste_emoji(x, y, emoji_stream, emoji_size, emoji_width, font)
            except Exception:
                pass

        # Fallback: draw placeholder
        self._draw.text((x, y), "□", fill=fill, font=font)
        return x + emoji_width

    def _paste_emoji(
        self, x: int, y: int, emoji_stream, emoji_size: int, emoji_width: int, font
    ) -> int:
        """Paste emoji image at position and return new x position."""
        from PIL import Image

        with Image.open(emoji_stream) as emoji_img:
            emoji_img = emoji_img.convert("RGBA")  # type: ignore[assignment]
            emoji_img = emoji_img.resize((emoji_size, emoji_size), Image.Resampling.LANCZOS)  # type: ignore[assignment]

            ox = (emoji_width - emoji_size) // 2
            oy = self._calculate_emoji_y_offset(emoji_size, font)

            self.image.paste(emoji_img, (int(x + ox), int(y + oy)), emoji_img)
            return x + emoji_width

    def _calculate_emoji_y_offset(self, emoji_size: int, font) -> int:
        """Calculate vertical offset for emoji alignment."""
        if self.line_height is not None:
            try:
                text_bbox = getattr(font, "getbbox", lambda s: None)("M")
                if text_bbox:
                    return int(text_bbox[3]) - emoji_size
                return int((self.line_height - emoji_size) // 2)
            except Exception:
                return int((self.line_height - emoji_size) // 2)
        return int(self.emoji_position_offset[1])

    # -------------------------------------------------------------------------
    # Text styling
    # -------------------------------------------------------------------------

    def _draw_decorations(self, x: int, y: int, width: int, text_style: TextStyle, color) -> None:
        """Draw text decorations (underline, strikethrough, overline)."""
        if not self.line_height or color is None:
            return

        line_thickness = max(1, self.line_height // 12)

        if text_style.underline:
            uy = y + self.line_height - 3
            self._draw.line([(x, uy), (x + width, uy)], fill=color, width=line_thickness)

        if text_style.strike:
            sy = y + self.line_height // 2
            self._draw.line([(x, sy), (x + width, sy)], fill=color, width=line_thickness)

        if text_style.overline:
            oy = y + 2
            self._draw.line([(x, oy), (x + width, oy)], fill=color, width=line_thickness)

    # -------------------------------------------------------------------------
    # Measurement helpers
    # -------------------------------------------------------------------------

    def _parse_single_line(self, text: str) -> list[Node]:
        """Parse a single line of text into nodes."""
        nodes = []
        for i, chunk in enumerate(EMOJI_REGEX.split(text)):
            if not chunk:
                continue
            if i % 2 == 0:
                nodes.append(Node(NodeType.TEXT, chunk))
            else:
                nodes.append(Node(NodeType.EMOJI, chunk))
        return nodes

    def _measure_text_width(self, content: str, font) -> int:
        """Measure width of text content.

        Uses visual_width which respects render target context for consistent
        emoji width calculations in both layout and rendering.
        """
        if self.char_width is not None:
            from styledconsole.utils.text import visual_width

            return visual_width(content) * self.char_width

        # Fallback to font metrics
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
