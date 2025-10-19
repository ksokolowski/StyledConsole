"""CI/CD Dashboard Example

A comprehensive example demonstrating a CI/CD pipeline dashboard using:
- Banner header with gradient
- 3x3 grid layout for pipeline stages
- Color-coded status indicators
- Emojis for visual status
- Pass/fail ratios with progress indicators
- Gradients for visual appeal
"""

from styledconsole import BannerRenderer, FrameRenderer, LayoutComposer


def create_cicd_dashboard():
    """Create a full CI/CD pipeline dashboard."""
    composer = LayoutComposer()
    banner_renderer = BannerRenderer()
    frame_renderer = FrameRenderer()

    # Header banner with gradient
    print("\n")
    title_banner = banner_renderer.render(
        "CI/CD PIPELINE",
        font="banner",
        gradient_start="deepskyblue",
        gradient_end="royalblue",
        width=80,
        align="center",
    )

    # Pipeline stages with status - 3x3 grid
    # Row 1: Build stages
    build_lint = frame_renderer.render(
        ["✅ Passed", "Duration: 1.2s", "Pass Rate: 100%"],
        title="🔍 Lint",
        border="rounded",
        content_color="lime",
        border_color="lime",
        title_color="white",
    )

    build_compile = frame_renderer.render(
        ["✅ Passed", "Duration: 45s", "Pass Rate: 98%"],
        title="⚙️  Compile",
        border="rounded",
        content_color="lime",
        border_color="lime",
        title_color="white",
    )

    build_security = frame_renderer.render(
        ["⚠️  Warning", "Duration: 8s", "3 minor issues"],
        title="🔒 Security",
        border="rounded",
        content_color="orange",
        border_color="orange",
        title_color="white",
    )

    # Row 2: Test stages
    test_unit = frame_renderer.render(
        ["✅ Passed", "329/329 tests", "Coverage: 99%"],
        title="🧪 Unit Tests",
        border="rounded",
        gradient_start="lime",
        gradient_end="darkgreen",
        border_color="lime",
        title_color="white",
    )

    test_integration = frame_renderer.render(
        ["✅ Passed", "47/47 tests", "Duration: 2m"],
        title="🔗 Integration",
        border="rounded",
        gradient_start="lime",
        gradient_end="darkgreen",
        border_color="lime",
        title_color="white",
    )

    test_e2e = frame_renderer.render(
        ["❌ Failed", "12/15 passed", "3 failures"],
        title="🌐 E2E Tests",
        border="rounded",
        content_color="red",
        border_color="red",
        title_color="white",
    )

    # Row 3: Deploy stages
    deploy_staging = frame_renderer.render(
        ["✅ Deployed", "Version: 1.2.3", "Healthy"],
        title="🚀 Staging",
        border="rounded",
        gradient_start="#00d4ff",  # Cyan
        gradient_end="#0066ff",  # Blue
        border_color="#00d4ff",
        title_color="#ffffff",
    )

    deploy_prod = frame_renderer.render(
        ["⏸️  Waiting", "Approval needed", "ETA: pending"],
        title="🌟 Production",
        border="rounded",
        content_color="#888888",  # Gray
        border_color="#888888",
        title_color="#ffffff",
    )

    deploy_rollback = frame_renderer.render(
        ["✅ Ready", "Last: v1.2.2", "Available"],
        title="🔄 Rollback",
        border="rounded",
        content_color="#00aaff",  # Light blue
        border_color="#00aaff",
        title_color="#ffffff",
    )

    # Create 3x3 grid
    row1 = [build_lint, build_compile, build_security]
    row2 = [test_unit, test_integration, test_e2e]
    row3 = [deploy_staging, deploy_prod, deploy_rollback]

    pipeline_grid = composer.grid([row1, row2, row3], column_spacing=2, row_spacing=1)

    # Overall summary frame
    summary = frame_renderer.render(
        [
            "Pipeline Status: 🔴 FAILED (E2E tests)",
            "Total Duration: 3m 45s",
            "Success Rate: 88.9% (8/9 stages passed)",
            "Next Action: Fix E2E failures and retry",
        ],
        title="📊 Summary",
        border="double",
        gradient_start="#ff0000",  # Red at top
        gradient_end="#ffaa00",  # Orange at bottom
        border_color="#ffaa00",
        title_color="#ffffff",
        width=80,
        align="left",
        padding=2,
    )

    # Combine all sections
    dashboard = composer.stack([title_banner, pipeline_grid, summary], spacing=1, width=80)

    # Print the dashboard
    for line in dashboard:
        print(line)
    print()


def create_success_dashboard():
    """Create a dashboard showing all stages passed."""
    composer = LayoutComposer()
    banner_renderer = BannerRenderer()
    frame_renderer = FrameRenderer()

    print("\n")

    # Success banner
    title_banner = banner_renderer.render(
        "ALL CLEAR",
        font="slant",
        gradient_start="#00ff00",
        gradient_end="#00aa00",
        width=80,
        align="center",
    )

    # Mini stats grid (2x2)
    stats_build = frame_renderer.render(
        ["✅ 100%", "0 errors"],
        title="Build",
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        title_color="#ffffff",
    )

    stats_test = frame_renderer.render(
        ["✅ 100%", "376 passed"],
        title="Tests",
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        title_color="#ffffff",
    )

    stats_coverage = frame_renderer.render(
        ["✅ 99.03%", "514 lines"],
        title="Coverage",
        border="solid",
        gradient_start="#00ff00",
        gradient_end="#00cc00",
        border_color="#00ff00",
        title_color="#ffffff",
    )

    stats_deploy = frame_renderer.render(
        ["✅ Live", "v1.2.4"],
        title="Deploy",
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        title_color="#ffffff",
    )

    stats_row1 = [stats_build, stats_test]
    stats_row2 = [stats_coverage, stats_deploy]
    stats_grid = composer.grid([stats_row1, stats_row2], column_spacing=2, row_spacing=1)

    # Success message
    message = frame_renderer.render(
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
        gradient_start="#00ff00",
        gradient_end="#00ffaa",
        border_color="#00ff00",
        title_color="#ffffff",
        width=80,
        align="left",
        padding=2,
    )

    dashboard = composer.stack([title_banner, stats_grid, message], spacing=1, width=80)

    for line in dashboard:
        print(line)
    print()


def create_monitoring_dashboard():
    """Create a system monitoring dashboard."""
    composer = LayoutComposer()
    banner_renderer = BannerRenderer()
    frame_renderer = FrameRenderer()

    print("\n")

    # Header
    header = banner_renderer.render(
        "MONITORING",
        font="standard",
        gradient_start="#ff00ff",  # Magenta
        gradient_end="#00ffff",  # Cyan
        width=80,
    )

    # System metrics (3x2 grid)
    cpu_metric = frame_renderer.render(
        ["Usage: 34%", "Load: 1.2", "Cores: 8"],
        title="💻 CPU",
        border="rounded",
        gradient_start="#00ff00",
        gradient_end="#ffff00",
        border_color="#00ff00",
    )

    memory_metric = frame_renderer.render(
        ["Used: 8.2GB", "Free: 7.8GB", "Total: 16GB"],
        title="🧠 Memory",
        border="rounded",
        gradient_start="#00ff00",
        gradient_end="#ffaa00",
        border_color="#ffaa00",
    )

    disk_metric = frame_renderer.render(
        ["Used: 145GB", "Free: 355GB", "Total: 500GB"],
        title="💾 Disk",
        border="rounded",
        content_color="#00ff00",
        border_color="#00ff00",
    )

    network_metric = frame_renderer.render(
        ["↓ 1.2 Mbps", "↑ 0.8 Mbps", "Latency: 12ms"],
        title="🌐 Network",
        border="rounded",
        content_color="#00aaff",
        border_color="#00aaff",
    )

    services_metric = frame_renderer.render(
        ["Running: 12", "Stopped: 0", "All healthy"],
        title="⚙️  Services",
        border="rounded",
        content_color="#00ff00",
        border_color="#00ff00",
    )

    uptime_metric = frame_renderer.render(
        ["42 days", "99.98%", "Last boot: OK"],
        title="⏱️  Uptime",
        border="rounded",
        gradient_start="#00ffff",
        gradient_end="#0066ff",
        border_color="#00ffff",
    )

    row1 = [cpu_metric, memory_metric, disk_metric]
    row2 = [network_metric, services_metric, uptime_metric]
    metrics_grid = composer.grid([row1, row2], column_spacing=2, row_spacing=1)

    # Status bar
    status = frame_renderer.render(
        ["🟢 All systems operational  |  Last updated: 2025-10-18 14:23:15"],
        border="solid",
        content_color="#00ff00",
        border_color="#00ff00",
        width=80,
    )

    dashboard = composer.stack([header, metrics_grid, status], spacing=1, width=80)

    for line in dashboard:
        print(line)
    print()


def main():
    """Run all dashboard examples."""
    print("=" * 80)
    print(" " * 25 + "CI/CD DASHBOARD EXAMPLES")
    print("=" * 80)

    create_cicd_dashboard()
    create_success_dashboard()
    create_monitoring_dashboard()

    print("=" * 80)


if __name__ == "__main__":
    main()
