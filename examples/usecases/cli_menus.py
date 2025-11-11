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
  {EMOJI.INFO} Launch the main application server

{EMOJI.GEAR} 2. Configuration
  {EMOJI.INFO} Manage application settings and preferences

{EMOJI.CHART_BAR} 3. View Logs
  {EMOJI.INFO} Browse application logs and monitoring data

{EMOJI.TEST_TUBE} 4. Run Tests
  {EMOJI.INFO} Execute test suites and validation

{EMOJI.WRENCH} 5. Database Tools
  {EMOJI.INFO} Database migrations, backups, and maintenance

{EMOJI.GLOBE} 6. Deployment
  {EMOJI.INFO} Deploy application to various environments

{EMOJI.LIGHTBULB} 7. Help & Documentation
  {EMOJI.INFO} View documentation and get help

{EMOJI.CROSS} 0. Exit
  {EMOJI.INFO} Close the application

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

{EMOJI.COMPUTER} Environment: production
{EMOJI.FLOPPY} Database: PostgreSQL (prod-db-01.internal)
{EMOJI.CARD_FILE_BOX} Cache: Redis (prod-cache-01.internal)
{EMOJI.LOCK} Security: TLS 1.3 enabled

─────────────────────────────────────────────────────────────

{EMOJI.GEAR} Configuration Options:

  {EMOJI.CHECK} 1. Change Environment
     Current: production
     Options: development, staging, production

  {EMOJI.FLOPPY} 2. Database Settings
     Connection, pool size, timeout

  {EMOJI.CARD_FILE_BOX} 3. Cache Configuration
     Type, TTL, max memory

  {EMOJI.LOCK} 4. Security Settings
     TLS, authentication, session timeout

  {EMOJI.GLOBE} 5. Network Settings
     Port, host, workers, timeouts

  {EMOJI.CHART_BAR} 6. Logging & Monitoring
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

console.rule(f"{EMOJI.TARGET} SELECTION INTERFACE", style="magenta")
console.newline()

console.frame(
    f"""
{EMOJI.ROCKET} Select Deployment Environment:

  {EMOJI.COMPUTER} 1. Development
     {EMOJI.INFO} URL: https://dev.example.com
     {EMOJI.INFO} Branch: develop
     {EMOJI.INFO} Auto-deploy: Enabled

> {EMOJI.GREEN_CIRCLE} 2. Staging              {EMOJI.ARROW_LEFT} SELECTED
     {EMOJI.INFO} URL: https://staging.example.com
     {EMOJI.INFO} Branch: main
     {EMOJI.INFO} Manual approval required

  {EMOJI.FIRE} 3. Production
     {EMOJI.WARNING} URL: https://example.com
     {EMOJI.WARNING} Branch: main
     {EMOJI.WARNING} Requires 2FA + approval

─────────────────────────────────────────────────────────────
{EMOJI.CHECK} Confirm [Y/n] | {EMOJI.CROSS} Cancel [Ctrl+C]
""",
    title=f"{EMOJI.GLOBE} Environment Selection",
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

{EMOJI.CHECK} Step 1: Choose Database      [COMPLETED]
    Selected: PostgreSQL

{EMOJI.CHECK} Step 2: Configure Connection [COMPLETED]
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
{EMOJI.ARROW_RIGHT} Continue [Enter] | {EMOJI.ARROW_LEFT} Back [P] | {EMOJI.CROSS} Cancel [C]

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

{EMOJI.CHECK} [X] Core Application (required)
  {EMOJI.INFO} 145 MB | Essential application files

{EMOJI.CHECK} [X] Web Server (nginx)
  {EMOJI.INFO} 23 MB | HTTP server and reverse proxy

{EMOJI.CHECK} [X] Database (PostgreSQL)
  {EMOJI.INFO} 287 MB | Relational database system

{EMOJI.GREEN_CIRCLE} [X] Cache Server (Redis)
  {EMOJI.INFO} 12 MB | In-memory data store

{EMOJI.YELLOW_CIRCLE} [ ] Monitoring Tools
  {EMOJI.INFO} 67 MB | Metrics, logs, and dashboards

{EMOJI.YELLOW_CIRCLE} [ ] Development Tools
  {EMOJI.INFO} 234 MB | Debuggers, profilers, analyzers

{EMOJI.YELLOW_CIRCLE} [ ] Documentation
  {EMOJI.INFO} 45 MB | API docs and tutorials

─────────────────────────────────────────────────────────────
Selected: 4 components | Total size: 467 MB

{EMOJI.INFO} Use Space to toggle | Enter to continue
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

console.rule(f"{EMOJI.FOLDER} NESTED NAVIGATION", style="blue")
console.newline()

console.frame(
    f"""
{EMOJI.WRENCH} Database Tools

{EMOJI.FLOPPY} 1. Migrations
   {EMOJI.ARROW_RIGHT} Pending: 3 | Applied: 47 | Status: Up to date

{EMOJI.PACKAGE} 2. Backup & Restore
   {EMOJI.ARROW_RIGHT} Last backup: 2 hours ago

{EMOJI.TEST_TUBE} 3. Database Health Check
   {EMOJI.ARROW_RIGHT} Status: {EMOJI.GREEN_CIRCLE} All checks passed

{EMOJI.CHART_BAR} 4. Performance Analysis
   {EMOJI.ARROW_RIGHT} Query stats, slow queries, indexes

{EMOJI.GEAR} 5. Connection Management
   {EMOJI.ARROW_RIGHT} Pool: 42/100 active | Settings

{EMOJI.ARROW_LEFT} 9. Back to Main Menu

─────────────────────────────────────────────────────────────

{EMOJI.FLOPPY} Migrations {EMOJI.ARROW_RIGHT} [1]

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

{EMOJI.CROSS} This action cannot be undone!

─────────────────────────────────────────────────────────────

Type "DELETE" to confirm:

{EMOJI.INFO} Or press Ctrl+C to cancel
""",
    title=f"{EMOJI.SIREN} Destructive Action Warning",
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

[1] {EMOJI.ROCKET} Deploy to Staging        [6] {EMOJI.CHART_BAR} View Metrics
[2] {EMOJI.TEST_TUBE} Run Tests                    [7] {EMOJI.SCROLL} View Logs
[3] {EMOJI.FLOPPY} Backup Database          [8] {EMOJI.COMPUTER} SSH to Server
[4] {EMOJI.GEAR} Restart Services          [9] {EMOJI.CALENDAR} View Schedule
[5] {EMOJI.WRENCH} Clear Cache               [0] {EMOJI.LIGHTBULB} Help

─────────────────────────────────────────────────────────────
{EMOJI.INFO} Shortcuts: [Q]uit | [R]efresh | [H]elp
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
{EMOJI.TARGET} MENU DESIGN PRINCIPLES

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
      {EMOJI.INFO} Brief description or current state
   • Emoji: Visual category indicator
   • Number: Quick selection
   • Description: What will happen

4. STATUS INDICATORS
   {EMOJI.CHECK} Completed or enabled
   {EMOJI.GEAR} Currently running or active
   {EMOJI.YELLOW_CIRCLE} Pending or disabled
   {EMOJI.WARNING} Requires attention
   {EMOJI.CROSS} Error or unavailable

5. INTERACTIVE ELEMENTS
   • Show available keys: [1-6, 0]
   • Indicate current step: (3/5)
   • Progress bars: ━━━━━░░░░░
   • Confirmation: Type keyword or press Y/N
""",
    title=f"{EMOJI.LIGHTBULB} Best Practices",
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

{EMOJI.TARGET} SELECTION INTERFACE
  Options with preview/details
  Use: Choosing from alternatives, environments

{EMOJI.SPARKLES} SETUP WIZARD
  Multi-step process, progress indicator
  Use: Installers, onboarding, complex config

{EMOJI.PACKAGE} MULTI-SELECT
  Checkboxes [X] [ ], Space to toggle
  Use: Component selection, feature flags

{EMOJI.FOLDER} NESTED NAVIGATION
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
