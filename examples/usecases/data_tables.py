#!/usr/bin/env python3
"""
Use Case: Data Tables

Real-world data display patterns for metrics, reports, and structured
information. Shows how to present tabular data clearly with proper
alignment, formatting, and visual hierarchy.

Use cases:
- System metrics tables
- Performance reports
- Configuration displays
- User data listings
- Financial reports
"""

from styledconsole import Console
from styledconsole.emojis import EMOJI

console = Console()

# ============================================================================
# SYSTEM METRICS TABLE
# ============================================================================

console.banner("DATA TABLES & METRICS")
console.text("Structured data display patterns")
console.newline()

console.frame(
    f"""
METRIC                    CURRENT      TARGET       STATUS
──────────────────────────────────────────────────────────────
Response Time (p95)       127 ms       < 200 ms     {EMOJI.CHECK_MARK_BUTTON} OK
Response Time (p99)       342 ms       < 500 ms     {EMOJI.CHECK_MARK_BUTTON} OK
Error Rate                0.03%        < 0.1%       {EMOJI.CHECK_MARK_BUTTON} OK
Throughput                2,847/s      > 1,000/s    {EMOJI.CHECK_MARK_BUTTON} OK
CPU Usage                 34.2%        < 80%        {EMOJI.CHECK_MARK_BUTTON} OK
Memory Usage              12.8 GB      < 28 GB      {EMOJI.CHECK_MARK_BUTTON} OK
Disk Usage                68.4%        < 90%        {EMOJI.CHECK_MARK_BUTTON} OK
Active Connections        847          < 10,000     {EMOJI.CHECK_MARK_BUTTON} OK
""",
    title=f"{EMOJI.BAR_CHART} Performance Metrics",
    border="rounded",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# SERVER INVENTORY
# ============================================================================

console.rule(f"{EMOJI.LAPTOP} INFRASTRUCTURE INVENTORY", style="cyan")
console.newline()

console.frame(
    f"""
SERVER           IP ADDRESS       CPU    MEMORY      UPTIME        STATUS
────────────────────────────────────────────────────────────────────────
prod-web-01      10.0.1.15        23%    12.8 GB     45d 8h        {EMOJI.GREEN_CIRCLE} UP
prod-web-02      10.0.1.16        28%    15.2 GB     45d 8h        {EMOJI.GREEN_CIRCLE} UP
prod-web-03      10.0.1.17        19%    11.4 GB     12d 3h        {EMOJI.GREEN_CIRCLE} UP
prod-api-01      10.0.2.10        45%    24.6 GB     45d 8h        {EMOJI.GREEN_CIRCLE} UP
prod-api-02      10.0.2.11        52%    28.3 GB     45d 8h        {EMOJI.GREEN_CIRCLE} UP
prod-db-01       10.0.3.20        34%    52.4 GB     123d 14h      {EMOJI.GREEN_CIRCLE} UP
prod-cache-01    10.0.4.30        12%    8.2 GB      45d 8h        {EMOJI.GREEN_CIRCLE} UP
staging-web-01   10.0.5.40        8%     4.2 GB      2d 6h         {EMOJI.GREEN_CIRCLE} UP
""",
    title=f"{EMOJI.FILE_CABINET} Server Inventory",
    border="solid",
    border_color="cyan",
    width=85,
)

console.newline()

# ============================================================================
# USER STATISTICS
# ============================================================================

console.rule(f"{EMOJI.BUSTS_IN_SILHOUETTE} USER STATISTICS", style="magenta")
console.newline()

console.frame(
    """
PERIOD          ACTIVE USERS    NEW SIGNUPS    CHURN RATE    REVENUE
───────────────────────────────────────────────────────────────────────
Today           12,847          423            0.8%          $23,456
Yesterday       11,234          387            1.2%          $19,234
This Week       45,678          2,134          0.9%          $145,234
Last Week       43,234          1,987          1.1%          $138,765
This Month      187,456         8,234          1.0%          $567,890
Last Month      175,234         7,456          1.3%          $534,567
""",
    title=f"{EMOJI.CHART_INCREASING} User Growth Metrics",
    border="rounded",
    border_color="magenta",
    width=80,
)

console.newline()

# ============================================================================
# KEY-VALUE CONFIGURATION
# ============================================================================

console.rule(f"{EMOJI.GEAR} CONFIGURATION DISPLAY", style="blue")
console.newline()

console.frame(
    f"""
APPLICATION CONFIGURATION
─────────────────────────────────────────────────────────────

Environment               production
Version                   v2.3.1
Build Date                2025-11-08 14:23:15
Commit Hash               a7f3e92

{EMOJI.LAPTOP} Server Settings
  Host                    0.0.0.0
  Port                    3000
  Workers                 8
  Timeout                 30s
  Max Connections         10,000

{EMOJI.FLOPPY_DISK} Database
  Host                    prod-db-01.internal
  Port                    5432
  Database                myapp_production
  Pool Size               20
  Connection Timeout      5s

{EMOJI.CARD_FILE_BOX} Cache
  Type                    Redis
  Host                    prod-cache-01.internal
  Port                    6379
  TTL                     3600s
  Max Memory              2 GB

{EMOJI.LOCKED} Security
  HTTPS Enabled           Yes
  TLS Version             1.3
  Certificate Expiry      2026-03-15
  Session Timeout         1800s
""",
    title=f"{EMOJI.MEMO} System Configuration",
    border="double",
    border_color="blue",
    width=75,
)

console.newline()

# ============================================================================
# API ENDPOINTS
# ============================================================================

console.rule(f"{EMOJI.GLOBE_WITH_MERIDIANS} API ENDPOINTS", style="green")
console.newline()

console.frame(
    f"""
ENDPOINT                 METHOD    AVG TIME    CALLS/MIN    ERROR RATE
─────────────────────────────────────────────────────────────────────────
/api/users               GET       23 ms       2,847        0.01%  {EMOJI.CHECK_MARK_BUTTON}
/api/users/:id           GET       12 ms       4,234        0.02%  {EMOJI.CHECK_MARK_BUTTON}
/api/users               POST      87 ms       234          0.05%  {EMOJI.CHECK_MARK_BUTTON}
/api/products            GET       45 ms       3,456        0.03%  {EMOJI.CHECK_MARK_BUTTON}
/api/orders              POST      234 ms      567          0.12%  {EMOJI.WARNING}
/api/payments            POST      1,234 ms    123          0.08%  {EMOJI.CHECK_MARK_BUTTON}
/api/analytics           GET       567 ms      89           0.00%  {EMOJI.CHECK_MARK_BUTTON}
/api/reports             GET       2,345 ms    12           0.00%  {EMOJI.CHECK_MARK_BUTTON}
""",
    title=f"{EMOJI.BAR_CHART} API Performance",
    border="solid",
    border_color="green",
    width=85,
)

console.newline()

# ============================================================================
# FINANCIAL REPORT
# ============================================================================

console.rule(f"{EMOJI.DOLLAR_BANKNOTE} FINANCIAL DATA", style="yellow")
console.newline()

console.frame(
    f"""
REVENUE BREAKDOWN (November 2025)
─────────────────────────────────────────────────────────────

CATEGORY             AMOUNT          %         CHANGE
─────────────────────────────────────────────────────────────
Subscriptions        $234,567        41.3%     {EMOJI.CHART_INCREASING} +12.3%
One-time Sales       $145,234        25.6%     {EMOJI.CHART_INCREASING} +5.7%
Premium Features     $89,456         15.7%     {EMOJI.CHART_INCREASING} +23.4%
Enterprise          $78,234         13.8%     {EMOJI.CHART_INCREASING} +8.9%
Partnerships        $19,876         3.5%      {EMOJI.CHART_DECREASING} -2.1%
Other               $678            0.1%      {EMOJI.CHART_INCREASING} +0.5%
─────────────────────────────────────────────────────────────
TOTAL               $568,045        100.0%    {EMOJI.CHART_INCREASING} +9.8%

{EMOJI.BAR_CHART} Month-over-Month Growth: +9.8%
{EMOJI.BULLSEYE} Target for November: $550,000 (103.3% achieved)
""",
    title=f"{EMOJI.MONEY_BAG} Monthly Revenue Report",
    border="thick",
    border_color="yellow",
    width=75,
)

console.newline()

# ============================================================================
# COMPARISON TABLE
# ============================================================================

console.rule(f"{EMOJI.TEST_TUBE} BENCHMARK COMPARISON", style="cyan")
console.newline()

console.frame(
    f"""
FRAMEWORK        REQUESTS/SEC    LATENCY    MEMORY    SCORE
─────────────────────────────────────────────────────────────
Express.js       12,847          23 ms      145 MB    {EMOJI.STAR * 4}
Fastify          18,234          15 ms      98 MB     {EMOJI.STAR * 5}
Koa              11,456          28 ms      132 MB    {EMOJI.STAR * 4}
Hapi             9,234           34 ms      178 MB    {EMOJI.STAR * 3}
Nest.js          8,456           42 ms      234 MB    {EMOJI.STAR}{EMOJI.STAR}{EMOJI.STAR}

{EMOJI.TROPHY} Winner: Fastify (highest throughput, lowest latency)
{EMOJI.BULLSEYE} Our choice: Express.js (good balance, mature ecosystem)
""",
    title=f"{EMOJI.BAR_CHART} Framework Benchmarks",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# DEPLOYMENT HISTORY
# ============================================================================

console.rule(f"{EMOJI.ROCKET} DEPLOYMENT HISTORY", style="blue")
console.newline()

console.frame(
    f"""
VERSION    DATE                 DEPLOYED BY    DURATION    STATUS
───────────────────────────────────────────────────────────────────────
v2.3.1     2025-11-11 14:23    alice          3m 42s      {EMOJI.CHECK_MARK_BUTTON} Success
v2.3.0     2025-11-08 10:15    bob            4m 18s      {EMOJI.CHECK_MARK_BUTTON} Success
v2.2.9     2025-11-05 16:45    alice          2m 54s      {EMOJI.CHECK_MARK_BUTTON} Success
v2.2.8     2025-11-03 09:30    charlie        5m 23s      {EMOJI.CHECK_MARK_BUTTON} Success
v2.2.7     2025-11-01 11:00    alice          3m 12s      {EMOJI.CROSS_MARK} Failed
v2.2.6     2025-10-29 14:20    bob            4m 05s      {EMOJI.CHECK_MARK_BUTTON} Success
v2.2.5     2025-10-25 08:45    alice          3m 38s      {EMOJI.CHECK_MARK_BUTTON} Success
""",
    title=f"{EMOJI.CALENDAR} Recent Deployments",
    border="solid",
    border_color="blue",
    width=80,
)

console.newline()

# ============================================================================
# ERROR LOG SUMMARY
# ============================================================================

console.rule(f"{EMOJI.CROSS_MARK} ERROR SUMMARY", style="red")
console.newline()

console.frame(
    f"""
ERROR TYPE                      COUNT      LAST SEEN           SEVERITY
─────────────────────────────────────────────────────────────────────────
Database Connection Timeout     23         3 minutes ago       {EMOJI.WARNING} Medium
API Rate Limit Exceeded         12         5 minutes ago       {EMOJI.INFORMATION} Low
Invalid User Input              8          1 minute ago        {EMOJI.INFORMATION} Low
Memory Allocation Failed        3          15 minutes ago      {EMOJI.CROSS_MARK} High
File Not Found                  2          30 minutes ago      {EMOJI.INFORMATION} Low
Authentication Failed           47         < 1 minute ago      {EMOJI.WARNING} Medium
Network Unreachable             1          2 hours ago         {EMOJI.CROSS_MARK} High
─────────────────────────────────────────────────────────────────────────
TOTAL ERRORS (Last Hour)        96
TOTAL WARNINGS                  82
TOTAL INFO                      57

{EMOJI.CHART_DECREASING} Trend: Errors decreased 12% compared to last hour
{EMOJI.BELL} Alerts triggered: 2 (Memory, Network)
""",
    title=f"{EMOJI.POLICE_CAR_LIGHT} Error Log Analysis",
    border="double",
    border_color="red",
    width=85,
)

console.newline()

# ============================================================================
# DESIGN GUIDELINES
# ============================================================================

console.banner("DATA TABLE DESIGN")

console.frame(
    f"""
{EMOJI.BULLSEYE} TABLE DESIGN PRINCIPLES

1. ALIGNMENT & FORMATTING
   • Left-align: Text, labels, categories
   • Right-align: Numbers, metrics, percentages
   • Center: Status indicators, icons
   • Monospace: Better column alignment

2. VISUAL HIERARCHY
   • Headers: Clear separation (underline or spacing)
   • Groups: Blank lines between sections
   • Totals: Separator line, bold or highlight
   • Key rows: Use emojis or color

3. DATA PRESENTATION
   • Units: Include with values (ms, GB, %)
   • Precision: Match context (2 decimals for %, integers for counts)
   • Ranges: Use "< 200ms" or "12.8 GB / 32 GB"
   • Trends: Show arrows or % change

4. STATUS INDICATORS
   {EMOJI.CHECK_MARK_BUTTON} Success/OK: Green, met targets
   {EMOJI.WARNING} Warning: Yellow, attention needed
   {EMOJI.CROSS_MARK} Error/Critical: Red, immediate action
   {EMOJI.INFORMATION} Info: Blue, informational

5. TABLE WIDTH
   • Fit content: Don't force unnecessary width
   • Max readable: ~85 characters
   • Align columns: Fixed-width fonts help
   • Wrap long values: Or truncate with "..."
""",
    title=f"{EMOJI.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
TABLE TYPES & USE CASES:

{EMOJI.BAR_CHART} METRICS TABLE
  Metrics + Current + Target + Status
  Use: Performance monitoring, SLAs, health checks

{EMOJI.LAPTOP} INVENTORY TABLE
  Resources + Identifiers + Status + Metrics
  Use: Server lists, infrastructure, resources

{EMOJI.GEAR} CONFIGURATION TABLE
  Key-value pairs, nested sections
  Use: Settings, environment variables, config dumps

{EMOJI.CHART_INCREASING} COMPARISON TABLE
  Items + Multiple metrics + Ranking
  Use: Benchmarks, A/B tests, vendor selection

{EMOJI.CALENDAR} TIME-SERIES TABLE
  Period + Metrics over time + Trends
  Use: Reports, analytics, historical data

{EMOJI.CROSS_MARK} ERROR/LOG TABLE
  Error type + Count + Timestamp + Severity
  Use: Debugging, monitoring, incident analysis

FORMATTING TIPS:
• Separator lines: "───────" for visual breaks
• Column headers: ALL CAPS or bold equivalent
• Numeric precision: Match the context (0-2 decimals)
• Status emojis: End of row or dedicated column
""",
    title=f"{EMOJI.BOOKMARK} Quick Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{EMOJI.SPARKLES} Data tables make complex information scannable and actionable!")
