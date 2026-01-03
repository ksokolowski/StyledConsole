import unittest
from unittest.mock import MagicMock, patch

from styledconsole.export.font_loader import FontFinder, FontLoader
from styledconsole.export.image_theme import ImageTheme


class TestFontFinder(unittest.TestCase):
    def test_find_font_cached(self):
        finder = FontFinder()
        # Mock the internal cache
        finder._cache["TestFont:Regular"] = "/path/to/font.ttf"

        path = finder.find_font(["TestFont"], "Regular")
        self.assertEqual(path, "/path/to/font.ttf")

    @patch("styledconsole.export.font_loader.shutil.which")
    def test_find_font_no_fc_list(self, mock_which):
        # Simulate no fc-list
        mock_which.return_value = None

        finder = FontFinder()
        # Should fall back to directory scan, which returns None in empty env
        # unless we mock os.walk as well, but here we just want to ensure it doesn't crash
        path = finder.find_font(["NonExistentFont"], "Regular")
        self.assertIsNone(path)

    @patch("styledconsole.export.font_loader.shutil.which")
    @patch("styledconsole.export.font_loader.subprocess.check_output")
    def test_find_font_fc_list(self, mock_subprocess, mock_which):
        mock_which.return_value = "/usr/bin/fc-list"
        mock_subprocess.return_value = (
            "/usr/share/fonts/dejavu/DejaVuSansMono.ttf: DejaVu Sans Mono:style=Book,Regular\n"
        )

        finder = FontFinder()
        path = finder.find_font(["DejaVu Sans Mono"], "Regular")
        self.assertEqual(path, "/usr/share/fonts/dejavu/DejaVuSansMono.ttf")

    def test_find_mono_family_structure(self):
        finder = FontFinder()
        # We Mock find_font to return dummy paths
        finder.find_font = MagicMock(side_effect=lambda names, style: f"/path/{style}.ttf")

        family = finder.find_mono_family()
        self.assertEqual(family["regular"], "/path/Regular.ttf")
        self.assertEqual(family["bold"], "/path/Bold.ttf")


class TestFontLoader(unittest.TestCase):
    @patch("styledconsole.export.font_loader.FontFinder.find_mono_family")
    def test_load_uses_finder(self, mock_find_family):
        mock_find_family.return_value = {
            "regular": "/path/reg.ttf",
            "bold": None,
            "italic": None,
            "bold_italic": None,
        }

        mock_font_module = MagicMock()
        mock_font = MagicMock()
        mock_font_module.truetype.return_value = mock_font
        mock_font.getlength.return_value = 10
        mock_font.getbbox.return_value = (0, 0, 10, 20)

        theme = ImageTheme()
        loader = FontLoader(theme)
        loader.load(mock_font_module)

        self.assertIsNotNone(loader.font)
        mock_font_module.truetype.assert_called()


if __name__ == "__main__":
    unittest.main()
