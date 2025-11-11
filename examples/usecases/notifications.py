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

from styledconsole import Console
from styledconsole.emojis import EMOJI

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
console.rule(f"{EMOJI.INFO} INFORMATIONAL MESSAGES", style="cyan")
console.text("Use for: General updates, non-urgent information, status changes")
console.newline()

console.frame(
    """System backup completed successfully

Backed up: 2,847 files (4.2 GB)
Duration: 3m 42s
Next backup: Tomorrow at 2:00 AM""",
    title=f"{EMOJI.INFO} Backup Complete",
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
    title=f"{EMOJI.PACKAGE} Package Updates",
    border="solid",
    border_color="cyan",
    width=65,
)

# ----------------------------------------------------------------------------
# 2. SUCCESS NOTIFICATIONS - Completed Actions
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{EMOJI.CHECK} SUCCESS CONFIRMATIONS", style="green")
console.text("Use for: Successful operations, confirmations, achievements")
console.newline()

console.frame(
    f"""{EMOJI.ROCKET} Service restarted successfully

Service: nginx
PID: 12847
Status: Active (running)
Memory: 45.2 MB
Uptime: 2 seconds""",
    title=f"{EMOJI.CHECK} Service Status",
    border="rounded",
    border_color="green",
    width=65,
)

console.newline()

console.frame(
    f"""{EMOJI.BOOKS} Documentation updated

Files modified: 12
New pages: 3
Build time: 2.8s

View at: https://docs.example.com""",
    title=f"{EMOJI.CHECK} Build Complete",
    border="double",
    border_color="green",
    width=65,
)

# ----------------------------------------------------------------------------
# 3. WARNING NOTIFICATIONS - Attention Required
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{EMOJI.WARNING} WARNING MESSAGES", style="yellow")
console.text("Use for: Issues that need attention, deprecations, resource limits")
console.newline()

console.frame(
    f"""{EMOJI.YELLOW_CIRCLE} Disk space running low

Partition: /dev/sda1 (/)
Used: 42.8 GB / 50.0 GB (85.6%)
Available: 7.2 GB

Action: Clean up old files or expand storage""",
    title=f"{EMOJI.WARNING} Disk Space Warning",
    border="thick",
    border_color="yellow",
    width=65,
)

console.newline()

console.frame(
    f"""{EMOJI.CLOCK} Certificate expiring soon

Certificate: example.com
Expires: 2025-11-25 (14 days)
Issuer: Let's Encrypt

Action: Run 'certbot renew' to update""",
    title=f"{EMOJI.WARNING} SSL Certificate",
    border="solid",
    border_color="yellow",
    width=65,
)

# ----------------------------------------------------------------------------
# 4. CRITICAL NOTIFICATIONS - Immediate Action Required
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{EMOJI.SIREN} CRITICAL ALERTS", style="red")
console.text("Use for: Critical errors, security issues, service outages")
console.newline()

console.frame(
    f"""{EMOJI.RED_CIRCLE} Service failure detected

Service: postgresql
Status: Failed (exit code 1)
Last log: Connection refused
Attempts: 3 (all failed)

Action: Check logs at /var/log/postgresql/""",
    title=f"{EMOJI.CROSS} Critical Failure",
    border="double",
    border_color="red",
    width=65,
)

console.newline()

console.frame(
    f"""{EMOJI.LOCK} Security vulnerability detected

Package: openssl
Version: 1.1.1k
CVE: CVE-2023-12345 (CRITICAL)
CVSS Score: 9.8

Action: Update immediately with 'apt upgrade openssl'""",
    title=f"{EMOJI.SIREN} Security Alert",
    border="thick",
    border_color="red",
    width=65,
)

# ----------------------------------------------------------------------------
# 5. PROGRESS NOTIFICATIONS - Background Tasks
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{EMOJI.HOURGLASS} PROGRESS UPDATES", style="blue")
console.text("Use for: Long-running tasks, batch operations, downloads")
console.newline()

console.frame(
    f"""{EMOJI.GEAR} Processing batch job...

Task: Video encoding
Files: 45 / 120 (37.5%)
Current: vacation_2024.mp4
Speed: 2.3x realtime
ETA: 18 minutes""",
    title=f"{EMOJI.HOURGLASS} Background Task",
    border="rounded",
    border_color="blue",
    width=65,
)

console.newline()

console.frame(
    f"""{EMOJI.GLOBE} Downloading updates...

Package: system-update-2024.11
Size: 847 MB / 1.2 GB (70.6%)
Speed: 15.3 MB/s
Time remaining: ~23 seconds""",
    title=f"{EMOJI.PACKAGE} Update Manager",
    border="solid",
    border_color="blue",
    width=65,
)

# ----------------------------------------------------------------------------
# 6. TIME-SENSITIVE NOTIFICATIONS
# ----------------------------------------------------------------------------
console.newline(2)
console.rule(f"{EMOJI.ALARM} TIME-SENSITIVE ALERTS", style="magenta")
console.text("Use for: Scheduled events, reminders, deadlines")
console.newline()

console.frame(
    f"""{EMOJI.CALENDAR} Scheduled maintenance

Service: Database backup
Starts: Tonight at 2:00 AM
Duration: ~15 minutes
Impact: Read-only mode

Prepare: Save work, expect brief downtime""",
    title=f"{EMOJI.CLOCK} Upcoming Maintenance",
    border="rounded",
    border_color="magenta",
    width=65,
)

console.newline()

console.frame(
    f"""{EMOJI.BELL} Daily report ready

Report: System Health Summary
Date: 2025-11-11
Status: {EMOJI.CHECK} All systems operational

View at: /var/reports/daily/2025-11-11.html""",
    title=f"{EMOJI.MEMO} Daily Report",
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
{EMOJI.TARGET} DESIGN PRINCIPLES

1. VISUAL HIERARCHY
   • Critical: Red, double border, {EMOJI.SIREN}/{EMOJI.CROSS}
   • Warning: Yellow, thick border, {EMOJI.WARNING}
   • Success: Green, rounded, {EMOJI.CHECK}
   • Info: Cyan/blue, rounded, {EMOJI.INFO}

2. ACTIONABLE INFORMATION
   • Always include: What happened, why it matters
   • Critical alerts: Include action steps
   • Time-sensitive: Show deadlines/ETAs

3. EMOJI USAGE
   • Status: {EMOJI.CHECK} {EMOJI.WARNING} {EMOJI.CROSS} {EMOJI.INFO}
   • Priority: {EMOJI.RED_CIRCLE} {EMOJI.YELLOW_CIRCLE} {EMOJI.GREEN_CIRCLE}
   • Context: {EMOJI.LOCK} {EMOJI.GEAR} {EMOJI.PACKAGE} {EMOJI.CLOCK}

4. CONSISTENCY
   • Same colors for same priorities
   • Same borders for same urgency
   • Same emojis for same types
""",
    title=f"{EMOJI.LIGHTBULB} Best Practices",
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

{EMOJI.INFO} INFO          Blue/Cyan, rounded    General updates
{EMOJI.CHECK} SUCCESS       Green, rounded        Confirmations
{EMOJI.WARNING} WARNING       Yellow, thick         Attention needed
{EMOJI.SIREN} CRITICAL      Red, double           Immediate action
{EMOJI.HOURGLASS} PROGRESS       Blue, rounded         Background tasks
{EMOJI.CLOCK} TIME-SENSITIVE Magenta, rounded      Scheduled events

WHEN TO USE:
• Info: Package updates, backups, status changes
• Success: Service restarts, deployments, builds
• Warning: Resource limits, deprecations, expiring certs
• Critical: Service failures, security issues, data loss
• Progress: Downloads, batch jobs, migrations
• Time-sensitive: Scheduled maintenance, reports, deadlines
""",
    title=f"{EMOJI.BOOKMARK} Quick Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{EMOJI.SPARKLES} Notifications keep users informed without overwhelming them!")
