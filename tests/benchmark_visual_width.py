"""Benchmark script for visual_width performance."""

import statistics
import time

from styledconsole.utils.text import visual_width


def benchmark():
    # Test data including mixed ASCII, Emoji, and ANSI
    items = [
        "Hello World",
        "Hello 🌍 World",
        "\x1b[31mRed\x1b[0m",
        "Rocket 🚀 Blastoff",
        "Family 👨‍👩‍👧‍👦 Time",
        "Flag 🏳️‍🌈 Pride",
        "A" * 100,
        "Complex 👨‍💻 Sequence",
    ] * 1000

    print(f"Benchmarking visual_width with {len(items)} calls...")

    times = []
    for _ in range(5):
        start = time.perf_counter()
        for item in items:
            visual_width(item)
        end = time.perf_counter()
        times.append(end - start)

    avg_time = statistics.mean(times)
    print(f"Average time: {avg_time:.4f} seconds")
    print(f"Calls per second: {len(items) / avg_time:.2f}")


if __name__ == "__main__":
    benchmark()
