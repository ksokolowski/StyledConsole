"""Test rainbow_cycling_frame vs rainbow_frame

Demonstrates the difference between:
- rainbow_frame: Smooth gradient across all lines
- rainbow_cycling_frame: Each line cycles through discrete rainbow colors
"""

from styledconsole import Console, rainbow_cycling_frame, rainbow_frame

console = Console()

print()
console.text("🌈 COMPARISON: Rainbow Effects", color="cyan", bold=True)
print("=" * 80)
print()

# Test content - 8 lines to show cycling (7 colors + 1 repeat)
content = [
    "Line 1 - Should be RED",
    "Line 2 - Should be ORANGE",
    "Line 3 - Should be YELLOW",
    "Line 4 - Should be GREEN (lime)",
    "Line 5 - Should be BLUE",
    "Line 6 - Should be INDIGO",
    "Line 7 - Should be VIOLET",
    "Line 8 - Should cycle back to RED",
]

# Standard rainbow_frame: Smooth gradient
console.text("1️⃣  rainbow_frame (smooth gradient):", color="yellow")
print("-" * 80)
lines = rainbow_frame(
    content,
    direction="vertical",
    mode="content",  # Only content colored
    border="rounded",
    title="Smooth Gradient",
)
for line in lines:
    print(line)
print()

# New rainbow_cycling_frame: Discrete colors per line
console.text("2️⃣  rainbow_cycling_frame (discrete colors per line):", color="yellow")
print("-" * 80)
lines = rainbow_cycling_frame(
    content,
    border_gradient_start="gold",
    border_gradient_end="purple",
    border="heavy",
    title="Cycling Rainbow",
)
for line in lines:
    print(line)
print()

# Show both modes
console.text("3️⃣  rainbow_frame with both content and borders:", color="yellow")
print("-" * 80)
lines = rainbow_frame(
    ["Line 1", "Line 2", "Line 3", "Line 4"],
    direction="vertical",
    mode="both",  # Both content and borders
    border="double",
    title="Gradient Both",
)
for line in lines:
    print(line)
print()

console.text("✅ Comparison complete!", color="lime", bold=True)
print()
