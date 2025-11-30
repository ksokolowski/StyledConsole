#!/usr/bin/env python3
"""
Emoji Comparison Demo
====================

Demonstrates emoji rendering in both terminal and HTML export,
showing the differences in VS16 emoji rendering.
"""

from styledconsole import Console
from styledconsole.core.export_manager import ExportManager


def main():
    console = Console(record=True, width=80)

    # Title
    console.banner(
        "EMOJI RENDERING COMPARISON", start_color="purple", end_color="pink", border="double"
    )

    # VS16 Emojis (width-1 in terminal, width-2 in browser)
    console.text("\n📌 VS16 Emojis (Terminal: width-1, Browser: width-2)", color="yellow")
    vs16_emojis = ["⚠️  Warning Sign", "ℹ️  Information", "⚙️  Gear", "✉️  Envelope", "☎️  Telephone"]
    console.frame(vs16_emojis, title="VS16 Emojis", border="rounded", border_color="yellow")

    # Consistent Width-2 Emojis
    console.text("\n📌 Consistent Width-2 Emojis (Same in both)", color="green")
    width2_emojis = [
        "🟢 Green Circle",
        "🟡 Yellow Circle",
        "🔴 Red Circle",
        "🚀 Rocket",
        "💻 Computer",
        "🎨 Palette",
    ]
    console.frame(width2_emojis, title="Width-2 Emojis", border="rounded", border_color="green")

    # Skin Tone Emojis
    console.text("\n📌 Skin Tone Modifiers", color="cyan")
    skin_tones = [
        "👋 Wave (default)",
        "👋🏻 Wave (light)",
        "👋🏼 Wave (medium-light)",
        "👋🏽 Wave (medium)",
        "👋🏾 Wave (medium-dark)",
        "👋🏿 Wave (dark)",
    ]
    console.frame(skin_tones, title="Skin Tones", border="rounded", border_color="cyan")

    # ZWJ Sequences
    console.text("\n📌 ZWJ Sequences", color="magenta")
    zwj_emojis = [
        "👨‍💻 Developer",
        "👩‍🎨 Artist",
        "🧑‍🔬 Scientist",
        "👨‍🚀 Astronaut",
        "🏳️‍🌈 Rainbow Flag",
    ]
    console.frame(zwj_emojis, title="ZWJ Emojis", border="rounded", border_color="magenta")

    # Regional Indicators (Flags)
    console.text("\n📌 Regional Indicator Flags", color="blue")
    flags = ["🇺🇸 United States", "🇬🇧 United Kingdom", "🇨🇦 Canada", "🇯🇵 Japan", "🇩🇪 Germany"]
    console.frame(flags, title="Flags", border="rounded", border_color="blue")

    # Summary
    console.text("\n" + "=" * 80, color="white")
    console.text("📊 COMPARISON NOTES:", color="yellow")
    console.text("• VS16 emojis: May show alignment differences between terminal and HTML")
    console.text("• Width-2 emojis: Render consistently across both environments")
    console.text("• For HTML export: Use colored circles (🟢🟡🔴) for best alignment")
    console.text("=" * 80 + "\n", color="white")

    # Export to HTML
    print("Exporting to emoji_comparison.html...")
    manager = ExportManager(console._rich_console)
    html = manager.export_html(
        page_title="Emoji Rendering Comparison",
        theme_css="""
        body {
            font-family: 'Fira Code', 'Cascadia Code', monospace;
            background-color: #1e1e1e;
            margin: 2rem;
            color: #d4d4d4;
        }
        pre {
            background-color: #252526;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        """,
    )

    with open("emoji_comparison.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("✅ Export complete!")
    print("📄 Open emoji_comparison.html in your browser to compare rendering")
    print("👁️  Compare the VS16 emojis section - notice the alignment differences")


if __name__ == "__main__":
    main()
