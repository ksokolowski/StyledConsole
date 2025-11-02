#!/usr/bin/env python3
"""Advanced Dashboard Example

Demonstrates all StyledConsole features in one comprehensive dashboard:
- Phase 1 improvements: Input validation, performance caching, lazy init, color system
- Phase 2 improvements: Literal types (AlignType), public API
- Emoji support with proper width calculation
- Gradients for both frames and content
- Multiple border styles in 3x3 grid
- Colored titles with emojis
- Variable-length content handling
- All alignment options

This example showcases the library's production-ready capabilities!
"""

from styledconsole import (
    AlignType,  # Phase 2: Type safety with Literal types
    BannerRenderer,
    Console,
    FrameRenderer,
    LayoutComposer,
)


def create_header_banner() -> list[str]:
    """Create impressive gradient banner header."""
    banner_renderer = BannerRenderer()
    return banner_renderer.render(
        "DASHBOARD",
        font="banner",
        start_color="red",
        end_color="yellow",
        border="double",
        width=80,
        align="center",  # AlignType: IDE knows this is valid!
    )


def create_status_grid() -> list[str]:
    """Create 3x3 grid with different frame styles, emojis, and gradients."""
    frame_renderer = FrameRenderer()
    composer = LayoutComposer()

    # Row 1: Different border styles with emoji titles
    frame1 = frame_renderer.render(
        ["Status: Online ✅", "Uptime: 99.9%", "Requests: 1.2M"],
        title="🚀 Server",  # 2 emojis in title!
        border="solid",
        start_color="lime",
        end_color="blue",
        border_color="lime",
        title_color="white",
        width=25,
        align="left",  # Type safety: "left" | "center" | "right"
    )

    frame2 = frame_renderer.render(
        ["CPU: 23% 📊", "RAM: 45% 💾", "Disk: 67% 💿"],
        title="⚡ Resources",
        border="rounded",
        content_color="orange",
        border_color="orange",
        title_color="yellow",
        width=25,
        align="center",
    )

    frame3 = frame_renderer.render(
        ["Active: 342 👥", "Peak: 891 📈", "Avg: 456 📊"],
        title="👥 Users",  # Single emoji to avoid width issues
        border="double",
        start_color="magenta",
        end_color="cyan",
        border_color="magenta",
        title_color="white",
        width=25,
        align="right",
    )

    row1 = composer.side_by_side(
        composer.stack([frame1], spacing=0),
        composer.side_by_side(
            composer.stack([frame2], spacing=0),
            composer.stack([frame3], spacing=0),
            spacing=2,
        ),
        spacing=2,
    )

    # Row 2: More styles with colorful content
    frame4 = frame_renderer.render(
        ["✅ Passed: 466", "❌ Failed: 0", "⏭️ Skipped: 0"],
        title="🧪 Tests",
        border="heavy",
        start_color="cyan",
        end_color="yellow",
        border_color="cyan",
        title_color="white",
        width=25,
        align="center",
    )

    frame5 = frame_renderer.render(
        ["Coverage: 95.76%", "Statements: 849", "Branches: 100%"],
        title="📊 Quality",
        border="thick",
        content_color="lime",
        border_color="lime",
        title_color="lime",
        width=25,
        align="center",
    )

    frame6 = frame_renderer.render(
        ["🔴 Critical: 0", "🟡 Warning: 2", "🟢 Info: 15"],
        title="⚠️ Alerts",
        border="minimal",
        start_color="red",
        end_color="yellow",
        border_color="orangered",
        title_color="white",
        width=25,
        align="center",
    )

    row2 = composer.side_by_side(
        composer.stack([frame4], spacing=0),
        composer.side_by_side(
            composer.stack([frame5], spacing=0),
            composer.stack([frame6], spacing=0),
            spacing=2,
        ),
        spacing=2,
    )

    # Row 3: Final row with ASCII and dots styles
    frame7 = frame_renderer.render(
        ["v0.1.0 → v0.2.0", "Features: +12", "Fixes: +8"],
        title="📦 Release",
        border="ascii",
        start_color="blue",
        end_color="red",
        border_color="blue",
        title_color="white",
        width=25,
        align="center",
    )

    frame8 = frame_renderer.render(
        ["Phase 1: ✅", "Phase 2: ✅", "Phase 3: 🔄"],
        title="🎯 Progress",
        border="dots",
        content_color="lime",
        border_color="lime",
        title_color="yellow",
        width=25,
        align="center",
    )

    frame9 = frame_renderer.render(
        ["AlignType ✅", "ColorType ✅", "__all__ ✅"],
        title="🔒 API",
        border="rounded",
        start_color="yellow",
        end_color="magenta",
        border_color="yellow",
        title_color="white",
        width=25,
        align="center",
    )

    row3 = composer.side_by_side(
        composer.stack([frame7], spacing=0),
        composer.side_by_side(
            composer.stack([frame8], spacing=0),
            composer.stack([frame9], spacing=0),
            spacing=2,
        ),
        spacing=2,
    )

    # Stack all rows
    return composer.stack([row1, row2, row3], spacing=1, align="center")


def create_feature_highlights() -> list[str]:
    """Showcase variable-length content and text wrapping."""
    frame_renderer = FrameRenderer()

    # Long content that demonstrates auto-wrapping
    features = [
        "✨ Phase 1: Input validation, performance caching (LRU), lazy initialization, "
        "color system mapping",
        "🎯 Phase 2: Literal types (AlignType, ColorType), Renderer protocol, "
        "public API with __all__",
        "🚀 Production Ready: 466 tests passing, 95.76% coverage, semantic versioning commitment",
        "🎨 Rich Features: 8 border styles, gradients, emojis, layouts, wrapping, "
        "export capabilities",
    ]

    return frame_renderer.render(
        features,
        title="🌟 Key Features",
        border="heavy",
        start_color="red",
        end_color="cyan",
        border_color="red",
        title_color="white",
        width=80,
        padding=2,
        align="left",
    )


def create_type_safety_demo() -> list[str]:
    """Demonstrate Phase 2 type safety improvements."""
    frame_renderer = FrameRenderer()

    # This showcases the new type safety - IDE knows align can only be "left", "center", or "right"
    alignments: list[tuple[AlignType, str]] = [
        ("left", "Left-aligned with type safety"),
        ("center", "Center-aligned with IDE support"),
        ("right", "Right-aligned, type-checked"),
    ]

    frames = []
    for align_type, description in alignments:
        frame = frame_renderer.render(
            [description, f"align='{align_type}' ✅"],
            title=f"AlignType: {align_type}",
            border="rounded",
            start_color="magenta",
            end_color="lime",
            border_color="magenta",
            title_color="white",
            width=35,
            align=align_type,  # IDE autocomplete shows only valid options!
        )
        frames.append(frame)

    composer = LayoutComposer()
    return composer.stack(frames, spacing=1, align="center")


def main():
    """Run the advanced dashboard demonstration."""
    console = Console()

    # Phase 1 improvement: Terminal detection and color system mapping
    print("\n")
    print("=" * 80)
    print(" " * 20 + "🎨 STYLEDCONSOLE ADVANCED DASHBOARD 🎨")
    print("=" * 80)
    print()

    # Display header banner
    print("HEADER BANNER (Gradient + Border):")
    print("-" * 80)
    header = create_header_banner()
    for line in header:
        print(line)
    print()

    # Display 3x3 status grid
    print("3x3 GRID (All Border Styles + Emojis + Gradients):")
    print("-" * 80)
    grid = create_status_grid()
    for line in grid:
        print(line)
    print()

    # Display feature highlights
    print("VARIABLE-LENGTH CONTENT (Auto-wrapping):")
    print("-" * 80)
    features = create_feature_highlights()
    for line in features:
        print(line)
    print()

    # Display type safety demo
    print("PHASE 2 TYPE SAFETY (AlignType Literal):")
    print("-" * 80)
    type_demo = create_type_safety_demo()
    for line in type_demo:
        print(line)
    print()

    # Footer with statistics
    print("=" * 80)
    console.frame(
        [
            "✅ All features demonstrated successfully!",
            "📊 Tests: 466/466 passing",
            "🎯 Coverage: 95.76%",
            "🚀 Status: Production Ready",
        ],
        title="🎉 Dashboard Complete",
        border="double",
        start_color="lime",
        end_color="cyan",
        border_color="lime",
        title_color="white",
        width=80,
        align="center",
    )
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
