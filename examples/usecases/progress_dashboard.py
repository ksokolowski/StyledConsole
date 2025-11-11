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

from styledconsole import Console
from styledconsole.emojis import EMOJI

console = Console()

# ============================================================================
# BUILD PIPELINE PROGRESS
# ============================================================================

console.banner("BUILD & DEPLOY PIPELINE")
console.text("Multi-step workflow progress tracking")
console.newline()

console.frame(
    f"""
{EMOJI.CHECK} Stage 1: Clone Repository        [DONE]    2.3s
{EMOJI.CHECK} Stage 2: Install Dependencies    [DONE]    8.1s
{EMOJI.CHECK} Stage 3: Run Tests               [DONE]   42.8s
{EMOJI.GEAR} Stage 4: Build Application        [RUNNING] 15.2s...
{EMOJI.YELLOW_CIRCLE} Stage 5: Deploy to Staging         [PENDING]
{EMOJI.YELLOW_CIRCLE} Stage 6: Run Smoke Tests           [PENDING]
{EMOJI.YELLOW_CIRCLE} Stage 7: Deploy to Production      [PENDING]

Pipeline: main-branch-build-342
Started: 2025-11-11 14:23:15
Elapsed: 1m 8s
""",
    title=f"{EMOJI.ROCKET} CI/CD Pipeline Status",
    border="rounded",
    border_color="blue",
    width=70,
)

console.newline()

# ============================================================================
# DEPLOYMENT PROGRESS
# ============================================================================

console.rule(f"{EMOJI.ROCKET} DEPLOYMENT TRACKING", style="green")
console.newline()

console.frame(
    f"""
{EMOJI.CHECK} Pre-deployment Checks
  {EMOJI.CHECK} Health checks passed
  {EMOJI.CHECK} Capacity verified
  {EMOJI.CHECK} Rollback plan ready

{EMOJI.GEAR} Deployment in Progress
  {EMOJI.CHECK} Traffic drained (0% on old version)
  {EMOJI.GEAR} Deploying to 3 zones...
    {EMOJI.CHECK} us-east-1: 12/12 instances healthy
    {EMOJI.GEAR} us-west-2: 8/12 instances starting...
    {EMOJI.YELLOW_CIRCLE} eu-west-1: 0/12 waiting

{EMOJI.YELLOW_CIRCLE} Post-deployment
  {EMOJI.YELLOW_CIRCLE} Smoke tests (pending)
  {EMOJI.YELLOW_CIRCLE} Monitoring verification (pending)
""",
    title=f"{EMOJI.GLOBE} Multi-Region Deployment",
    border="double",
    border_color="green",
    width=70,
)

console.newline()

# ============================================================================
# BUILD COMPILATION
# ============================================================================

console.rule(f"{EMOJI.GEAR} COMPILATION PROGRESS", style="cyan")
console.newline()

console.frame(
    f"""
{EMOJI.BOOK} Build Configuration
  Project: large-scale-application
  Target: production
  Compiler: gcc 11.4.0

{EMOJI.GEAR} Compilation Status
  Files compiled: 847 / 1,203 (70.4%)
  Current: src/core/network/http_client.cpp
  Speed: 12.3 files/sec
  Time elapsed: 1m 8s
  Time remaining: ~29s

{EMOJI.FIRE} Hot Modules
  {EMOJI.CHECK} Core libraries (423 files)
  {EMOJI.GEAR} Network layer (127/156 files)
  {EMOJI.YELLOW_CIRCLE} UI components (0/312 files)
  {EMOJI.YELLOW_CIRCLE} Tests (0/312 files)
""",
    title=f"{EMOJI.WRENCH} C++ Compilation",
    border="solid",
    border_color="cyan",
    width=70,
)

console.newline()

# ============================================================================
# DATA PROCESSING
# ============================================================================

console.rule(f"{EMOJI.CHART_BAR} DATA PROCESSING", style="magenta")
console.newline()

console.frame(
    f"""
{EMOJI.HOURGLASS} Batch Job Progress

Job ID: analytics-daily-2025-11-11
Started: 14:00:00 (3h 45m ago)

{EMOJI.CHECK} Phase 1: Data Ingestion          100% ━━━━━━━━━━ 2.1M records
{EMOJI.CHECK} Phase 2: Data Validation          100% ━━━━━━━━━━ 2.0M valid
{EMOJI.GEAR} Phase 3: Data Transformation        67% ━━━━━━━━░░ 1.3M / 2.0M
{EMOJI.YELLOW_CIRCLE} Phase 4: Data Aggregation           0% ░░░░░░░░░░
{EMOJI.YELLOW_CIRCLE} Phase 5: Export Results              0% ░░░░░░░░░░

Current throughput: 1,247 records/sec
ETA: 42 minutes remaining
""",
    title=f"{EMOJI.PACKAGE} Batch Processing Pipeline",
    border="rounded",
    border_color="magenta",
    width=70,
)

console.newline()

# ============================================================================
# DATABASE MIGRATION
# ============================================================================

console.rule(f"{EMOJI.FLOPPY} DATABASE MIGRATION", style="yellow")
console.newline()

console.frame(
    f"""
{EMOJI.GEAR} Migration Status: v2.5.0 → v2.6.0

{EMOJI.CHECK} Pre-migration Tasks
  {EMOJI.CHECK} Backup completed (4.2 GB)
  {EMOJI.CHECK} Read-only mode enabled
  {EMOJI.CHECK} Connection pool drained

{EMOJI.GEAR} Schema Updates (3 / 7 migrations)
  {EMOJI.CHECK} 001_add_user_indexes.sql           [DONE]    2.1s
  {EMOJI.CHECK} 002_create_audit_tables.sql        [DONE]    5.8s
  {EMOJI.CHECK} 003_update_permissions.sql         [DONE]    1.3s
  {EMOJI.GEAR} 004_migrate_user_data.sql           [RUNNING] 45.2s...
                 Rows: 123,847 / 500,000 (24.8%)
  {EMOJI.YELLOW_CIRCLE} 005_add_foreign_keys.sql             [PENDING]
  {EMOJI.YELLOW_CIRCLE} 006_create_materialized_views.sql    [PENDING]
  {EMOJI.YELLOW_CIRCLE} 007_optimize_indexes.sql             [PENDING]

{EMOJI.YELLOW_CIRCLE} Post-migration Validation (pending)
""",
    title=f"{EMOJI.CARD_FILE_BOX} Database Migration",
    border="thick",
    border_color="yellow",
    width=75,
)

console.newline()

# ============================================================================
# DOCKER IMAGE BUILD
# ============================================================================

console.rule(f"{EMOJI.PACKAGE} CONTAINER BUILD", style="blue")
console.newline()

console.frame(
    f"""
{EMOJI.GEAR} Building Docker Image

Image: myapp:v2.3.1
Platform: linux/amd64
Build context: 847 MB

{EMOJI.GEAR} Build Steps (4 / 8 completed)
  {EMOJI.CHECK} Step 1/8 : FROM node:18-alpine
  {EMOJI.CHECK} Step 2/8 : WORKDIR /app
  {EMOJI.CHECK} Step 3/8 : COPY package*.json ./
  {EMOJI.CHECK} Step 4/8 : RUN npm ci --production
  {EMOJI.GEAR} Step 5/8 : COPY . .
                 Transferring: 423 MB / 847 MB (50%)
  {EMOJI.YELLOW_CIRCLE} Step 6/8 : RUN npm run build
  {EMOJI.YELLOW_CIRCLE} Step 7/8 : EXPOSE 3000
  {EMOJI.YELLOW_CIRCLE} Step 8/8 : CMD ["npm", "start"]

Time elapsed: 2m 18s
""",
    title=f"{EMOJI.PACKAGE} Docker Build",
    border="rounded",
    border_color="blue",
    width=70,
)

console.newline()

# ============================================================================
# TEST EXECUTION
# ============================================================================

console.rule(f"{EMOJI.TEST_TUBE} TEST EXECUTION", style="green")
console.newline()

console.frame(
    f"""
{EMOJI.TEST_TUBE} Test Suite Progress

{EMOJI.CHECK} Unit Tests                 [PASSED]    847 / 847    8.2s
{EMOJI.CHECK} Integration Tests          [PASSED]     52 / 52    23.1s
{EMOJI.GEAR} End-to-End Tests            [RUNNING]    12 / 28    45.2s...
  {EMOJI.CHECK} Login flow
  {EMOJI.CHECK} User registration
  {EMOJI.CHECK} Dashboard loading
  {EMOJI.CHECK} Data export
  {EMOJI.GEAR} Payment processing (running)
  {EMOJI.YELLOW_CIRCLE} Admin panel (pending)
  {EMOJI.YELLOW_CIRCLE} API stress test (pending)

Total: 911 / 927 tests (98.3%)
Coverage: 87.4% (target: 85%)
""",
    title=f"{EMOJI.CHECK} Automated Testing",
    border="double",
    border_color="green",
    width=70,
)

console.newline()

# ============================================================================
# PARALLEL JOBS
# ============================================================================

console.rule(f"{EMOJI.GEAR} PARALLEL EXECUTION", style="cyan")
console.newline()

console.frame(
    f"""
{EMOJI.ROCKET} Parallel Job Execution (4 workers)

Worker 1: {EMOJI.GEAR} Processing batch 1/10  [RUNNING]  23% ━━━░░░░░░░
Worker 2: {EMOJI.GEAR} Processing batch 2/10  [RUNNING]  45% ━━━━━░░░░░
Worker 3: {EMOJI.CHECK} Processing batch 3/10  [DONE]    100% ━━━━━━━━━━
Worker 4: {EMOJI.GEAR} Processing batch 4/10  [RUNNING]  67% ━━━━━━━░░░

Completed: 3 / 10 batches (30%)
Active: 3 jobs running
Queue: 6 jobs pending
Throughput: 847 items/sec
""",
    title=f"{EMOJI.GEAR} Parallel Processing",
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
{EMOJI.TARGET} PROGRESS DASHBOARD PRINCIPLES

1. VISUAL STATUS HIERARCHY
   {EMOJI.CHECK} Done: Green, check mark
   {EMOJI.GEAR} Running: Blue/cyan, gear/spinner
   {EMOJI.YELLOW_CIRCLE} Pending: Yellow, circle
   {EMOJI.CROSS} Failed: Red, X mark

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
   {EMOJI.CROSS} Failed steps: Show error clearly
   {EMOJI.WARNING} Warnings: Don't stop progress
   {EMOJI.INFO} Retries: Show attempt count
""",
    title=f"{EMOJI.LIGHTBULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
STATUS INDICATORS REFERENCE:

{EMOJI.CHECK} COMPLETED       Green        Task finished successfully
{EMOJI.GEAR} IN PROGRESS     Blue/Cyan    Currently executing
{EMOJI.YELLOW_CIRCLE} PENDING         Yellow       Waiting to start
{EMOJI.CROSS} FAILED          Red          Task failed
{EMOJI.WARNING} WARNING         Yellow       Issues but continuing
{EMOJI.HOURGLASS} QUEUED          Gray         In queue, not started

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
    title=f"{EMOJI.BOOKMARK} Quick Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{EMOJI.SPARKLES} Progress dashboards keep users informed during long operations!")
