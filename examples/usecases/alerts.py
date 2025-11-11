#!/usr/bin/env python3
"""
Alert Messages - Use Case Example

Real-world scenario: Displaying success, error, warning, and info alerts
in CLI applications (deployment scripts, build tools, system monitors).

This example shows best practices for:
- Consistent visual language (colors + emojis)
- Appropriate styling for message severity
- Clear, scannable alert formats
- Professional CLI output

Use cases:
- CI/CD pipeline status messages
- Deployment success/failure notifications
- System health warnings
- User action confirmations
"""

from styledconsole import EMOJI, Console

# Initialize console
console = Console()


def main():
    """Demonstrate alert message patterns."""

    print()
    print("=" * 80)
    print(f"{EMOJI.SIREN} ALERT MESSAGES - Real-World Use Cases")
    print("=" * 80)
    print()

    # ============================================================================
    # SUCCESS ALERTS - Green theme, checkmark emoji
    # ============================================================================

    console.text(f"{EMOJI.CHECK} SUCCESS ALERTS", color="lime", bold=True)
    console.text(
        "Use for: Completed operations, successful deployments, passed tests",
        color="gray",
    )
    print()

    # Simple success
    console.frame(
        "Application deployed successfully to production!",
        title=f"{EMOJI.CHECK} Deployment Complete",
        border="rounded",
        border_color="lime",
        content_color="lightgreen",
        width=70,
        align="left",
    )
    print()

    # Success with details
    console.frame(
        [
            "Build completed successfully",
            "",
            "Duration: 3m 42s",
            "Artifacts: 12 files (4.2 MB)",
            "Environment: production",
        ],
        title=f"{EMOJI.CHECK} Build Success",
        border="double",
        border_color="green",
        content_color="white",
        width=60,
        align="left",
    )
    print()
    print()

    # ============================================================================
    # ERROR ALERTS - Red theme, X emoji
    # ============================================================================

    console.text(f"{EMOJI.CROSS} ERROR ALERTS", color="red", bold=True)
    console.text(
        "Use for: Failed operations, critical errors, deployment failures",
        color="gray",
    )
    print()

    # Simple error
    console.frame(
        "Database connection failed!",
        title=f"{EMOJI.CROSS} Connection Error",
        border="heavy",
        border_color="red",
        content_color="lightcoral",
        width=70,
        align="left",
    )
    print()

    # Error with stack trace preview
    console.frame(
        [
            "Failed to deploy application",
            "",
            "Error: Permission denied",
            "File: /var/www/app/config.yml",
            "Action: Check deployment credentials",
        ],
        title=f"{EMOJI.CROSS} Deployment Failed",
        border="double",
        border_color="darkred",
        content_color="white",
        width=60,
        align="left",
    )
    print()
    print()

    # ============================================================================
    # WARNING ALERTS - Yellow theme, warning emoji
    # ============================================================================

    console.text(f"{EMOJI.WARNING}  WARNING ALERTS", color="yellow", bold=True)
    console.text("Use for: Non-critical issues, deprecation notices, resource limits", color="gray")
    print()

    # Simple warning
    console.frame(
        "API rate limit approaching: 980/1000 requests",
        title=f"{EMOJI.WARNING}  Rate Limit Warning",
        border="rounded",
        border_color="yellow",
        content_color="khaki",
        width=70,
        align="left",
    )
    print()

    # Warning with action items
    console.frame(
        [
            "Memory usage is high",
            "",
            "Current: 7.2 GB / 8.0 GB (90%)",
            "Recommendation: Restart workers or scale up",
            "Auto-scaling: Enabled",
        ],
        title=f"{EMOJI.WARNING}  Resource Warning",
        border="heavy",
        border_color="orange",
        content_color="white",
        width=60,
        align="left",
    )
    print()
    print()

    # ============================================================================
    # INFO ALERTS - Blue theme, info emoji
    # ============================================================================

    console.text(f"{EMOJI.INFO}  INFO ALERTS", color="dodgerblue", bold=True)
    console.text(
        "Use for: Status updates, informational messages, progress notifications", color="gray"
    )
    print()

    # Simple info
    console.frame(
        "Health check passed for all services",
        title=f"{EMOJI.INFO}  System Status",
        border="rounded",
        border_color="dodgerblue",
        content_color="lightblue",
        width=70,
        align="left",
    )
    print()

    # Info with metrics
    console.frame(
        [
            "Daily backup completed",
            "",
            "Files backed up: 1,247",
            "Total size: 12.8 GB",
            "Next backup: Tomorrow 02:00 AM",
        ],
        title=f"{EMOJI.INFO}  Backup Status",
        border="double",
        border_color="steelblue",
        content_color="white",
        width=60,
        align="left",
    )
    print()
    print()

    # ============================================================================
    # REAL-WORLD EXAMPLE: Deployment Sequence
    # ============================================================================

    console.text(
        f"{EMOJI.ROCKET} REAL-WORLD SEQUENCE: Deployment Workflow", color="cyan", bold=True
    )
    print()

    # Starting
    console.frame(
        "Starting deployment to production...",
        title=f"{EMOJI.INFO}  Deploy Started",
        border="rounded",
        border_color="dodgerblue",
        content_color="lightblue",
        width=70,
    )
    print()

    # Warning during deployment
    console.frame(
        "Detected 3 outdated dependencies. Consider upgrading after deployment.",
        title=f"{EMOJI.WARNING}  Dependencies Notice",
        border="rounded",
        border_color="yellow",
        content_color="khaki",
        width=70,
    )
    print()

    # Success completion
    console.frame(
        [
            "Deployment completed successfully!",
            "",
            "Version: v2.4.1",
            "Instances: 8 updated",
            "Health checks: All passing",
            "",
            f"{EMOJI.GLOBE} https://app.example.com",
        ],
        title=f"{EMOJI.CHECK} Deployment Complete",
        border="double",
        border_color="lime",
        content_color="white",
        width=70,
    )
    print()
    print()

    # ============================================================================
    # DESIGN GUIDELINES
    # ============================================================================

    console.text(f"{EMOJI.TRIANGLE_RULER} DESIGN GUIDELINES", color="magenta", bold=True)
    print()

    console.frame(
        [
            "Best Practices for Alert Messages:",
            "",
            "✅ Use consistent emoji + color combinations",
            "✅ Keep messages concise and actionable",
            "✅ Include context (what, why, next steps)",
            "✅ Match severity with visual weight",
            "✅ Align left for readability",
            "",
            "❌ Don't mix visual themes",
            "❌ Don't overuse heavy borders (reserve for errors)",
            "❌ Don't center-align long messages",
        ],
        title="Guidelines",
        border="minimal",
        border_color="gray",
        content_color="white",
        width=70,
        align="left",
    )
    print()


if __name__ == "__main__":
    main()
