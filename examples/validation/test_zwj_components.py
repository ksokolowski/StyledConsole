#!/usr/bin/env python3
"""
Test ZWJ emoji width based on number of component emojis.

Hypothesis: Kitty renders ZWJ sequences at width 2 regardless of components,
but wcwidth/our calculation may vary.
"""

import sys

sys.path.insert(0, "src")

from styledconsole.utils.text import visual_width


def count_emoji_components(s: str) -> int:
    """Count emoji codepoints (excluding ZWJ and VS16)."""
    count = 0
    for c in s:
        cp = ord(c)
        # Skip ZWJ (U+200D) and VS16 (U+FE0F)
        if cp == 0x200D or cp == 0xFE0F:
            continue
        # Count if it's an emoji (rough check: > 0x1F000 or specific ranges)
        if cp > 0x1F000 or (0x2600 <= cp <= 0x27BF):
            count += 1
    return count


def main():
    print("=" * 60)
    print("ZWJ COMPONENT COUNT TEST")
    print("=" * 60)
    print()

    # ZWJ emojis with different numbers of components
    zwj_emojis = [
        # 2-component ZWJ
        ("👨‍💻", "Man + Laptop (2 parts)"),
        ("👩‍🎨", "Woman + Palette (2 parts)"),
        ("👨‍🔬", "Man + Microscope (2 parts)"),
        # 3-component ZWJ
        ("👨‍👩‍👧", "Family M+W+G (3 parts)"),
        ("👨‍👩‍👦", "Family M+W+B (3 parts)"),
        # 4-component ZWJ
        ("👨‍👩‍👧‍👦", "Family M+W+G+B (4 parts)"),
        # Flag with ZWJ
        ("🏳️‍🌈", "Rainbow flag (2 parts + VS16)"),
        ("🏴‍☠️", "Pirate flag (2 parts + VS16)"),
    ]

    print("ZWJ Emoji Analysis:")
    print("-" * 60)
    print(f"{'Emoji':<8} {'Parts':<6} {'Width':<6} Description")
    print("-" * 60)

    for emoji, desc in zwj_emojis:
        parts = count_emoji_components(emoji)
        width = visual_width(emoji)
        print(f"{emoji:<8} {parts:<6} {width:<6} {desc}")

    print()
    print("=" * 60)
    print("VISUAL ALIGNMENT TEST")
    print("=" * 60)
    print("All ':' should align if width calculation is correct:")
    print()

    target = 12

    # Reference
    ref = "X" * 10
    w = visual_width(ref)
    pad = " " * (target - w)
    print(f"{ref}{pad}: w={w} (reference)")

    print()
    for emoji, _desc in zwj_emojis:
        # Emoji + padding to fixed width
        w = visual_width(emoji)
        pad = " " * (target - w)
        parts = count_emoji_components(emoji)
        print(f"{emoji}{pad}: w={w}, parts={parts}")

    print()
    print("-" * 60)
    print("12345678901234567890")
    print("          1111111111")


if __name__ == "__main__":
    main()
