"""Image export functionality for Console output.

This module provides the ImageExporter class for exporting terminal output
to image formats (PNG, WebP, GIF, AVIF).

Related modules:
- image_theme: Theme and style dataclasses
- font_loader: Font loading utilities
- image_cropper: Cropping utilities
- emoji_renderer: Emoji rendering support

Requires: pip install styledconsole[image] (or Pillow>=10.0.0)
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

# Re-export theme classes for convenience
from .config import (
    TEXT_DECORATION_OVERLINE_OFFSET,
    TEXT_DECORATION_THICKNESS_DIVISOR,
    TEXT_DECORATION_UNDERLINE_OFFSET,
)
from .font_loader import FontLoader
from .image_cropper import auto_crop, auto_crop_frames
from .image_theme import (
    DEFAULT_THEME,
    FontFamily,
    ImageTheme,
    TextStyle,
)

if TYPE_CHECKING:
    from PIL import Image as PILImage
    from PIL import ImageFont as PILImageFont
    from rich.console import Console as RichConsole
    from rich.segment import Segment

    from .emoji_renderer import BaseEmojiSource


class ImageExporter:
    """Export console output to image formats using Pillow.

    This class converts Rich console recorded output to raster images,
    preserving colors, styles, and formatting.

    Example:
        >>> from rich.console import Console
        >>> console = Console(record=True)
        >>> console.print("[bold red]Hello[/bold red] World")
        >>> exporter = ImageExporter(console)
        >>> exporter.save_png("output.png")
    """

    def __init__(
        self,
        rich_console: RichConsole,
        theme: ImageTheme | None = None,
        font_path: str | None = None,
        emoji_source: BaseEmojiSource | None = None,
        render_emojis: bool = True,
    ) -> None:
        """Initialize image exporter.

        Args:
            rich_console: Rich Console instance with recording enabled.
            theme: Color theme for the image. Defaults to dark theme.
            font_path: Path to a TrueType font file. If None, uses system fonts.
            emoji_source: Emoji image source. If None, uses NotoColorEmojiSource.
            render_emojis: Whether to render emojis as images. Defaults to True.
        """
        self._console = rich_console
        self._theme = theme or DEFAULT_THEME
        self._emoji_source = emoji_source
        self._render_emojis = render_emojis
        self._font_loader = FontLoader(self._theme, font_path)
        self._frames: list[PILImage.Image] = []

    # -------------------------------------------------------------------------
    # Pillow imports
    # -------------------------------------------------------------------------

    def _lazy_import_pillow(self) -> tuple:
        """Lazy import Pillow modules.

        Returns:
            Tuple of (Image, ImageDraw, ImageFont) modules.

        Raises:
            ImportError: If Pillow is not installed.
        """
        try:
            from PIL import Image, ImageDraw, ImageFont

            return Image, ImageDraw, ImageFont
        except ImportError as e:
            raise ImportError(
                "Image export requires Pillow. Install with: pip install styledconsole[image]"
            ) from e

    # -------------------------------------------------------------------------
    # Character utilities
    # -------------------------------------------------------------------------

    def _is_braille(self, char: str) -> bool:
        """Check if a character is a Braille pattern.

        Braille patterns are in Unicode block U+2800 to U+28FF.

        Args:
            char: Single character to check.

        Returns:
            True if character is a Braille pattern.
        """
        if len(char) != 1:
            return False
        code = ord(char)
        return 0x2800 <= code <= 0x28FF

    def _get_font_for_char(
        self, char: str, text_style: TextStyle | None = None
    ) -> PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None:
        """Get the appropriate font for a character.

        Uses fallback font for Braille characters if available.
        Uses styled font variant if text_style specifies bold/italic.

        Args:
            char: Single character.
            text_style: Text style properties.

        Returns:
            Font to use for rendering the character.
        """
        # Braille characters always use fallback font
        if self._is_braille(char) and self._font_loader.fallback_font is not None:
            return self._font_loader.fallback_font

        # Select font variant based on style
        if self._font_loader.font_family and text_style:
            return self._font_loader.font_family.get_font(text_style.bold, text_style.italic)

        return self._font_loader.font

    # -------------------------------------------------------------------------
    # Color utilities
    # -------------------------------------------------------------------------

    def _get_color_hex(self, color: Any) -> str | None:
        """Convert Rich color to hex string.

        Args:
            color: Rich Color object or None.

        Returns:
            Hex color string like "#RRGGBB" or None.
        """
        if color is None:
            return None

        triplet = color.get_truecolor()
        return f"#{triplet.red:02x}{triplet.green:02x}{triplet.blue:02x}"

    # -------------------------------------------------------------------------
    # Text rendering
    # -------------------------------------------------------------------------

    def _render_text_with_fallback(
        self,
        draw: Any,
        x: int,
        y: int,
        text: str,
        color: str,
        text_style: TextStyle | None = None,
    ) -> None:
        """Render text character by character, using fallback font for Braille.

        Args:
            draw: PIL ImageDraw instance.
            x: Starting x position.
            y: Starting y position.
            text: Text to render.
            color: Text color (hex string).
            text_style: Text style properties (bold, italic, underline, etc.).
        """
        current_x = x
        actual_color = color
        if text_style and text_style.dim:
            from styledconsole.utils.color import apply_dim

            # apply_dim returns None only if input is None, but here color is guaranteed str
            dimmed = apply_dim(color)
            if dimmed:
                actual_color = str(dimmed)

        from styledconsole.utils.text import split_graphemes, visual_width

        char_width = self._font_loader.char_width
        char_height = self._font_loader.char_height

        # Render by grapheme clusters using visual_width which respects the
        # render target context ("image" mode = consistent emoji widths).
        for grapheme in split_graphemes(text):
            font = self._get_font_for_char(grapheme, text_style)
            draw.text((current_x, y), grapheme, font=font, fill=actual_color)

            grapheme_pixel_width = visual_width(grapheme) * char_width

            if text_style:
                self._draw_char_decorations(
                    draw,
                    current_x,
                    y,
                    grapheme_pixel_width,
                    char_height,
                    text_style,
                    actual_color,
                )

            current_x += grapheme_pixel_width

    def _draw_char_decorations(
        self,
        draw: Any,
        x: int,
        y: int,
        width: int,
        height: float,
        text_style: TextStyle,
        color: str,
    ) -> None:
        """Draw text decorations (underline, strikethrough, overline).

        Args:
            draw: PIL ImageDraw instance.
            x: Character x position.
            y: Character y position.
            width: Character width.
            height: Character height.
            text_style: Text style properties.
            color: Decoration color.
        """
        line_thickness = max(1, int(height) // TEXT_DECORATION_THICKNESS_DIVISOR)

        if text_style.underline:
            underline_y = y + int(height) - TEXT_DECORATION_UNDERLINE_OFFSET
            draw.line(
                [(x, underline_y), (x + width, underline_y)],
                fill=color,
                width=line_thickness,
            )

        if text_style.strike:
            strike_y = y + int(height) // 2
            draw.line(
                [(x, strike_y), (x + width, strike_y)],
                fill=color,
                width=line_thickness,
            )

        if text_style.overline:
            overline_y = y + TEXT_DECORATION_OVERLINE_OFFSET
            draw.line(
                [(x, overline_y), (x + width, overline_y)],
                fill=color,
                width=line_thickness,
            )

    # -------------------------------------------------------------------------
    # Segment processing
    # -------------------------------------------------------------------------

    def _get_segments_by_line(self) -> list[list[Segment]]:
        """Get recorded segments organized by line.

        Returns:
            List of lines, where each line is a list of Segments.
        """
        lines: list[list[Segment]] = [[]]

        for segment in self._console._record_buffer:
            if segment.text == "\n":
                lines.append([])
            elif segment.text:
                self._split_segment_by_newlines(segment, lines)

        # Remove trailing empty line if present
        if lines and not lines[-1]:
            lines.pop()

        return lines

    def _split_segment_by_newlines(self, segment: Segment, lines: list[list[Segment]]) -> None:
        """Split a segment containing embedded newlines across lines.

        Args:
            segment: Rich Segment to split.
            lines: List of lines to append to.
        """
        from rich.segment import Segment as RichSegment

        parts = segment.text.split("\n")
        for i, part in enumerate(parts):
            if part:
                lines[-1].append(RichSegment(part, segment.style, segment.control))
            if i < len(parts) - 1:
                lines.append([])

    # -------------------------------------------------------------------------
    # Dimension calculation
    # -------------------------------------------------------------------------

    def _calculate_dimensions(self) -> tuple[int, int]:
        """Calculate image dimensions based on recorded content or fixed size.

        Returns:
            Tuple of (width, height) in pixels.
        """
        char_width = self._font_loader.char_width
        char_height = self._font_loader.char_height

        # If fixed terminal size is set, use it
        if self._theme.terminal_size is not None:
            cols, rows = self._theme.terminal_size
            width = int(self._theme.padding * 2 + cols * char_width)
            height = int(self._theme.padding * 2 + rows * char_height)
            return width, height

        lines = self._get_segments_by_line()

        if not lines:
            return self._get_minimum_dimensions()

        width_calculator = self._create_width_calculator()
        max_width = self._calculate_max_line_width(lines, width_calculator)

        width = int(self._theme.padding * 2 + max_width)
        height = int(self._theme.padding * 2 + len(lines) * char_height)

        return width, height

    def _get_minimum_dimensions(self) -> tuple[int, int]:
        """Get minimum dimensions for empty content.

        Returns:
            Tuple of (width, height) in pixels.
        """
        char_width = self._font_loader.char_width
        char_height = self._font_loader.char_height
        return (
            int(self._theme.padding * 2 + char_width * 10),
            int(self._theme.padding * 2 + char_height),
        )

    def _create_width_calculator(self) -> Any:
        """Create emoji renderer for width calculation if enabled.

        Returns:
            EmojiRenderer instance or None.
        """
        if not self._render_emojis:
            return None

        try:
            from PIL import Image as PILImage

            from .emoji_renderer import EmojiRenderer, NotoColorEmojiSource

            temp_img = PILImage.new("RGB", (1, 1))
            source = self._emoji_source or NotoColorEmojiSource()
            return EmojiRenderer(
                image=temp_img,
                source=source,
                emoji_scale_factor=1.0,
                char_width=self._font_loader.char_width,
            )
        except ImportError:
            return None

    def _calculate_max_line_width(self, lines: list[list[Segment]], width_calculator: Any) -> int:
        """Calculate maximum line width across all lines.

        Args:
            lines: List of lines with segments.
            width_calculator: EmojiRenderer for width calculation or None.

        Returns:
            Maximum width in pixels.
        """
        font = self._font_loader.font
        max_width = 0

        for line in lines:
            line_width = 0
            for seg in line:
                if width_calculator:
                    line_width += width_calculator.getwidth(seg.text, font=font)
                else:
                    line_width += self._measure_text_width_cells(seg.text)
            max_width = max(max_width, line_width)

        return max_width

    # -------------------------------------------------------------------------
    # Frame rendering
    # -------------------------------------------------------------------------

    def _render_frame(self) -> PILImage.Image:
        """Render current console output to PIL Image.

        Returns:
            PIL Image with rendered console output.
        """
        pil_image, pil_draw, pil_font = self._lazy_import_pillow()

        # Load font if not already loaded
        if self._font_loader.font is None:
            self._font_loader.load(pil_font)

        # Calculate dimensions
        width, height = self._calculate_dimensions()

        # Create image with background color
        img = pil_image.new("RGB", (width, height), self._theme.background)
        draw = pil_draw.Draw(img)

        # Set up emoji renderer if enabled
        emoji_renderer = self._create_emoji_renderer(img)

        # Get segments organized by line and render
        lines = self._get_segments_by_line()
        self._render_lines(draw, lines, emoji_renderer)

        # Optional: overlay debug grid showing terminal cell boundaries
        if getattr(self._theme, "debug_grid", False):
            self._draw_debug_grid(draw, width, height)

        return img

    def _draw_debug_grid(self, draw: Any, width: int, height: int) -> None:
        """Overlay a terminal cell grid for debugging alignment issues."""
        char_width = self._font_loader.char_width
        char_height = int(self._font_loader.char_height)
        padding = int(self._theme.padding)

        if char_width <= 0 or char_height <= 0:
            return

        # Prefer explicit terminal size so the grid matches the intended virtual terminal.
        if self._theme.terminal_size is not None:
            cols, rows = self._theme.terminal_size
        else:
            cols = max(0, (width - padding * 2) // char_width)
            rows = max(0, (height - padding * 2) // char_height)

        every = int(getattr(self._theme, "debug_grid_every", 1) or 1)
        if every < 1:
            every = 1

        # Use a dimmed foreground so the grid is visible but not overpowering.
        grid_color: str = self._theme.foreground
        try:
            from styledconsole.utils.color import apply_dim

            dimmed = apply_dim(grid_color)
            if isinstance(dimmed, str) and dimmed:
                grid_color = dimmed
        except Exception:
            pass

        # Vertical lines
        for c in range(0, cols + 1, every):
            x = padding + c * char_width
            draw.line([(x, padding), (x, padding + rows * char_height)], fill=grid_color, width=1)

        # Horizontal lines
        for r in range(0, rows + 1, every):
            y = padding + r * char_height
            draw.line([(padding, y), (padding + cols * char_width, y)], fill=grid_color, width=1)

    def _create_emoji_renderer(self, img: PILImage.Image) -> Any:
        """Create emoji renderer for the image if enabled.

        Args:
            img: PIL Image to render on.

        Returns:
            EmojiRenderer instance or None.
        """
        if not self._render_emojis:
            return None

        try:
            from .emoji_renderer import EmojiRenderer, NotoColorEmojiSource

            source = self._emoji_source or NotoColorEmojiSource()
            return EmojiRenderer(
                image=img,
                source=source,
                emoji_scale_factor=1.0,
                emoji_position_offset=(0, 0),
                char_width=self._font_loader.char_width,
                line_height=int(self._font_loader.char_height),
            )
        except ImportError:
            return None

    def _render_lines(self, draw: Any, lines: list[list[Segment]], emoji_renderer: Any) -> None:
        """Render all lines to the image.

        Args:
            draw: PIL ImageDraw instance.
            lines: List of lines with segments.
            emoji_renderer: EmojiRenderer instance or None.
        """
        y = self._theme.padding
        char_height = self._font_loader.char_height

        for line in lines:
            self._render_line(draw, line, y, emoji_renderer)
            y += int(char_height)

    def _render_line(self, draw: Any, line: list[Segment], y: int, emoji_renderer: Any) -> None:
        """Render a single line to the image.

        Args:
            draw: PIL ImageDraw instance.
            line: List of segments in the line.
            y: Y position for the line.
            emoji_renderer: EmojiRenderer instance or None.
        """
        x = self._theme.padding
        char_height = self._font_loader.char_height
        font = self._font_loader.font

        for segment in line:
            text = segment.text
            style = segment.style

            # Get colors and text style
            fg_color = self._theme.foreground
            bg_color = None
            text_style = TextStyle()

            if style:
                if style.color:
                    fg_color = self._get_color_hex(style.color) or fg_color
                if style.bgcolor:
                    bg_color = self._get_color_hex(style.bgcolor)
                text_style = TextStyle.from_rich_style(style)

            # Calculate text width
            if emoji_renderer:
                text_width = emoji_renderer.getwidth(text, font=font)
            else:
                text_width = self._measure_text_width_cells(text)

            # Draw background if present
            if bg_color:
                draw.rectangle(
                    [x, y, x + text_width, y + int(char_height)],
                    fill=bg_color,
                )

            # Draw text
            if emoji_renderer:
                emoji_renderer.text(
                    (x, y),
                    text,
                    fill=fg_color,
                    font=font,
                    spacing=0,
                    fallback_font=self._font_loader.fallback_font,
                    is_braille_func=self._is_braille,
                    text_style=text_style,
                    font_family=self._font_loader.font_family,
                )
            else:
                self._render_text_with_fallback(draw, x, y, text, fg_color, text_style)

            x += text_width

    def _measure_text_width_cells(self, text: str) -> int:
        """Measure text width in pixels using visual_width.

        Uses visual_width which respects the render target context ("image" mode
        treats all emojis as 2 cells for consistency with layout calculations).
        """
        from styledconsole.utils.text import visual_width

        char_width = self._font_loader.char_width
        return visual_width(text) * char_width

    # -------------------------------------------------------------------------
    # Animation support
    # -------------------------------------------------------------------------

    def capture_frame(self) -> None:
        """Capture current console output as a frame for animation.

        Call this method after each state change to build an animation.
        """
        frame = self._render_frame()
        self._frames.append(frame)

    def clear_frames(self) -> None:
        """Clear all captured frames."""
        self._frames.clear()

    # -------------------------------------------------------------------------
    # Save methods
    # -------------------------------------------------------------------------

    def save_png(
        self,
        path: str | Path,
        *,
        scale: float = 1.0,
        do_auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save console output as PNG image.

        Args:
            path: Output file path.
            scale: Scale factor (e.g., 2.0 for retina displays).
            do_auto_crop: If True, crop to content with margin. Defaults to False.
            crop_margin: Margin in pixels when do_auto_crop is True. Defaults to 20.
        """
        pil_image, _, _ = self._lazy_import_pillow()

        img = self._render_frame()

        if do_auto_crop:
            img = auto_crop(img, self._theme.background, margin=crop_margin)

        if scale != 1.0:
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, pil_image.Resampling.LANCZOS)

        img.save(str(path), "PNG")

    def save_webp(
        self,
        path: str | Path,
        *,
        quality: int = 90,
        animated: bool = False,
        fps: int = 10,
        loop: int = 0,
        do_auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save console output as WebP image.

        Args:
            path: Output file path.
            quality: Image quality (0-100). Defaults to 90.
            animated: If True, save as animated WebP using captured frames.
            fps: Frames per second for animation. Defaults to 10.
            loop: Number of loops (0 = infinite). Defaults to 0.
            do_auto_crop: If True, crop to content with margin. Defaults to False.
            crop_margin: Margin in pixels when do_auto_crop is True. Defaults to 20.
        """
        if animated:
            self._save_animated(
                str(path),
                "WEBP",
                fps=fps,
                loop=loop,
                quality=quality,
                do_auto_crop=do_auto_crop,
                crop_margin=crop_margin,
            )
        else:
            img = self._render_frame()
            if do_auto_crop:
                img = auto_crop(img, self._theme.background, margin=crop_margin)
            img.save(str(path), "WEBP", quality=quality)

    def save_gif(
        self,
        path: str | Path,
        *,
        fps: int = 10,
        loop: int = 0,
        do_auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save console output as animated GIF.

        Args:
            path: Output file path.
            fps: Frames per second. Defaults to 10.
            loop: Number of loops (0 = infinite). Defaults to 0.
            do_auto_crop: If True, crop all frames to common bounding box.
            crop_margin: Margin in pixels when do_auto_crop is True. Defaults to 20.
        """
        self._save_animated(
            str(path),
            "GIF",
            fps=fps,
            loop=loop,
            do_auto_crop=do_auto_crop,
            crop_margin=crop_margin,
        )

    def _save_animated(
        self,
        path: str,
        fmt: str,
        *,
        fps: int = 10,
        loop: int = 0,
        quality: int = 90,
        do_auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save captured frames as animation.

        Args:
            path: Output file path.
            fmt: Image format ("GIF" or "WEBP").
            fps: Frames per second.
            loop: Number of loops (0 = infinite).
            quality: Quality for WebP (ignored for GIF).
            do_auto_crop: If True, crop all frames to common bounding box.
            crop_margin: Margin in pixels when do_auto_crop is True.
        """
        frames = self._frames if self._frames else [self._render_frame()]
        bg_color = self._theme.background

        # Auto-crop all frames to common bounding box
        if do_auto_crop and len(frames) > 1:
            frames = auto_crop_frames(frames, bg_color, margin=crop_margin)

        if len(frames) == 1:
            self._save_single_frame(path, fmt, frames[0], quality, do_auto_crop, crop_margin)
            return

        self._save_multiple_frames(path, fmt, frames, fps, loop, quality)

    def _save_single_frame(
        self,
        path: str,
        fmt: str,
        frame: PILImage.Image,
        quality: int,
        do_auto_crop: bool,
        crop_margin: int,
    ) -> None:
        """Save a single frame as static image.

        Args:
            path: Output file path.
            fmt: Image format.
            frame: Frame to save.
            quality: Quality for WebP.
            do_auto_crop: Whether to auto-crop.
            crop_margin: Crop margin in pixels.
        """
        if do_auto_crop:
            frame = auto_crop(frame, self._theme.background, margin=crop_margin)
        if fmt == "GIF":
            frame.save(path, fmt)
        else:
            frame.save(path, fmt, quality=quality)

    def _save_multiple_frames(
        self,
        path: str,
        fmt: str,
        frames: list[PILImage.Image],
        fps: int,
        loop: int,
        quality: int,
    ) -> None:
        """Save multiple frames as animation.

        Args:
            path: Output file path.
            fmt: Image format.
            frames: List of frames to save.
            fps: Frames per second.
            loop: Number of loops.
            quality: Quality for WebP.
        """
        duration = 1000 // fps

        save_kwargs: dict[str, Any] = {
            "save_all": True,
            "append_images": frames[1:],
            "duration": duration,
            "loop": loop,
        }

        if fmt == "WEBP":
            save_kwargs["quality"] = quality

        frames[0].save(path, fmt, **save_kwargs)


__all__ = ["DEFAULT_THEME", "FontFamily", "ImageExporter", "ImageTheme", "TextStyle"]
