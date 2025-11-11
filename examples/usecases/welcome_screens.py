#!/usr/bin/env python3
"""
Use Case: Welcome Screens

Real-world welcome and splash screen patterns for CLI applications.
Shows how to create engaging launch screens with version info, system
checks, and initialization status.

Use cases:
- Application startup screens
- Tool launch interfaces
- System initialization displays
- Version and credits screens
- Setup completion screens
"""

from styledconsole import Console
from styledconsole.emojis import EMOJI

console = Console()

# ============================================================================
# SIMPLE WELCOME
# ============================================================================

console.banner("WELCOME SCREENS")
console.text("Application launch and splash screen patterns")
console.newline()

console.frame(
    f"""
{EMOJI.SPARKLES} Welcome to MyApp!

Version: 2.3.1
Build: a7f3e92
Released: November 8, 2025

{EMOJI.ROCKET} Ready to start building amazing things!

Type 'help' for available commands or 'start' to begin.
""",
    title=f"{EMOJI.STAR} MyApp CLI",
    border="rounded",
    border_color="cyan",
    width=70,
)

console.newline()

# ============================================================================
# DETAILED SPLASH SCREEN
# ============================================================================

console.rule(f"{EMOJI.ROCKET} DETAILED LAUNCH", style="magenta")
console.newline()

console.banner("APPLICATION SUITE")
console.newline()

console.frame(
    f"""
{EMOJI.PACKAGE} Application Suite v2.3.1

{EMOJI.INFO} Build Information
  Version: 2.3.1 (stable)
  Commit: a7f3e92b
  Built: 2025-11-08 14:23:15 UTC
  Build time: 3m 42s
  Platform: linux-x64

{EMOJI.COMPUTER} System Information
  OS: Ubuntu 22.04.3 LTS
  Kernel: 6.2.0-36-generic
  CPU: AMD Ryzen 9 5950X (32 cores)
  Memory: 64 GB
  Python: 3.11.6

{EMOJI.GEAR} Environment
  Config: /etc/myapp/config.yaml
  Logs: /var/log/myapp/
  Data: /var/lib/myapp/
  Mode: production

{EMOJI.SPARKLES} All systems ready!
""",
    title=f"{EMOJI.ROCKET} System Startup",
    border="double",
    border_color="magenta",
    width=75,
)

console.newline()

# ============================================================================
# INITIALIZATION WITH CHECKS
# ============================================================================

console.rule(f"{EMOJI.GEAR} STARTUP CHECKS", style="green")
console.newline()

console.frame(
    f"""
{EMOJI.GEAR} Initializing Application...

{EMOJI.CHECK} Configuration loaded       /etc/myapp/config.yaml
{EMOJI.CHECK} Environment validated      production
{EMOJI.CHECK} Database connected         PostgreSQL 15.4
{EMOJI.CHECK} Cache service ready        Redis 7.2.3
{EMOJI.CHECK} Message queue connected    RabbitMQ 3.12.8
{EMOJI.CHECK} Storage initialized        S3 (us-east-1)
{EMOJI.CHECK} Monitoring configured      Prometheus + Grafana
{EMOJI.CHECK} Logging configured         /var/log/myapp/

{EMOJI.TEST_TUBE} Running health checks...
{EMOJI.CHECK} API endpoints: 47/47 responding
{EMOJI.CHECK} Background workers: 8/8 ready
{EMOJI.CHECK} Scheduled jobs: 12/12 loaded
{EMOJI.CHECK} Plugins: 5/5 initialized

{EMOJI.ROCKET} Application ready! (startup time: 2.8s)
""",
    title=f"{EMOJI.CHECK} Startup Complete",
    border="rounded",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# FIRST-TIME SETUP WELCOME
# ============================================================================

console.rule(f"{EMOJI.SPARKLES} FIRST-TIME SETUP", style="cyan")
console.newline()

console.frame(
    f"""
{EMOJI.SPARKLES} Welcome to MyApp!

This appears to be your first time running MyApp.
Let's get you set up quickly!

{EMOJI.GEAR} What we'll do:
  1. {EMOJI.FLOPPY} Create configuration files
  2. {EMOJI.FOLDER} Set up data directories
  3. {EMOJI.LOCK} Configure security settings
  4. {EMOJI.COMPUTER} Create admin account
  5. {EMOJI.TEST_TUBE} Run initial health check

{EMOJI.CLOCK} Estimated time: ~3 minutes

{EMOJI.LIGHTBULB} You can skip setup with --skip-setup flag
{EMOJI.INFO} Configuration can be changed later in settings

─────────────────────────────────────────────────────────────
Press Enter to begin setup or Ctrl+C to exit
""",
    title=f"{EMOJI.STAR} First Time Setup",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# DEVELOPER MODE SPLASH
# ============================================================================

console.rule(f"{EMOJI.WRENCH} DEVELOPMENT MODE", style="yellow")
console.newline()

console.frame(
    f"""
{EMOJI.WRENCH} MyApp - Development Mode

{EMOJI.WARNING} Running in DEVELOPMENT mode

{EMOJI.GEAR} Development Features Enabled:
  {EMOJI.CHECK} Hot reload: Enabled
  {EMOJI.CHECK} Debug logging: Verbose
  {EMOJI.CHECK} Source maps: Enabled
  {EMOJI.CHECK} CORS: Permissive (all origins)
  {EMOJI.CHECK} Auth: Relaxed (tokens optional)
  {EMOJI.WARNING} SQL logging: Enabled (may impact performance)

{EMOJI.COMPUTER} Development Server
  URL: http://localhost:3000
  API: http://localhost:3000/api
  Docs: http://localhost:3000/docs
  Admin: http://localhost:3000/admin

{EMOJI.INFO} Quick Commands:
  • npm run dev: Start dev server
  • npm run test: Run test suite
  • npm run lint: Check code style
  • npm run build: Build for production

{EMOJI.WARNING} Not for production use!
""",
    title=f"{EMOJI.WARNING} Development Environment",
    border="thick",
    border_color="yellow",
    width=75,
)

console.newline()

# ============================================================================
# CREDITS AND INFO
# ============================================================================

console.rule(f"{EMOJI.STAR} ABOUT SCREEN", style="blue")
console.newline()

console.frame(
    f"""
{EMOJI.SPARKLES} MyApp - Application Suite

{EMOJI.INFO} Version Information
  Version: 2.3.1 (stable)
  Released: November 8, 2025
  License: MIT
  Website: https://myapp.example.com

{EMOJI.PEOPLE} Credits
  Lead Developer: Alice Johnson
  Contributors: 47 awesome people
  GitHub: https://github.com/myorg/myapp
  Issues: https://github.com/myorg/myapp/issues

{EMOJI.BOOKS} Documentation
  User Guide: https://docs.myapp.example.com
  API Reference: https://api.myapp.example.com
  Tutorials: https://learn.myapp.example.com

{EMOJI.LIGHTBULB} Support
  Email: support@myapp.example.com
  Discord: https://discord.gg/myapp
  Twitter: @myapp_official

{EMOJI.HEART} Thank you for using MyApp!
""",
    title=f"{EMOJI.STAR} About MyApp",
    border="solid",
    border_color="blue",
    width=75,
)

console.newline()

# ============================================================================
# UPDATE AVAILABLE NOTICE
# ============================================================================

console.rule(f"{EMOJI.ROCKET} UPDATE NOTIFICATION", style="green")
console.newline()

console.frame(
    f"""
{EMOJI.SPARKLES} New Version Available!

Current version: 2.3.1
Latest version:  2.4.0

{EMOJI.STAR} What's New in 2.4.0:
  {EMOJI.ROCKET} Performance improvements (2x faster queries)
  {EMOJI.LOCK} Enhanced security features
  {EMOJI.GEAR} New configuration options
  {EMOJI.TEST_TUBE} Improved test coverage (95% → 98%)
  {EMOJI.CROSS} Bug fixes (12 issues resolved)

{EMOJI.PACKAGE} Update command:
  npm install -g myapp@latest

{EMOJI.SCROLL} Release notes:
  https://github.com/myorg/myapp/releases/v2.4.0

{EMOJI.INFO} You can disable these notifications in settings
""",
    title=f"{EMOJI.BELL} Update Available",
    border="rounded",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# SETUP COMPLETE
# ============================================================================

console.rule(f"{EMOJI.CHECK} SETUP COMPLETE", style="green")
console.newline()

console.frame(
    f"""
{EMOJI.PARTY} Setup Complete!

{EMOJI.CHECK} Configuration created      /etc/myapp/config.yaml
{EMOJI.CHECK} Data directory ready       /var/lib/myapp/
{EMOJI.CHECK} Logs directory ready       /var/log/myapp/
{EMOJI.CHECK} Admin account created      admin@example.com
{EMOJI.CHECK} Database initialized       PostgreSQL
{EMOJI.CHECK} Sample data loaded         47 records

{EMOJI.ROCKET} MyApp is ready to use!

{EMOJI.LIGHTBULB} Next Steps:
  1. Log in with your admin account
  2. Explore the dashboard at http://localhost:3000
  3. Check out the documentation
  4. Join our community Discord

{EMOJI.INFO} Quick Start Guide:
  myapp start      - Start the application
  myapp status     - Check service status
  myapp help       - View all commands

{EMOJI.SPARKLES} Happy building!
""",
    title=f"{EMOJI.CHECK} Welcome Aboard!",
    border="double",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# SHUTDOWN SCREEN
# ============================================================================

console.rule(f"{EMOJI.CROSS} SHUTDOWN", style="red")
console.newline()

console.frame(
    f"""
{EMOJI.GEAR} Shutting down gracefully...

{EMOJI.CHECK} Stopping web server             [DONE]
{EMOJI.CHECK} Draining active connections      [DONE] 0/847
{EMOJI.CHECK} Finishing background jobs        [DONE] 0/3
{EMOJI.CHECK} Closing database connections     [DONE]
{EMOJI.CHECK} Flushing cache                   [DONE]
{EMOJI.CHECK} Saving application state         [DONE]
{EMOJI.CHECK} Stopping monitoring              [DONE]

{EMOJI.FLOPPY} Session saved                    /var/lib/myapp/session.dat
{EMOJI.SCROLL} Logs finalized                   /var/log/myapp/

{EMOJI.CHECK} Application stopped cleanly

{EMOJI.SPARKLES} Goodbye! See you next time.
""",
    title=f"{EMOJI.CROSS} Shutdown Complete",
    border="rounded",
    border_color="red",
    width=75,
)

console.newline()

# ============================================================================
# DESIGN GUIDELINES
# ============================================================================

console.banner("WELCOME SCREEN DESIGN")

console.frame(
    f"""
{EMOJI.TARGET} WELCOME SCREEN PRINCIPLES

1. FIRST IMPRESSIONS
   • Brand identity: Logo, name, tagline
   • Version info: Build, release date
   • Quick orientation: What can I do here?
   • Call to action: Next steps clearly stated

2. INFORMATION HIERARCHY
   {EMOJI.STAR} Most important: App name, version
   {EMOJI.INFO} Supporting: System info, environment
   {EMOJI.GEAR} Details: Configuration, paths
   {EMOJI.LIGHTBULB} Guidance: Help, documentation links

3. STARTUP SEQUENCE
   • Brief: Don't delay user (< 3s ideal)
   • Informative: Show what's happening
   • Reassuring: {EMOJI.CHECK} marks for completed steps
   • Actionable: Clear next steps

4. VISUAL STYLE
   • Banner/logo: ASCII art or large text
   • Color coding: Green for ready, yellow for dev mode
   • Emojis: Add personality and visual interest
   • Borders: Frame content professionally

5. CONTEXTUAL CONTENT
   • First run: Setup wizard, onboarding
   • Dev mode: Warnings, dev features
   • Production: System checks, status
   • Updates: What's new, upgrade path
""",
    title=f"{EMOJI.LIGHTBULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
WELCOME SCREEN TYPES:

{EMOJI.SPARKLES} SIMPLE WELCOME
  App name, version, quick start
  Use: Simple CLIs, focused tools

{EMOJI.ROCKET} DETAILED SPLASH
  Full system info, environment, config
  Use: Complex applications, enterprise tools

{EMOJI.GEAR} STARTUP CHECKS
  Initialization progress, health checks
  Use: Services, servers, distributed systems

{EMOJI.STAR} FIRST-TIME SETUP
  Onboarding, setup wizard
  Use: New installations, complex configuration

{EMOJI.WRENCH} DEVELOPER MODE
  Dev features, warnings, local URLs
  Use: Development builds, debug mode

{EMOJI.PEOPLE} CREDITS & ABOUT
  Team, license, documentation links
  Use: About screens, --version output

{EMOJI.BELL} UPDATE NOTIFICATIONS
  New version available, what's new
  Use: Version checks, auto-updates

{EMOJI.PARTY} SETUP COMPLETE
  Success confirmation, next steps
  Use: Installation completion, onboarding done

{EMOJI.CROSS} SHUTDOWN SCREEN
  Graceful shutdown status
  Use: Application exit, cleanup

CONTENT TO INCLUDE:
• App name and version (always)
• Build info (commit, date, platform)
• System requirements met? (check marks)
• Next steps or quick commands
• Documentation/help links
• Credits (for about screens)
""",
    title=f"{EMOJI.BOOKMARK} Screen Types Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{EMOJI.SPARKLES} Great welcome screens set the tone for a great user experience!")
