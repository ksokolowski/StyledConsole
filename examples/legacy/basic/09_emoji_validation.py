#!/usr/bin/env python3
"""
Safe Emoji Showcase Example (v0.3.0 - Rich Native)

Demonstrates the comprehensive safe emoji list with visual validation.
Shows how emojis work correctly in frames and styled output.

This example showcases:
- All safe emoji categories
- Emoji validation framework
- Practical usage in styled frames
- Emoji width calculation and alignment

v0.3.0: Simplified and updated to use Console.frame() (Rich Panel internally).
"""

from styledconsole import (
    SAFE_EMOJIS,
    Console,
    get_safe_emojis,
    validate_emoji,
)
from styledconsole.utils.text import visual_width

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

    content = "\n".join(
        [
            f"Emoji: {emoji}",
            f"Status: {status}",
            f"Name: {result['name'] or 'Unknown'}",
            f"Category: {result['category'] or 'N/A'}",
            f"Info: {result['recommendation']}",
        ]
    )

    console.frame(
        content,
        title=description,
        border="minimal",
        width=60,
        padding=1,
    )
    print()

# ============================================================================
# Part 4: Dashboard Example - CI/CD Pipeline
# ============================================================================
console.rule("Dashboard Example: CI/CD Pipeline", color="lime")
print()

console.frame(
    "\n".join(
        [
            "🚀 Deployment Pipeline Status",
            "",
            "✅ Source Build        [████████░░] 80%",
            "✅ Unit Tests          [██████████] 100%",
            "✅ Integration Tests   [██████████] 100%",
            "🟡 Staging Deploy      [██████░░░░] 60%",
            "❌ Production Deploy   [░░░░░░░░░░] 0%",
            "",
            "Next Action: Review staging deployment logs",
        ]
    ),
    title="💻 CI/CD Dashboard",
    border="double",
    width=70,
)
print()

# ============================================================================
# Part 5: Width Calculation Examples
# ============================================================================
console.rule("Emoji Width Calculation", color="cyan")
print()

console.text("Emojis are correctly handled with visual_width():", color="cyan", bold=True)
print()

test_strings = [
    "Hello",
    "🚀 Rocket",
    "✅ Success ✅",
    "🎨 Art & Design 🎨",
]

width_info = []
for s in test_strings:
    char_len = len(s)
    visual_len = visual_width(s)
    width_info.append(f"'{s}' → len()={char_len}, visual_width()={visual_len}")

console.frame(
    "\n".join(width_info),
    title="📏 Width Calculations",
    border="rounded",
    width=70,
)
print()

# ============================================================================
# Part 6: Usage Recommendations
# ============================================================================
console.rule("Best Practices", color="magenta")
print()

console.frame(
    "\n".join(
        [
            "✅ DO: Use emojis from SAFE_EMOJIS dictionary",
            "✅ DO: Validate emojis with validate_emoji()",
            "✅ DO: Use format_emoji_with_spacing() for titles",
            "✅ DO: Use visual_width() for width calculations",
            "",
            "❌ DON'T: Use ZWJ sequences (👨‍💻)",
            "❌ DON'T: Use skin tone modifiers (👍🏽)",
            "❌ DON'T: Use untested emojis in production",
            "❌ DON'T: Assume emoji width = character count",
        ]
    ),
    title="💡 Emoji Best Practices",
    border="double",
    width=70,
    padding=1,
)
print()

# ============================================================================
# Summary
# ============================================================================
console.frame(
    f"All {len(SAFE_EMOJIS)} safe emojis are tested and verified!\n"
    "Use get_safe_emojis(category) to filter by category.\n"
    "See EMOJI_GUIDELINES.md for complete documentation.",
    title="✨ Summary",
    border="double",
    border_color="green",
    align="center",
    width=70,
)
print()
