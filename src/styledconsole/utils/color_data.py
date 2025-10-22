"""CSS4 and Rich color name definitions.

Complete list of 148 CSS4 named colors from the W3C standard, plus mappings
to Rich's extended color palette for maximum human-readable color support.

Sources:
- CSS4: https://www.w3.org/TR/css-color-4/#named-colors
- Rich: https://github.com/Textualize/rich

This allows using both CSS4 color names (for StyledConsole compatibility)
and Rich color names (for Rich Panel/Text compatibility) throughout the library.
"""

# CSS4 named colors (148 total) - W3C standard
# Sorted alphabetically for easy lookup
CSS4_COLORS = {
    "aliceblue": "#f0f8ff",
    "antiquewhite": "#faebd7",
    "aqua": "#00ffff",
    "aquamarine": "#7fffd4",
    "azure": "#f0ffff",
    "beige": "#f5f5dc",
    "bisque": "#ffe4c4",
    "black": "#000000",
    "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    "burlywood": "#deb887",
    "cadetblue": "#5f9ea0",
    "chartreuse": "#7fff00",
    "chocolate": "#d2691e",
    "coral": "#ff7f50",
    "cornflowerblue": "#6495ed",
    "cornsilk": "#fff8dc",
    "crimson": "#dc143c",
    "cyan": "#00ffff",
    "darkblue": "#00008b",
    "darkcyan": "#008b8b",
    "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    "darkgreen": "#006400",
    "darkgrey": "#a9a9a9",
    "darkkhaki": "#bdb76b",
    "darkmagenta": "#8b008b",
    "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    "darksalmon": "#e9967a",
    "darkseagreen": "#8fbc8f",
    "darkslateblue": "#483d8b",
    "darkslategray": "#2f4f4f",
    "darkslategrey": "#2f4f4f",
    "darkturquoise": "#00ced1",
    "darkviolet": "#9400d3",
    "deeppink": "#ff1493",
    "deepskyblue": "#00bfff",
    "dimgray": "#696969",
    "dimgrey": "#696969",
    "dodgerblue": "#1e90ff",
    "firebrick": "#b22222",
    "floralwhite": "#fffaf0",
    "forestgreen": "#228b22",
    "fuchsia": "#ff00ff",
    "gainsboro": "#dcdcdc",
    "ghostwhite": "#f8f8ff",
    "gold": "#ffd700",
    "goldenrod": "#daa520",
    "gray": "#808080",
    "green": "#008000",
    "greenyellow": "#adff2f",
    "grey": "#808080",
    "honeydew": "#f0fff0",
    "hotpink": "#ff69b4",
    "indianred": "#cd5c5c",
    "indigo": "#4b0082",
    "ivory": "#fffff0",
    "khaki": "#f0e68c",
    "lavender": "#e6e6fa",
    "lavenderblush": "#fff0f5",
    "lawngreen": "#7cfc00",
    "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    "lightcoral": "#f08080",
    "lightcyan": "#e0ffff",
    "lightgoldenrodyellow": "#fafad2",
    "lightgray": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightgrey": "#d3d3d3",
    "lightpink": "#ffb6c1",
    "lightsalmon": "#ffa07a",
    "lightseagreen": "#20b2aa",
    "lightskyblue": "#87cefa",
    "lightslategray": "#778899",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "linen": "#faf0e6",
    "magenta": "#ff00ff",
    "maroon": "#800000",
    "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "mediumseagreen": "#3cb371",
    "mediumslateblue": "#7b68ee",
    "mediumspringgreen": "#00fa9a",
    "mediumturquoise": "#48d1cc",
    "mediumvioletred": "#c71585",
    "midnightblue": "#191970",
    "mintcream": "#f5fffa",
    "mistyrose": "#ffe4e1",
    "moccasin": "#ffe4b5",
    "navajowhite": "#ffdead",
    "navy": "#000080",
    "oldlace": "#fdf5e6",
    "olive": "#808000",
    "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    "orangered": "#ff4500",
    "orchid": "#da70d6",
    "palegoldenrod": "#eee8aa",
    "palegreen": "#98fb98",
    "paleturquoise": "#afeeee",
    "palevioletred": "#db7093",
    "papayawhip": "#ffefd5",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "pink": "#ffc0cb",
    "plum": "#dda0dd",
    "powderblue": "#b0e0e6",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "red": "#ff0000",
    "rosybrown": "#bc8f8f",
    "royalblue": "#4169e1",
    "saddlebrown": "#8b4513",
    "salmon": "#fa8072",
    "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    "seashell": "#fff5ee",
    "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    "slateblue": "#6a5acd",
    "slategray": "#708090",
    "slategrey": "#708090",
    "snow": "#fffafa",
    "springgreen": "#00ff7f",
    "steelblue": "#4682b4",
    "tan": "#d2b48c",
    "teal": "#008080",
    "thistle": "#d8bfd8",
    "tomato": "#ff6347",
    "turquoise": "#40e0d0",
    "violet": "#ee82ee",
    "wheat": "#f5deb3",
    "white": "#ffffff",
    "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    "yellowgreen": "#9acd32",
}


def get_color_names() -> list[str]:
    """Get list of all supported CSS4 color names.

    Returns:
        Sorted list of 148 CSS4 color names

    Example:
        >>> names = get_color_names()
        >>> len(names)
        148
        >>> "red" in names
        True
        >>> "dodgerblue" in names
        True
    """
    return sorted(CSS4_COLORS.keys())


# Rich color name to hex mapping
# These are Rich's ANSI extended colors that don't exist in CSS4
# or have underscored names that map to similar CSS4 colors
RICH_TO_CSS4_MAPPING = {
    # Basic bright colors (Rich style with underscore)
    "bright_black": "#808080",  # gray
    "bright_blue": "#5c5cff",
    "bright_cyan": "#00ffff",
    "bright_green": "#00ff00",  # lime
    "bright_magenta": "#ff00ff",
    "bright_red": "#ff5555",
    "bright_white": "#ffffff",
    "bright_yellow": "#ffff00",
    # Rich underscore variants of CSS4 colors
    "blue_violet": "#8a2be2",  # blueviolet
    "cadet_blue": "#5f9ea0",  # cadetblue
    "cornflower_blue": "#6495ed",  # cornflowerblue
    "dark_blue": "#00008b",  # darkblue
    "dark_cyan": "#008b8b",  # darkcyan
    "dark_goldenrod": "#b8860b",  # darkgoldenrod
    "dark_green": "#006400",  # darkgreen
    "dark_khaki": "#bdb76b",  # darkkhaki
    "dark_magenta": "#8b008b",  # darkmagenta
    "dark_orange": "#ff8c00",  # darkorange
    "dark_red": "#8b0000",  # darkred
    "dark_sea_green": "#8fbc8f",  # darkseagreen
    "dark_turquoise": "#00ced1",  # darkturquoise
    "dark_violet": "#9400d3",  # darkviolet
    "deep_pink": "#ff1493",  # deeppink
    "deep_sky_blue": "#00bfff",  # deepskyblue
    "dodger_blue": "#1e90ff",  # dodgerblue (no number variant)
    "forest_green": "#228b22",  # forestgreen
    "green_yellow": "#adff2f",  # greenyellow
    "hot_pink": "#ff69b4",  # hotpink
    "indian_red": "#cd5c5c",  # indianred
    "light_coral": "#f08080",  # lightcoral
    "light_cyan": "#e0ffff",  # lightcyan
    "light_green": "#90ee90",  # lightgreen
    "light_pink": "#ffb6c1",  # lightpink
    "light_salmon": "#ffa07a",  # lightsalmon
    "light_sea_green": "#20b2aa",  # lightseagreen
    "light_sky_blue": "#87cefa",  # lightskyblue
    "light_slate_blue": "#8470ff",  # Similar to mediumslateblue
    "light_slate_gray": "#778899",  # lightslategray
    "light_slate_grey": "#778899",  # lightslategrey
    "light_steel_blue": "#b0c4de",  # lightsteelblue
    "medium_orchid": "#ba55d3",  # mediumorchid
    "medium_purple": "#9370db",  # mediumpurple
    "medium_spring_green": "#00fa9a",  # mediumspringgreen
    "medium_turquoise": "#48d1cc",  # mediumturquoise
    "medium_violet_red": "#c71585",  # mediumvioletred
    "misty_rose": "#ffe4e1",  # mistyrose
    "navajo_white": "#ffdead",  # navajowhite
    "navy_blue": "#000080",  # navy
    "olive_drab": "#6b8e23",  # olivedrab
    "orange_red": "#ff4500",  # orangered
    "pale_goldenrod": "#eee8aa",  # palegoldenrod
    "pale_green": "#98fb98",  # palegreen
    "pale_turquoise": "#afeeee",  # paleturquoise
    "pale_violet_red": "#db7093",  # palevioletred
    "rosy_brown": "#bc8f8f",  # rosybrown
    "royal_blue": "#4169e1",  # royalblue
    "saddle_brown": "#8b4513",  # saddlebrown
    "sandy_brown": "#f4a460",  # sandybrown
    "sea_green": "#2e8b57",  # seagreen
    "sky_blue": "#87ceeb",  # skyblue
    "slate_blue": "#6a5acd",  # slateblue
    "slate_gray": "#708090",  # slategray
    "slate_grey": "#708090",  # slategrey
    "spring_green": "#00ff7f",  # springgreen
    "steel_blue": "#4682b4",  # steelblue
    "yellow_green": "#9acd32",  # yellowgreen
    # Rich numbered variants (map to closest CSS4 color)
    "aquamarine1": "#7fffd4",  # aquamarine
    "aquamarine3": "#66cdaa",  # mediumaquamarine
    "blue1": "#0000ff",  # blue
    "blue3": "#0000cd",  # mediumblue
    "chartreuse1": "#7fff00",  # chartreuse
    "chartreuse2": "#7fff00",  # chartreuse
    "chartreuse3": "#7fff00",  # chartreuse
    "chartreuse4": "#7fff00",  # chartreuse
    "cornsilk1": "#fff8dc",  # cornsilk
    "cyan1": "#00ffff",  # cyan
    "cyan2": "#00eeee",
    "cyan3": "#00cdcd",
    "dark_olive_green1": "#caff70",
    "dark_olive_green2": "#bcee68",
    "dark_olive_green3": "#a2cd5a",
    "dark_orange3": "#cd8500",
    "dark_sea_green1": "#c1ffc1",
    "dark_sea_green2": "#b4eeb4",
    "dark_sea_green3": "#9bcd9b",
    "dark_sea_green4": "#698b69",
    "dark_slate_gray1": "#97ffff",
    "dark_slate_gray2": "#8deeee",
    "dark_slate_gray3": "#79cdcd",
    "deep_pink1": "#ff1493",  # deeppink
    "deep_pink2": "#ee1289",
    "deep_pink3": "#cd1076",
    "deep_pink4": "#8b0a50",
    "deep_sky_blue1": "#00bfff",  # deepskyblue
    "deep_sky_blue2": "#00b2ee",
    "deep_sky_blue3": "#009acd",
    "deep_sky_blue4": "#00688b",
    "dodger_blue1": "#1e90ff",  # dodgerblue
    "dodger_blue2": "#1c86ee",
    "dodger_blue3": "#1874cd",
    "gold1": "#ffd700",  # gold
    "gold3": "#cdad00",
    "green1": "#00ff00",  # lime
    "green3": "#00cd00",
    "green4": "#008b00",
    "honeydew2": "#e0eee0",
    "hot_pink2": "#ee6aa7",
    "hot_pink3": "#cd6090",
    "indian_red1": "#ff6a6a",
    "khaki1": "#fff68f",
    "khaki3": "#cdc673",
    "light_cyan1": "#e0ffff",  # lightcyan
    "light_cyan3": "#c1cdcd",
    "light_goldenrod1": "#ffec8b",
    "light_goldenrod2": "#eedc82",
    "light_goldenrod3": "#cdbe70",
    "light_pink1": "#ffaeb9",
    "light_pink3": "#cd8c95",
    "light_pink4": "#8b5f65",
    "light_salmon1": "#ffa07a",  # lightsalmon
    "light_salmon3": "#cd8162",
    "light_sky_blue1": "#b0e2ff",
    "light_sky_blue3": "#96cdcd",
    "light_steel_blue1": "#cae1ff",
    "light_steel_blue3": "#a2b5cd",
    "light_yellow3": "#cdcdb4",
    "magenta1": "#ff00ff",  # magenta
    "magenta2": "#ee00ee",
    "magenta3": "#cd00cd",
    "medium_orchid1": "#e066ff",
    "medium_orchid3": "#b452cd",
    "medium_purple1": "#ab82ff",
    "medium_purple2": "#9f79ee",
    "medium_purple3": "#8968cd",
    "medium_purple4": "#5d478b",
    "misty_rose1": "#ffe4e1",  # mistyrose
    "misty_rose3": "#cdc5bf",
    "navajo_white1": "#ffdead",  # navajowhite
    "navajo_white3": "#cdc0b0",
    "orange1": "#ffa500",  # orange
    "orange3": "#cd8500",
    "orange4": "#8b5a00",
    "orange_red1": "#ff4500",  # orangered
    "orchid1": "#ff83fa",
    "orchid2": "#ee7ae9",
    "pale_green1": "#9aff9a",
    "pale_green3": "#7ccd7c",
    "pale_turquoise1": "#bbffff",
    "pale_turquoise4": "#668b8b",
    "pale_violet_red1": "#ff82ab",
    "pink1": "#ffb5c5",
    "pink3": "#cd919e",
    "plum1": "#ffbbff",
    "plum2": "#eeaeee",
    "plum3": "#cd96cd",
    "plum4": "#8b668b",
    "purple": "#800080",  # purple (CSS4 is darker than Rich purple)
    "purple3": "#7d26cd",
    "purple4": "#551a8b",
    "red1": "#ff0000",  # red
    "red3": "#cd0000",
    "royal_blue1": "#4876ff",
    "salmon1": "#ff8c69",
    "sea_green1": "#54ff9f",
    "sea_green2": "#4eee94",
    "sea_green3": "#43cd80",
    "sky_blue1": "#87ceff",
    "sky_blue2": "#7ec0ee",
    "sky_blue3": "#6ca6cd",
    "slate_blue1": "#836fff",
    "slate_blue3": "#6959cd",
    "spring_green1": "#00ff7f",  # springgreen
    "spring_green2": "#00ee76",
    "spring_green3": "#00cd66",
    "spring_green4": "#008b45",
    "steel_blue1": "#63b8ff",
    "steel_blue3": "#4f94cd",
    "tan": "#d2b48c",  # tan
    "thistle1": "#ffe1ff",
    "thistle3": "#cdb5cd",
    "turquoise2": "#00e5ee",
    "turquoise4": "#00868b",
    "violet": "#ee82ee",  # violet
    "wheat1": "#ffe7ba",
    "wheat4": "#8b7e66",
    "yellow1": "#ffff00",  # yellow
    "yellow2": "#eeee00",
    "yellow3": "#cdcd00",
    "yellow4": "#8b8b00",
    # Gray/Grey scales (0-100)
    "gray0": "#000000",
    "grey0": "#000000",
    "gray3": "#080808",
    "grey3": "#080808",
    "gray7": "#121212",
    "grey7": "#121212",
    "gray11": "#1c1c1c",
    "grey11": "#1c1c1c",
    "gray15": "#262626",
    "grey15": "#262626",
    "gray19": "#303030",
    "grey19": "#303030",
    "gray23": "#3a3a3a",
    "grey23": "#3a3a3a",
    "gray27": "#444444",
    "grey27": "#444444",
    "gray30": "#4e4e4e",
    "grey30": "#4e4e4e",
    "gray35": "#595959",
    "grey35": "#595959",
    "gray37": "#5e5e5e",
    "grey37": "#5e5e5e",
    "gray39": "#626262",
    "grey39": "#626262",
    "gray42": "#6c6c6c",
    "grey42": "#6c6c6c",
    "gray46": "#767676",
    "grey46": "#767676",
    "gray50": "#808080",
    "grey50": "#808080",
    "gray53": "#878787",
    "grey53": "#878787",
    "gray54": "#8a8a8a",
    "grey54": "#8a8a8a",
    "gray58": "#949494",
    "grey58": "#949494",
    "gray62": "#9e9e9e",
    "grey62": "#9e9e9e",
    "gray63": "#a8a8a8",
    "grey63": "#a8a8a8",
    "gray66": "#adadad",
    "grey66": "#adadad",
    "gray69": "#b2b2b2",
    "grey69": "#b2b2b2",
    "gray70": "#b7b7b7",
    "grey70": "#b7b7b7",
    "gray74": "#c1c1c1",
    "grey74": "#c1c1c1",
    "gray78": "#cbcbcb",
    "grey78": "#cbcbcb",
    "gray82": "#d5d5d5",
    "grey82": "#d5d5d5",
    "gray84": "#dfdfdf",
    "grey84": "#dfdfdf",
    "gray85": "#e4e4e4",
    "grey85": "#e4e4e4",
    "gray89": "#eeeeee",
    "grey89": "#eeeeee",
    "gray93": "#f8f8f8",
    "grey93": "#f8f8f8",
    "gray100": "#ffffff",
    "grey100": "#ffffff",
}


def get_rich_color_names() -> list[str]:
    """Get list of all supported Rich color names.

    Returns:
        Sorted list of Rich color names (250+ colors including numbered variants)

    Example:
        >>> names = get_rich_color_names()
        >>> "bright_green" in names
        True
        >>> "dodger_blue1" in names
        True
    """
    return sorted(RICH_TO_CSS4_MAPPING.keys())


def get_all_color_names() -> list[str]:
    """Get combined list of all supported color names (CSS4 + Rich).

    Returns:
        Sorted list of all color names (~400 total)

    Example:
        >>> names = get_all_color_names()
        >>> len(names) > 350
        True
        >>> "lime" in names  # CSS4
        True
        >>> "bright_green" in names  # Rich
        True
    """
    all_names = set(CSS4_COLORS.keys()) | set(RICH_TO_CSS4_MAPPING.keys())
    return sorted(all_names)
