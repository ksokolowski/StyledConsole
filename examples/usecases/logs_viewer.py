#!/usr/bin/env python3
"""
Use Case: Log Viewer

Real-world log display patterns for application logs, system logs, and
monitoring. Shows how to present log entries clearly with severity levels,
timestamps, and structured information.

Use cases:
- Application log viewing
- System log monitoring
- Error tracking
- Audit trail display
- Debug output
"""

from styledconsole import Console
from styledconsole.emojis import EMOJI

console = Console()

# ============================================================================
# APPLICATION LOGS
# ============================================================================

console.banner("LOG VIEWER & MONITORING")
console.text("Structured log display patterns with severity levels")
console.newline()

console.frame(
    f"""
{EMOJI.INFORMATION} 2025-11-11 14:23:15.234  INFO     [HTTP] GET /api/users → 200 (23ms)
{EMOJI.INFORMATION} 2025-11-11 14:23:15.456  INFO     [HTTP] GET /api/products → 200 (45ms)
{EMOJI.CHECK_MARK_BUTTON} 2025-11-11 14:23:16.123  INFO     [AUTH] User login: alice@example.com
{EMOJI.INFORMATION} 2025-11-11 14:23:16.789  INFO     [DB] Query executed in 12ms
{EMOJI.WARNING} 2025-11-11 14:23:17.234  WARN     [CACHE] Cache miss for key: user:1234
{EMOJI.INFORMATION} 2025-11-11 14:23:17.567  INFO     [HTTP] POST /api/orders → 201 (234ms)
{EMOJI.CROSS_MARK} 2025-11-11 14:23:18.890  ERROR    [DB] Connection timeout after 5000ms
{EMOJI.INFORMATION} 2025-11-11 14:23:19.123  INFO     [DB] Reconnection successful
{EMOJI.INFORMATION} 2025-11-11 14:23:19.456  INFO     [HTTP] GET /api/analytics → 200 (567ms)
{EMOJI.CHECK_MARK_BUTTON} 2025-11-11 14:23:20.789  INFO     [AUTH] Session renewed: alice
""",
    title=f"{EMOJI.SCROLL} Application Logs (Last 10 entries)",
    border="rounded",
    border_color="cyan",
    width=90,
)

console.newline()

# ============================================================================
# SYSTEM LOGS
# ============================================================================

console.rule(f"{EMOJI.LAPTOP} SYSTEM LOGS", style="blue")
console.newline()

console.frame(
    f"""
{EMOJI.INFORMATION} Nov 11 14:20:15 prod-web-01 systemd[1]: Started nginx.service
{EMOJI.CHECK_MARK_BUTTON} Nov 11 14:20:16 prod-web-01 nginx: config test successful
{EMOJI.INFORMATION} Nov 11 14:20:16 prod-web-01 systemd[1]: Reloading nginx
{EMOJI.CHECK_MARK_BUTTON} Nov 11 14:20:17 prod-web-01 nginx: signal process started
{EMOJI.INFORMATION} Nov 11 14:21:34 prod-web-01 sshd[12847]: Accepted publickey for alice
{EMOJI.INFORMATION} Nov 11 14:22:15 prod-web-01 sudo: alice : /usr/bin/systemctl status nginx
{EMOJI.WARNING} Nov 11 14:23:42 prod-web-01 kernel: [12847.234] Out of memory
{EMOJI.CROSS_MARK} Nov 11 14:23:43 prod-web-01 systemd[1]: node-app.service: Main process exited
{EMOJI.WARNING} Nov 11 14:23:43 prod-web-01 systemd[1]: node-app.service: Failed with 'oom-kill'
{EMOJI.INFORMATION} Nov 11 14:23:44 prod-web-01 systemd[1]: node-app.service: Scheduled restart
{EMOJI.CHECK_MARK_BUTTON} Nov 11 14:23:45 prod-web-01 systemd[1]: Started node-app.service
""",
    title=f"{EMOJI.GEAR} System Logs (/var/log/syslog)",
    border="solid",
    border_color="blue",
    width=95,
)

console.newline()

# ============================================================================
# ERROR LOGS
# ============================================================================

console.rule(f"{EMOJI.CROSS_MARK} ERROR TRACKING", style="red")
console.newline()

console.frame(
    f"""
{EMOJI.CROSS_MARK} 2025-11-11 14:23:18.890  ERROR
  Component: Database
  Message: Connection timeout after 5000ms
  Query: SELECT * FROM users WHERE id = $1
  Parameters: [1234]
  Stack trace:
    at Database.query (/app/lib/database.js:234)
    at UserService.findById (/app/services/user.js:45)
    at UserController.getUser (/app/controllers/user.js:23)

{EMOJI.CROSS_MARK} 2025-11-11 14:25:32.123  ERROR
  Component: Payment Processing
  Message: Payment gateway returned 503
  Transaction ID: txn_1234567890
  Amount: $127.50
  Retry: 3/3 attempts failed
  Next action: Manual review required

{EMOJI.CROSS_MARK} 2025-11-11 14:27:45.678  ERROR
  Component: Email Service
  Message: SMTP connection failed
  Recipient: customer@example.com
  Template: order_confirmation
  Error code: ECONNREFUSED
  Action: Queued for retry in 5 minutes
""",
    title=f"{EMOJI.POLICE_CAR_LIGHT} Critical Errors (Last hour)",
    border="double",
    border_color="red",
    width=80,
)

console.newline()

# ============================================================================
# STRUCTURED LOGS (JSON-LIKE)
# ============================================================================

console.rule(f"{EMOJI.GEAR} STRUCTURED LOGGING", style="magenta")
console.newline()

console.frame(
    f"""
{EMOJI.INFORMATION} 2025-11-11 14:23:15.234
  level: info
  component: http
  method: GET
  path: /api/users
  status: 200
  duration: 23ms
  user_id: 1234
  request_id: req_abc123def456

{EMOJI.WARNING} 2025-11-11 14:23:17.234
  level: warn
  component: cache
  event: cache_miss
  key: user:1234
  ttl: 3600
  action: fetch_from_db
  duration: 12ms

{EMOJI.CROSS_MARK} 2025-11-11 14:23:18.890
  level: error
  component: database
  event: connection_timeout
  query: SELECT * FROM users WHERE id = $1
  timeout: 5000ms
  retry_count: 3
  last_error: ECONNREFUSED
""",
    title=f"{EMOJI.MEMO} Structured Log Format",
    border="rounded",
    border_color="magenta",
    width=80,
)

console.newline()

# ============================================================================
# AUDIT TRAIL
# ============================================================================

console.rule(f"{EMOJI.SCROLL} AUDIT LOGS", style="yellow")
console.newline()

console.frame(
    f"""
{EMOJI.CHECK_MARK_BUTTON} 2025-11-11 14:20:00  USER_LOGIN
  User: alice@example.com (ID: 1234)
  IP: 192.168.1.100
  Location: San Francisco, CA
  Device: Chrome 118.0 (macOS)
  Status: Success

{EMOJI.GEAR} 2025-11-11 14:21:15  CONFIG_CHANGE
  User: alice@example.com (ID: 1234)
  Action: Updated database pool size
  Old value: 20
  New value: 30
  Reason: Performance optimization

{EMOJI.CROSS_MARK} 2025-11-11 14:22:30  PERMISSION_DENIED
  User: bob@example.com (ID: 5678)
  Action: Attempted to delete user account
  Resource: User ID 9012
  Reason: Insufficient permissions (requires admin role)

{EMOJI.CHECK_MARK_BUTTON} 2025-11-11 14:23:45  DATA_EXPORT
  User: charlie@example.com (ID: 9012)
  Resource: Customer database
  Records: 12,847
  Format: CSV
  Size: 4.2 MB
  Compliance: GDPR approved
""",
    title=f"{EMOJI.LOCKED} Security Audit Trail",
    border="thick",
    border_color="yellow",
    width=85,
)

console.newline()

# ============================================================================
# DEBUG LOGS
# ============================================================================

console.rule(f"{EMOJI.TEST_TUBE} DEBUG OUTPUT", style="cyan")
console.newline()

console.frame(
    f"""
{EMOJI.GEAR} 2025-11-11 14:23:15.123  DEBUG    [UserService] findById called
{EMOJI.GEAR} 2025-11-11 14:23:15.125  DEBUG    [Database] Executing query
  SQL: SELECT * FROM users WHERE id = $1
  Params: [1234]
{EMOJI.GEAR} 2025-11-11 14:23:15.137  DEBUG    [Database] Query returned 1 row
{EMOJI.GEAR} 2025-11-11 14:23:15.139  DEBUG    [Cache] Storing result in cache
  Key: user:1234
  TTL: 3600s
{EMOJI.CHECK_MARK_BUTTON} 2025-11-11 14:23:15.142  DEBUG    [UserService] User found and cached
{EMOJI.GEAR} 2025-11-11 14:23:15.145  DEBUG    [HTTP] Building response
  Status: 200
  Body size: 847 bytes
{EMOJI.CHECK_MARK_BUTTON} 2025-11-11 14:23:15.148  DEBUG    [HTTP] Response sent successfully
  Total time: 25ms
""",
    title=f"{EMOJI.TEST_TUBE} Debug Log (Verbose Mode)",
    border="solid",
    border_color="cyan",
    width=85,
)

console.newline()

# ============================================================================
# LOG AGGREGATION VIEW
# ============================================================================

console.rule(f"{EMOJI.BAR_CHART} LOG STATISTICS", style="green")
console.newline()

console.frame(
    f"""
{EMOJI.BAR_CHART} Log Summary (Last hour)

SEVERITY BREAKDOWN:
  {EMOJI.CROSS_MARK} ERROR      23 entries    (1.2%)
  {EMOJI.WARNING} WARN       82 entries    (4.3%)
  {EMOJI.INFORMATION} INFO      1,847 entries (96.5%)
  {EMOJI.GEAR} DEBUG     12,234 entries (not shown by default)

TOP ERROR SOURCES:
  1. Database connection: 8 errors
  2. Payment gateway: 5 errors
  3. Email service: 4 errors
  4. Cache timeout: 3 errors
  5. API rate limit: 3 errors

TOP COMPONENTS:
  1. HTTP: 1,234 log entries
  2. Database: 423 log entries
  3. Authentication: 156 log entries
  4. Cache: 34 log entries

RESPONSE TIME TRENDS:
  Average: 127ms
  P95: 342ms
  P99: 1,234ms
  Max: 5,678ms (query timeout)
""",
    title=f"{EMOJI.CHART_INCREASING} Log Analytics",
    border="rounded",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# REAL-TIME LOG TAIL
# ============================================================================

console.rule(f"{EMOJI.FIRE} LIVE LOG STREAM", style="blue")
console.newline()

console.frame(
    f"""
{EMOJI.FIRE} Following /var/log/app/production.log...

{EMOJI.INFORMATION} 14:28:45.123  INFO   [HTTP] GET /api/users → 200 (23ms)
{EMOJI.INFORMATION} 14:28:45.456  INFO   [HTTP] GET /api/products → 200 (45ms)
{EMOJI.CHECK_MARK_BUTTON} 14:28:46.789  INFO   [AUTH] Token validated: user_1234
{EMOJI.INFORMATION} 14:28:47.012  INFO   [CACHE] Hit rate: 94.2%
{EMOJI.WARNING} 14:28:47.345  WARN   [DB] Slow query detected (2,345ms)
{EMOJI.INFORMATION} 14:28:48.678  INFO   [HTTP] POST /api/orders → 201 (234ms)
{EMOJI.INFORMATION} 14:28:49.901  INFO   [HTTP] GET /health → 200 (2ms)
{EMOJI.INFORMATION} 14:28:50.234  INFO   [SCHEDULER] Running background job
{EMOJI.CHECK_MARK_BUTTON} 14:28:51.567  INFO   [JOB] Processed 847 items in 1.2s
{EMOJI.INFORMATION} 14:28:52.890  INFO   [HTTP] GET /api/analytics → 200 (567ms)

{EMOJI.INFORMATION} Press Ctrl+C to stop following...
""",
    title=f"{EMOJI.SCROLL} Live Log Tail (tail -f production.log)",
    border="solid",
    border_color="blue",
    width=85,
)

console.newline()

# ============================================================================
# DESIGN GUIDELINES
# ============================================================================

console.banner("LOG DISPLAY DESIGN")

console.frame(
    f"""
{EMOJI.BULLSEYE} LOG VIEWER PRINCIPLES

1. SEVERITY HIERARCHY
   {EMOJI.CROSS_MARK} ERROR: Red, immediate attention required
   {EMOJI.WARNING} WARN: Yellow, should investigate
   {EMOJI.INFORMATION} INFO: Cyan/blue, normal operations
   {EMOJI.CHECK_MARK_BUTTON} SUCCESS: Green, positive confirmation
   {EMOJI.GEAR} DEBUG: Gray/dim, verbose details

2. TIMESTAMP FORMATTING
   • ISO 8601: 2025-11-11 14:23:15.234
   • Include milliseconds for debugging
   • Consistent width for alignment
   • Consider timezone (UTC recommended)

3. LOG STRUCTURE
   [Timestamp] [Level] [Component] Message
   • Timestamp: When it happened
   • Level: Severity (ERROR, WARN, INFO, DEBUG)
   • Component: What part of system (HTTP, DB, Cache)
   • Message: What happened

4. CONTEXT INFORMATION
   • Request IDs: Track related log entries
   • User IDs: Who triggered the action
   • Duration: How long operation took
   • Stack traces: For errors (indented)

5. READABILITY
   • Monospace fonts: Better alignment
   • Color coding: Severity at a glance
   • Truncate long values: Or wrap intelligently
   • Group related entries: Blank lines between requests
""",
    title=f"{EMOJI.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
LOG LEVEL GUIDELINES:

{EMOJI.CROSS_MARK} ERROR
  System failures, exceptions, data loss
  Requires immediate investigation
  Example: Database connection failed, API error

{EMOJI.WARNING} WARN
  Degraded performance, deprecated features, recoverable errors
  Should investigate but not urgent
  Example: Slow query, cache miss, retry succeeded

{EMOJI.INFORMATION} INFO
  Normal operations, state changes, milestones
  Standard operational logging
  Example: HTTP requests, service start/stop, user login

{EMOJI.CHECK_MARK_BUTTON} SUCCESS
  Explicitly successful operations
  Useful for auditing and confirmation
  Example: Deployment complete, backup successful

{EMOJI.GEAR} DEBUG
  Detailed diagnostics, variable values, call traces
  Only in development or troubleshooting
  Example: Function calls, query parameters

LOG FORMATS:

Simple:    [LEVEL] Message
Standard:  [Timestamp] [Level] [Component] Message
Detailed:  [Timestamp] [Level] [Component] [Request ID] Message
Structured: JSON with nested fields

USE IN:
• Application monitoring
• Error tracking and debugging
• Security audits
• Performance analysis
• Compliance and reporting
""",
    title=f"{EMOJI.BOOKMARK} Log Levels & Formats",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{EMOJI.SPARKLES} Clear log displays help diagnose issues quickly and accurately!")
