#!/usr/bin/env python3
"""
Dashboard Preset Demo

Demonstrates the usage of the dashboard preset for creating grid-based layouts.
"""

from styledconsole import EMOJI, Console
from styledconsole.presets import DashboardWidget, dashboard


def main():
    console = Console()
    console.clear()

    # Define widgets
    widgets: list[DashboardWidget] = [
        {
            "title": f"{EMOJI.CHART_INCREASING} System Load",
            "content": "CPU: 45%\nMemory: 2.4GB\nDisk: 85%",
        },
        {
            "title": f"{EMOJI.GLOBE_WITH_MERIDIANS} Network",
            "content": "In: 1.2 MB/s\nOut: 0.4 MB/s\nActive Connections: 124",
        },
        {
            "title": f"{EMOJI.WARNING} Alerts",
            "content": f"{EMOJI.WARNING} High Latency (us-east-1)\n"
            f"{EMOJI.CHECK} Database Backup Complete",
        },
        {
            "title": f"{EMOJI.CALENDAR} Schedule",
            "content": "12:00 - Deployment\n14:30 - Team Sync\n16:00 - Code Review",
        },
    ]

    # Render dashboard
    dashboard(
        title=f"{EMOJI.ROCKET} Mission Control Center", widgets=widgets, columns=2, console=console
    )

    console.newline(2)

    # 3-column layout
    widgets_3col: list[DashboardWidget] = [
        {"title": "Service A", "content": "Status: OK"},
        {"title": "Service B", "content": "Status: OK"},
        {"title": "Service C", "content": "Status: Degraded"},
    ]

    dashboard(title="Microservices Status", widgets=widgets_3col, columns=3, console=console)


if __name__ == "__main__":
    main()
