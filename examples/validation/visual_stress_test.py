#!/usr/bin/env python3
"""Visual stress test for StyledConsole on limited terminals.

This script uses ALL visually challenging features:
- Colorful frames with gradients
- Banners with ASCII art fonts
- Emojis and icons
- Animations
- Progress bars
- Nested/grouped frames

Run with different environments to see graceful degradation:

    # Full featured terminal
    uv run python examples/validation/visual_stress_test.py

    # Dumb terminal (no ANSI)
    TERM=dumb uv run python examples/validation/visual_stress_test.py

    # No color mode
    NO_COLOR=1 uv run python examples/validation/visual_stress_test.py

    # CI environment
    CI=true uv run python examples/validation/visual_stress_test.py

    # Pipe to file
    uv run python examples/validation/visual_stress_test.py 2>&1 | tee output.txt
"""

import os
import sys
import time

from styledconsole import Console, icons
from styledconsole.animation import Animation


def show_environment():
    """Display current environment and detected policy."""
    console = Console()
    policy = console.policy

    env_info = [
        f"TERM: {os.environ.get('TERM', '(not set)')}",
        f"NO_COLOR: {os.environ.get('NO_COLOR', '(not set)')}",
        f"CI: {os.environ.get('CI', '(not set)')}",
        f"TTY: {sys.stdout.isatty()}",
    ]

    policy_info = [
        f"unicode: {policy.unicode}",
        f"color: {policy.color}",
        f"emoji: {policy.emoji}",
        f"force_ascii_icons: {policy.force_ascii_icons}",
    ]

    console.frame(env_info, title=f"{icons.GEAR} Environment", border="rounded")
    console.frame(policy_info, title=f"{icons.INFO} Policy", border="rounded")
    console.newline()


def test_colorful_banner():
    """Test banner with gradient colors."""
    print("=" * 60)
    print("TEST 1: Colorful Banner with Gradient")
    print("=" * 60)

    console = Console()

    # Gradient banner
    console.banner(
        "WELCOME",
        font="slant",
        start_color="magenta",
        end_color="cyan",
        border="double",
    )
    console.newline()


def test_emoji_rich_frames():
    """Test frames with emojis and icons."""
    print("=" * 60)
    print("TEST 2: Emoji-Rich Frames")
    print("=" * 60)

    console = Console()

    # Status frame with policy-aware icons
    status_content = [
        f"{icons.CHECK} All tests passed",
        f"{icons.ROCKET} Deployment ready",
        f"{icons.STAR} Performance: Excellent",
        f"{icons.FIRE} 0 critical issues",
    ]
    console.frame(
        status_content,
        title=f"{icons.SPARKLES} Status Report {icons.SPARKLES}",
        border="rounded",
        border_color="green",
    )

    # Warning frame
    warning_content = [
        f"{icons.WARNING} 3 deprecation warnings",
        f"{icons.CLOCK} Build time: 45s",
    ]
    console.frame(
        warning_content,
        title=f"{icons.WARNING} Warnings",
        border="rounded",
        border_color="yellow",
    )

    # Error frame
    error_content = [
        f"{icons.CROSS} Connection timeout",
        f"{icons.BUG} Stack trace available",
    ]
    console.frame(
        error_content,
        title=f"{icons.CROSS} Errors",
        border="rounded",
        border_color="red",
    )
    console.newline()


def test_icon_provider():
    """Test the Icon provider system."""
    print("=" * 60)
    print("TEST 3: Icon Provider (emoji vs ASCII)")
    print("=" * 60)

    console = Console()

    # Icons adapt to terminal capabilities
    icon_demo = [
        f"{icons.CHECK} Success icon",
        f"{icons.CROSS} Error icon",
        f"{icons.WARNING} Warning icon",
        f"{icons.INFO} Info icon",
        f"{icons.STAR} Star icon",
        f"{icons.ARROW_RIGHT} Arrow right",
    ]
    console.frame(
        icon_demo,
        title="Icons (auto-adapt to terminal)",
        border="rounded",
        border_color="cyan",
    )
    console.newline()


def test_gradient_frames():
    """Test frames with border gradients."""
    print("=" * 60)
    print("TEST 4: Gradient Border Frames")
    print("=" * 60)

    console = Console()

    # Vertical gradient
    console.frame(
        ["This frame has a", "gradient border", "from red to blue"],
        title="Gradient Border",
        border="rounded",
        border_gradient_start="red",
        border_gradient_end="blue",
    )

    # Another gradient
    console.frame(
        ["Purple to gold", "gradient effect"],
        title="Royal Gradient",
        border="double",
        border_gradient_start="purple",
        border_gradient_end="gold",
    )
    console.newline()


def test_styled_text():
    """Test styled text output."""
    print("=" * 60)
    print("TEST 5: Styled Text")
    print("=" * 60)

    console = Console()

    console.text("Bold text", bold=True)
    console.text("Italic text", italic=True)
    console.text("Underlined text", underline=True)
    console.text("Dimmed text", dim=True)
    console.text("Colored text (cyan)", color="cyan")
    console.text("Colored text (magenta)", color="magenta")
    console.text("Combined: bold + color", bold=True, color="green")
    console.newline()

    # Styled rule
    console.rule("Section Divider", color="yellow")
    console.newline()


def test_animated_dashboard():
    """Test animated content inside frames."""
    print("=" * 60)
    print("TEST 6: Animated Dashboard")
    print("=" * 60)

    console = Console()

    def dashboard_frames():
        metrics = [
            ("CPU", 45, 78, 92, 65, 55, 70, 82, 60),
            ("MEM", 62, 65, 68, 71, 74, 72, 70, 68),
            ("NET", 10, 25, 45, 80, 95, 60, 30, 15),
        ]

        for i in range(8):
            content = [
                f"{icons.CHART_BAR} System Monitor",
                "",
            ]
            for name, *values in metrics:
                val = values[i]
                bar_len = val // 10
                bar = "█" * bar_len + "░" * (10 - bar_len)
                # Use policy-aware colored circle icons
                if val < 70:
                    status_icon = icons.GREEN_CIRCLE
                elif val < 90:
                    status_icon = icons.YELLOW_CIRCLE
                else:
                    status_icon = icons.RED_CIRCLE
                content.append(f"  {name}: [{bar}] {val:3d}% {status_icon}")

            content.append("")
            content.append(f"  {icons.CLOCK} Update {i + 1}/8")

            frame = console.render_frame(
                content,
                title=f"{icons.COMPUTER} Dashboard",
                border="rounded",
                border_color="cyan",
                width=45,
            )
            yield frame + "\n"

    Animation.run(dashboard_frames(), fps=2, duration=5)
    print()


def test_progress_bars():
    """Test multiple progress bars."""
    print("=" * 60)
    print("TEST 7: Progress Bars")
    print("=" * 60)

    console = Console()

    print("Single task progress:")
    with console.progress() as progress:
        task = progress.add_task(f"{icons.PACKAGE} Installing...", total=100)
        for _ in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)

    print()
    print("Multiple concurrent tasks:")
    with console.progress() as progress:
        task1 = progress.add_task(f"{icons.ARROW_DOWN} Downloading", total=100)
        task2 = progress.add_task(f"{icons.GEAR} Processing", total=100)
        task3 = progress.add_task(f"{icons.CHECK} Verifying", total=100)

        for i in range(100):
            time.sleep(0.03)
            progress.update(task1, advance=1)
            if i >= 20:
                progress.update(task2, advance=1.25)
            if i >= 50:
                progress.update(task3, advance=2)

    console.newline()


def test_nested_frames():
    """Test frame groups and nesting."""
    print("=" * 60)
    print("TEST 8: Nested/Grouped Frames")
    print("=" * 60)

    console = Console()

    # Use frame_group for related content
    console.frame_group(
        items=[
            {"content": ["Server: Online", "Uptime: 99.9%"], "title": "Backend"},
            {"content": ["Cache: Active", "Hit rate: 87%"], "title": "Redis"},
            {"content": ["Pool: 45/100", "Queries: 1.2k/s"], "title": "Database"},
        ],
        title=f"{icons.CLOUD} Infrastructure Status",
        border="double",
        border_color="blue",
        gap=0,
    )
    console.newline()


def test_all_border_styles():
    """Test all border styles."""
    print("=" * 60)
    print("TEST 9: All Border Styles")
    print("=" * 60)

    console = Console()

    styles = ["solid", "rounded", "double", "heavy", "thick", "ascii", "minimal"]

    for style in styles:
        console.frame(
            f"Border style: {style}",
            title=style.upper(),
            border=style,
            border_color="cyan",
            width=30,
        )
    console.newline()


def test_mixed_content():
    """Test complex mixed content."""
    print("=" * 60)
    print("TEST 10: Complex Mixed Content")
    print("=" * 60)

    console = Console()

    # Complex report
    console.banner(
        "REPORT",
        font="small",
        start_color="green",
        end_color="blue",
    )

    console.rule(f"{icons.INFO} Summary", color="cyan")

    summary = [
        f"{icons.CHECK} 142 tests passed",
        f"{icons.CROSS} 3 tests failed",
        f"{icons.WARNING} 12 warnings",
        f"{icons.INFO} Coverage: 94.2%",
    ]
    console.frame(summary, title="Test Results", border="rounded", border_color="green")

    console.rule(f"{icons.CHART_BAR} Metrics", color="yellow")

    metrics = [
        "Build time:     2m 34s",
        "Bundle size:    1.2 MB",
        "Dependencies:   47",
        "Security:       No issues",
    ]
    console.frame(metrics, title="Build Info", border="rounded", border_color="blue")

    console.newline()
    console.text(f"{icons.SPARKLES} Report generated successfully!", color="green", bold=True)
    console.newline()


def main():
    """Run all visual stress tests."""
    import argparse

    parser = argparse.ArgumentParser(description="Visual stress test for StyledConsole")
    parser.add_argument(
        "--skip-slow",
        action="store_true",
        help="Skip slow tests (animations, progress bars)",
    )
    args = parser.parse_args()

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " STYLEDCONSOLE VISUAL STRESS TEST ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()

    show_environment()

    tests = [
        ("Colorful Banner", test_colorful_banner, False),
        ("Emoji-Rich Frames", test_emoji_rich_frames, False),
        ("Icon Provider", test_icon_provider, False),
        ("Gradient Frames", test_gradient_frames, False),
        ("Styled Text", test_styled_text, False),
        ("Animated Dashboard", test_animated_dashboard, True),  # slow
        ("Progress Bars", test_progress_bars, True),  # slow
        ("Nested Frames", test_nested_frames, False),
        ("Border Styles", test_all_border_styles, False),
        ("Mixed Content", test_mixed_content, False),
    ]

    for i, (name, test_func, is_slow) in enumerate(tests, 1):
        if args.skip_slow and is_slow:
            print(f"\nSKIPPING TEST {i}: {name}")
            continue

        print(f"\n>>> TEST {i}: {name}")
        try:
            test_func()
        except Exception as e:
            print(f"ERROR in {name}: {e}")

    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " ALL TESTS COMPLETE ".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    print("Check if output degraded gracefully based on your terminal.")
    print("- Colors should disappear with NO_COLOR=1")
    print("- Emojis should become ASCII with TERM=dumb or CI=true")
    print("- Borders should use ASCII with TERM=dumb")
    print("- Animations should show all frames with TERM=dumb or pipe")
    print()


if __name__ == "__main__":
    main()
