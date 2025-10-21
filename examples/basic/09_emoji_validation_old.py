#!/usr/bin/env python3
"""
Safe Emoji Showcase Example (v0.3.0 - Rich Native)

Demonstrates the comprehensive safe emoji list with visual validation.
Shows how emojis work correctly in frames, gradients, and layouts.

This example showcases:
- All safe emoji categories
- Emoji validation framework
- Practical usage in styled frames
- Emoji width calculation and alignment

v0.3.0: Updated to use Console.frame() which uses Rich Panel internally.
"""

from styledconsole import (
    SAFE_EMOJIS,
    Console,
    get_safe_emojis,
    gradient_frame,
    rainbow_frame,
    validate_emoji,
)
from styledconsole.utils.text import format_emoji_with_spacing, visual_width

print("=" * 70)
print("🌈 STYLEDCONSOLE SAFE EMOJI SHOWCASE")
print("=" * 70)
print()

# Initialize console
console = Console()

# ============================================================================
# Part 1: Safe Emoji Categories Overview
# ============================================================================
console.banner("SAFE EMOJIS", font="slant")
print()

console.text(
    f"Total Safe Emojis: {len(SAFE_EMOJIS)} emoji characters tested and verified ✅",
    color="cyan",
    bold=True,
)
print()

# Show distribution by category
categories = {}
for info in SAFE_EMOJIS.values():
    cat = info["category"]
    categories[cat] = categories.get(cat, 0) + 1

console.frame(
    "\n".join(
        f"  {cat.upper():12} {categories[cat]:3} emojis" for cat in sorted(categories.keys())
    ),
    title="📊 Distribution by Category",
    border="rounded",
    width=50,
)
print()

# ============================================================================
# Part 2: Safe Emojis by Category
# ============================================================================
console.rule("Category Showcase", color="lime")
print()

categories_to_show = [
    ("status", "Status & Indicators"),
    ("tech", "Tech & Objects"),
    ("nature", "Nature & Weather"),
    ("activity", "Fun & Activities"),
    ("direction", "Arrows & Direction"),
]

for category, title in categories_to_show:
    emojis = get_safe_emojis(category)
    emoji_line = " ".join(emojis.keys())

    console.frame(
        emoji_line,
        title=f"✨ {title}",
        border="solid",
        width=65,
        align="center",
    )
    print()

# ============================================================================
# Part 3: Emoji Validation Example
# ============================================================================
console.rule("Emoji Validation System", color="yellow")
print()

console.text("Testing emoji validation framework:", color="yellow", bold=True)
print()

test_emojis = [
    ("✅", "Safe status emoji"),
    ("🚀", "Safe tech emoji"),
    ("👨‍💻", "ZWJ sequence (not supported)"),
    ("👍🏽", "Skin tone modifier (not supported)"),
]

for emoji, description in test_emojis:
    result = validate_emoji(emoji)
    status = "✅ SAFE" if result["safe"] else "❌ NOT SAFE"

    console.frame(
        [
            f"Emoji: {emoji}",
            f"Status: {status}",
            f"Name: {result['name'] or 'Unknown'}",
            f"Category: {result['category'] or 'N/A'}",
            f"Info: {result['recommendation']}",
        ],
        title=description,
        border="minimal",
        width=60,
        padding=1,
    )
    print()

# ============================================================================
# Part 4: Emoji in Gradient Frames
# ============================================================================
console.rule("Safe Emojis in Gradients", color="magenta")
print()

console.text("Emojis work beautifully with gradient effects:", color="magenta", bold=True)
print()

# Status gradient frame
status_content = [
    "✅ Build Passed",
    "✅ Tests Passed",
    "✅ Linting Passed",
    "✅ Deployment Ready",
]

lines = gradient_frame(
    status_content,
    start_color="red",
    end_color="green",
    target="content",
)

console.frame(
    lines,
    title="🌈 Status Report with Gradient",
    border="double",
    align="left",
)
print()

# ============================================================================
# Part 5: Emoji in Rainbow Frames
# ============================================================================
console.rule("Safe Emojis with Rainbow Effects", color="cyan")
print()

rainbow_content = [
    "🚀 Rocket Launch",
    "🎉 Party Time",
    "💡 Bright Idea",
    "🌟 Shining Star",
    "🎯 On Target",
]

lines = rainbow_frame(
    rainbow_content,
    direction="vertical",
    mode="both",
)

console.frame(
    lines,
    title="🌈 Rainbow Showcase",
    border="rounded",
)
print()

# ============================================================================
# Part 6: Complex Example - Status Dashboard
# ============================================================================
console.rule("Dashboard Example: CI/CD Pipeline", color="lime")
print()

console.frame(
    [
        "🚀 Deployment Pipeline Status",
        "",
        "✅ Source Build        [████████░░] 80%",
        "✅ Unit Tests          [██████████] 100%",
        "✅ Integration Tests   [██████████] 100%",
        "🟡 Staging Deploy      [██████░░░░] 60%",
        "❌ Production Deploy   [░░░░░░░░░░] 0%",
        "",
        "⏭️  Next: Manual approval required",
    ],
    title="📊 Pipeline Dashboard",
    border="heavy",
    width=55,
    padding=1,
    align="left",
)
print()

# ============================================================================
# Part 7: Technical Details - Visual Width Validation
# ============================================================================
console.rule("Technical: Visual Width Validation", color="blue")
print()

console.text(
    "Emoji alignment is guaranteed with visual_width() calculations:",
    color="blue",
    bold=True,
)
print()

test_cases = [
    ("✅ Task Complete", 13),
    ("🚀 Launch", 10),
    ("🌈 Rainbow", 11),
    ("🎉 Party 🎊", 14),
]

for text, expected_width in test_cases:
    actual_width = visual_width(text)
    match = "✅" if actual_width == expected_width else "⚠️"
    console.frame(
        [
            f"Text: {text}",
            f"Expected Width: {expected_width}",
            f"Actual Width: {actual_width}",
            f"Match: {match}",
        ],
        title="Width Calculation",
        border="minimal",
        width=45,
        padding=0,
    )
    print()

# ============================================================================
# Part 8: Summary and Guidelines
# ============================================================================
console.rule("Usage Guidelines", color="cyan")
print()

guidelines = [
    "✅ USE: Single-codepoint emojis from SAFE_EMOJIS",
    "✅ USE: Tier 1 basic pictographs (🚀 🎉 🌈 💡)",
    "✅ USE: Status symbols (✅ ❌ ⚠️ ℹ️)",
    "✅ USE: validate_emoji() to check before using",
    "",
    "❌ AVOID: ZWJ sequences (👨‍💻 🏳️‍🌈 etc.)",
    "❌ AVOID: Skin tone modifiers (👍🏽 👨🏻)",
    "❌ AVOID: Multi-codepoint combinations",
    "❌ AVOID: Obscure or new emoji variants",
]

console.frame(
    guidelines,
    title="📋 Best Practices",
    border="rounded",
    width=60,
    align="left",
    padding=1,
)
print()

# ============================================================================
# Part 9: API Reference
# ============================================================================
console.rule("API Reference", color="yellow")
print()

console.text("Three ways to use safe emojis:", color="yellow", bold=True)
print()

console.frame(
    [
        "1. Direct Usage:",
        "   emoji = '✅'",
        "   console.text(f'{emoji} Task Done')",
        "",
        "2. Get by Category:",
        "   tech_emojis = get_safe_emojis('tech')",
        "   for emoji in tech_emojis.keys():",
        "       print(emoji)",
        "",
        "3. Validate First:",
        "   result = validate_emoji('🚀')",
        "   if result['safe']:",
        "       use_emoji(result['emoji'])",
    ],
    title="💻 Usage Examples",
    border="ascii",
    width=60,
    align="left",
    padding=1,
)
print()

# ============================================================================
# Part 10: Advanced 2x2 Layouts with Complete Category Emojis
# ============================================================================
console.rule("Advanced Emoji Layouts - Complete 2x2 Grids", color="magenta")
print()

console.text("All emojis organized by category in 2x2 grid layouts:", color="magenta", bold=True)
print()

frame_renderer = FrameRenderer()

# Helper emoji descriptions
emoji_descriptions = {
    "✅": "Success",
    "❌": "Failed",
    "⚠️": "Warning",
    "ℹ️": "Info",
    "🔴": "Red",
    "🟡": "Yellow",
    "🟢": "Green",
    "🔵": "Blue",
    "💻": "Laptop",
    "🖥️": "Desktop",
    "⌨️": "Keyboard",
    "💾": "Floppy",
    "💿": "CD",
    "🔧": "Wrench",
    "🔨": "Hammer",
    "⚙️": "Gear",
    "🚀": "Rocket",
    "📦": "Package",
    "📁": "Folder",
    "📂": "Open Folder",
    "📝": "Notes",
    "📋": "Clipboard",
    "🌈": "Rainbow",
    "☀️": "Sun",
    "🌙": "Moon",
    "⭐": "Star",
    "✨": "Sparkles",
    "💫": "Dizzy",
    "🌟": "Bright Star",
    "❄️": "Ice",
    "☔": "Rain",
    "⚡": "Lightning",
    "🔥": "Fire",
    "🎉": "Party",
    "🎊": "Confetti",
    "🎁": "Gift",
    "🎯": "Target",
    "🎨": "Art",
    "🎭": "Theater",
    "🎮": "Game",
    "🏆": "Trophy",
    "➡️": "Right",
    "⬅️": "Left",
    "⬆️": "Up",
    "⬇️": "Down",
    "↗️": "Up-Right",
    "↘️": "Down-Right",
    "↙️": "Down-Left",
    "↖️": "Up-Left",
    "🔃": "Refresh",
    "🔄": "Reload",
}


# Function to create a frame with all emojis from a category
def create_complete_emoji_frame(category, title, border_color, max_width=45):
    """Create a frame with ALL emojis from a category with descriptions.

    Uses the automatic spacing adjustment API to handle all emoji spacing issues,
    including VS16 emojis and multi-grapheme sequences.
    """

    emojis = get_safe_emojis(category)
    content = []

    for emoji, info in emojis.items():
        desc = emoji_descriptions.get(emoji, f"{info['name'].replace('_', ' ')}")

        # Use the new automatic spacing adjustment API
        # This handles ALL emojis with spacing issues:
        # - VS16 emojis (⚠️, ℹ️, ➡️, 🖥️, 🖱️)
        # - Multi-grapheme emojis (⬅️, ⬆️, ⬇️, etc.)
        # Returns formatted string with correct spacing
        line = format_emoji_with_spacing(emoji, desc)

        content.append(line)

    # Join content and wrap if needed
    content_text = "\n".join(content)

    return frame_renderer.render(
        content_text,
        title=title,
        border="rounded",
        width=max_width,
        content_color=border_color,
        border_color=border_color,
    )


# Define category colors for visual distinction
# Using CSS4 color names from the library (148 named colors available)
category_colors = {
    "status": "lime",  # Bright green
    "tech": "cyan",  # Bright cyan
    "nature": "orange",  # Orange
    "activity": "fuchsia",  # Bright magenta
    "direction": "yellow",  # Bright yellow
    "progress": "turquoise",  # Cyan-green
    "data": "hotpink",  # Bright pink
    "food": "salmon",  # Light orange-red
}

# Create composer for layouts
composer = LayoutComposer()

# ============================================================================
# Grid 1: Status, Tech, Nature, Activity
# ============================================================================
print()
console.text("📍 Grid 1: Core Categories", color="yellow", bold=True)
print()

status_frame = create_complete_emoji_frame(
    "status", "✅ Status", category_colors["status"], max_width=40
)
tech_frame = create_complete_emoji_frame("tech", "💻 Tech", category_colors["tech"], max_width=40)
nature_frame = create_complete_emoji_frame(
    "nature", "🌈 Nature", category_colors["nature"], max_width=40
)
activity_frame = create_complete_emoji_frame(
    "activity", "🎉 Activity", category_colors["activity"], max_width=40
)

grid1_layout = composer.grid(
    [
        [status_frame, tech_frame],
        [nature_frame, activity_frame],
    ],
    column_spacing=2,
    row_spacing=1,
)

for line in grid1_layout:
    console.print(line, highlight=False, soft_wrap=False)

# ============================================================================
# Grid 2: Direction, Progress, Data, Food
# ============================================================================
print()
console.text("📍 Grid 2: Navigation & Other Categories", color="yellow", bold=True)
print()

direction_frame = create_complete_emoji_frame(
    "direction", "➡️ Direction", category_colors["direction"], max_width=40
)
progress_frame = create_complete_emoji_frame(
    "progress", "▶️ Progress", category_colors["progress"], max_width=40
)
data_frame = create_complete_emoji_frame("data", "📊 Data", category_colors["data"], max_width=40)
food_frame = create_complete_emoji_frame("food", "🍔 Food", category_colors["food"], max_width=40)

grid2_layout = composer.grid(
    [
        [direction_frame, progress_frame],
        [data_frame, food_frame],
    ],
    column_spacing=2,
    row_spacing=1,
)

for line in grid2_layout:
    console.print(line, highlight=False, soft_wrap=False)

# ============================================================================
# Grid 3: Hand, Other (Extended categories)
# ============================================================================
print()
console.text("📍 Grid 3: Gestures & Miscellaneous", color="yellow", bold=True)
print()

hand_frame = create_complete_emoji_frame("hand", "👆 Hand", "lightsalmon", max_width=40)
other_frame = create_complete_emoji_frame("other", "🎀 Other", "skyblue", max_width=40)

# Create a summary frame showing all categories
summary_content = []
all_categories = get_safe_emojis()
categories_dict = {}
for emoji, info in all_categories.items():
    cat = info["category"]
    if cat not in categories_dict:
        categories_dict[cat] = []
    categories_dict[cat].append(emoji)

for cat in sorted(categories_dict.keys()):
    emoji_line = " ".join(categories_dict[cat])
    summary_content.append(f"{cat.upper()}: {emoji_line}")

summary_frame = frame_renderer.render(
    "\n".join(summary_content),
    title="📋 All Categories Summary",
    border="double",
    width=40,
    content_color="silver",
    border_color="silver",
)

# For Grid 3, use a 2x1 layout (or 2x2 with summary taking up bottom-right area)
grid3_layout = composer.grid(
    [
        [hand_frame, other_frame],
        [summary_frame, summary_frame],  # Summary spans two columns
    ],
    column_spacing=2,
    row_spacing=1,
)

for line in grid3_layout:
    console.print(line, highlight=False, soft_wrap=False)

print()

# ============================================================================
# Part 11: Rainbow-Styled Complete Category Showcase
# ============================================================================
console.rule("Rainbow Gallery - All Categories", color="cyan")
print()

console.text("Complete emoji categories with rainbow gradient frames:", color="cyan", bold=True)
print()

rainbow_categories = [
    ("status", "✅ Status & Indicators"),
    ("tech", "💻 Tech & Objects"),
    ("nature", "🌈 Nature & Elements"),
    ("activity", "🎉 Activities & Fun"),
    ("direction", "➡️ Arrows & Direction"),
]

for category, title in rainbow_categories:
    emojis = get_safe_emojis(category)
    emoji_list = " ".join(emojis.keys())

    # Use rainbow_frame to get rendered lines with gradient effect
    rainbow_lines = rainbow_frame(
        emoji_list,
        title=title,
        border="rounded",
        width=70,
        align="center",
        direction="vertical",
        mode="both",
    )

    # Print each line
    for line in rainbow_lines:
        console.print(line, highlight=False, soft_wrap=False)
    print()

# ============================================================================
# Closing
# ============================================================================
print()
console.rule("", color="cyan")
console.banner("Thanks!", font="small")
print()
console.text(
    "For more emoji information, see: doc/guides/EMOJI_GUIDELINES.md",
    color="cyan",
    italic=True,
)
print()
