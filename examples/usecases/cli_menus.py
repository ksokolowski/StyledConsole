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

from styledconsole import Console, icons

console = Console()

# ============================================================================
# MAIN APPLICATION MENU
# ============================================================================

console.banner("CLI MENUS & NAVIGATION")
console.text("Interactive menu patterns and selection interfaces")
console.newline()

console.frame(
    f"""
{icons.ROCKET} Main Menu

{icons.GREEN_CIRCLE} 1. Start Application
  {icons.INFORMATION} Launch the main application server

{icons.GEAR} 2. Configuration
  {icons.INFORMATION} Manage application settings and preferences

{icons.BAR_CHART} 3. View Logs
  {icons.INFORMATION} Browse application logs and monitoring data

{icons.TEST_TUBE} 4. Run Tests
  {icons.INFORMATION} Execute test suites and validation

{icons.WRENCH} 5. Database Tools
  {icons.INFORMATION} Database migrations, backups, and maintenance

{icons.GLOBE_WITH_MERIDIANS} 6. Deployment
  {icons.INFORMATION} Deploy application to various environments

{icons.LIGHT_BULB} 7. Help & Documentation
  {icons.INFORMATION} View documentation and get help

{icons.CROSS_MARK} 0. Exit
  {icons.INFORMATION} Close the application

─────────────────────────────────────────────────────────────
Enter your choice [0-7]:
""",
    title=f"{icons.ROCKET} Application Control Panel",
    border="rounded",
    border_color="cyan",
    width=70,
)

console.newline()

# ============================================================================
# CONFIGURATION MENU
# ============================================================================

console.rule(f"{icons.GEAR} CONFIGURATION MENU", style="blue")
console.newline()

console.frame(
    f"""
Current Configuration:

{icons.LAPTOP} Environment: production
{icons.FLOPPY_DISK} Database: PostgreSQL (prod-db-01.internal)
{icons.CARD_FILE_BOX} Cache: Redis (prod-cache-01.internal)
{icons.LOCKED} Security: TLS 1.3 enabled

─────────────────────────────────────────────────────────────

{icons.GEAR} Configuration Options:

  {icons.CHECK_MARK_BUTTON} 1. Change Environment
     Current: production
     Options: development, staging, production

  {icons.FLOPPY_DISK} 2. Database Settings
     Connection, pool size, timeout

  {icons.CARD_FILE_BOX} 3. Cache Configuration
     Type, TTL, max memory

  {icons.LOCKED} 4. Security Settings
     TLS, authentication, session timeout

  {icons.GLOBE_WITH_MERIDIANS} 5. Network Settings
     Port, host, workers, timeouts

  {icons.BAR_CHART} 6. Logging & Monitoring
     Log level, metrics, alerts

  {icons.ARROW_LEFT} 9. Back to Main Menu

─────────────────────────────────────────────────────────────
Select option [1-6, 9]:
""",
    title=f"{icons.GEAR} Configuration Manager",
    border="solid",
    border_color="blue",
    width=70,
)

console.newline()

# ============================================================================
# SELECTION WITH PREVIEW
# ============================================================================

console.rule(f"{icons.BULLSEYE} SELECTION INTERFACE", style="magenta")
console.newline()

console.frame(
    f"""
{icons.ROCKET} Select Deployment Environment:

  {icons.LAPTOP} 1. Development
     {icons.INFORMATION} URL: https://dev.example.com
     {icons.INFORMATION} Branch: develop
     {icons.INFORMATION} Auto-deploy: Enabled

> {icons.GREEN_CIRCLE} 2. Staging              {icons.ARROW_LEFT} SELECTED
     {icons.INFORMATION} URL: https://staging.example.com
     {icons.INFORMATION} Branch: main
     {icons.INFORMATION} Manual approval required

  {icons.FIRE} 3. Production
     {icons.WARNING} URL: https://example.com
     {icons.WARNING} Branch: main
     {icons.WARNING} Requires 2FA + approval

─────────────────────────────────────────────────────────────
{icons.CHECK_MARK_BUTTON} Confirm [Y/n] | {icons.CROSS_MARK} Cancel [Ctrl+C]
""",
    title=f"{icons.GLOBE_WITH_MERIDIANS} Environment Selection",
    border="rounded",
    border_color="magenta",
    width=70,
)

console.newline()

# ============================================================================
# WIZARD INTERFACE
# ============================================================================

console.rule(f"{icons.SPARKLES} SETUP WIZARD", style="green")
console.newline()

console.frame(
    f"""
{icons.GEAR} Application Setup Wizard

{icons.CHECK_MARK_BUTTON} Step 1: Choose Database      [COMPLETED]
    Selected: PostgreSQL

{icons.CHECK_MARK_BUTTON} Step 2: Configure Connection [COMPLETED]
    Host: localhost
    Port: 5432

> {icons.GEAR} Step 3: Create Admin User    [CURRENT]
    ┌────────────────────────────────────────────┐
    │ Username: admin                            │
    │ Email: admin@example.com                   │
    │ Password: ••••••••                         │
    │ Confirm: ••••••••                          │
    └────────────────────────────────────────────┘

  {icons.YELLOW_CIRCLE} Step 4: Set Preferences      [PENDING]

  {icons.YELLOW_CIRCLE} Step 5: Review & Confirm     [PENDING]

─────────────────────────────────────────────────────────────
{icons.ARROW_RIGHT} Continue [Enter] | {icons.ARROW_LEFT} Back [P] | {icons.CROSS_MARK} Cancel [C]

Progress: 3/5 steps (60%)
""",
    title=f"{icons.SPARKLES} Setup Wizard (Step 3/5)",
    border="double",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# MULTI-SELECT INTERFACE
# ============================================================================

console.rule(f"{icons.PACKAGE} MULTI-SELECT", style="cyan")
console.newline()

console.frame(
    f"""
{icons.PACKAGE} Select Components to Install:

{icons.CHECK_MARK_BUTTON} [X] Core Application (required)
  {icons.INFORMATION} 145 MB | Essential application files

{icons.CHECK_MARK_BUTTON} [X] Web Server (nginx)
  {icons.INFORMATION} 23 MB | HTTP server and reverse proxy

{icons.CHECK_MARK_BUTTON} [X] Database (PostgreSQL)
  {icons.INFORMATION} 287 MB | Relational database system

{icons.GREEN_CIRCLE} [X] Cache Server (Redis)
  {icons.INFORMATION} 12 MB | In-memory data store

{icons.YELLOW_CIRCLE} [ ] Monitoring Tools
  {icons.INFORMATION} 67 MB | Metrics, logs, and dashboards

{icons.YELLOW_CIRCLE} [ ] Development Tools
  {icons.INFORMATION} 234 MB | Debuggers, profilers, analyzers

{icons.YELLOW_CIRCLE} [ ] Documentation
  {icons.INFORMATION} 45 MB | API docs and tutorials

─────────────────────────────────────────────────────────────
Selected: 4 components | Total size: 467 MB

{icons.INFORMATION} Use Space to toggle | Enter to continue
""",
    title=f"{icons.WRENCH} Component Selection",
    border="solid",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# NESTED MENU
# ============================================================================

console.rule(f"{icons.FILE_FOLDER} NESTED NAVIGATION", style="blue")
console.newline()

console.frame(
    f"""
{icons.WRENCH} Database Tools

{icons.FLOPPY_DISK} 1. Migrations
   {icons.ARROW_RIGHT} Pending: 3 | Applied: 47 | Status: Up to date

{icons.PACKAGE} 2. Backup & Restore
   {icons.ARROW_RIGHT} Last backup: 2 hours ago

{icons.TEST_TUBE} 3. Database Health Check
   {icons.ARROW_RIGHT} Status: {icons.GREEN_CIRCLE} All checks passed

{icons.BAR_CHART} 4. Performance Analysis
   {icons.ARROW_RIGHT} Query stats, slow queries, indexes

{icons.GEAR} 5. Connection Management
   {icons.ARROW_RIGHT} Pool: 42/100 active | Settings

{icons.ARROW_LEFT} 9. Back to Main Menu

─────────────────────────────────────────────────────────────

{icons.FLOPPY_DISK} Migrations {icons.ARROW_RIGHT} [1]

  {icons.CHART_INCREASING} 1. View Migration Status
  {icons.ROCKET} 2. Run Pending Migrations
  {icons.ARROW_LEFT} 3. Rollback Last Migration
  {icons.SCROLL} 4. Create New Migration
  {icons.ARROW_LEFT} 9. Back

─────────────────────────────────────────────────────────────
Select option:
""",
    title=f"{icons.WRENCH} Tools {icons.ARROW_RIGHT} Database {icons.ARROW_RIGHT} Migrations",
    border="rounded",
    border_color="blue",
    width=75,
)

console.newline()

# ============================================================================
# ACTION CONFIRMATION
# ============================================================================

console.rule(f"{icons.WARNING} CONFIRMATION DIALOGS", style="yellow")
console.newline()

console.frame(
    f"""
{icons.WARNING} Confirm Destructive Action

You are about to delete the database:

  Name: production_backup_2025_11_01
  Size: 4.2 GB
  Created: 2025-11-01 02:00:00
  Tables: 47
  Records: ~2.4M

{icons.CROSS_MARK} This action cannot be undone!

─────────────────────────────────────────────────────────────

Type "DELETE" to confirm:

{icons.INFORMATION} Or press Ctrl+C to cancel
""",
    title=f"{icons.POLICE_CAR_LIGHT} Destructive Action Warning",
    border="thick",
    border_color="red",
    width=70,
)

console.newline()

# ============================================================================
# QUICK ACTIONS MENU
# ============================================================================

console.rule(f"{icons.FIRE} QUICK ACTIONS", style="magenta")
console.newline()

console.frame(
    f"""
{icons.FIRE} Quick Actions (Press key to execute)

[1] {icons.ROCKET} Deploy to Staging        [6] {icons.BAR_CHART} View Metrics
[2] {icons.TEST_TUBE} Run Tests                    [7] {icons.SCROLL} View Logs
[3] {icons.FLOPPY_DISK} Backup Database          [8] {icons.LAPTOP} SSH to Server
[4] {icons.GEAR} Restart Services          [9] {icons.CALENDAR} View Schedule
[5] {icons.WRENCH} Clear Cache               [0] {icons.LIGHT_BULB} Help

─────────────────────────────────────────────────────────────
{icons.INFORMATION} Shortcuts: [Q]uit | [R]efresh | [H]elp
""",
    title=f"{icons.FIRE} Quick Actions Panel",
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
{icons.BULLSEYE} MENU DESIGN PRINCIPLES

1. VISUAL HIERARCHY
   • Title: Clear context, where am I?
   • Options: Numbered or lettered
   • Descriptions: Brief explanation below option
   • Current selection: Highlighted with {icons.ARROW_LEFT} or >

2. NAVIGATION CLARITY
   • Show breadcrumbs: Menu > Submenu > Action
   • Back option: Always [9] or [B] for consistency
   • Exit option: [0], [Q], or Ctrl+C
   • Shortcuts: Single-key for common actions

3. OPTION FORMATTING
   {icons.GREEN_CIRCLE} [1] Action Name
      {icons.INFORMATION} Brief description or current state
   • Emoji: Visual category indicator
   • Number: Quick selection
   • Description: What will happen

4. STATUS INDICATORS
   {icons.CHECK_MARK_BUTTON} Completed or enabled
   {icons.GEAR} Currently running or active
   {icons.YELLOW_CIRCLE} Pending or disabled
   {icons.WARNING} Requires attention
   {icons.CROSS_MARK} Error or unavailable

5. INTERACTIVE ELEMENTS
   • Show available keys: [1-6, 0]
   • Indicate current step: (3/5)
   • Progress bars: ━━━━━░░░░░
   • Confirmation: Type keyword or press Y/N
""",
    title=f"{icons.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
MENU PATTERNS:

{icons.ROCKET} MAIN MENU
  Numbered options, brief descriptions
  Use: Application entry point, top-level navigation

{icons.GEAR} CONFIGURATION MENU
  Current values shown, options to change
  Use: Settings, preferences, system config

{icons.BULLSEYE} SELECTION INTERFACE
  Options with preview/details
  Use: Choosing from alternatives, environments

{icons.SPARKLES} SETUP WIZARD
  Multi-step process, progress indicator
  Use: Installers, onboarding, complex config

{icons.PACKAGE} MULTI-SELECT
  Checkboxes [X] [ ], Space to toggle
  Use: Component selection, feature flags

{icons.FILE_FOLDER} NESTED NAVIGATION
  Breadcrumbs, hierarchical menus
  Use: Complex tools, file browsers

{icons.WARNING} CONFIRMATION DIALOGS
  Destructive actions require explicit confirm
  Use: Delete, reset, deploy to production

{icons.FIRE} QUICK ACTIONS
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
    title=f"{icons.BOOKMARK} Menu Patterns Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{icons.SPARKLES} Well-designed menus make CLI apps intuitive and efficient!")
