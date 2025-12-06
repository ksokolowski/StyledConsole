#!/usr/bin/env python3
"""Emoji Package Integration Demo.

This example demonstrates the enhanced emoji capabilities provided by the
optional `emoji` package integration. It showcases:

1. Comprehensive emoji validation (4,000+ vs 200 emojis)
2. ZWJ sequence detection for terminal safety
3. Emoji version filtering for compatibility
4. Shortcode conversion (:rocket: → 🚀)
5. Emoji extraction and analysis

Run: uv run python examples/demos/emoji_integration_demo.py
"""

from styledconsole import EMOJI, Console

# Import emoji_support utilities
from styledconsole.utils.emoji_support import (
    EMOJI_PACKAGE_AVAILABLE,
    analyze_emoji_safety,
    demojize,
    emoji_list,
    emojize,
    filter_by_version,
    get_all_emojis,
    get_emoji_info,
    get_emoji_version,
    is_valid_emoji,
    is_zwj_sequence,
)

console = Console()


def demo_package_status():
    """Show emoji package availability status."""
    console.frame(
        f"emoji package available: {EMOJI_PACKAGE_AVAILABLE}\n"
        f"Total emojis available: {len(get_all_emojis()):,}",
        title=f"{EMOJI.PACKAGE} Emoji Package Status",
        border="rounded",
        border_color="cyan",
    )


def demo_emoji_validation():
    """Demonstrate emoji validation capabilities."""
    test_cases = [
        ("🚀", "Rocket (standard)"),
        ("✅", "Check mark"),
        ("👨‍💻", "Technologist (ZWJ)"),
        ("👨‍👩‍👧", "Family (ZWJ)"),
        ("A", "Letter A"),
        ("☰", "Trigram (symbol)"),
    ]

    lines = []
    for char, description in test_cases:
        is_valid = is_valid_emoji(char)
        status = f"{EMOJI.CHECK} Valid" if is_valid else f"{EMOJI.CROSS} Invalid"
        lines.append(f"  {char}  {description}: {status}")

    console.frame(
        "\n".join(lines),
        title=f"{EMOJI.MAGNIFYING_GLASS} Emoji Validation",
        border="rounded",
        border_color="green",
    )


def demo_zwj_detection():
    """Demonstrate ZWJ sequence detection."""
    test_cases = [
        ("🚀", "Single emoji"),
        ("👨‍💻", "Man Technologist"),
        ("👩‍🔬", "Woman Scientist"),
        ("👨‍👩‍👧‍👦", "Family"),
        ("🏳️‍🌈", "Rainbow Flag"),
        ("Hello 🌍", "Text with emoji"),
    ]

    lines = []
    for text, description in test_cases:
        has_zwj = is_zwj_sequence(text)
        if has_zwj:
            status = f"{EMOJI.WARNING} ZWJ (may not render correctly)"
        else:
            status = f"{EMOJI.CHECK} Terminal safe"
        lines.append(f"  {text}  {description}")
        lines.append(f"      {status}")

    console.frame(
        "\n".join(lines),
        title=f"{EMOJI.LINK} ZWJ Sequence Detection",
        border="rounded",
        border_color="yellow",
    )


def demo_emoji_info():
    """Demonstrate getting detailed emoji information."""
    emojis = ["🚀", "🎉", "⚡", "👨‍💻"]

    lines = []
    for char in emojis:
        info = get_emoji_info(char)
        version = get_emoji_version(char)
        version_str = f"v{version}" if version else "unknown"

        lines.append(f"  {char} {info.name}")
        lines.append(f"      Version: {version_str}")
        lines.append(f"      ZWJ: {info.is_zwj}  Safe: {info.terminal_safe}")

    console.frame(
        "\n".join(lines),
        title=f"{EMOJI.INFO} Emoji Information",
        border="rounded",
        border_color="blue",
    )


def demo_safety_analysis():
    """Demonstrate emoji safety analysis for terminals."""
    test_texts = [
        "Hello 🚀 World 🌍",
        "Family: 👨‍👩‍👧",
        "Status: ✅ Done",
        "Mixed: 🎉 and 👨‍💻",
    ]

    for text in test_texts:
        result = analyze_emoji_safety(text)
        safe_status = (
            f"{EMOJI.CHECK} All safe" if result["all_safe"] else f"{EMOJI.WARNING} Contains unsafe"
        )

        console.text(f'"{text}"', bold=True)
        console.text(
            f"  Emojis: {result['emoji_count']} | "
            f"Safe: {len(result['safe_emojis'])} | "
            f"ZWJ: {len(result['zwj_sequences'])} | "
            f"{safe_status}"
        )
        console.text("")


def demo_shortcode_conversion():
    """Demonstrate shortcode conversion."""
    examples = [
        ":rocket: Launch!",
        ":check_mark: Done",
        ":fire: Hot :fire:",
        ":star: Rating: 5 stars",
    ]

    lines = []
    for shortcode_text in examples:
        converted = emojize(shortcode_text)
        lines.append(f"  {shortcode_text}")
        lines.append(f"  → {converted}")
        lines.append("")

    console.frame(
        "\n".join(lines).rstrip(),
        title=f"{EMOJI.ARROW_RIGHT} Shortcode Conversion",
        border="rounded",
        border_color="magenta",
    )


def demo_reverse_conversion():
    """Demonstrate emoji to shortcode conversion."""
    text = "Hello 🚀 World 🌍 Done ✅"
    converted = demojize(text)

    console.frame(
        f"Original:  {text}\nShortcode: {converted}",
        title=f"{EMOJI.ARROW_LEFT} Reverse Conversion",
        border="rounded",
        border_color="cyan",
    )


def demo_version_filtering():
    """Demonstrate emoji version filtering for compatibility."""
    text = "Modern: 🦖 🦕 Classic: 🚀 ⭐"

    lines = [f"Original: {text}"]

    # Filter for older terminals
    filtered_5 = filter_by_version(text, max_version=5.0, replacement="[?]")
    lines.append(f"Max v5.0: {filtered_5}")

    filtered_1 = filter_by_version(text, max_version=1.0, replacement="[?]")
    lines.append(f"Max v1.0: {filtered_1}")

    console.frame(
        "\n".join(lines),
        title=f"{EMOJI.CLOCK} Version Filtering",
        border="rounded",
        border_color="orange",
    )


def demo_emoji_extraction():
    """Demonstrate finding emojis in text."""
    text = "Hello 👋 World 🌍 Done ✅"

    emojis = emoji_list(text)

    lines = [f'Text: "{text}"', "", "Found emojis:"]
    for e in emojis:
        lines.append(f"  {e['emoji']} at position {e['match_start']}")

    console.frame(
        "\n".join(lines),
        title=f"{EMOJI.MAGNIFYING_GLASS} Emoji Extraction",
        border="rounded",
        border_color="green",
    )


def main():
    """Run all demos."""
    console.banner("EMOJI INTEGRATION", font="slant", start_color="cyan", end_color="magenta")
    console.text("")

    demo_package_status()
    console.text("")

    demo_emoji_validation()
    console.text("")

    demo_zwj_detection()
    console.text("")

    demo_emoji_info()
    console.text("")

    console.frame(
        "",
        title=f"{EMOJI.SHIELD} Safety Analysis",
        border="rounded",
        border_color="red",
    )
    demo_safety_analysis()

    demo_shortcode_conversion()
    console.text("")

    demo_reverse_conversion()
    console.text("")

    demo_version_filtering()
    console.text("")

    demo_emoji_extraction()
    console.text("")

    console.frame(
        f"The emoji package integration provides:\n"
        f"  {EMOJI.CHECK} 4,000+ emoji validation (vs 200 in SAFE_EMOJIS)\n"
        f"  {EMOJI.CHECK} Proper ZWJ sequence detection\n"
        f"  {EMOJI.CHECK} Emoji version filtering for compatibility\n"
        f"  {EMOJI.CHECK} Shortcode conversion (:rocket: → 🚀)\n"
        f"  {EMOJI.CHECK} Graceful fallback when package unavailable",
        title=f"{EMOJI.SPARKLES} Summary",
        border="double",
        border_color="gold",
    )


if __name__ == "__main__":
    main()
