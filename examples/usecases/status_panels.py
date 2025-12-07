#!/usr/bin/env python3
"""
Use Case: Status Panels

Real-world status monitoring patterns for services, infrastructure, and
system health. Shows how to display service status, uptime, metrics, and
health indicators at a glance.

Use cases:
- Service health dashboards
- Infrastructure monitoring
- System resource usage
- Application health checks
- Uptime displays
"""

from styledconsole import Console, icons

console = Console()

# ============================================================================
# SERVICE HEALTH DASHBOARD
# ============================================================================

console.banner("SERVICE STATUS DASHBOARD")
console.text("Real-time service health monitoring")
console.newline()

console.frame(
    f"""
{icons.CHECK_MARK_BUTTON} Web Server (nginx)
  Status: Running | Uptime: 23d 14h 32m
  Requests/sec: 1,247 | CPU: 12.3% | Memory: 342 MB

{icons.CHECK_MARK_BUTTON} Application Server (Node.js)
  Status: Running | Uptime: 23d 14h 30m
  Active connections: 847 | CPU: 34.2% | Memory: 1.2 GB

{icons.CHECK_MARK_BUTTON} Database (PostgreSQL)
  Status: Running | Uptime: 45d 8h 15m
  Connections: 42/100 | CPU: 18.7% | Memory: 4.8 GB

{icons.CHECK_MARK_BUTTON} Cache (Redis)
  Status: Running | Uptime: 45d 8h 15m
  Hit rate: 94.2% | Memory: 847 MB / 2 GB

{icons.CHECK_MARK_BUTTON} Message Queue (RabbitMQ)
  Status: Running | Uptime: 23d 14h 28m
  Messages: 123 queued | Throughput: 456 msg/sec
""",
    title=f"{icons.GREEN_CIRCLE} All Services Healthy",
    border="rounded",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# DEGRADED SERVICE
# ============================================================================

console.rule(f"{icons.WARNING} DEGRADED PERFORMANCE", style="yellow")
console.newline()

console.frame(
    f"""
{icons.CHECK_MARK_BUTTON} Web Server (nginx)
  Status: Running | Uptime: 2d 8h 15m
  Requests/sec: 2,847 | CPU: 45.2% | Memory: 512 MB

{icons.WARNING} Application Server (Node.js)
  Status: Degraded | Uptime: 2d 8h 12m
  Response time: 2,847ms (normally 120ms)
  CPU: 89.3% {icons.FIRE} HIGH | Memory: 3.8 GB / 4 GB
  Active connections: 1,247 (normally 400)

{icons.CHECK_MARK_BUTTON} Database (PostgreSQL)
  Status: Running | Uptime: 45d 8h 15m
  Connections: 87/100 | CPU: 34.8% | Memory: 5.2 GB

{icons.CHECK_MARK_BUTTON} Cache (Redis)
  Status: Running | Uptime: 45d 8h 15m
  Hit rate: 87.4% | Memory: 1.2 GB / 2 GB
""",
    title=f"{icons.YELLOW_CIRCLE} Performance Degradation Detected",
    border="thick",
    border_color="yellow",
    width=75,
)

console.newline()

# ============================================================================
# SERVICE OUTAGE
# ============================================================================

console.rule(f"{icons.CROSS_MARK} SERVICE OUTAGE", style="red")
console.newline()

console.frame(
    f"""
{icons.CHECK_MARK_BUTTON} Web Server (nginx)
  Status: Running | Uptime: 12h 45m
  Requests/sec: 523 | CPU: 8.2% | Memory: 234 MB

{icons.CROSS_MARK} Application Server (Node.js)
  Status: Down | Last seen: 3m 42s ago
  Error: Connection refused (port 3000)
  Exit code: 137 (OOM killed)
  Restart attempts: 3/3 failed

{icons.WARNING} Database (PostgreSQL)
  Status: Degraded | Uptime: 45d 8h 15m
  Connections: 95/100 {icons.WARNING} HIGH
  Slow queries: 23 (> 5s each)

{icons.CHECK_MARK_BUTTON} Cache (Redis)
  Status: Running | Uptime: 45d 8h 15m
  Hit rate: 94.2% | Memory: 847 MB / 2 GB
""",
    title=f"{icons.RED_CIRCLE} Critical Service Failure",
    border="double",
    border_color="red",
    width=75,
)

console.newline()

# ============================================================================
# INFRASTRUCTURE HEALTH
# ============================================================================

console.rule(f"{icons.LAPTOP} INFRASTRUCTURE STATUS", style="cyan")
console.newline()

console.frame(
    f"""
{icons.LAPTOP} Server: prod-web-01 (10.0.1.15)
  Status: {icons.GREEN_CIRCLE} Healthy | Uptime: 45d 8h 15m
  CPU: 23.4% | Memory: 12.8 GB / 32 GB | Disk: 342 GB / 500 GB
  Network: 12.3 MB/s in, 45.7 MB/s out

{icons.LAPTOP} Server: prod-web-02 (10.0.1.16)
  Status: {icons.GREEN_CIRCLE} Healthy | Uptime: 45d 8h 12m
  CPU: 28.7% | Memory: 15.2 GB / 32 GB | Disk: 387 GB / 500 GB
  Network: 15.8 MB/s in, 52.3 MB/s out

{icons.LAPTOP} Server: prod-db-01 (10.0.2.10)
  Status: {icons.GREEN_CIRCLE} Healthy | Uptime: 123d 14h 45m
  CPU: 45.2% | Memory: 52.4 GB / 64 GB | Disk: 2.1 TB / 4 TB
  Network: 5.2 MB/s in, 8.7 MB/s out

{icons.FIRE} Load Balancer
  Active connections: 1,247
  Requests/sec: 2,847
  Backend health: 3/3 servers healthy
""",
    title=f"{icons.GLOBE_WITH_MERIDIANS} Infrastructure Health",
    border="solid",
    border_color="cyan",
    width=80,
)

console.newline()

# ============================================================================
# SYSTEM RESOURCES
# ============================================================================

console.rule(f"{icons.BAR_CHART} SYSTEM RESOURCES", style="blue")
console.newline()

console.frame(
    f"""
{icons.GEAR} CPU Usage
  Current: 34.2% | Peak (24h): 78.3%
  Cores: 16 | Load average: 4.23, 3.87, 3.45

{icons.FLOPPY_DISK} Memory
  Used: 24.8 GB / 64 GB (38.8%)
  Cached: 12.3 GB | Available: 26.9 GB
  Swap: 0 MB (not used)

{icons.CARD_FILE_BOX} Disk Usage
  /: 342 GB / 500 GB (68.4%)
  /data: 2.1 TB / 4 TB (52.5%)
  /backups: 847 GB / 2 TB (41.2%)
  IOPS: 2,847 reads/s, 1,234 writes/s

{icons.GLOBE_WITH_MERIDIANS} Network
  Inbound: 45.2 MB/s | Peak: 123.4 MB/s
  Outbound: 78.9 MB/s | Peak: 234.5 MB/s
  Connections: 1,247 active, 8,456 total

{icons.ONE_OCLOCK} System Load
  1 minute: 4.23 | 5 minutes: 3.87 | 15 minutes: 3.45
  Processes: 234 running, 847 total
""",
    title=f"{icons.BAR_CHART} Resource Monitoring",
    border="rounded",
    border_color="blue",
    width=75,
)

console.newline()

# ============================================================================
# APPLICATION HEALTH
# ============================================================================

console.rule(f"{icons.TEST_TUBE} APPLICATION HEALTH", style="green")
console.newline()

console.frame(
    f"""
{icons.CHECK_MARK_BUTTON} Health Checks (5 / 5 passing)
  {icons.CHECK_MARK_BUTTON} Database connection
  {icons.CHECK_MARK_BUTTON} Cache connection
  {icons.CHECK_MARK_BUTTON} External API connectivity
  {icons.CHECK_MARK_BUTTON} Disk space available
  {icons.CHECK_MARK_BUTTON} Memory within limits

{icons.CHART_INCREASING} Performance Metrics
  Response time (p95): 127ms (target: < 200ms)
  Response time (p99): 342ms (target: < 500ms)
  Error rate: 0.03% (target: < 0.1%)
  Throughput: 2,847 req/sec

{icons.GREEN_CIRCLE} Dependencies
  {icons.CHECK_MARK_BUTTON} Auth service: 8ms avg latency
  {icons.CHECK_MARK_BUTTON} Payment API: 123ms avg latency
  {icons.CHECK_MARK_BUTTON} Email service: 45ms avg latency
  {icons.CHECK_MARK_BUTTON} Storage API: 23ms avg latency
""",
    title=f"{icons.CHECK_MARK_BUTTON} Application Health: Excellent",
    border="double",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# KUBERNETES CLUSTER
# ============================================================================

console.rule(f"{icons.PACKAGE} KUBERNETES CLUSTER", style="magenta")
console.newline()

console.frame(
    f"""
{icons.GEAR} Cluster: production-us-east-1

{icons.LAPTOP} Nodes (3 / 3 ready)
  {icons.GREEN_CIRCLE} node-1: Ready | CPU: 45.2% | Memory: 12.8 GB / 32 GB
  {icons.GREEN_CIRCLE} node-2: Ready | CPU: 52.3% | Memory: 15.4 GB / 32 GB
  {icons.GREEN_CIRCLE} node-3: Ready | CPU: 38.7% | Memory: 11.2 GB / 32 GB

{icons.PACKAGE} Pods (24 / 24 running)
  web: 8/8 running | Restarts: 0
  api: 6/6 running | Restarts: 0
  worker: 4/4 running | Restarts: 2
  cron: 3/3 running | Restarts: 0
  monitoring: 3/3 running | Restarts: 0

{icons.CHECK_MARK_BUTTON} Deployments
  {icons.CHECK_MARK_BUTTON} web (v2.3.1): 8/8 replicas ready
  {icons.CHECK_MARK_BUTTON} api (v1.8.2): 6/6 replicas ready
  {icons.CHECK_MARK_BUTTON} worker (v1.5.0): 4/4 replicas ready

{icons.GLOBE_WITH_MERIDIANS} Services
  {icons.CHECK_MARK_BUTTON} web-service: LoadBalancer (external IP assigned)
  {icons.CHECK_MARK_BUTTON} api-service: ClusterIP (internal)
  {icons.CHECK_MARK_BUTTON} redis-service: ClusterIP (internal)
""",
    title=f"{icons.ROCKET} Kubernetes Status",
    border="rounded",
    border_color="magenta",
    width=80,
)

console.newline()

# ============================================================================
# UPTIME TRACKER
# ============================================================================

console.rule(f"{icons.CALENDAR} UPTIME TRACKING", style="cyan")
console.newline()

console.frame(
    f"""
{icons.CHART_INCREASING} Availability Metrics (Last 30 days)

{icons.CHECK_MARK_BUTTON} Web Application
  Uptime: 99.97% (SLA: 99.9%)
  Incidents: 1 (planned maintenance)
  Downtime: 18 minutes total
  MTTR: 18 minutes

{icons.CHECK_MARK_BUTTON} API Service
  Uptime: 99.99% (SLA: 99.95%)
  Incidents: 0
  Downtime: 2 minutes total
  MTTR: 2 minutes

{icons.CHECK_MARK_BUTTON} Database
  Uptime: 100.00% (SLA: 99.9%)
  Incidents: 0
  Downtime: 0 minutes
  MTTR: N/A

{icons.CALENDAR} Historical Performance
  Last 7 days: 100.00%
  Last 30 days: 99.97%
  Last 90 days: 99.94%
  This year: 99.92%
""",
    title=f"{icons.TROPHY} Uptime & Reliability",
    border="solid",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# DESIGN GUIDELINES
# ============================================================================

console.banner("STATUS PANEL DESIGN")

console.frame(
    f"""
{icons.BULLSEYE} STATUS PANEL PRINCIPLES

1. STATUS HIERARCHY
   {icons.GREEN_CIRCLE} Healthy: Green, check mark, normal metrics
   {icons.YELLOW_CIRCLE} Degraded: Yellow, warning, elevated metrics
   {icons.RED_CIRCLE} Critical: Red, X mark, failure indicators
   {icons.BLUE_CIRCLE} Unknown: Blue/gray, unknown state

2. KEY METRICS
   • Always show: Status, Uptime, Resource usage
   • Include thresholds: "42/100 connections"
   • Show trends: "normally 120ms"
   • Highlight issues: "{icons.FIRE} HIGH" for alerts

3. CONTEXT INFORMATION
   • Service name and identifier
   • Current values vs normal/target
   • Time-based: uptime, last seen
   • Dependencies: what relies on this

4. VISUAL GROUPING
   • Related services together
   • Infrastructure by environment
   • Dependencies show relationships
   • Color-code by health status

5. ACTIONABLE DATA
   • Not just "down" - show why
   • Include timestamps (last seen, uptime)
   • Show restart attempts, error codes
   • Link to logs or details
""",
    title=f"{icons.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
STATUS INDICATORS:

{icons.GREEN_CIRCLE} HEALTHY         All systems operational
{icons.YELLOW_CIRCLE} DEGRADED        Performance issues, still working
{icons.RED_CIRCLE} CRITICAL        Service down or failing
{icons.BLUE_CIRCLE} UNKNOWN         Cannot determine status
{icons.GEAR} STARTING        Service initializing
{icons.WARNING} WARNING         Issues detected, monitoring

COMMON METRICS:

Uptime:         "45d 8h 15m" or "99.97%"
CPU:            "34.2%" with threshold indicators
Memory:         "12.8 GB / 32 GB (40%)"
Disk:           "342 GB / 500 GB (68.4%)"
Network:        "45.2 MB/s in, 78.9 MB/s out"
Connections:    "42/100" (current/max)
Response time:  "127ms (p95)" or "< 200ms"
Throughput:     "2,847 req/sec"

USE IN:
• Service monitoring dashboards
• Infrastructure health pages
• Application status screens
• DevOps operations centers
• SRE incident response
""",
    title=f"{icons.BOOKMARK} Quick Reference",
    border="double",
    border_color="white",
    width=75,
)

# ============================================================================
# CONTEXT MANAGER APPROACH (v0.7.0)
# ============================================================================

console.rule(f"{icons.SPARKLES} CONTEXT MANAGER APPROACH", style="magenta")
console.newline()

console.text("Using console.group() for organized status displays:", bold=True)
console.newline()

# Grouped services with aligned widths
with console.group(
    title=f"{icons.BAR_CHART} Service Status Overview",
    border="rounded",
    border_color="cyan",
    align_widths=True,
):
    console.frame(
        f"{icons.GREEN_CIRCLE} Running | Uptime: 23d 14h 32m",
        title=f"{icons.CHECK_MARK_BUTTON} Web Server",
        border_color="green",
    )
    console.frame(
        f"{icons.YELLOW_CIRCLE} Degraded | Response: 2.8s",
        title=f"{icons.WARNING} API Server",
        border_color="yellow",
    )
    console.frame(
        f"{icons.GREEN_CIRCLE} Running | Connections: 42/100",
        title=f"{icons.CHECK_MARK_BUTTON} Database",
        border_color="green",
    )

console.newline()

# Nested groups for hierarchical status
console.text("Nested groups for complex hierarchies:", bold=True)
console.newline()

with console.group(title=f"{icons.GLOBE_WITH_MERIDIANS} Production Environment", border="heavy"):
    console.frame(f"{icons.GREEN_CIRCLE} All endpoints responding", title="Load Balancer")

    with console.group(title="Backend Services", border="rounded", border_color="cyan"):
        console.frame(f"{icons.CHECK_MARK_BUTTON} 8/8 replicas healthy", border_color="green")
        console.frame(f"{icons.CHECK_MARK_BUTTON} Queue depth: 0", border_color="green")

    with console.group(title="Data Layer", border="rounded", border_color="blue"):
        console.frame(f"{icons.CHECK_MARK_BUTTON} Primary: online", border_color="green")
        console.frame(f"{icons.CHECK_MARK_BUTTON} Replica: synced", border_color="green")

console.newline()

console.rule()
console.text(f"{icons.SPARKLES} Status panels provide at-a-glance system health visibility!")
