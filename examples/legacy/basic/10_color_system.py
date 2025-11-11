#!/usr/bin/env python3
"""Color System Demonstration

Showcases the unified CSS4 + Rich color system with 396 human-readable color names.
"""

from styledconsole import (
    Console,
    get_all_color_names,
    get_color_names,
    get_rich_color_names,
)

console = Console()

# Header
console.frame(
    [
        "StyledConsole v0.3.0 supports 396 human-readable color names:",
        "",
        "• 148 CSS4 standard colors (lime, dodgerblue, hotpink)",
        "• 250+ Rich extended colors (bright_green, dodger_blue1, hot_pink2)",
        "",
        "Use CSS4 names everywhere: Console.frame(), effects, banners!",
    ],
    title="🎨 Unified Color System",
    border="double",
    border_color="bright_cyan",
    title_color="white",
)

print()

# CSS4 Examples
console.frame(
    [
        "lime        🟢 (0, 255, 0)",
        "limegreen   🟢 (50, 205, 50)",
        "orangered   🔴 (255, 69, 0)",
        "dodgerblue  🔵 (30, 144, 255)",
        "hotpink     🌸 (255, 105, 180)",
        "gold        🌟 (255, 215, 0)",
    ],
    title="CSS4 Color Names (148 total)",
    border="rounded",
    border_color="gold",
    content_color="yellow",
)

print()

# Rich Examples
console.frame(
    [
        "bright_green    🟢 (0, 255, 0) - Same as 'lime'",
        "bright_red      🔴 (255, 85, 85)",
        "bright_cyan     💠 (0, 255, 255)",
        "dodger_blue1    🔵 (30, 144, 255)",
        "hot_pink        🌸 (255, 105, 180)",
        "gold1           🌟 (255, 215, 0)",
    ],
    title="Rich Color Names (250+ total)",
    border="rounded",
    border_color="bright_magenta",
    content_color="bright_white",
)

print()

# Gradient Demo
console.frame(
    [
        "Gradient from lime to dodgerblue",
        "All colors work in gradients too!",
        "CSS4 + Rich = Maximum flexibility",
    ],
    title="🌈 Gradient Support",
    border="heavy",
    start_color="lime",
    end_color="dodgerblue",
    border_color="bright_cyan",
)

print()

# Summary
css4_count = len(get_color_names())
rich_count = len(get_rich_color_names())
total_count = len(get_all_color_names())

console.frame(
    [
        f"✅ CSS4 colors: {css4_count}",
        f"✅ Rich colors: {rich_count}",
        f"✅ Total unique: {total_count}",
        "",
        "All colors work everywhere:",
        "• Console.frame()",
        "• Effects (gradients, rainbow)",
        "• Banner rendering",
    ],
    title="📊 Color Summary",
    border="double",
    border_color="bright_green",
    title_color="bright_yellow",
)

print()
print("💡 Tip: Use human-readable names instead of hex codes for cleaner code!")
print()
