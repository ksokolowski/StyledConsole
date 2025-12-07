#!/usr/bin/env python3
"""
Use Case: System Notifications

Real-world notification patterns for CLI applications, system monitors,
and background processes. Demonstrates priority levels, time-sensitive
alerts, and different notification styles.

Use cases:
- System monitoring alerts
- Background task notifications
- Package manager updates
- Security alerts
- Service status changes
"""

from styledconsole import Console, icons

console = Console()

# ============================================================================
# NOTIFICATION PATTERNS
# ============================================================================

console.banner("SYSTEM NOTIFICATIONS")
console.text("Different notification styles for different scenarios")
console.newline()

# ----------------------------------------------------------------------------
# 1. INFO NOTIFICATIONS - General Information
# ----------------------------------------------------------------------------
console.rule(f"{icons.INFORMATION} INFORMATIONAL MESSAGES", style="cyan")
console.text("Use for: General updates, non-urgent information, status changes")
console.newline()

console.frame(
    """System backup completed successfully

Backed up: 2,847 files (4.2 GB)
Duration: 3m 42s
Next backup: Tomorrow at 2:00 AM""",
    title=f"{icons.INFORMATION} Backup Complete",
    border="rounded",
    border_color="cyan",
    width=65,
)

console.newline()

console.frame(
    """New package updates available:
  • python-requests (2.31.0 → 2.32.0)
  • numpy (1.24.3 → 1.25.0)
  • pandas (2.0.1 → 2.0.3)

Run 'sudo apt upgrade' to install updates""",
    title=f"{icons.PACKAGE} Package Updates",
    border="solid",
    border_color="cyan",
    width=65,
)

# ----------------------------------------------------------------------------
# 2. SUCCESS NOTIFICATIONS - Completed Actions
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{icons.CHECK_MARK_BUTTON} SUCCESS CONFIRMATIONS", style="green")
console.text("Use for: Successful operations, confirmations, achievements")
console.newline()

console.frame(
    f"""{icons.ROCKET} Service restarted successfully

Service: nginx
PID: 12847
Status: Active (running)
Memory: 45.2 MB
Uptime: 2 seconds""",
    title=f"{icons.CHECK_MARK_BUTTON} Service Status",
    border="rounded",
    border_color="green",
    width=65,
)

console.newline()

console.frame(
    f"""{icons.BOOKS} Documentation updated

Files modified: 12
New pages: 3
Build time: 2.8s

View at: https://docs.example.com""",
    title=f"{icons.CHECK_MARK_BUTTON} Build Complete",
    border="double",
    border_color="green",
    width=65,
)

# ----------------------------------------------------------------------------
# 3. WARNING NOTIFICATIONS - Attention Required
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{icons.WARNING} WARNING MESSAGES", style="yellow")
console.text("Use for: Issues that need attention, deprecations, resource limits")
console.newline()

console.frame(
    f"""{icons.YELLOW_CIRCLE} Disk space running low

Partition: /dev/sda1 (/)
Used: 42.8 GB / 50.0 GB (85.6%)
Available: 7.2 GB

Action: Clean up old files or expand storage""",
    title=f"{icons.WARNING} Disk Space Warning",
    border="thick",
    border_color="yellow",
    width=65,
)

console.newline()

console.frame(
    f"""{icons.ONE_OCLOCK} Certificate expiring soon

Certificate: example.com
Expires: 2025-11-25 (14 days)
Issuer: Let's Encrypt

Action: Run 'certbot renew' to update""",
    title=f"{icons.WARNING} SSL Certificate",
    border="solid",
    border_color="yellow",
    width=65,
)

# ----------------------------------------------------------------------------
# 4. CRITICAL NOTIFICATIONS - Immediate Action Required
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{icons.POLICE_CAR_LIGHT} CRITICAL ALERTS", style="red")
console.text("Use for: Critical errors, security issues, service outages")
console.newline()

console.frame(
    f"""{icons.RED_CIRCLE} Service failure detected

Service: postgresql
Status: Failed (exit code 1)
Last log: Connection refused
Attempts: 3 (all failed)

Action: Check logs at /var/log/postgresql/""",
    title=f"{icons.CROSS_MARK} Critical Failure",
    border="double",
    border_color="red",
    width=65,
)

console.newline()

console.frame(
    f"""{icons.LOCKED} Security vulnerability detected

Package: openssl
Version: 1.1.1k
CVE: CVE-2023-12345 (CRITICAL)
CVSS Score: 9.8

Action: Update immediately with 'apt upgrade openssl'""",
    title=f"{icons.POLICE_CAR_LIGHT} Security Alert",
    border="thick",
    border_color="red",
    width=65,
)

# ----------------------------------------------------------------------------
# 5. PROGRESS NOTIFICATIONS - Background Tasks
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{icons.HOURGLASS_DONE} PROGRESS UPDATES", style="blue")
console.text("Use for: Long-running tasks, batch operations, downloads")
console.newline()

console.frame(
    f"""{icons.GEAR} Processing batch job...

Task: Video encoding
Files: 45 / 120 (37.5%)
Current: vacation_2024.mp4
Speed: 2.3x realtime
ETA: 18 minutes""",
    title=f"{icons.HOURGLASS_DONE} Background Task",
    border="rounded",
    border_color="blue",
    width=65,
)

console.newline()

console.frame(
    f"""{icons.GLOBE_WITH_MERIDIANS} Downloading updates...

Package: system-update-2024.11
Size: 847 MB / 1.2 GB (70.6%)
Speed: 15.3 MB/s
Time remaining: ~23 seconds""",
    title=f"{icons.PACKAGE} Update Manager",
    border="solid",
    border_color="blue",
    width=65,
)

# ----------------------------------------------------------------------------
# 6. TIME-SENSITIVE NOTIFICATIONS
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{icons.ALARM_CLOCK} TIME-SENSITIVE ALERTS", style="magenta")
console.text("Use for: Scheduled events, reminders, deadlines")
console.newline()

console.frame(
    f"""{icons.CALENDAR} Scheduled maintenance

Service: Database backup
Starts: Tonight at 2:00 AM
Duration: ~15 minutes
Impact: Read-only mode

Prepare: Save work, expect brief downtime""",
    title=f"{icons.ONE_OCLOCK} Upcoming Maintenance",
    border="rounded",
    border_color="magenta",
    width=65,
)

console.newline()

console.frame(
    f"""{icons.BELL} Daily report ready

Report: System Health Summary
Date: 2025-11-11
Status: {icons.CHECK_MARK_BUTTON} All systems operational

View at: /var/reports/daily/2025-11-11.html""",
    title=f"{icons.MEMO} Daily Report",
    border="solid",
    border_color="magenta",
    width=65,
)

# ============================================================================
# DESIGN GUIDELINES
# ============================================================================

console.newline(2)
console.banner("NOTIFICATION DESIGN")

console.frame(
    f"""
{icons.BULLSEYE} DESIGN PRINCIPLES

1. VISUAL HIERARCHY
   • Critical: Red, double border, {icons.POLICE_CAR_LIGHT}/{icons.CROSS_MARK}
   • Warning: Yellow, thick border, {icons.WARNING}
   • Success: Green, rounded, {icons.CHECK_MARK_BUTTON}
   • Info: Cyan/blue, rounded, {icons.INFORMATION}

2. ACTIONABLE INFORMATION
   • Always include: What happened, why it matters
   • Critical alerts: Include action steps
   • Time-sensitive: Show deadlines/ETAs

3. EMOJI USAGE
   • Status: {icons.CHECK_MARK_BUTTON} {icons.WARNING} {icons.CROSS_MARK} {icons.INFORMATION}
   • Priority: {icons.RED_CIRCLE} {icons.YELLOW_CIRCLE} {icons.GREEN_CIRCLE}
   • Context: {icons.LOCKED} {icons.GEAR} {icons.PACKAGE} {icons.ONE_OCLOCK}

4. CONSISTENCY
   • Same colors for same priorities
   • Same borders for same urgency
   • Same emojis for same types
""",
    title=f"{icons.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# NOTIFICATION PATTERNS SUMMARY
# ============================================================================

console.frame(
    f"""
PRIORITY LEVELS:

{icons.INFORMATION} INFO          Blue/Cyan, rounded    General updates
{icons.CHECK_MARK_BUTTON} SUCCESS       Green, rounded        Confirmations
{icons.WARNING} WARNING       Yellow, thick         Attention needed
{icons.POLICE_CAR_LIGHT} CRITICAL      Red, double           Immediate action
{icons.HOURGLASS_DONE} PROGRESS       Blue, rounded         Background tasks
{icons.ONE_OCLOCK} TIME-SENSITIVE Magenta, rounded      Scheduled events

WHEN TO USE:
• Info: Package updates, backups, status changes
• Success: Service restarts, deployments, builds
• Warning: Resource limits, deprecations, expiring certs
• Critical: Service failures, security issues, data loss
• Progress: Downloads, batch jobs, migrations
• Time-sensitive: Scheduled maintenance, reports, deadlines
""",
    title=f"{icons.BOOKMARK} Quick Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{icons.SPARKLES} Notifications keep users informed without overwhelming them!")
