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

from styledconsole import Console, icons

console = Console()

# ============================================================================
# SIMPLE WELCOME
# ============================================================================

console.banner("WELCOME SCREENS")
console.text("Application launch and splash screen patterns")
console.newline()

console.frame(
    f"""
{icons.SPARKLES} Welcome to MyApp!

Version: 2.3.1
Build: a7f3e92
Released: November 8, 2025

{icons.ROCKET} Ready to start building amazing things!

Type 'help' for available commands or 'start' to begin.
""",
    title=f"{icons.STAR} MyApp CLI",
    border="rounded",
    border_color="cyan",
    width=70,
)

console.newline()

# ============================================================================
# DETAILED SPLASH SCREEN
# ============================================================================

console.rule(f"{icons.ROCKET} DETAILED LAUNCH", style="magenta")
console.newline()

console.banner("APPLICATION SUITE")
console.newline()

console.frame(
    f"""
{icons.PACKAGE} Application Suite v2.3.1

{icons.INFORMATION} Build Information
  Version: 2.3.1 (stable)
  Commit: a7f3e92b
  Built: 2025-11-08 14:23:15 UTC
  Build time: 3m 42s
  Platform: linux-x64

{icons.LAPTOP} System Information
  OS: Ubuntu 22.04.3 LTS
  Kernel: 6.2.0-36-generic
  CPU: AMD Ryzen 9 5950X (32 cores)
  Memory: 64 GB
  Python: 3.11.6

{icons.GEAR} Environment
  Config: /etc/myapp/config.yaml
  Logs: /var/log/myapp/
  Data: /var/lib/myapp/
  Mode: production

{icons.SPARKLES} All systems ready!
""",
    title=f"{icons.ROCKET} System Startup",
    border="double",
    border_color="magenta",
    width=75,
)

console.newline()

# ============================================================================
# INITIALIZATION WITH CHECKS
# ============================================================================

console.rule(f"{icons.GEAR} STARTUP CHECKS", style="green")
console.newline()

console.frame(
    f"""
{icons.GEAR} Initializing Application...

{icons.CHECK_MARK_BUTTON} Configuration loaded       /etc/myapp/config.yaml
{icons.CHECK_MARK_BUTTON} Environment validated      production
{icons.CHECK_MARK_BUTTON} Database connected         PostgreSQL 15.4
{icons.CHECK_MARK_BUTTON} Cache service ready        Redis 7.2.3
{icons.CHECK_MARK_BUTTON} Message queue connected    RabbitMQ 3.12.8
{icons.CHECK_MARK_BUTTON} Storage initialized        S3 (us-east-1)
{icons.CHECK_MARK_BUTTON} Monitoring configured      Prometheus + Grafana
{icons.CHECK_MARK_BUTTON} Logging configured         /var/log/myapp/

{icons.TEST_TUBE} Running health checks...
{icons.CHECK_MARK_BUTTON} API endpoints: 47/47 responding
{icons.CHECK_MARK_BUTTON} Background workers: 8/8 ready
{icons.CHECK_MARK_BUTTON} Scheduled jobs: 12/12 loaded
{icons.CHECK_MARK_BUTTON} Plugins: 5/5 initialized

{icons.ROCKET} Application ready! (startup time: 2.8s)
""",
    title=f"{icons.CHECK_MARK_BUTTON} Startup Complete",
    border="rounded",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# FIRST-TIME SETUP WELCOME
# ============================================================================

console.rule(f"{icons.SPARKLES} FIRST-TIME SETUP", style="cyan")
console.newline()

console.frame(
    f"""
{icons.SPARKLES} Welcome to MyApp!

This appears to be your first time running MyApp.
Let's get you set up quickly!

{icons.GEAR} What we'll do:
  1. {icons.FLOPPY_DISK} Create configuration files
  2. {icons.FILE_FOLDER} Set up data directories
  3. {icons.LOCKED} Configure security settings
  4. {icons.LAPTOP} Create admin account
  5. {icons.TEST_TUBE} Run initial health check

{icons.ONE_OCLOCK} Estimated time: ~3 minutes

{icons.LIGHT_BULB} You can skip setup with --skip-setup flag
{icons.INFORMATION} Configuration can be changed later in settings

─────────────────────────────────────────────────────────────
Press Enter to begin setup or Ctrl+C to exit
""",
    title=f"{icons.STAR} First Time Setup",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

# ============================================================================
# DEVELOPER MODE SPLASH
# ============================================================================

console.rule(f"{icons.WRENCH} DEVELOPMENT MODE", style="yellow")
console.newline()

console.frame(
    f"""
{icons.WRENCH} MyApp - Development Mode

{icons.WARNING} Running in DEVELOPMENT mode

{icons.GEAR} Development Features Enabled:
  {icons.CHECK_MARK_BUTTON} Hot reload: Enabled
  {icons.CHECK_MARK_BUTTON} Debug logging: Verbose
  {icons.CHECK_MARK_BUTTON} Source maps: Enabled
  {icons.CHECK_MARK_BUTTON} CORS: Permissive (all origins)
  {icons.CHECK_MARK_BUTTON} Auth: Relaxed (tokens optional)
  {icons.WARNING} SQL logging: Enabled (may impact performance)

{icons.LAPTOP} Development Server
  URL: http://localhost:3000
  API: http://localhost:3000/api
  Docs: http://localhost:3000/docs
  Admin: http://localhost:3000/admin

{icons.INFORMATION} Quick Commands:
  • npm run dev: Start dev server
  • npm run test: Run test suite
  • npm run lint: Check code style
  • npm run build: Build for production

{icons.WARNING} Not for production use!
""",
    title=f"{icons.WARNING} Development Environment",
    border="thick",
    border_color="yellow",
    width=75,
)

console.newline()

# ============================================================================
# CREDITS AND INFO
# ============================================================================

console.rule(f"{icons.STAR} ABOUT SCREEN", style="blue")
console.newline()

console.frame(
    f"""
{icons.SPARKLES} MyApp - Application Suite

{icons.INFORMATION} Version Information
  Version: 2.3.1 (stable)
  Released: November 8, 2025
  License: MIT
  Website: https://myapp.example.com

{icons.BUSTS_IN_SILHOUETTE} Credits
  Lead Developer: Alice Johnson
  Contributors: 47 awesome people
  GitHub: https://github.com/myorg/myapp
  Issues: https://github.com/myorg/myapp/issues

{icons.BOOKS} Documentation
  User Guide: https://docs.myapp.example.com
  API Reference: https://api.myapp.example.com
  Tutorials: https://learn.myapp.example.com

{icons.LIGHT_BULB} Support
  Email: support@myapp.example.com
  Discord: https://discord.gg/myapp
  Twitter: @myapp_official

{icons.RED_HEART} Thank you for using MyApp!
""",
    title=f"{icons.STAR} About MyApp",
    border="solid",
    border_color="blue",
    width=75,
)

console.newline()

# ============================================================================
# UPDATE AVAILABLE NOTICE
# ============================================================================

console.rule(f"{icons.ROCKET} UPDATE NOTIFICATION", style="green")
console.newline()

console.frame(
    f"""
{icons.SPARKLES} New Version Available!

Current version: 2.3.1
Latest version:  2.4.0

{icons.STAR} What's New in 2.4.0:
  {icons.ROCKET} Performance improvements (2x faster queries)
  {icons.LOCKED} Enhanced security features
  {icons.GEAR} New configuration options
  {icons.TEST_TUBE} Improved test coverage (95% → 98%)
  {icons.CROSS_MARK} Bug fixes (12 issues resolved)

{icons.PACKAGE} Update command:
  npm install -g myapp@latest

{icons.SCROLL} Release notes:
  https://github.com/myorg/myapp/releases/v2.4.0

{icons.INFORMATION} You can disable these notifications in settings
""",
    title=f"{icons.BELL} Update Available",
    border="rounded",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# SETUP COMPLETE
# ============================================================================

console.rule(f"{icons.CHECK_MARK_BUTTON} SETUP COMPLETE", style="green")
console.newline()

console.frame(
    f"""
{icons.PARTY_POPPER} Setup Complete!

{icons.CHECK_MARK_BUTTON} Configuration created      /etc/myapp/config.yaml
{icons.CHECK_MARK_BUTTON} Data directory ready       /var/lib/myapp/
{icons.CHECK_MARK_BUTTON} Logs directory ready       /var/log/myapp/
{icons.CHECK_MARK_BUTTON} Admin account created      admin@example.com
{icons.CHECK_MARK_BUTTON} Database initialized       PostgreSQL
{icons.CHECK_MARK_BUTTON} Sample data loaded         47 records

{icons.ROCKET} MyApp is ready to use!

{icons.LIGHT_BULB} Next Steps:
  1. Log in with your admin account
  2. Explore the dashboard at http://localhost:3000
  3. Check out the documentation
  4. Join our community Discord

{icons.INFORMATION} Quick Start Guide:
  myapp start      - Start the application
  myapp status     - Check service status
  myapp help       - View all commands

{icons.SPARKLES} Happy building!
""",
    title=f"{icons.CHECK_MARK_BUTTON} Welcome Aboard!",
    border="double",
    border_color="green",
    width=75,
)

console.newline()

# ============================================================================
# SHUTDOWN SCREEN
# ============================================================================

console.rule(f"{icons.CROSS_MARK} SHUTDOWN", style="red")
console.newline()

console.frame(
    f"""
{icons.GEAR} Shutting down gracefully...

{icons.CHECK_MARK_BUTTON} Stopping web server             [DONE]
{icons.CHECK_MARK_BUTTON} Draining active connections      [DONE] 0/847
{icons.CHECK_MARK_BUTTON} Finishing background jobs        [DONE] 0/3
{icons.CHECK_MARK_BUTTON} Closing database connections     [DONE]
{icons.CHECK_MARK_BUTTON} Flushing cache                   [DONE]
{icons.CHECK_MARK_BUTTON} Saving application state         [DONE]
{icons.CHECK_MARK_BUTTON} Stopping monitoring              [DONE]

{icons.FLOPPY_DISK} Session saved                    /var/lib/myapp/session.dat
{icons.SCROLL} Logs finalized                   /var/log/myapp/

{icons.CHECK_MARK_BUTTON} Application stopped cleanly

{icons.SPARKLES} Goodbye! See you next time.
""",
    title=f"{icons.CROSS_MARK} Shutdown Complete",
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
{icons.BULLSEYE} WELCOME SCREEN PRINCIPLES

1. FIRST IMPRESSIONS
   • Brand identity: Logo, name, tagline
   • Version info: Build, release date
   • Quick orientation: What can I do here?
   • Call to action: Next steps clearly stated

2. INFORMATION HIERARCHY
   {icons.STAR} Most important: App name, version
   {icons.INFORMATION} Supporting: System info, environment
   {icons.GEAR} Details: Configuration, paths
   {icons.LIGHT_BULB} Guidance: Help, documentation links

3. STARTUP SEQUENCE
   • Brief: Don't delay user (< 3s ideal)
   • Informative: Show what's happening
   • Reassuring: {icons.CHECK_MARK_BUTTON} marks for completed steps
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
    title=f"{icons.LIGHT_BULB} Best Practices",
    border="rounded",
    border_color="cyan",
    width=75,
)

console.newline()

console.frame(
    f"""
WELCOME SCREEN TYPES:

{icons.SPARKLES} SIMPLE WELCOME
  App name, version, quick start
  Use: Simple CLIs, focused tools

{icons.ROCKET} DETAILED SPLASH
  Full system info, environment, config
  Use: Complex applications, enterprise tools

{icons.GEAR} STARTUP CHECKS
  Initialization progress, health checks
  Use: Services, servers, distributed systems

{icons.STAR} FIRST-TIME SETUP
  Onboarding, setup wizard
  Use: New installations, complex configuration

{icons.WRENCH} DEVELOPER MODE
  Dev features, warnings, local URLs
  Use: Development builds, debug mode

{icons.BUSTS_IN_SILHOUETTE} CREDITS & ABOUT
  Team, license, documentation links
  Use: About screens, --version output

{icons.BELL} UPDATE NOTIFICATIONS
  New version available, what's new
  Use: Version checks, auto-updates

{icons.PARTY_POPPER} SETUP COMPLETE
  Success confirmation, next steps
  Use: Installation completion, onboarding done

{icons.CROSS_MARK} SHUTDOWN SCREEN
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
    title=f"{icons.BOOKMARK} Screen Types Reference",
    border="double",
    border_color="white",
    width=75,
)

console.rule()
console.text(f"{icons.SPARKLES} Great welcome screens set the tone for a great user experience!")
