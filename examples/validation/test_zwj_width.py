#!/usr/bin/env python3
"""
Test script to diagnose ZWJ emoji width in different terminals.

Run this directly in your terminal (Kitty, VS Code, etc.) to see
how ZWJ emojis are measured vs rendered.
"""

import os
import sys

# Add src to path for local testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from styledconsole.utils.terminal import detect_terminal_capabilities, is_modern_terminal
from styledconsole.utils.text import (
    VARIATION_SELECTOR_16,
    _grapheme_width_modern,
    _grapheme_width_standard,
    _is_modern_terminal_mode,
    split_graphemes,
    visual_width,
)


def main():
    print("=" * 60)
    print("ZWJ WIDTH DIAGNOSTIC")
    print("=" * 60)

    # Terminal detection
    profile = detect_terminal_capabilities()
    print(f"\nTerminal: {profile.terminal_name or 'unknown'}")
    print(f"TERM: {os.environ.get('TERM', 'not set')}")
    print(f"TERM_PROGRAM: {os.environ.get('TERM_PROGRAM', 'not set')}")
    print(f"Modern terminal: {is_modern_terminal()}")
    print(f"Using modern mode: {_is_modern_terminal_mode()}")

    # Test emojis
    test_cases = [
        ("Simple emoji", "🚀"),
        ("VS16 emoji", "⚠️"),
        ("ZWJ Developer", "👨‍💻"),
        ("ZWJ Artist", "👩‍🎨"),
        ("ZWJ Family", "👨‍👩‍👧"),
        ("Rainbow Flag", "🏳️‍🌈"),
        ("Skin tone", "👋🏻"),
    ]

    print("\n" + "-" * 60)
    print("EMOJI WIDTH ANALYSIS")
    print("-" * 60)
    print(f"{'Emoji':<20} {'Visual':<8} {'Modern':<8} {'Standard':<8} {'Graphemes'}")
    print("-" * 60)

    for name, emoji in test_cases:
        graphemes = split_graphemes(emoji)
        v_width = visual_width(emoji)
        m_width = sum(_grapheme_width_modern(g) for g in graphemes)
        s_width = sum(_grapheme_width_standard(g) for g in graphemes)

        has_vs16 = VARIATION_SELECTOR_16 in emoji
        has_zwj = "\u200d" in emoji

        markers = []
        if has_vs16:
            markers.append("VS16")
        if has_zwj:
            markers.append("ZWJ")
        marker_str = f"[{','.join(markers)}]" if markers else ""

        # Format output line
        line = f"{emoji} {name:<16} {v_width:<8} {m_width:<8} {s_width:<8}"
        print(f"{line} {len(graphemes)} {marker_str}")

    # Debug: Show grapheme breakdown for ZWJ
    print("\n" + "-" * 60)
    print("GRAPHEME BREAKDOWN FOR ZWJ STRING")
    print("-" * 60)
    test_str = "👨‍💻 Developer"
    print(f"String: {test_str!r}")
    print(f"Length (chars): {len(test_str)}")
    graphemes = split_graphemes(test_str)
    print(f"Graphemes: {len(graphemes)}")
    for i, g in enumerate(graphemes):
        g_width = _grapheme_width_modern(g)
        codepoints = [f"U+{ord(c):04X}" for c in g]
        print(f"  [{i}] {g!r} -> width={g_width}, codepoints: {codepoints}")

    # Visual alignment test
    print("\n" + "-" * 60)
    print("VISUAL ALIGNMENT TEST")
    print("-" * 60)
    print("If the | characters line up, width calculation is correct:")
    print()

    test_lines = [
        ("Reference (10 chars)", "XXXXXXXXXX"),
        ("Simple emoji + text", "🚀 Rocket!"),
        ("VS16 emoji + text ", "⚠️ Warning"),
        ("ZWJ emoji + text  ", "👨‍💻 Developer"),
    ]

    for name, content in test_lines:
        width = visual_width(content)
        # Pad to width 20 using our calculation
        padding = " " * (20 - width)
        print(f"|{content}{padding}| {name} (width={width})")

    print("\n" + "=" * 60)
    print("If lines don't align, the mismatch shows width calculation error")
    print("=" * 60)


if __name__ == "__main__":
    main()
