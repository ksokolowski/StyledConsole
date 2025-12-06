#!/usr/bin/env python3
"""
Use Case: CLI Menus

Real-world menu patterns for interactive CLI applications. Shows how to
present options, navigation, and selection interfaces clearly.

Note: These are visual mockups showing menu patterns. Actual interactive
input would require additional libraries (like prompt_toolkit or inquirer).

Use cases:
- Main application menus
- Configuration wizards
- Interactive installers
- Tool selection interfaces
- Navigation systems
"""

from styledconsole import Console
from styledconsole.emojis import EMOJI

console = Console()

# ============================================================================
# MAIN APPLICATION MENU
# ============================================================================

console.banner("CLI MENUS & NAVIGATION")
console.text("Interactive menu patterns and selection interfaces")
console.newline()

console.frame(
    f"""
{EMOJI.ROCKET} Main Menu

{EMOJI.GREEN_CIRCLE} 1. Start Application
  {EMOJI.INFORMATION} Launch the main application server

{EMOJI.GEAR} 2. Configuration
  {EMOJI.INFORMATION} Manage application settings and preferences

{EMOJI.BAR_CHART} 3. View Logs
  {EMOJI.INFORMATION} Browse application logs and monitoring data

{EMOJI.TEST_TUBE} 4. Run Tests
  {EMOJI.INFORMATION} Execute test suites and validation

{EMOJI.WRENCH} 5. Database Tools
  {EMOJI.INFORMATION} Database migrations, backups, and maintenance

{EMOJI.GLOBE_WITH_MERIDIANS} 6. Deployment
  {EMOJI.INFORMATION} Deploy application to various environments

{EMOJI.LIGHT_BULB} 7. Help & Documentation
  {EMOJI.INFORMATION} View documentation and get help

{EMOJI.CROSS_MARK} 0. Exit
  {EMOJI.INFORMATION} Close the application

─────────────────────────────────────────────────────────────
Enter your choice [0-7]:
""",
    title=f"{EMOJI.ROCKET} Application Control Panel",
    border="rounded",
    border_color="cyan",
    width=70,
)

console.newline()

# ============================================================================
# CONFIGURATION MENU
# ============================================================================

console.rule(f"{EMOJI.GEAR} CONFIGURATION MENU", style="blue")
console.newline()

console.frame(
    f"""
Current Configuration:

{EMOJI.LAPTOP} Environment: production
{EMOJI.FLOPPY_DISK} Database: PostgreSQL (prod-db-01.internal)
{EMOJI.CARD_FILE_BOX} Cache: Redis (prod-cache-01.internal)
{EMOJI.LOCKED} Security: TLS 1.3 enabled

─────────────────────────────────────────────────────────────

{EMOJI.GEAR} Configuration Options:

  {EMOJI.CHECK_MARK_BUTTON} 1. Change Environment
     Current: production
     Options: development, staging, production

  {EMOJI.FLOPPY_DISK} 2. Database Settings
     Connection, pool size, timeout

  {EMOJI.CARD_FILE_BOX} 3. Cache Configuration
     Type, TTL, max memory

  {EMOJI.LOCKED} 4. Security Settings
     TLS, authentication, session timeout

  {EMOJI.GLOBE_WITH_MERIDIANS} 5. Network Settings
     Port, host, workers, timeouts

  {EMOJI.BAR_CHART} 6. Logging & Monitoring
     Log level, metrics, alerts

  {EMOJI.ARROW_LEFT} 9. Back to Main Menu

─────────────────────────────────────────────────────────────
Select option [1-6, 9]:
""",
    title=f"{EMOJI.GEAR} Configuration Manager",
    border="solid",
    border_color="blue",
    width=70,
)

console.newline()

# ============================================================================
# SELECTION WITH PREVIEW
# ============================================================================

console.rule(f"{EMOJI.BULLSEYE} SELECTION INTERFACE", style="magenta")
console.newline()

console.frame(
    f"""
{EMOJI.ROCKET} Select Deployment Environment:

  {EMOJI.LAPTOP} 1. Development
     {EMOJI.INFORMATION} URL: https://dev.example.com
     {EMOJI.INFORMATION} Branch: develop
     {EMOJI.INFORMATION} Auto-deploy: Enabled

> {EMOJI.GREEN_CIRCLE} 2. Staging              {EMOJI.ARROW_LEFT} SELECTED
     {EMOJI.INFORMATION} URL: https://staging.example.com
     {EMOJI.INFORMATION} Branch: main
     {EMOJI.INFORMATION} Manual approval required

  {EMOJI.FIRE} 3. Production
     {EMOJI.WARNING} URL: https://example.com
     {EMOJI.WARNING} Branch: main
     {EMOJI.WARNING} Requires 2FA + approval

─────────────────────────────────────────────────────────────
{EMOJI.CHECK_MARK_BUTTON} Confirm [Y/n] | {EMOJI.CROSS_MARK} Cancel [Ctrl+C]
""",
    title=f"{EMOJI.GLOBE_WITH_MERIDIANS} Environment Selection",
    border="rounded",
    border_color="magenta",
    width=70,
)

console.newline()

# ============================================================================
# WIZARD INTERFACE
# ============================================================================

console.rule(f"{EMOJI.SPARKLES} SETUP WIZARD", style="green")
console.newline()

console.frame(
    f"""
{EMOJI.GEAR} Application Setup Wizard

{EMOJI.CHECK_MARK_BUTTON} Step 1: Choose Database      [COMPLETED]
    Selected: PostgreSQL

{EMOJI.CHECK_MARK_BUTTON} Step 2: Configure Connection [COMPLETED]
    Host: localhost
    Port: 5432

> {EMOJI.GEAR} Step 3: Create Admin User    [CURRENT]
    ┌────────────────────────────────────────────┐
    │ Username: admin                            │
    │ Email: admin@example.com                   │
    │ Password: ••••••••                         │
    │ Confirm: ••••••••                          │
    └────────────────────────────────────────────┘

  {EMOJI.YELLOW_CIRCLE} Step 4: Set Preferences      [PENDING]

  {EMOJI.YELLOW_CIRCLE} Step 5: Review & Confirm     [PENDING]

─────────────────────────────────────────────────────────────
{EMOJI.ARROW_RIGHT} Continue [Enter] | {EMOJI.ARROW_LEFT} Back [P] | {EMOJI.CROSS_MARK} Cancel [C]

Progress: 3/5 steps (60%)
""",
    title=f"{EMOJI.SPARKLES} Setup Wizard (Step 3/5)",
    border="double",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# MULTI-SELECT INTERFACE
# ============================================================================

console.rule(f"{EMOJI.PACKAGE} MULTI-SELECT", style="cyan")
console.newline()

console.frame(
    f"""
{EMOJI.PACKAGE} Select Components to Install:

{EMOJI.CHECK_MARK_BUTTON} [X] Core Application (required)
  {EMOJI.INFORMATION} 145 MB | Essential application files

{EMOJI.CHECK_MARK_BUTTON} [X] Web Server (nginx)
  {EMOJI.INFORMATION} 23 MB | HTTP server and reverse proxy

{EMOJI.CHECK_MARK_BUTTON} [X] Database (PostgreSQL)
  {EMOJI.INFORMATION} 287 MB | Relational database system

{EMOJI.GREEN_CIRCLE} [X] Cache Server (Redis)
  {EMOJI.INFORMATION} 12 MB | In-memory data store

{EMOJI.YELLOW_CIRCLE} [ ] Monitoring Tools
  {EMOJI.INFORMATION} 67 MB | Metrics, logs, and dashboards

{EMOJI.YELLOW_CIRCLE} [ ] Development Tools
  {EMOJI.INFORMATION} 234 MB | Debuggers, profilers, analyzers

{EMOJI.YELLOW_CIRCLE} [ ] Documentation
  {EMOJI.INFORMATION} 45 MB | API docs and tutorials

─────────────────────────────────────────────────────────────
Selected: 4 components | Total size: 467 MB

{EMOJI.INFORMATION} Use Space to toggle | Enter to continue
""",
    title=f"{EMOJI.WRENCH} Component Selection",
    border="solid",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# NESTED MENU
# ============================================================================

console.rule(f"{EMOJI.FILE_FOLDER} NESTED NAVIGATION", style="blue")
console.newline()

console.frame(
    f"""
{EMOJI.WRENCH} Database Tools

{EMOJI.FLOPPY_DISK} 1. Migrations
   {EMOJI.ARROW_RIGHT} Pending: 3 | Applied: 47 | Status: Up to date

{EMOJI.PACKAGE} 2. Backup & Restore
   {EMOJI.ARROW_RIGHT} Last backup: 2 hours ago

{EMOJI.TEST_TUBE} 3. Database Health Check
   {EMOJI.ARROW_RIGHT} Status: {EMOJI.GREEN_CIRCLE} All checks passed

{EMOJI.BAR_CHART} 4. Performance Analysis
   {EMOJI.ARROW_RIGHT} Query stats, slow queries, indexes

{EMOJI.GEAR} 5. Connection Management
   {EMOJI.ARROW_RIGHT} Pool: 42/100 active | Settings

{EMOJI.ARROW_LEFT} 9. Back to Main Menu

─────────────────────────────────────────────────────────────

{EMOJI.FLOPPY_DISK} Migrations {EMOJI.ARROW_RIGHT} [1]

  {EMOJI.CHART_INCREASING} 1. View Migration Status
  {EMOJI.ROCKET} 2. Run Pending Migrations
  {EMOJI.ARROW_LEFT} 3. Rollback Last Migration
  {EMOJI.SCROLL} 4. Create New Migration
  {EMOJI.ARROW_LEFT} 9. Back

─────────────────────────────────────────────────────────────
Select option:
""",
    title=f"{EMOJI.WRENCH} Tools {EMOJI.ARROW_RIGHT} Database {EMOJI.ARROW_RIGHT} Migrations",
    border="rounded",
    border_color="blue",
    width=75,
)

console.newline()

# ============================================================================
# ACTION CONFIRMATION
# ============================================================================

console.rule(f"{EMOJI.WARNING} CONFIRMATION DIALOGS", style="yellow")
console.newline()

console.frame(
    f"""
{EMOJI.WARNING} Confirm Destructive Action

You are about to delete the database:

  Name: production_backup_2025_11_01
  Size: 4.2 GB
  Created: 2025-11-01 02:00:00
  Tables: 47
  Records: ~2.4M

{EMOJI.CROSS_MARK} This action cannot be undone!

─────────────────────────────────────────────────────────────

Type "DELETE" to confirm:

{EMOJI.INFORMATION} Or press Ctrl+C to cancel
""",
    title=f"{EMOJI.POLICE_CAR_LIGHT} Destructive Action Warning",
    border="thick",
    border_color="red",
    width=70,
)

console.newline()

# ============================================================================
# QUICK ACTIONS MENU
# ============================================================================

console.rule(f"{EMOJI.FIRE} QUICK ACTIONS", style="magenta")
console.newline()

console.frame(
    f"""
{EMOJI.FIRE} Quick Actions (Press key to execute)

[1] {EMOJI.ROCKET} Deploy to Staging        [6] {EMOJI.BAR_CHART} View Metrics
[2] {EMOJI.TEST_TUBE} Run Tests                    [7] {EMOJI.SCROLL} View Logs
[3] {EMOJI.FLOPPY_DISK} Backup Database          [8] {EMOJI.LAPTOP} SSH to Server
[4] {EMOJI.GEAR} Restart Services          [9] {EMOJI.CALENDAR} View Schedule
[5] {EMOJI.WRENCH} Clear Cache               [0] {EMOJI.LIGHT_BULB} Help

─────────────────────────────────────────────────────────────
{EMOJI.INFORMATION} Shortcuts: [Q]uit | [R]efresh | [H]elp
""",
    title=f"{EMOJI.FIRE} Quick Actions Panel",
    border="rounded",
    border_color="magenta",
    width=75,
)

console.newline()

# ============================================================================
# DESIGN GUIDELINES
# ============================================================================

console.banner("MENU DESIGN PATTERNS")

console.frame(
    f"""
{EMOJI.BULLSEYE} MENU DESIGN PRINCIPLES

1. VISUAL HIERARCHY
   • Title: Clear context, where am I?
   • Options: Numbered or lettered
   • Descriptions: Brief explanation below option
   • Current selection: Highlighted with {EMOJI.ARROW_LEFT} or >

2. NAVIGATION CLARITY
   • Show breadcrumbs: Menu > Submenu > Action
   • Back option: Always [9] or [B] for consistency
   • Exit option: [0], [Q], or Ctrl+C
   • Shortcuts: Single-key for common actions

3. OPTION FORMATTING
   {EMOJI.GREEN_CIRCLE} [1] Action Name
      {EMOJI.INFORMATION} Brief description or current state
   • Emoji: Visual category indicator
   • Number: Quick selection
   • Description: What will happen

4. STATUS INDICATORS
   {EMOJI.CHECK_MARK_BUTTON} Completed or enabled
   {EMOJI.GEAR} Currently running or active
   {EMOJI.YELLOW_CIRCLE} Pending or disabled
   {EMOJI.WARNING} Requires attention
   {EMOJI.CROSS_MARK} Error or unavailable

5. INTERACTIVE ELEMENTS
   • Show available keys: [1-6, 0]
   • Indicate current step: (3/5)
   • Progress bars: ━━━━━░░░░░
   • Confirmation: Type keyword or press Y/N
""",
    title=f"{EMOJI.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
MENU PATTERNS:

{EMOJI.ROCKET} MAIN MENU
  Numbered options, brief descriptions
  Use: Application entry point, top-level navigation

{EMOJI.GEAR} CONFIGURATION MENU
  Current values shown, options to change
  Use: Settings, preferences, system config

{EMOJI.BULLSEYE} SELECTION INTERFACE
  Options with preview/details
  Use: Choosing from alternatives, environments

{EMOJI.SPARKLES} SETUP WIZARD
  Multi-step process, progress indicator
  Use: Installers, onboarding, complex config

{EMOJI.PACKAGE} MULTI-SELECT
  Checkboxes [X] [ ], Space to toggle
  Use: Component selection, feature flags

{EMOJI.FILE_FOLDER} NESTED NAVIGATION
  Breadcrumbs, hierarchical menus
  Use: Complex tools, file browsers

{EMOJI.WARNING} CONFIRMATION DIALOGS
  Destructive actions require explicit confirm
  Use: Delete, reset, deploy to production

{EMOJI.FIRE} QUICK ACTIONS
  Single-key shortcuts, no confirmation
  Use: Common tasks, power user features

KEYBOARD CONVENTIONS:
[1-9, 0]: Numbered selection
[Enter]: Confirm/Continue
[Space]: Toggle (multi-select)
[Y/N]: Yes/No confirmation
[P/B]: Previous/Back
[Q]: Quit
[H/?]: Help
[Ctrl+C]: Cancel/Exit
""",
    title=f"{EMOJI.BOOKMARK} Menu Patterns Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{EMOJI.SPARKLES} Well-designed menus make CLI apps intuitive and efficient!")
