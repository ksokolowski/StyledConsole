#!/usr/bin/env python3
"""
Precise ZWJ width test for Kitty terminal.

This test uses exact character counts to diagnose the width issue.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from styledconsole.utils.text import split_graphemes, visual_width


def main():
    print("=" * 50)
    print("PRECISE ZWJ WIDTH TEST")
    print("=" * 50)

    # Test strings with EXACT same visual content length after emoji
    # All should end at the same column if width calculation is correct

    test_cases = [
        # (label, string, expected_visual_width)
        ("10 X chars     ", "XXXXXXXXXX", 10),
        ("Rocket + 7     ", "🚀 Rocket!", 10),  # 2 + 1 + 7 = 10
        ("Warning + 7    ", "⚠️ Warning", 10),  # 2 + 1 + 7 = 10
        ("ZWJ Dev + 9    ", "👨‍💻 Developer", 12),  # 2 + 1 + 9 = 12
        ("ZWJ + 7 chars  ", "👨‍💻 Hello!!", 10),  # 2 + 1 + 7 = 10
    ]

    print("\nGRAPHEME ANALYSIS:")
    print("-" * 50)
    for label, s, expected in test_cases:
        graphemes = split_graphemes(s)
        calc_width = visual_width(s)
        print(f"{label}: {s!r}")
        print(f"  Graphemes: {len(graphemes)}, Calculated: {calc_width}, Expected: {expected}")
        for i, g in enumerate(graphemes):
            cps = " ".join(f"U+{ord(c):04X}" for c in g)
            print(f"    [{i}] {g!r} = {cps}")
        print()

    print("=" * 50)
    print("VISUAL ALIGNMENT TEST")
    print("=" * 50)
    print("All lines should have | at the same column:")
    print()

    # Create lines that SHOULD all be width 10
    width_10_tests = [
        ("10 X", "XXXXXXXXXX"),
        ("Rocket", "🚀 Rocket!"),
        ("Warning", "⚠️ Warning"),
        ("ZWJ+7", "👨‍💻 Hello!!"),
    ]

    for label, content in width_10_tests:
        w = visual_width(content)
        pad = " " * (15 - w)  # Pad to 15
        print(f"|{content}{pad}| {label} (w={w})")

    print()
    print("Now testing the problematic string (width 12):")
    content = "👨‍💻 Developer"
    w = visual_width(content)
    pad = " " * (15 - w)
    print(f"|{content}{pad}| ZWJ+Dev (w={w})")

    print()
    print("=" * 50)
    print("RULER (each digit = 1 cell):")
    print("1234567890123456789012345")
    print("=" * 50)


if __name__ == "__main__":
    main()
