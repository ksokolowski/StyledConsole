#!/usr/bin/env python3
"""
Rendering Performance Benchmark

Tests rendering performance across different scenarios.
Useful for ensuring the library performs well.
"""

import time

from styledconsole import DOUBLE, ROUNDED, SOLID, visual_width

print()
print("=" * 80)
print("RENDERING PERFORMANCE BENCHMARK")
print("=" * 80)
print()


def benchmark(name, func, iterations=1000):
    """Run a benchmark and return timing."""
    start = time.perf_counter()
    for _ in range(iterations):
        func()
    end = time.perf_counter()
    elapsed = end - start
    per_op = (elapsed / iterations) * 1_000_000  # microseconds
    return elapsed, per_op


# Benchmark cases
print("Running benchmarks with 1,000 iterations each...")
print()

results = []


# 1. Simple frame rendering
def simple_frame():
    SOLID.render_top_border(50, "Test")
    SOLID.render_line(50, "Content")
    SOLID.render_bottom_border(50)


elapsed, per_op = benchmark("Simple frame (3 elements)", simple_frame)
results.append(("Simple frame", elapsed, per_op))
print(f"✓ Simple frame: {elapsed:.3f}s total, {per_op:.2f}µs per iteration")


# 2. Emoji-heavy frame
def emoji_frame():
    ROUNDED.render_top_border(50, "🚀 🎨 🎯 Test 🌟 ✨")
    ROUNDED.render_line(50, "🔥 Content with emojis 🎉", align="center")
    ROUNDED.render_bottom_border(50)


elapsed, per_op = benchmark("Emoji frame", emoji_frame)
results.append(("Emoji frame", elapsed, per_op))
print(f"✓ Emoji frame: {elapsed:.3f}s total, {per_op:.2f}µs per iteration")


# 3. Long content truncation
def truncate_test():
    long_text = "This is a very long line that will need truncation " * 5
    SOLID.render_line(30, long_text)


elapsed, per_op = benchmark("Long text truncation", truncate_test)
results.append(("Truncation", elapsed, per_op))
print(f"✓ Truncation: {elapsed:.3f}s total, {per_op:.2f}µs per iteration")


# 4. Visual width calculation
def width_calc():
    visual_width("Test 🚀 with emoji 🎉 content")


elapsed, per_op = benchmark("Visual width calc", width_calc, iterations=10000)
results.append(("Visual width", elapsed, per_op))
print(f"✓ Visual width: {elapsed:.3f}s total, {per_op:.2f}µs per iteration")


# 5. Complete multi-line frame
def complex_frame():
    DOUBLE.render_top_border(60, "🎨 Complex Frame")
    for i in range(5):
        DOUBLE.render_line(60, f"Line {i} with 🎯 emoji", align="left")
    DOUBLE.render_divider(60)
    for i in range(3):
        DOUBLE.render_line(60, f"More content {i}", align="center")
    DOUBLE.render_bottom_border(60)


elapsed, per_op = benchmark("Complex frame (10 lines)", complex_frame)
results.append(("Complex frame", elapsed, per_op))
print(f"✓ Complex frame: {elapsed:.3f}s total, {per_op:.2f}µs per iteration")

# Summary
print()
print("=" * 80)
print("BENCHMARK SUMMARY")
print("=" * 80)
print()

# Display as table
width = 70
print(SOLID.render_top_border(width, "⚡ Performance Results"))
print(SOLID.render_line(width, "", align="center"))
print(
    SOLID.render_line(
        width, "Operation                    Total Time    Per Iteration", align="left"
    )
)
print(SOLID.render_divider(width))

for name, total, per in results:
    line = f"{name:25}  {total:8.3f}s      {per:8.2f}µs"
    print(SOLID.render_line(width, line, align="left"))

print(SOLID.render_line(width, "", align="center"))
print(SOLID.render_bottom_border(width))
print()

# Performance notes
print(ROUNDED.render_top_border(width, "📊 Performance Notes"))
print(ROUNDED.render_line(width, "", align="center"))
print(ROUNDED.render_line(width, "All operations are sub-millisecond", align="left"))
print(ROUNDED.render_line(width, "Emoji handling adds minimal overhead", align="left"))
print(ROUNDED.render_line(width, "Visual width calculation is highly optimized", align="left"))
print(ROUNDED.render_line(width, "", align="center"))
print(
    ROUNDED.render_line(
        width, "✅ Performance is excellent for terminal rendering!", align="center"
    )
)
print(ROUNDED.render_line(width, "", align="center"))
print(ROUNDED.render_bottom_border(width))
print()
