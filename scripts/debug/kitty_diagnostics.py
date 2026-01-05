#!/usr/bin/env python3
"""Diagnostic script for Kitty terminal visual issues.

Run this script in Kitty terminal to:
1. Confirm terminal is detected as "modern"
2. Compare visual_width() vs Rich's cell_len() for test strings
3. Test frames with/without soft_wrap to isolate issues
4. Output results to help diagnose rendering problems

Usage:
    cd StyledConsole
    uv run python scripts/debug/kitty_diagnostics.py
"""

from __future__ import annotations

import io
import os
import sys

# Add src to path for development
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from rich.cells import cell_len
from rich.console import Console as RichConsole
from rich.text import Text as RichText

from styledconsole import Console
from styledconsole.utils.terminal import (
    detect_terminal_capabilities,
    is_modern_terminal,
)
from styledconsole.utils.text import visual_width


def print_header(title: str) -> None:
    """Print a section header."""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_terminal_detection() -> bool:
    """Test if terminal is detected as modern."""
    print_header("Terminal Detection")

    env_vars = {
        "TERM": os.environ.get("TERM", "<not set>"),
        "COLORTERM": os.environ.get("COLORTERM", "<not set>"),
        "TERM_PROGRAM": os.environ.get("TERM_PROGRAM", "<not set>"),
        "KITTY_WINDOW_ID": os.environ.get("KITTY_WINDOW_ID", "<not set>"),
        "WEZTERM_PANE": os.environ.get("WEZTERM_PANE", "<not set>"),
        "ITERM_SESSION_ID": os.environ.get("ITERM_SESSION_ID", "<not set>"),
    }

    print("\nEnvironment Variables:")
    for key, value in env_vars.items():
        print(f"  {key}: {value}")

    profile = detect_terminal_capabilities()
    print("\nDetected Terminal Profile:")
    print(f"  terminal_name: {profile.terminal_name}")
    print(f"  modern_emoji: {profile.modern_emoji}")
    print(f"  emoji_safe: {profile.emoji_safe}")
    print(f"  color_depth: {profile.color_depth}")
    print(f"  ansi_support: {profile.ansi_support}")

    is_modern = is_modern_terminal()
    print(f"\nis_modern_terminal(): {is_modern}")

    if is_modern:
        print("  [OK] Terminal correctly detected as modern")
    else:
        print("  [WARNING] Terminal NOT detected as modern!")
        print("  This may cause width calculation issues.")

    return is_modern


def test_width_calculations() -> None:
    """Compare visual_width() vs Rich's cell_len()."""
    print_header("Width Calculations")

    test_strings = [
        ("ASCII only", "Hello World"),
        ("Basic emoji", "Hello World"),
        ("VS16 emoji (warning)", "Warning"),
        ("VS16 emoji (heart)", "Love"),
        ("ZWJ sequence", "Developer"),
        ("Multiple emojis", " Status:  Ready"),
        ("Box drawing", "Content"),
        ("Mixed content", " Launch  Ready"),
    ]

    print("\nComparing visual_width() vs Rich cell_len():")
    print("-" * 60)
    print(f"{'Description':<25} {'visual_width':<12} {'cell_len':<12} {'Match'}")
    print("-" * 60)

    mismatches = []
    for desc, text in test_strings:
        vw = visual_width(text)
        cl = cell_len(text)
        match = ""

        if vw != cl:
            mismatches.append((desc, text, vw, cl))

        print(f"{desc:<25} {vw:<12} {cl:<12} {match}")

    print("-" * 60)

    if mismatches:
        print(f"\n[WARNING] Found {len(mismatches)} width mismatches!")
        print("These may cause frame alignment issues when Rich re-wraps content.")
    else:
        print("\n[OK] All width calculations match!")


def test_soft_wrap_behavior() -> None:
    """Test how soft_wrap affects frame output."""
    print_header("soft_wrap Behavior Test")

    test_content = " Status:  Ready |  Tasks Complete"

    # Create a narrow console to force potential wrapping
    width = 50

    print(f"\nTest content: {test_content!r}")
    print(f"Content visual_width: {visual_width(test_content)}")
    print(f"Content cell_len: {cell_len(test_content)}")
    print(f"Console width: {width}")

    # Test with soft_wrap=True
    buffer_true = io.StringIO()
    console_true = RichConsole(file=buffer_true, width=width, force_terminal=True)
    text_true = RichText(test_content)
    console_true.print(text_true, soft_wrap=True)
    output_true = buffer_true.getvalue()

    # Test with soft_wrap=False
    buffer_false = io.StringIO()
    console_false = RichConsole(file=buffer_false, width=width, force_terminal=True)
    text_false = RichText(test_content)
    console_false.print(text_false, soft_wrap=False)
    output_false = buffer_false.getvalue()

    lines_true = output_true.strip().split("\n")
    lines_false = output_false.strip().split("\n")

    print(f"\nWith soft_wrap=True: {len(lines_true)} line(s)")
    for i, line in enumerate(lines_true):
        print(f"  Line {i + 1}: {line!r}")

    print(f"\nWith soft_wrap=False: {len(lines_false)} line(s)")
    for i, line in enumerate(lines_false):
        print(f"  Line {i + 1}: {line!r}")

    if len(lines_true) != len(lines_false):
        print("\n[ISSUE FOUND] soft_wrap=True causes extra lines!")
        print("This is likely the root cause of Kitty visual issues.")
    else:
        print("\n[OK] Both modes produce same number of lines")


def test_frame_rendering() -> None:
    """Test actual frame rendering."""
    print_header("Frame Rendering Test")

    console = Console(record=True)

    print("\nRendering test frames...")

    # Simple frame
    console.frame("Simple content", title="Test 1: Simple")

    # Emoji frame
    console.frame(
        [" Task complete", " Low memory", " Connection failed"],
        title="Test 2: Emojis",
    )

    # Get rendered output
    output = console.export_text()
    lines = output.strip().split("\n")

    print(f"\nTotal lines rendered: {len(lines)}")
    print("\nFrame output:")
    for i, line in enumerate(lines):
        vw = visual_width(line)
        print(f"  {i + 1:2}: (w={vw:2}) {line}")

    # Check for visual width consistency
    frame_lines = [line for line in lines if line.strip()]
    widths = [visual_width(line) for line in frame_lines]
    unique_widths = set(widths)

    if len(unique_widths) <= 2:  # Allow for some variation due to frame groups
        print("\n[OK] Frame line widths are consistent")
    else:
        print(f"\n[WARNING] Inconsistent frame widths: {unique_widths}")


def main() -> None:
    """Run all diagnostic tests."""
    print("\n" + "=" * 60)
    print("  StyledConsole Kitty Terminal Diagnostics")
    print("=" * 60)

    is_modern = test_terminal_detection()
    test_width_calculations()
    test_soft_wrap_behavior()
    test_frame_rendering()

    print_header("Summary")

    if is_modern:
        print("\nTerminal correctly detected as modern.")
        print("If visual issues persist, the problem is likely:")
        print("  1. soft_wrap=True causing Rich to re-wrap content")
        print("  2. Width mismatches between visual_width() and cell_len()")
    else:
        print("\nTerminal NOT detected as modern!")
        print("Try setting: export STYLEDCONSOLE_MODERN_TERMINAL=1")

    print("\n" + "=" * 60)
    print("  Diagnostics complete")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
