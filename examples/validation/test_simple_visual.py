#!/usr/bin/env python3
"""
Simple visual test - print emoji followed by fixed column marker.

The RULER at bottom shows column positions.
If alignment is correct, the ':' should appear at the same column.
"""


def main():
    print("=" * 40)
    print("SIMPLE VISUAL WIDTH TEST")
    print("=" * 40)
    print()

    # Each line: content + ':' at column 15
    # We manually add spaces to reach column 15

    lines = [
        # (content, calculated_width, spaces_to_add)
        ("XXXXXXXXXX", 10, 5),  # 10 + 5 = 15
        ("🚀Rocket!!", 10, 5),  # 2 + 8 = 10, then +5 = 15
        ("⚠️Warning!!", 10, 5),  # VS16 + 8 = 10 (assuming modern), then +5 = 15
        ("👨‍💻Hello!!!!", 10, 5),  # ZWJ + 8 = 10, then +5 = 15
        ("👨‍💻Developer", 11, 4),  # ZWJ + 9 = 11, then +4 = 15
    ]

    print("All ':' should align at column 15:")
    print("-" * 40)

    for content, width, spaces in lines:
        padding = " " * spaces
        print(f"{content}{padding}: width={width}")

    print("-" * 40)
    print("123456789012345678901234567890")
    print("         1111111111222222222233")
    print()

    print("=" * 40)
    print("NOW TESTING WITH OUR CALCULATED WIDTHS")
    print("=" * 40)

    import sys

    sys.path.insert(0, "src")
    from styledconsole.utils.text import visual_width

    test_strings = [
        "XXXXXXXXXX",
        "🚀Rocket!!",
        "⚠️Warning!!",
        "👨‍💻Hello!!!!",
        "👨‍💻Developer",
    ]

    target = 15
    print(f"\nPadding to column {target}:")
    print("-" * 40)

    for s in test_strings:
        w = visual_width(s)
        padding = " " * (target - w)
        print(f"{s}{padding}: w={w}")

    print("-" * 40)
    print("123456789012345678901234567890")


if __name__ == "__main__":
    main()
