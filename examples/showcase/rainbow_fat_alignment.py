#!/usr/bin/env python
"""Rainbow Fat Alignment Showcase.

Advanced example demonstrating:
- Large, colorful banners with rainbow gradients
- Emoji integration throughout layout
- All three alignment types: left, center, right
- Complex multi-section layouts
- Border gradients and color combinations

This example showcases the library's ability to create vibrant,
visually rich terminal UIs with precise alignment control.
"""

from styledconsole import Console
from styledconsole.core.banner import BannerRenderer
from styledconsole.core.frame import FrameRenderer
from styledconsole.core.layout import LayoutComposer
from styledconsole.utils.text import format_emoji_with_spacing


def create_rainbow_banner(text: str, font: str = "slant", max_width: int = 100) -> list[str]:
    """Create a rainbow gradient banner.

    Args:
        text: Text to display in banner
        font: Pyfiglet font to use
        max_width: Maximum banner width (actual may be less)

    Returns:
        List of lines representing the banner
    """
    renderer = BannerRenderer()
    return renderer.render(
        text,
        font=font,
        start_color="red",
        end_color="magenta",
        width=max_width,
    )


def create_section_frame(
    title: str,
    content: str,
    emoji: str = "✨",
    border_style: str = "solid",
    border_color: str = "cyan",
    content_color: str = "white",
    width: int = 50,
) -> list[str]:
    """Create a decorated section frame.

    Args:
        title: Frame title
        content: Frame content
        emoji: Emoji to use in title
        border_style: Border style name
        border_color: Border color (CSS4 name or hex)
        content_color: Content color
        width: Frame width

    Returns:
        List of lines representing the frame
    """
    # Format emoji with spacing
    formatted_emoji = format_emoji_with_spacing(emoji, f" {title}")
    full_title = formatted_emoji.strip()

    renderer = FrameRenderer()
    return renderer.render(
        content,
        border=border_style,
        title=full_title,
        border_color=border_color,
        content_color=content_color,
        width=width,
        padding=2,
    )


def create_alignment_showcase() -> None:
    """Main showcase function with all alignments."""
    console = Console()
    composer = LayoutComposer()
    renderer = FrameRenderer()

    # Get terminal width for proper alignment - use Rich console's detected width
    terminal_width = console._rich_console.width

    # Use a safe frame width that accounts for ANSI codes and terminal wrapping
    # Keep frames at a reasonable width (60 chars) to avoid any wrapping issues
    max_frame_width = min(60, terminal_width // 2)  # Max 60 or half terminal width

    # ==============================================================================
    # SECTION 1: Rainbow Banner Header
    # ==============================================================================
    console.newline()
    banner = create_rainbow_banner("ALIGNMENT", font="banner", max_width=max_frame_width)
    for line in banner:
        console.print(line, highlight=False, soft_wrap=False)

    console.newline()

    # ==============================================================================
    # SECTION 2: Three Alignment Demonstration
    # ==============================================================================
    console.frame(
        "Demonstrating Left, Center, and Right alignment with vibrant colors",
        title="🎨 Alignment Showcase",
        border="double",
        border_color="magenta",
        content_color="lightyellow",
        padding=2,
    )

    console.newline(2)

    # ==============================================================================
    # LEFT ALIGNMENT SECTION
    # ==============================================================================
    left_banner = BannerRenderer().render(
        "LEFT",
        font="small",
        start_color="red",
        end_color="orange",
        width=max_frame_width,
    )

    left_frame_1 = create_section_frame(
        "Fast & Quick",
        "⚡ Lightning speed\n🚀 Rapid deployment\n📈 Quick response",
        emoji="⚡",
        border_style="rounded",
        border_color="orange",
        content_color="lightyellow",
        width=max_frame_width,
    )

    left_frame_2 = create_section_frame(
        "Powerful",
        "✨ Strong performance\n💎 Hot features\n⚙️ Robust engine",
        emoji="✨",
        border_style="solid",
        border_color="red",
        content_color="yellow",
        width=max_frame_width,
    )

    # Stack left-aligned (default)
    left_layout = composer.stack(
        [left_banner, left_frame_1, left_frame_2],
        align="left",
        spacing=1,
        width=terminal_width,
    )

    console.print("┌─ LEFT-ALIGNED (Default) ─────────────────────────────────┐")
    for line in left_layout:
        console.print(line, highlight=False, soft_wrap=False)
    console.print("└──────────────────────────────────────────────────────────┘")
    console.newline(2)

    # ==============================================================================
    # CENTER ALIGNMENT SECTION
    # ==============================================================================
    center_banner = BannerRenderer().render(
        "CENTER",
        font="small",
        start_color="green",
        end_color="cyan",
        width=max_frame_width,
    )

    center_frame_1 = create_section_frame(
        "Balanced",
        "✅ Perfect equilibrium\n🎯 Focused approach\n🌟 Best practices",
        emoji="✅",
        border_style="double",
        border_color="green",
        content_color="lightgreen",
        width=max_frame_width,
    )

    center_frame_2 = create_section_frame(
        "Harmonious",
        "🎨 Beautiful design\n🌈 Rich gradients\n✨ Premium quality",
        emoji="🎨",
        border_style="rounded",
        border_color="cyan",
        content_color="lightcyan",
        width=max_frame_width,
    )

    # Stack center-aligned
    center_layout = composer.stack(
        [center_banner, center_frame_1, center_frame_2],
        align="center",
        spacing=1,
        width=terminal_width,
    )

    console.print("┌─ CENTER-ALIGNED ──────────────────────────────────────────┐")
    for line in center_layout:
        console.print(line, highlight=False, soft_wrap=False)
    console.print("└──────────────────────────────────────────────────────────┘")
    console.newline(2)

    # ==============================================================================
    # RIGHT ALIGNMENT SECTION
    # ==============================================================================
    right_banner = BannerRenderer().render(
        "RIGHT",
        font="small",
        start_color="blue",
        end_color="magenta",
        width=max_frame_width,
    )

    right_frame_1 = create_section_frame(
        "Advanced",
        "🚀 Next generation\n✨ Cutting edge\n🌟 Innovation",
        emoji="🚀",
        border_style="heavy",
        border_color="blue",
        content_color="lightblue",
        width=max_frame_width,
    )

    right_frame_2 = create_section_frame(
        "Exclusive",
        "⭐ Premium features\n🏆 Luxury experience\n🎉 Award winning",
        emoji="⭐",
        border_style="double",
        border_color="magenta",
        content_color="lightpink",
        width=max_frame_width,
    )

    # Stack right-aligned
    right_layout = composer.stack(
        [right_banner, right_frame_1, right_frame_2],
        align="right",
        spacing=1,
        width=terminal_width,
    )

    console.print("┌─ RIGHT-ALIGNED ───────────────────────────────────────────┐")
    for line in right_layout:
        console.print(line, highlight=False, soft_wrap=False)
    console.print("└──────────────────────────────────────────────────────────┘")
    console.newline(2)

    # ==============================================================================
    # SECTION 3: Mixed Alignment Layout
    # ==============================================================================
    console.frame(
        "Creating dynamic visual hierarchy with mixed alignments",
        title="🎭 Mixed Alignment Display",
        border="double",
        border_color="yellow",
        content_color="white",
        padding=2,
    )

    console.newline(2)

    # Create three independent sections with different alignments
    section_a = create_section_frame(
        "Section A",
        "🎯 Left aligned\n📊 Data display\n💻 Technical info",
        emoji="🎯",
        border_style="solid",
        border_color="lime",
        content_color="lightgreen",
        width=max_frame_width,
    )

    section_b = create_section_frame(
        "Section B",
        "⭐ Center stage\n✨ Main focus\n🌟 Spotlight",
        emoji="⭐",
        border_style="rounded",
        border_color="yellow",
        content_color="lightyellow",
        width=max_frame_width,
    )

    section_c = create_section_frame(
        "Section C",
        "📈 Right side\n📋 Notifications\n⚠️ Important",
        emoji="📈",
        border_style="double",
        border_color="hotpink",
        content_color="lightpink",
        width=max_frame_width,
    )

    # Create three separate layouts
    left_mixed = composer.stack([section_a], align="left", width=terminal_width)
    center_mixed = composer.stack([section_b], align="center", width=terminal_width)
    right_mixed = composer.stack([section_c], align="right", width=terminal_width)

    # Combine them vertically
    mixed_layout = composer.stack(
        [left_mixed, center_mixed, right_mixed],
        spacing=1,
        width=terminal_width,
    )

    console.print("┌─ MIXED ALIGNMENTS ────────────────────────────────────────┐")
    for line in mixed_layout:
        console.print(line, highlight=False, soft_wrap=False)
    console.print("└──────────────────────────────────────────────────────────┘")
    console.newline(2)

    # ==============================================================================
    # SECTION 4: Emoji-Rich Dashboard
    # ==============================================================================
    banner_dash = BannerRenderer().render(
        "DASHBOARD",
        font="small",
        start_color="magenta",
        end_color="cyan",
        width=max_frame_width,
    )

    # Create dashboard cards with emojis
    card_1 = renderer.render(
        format_emoji_with_spacing("🚀", " Performance") + "\n\n95% uptime",
        border="rounded",
        border_color="green",
        content_color="lightgreen",
        width=max_frame_width // 2,
    )

    card_2 = renderer.render(
        format_emoji_with_spacing("💾", " Storage") + "\n\n512 GB free",
        border="rounded",
        border_color="cyan",
        content_color="lightcyan",
        width=max_frame_width // 2,
    )

    card_3 = renderer.render(
        format_emoji_with_spacing("📊", " Users") + "\n\n1,234 online",
        border="rounded",
        border_color="yellow",
        content_color="lightyellow",
        width=max_frame_width // 2,
    )

    # Stack dashboard centered
    dashboard_layout = composer.stack(
        [banner_dash, card_1, card_2, card_3],
        align="center",
        spacing=1,
        width=terminal_width,
    )

    console.print("┌─ EMOJI DASHBOARD (Centered) ──────────────────────────────┐")
    for line in dashboard_layout:
        console.print(line, highlight=False, soft_wrap=False)
    console.print("└──────────────────────────────────────────────────────────┘")
    console.newline(2)

    # ==============================================================================
    # SECTION 5: Rainbow Gradient Borders with All Styles
    # ==============================================================================
    console.frame(
        "All border styles with alignment demonstration",
        title="🌈 Border Style Gallery",
        border="double",
        border_color="magenta",
        content_color="white",
        padding=2,
    )

    console.newline(2)

    styles_to_show = ["solid", "rounded", "double", "heavy"]
    colors = ["lime", "cyan", "yellow", "hotpink"]

    for i, (style_name, color) in enumerate(zip(styles_to_show, colors)):
        style_frame = renderer.render(
            format_emoji_with_spacing("✨", f" {style_name.upper()}") + "\nBorder style demo",
            border=style_name,
            border_color=color,
            content_color="white",
            width=max_frame_width,
        )

        # Rotate alignments
        alignments = ["left", "center", "right"]
        align_choice = alignments[i % 3]

        style_layout = composer.stack([style_frame], align=align_choice, width=terminal_width)

        alignment_label = f"({align_choice.upper():^6})"
        console.print(f"  {alignment_label}")
        for line in style_layout:
            console.print(line, highlight=False, soft_wrap=False)
        console.newline()

    # ==============================================================================
    # FOOTER
    # ==============================================================================
    console.newline()
    footer_banner = BannerRenderer().render(
        "THE END",
        font="small",
        start_color="magenta",
        end_color="red",
        width=max_frame_width,
    )

    footer_layout = composer.stack([footer_banner], align="center", width=terminal_width)
    for line in footer_layout:
        console.print(line, highlight=False, soft_wrap=False)

    console.newline()
    footer_text = "🎉 Rainbow Fat Alignment Showcase Complete! 🎉"
    footer_frame = renderer.render(
        footer_text,
        border="double",
        border_color="magenta",
        content_color="white",
        width=max_frame_width,
    )
    footer_centered = composer.stack([footer_frame], align="center", width=terminal_width)
    for line in footer_centered:
        console.print(line, highlight=False, soft_wrap=False)

    console.newline()


if __name__ == "__main__":
    create_alignment_showcase()
