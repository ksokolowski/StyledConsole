"""CI/CD Dashboard Example

A comprehensive example demonstrating a CI/CD pipeline dashboard using:
- Banner header with gradient
- Grid layout using manual formatting
- Color-coded status indicators
- Emojis for visual status
- Pass/fail ratios with progress indicators
- Gradients for visual appeal

v0.4.0: Updated to use Console.banner() and Console.frame() exclusively.
"""

from io import StringIO

from styledconsole import Console


def print_row(buffers, spacing=2):
    """Print multiple frames side by side."""
    all_lines = [buf.getvalue().splitlines() for buf in buffers]
    max_lines = max(len(lines) for lines in all_lines)

    for i in range(max_lines):
        row_parts = []
        for lines in all_lines:
            if i < len(lines):
                row_parts.append(lines[i])
            else:
                # Get width from first line if available
                width = len(lines[0]) if lines else 24
                row_parts.append(" " * width)
        print((" " * spacing).join(row_parts))


def create_cicd_dashboard():
    """Create a full CI/CD pipeline dashboard."""
    console = Console()

    # Header banner with gradient
    print("\n")
    console.banner(
        "CI/CD PIPELINE",
        font="banner",
        start_color="deepskyblue",
        end_color="royalblue",
        width=80,
        align="center",
    )
    print()

    # Row 1: Build stages
    print("BUILD STAGE")
    print("=" * 80)

    buffer1 = StringIO()
    Console(file=buffer1, detect_terminal=False).frame(
        ["✅ Passed", "Duration: 1.2s", "Pass Rate: 100%"],
        title="🔍 Lint",
        border="rounded",
        content_color="lime",
        border_color="lime",
        title_color="white",
        width=24,
    )

    buffer2 = StringIO()
    Console(file=buffer2, detect_terminal=False).frame(
        ["✅ Passed", "Duration: 45s", "Pass Rate: 98%"],
        title="⚙️  Compile",
        border="rounded",
        content_color="lime",
        border_color="lime",
        title_color="white",
        width=24,
    )

    buffer3 = StringIO()
    Console(file=buffer3, detect_terminal=False).frame(
        ["⚠️  Warning", "Duration: 8s", "3 minor issues"],
        title="🔒 Security",
        border="rounded",
        content_color="orange",
        border_color="orange",
        title_color="white",
        width=24,
    )

    print_row([buffer1, buffer2, buffer3])
    print()

    # Row 2: Test stages
    print("TEST STAGE")
    print("=" * 80)

    buffer4 = StringIO()
    Console(file=buffer4, detect_terminal=False).frame(
        ["✅ Passed", "329/329 tests", "Coverage: 99%"],
        title="🧪 Unit Tests",
        border="rounded",
        start_color="lime",
        end_color="darkgreen",
        border_color="lime",
        title_color="white",
        width=24,
    )

    buffer5 = StringIO()
    Console(file=buffer5, detect_terminal=False).frame(
        ["✅ Passed", "47/47 tests", "Duration: 2m"],
        title="🔗 Integration",
        border="rounded",
        start_color="lime",
        end_color="darkgreen",
        border_color="lime",
        title_color="white",
        width=24,
    )

    buffer6 = StringIO()
    Console(file=buffer6, detect_terminal=False).frame(
        ["❌ Failed", "12/15 passed", "3 failures"],
        title="🌐 E2E Tests",
        border="rounded",
        content_color="red",
        border_color="red",
        title_color="white",
        width=24,
    )

    print_row([buffer4, buffer5, buffer6])
    print()

    # Row 3: Deploy stages
    print("DEPLOY STAGE")
    print("=" * 80)

    buffer7 = StringIO()
    Console(file=buffer7, detect_terminal=False).frame(
        ["✅ Deployed", "Version: 1.2.3", "Healthy"],
        title="🚀 Staging",
        border="rounded",
        start_color="#00d4ff",
        end_color="#0066ff",
        border_color="#00d4ff",
        title_color="#ffffff",
        width=24,
    )

    buffer8 = StringIO()
    Console(file=buffer8, detect_terminal=False).frame(
        ["⏸️  Waiting", "Approval needed", "ETA: pending"],
        title="🌟 Production",
        border="rounded",
        content_color="#888888",
        border_color="#888888",
        title_color="#ffffff",
        width=24,
    )

    buffer9 = StringIO()
    Console(file=buffer9, detect_terminal=False).frame(
        ["✅ Ready", "Last: v1.2.2", "Available"],
        title="🔄 Rollback",
        border="rounded",
        content_color="#00aaff",
        border_color="#00aaff",
        title_color="#ffffff",
        width=24,
    )

    print_row([buffer7, buffer8, buffer9])
    print()

    # Overall summary frame
    console.frame(
        [
            "Pipeline Status: 🔴 FAILED (E2E tests)",
            "Total Duration: 3m 45s",
            "Success Rate: 88.9% (8/9 stages passed)",
            "Next Action: Fix E2E failures and retry",
        ],
        title="📊 Summary",
        border="double",
        start_color="#ff0000",
        end_color="#ffaa00",
        border_color="#ffaa00",
        title_color="#ffffff",
        width=80,
        align="left",
        padding=2,
    )
    print()


def create_success_dashboard():
    """Create a dashboard showing all stages passed."""
    console = Console()

    print("\n")

    # Success banner
    console.banner(
        "ALL CLEAR",
        font="slant",
        start_color="#00ff00",
        end_color="#00aa00",
        width=80,
        align="center",
    )
    print()

    # Mini stats grid (2x2)
    print("STATS")
    print("=" * 80)

    # Row 1
    buffer1 = StringIO()
    Console(file=buffer1, detect_terminal=False).frame(
        ["✅ 100%", "0 errors"],
        title="Build",
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        title_color="#ffffff",
        width=24,
    )

    buffer2 = StringIO()
    Console(file=buffer2, detect_terminal=False).frame(
        ["✅ 100%", "376 passed"],
        title="Tests",
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        title_color="#ffffff",
        width=24,
    )

    print_row([buffer1, buffer2], spacing=10)
    print()

    # Row 2
    buffer3 = StringIO()
    Console(file=buffer3, detect_terminal=False).frame(
        ["✅ 99.03%", "514 lines"],
        title="Coverage",
        border="solid",
        start_color="#00ff00",
        end_color="#00cc00",
        border_color="#00ff00",
        title_color="#ffffff",
        width=24,
    )

    buffer4 = StringIO()
    Console(file=buffer4, detect_terminal=False).frame(
        ["✅ Live", "v1.2.4"],
        title="Deploy",
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        title_color="#ffffff",
        width=24,
    )

    print_row([buffer3, buffer4], spacing=10)
    print()

    # Success message
    console.frame(
        [
            "🎉 All pipeline stages completed successfully!",
            "",
            "✨ Build: Passed",
            "✨ Tests: 376/376 passed (99.03% coverage)",
            "✨ Security: No vulnerabilities",
            "✨ Deploy: Production updated to v1.2.4",
            "",
            "Duration: 4m 12s  |  Commit: abc123f  |  Branch: main",
        ],
        title="SUCCESS",
        border="heavy",
        start_color="#00ff00",
        end_color="#00ffaa",
        border_color="#00ff00",
        title_color="#ffffff",
        width=80,
        align="left",
        padding=2,
    )
    print()


def create_monitoring_dashboard():
    """Create a system monitoring dashboard."""
    console = Console()

    print("\n")

    # Header
    console.banner(
        "MONITORING",
        font="standard",
        start_color="#ff00ff",
        end_color="#00ffff",
        width=80,
    )
    print()

    # System metrics (3x2 grid)
    print("SYSTEM METRICS")
    print("=" * 80)

    # Row 1
    buffer1 = StringIO()
    Console(file=buffer1, detect_terminal=False).frame(
        ["Usage: 34%", "Load: 1.2", "Cores: 8"],
        title="💻 CPU",
        border="rounded",
        start_color="#00ff00",
        end_color="#ffff00",
        border_color="#00ff00",
        width=24,
    )

    buffer2 = StringIO()
    Console(file=buffer2, detect_terminal=False).frame(
        ["Used: 8.2GB", "Free: 7.8GB", "Total: 16GB"],
        title="🧠 Memory",
        border="rounded",
        start_color="#00ff00",
        end_color="#ffaa00",
        border_color="#ffaa00",
        width=24,
    )

    buffer3 = StringIO()
    Console(file=buffer3, detect_terminal=False).frame(
        ["Used: 145GB", "Free: 355GB", "Total: 500GB"],
        title="💾 Disk",
        border="rounded",
        content_color="#00ff00",
        border_color="#00ff00",
        width=24,
    )

    print_row([buffer1, buffer2, buffer3])
    print()

    # Row 2
    buffer4 = StringIO()
    Console(file=buffer4, detect_terminal=False).frame(
        ["↓ 1.2 Mbps", "↑ 0.8 Mbps", "Latency: 12ms"],
        title="🌐 Network",
        border="rounded",
        content_color="#00aaff",
        border_color="#00aaff",
        width=24,
    )

    buffer5 = StringIO()
    Console(file=buffer5, detect_terminal=False).frame(
        ["Running: 12", "Stopped: 0", "All healthy"],
        title="⚙️  Services",
        border="rounded",
        content_color="#00ff00",
        border_color="#00ff00",
        width=24,
    )

    buffer6 = StringIO()
    Console(file=buffer6, detect_terminal=False).frame(
        ["42 days", "99.98%", "Last boot: OK"],
        title="⏱️  Uptime",
        border="rounded",
        start_color="#00ffff",
        end_color="#0066ff",
        border_color="#00ffff",
        width=24,
    )

    print_row([buffer4, buffer5, buffer6])
    print()

    # Status bar
    console.frame(
        ["🟢 All systems operational  |  Last updated: 2025-10-18 14:23:15"],
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        width=80,
    )
    print()


def main():
    """Run all dashboard examples."""
    print("=" * 80)
    print(" " * 25 + "CI/CD DASHBOARD EXAMPLES")
    print("=" * 80)

    create_cicd_dashboard()
    print("\n" + "=" * 80)
    create_success_dashboard()
    print("\n" + "=" * 80)
    create_monitoring_dashboard()

    print("=" * 80)


if __name__ == "__main__":
    main()
