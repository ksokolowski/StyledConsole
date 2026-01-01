"""Image export functionality for Console output.

This module provides image export capabilities using Pillow, supporting
PNG, WebP, GIF, and AVIF formats with both static and animated output.

Requires: pip install styledconsole[image] (or Pillow>=10.0.0)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from PIL import Image as PILImage
    from PIL import ImageFont as PILImageFont
    from rich.console import Console as RichConsole
    from rich.segment import Segment

    from .emoji_renderer import BaseEmojiSource


@dataclass
class ImageTheme:
    """Color theme for image export."""

    background: str = "#11111b"  # Darker background (Catppuccin Mocha Crust)
    foreground: str = "#cdd6f4"  # Light text
    font_size: int = 16
    padding: int = 20
    line_height: float = 1.4  # Good spacing for readability and emoji fit
    # Fixed terminal size (columns, rows). If set, image will always be this size.
    # None means auto-size based on content.
    terminal_size: tuple[int, int] | None = None


@dataclass
class FontFamily:
    """Collection of font variants for a font family.

    Manages Regular, Bold, Italic, and Bold+Italic font variants for
    styled text rendering in image export.
    """

    regular: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None
    bold: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
    italic: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
    bold_italic: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None

    def get_font(
        self, bold: bool = False, italic: bool = False
    ) -> PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None:
        """Get appropriate font variant for requested style.

        Args:
            bold: Whether bold style is requested.
            italic: Whether italic style is requested.

        Returns:
            The most appropriate font variant available.
        """
        if bold and italic and self.bold_italic:
            return self.bold_italic
        if bold and self.bold:
            return self.bold
        if italic and self.italic:
            return self.italic
        return self.regular


@dataclass
class TextStyle:
    """Text style properties for rendering.

    Captures Rich text style attributes for image rendering.
    """

    bold: bool = False
    italic: bool = False
    underline: bool = False
    strike: bool = False
    overline: bool = False
    dim: bool = False

    @classmethod
    def from_rich_style(cls, style) -> TextStyle:
        """Create TextStyle from Rich Style object.

        Args:
            style: Rich Style object or None.

        Returns:
            TextStyle with properties extracted from Rich style.
        """
        if style is None:
            return cls()
        return cls(
            bold=bool(style.bold),
            italic=bool(style.italic),
            underline=bool(style.underline),
            strike=bool(style.strike),
            overline=bool(getattr(style, "overline", False)),
            dim=bool(style.dim),
        )


# Default theme matching common terminal dark themes
DEFAULT_THEME = ImageTheme()

# Standard ANSI color palette (used when Rich provides standard colors)
ANSI_COLORS = {
    0: "#000000",  # Black
    1: "#cc0000",  # Red
    2: "#00cc00",  # Green
    3: "#cccc00",  # Yellow
    4: "#0000cc",  # Blue
    5: "#cc00cc",  # Magenta
    6: "#00cccc",  # Cyan
    7: "#cccccc",  # White
    8: "#666666",  # Bright Black
    9: "#ff0000",  # Bright Red
    10: "#00ff00",  # Bright Green
    11: "#ffff00",  # Bright Yellow
    12: "#0000ff",  # Bright Blue
    13: "#ff00ff",  # Bright Magenta
    14: "#00ffff",  # Bright Cyan
    15: "#ffffff",  # Bright White
}


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
            emoji_source: Emoji image source. If None, uses NotoColorEmojiSource (local font).
            render_emojis: Whether to render emojis as images. Defaults to True.
        """
        self._console = rich_console
        self._theme = theme or DEFAULT_THEME
        self._font_path = font_path
        self._emoji_source = emoji_source
        self._render_emojis = render_emojis
        self._font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
        self._font_family: FontFamily | None = None
        self._fallback_font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
        self._char_width: int = 0
        self._char_height: float = 0.0
        self._frames: list[PILImage.Image] = []

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

    def _try_load_font(
        self, image_font_module: Any, path: str, size: int
    ) -> PILImageFont.FreeTypeFont | PILImageFont.ImageFont:
        """Try to load a font, return None on failure.

        Args:
            image_font_module: PIL ImageFont module.
            path: Path to the font file.
            size: Font size in pixels.

        Returns:
            Loaded font or None if loading failed.
        """
        try:
            return image_font_module.truetype(path, size)
        except OSError:
            # Fall back to a default ImageFont to keep return type non-optional
            return image_font_module.load_default()

    def _load_font(self, image_font_module: Any) -> None:
        """Load monospace font family with all available variants.

        Loads DejaVu Sans Mono as primary (complete bold/italic/bolditalic set),
        with Noto Sans Mono as fallback (bold only, no italic).

        Args:
            image_font_module: PIL ImageFont module.
        """
        font_size = self._theme.font_size

        # DejaVu font family paths (complete set with bold/italic/bolditalic)
        dejavu_paths = {
            "regular": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "italic": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf",
            "bold_italic": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-BoldOblique.ttf",
        }

        # Noto fallback paths (no italic variants available)
        noto_paths = {
            "regular": "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
            "bold": "/usr/share/fonts/truetype/noto/NotoSansMono-Bold.ttf",
        }

        # Try user-specified font first (single variant only)
        if self._font_path:
            font = self._try_load_font(image_font_module, self._font_path, font_size)
            if font:
                self._font = font
                self._font_family = FontFamily(regular=font)
                self._calculate_char_dimensions()
                self._load_fallback_font(image_font_module)
                return

        # Try DejaVu family first (complete set for full style support)
        regular = self._try_load_font(image_font_module, dejavu_paths["regular"], font_size)
        if regular:
            bold = self._try_load_font(image_font_module, dejavu_paths["bold"], font_size)
            italic = self._try_load_font(image_font_module, dejavu_paths["italic"], font_size)
            bold_italic = self._try_load_font(
                image_font_module, dejavu_paths["bold_italic"], font_size
            )
            self._font = regular
            self._font_family = FontFamily(
                regular=regular, bold=bold, italic=italic, bold_italic=bold_italic
            )
            self._calculate_char_dimensions()
            self._load_fallback_font(image_font_module)
            return

        # Try Noto family (bold only, no italic)
        regular = self._try_load_font(image_font_module, noto_paths["regular"], font_size)
        if regular:
            bold = self._try_load_font(image_font_module, noto_paths["bold"], font_size)
            self._font = regular
            self._font_family = FontFamily(regular=regular, bold=bold)
            self._calculate_char_dimensions()
            self._load_fallback_font(image_font_module)
            return

        # Fallback to default font (no variants)
        self._font = image_font_module.load_default()
        self._font_family = FontFamily(regular=self._font)
        self._calculate_char_dimensions()
        self._load_fallback_font(image_font_module)

    def _load_fallback_font(self, image_font_module: Any) -> None:
        """Load fallback font for characters not supported by primary font (e.g., Braille).

        Args:
            image_font_module: PIL ImageFont module.
        """
        font_size = self._theme.font_size
        self._fallback_font = None

        # Fonts with Braille support
        # Noto Sans Symbols 2 preferred for consistent Noto family look
        braille_fonts = [
            "/usr/share/fonts/truetype/noto/NotoSansSymbols2-Regular.ttf",
            "NotoSansSymbols2-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
            "FreeMono.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
            "DejaVuSansMono.ttf",
        ]

        for font_name in braille_fonts:
            try:
                self._fallback_font = image_font_module.truetype(font_name, font_size)
                return
            except OSError:
                continue

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

    def _render_text_with_fallback(
        self,
        draw,
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

        # Apply dim effect if needed
        actual_color = color
        if text_style and text_style.dim:
            actual_color = self._apply_dim_color(color)

        for char in text:
            font = self._get_font_for_char(char, text_style)
            draw.text((current_x, y), char, font=font, fill=actual_color)

            # Draw decorations for this character
            if text_style:
                self._draw_char_decorations(
                    draw, current_x, y, self._char_width, text_style, actual_color
                )

            current_x += self._char_width

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
        if self._is_braille(char) and self._fallback_font is not None:
            return self._fallback_font

        # Select font variant based on style
        if self._font_family and text_style:
            return self._font_family.get_font(text_style.bold, text_style.italic)

        return self._font

    def _apply_dim_color(self, color: str) -> str:
        """Apply dim effect by darkening the color.

        Args:
            color: Hex color string like "#RRGGBB".

        Returns:
            Darkened hex color string.
        """
        if not color.startswith("#") or len(color) != 7:
            return color

        try:
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)

            # Dim by reducing to 50% brightness
            r = r // 2
            g = g // 2
            b = b // 2

            return f"#{r:02x}{g:02x}{b:02x}"
        except ValueError:
            return color

    def _draw_char_decorations(
        self,
        draw,
        x: int,
        y: int,
        width: int,
        text_style: TextStyle,
        color: str,
    ) -> None:
        """Draw text decorations (underline, strikethrough, overline) for a character.

        Args:
            draw: PIL ImageDraw instance.
            x: Character x position.
            y: Character y position.
            width: Character width.
            text_style: Text style properties.
            color: Decoration color.
        """
        line_thickness = max(1, int(self._char_height) // 12)

        if text_style.underline:
            underline_y = y + int(self._char_height) - 3
            draw.line(
                [(x, underline_y), (x + width, underline_y)],
                fill=color,
                width=line_thickness,
            )

        if text_style.strike:
            strike_y = y + int(self._char_height) // 2
            draw.line(
                [(x, strike_y), (x + width, strike_y)],
                fill=color,
                width=line_thickness,
            )

        if text_style.overline:
            overline_y = y + 2
            draw.line(
                [(x, overline_y), (x + width, overline_y)],
                fill=color,
                width=line_thickness,
            )

    def _calculate_char_dimensions(self) -> None:
        """Calculate character width and height for the loaded font."""
        from PIL import Image, ImageDraw

        # Create a temporary image to measure text
        temp_img = Image.new("RGB", (100, 100))
        draw = ImageDraw.Draw(temp_img)

        # Ensure font is loaded for type checkers
        assert self._font is not None

        # Measure character width using getlength for accuracy
        # (getlength returns fractional advance width, textbbox gives integer bounds)
        try:
            # Use getlength for accurate width (Pillow 9.2+)
            self._char_width = int(self._font.getlength("M"))
        except AttributeError:
            # Fallback for older Pillow versions
            bbox = draw.textbbox((0, 0), "M", font=self._font)
            self._char_width = int(bbox[2] - bbox[0])

        # Calculate height from bounding box with line_height factor
        bbox = draw.textbbox((0, 0), "M", font=self._font)
        char_height = bbox[3] - bbox[1]
        # Calculate and store (possibly fractional) line height for layout
        self._char_height = char_height * self._theme.line_height

    def _get_color_hex(self, color) -> str | None:
        """Convert Rich color to hex string.

        Args:
            color: Rich Color object or None.

        Returns:
            Hex color string like "#RRGGBB" or None.
        """
        if color is None:
            return None

        # Get truecolor representation
        triplet = color.get_truecolor()
        return f"#{triplet.red:02x}{triplet.green:02x}{triplet.blue:02x}"

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
                # Handle text with embedded newlines
                parts = segment.text.split("\n")
                for i, part in enumerate(parts):
                    if part:
                        # Create new segment with just this part
                        from rich.segment import Segment as RichSegment

                        lines[-1].append(RichSegment(part, segment.style, segment.control))
                    if i < len(parts) - 1:
                        lines.append([])

        # Remove trailing empty line if present
        if lines and not lines[-1]:
            lines.pop()

        return lines

    def _calculate_dimensions(self) -> tuple[int, int]:
        """Calculate image dimensions based on recorded content or fixed terminal size.

        Returns:
            Tuple of (width, height) in pixels.
        """
        # If fixed terminal size is set, use it
        if self._theme.terminal_size is not None:
            cols, rows = self._theme.terminal_size
            width = int(self._theme.padding * 2 + cols * self._char_width)
            height = int(self._theme.padding * 2 + rows * self._char_height)
            return width, height

        lines = self._get_segments_by_line()

        if not lines:
            # Minimum dimensions for empty content
            return (
                int(self._theme.padding * 2 + self._char_width * 10),
                int(self._theme.padding * 2 + self._char_height),
            )

        # Create a temporary emoji renderer for width calculation if enabled
        width_calculator = None
        if self._render_emojis:
            try:
                # Create temporary renderer just for size calculation
                # (we don't need an actual image for getwidth)
                from PIL import Image as PILImage

                from .emoji_renderer import EmojiRenderer, NotoColorEmojiSource

                temp_img = PILImage.new("RGB", (1, 1))
                source = self._emoji_source or NotoColorEmojiSource()
                width_calculator = EmojiRenderer(
                    image=temp_img,
                    source=source,
                    emoji_scale_factor=1.0,
                    char_width=self._char_width,  # For proper emoji alignment
                )
            except ImportError:
                pass

        # Calculate max line width
        max_width = 0
        for line in lines:
            line_width = 0
            for seg in line:
                if width_calculator:
                    line_width += width_calculator.getwidth(seg.text, font=self._font)
                else:
                    line_width += len(seg.text) * self._char_width
            max_width = max(max_width, line_width)

        width = int(self._theme.padding * 2 + max_width)
        height = int(self._theme.padding * 2 + len(lines) * self._char_height)

        return width, height

    def _render_frame(self) -> PILImage.Image:
        """Render current console output to PIL Image.

        Returns:
            PIL Image with rendered console output.
        """
        pil_image, pil_draw, pil_font = self._lazy_import_pillow()

        # Load font if not already loaded
        if self._font is None:
            self._load_font(pil_font)

        # Calculate dimensions
        width, height = self._calculate_dimensions()

        # Create image with background color
        img = pil_image.new("RGB", (width, height), self._theme.background)
        draw = pil_draw.Draw(img)

        # Set up emoji renderer if enabled
        emoji_renderer = None
        if self._render_emojis:
            try:
                from .emoji_renderer import EmojiRenderer, NotoColorEmojiSource

                source = self._emoji_source or NotoColorEmojiSource()
                emoji_renderer = EmojiRenderer(
                    image=img,
                    source=source,
                    emoji_scale_factor=1.0,
                    emoji_position_offset=(0, 0),
                    char_width=self._char_width,  # For proper emoji alignment
                    line_height=int(self._char_height),  # Scale emoji to fit line height
                )
            except ImportError:
                pass  # Emoji rendering not available

        # Get segments organized by line
        lines = self._get_segments_by_line()

        # Render each line
        y = self._theme.padding
        for line in lines:
            x = self._theme.padding

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

                # Calculate actual text width (accounting for emojis if renderer available)
                if emoji_renderer:
                    text_width = emoji_renderer.getwidth(text, font=self._font)
                else:
                    text_width = len(text) * self._char_width

                # Draw background if present
                if bg_color:
                    draw.rectangle(
                        [x, y, x + text_width, y + int(self._char_height)],
                        fill=bg_color,
                    )

                # Draw text (with emoji support if available)
                # Handle Braille characters with fallback font
                if emoji_renderer:
                    # Use emoji renderer for text with potential emojis
                    # Pass fallback font for Braille support and text style for formatting
                    emoji_renderer.text(
                        (x, y),
                        text,
                        fill=fg_color,
                        font=self._font,
                        spacing=0,
                        fallback_font=self._fallback_font,
                        is_braille_func=self._is_braille,
                        text_style=text_style,
                        font_family=self._font_family,
                    )
                else:
                    # Render text character by character to handle font fallback
                    self._render_text_with_fallback(draw, x, y, text, fg_color, text_style)

                # Move x position using calculated width
                x += text_width

                # Move to next line
            y += int(self._char_height)

        return img

    def _auto_crop(
        self,
        img: PILImage.Image,
        margin: int = 20,
        background_color: str | None = None,
    ) -> PILImage.Image:
        """Auto-crop image to content with margin.

        Finds the bounding box of non-background pixels and crops with a margin.

        Note: This method is for static images only. For animations, all frames
        need to be cropped to a common bounding box to prevent "jumping".

        Args:
            img: PIL Image to crop.
            margin: Margin in pixels around content. Defaults to 20.
            background_color: Background color to detect. If None, uses theme background.

        Returns:
            Cropped PIL Image.
        """
        from PIL import Image, ImageChops

        bg_color = background_color or self._theme.background
        bg = Image.new("RGB", img.size, bg_color)
        diff = ImageChops.difference(img.convert("RGB"), bg)
        bbox = diff.getbbox()

        if bbox is None:
            return img

        x1, y1, x2, y2 = bbox
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(img.width, x2 + margin)
        y2 = min(img.height, y2 + margin)

        return img.crop((x1, y1, x2, y2))

    def _get_content_bbox(
        self,
        img: PILImage.Image,
        background_color: str | None = None,
    ) -> tuple[int, int, int, int] | None:
        """Get bounding box of non-background content in image.

        Args:
            img: PIL Image to analyze.
            background_color: Background color to detect. If None, uses theme background.

        Returns:
            Bounding box tuple (x1, y1, x2, y2) or None if image is entirely background.
        """
        from PIL import Image, ImageChops

        bg_color = background_color or self._theme.background
        bg = Image.new("RGB", img.size, bg_color)
        diff = ImageChops.difference(img.convert("RGB"), bg)
        return diff.getbbox()

    def _auto_crop_frames(
        self,
        frames: list[PILImage.Image],
        margin: int = 20,
        background_color: str | None = None,
    ) -> list[PILImage.Image]:
        """Auto-crop multiple frames to a common bounding box.

        Calculates the union of all content bounding boxes across frames,
        then crops all frames to that same area. This prevents "jumping"
        in animations.

        Args:
            frames: List of PIL Images to crop.
            margin: Margin in pixels around content. Defaults to 20.
            background_color: Background color to detect. If None, uses theme background.

        Returns:
            List of cropped PIL Images, all with identical dimensions.
        """
        if not frames:
            return frames

        # Calculate union of all bounding boxes
        union_bbox: tuple[int, int, int, int] | None = None

        for frame in frames:
            bbox = self._get_content_bbox(frame, background_color)
            if bbox is None:
                continue

            if union_bbox is None:
                union_bbox = bbox
            else:
                # Expand union to include this bbox
                union_bbox = (
                    min(union_bbox[0], bbox[0]),
                    min(union_bbox[1], bbox[1]),
                    max(union_bbox[2], bbox[2]),
                    max(union_bbox[3], bbox[3]),
                )

        if union_bbox is None:
            # All frames are entirely background
            return frames

        # Apply margin to union bbox
        x1, y1, x2, y2 = union_bbox
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(frames[0].width, x2 + margin)
        y2 = min(frames[0].height, y2 + margin)

        # Crop all frames to the same bbox
        return [frame.crop((x1, y1, x2, y2)) for frame in frames]

    def capture_frame(self) -> None:
        """Capture current console output as a frame for animation.

        Call this method after each state change to build an animation.
        """
        frame = self._render_frame()
        self._frames.append(frame)

    def clear_frames(self) -> None:
        """Clear all captured frames."""
        self._frames.clear()

    def save_png(
        self,
        path: str | Path,
        *,
        scale: float = 1.0,
        auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save console output as PNG image.

        Args:
            path: Output file path.
            scale: Scale factor (e.g., 2.0 for retina displays).
            auto_crop: If True, crop to content with margin. Defaults to False.
            crop_margin: Margin in pixels when auto_crop is True. Defaults to 20.
        """
        pil_image, _, _ = self._lazy_import_pillow()

        img = self._render_frame()

        if auto_crop:
            img = self._auto_crop(img, margin=crop_margin)

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
        auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save console output as WebP image.

        Args:
            path: Output file path.
            quality: Image quality (0-100). Defaults to 90.
            animated: If True, save as animated WebP using captured frames.
            fps: Frames per second for animation. Defaults to 10.
            loop: Number of loops (0 = infinite). Defaults to 0.
            auto_crop: If True, crop to content with margin. Defaults to False.
                For animations, all frames are cropped to a common bounding box.
            crop_margin: Margin in pixels when auto_crop is True. Defaults to 20.
        """
        if animated:
            self._save_animated(
                str(path),
                "WEBP",
                fps=fps,
                loop=loop,
                quality=quality,
                auto_crop=auto_crop,
                crop_margin=crop_margin,
            )
        else:
            img = self._render_frame()
            if auto_crop:
                img = self._auto_crop(img, margin=crop_margin)
            img.save(str(path), "WEBP", quality=quality)

    def save_gif(
        self,
        path: str | Path,
        *,
        fps: int = 10,
        loop: int = 0,
        auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save console output as animated GIF.

        Args:
            path: Output file path.
            fps: Frames per second. Defaults to 10.
            loop: Number of loops (0 = infinite). Defaults to 0.
            auto_crop: If True, crop all frames to common bounding box. Defaults to False.
            crop_margin: Margin in pixels when auto_crop is True. Defaults to 20.
        """
        self._save_animated(
            str(path), "GIF", fps=fps, loop=loop, auto_crop=auto_crop, crop_margin=crop_margin
        )

    def _save_animated(
        self,
        path: str,
        format: str,
        *,
        fps: int = 10,
        loop: int = 0,
        quality: int = 90,
        auto_crop: bool = False,
        crop_margin: int = 20,
    ) -> None:
        """Save captured frames as animation.

        Args:
            path: Output file path.
            format: Image format ("GIF" or "WEBP").
            fps: Frames per second.
            loop: Number of loops (0 = infinite).
            quality: Quality for WebP (ignored for GIF).
            auto_crop: If True, crop all frames to common bounding box.
            crop_margin: Margin in pixels when auto_crop is True.
        """
        frames = self._frames if self._frames else [self._render_frame()]

        # Auto-crop all frames to common bounding box
        if auto_crop and len(frames) > 1:
            frames = self._auto_crop_frames(frames, margin=crop_margin)

        if len(frames) == 1:
            # Single frame - just save as static
            if auto_crop:
                frames[0] = self._auto_crop(frames[0], margin=crop_margin)
            if format == "GIF":
                frames[0].save(path, format)
            else:
                frames[0].save(path, format, quality=quality)
            return

        # Calculate duration per frame in milliseconds
        duration = 1000 // fps

        # Save animated image
        save_kwargs = {
            "save_all": True,
            "append_images": frames[1:],
            "duration": duration,
            "loop": loop,
        }

        if format == "WEBP":
            save_kwargs["quality"] = quality

        frames[0].save(path, format, **save_kwargs)


__all__ = ["DEFAULT_THEME", "FontFamily", "ImageExporter", "ImageTheme", "TextStyle"]
