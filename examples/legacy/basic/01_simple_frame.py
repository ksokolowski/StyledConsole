#!/usr/bin/env python3
"""
Simple Frame Example

Demonstrates basic frame rendering with different border styles.
Uses the high-level Console API for easy frame creation.

This is the recommended way to use StyledConsole!
"""

from styledconsole import Console

print("=" * 60)
print("SIMPLE FRAME EXAMPLES")
print("=" * 60)
print()

# Initialize Console - the main entry point for StyledConsole
console = Console()

# Example 1: SOLID border
print("1. SOLID Border:")
console.frame(
    "Hello, StyledConsole!",
    title="Welcome",
    border="solid",
    width=50,
    align="center",
)
print()

# Example 2: ROUNDED border
print("2. ROUNDED Border:")
console.frame(
    "Smooth and modern",
    title="Rounded Corners",
    border="rounded",
    width=50,
    align="center",
)
print()

# Example 3: DOUBLE border
print("3. DOUBLE Border:")
console.frame(
    "For emphasis",
    title="Double Lines",
    border="double",
    width=50,
    align="center",
)
print()

# Example 4: ASCII border (universal compatibility)
print("4. ASCII Border (Universal):")
console.frame(
    "Works everywhere",
    title="ASCII Compatible",
    border="ascii",
    width=50,
    align="center",
)
print()

# Example 5: Multiple content lines
print("5. Multiple Lines:")
console.frame(
    ["First line", "Second line", "Third line"],
    title="Multi-line Content",
    border="solid",
    width=50,
)
print()

# Pro Tip: For advanced customization, explore the effects module:
#
# from styledconsole import gradient_frame, rainbow_frame
# gradient_frame("content", start_color="red", end_color="blue")
# rainbow_frame(["line 1", "line 2"], direction="vertical")
