# CSS4 Color Names Reference

**Project:** StyledConsole
**Feature:** Human-readable color names
**Standard:** CSS4 / W3C Color Module Level 4
**Total Colors:** 148

---

## Overview

StyledConsole supports all **148 CSS4 named colors**, allowing users to specify colors using memorable names instead of hex codes or RGB tuples.

### Supported Formats

```python
# All of these work!
console.frame("Text", color="coral")            # CSS4 named color ✅
console.frame("Text", color="#FF7F50")          # Hex (6 digits) ✅
console.frame("Text", color="#f75")             # Hex shorthand (3 digits) ✅
console.frame("Text", color="rgb(255,127,80)")  # RGB function ✅
console.frame("Text", color=(255, 127, 80))     # RGB tuple ✅
```

### Why CSS4 Colors?

1. **Memorable:** `dodgerblue` is easier to remember than `#1E90FF`
2. **Standard:** Same names as CSS, matplotlib, web browsers
3. **Discoverable:** Use `get_color_names()` to see all options
4. **Compatible:** Works with gradients and all color features

---

## Color Categories

### Status Colors (Testing/CI)

Perfect for test reports and status displays:

```python
# Success indicators
'green'        # #008000 - Standard success
'lime'         # #00FF00 - Bright success
'lightgreen'   # #90EE90 - Soft success
'limegreen'    # #32CD32 - Medium success

# Error indicators
'red'          # #FF0000 - Standard error
'crimson'      # #DC143C - Deep red error
'indianred'    # #CD5C5C - Softer error
'darkred'      # #8B0000 - Dark error

# Warning indicators
'yellow'       # #FFFF00 - Bright warning
'gold'         # #FFD700 - Rich warning
'orange'       # #FFA500 - Standard warning
'darkorange'   # #FF8C00 - Deep warning

# Info indicators
'blue'         # #0000FF - Standard info
'dodgerblue'   # #1E90FF - Bright info
'royalblue'    # #4169E1 - Rich info
'cornflowerblue' # #6495ED - Softer info

# Skip/disabled
'gray'         # #808080 - Neutral
'silver'       # #C0C0C0 - Light neutral
'darkgray'     # #A9A9A9 - Medium gray
```

**Example Usage:**

```python
from styledconsole import Console

console = Console()
console.frame("✅ All tests passed", color="limegreen", title="Success")
console.frame("❌ 3 tests failed", color="crimson", title="Error")
console.frame("⚠️ Rate limit exceeded", color="gold", title="Warning")
console.frame("ℹ️ Deployment started", color="dodgerblue", title="Info")
```

---

### Blues (50+ shades)

```python
# Light blues
'aliceblue'      # #F0F8FF - Very light
'lightblue'      # #ADD8E6 - Light
'lightskyblue'   # #87CEFA - Light sky
'skyblue'        # #87CEEB - Sky

# Medium blues
'deepskyblue'    # #00BFFF - Deep sky
'dodgerblue'     # #1E90FF - Vibrant (recommended)
'cornflowerblue' # #6495ED - Cornflower
'royalblue'      # #4169E1 - Royal
'steelblue'      # #4682B4 - Steel

# Dark blues
'blue'           # #0000FF - Pure blue
'mediumblue'     # #0000CD - Medium
'darkblue'       # #00008B - Dark
'navy'           # #000080 - Navy (darkest)
'midnightblue'   # #191970 - Midnight
```

---

### Greens (40+ shades)

```python
# Light greens
'lightgreen'     # #90EE90 - Light
'palegreen'      # #98FB98 - Pale
'lightseagreen'  # #20B2AA - Light sea (teal-ish)
'mediumseagreen' # #3CB371 - Medium sea

# Medium greens
'limegreen'      # #32CD32 - Lime (vibrant)
'lime'           # #00FF00 - Pure lime (brightest)
'springgreen'    # #00FF7F - Spring
'mediumspringgreen' # #00FA9A - Medium spring

# Dark greens
'green'          # #008000 - Standard
'forestgreen'    # #228B22 - Forest
'seagreen'       # #2E8B57 - Sea
'darkgreen'      # #006400 - Dark
'darkolivegreen' # #556B2F - Olive
```

---

### Reds & Pinks (30+ shades)

```python
# Light reds/pinks
'pink'           # #FFC0CB - Light pink
'lightpink'      # #FFB6C1 - Light pink
'lightcoral'     # #F08080 - Light coral
'salmon'         # #FA8072 - Salmon
'lightsalmon'    # #FFA07A - Light salmon

# Vibrant reds
'red'            # #FF0000 - Pure red
'crimson'        # #DC143C - Crimson
'tomato'         # #FF6347 - Tomato
'orangered'      # #FF4500 - Orange-red
'coral'          # #FF7F50 - Coral (recommended)

# Deep reds
'firebrick'      # #B22222 - Firebrick
'darkred'        # #8B0000 - Dark
'indianred'      # #CD5C5C - Indian red
'maroon'         # #800000 - Maroon
```

---

### Yellows & Oranges (20+ shades)

```python
# Yellows
'yellow'         # #FFFF00 - Pure yellow
'gold'           # #FFD700 - Gold (recommended)
'lightyellow'    # #FFFFE0 - Light
'lemonchiffon'   # #FFFACD - Lemon chiffon
'lightgoldenrodyellow' # #FAFAD2 - Light goldenrod

# Oranges
'orange'         # #FFA500 - Standard orange
'darkorange'     # #FF8C00 - Dark orange
'coral'          # #FF7F50 - Coral (reddish)
'tomato'         # #FF6347 - Tomato (reddish)
'sandybrown'     # #F4A460 - Sandy brown
'peru'           # #CD853F - Peru
```

---

### Purples & Magentas (25+ shades)

```python
# Light purples
'lavender'       # #E6E6FA - Lavender
'thistle'        # #D8BFD8 - Thistle
'plum'           # #DDA0DD - Plum
'violet'         # #EE82EE - Violet
'orchid'         # #DA70D6 - Orchid

# Medium purples
'mediumorchid'   # #BA55D3 - Medium orchid
'mediumpurple'   # #9370DB - Medium purple
'blueviolet'     # #8A2BE2 - Blue-violet
'darkorchid'     # #9932CC - Dark orchid
'darkviolet'     # #9400D3 - Dark violet

# Deep purples
'purple'         # #800080 - Standard purple
'indigo'         # #4B0082 - Indigo
'darkmagenta'    # #8B008B - Dark magenta

# Magentas
'magenta'        # #FF00FF - Pure magenta
'fuchsia'        # #FF00FF - Fuchsia (same as magenta)
'hotpink'        # #FF69B4 - Hot pink
'deeppink'       # #FF1493 - Deep pink
```

---

### Greens/Cyans/Teals (30+ shades)

```python
# Cyans
'cyan'           # #00FFFF - Pure cyan
'aqua'           # #00FFFF - Aqua (same as cyan)
'lightcyan'      # #E0FFFF - Light cyan
'paleturquoise'  # #AFEEEE - Pale turquoise
'turquoise'      # #40E0D0 - Turquoise
'mediumturquoise' # #48D1CC - Medium turquoise
'darkturquoise'  # #00CED1 - Dark turquoise

# Teals/sea greens
'teal'           # #008080 - Standard teal
'lightseagreen'  # #20B2AA - Light sea green
'cadetblue'      # #5F9EA0 - Cadet blue
'darkcyan'       # #008B8B - Dark cyan
'aquamarine'     # #7FFFD4 - Aquamarine
'mediumaquamarine' # #66CDAA - Medium aquamarine
```

---

### Browns & Naturals (20+ shades)

```python
# Light browns
'wheat'          # #F5DEB3 - Wheat
'burlywood'      # #DEB887 - Burlywood
'tan'            # #D2B48C - Tan
'rosybrown'      # #BC8F8F - Rosy brown
'sandybrown'     # #F4A460 - Sandy brown

# Medium browns
'peru'           # #CD853F - Peru
'chocolate'      # #D2691E - Chocolate
'saddlebrown'    # #8B4513 - Saddle brown
'sienna'         # #A0522D - Sienna

# Dark browns
'brown'          # #A52A2A - Standard brown
'maroon'         # #800000 - Maroon
```

---

### Grays (20+ shades)

**Note:** Both `gray` and `grey` spellings are supported!

```python
# Light grays
'white'          # #FFFFFF - Pure white
'whitesmoke'     # #F5F5F5 - White smoke
'gainsboro'      # #DCDCDC - Gainsboro
'lightgray'      # #D3D3D3 - Light gray
'lightgrey'      # #D3D3D3 - Light grey (same)

# Medium grays
'silver'         # #C0C0C0 - Silver
'darkgray'       # #A9A9A9 - Dark gray
'darkgrey'       # #A9A9A9 - Dark grey (same)
'gray'           # #808080 - Standard gray
'grey'           # #808080 - Standard grey (same)

# Dark grays
'dimgray'        # #696969 - Dim gray
'dimgrey'        # #696969 - Dim grey (same)
'slategray'      # #708090 - Slate gray
'slategrey'      # #708090 - Slate grey (same)
'darkslategray'  # #2F4F4F - Dark slate gray
'darkslategrey'  # #2F4F4F - Dark slate grey (same)
'black'          # #000000 - Pure black
```

---

## Usage Examples

### Simple Frames

```python
from styledconsole import Console

console = Console()

# Status frames with semantic colors
console.frame("Build successful", color="limegreen", title="✅ Success")
console.frame("Tests failed", color="crimson", title="❌ Error")
console.frame("Deprecation warning", color="gold", title="⚠️ Warning")
console.frame("Deployment info", color="dodgerblue", title="ℹ️ Info")
```

### Gradients

```python
# Ocean theme
console.banner("DEPLOY", gradient=("lightblue", "navy"))

# Sunset theme
console.banner("SUNSET", gradient=("gold", "orangered"))

# Forest theme
console.banner("NATURE", gradient=("lightgreen", "darkgreen"))

# Fire theme
console.banner("ALERT", gradient=("yellow", "crimson"))
```

### Dashboard with Color Coding

```python
from styledconsole.presets import dashboard_large

dashboard_large(
    stats={
        "passed": {"value": 182, "color": "limegreen"},
        "failed": {"value": 3, "color": "crimson"},
        "skipped": {"value": 7, "color": "gold"},
    },
    sections=[
        ("Recent Failures", ["test_login", "test_api"], "tomato"),
        ("Performance", ["<50ms average"], "dodgerblue"),
    ],
    banner="CI Results",
    banner_color="royalblue"
)
```

---

## Color Discovery

### List All Colors

```python
from styledconsole.utils.color import get_color_names

# Get all 148 color names
colors = get_color_names()
print(f"Total colors: {len(colors)}")

# Show first 10
for name in colors[:10]:
    print(name)
```

### Search by Pattern

```python
colors = get_color_names()

# Find all blues
blues = [c for c in colors if 'blue' in c]
print(blues)
# ['aliceblue', 'blue', 'blueviolet', 'cadetblue', 'cornflowerblue', ...]

# Find all dark colors
dark_colors = [c for c in colors if c.startswith('dark')]
print(dark_colors)
# ['darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', ...]

# Find all light colors
light_colors = [c for c in colors if c.startswith('light')]
print(light_colors)
# ['lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', ...]
```

---

## Implementation Details

### Color Parsing Order

When you specify a color, StyledConsole tries formats in this order:

1. **CSS4 named color** (case-insensitive)
2. **Hex format** (`#RRGGBB` or `#RGB`)
3. **RGB function** (`rgb(r, g, b)`)
4. **RGB tuple** (`(r, g, b)`)

```python
# All of these produce the same color:
parse_color("coral")           # Named (preferred) ✅
parse_color("CORAL")           # Case-insensitive ✅
parse_color("#ff7f50")         # Hex ✅
parse_color("#FF7F50")         # Hex (uppercase) ✅
parse_color("rgb(255,127,80)") # RGB function ✅
parse_color((255, 127, 80))    # RGB tuple ✅
```

### Color Data Source

The CSS4 color dictionary is defined in `styledconsole/utils/color_data.py`:

```python
# Matches matplotlib.colors.CSS4_COLORS
# Source: W3C CSS Color Module Level 4
CSS4_COLORS = {
    'aliceblue': '#f0f8ff',
    'antiquewhite': '#faebd7',
    # ... 148 total colors
}
```

---

## Compatibility

### With Matplotlib

StyledConsole uses the **same color names as matplotlib**, so if you're familiar with matplotlib plotting, the colors work identically:

```python
# In matplotlib
plt.plot(x, y, color='dodgerblue')

# In StyledConsole
console.frame("Plot data", color='dodgerblue')
```

### With Web/CSS

These are **standard CSS4 colors**, so they match web development:

```css
/* In CSS */
.alert { color: coral; }
```

```python
# In StyledConsole
console.frame("Alert", color='coral')
```

---

## Reference: Complete Color List

All 148 CSS4 colors (alphabetical):

```
aliceblue, antiquewhite, aqua, aquamarine, azure, beige, bisque, black,
blanchedalmond, blue, blueviolet, brown, burlywood, cadetblue, chartreuse,
chocolate, coral, cornflowerblue, cornsilk, crimson, cyan, darkblue, darkcyan,
darkgoldenrod, darkgray, darkgrey, darkgreen, darkkhaki, darkmagenta,
darkolivegreen, darkorange, darkorchid, darkred, darksalmon, darkseagreen,
darkslateblue, darkslategray, darkslategrey, darkturquoise, darkviolet,
deeppink, deepskyblue, dimgray, dimgrey, dodgerblue, firebrick, floralwhite,
forestgreen, fuchsia, gainsboro, ghostwhite, gold, goldenrod, gray, grey,
green, greenyellow, honeydew, hotpink, indianred, indigo, ivory, khaki,
lavender, lavenderblush, lawngreen, lemonchiffon, lightblue, lightcoral,
lightcyan, lightgoldenrodyellow, lightgray, lightgrey, lightgreen, lightpink,
lightsalmon, lightseagreen, lightskyblue, lightslategray, lightslategrey,
lightsteelblue, lightyellow, lime, limegreen, linen, magenta, maroon,
mediumaquamarine, mediumblue, mediumorchid, mediumpurple, mediumseagreen,
mediumslateblue, mediumspringgreen, mediumturquoise, mediumvioletred,
midnightblue, mintcream, mistyrose, moccasin, navajowhite, navy, oldlace,
olive, olivedrab, orange, orangered, orchid, palegoldenrod, palegreen,
paleturquoise, palevioletred, papayawhip, peachpuff, peru, pink, plum,
powderblue, purple, rebeccapurple, red, rosybrown, royalblue, saddlebrown,
salmon, sandybrown, seagreen, seashell, sienna, silver, skyblue, slateblue,
slategray, slategrey, snow, springgreen, steelblue, tan, teal, thistle,
tomato, turquoise, violet, wheat, white, whitesmoke, yellow, yellowgreen
```

---

## Testing

```python
def test_css4_color_support():
    """Verify all 148 CSS4 colors work."""
    from styledconsole.utils.color import parse_color, CSS4_COLORS

    for name, hex_value in CSS4_COLORS.items():
        # Named color should parse correctly
        rgb = parse_color(name)

        # Should match hex equivalent
        expected = parse_color(hex_value)
        assert rgb == expected, f"Color {name} mismatch"

    # Both gray spellings
    assert parse_color("gray") == parse_color("grey")
    assert parse_color("darkgray") == parse_color("darkgrey")

    print("✅ All 148 CSS4 colors validated!")
```

---

## External References

- **W3C CSS Color Module:** https://www.w3.org/TR/css-color-4/
- **Matplotlib Named Colors:** https://matplotlib.org/stable/gallery/color/named_colors.html
- **MDN CSS Colors:** https://developer.mozilla.org/en-US/docs/Web/CSS/named-color

---

**Status:** ✅ Full CSS4 color support in StyledConsole v0.1
**Maintained by:** StyledConsole project
**Last updated:** October 15, 2025
