#!/usr/bin/env python3
"""
Use Case: Progress Dashboards

Real-world progress tracking patterns for build systems, deployment pipelines,
data processing, and long-running operations. Shows how to present multi-step
workflows with clear status indicators.

Use cases:
- CI/CD pipelines
- Build processes
- Deployment workflows
- Data migrations
- Batch processing
"""

from styledconsole import Console, icons

console = Console()

# ============================================================================
# BUILD PIPELINE PROGRESS
# ============================================================================

console.banner("BUILD & DEPLOY PIPELINE")
console.text("Multi-step workflow progress tracking")
console.newline()

console.frame(
    f"""
{icons.CHECK_MARK_BUTTON} Stage 1: Clone Repository        [DONE]    2.3s
{icons.CHECK_MARK_BUTTON} Stage 2: Install Dependencies    [DONE]    8.1s
{icons.CHECK_MARK_BUTTON} Stage 3: Run Tests               [DONE]   42.8s
{icons.GEAR} Stage 4: Build Application        [RUNNING] 15.2s...
{icons.YELLOW_CIRCLE} Stage 5: Deploy to Staging         [PENDING]
{icons.YELLOW_CIRCLE} Stage 6: Run Smoke Tests           [PENDING]
{icons.YELLOW_CIRCLE} Stage 7: Deploy to Production      [PENDING]

Pipeline: main-branch-build-342
Started: 2025-11-11 14:23:15
Elapsed: 1m 8s
""",
    title=f"{icons.ROCKET} CI/CD Pipeline Status",
    border="rounded",
    border_color="blue",
    width=70,
)

console.newline()

# ============================================================================
# DEPLOYMENT PROGRESS
# ============================================================================

console.rule(f"{icons.ROCKET} DEPLOYMENT TRACKING", style="green")
console.newline()

console.frame(
    f"""
{icons.CHECK_MARK_BUTTON} Pre-deployment Checks
  {icons.CHECK_MARK_BUTTON} Health checks passed
  {icons.CHECK_MARK_BUTTON} Capacity verified
  {icons.CHECK_MARK_BUTTON} Rollback plan ready

{icons.GEAR} Deployment in Progress
  {icons.CHECK_MARK_BUTTON} Traffic drained (0% on old version)
  {icons.GEAR} Deploying to 3 zones...
    {icons.CHECK_MARK_BUTTON} us-east-1: 12/12 instances healthy
    {icons.GEAR} us-west-2: 8/12 instances starting...
    {icons.YELLOW_CIRCLE} eu-west-1: 0/12 waiting

{icons.YELLOW_CIRCLE} Post-deployment
  {icons.YELLOW_CIRCLE} Smoke tests (pending)
  {icons.YELLOW_CIRCLE} Monitoring verification (pending)
""",
    title=f"{icons.GLOBE_WITH_MERIDIANS} Multi-Region Deployment",
    border="double",
    border_color="green",
    width=70,
)

console.newline()

# ============================================================================
# BUILD COMPILATION
# ============================================================================

console.rule(f"{icons.GEAR} COMPILATION PROGRESS", style="cyan")
console.newline()

console.frame(
    f"""
{icons.OPEN_BOOK} Build Configuration
  Project: large-scale-application
  Target: production
  Compiler: gcc 11.4.0

{icons.GEAR} Compilation Status
  Files compiled: 847 / 1,203 (70.4%)
  Current: src/core/network/http_client.cpp
  Speed: 12.3 files/sec
  Time elapsed: 1m 8s
  Time remaining: ~29s

{icons.FIRE} Hot Modules
  {icons.CHECK_MARK_BUTTON} Core libraries (423 files)
  {icons.GEAR} Network layer (127/156 files)
  {icons.YELLOW_CIRCLE} UI components (0/312 files)
  {icons.YELLOW_CIRCLE} Tests (0/312 files)
""",
    title=f"{icons.WRENCH} C++ Compilation",
    border="solid",
    border_color="cyan",
    width=70,
)

console.newline()

# ============================================================================
# DATA PROCESSING
# ============================================================================

console.rule(f"{icons.BAR_CHART} DATA PROCESSING", style="magenta")
console.newline()

console.frame(
    f"""
{icons.HOURGLASS_DONE} Batch Job Progress

Job ID: analytics-daily-2025-11-11
Started: 14:00:00 (3h 45m ago)

{icons.CHECK_MARK_BUTTON} Phase 1: Data Ingestion          100% ━━━━━━━━━━ 2.1M records
{icons.CHECK_MARK_BUTTON} Phase 2: Data Validation          100% ━━━━━━━━━━ 2.0M valid
{icons.GEAR} Phase 3: Data Transformation        67% ━━━━━━━━░░ 1.3M / 2.0M
{icons.YELLOW_CIRCLE} Phase 4: Data Aggregation           0% ░░░░░░░░░░
{icons.YELLOW_CIRCLE} Phase 5: Export Results              0% ░░░░░░░░░░

Current throughput: 1,247 records/sec
ETA: 42 minutes remaining
""",
    title=f"{icons.PACKAGE} Batch Processing Pipeline",
    border="rounded",
    border_color="magenta",
    width=70,
)

console.newline()

# ============================================================================
# DATABASE MIGRATION
# ============================================================================

console.rule(f"{icons.FLOPPY_DISK} DATABASE MIGRATION", style="yellow")
console.newline()

console.frame(
    f"""
{icons.GEAR} Migration Status: v2.5.0 → v2.6.0

{icons.CHECK_MARK_BUTTON} Pre-migration Tasks
  {icons.CHECK_MARK_BUTTON} Backup completed (4.2 GB)
  {icons.CHECK_MARK_BUTTON} Read-only mode enabled
  {icons.CHECK_MARK_BUTTON} Connection pool drained

{icons.GEAR} Schema Updates (3 / 7 migrations)
  {icons.CHECK_MARK_BUTTON} 001_add_user_indexes.sql           [DONE]    2.1s
  {icons.CHECK_MARK_BUTTON} 002_create_audit_tables.sql        [DONE]    5.8s
  {icons.CHECK_MARK_BUTTON} 003_update_permissions.sql         [DONE]    1.3s
  {icons.GEAR} 004_migrate_user_data.sql           [RUNNING] 45.2s...
                 Rows: 123,847 / 500,000 (24.8%)
  {icons.YELLOW_CIRCLE} 005_add_foreign_keys.sql             [PENDING]
  {icons.YELLOW_CIRCLE} 006_create_materialized_views.sql    [PENDING]
  {icons.YELLOW_CIRCLE} 007_optimize_indexes.sql             [PENDING]

{icons.YELLOW_CIRCLE} Post-migration Validation (pending)
""",
    title=f"{icons.CARD_FILE_BOX} Database Migration",
    border="thick",
    border_color="yellow",
    width=75,
)

console.newline()

# ============================================================================
# DOCKER IMAGE BUILD
# ============================================================================

console.rule(f"{icons.PACKAGE} CONTAINER BUILD", style="blue")
console.newline()

console.frame(
    f"""
{icons.GEAR} Building Docker Image

Image: myapp:v2.3.1
Platform: linux/amd64
Build context: 847 MB

{icons.GEAR} Build Steps (4 / 8 completed)
  {icons.CHECK_MARK_BUTTON} Step 1/8 : FROM node:18-alpine
  {icons.CHECK_MARK_BUTTON} Step 2/8 : WORKDIR /app
  {icons.CHECK_MARK_BUTTON} Step 3/8 : COPY package*.json ./
  {icons.CHECK_MARK_BUTTON} Step 4/8 : RUN npm ci --production
  {icons.GEAR} Step 5/8 : COPY . .
                 Transferring: 423 MB / 847 MB (50%)
  {icons.YELLOW_CIRCLE} Step 6/8 : RUN npm run build
  {icons.YELLOW_CIRCLE} Step 7/8 : EXPOSE 3000
  {icons.YELLOW_CIRCLE} Step 8/8 : CMD ["npm", "start"]

Time elapsed: 2m 18s
""",
    title=f"{icons.PACKAGE} Docker Build",
    border="rounded",
    border_color="blue",
    width=70,
)

console.newline()

# ============================================================================
# TEST EXECUTION
# ============================================================================

console.rule(f"{icons.TEST_TUBE} TEST EXECUTION", style="green")
console.newline()

console.frame(
    f"""
{icons.TEST_TUBE} Test Suite Progress

{icons.CHECK_MARK_BUTTON} Unit Tests                 [PASSED]    847 / 847    8.2s
{icons.CHECK_MARK_BUTTON} Integration Tests          [PASSED]     52 / 52    23.1s
{icons.GEAR} End-to-End Tests            [RUNNING]    12 / 28    45.2s...
  {icons.CHECK_MARK_BUTTON} Login flow
  {icons.CHECK_MARK_BUTTON} User registration
  {icons.CHECK_MARK_BUTTON} Dashboard loading
  {icons.CHECK_MARK_BUTTON} Data export
  {icons.GEAR} Payment processing (running)
  {icons.YELLOW_CIRCLE} Admin panel (pending)
  {icons.YELLOW_CIRCLE} API stress test (pending)

Total: 911 / 927 tests (98.3%)
Coverage: 87.4% (target: 85%)
""",
    title=f"{icons.CHECK_MARK_BUTTON} Automated Testing",
    border="double",
    border_color="green",
    width=70,
)

console.newline()

# ============================================================================
# PARALLEL JOBS
# ============================================================================

console.rule(f"{icons.GEAR} PARALLEL EXECUTION", style="cyan")
console.newline()

console.frame(
    f"""
{icons.ROCKET} Parallel Job Execution (4 workers)

Worker 1: {icons.GEAR} Processing batch 1/10  [RUNNING]  23% ━━━░░░░░░░
Worker 2: {icons.GEAR} Processing batch 2/10  [RUNNING]  45% ━━━━━░░░░░
Worker 3: {icons.CHECK_MARK_BUTTON} Processing batch 3/10  [DONE]    100% ━━━━━━━━━━
Worker 4: {icons.GEAR} Processing batch 4/10  [RUNNING]  67% ━━━━━━━░░░

Completed: 3 / 10 batches (30%)
Active: 3 jobs running
Queue: 6 jobs pending
Throughput: 847 items/sec
""",
    title=f"{icons.GEAR} Parallel Processing",
    border="solid",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# DESIGN GUIDELINES
# ============================================================================

console.banner("PROGRESS UI DESIGN")

console.frame(
    f"""
{icons.BULLSEYE} PROGRESS DASHBOARD PRINCIPLES

1. VISUAL STATUS HIERARCHY
   {icons.CHECK_MARK_BUTTON} Done: Green, check mark
   {icons.GEAR} Running: Blue/cyan, gear/spinner
   {icons.YELLOW_CIRCLE} Pending: Yellow, circle
   {icons.CROSS_MARK} Failed: Red, X mark

2. PROGRESS INDICATORS
   • Percentages: "847 / 1,203 (70.4%)"
   • Progress bars: "━━━━━━━░░░"
   • Time estimates: "ETA: 42 minutes"
   • Throughput: "1,247 records/sec"

3. CONTEXT INFORMATION
   • What's happening: Current step/file
   • How much done: Percentage or count
   • How long left: Time remaining
   • Overall status: Pipeline health

4. MULTI-STEP WORKFLOWS
   • Show all steps (past, current, future)
   • Clear stage boundaries
   • Sequential vs parallel indication
   • Dependencies visible

5. ERROR HANDLING
   {icons.CROSS_MARK} Failed steps: Show error clearly
   {icons.WARNING} Warnings: Don't stop progress
   {icons.INFORMATION} Retries: Show attempt count
""",
    title=f"{icons.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
STATUS INDICATORS REFERENCE:

{icons.CHECK_MARK_BUTTON} COMPLETED       Green        Task finished successfully
{icons.GEAR} IN PROGRESS     Blue/Cyan    Currently executing
{icons.YELLOW_CIRCLE} PENDING         Yellow       Waiting to start
{icons.CROSS_MARK} FAILED          Red          Task failed
{icons.WARNING} WARNING         Yellow       Issues but continuing
{icons.HOURGLASS_DONE} QUEUED          Gray         In queue, not started

PROGRESS FORMATS:

Percentage:     "847 / 1,203 (70.4%)"
Progress bar:   "━━━━━━━━░░ 80%"
Time-based:     "2m 18s / 3m 00s"
Throughput:     "1,247 records/sec"
ETA:            "~42 minutes remaining"

USE IN:
• CI/CD pipelines (builds, tests, deploys)
• Data processing (ETL, migrations, batch jobs)
• File operations (uploads, downloads, sync)
• Installation/setup wizards
• Long-running computations
""",
    title=f"{icons.BOOKMARK} Quick Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{icons.SPARKLES} Progress dashboards keep users informed during long operations!")
