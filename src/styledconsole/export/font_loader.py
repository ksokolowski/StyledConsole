"""Font loading utilities for image export.

This module provides the FontLoader class that handles loading
monospace font families with Regular, Bold, Italic, and Bold+Italic variants.

It includes a cross-platform FontFinder that attempts to locate
suitable fonts on Linux, macOS, and Windows.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .config import (
    FONT_DIRS,
    FONT_MEASURE_CHAR,
    FONT_NAMES_EMOJI,
    FONT_NAMES_MONOSPACE,
    TEMP_IMAGE_SIZE,
)

if TYPE_CHECKING:
    from PIL import ImageFont as PILImageFont

    from .image_theme import FontFamily, ImageTheme

__all__ = [
    "FontFinder",
    "FontLoader",
]


class FontFinder:
    """Cross-platform font discovery utility.

    Attempts to find font files by:
    1. Using `fc-list` if available (Linux/macOS)
    2. Scanning standard system font directories
    """

    def __init__(self) -> None:
        self._cache: dict[str, str | None] = {}
        self._system = sys.platform

    def find_font(self, font_names: list[str], style: str = "Regular") -> str | None:
        """Find the first available font from a list of names.

        Args:
            font_names: List of font family names to search for.
            style: Font style (Regular, Bold, Italic, Bold Italic).

        Returns:
            Path to the font file, or None if not found.
        """
        for name in font_names:
            cache_key = f"{name}:{style}"
            if cache_key in self._cache:
                if self._cache[cache_key]:
                    return self._cache[cache_key]
                continue

            path = self._find_single_font(name, style)
            if path:
                self._cache[cache_key] = path
                return path
            self._cache[cache_key] = None

        return None

    def _find_single_font(self, name: str, style: str) -> str | None:
        """Find a single font family and style."""
        # Try fc-list (Linux key-value format)
        result = self._try_fc_list(name, style)
        if result:
            return result

        # Fallback: Scan standard directories
        return self._scan_font_directories(name, style)

    def _try_fc_list(self, name: str, style: str) -> str | None:
        """Try to find font using fc-list command."""
        if not shutil.which("fc-list"):
            return None

        try:
            # fc-list : family style file
            cmd = ["fc-list", ":", "family", "style", "file"]
            output = subprocess.check_output(cmd, text=True)
            for line in output.splitlines():
                if ":" not in line:
                    continue
                parts = [p.strip() for p in line.split(":")]
                if len(parts) < 3:
                    # Sometimes family/style might contain colons?
                    # But basic format is file: family: style
                    # If file path has colon, we might have issues, but unlikely for font paths.
                    continue

                # parts[0] is often file, but check valid index
                # fc-list output with 3 args usually gives: file: family: style
                file_path = parts[0]
                families = [f.strip() for f in parts[1].split(",")]
                styles = [s.strip() for s in parts[2].split(",")]

                if name in families and style in styles:
                    return file_path
        except subprocess.SubprocessError:
            pass

        return None

    def _get_search_directories(self) -> list[str]:
        """Get font search directories for current platform."""
        if self._system == "linux":
            return [os.path.expanduser(d) for d in FONT_DIRS["linux"]]
        elif self._system == "darwin":
            return [os.path.expanduser(d) for d in FONT_DIRS["darwin"]]
        elif self._system == "win32":
            return [os.path.expandvars(d) for d in FONT_DIRS["win32"]]
        return []

    def _get_style_suffixes(self, style: str) -> list[str]:
        """Get common filename suffixes for a font style."""
        suffixes_map = {
            "Regular": ["-Regular", "Regular"],
            "Bold": ["-Bold", "Bold", "Bd", "b"],
            "Italic": ["-Italic", "Italic", "-Oblique", "Oblique", "It", "i"],
            "Bold Italic": ["-BoldItalic", "BoldItalic", "-BoldOblique", "BoldOblique", "z"],
        }
        return suffixes_map.get(style, [])

    def _check_font_file(
        self, filename: str, clean_name: str, style: str, suffixes: list[str], root: str
    ) -> str | None:
        """Check if a font file matches the desired name and style."""
        if not filename.lower().endswith((".ttf", ".otf")):
            return None

        # Check if filename roughly matches
        if clean_name.lower() not in filename.lower():
            return None

        # Special case for Regular: also match exact filename without suffix
        # e.g. "DejaVuSansMono.ttf"
        if style == "Regular":
            stem = Path(filename).stem
            if stem.lower() == clean_name.lower():
                return os.path.join(root, filename)

        for suffix in suffixes:
            # Strict suffix check to distinguish Bold from BoldItalic
            stem = Path(filename).stem
            if stem.lower().endswith(suffix.lower()):
                return os.path.join(root, filename)

        return None

    def _scan_font_directories(self, name: str, style: str) -> str | None:
        """Scan font directories for matching font file."""
        search_dirs = self._get_search_directories()

        # Simple filename matching (fragile, but better than nothing)
        # e.g., "DejaVu Sans Mono" -> "DejaVuSansMono"
        clean_name = name.replace(" ", "")
        suffixes = self._get_style_suffixes(style)

        for d in search_dirs:
            if not os.path.exists(d):
                continue
            for root, _, files in os.walk(d):
                for f in files:
                    result = self._check_font_file(f, clean_name, style, suffixes, root)
                    if result:
                        return result
        return None

    def find_mono_family(self) -> dict[str, str | None]:
        """Find a complete monospace font family."""
        family_map: dict[str, str | None] = {
            "regular": None,
            "bold": None,
            "italic": None,
            "bold_italic": None,
        }

        # Search for each style in our preferred font list
        # We try to keep the same family for all styles if possible
        for name in FONT_NAMES_MONOSPACE:
            reg = self.find_font([name], "Regular")
            if not reg:
                continue

            # Found a base font, try to find variants
            family_map["regular"] = reg
            family_map["bold"] = self.find_font([name], "Bold")
            family_map["italic"] = self.find_font([name], "Italic")
            family_map["bold_italic"] = self.find_font([name], "Bold Italic")

            return family_map

        return family_map

    def find_fallback_font(self) -> str | None:
        """Find a fallback font for special characters (Braille/Emoji)."""
        # Try finding a font that likely has symbols
        return self.find_font([*FONT_NAMES_EMOJI, "Symbola", "FreeMono"], "Regular")


class FontLoader:
    """Loads and manages font families for image export.

    Attributes:
        font: Primary regular font.
        font_family: FontFamily with all loaded variants.
        fallback_font: Fallback font for special characters.
        char_width: Character width in pixels.
        char_height: Character height in pixels.
    """

    def __init__(self, theme: ImageTheme, font_path: str | None = None) -> None:
        self._theme = theme
        self._font_path = font_path
        self._finder = FontFinder()

        self.font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
        self.font_family: FontFamily | None = None
        self.fallback_font: PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None = None
        self.char_width: int = 0
        self.char_height: float = 0.0

    def load(self, image_font_module: Any) -> None:
        """Load all fonts.

        Args:
            image_font_module: PIL ImageFont module.
        """
        self._load_font_family(image_font_module)
        self._calculate_char_dimensions()
        self._load_fallback_font(image_font_module)

    def _try_load_font(
        self, image_font_module: Any, path: str, size: int
    ) -> PILImageFont.FreeTypeFont | PILImageFont.ImageFont | None:
        """Try to load a font, return None on failure."""
        try:
            return image_font_module.truetype(path, size)
        except OSError:
            return None

    def _load_font_family(self, image_font_module: Any) -> None:
        """Load monospace font family using finder or user path."""
        from .image_theme import FontFamily

        font_size = self._theme.font_size

        # 1. User specified path
        if self._font_path:
            font = self._try_load_font(image_font_module, self._font_path, font_size)
            if font:
                self.font = font
                self.font_family = FontFamily(regular=font)
                return

        # 2. Dynamic Discovery
        paths = self._finder.find_mono_family()

        regular = None
        if paths["regular"]:
            regular = self._try_load_font(image_font_module, paths["regular"], font_size)

        if regular:
            self.font = regular

            bold = None
            if paths["bold"]:
                bold = self._try_load_font(image_font_module, paths["bold"], font_size)

            italic = None
            if paths["italic"]:
                italic = self._try_load_font(image_font_module, paths["italic"], font_size)

            bold_italic = None
            if paths["bold_italic"]:
                bold_italic = self._try_load_font(
                    image_font_module, paths["bold_italic"], font_size
                )

            self.font_family = FontFamily(
                regular=regular, bold=bold, italic=italic, bold_italic=bold_italic
            )
            return

        # 3. Last Resort: PIL Default
        self.font = image_font_module.load_default()
        self.font_family = FontFamily(regular=self.font)

    def _load_fallback_font(self, image_font_module: Any) -> None:
        """Load fallback font for special characters."""
        font_size = self._theme.font_size
        path = self._finder.find_fallback_font()

        if path:
            self.fallback_font = self._try_load_font(image_font_module, path, font_size)

    def _calculate_char_dimensions(self) -> None:
        """Calculate character width and height for the loaded font."""
        from PIL import Image, ImageDraw

        temp_img = Image.new("RGB", TEMP_IMAGE_SIZE)
        draw = ImageDraw.Draw(temp_img)

        assert self.font is not None

        try:
            self.char_width = int(self.font.getlength(FONT_MEASURE_CHAR))
        except AttributeError:
            bbox = draw.textbbox((0, 0), FONT_MEASURE_CHAR, font=self.font)
            self.char_width = int(bbox[2] - bbox[0])

        bbox = draw.textbbox((0, 0), FONT_MEASURE_CHAR, font=self.font)
        char_height = bbox[3] - bbox[1]
        self.char_height = char_height * self._theme.line_height
