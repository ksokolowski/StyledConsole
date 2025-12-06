#!/usr/bin/env python3
"""
✨ Emoji Showcase Gallery

A comprehensive catalog of Tier 1 safe emojis organized by categories,
demonstrating perfect alignment, visual harmony, and creative applications.

Design Philosophy:
- Only Tier 1 safe emojis (verified cross-platform compatibility)
- Organized by thematic categories for easy discovery
- Show real-world usage patterns
- Demonstrate proper alignment and width handling

Run: python examples/gallery/emojis_showcase.py
"""

from styledconsole import Console
from styledconsole.emojis import EMOJI

console = Console(record=True)


def demo_status_emojis():
    """Status indicators - the workhorses of terminal UI."""
    console.banner("STATUS", font="standard", start_color="green", end_color="red")
    console.newline()

    console.frame(
        f"{EMOJI.CHECK_MARK_BUTTON} Success - Operation completed\n"
        f"{EMOJI.CROSS_MARK} Error - Operation failed\n"
        f"{EMOJI.WARNING} Warning - Proceed with caution\n"
        f"{EMOJI.INFORMATION} Information - Details available\n"
        f"{EMOJI.RED_QUESTION_MARK} Unknown - Status unclear\n\n"
        "The five essential status indicators,\n"
        "Speaking volumes without words.",
        title="🎯 Status Indicators",
        border="rounded",
        border_gradient_start="green",
        border_gradient_end="red",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()

    # Demonstrate in context
    console.frame(
        "BUILD PIPELINE STATUS:\n\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Lint checks passed\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Unit tests passed (427/427)\n"
        f"{EMOJI.WARNING} Coverage at 94% (target: 95%)\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Integration tests passed\n"
        f"{EMOJI.CROSS_MARK} Deployment failed - rollback initiated\n\n"
        "Status emojis provide instant visual feedback.",
        title="💼 Real-World Usage",
        border="solid",
        border_color="cyan",
        content_color="white",
        align="left",
        width=70,
    )
    console.newline(2)


def demo_arrow_emojis():
    """Arrows - direction, navigation, flow."""
    console.banner("ARROWS", font="standard", start_color="cyan", end_color="blue")
    console.newline()

    console.frame(
        f"{EMOJI.ARROW_UP} Up - Previous, increase, upload\n"
        f"{EMOJI.ARROW_DOWN} Down - Next, decrease, download\n"
        f"{EMOJI.ARROW_LEFT} Left - Back, undo, previous\n"
        f"{EMOJI.ARROW_RIGHT} Right - Forward, next, continue\n"
        f"{EMOJI.UP_RIGHT_ARROW} Diagonal - External link, export\n"
        f"{EMOJI.COUNTERCLOCKWISE_ARROWS_BUTTON} Refresh - Reload, retry, restart\n\n"
        "Arrows guide users through interfaces,\n"
        "Pointing the way with visual clarity.",
        title="🧭 Navigation",
        border="rounded",
        border_color="cyan",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()

    # Menu example
    console.frame(
        "MAIN MENU:\n\n"
        f"{EMOJI.ARROW_RIGHT} Deploy Application\n"
        f"{EMOJI.ARROW_RIGHT} View Metrics\n"
        f"{EMOJI.ARROW_RIGHT} Configuration\n"
        f"{EMOJI.ARROW_DOWN} More Options\n\n"
        f"{EMOJI.ARROW_LEFT} Back   "
        f"{EMOJI.COUNTERCLOCKWISE_ARROWS_BUTTON} Refresh   "
        f"{EMOJI.CROSS_MARK} Exit",
        title="📋 Menu Navigation",
        border="solid",
        border_color="blue",
        content_color="white",
        align="left",
        width=70,
    )
    console.newline(2)


def demo_progress_emojis():
    """Progress and time indicators."""
    console.banner("PROGRESS", font="standard", start_color="yellow", end_color="green")
    console.newline()

    console.frame(
        f"{EMOJI.HOURGLASS_DONE} Pending - Waiting to start\n"
        f"{EMOJI.GEAR} In Progress - Currently running\n"
        f"{EMOJI.ROCKET} Launching - Startup phase\n"
        f"{EMOJI.FIRE} Active - High activity\n"
        f"{EMOJI.SPARKLES} Complete - Finished successfully\n"
        f"{EMOJI.ONE_OCLOCK} Scheduled - Queued for later\n\n"
        "Progress emojis show state transitions,\n"
        "Making time visible.",
        title="⏱️  Progress States",
        border="rounded",
        border_gradient_start="yellow",
        border_gradient_end="green",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()

    # Pipeline example
    console.frame(
        "DEPLOYMENT PIPELINE:\n\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Build      (2m 34s) Complete\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Test       (4m 12s) Complete\n"
        f"{EMOJI.GEAR} Deploy     (1m 45s) In Progress...\n"
        f"{EMOJI.HOURGLASS_DONE} Verify    (---) Pending\n"
        f"{EMOJI.HOURGLASS_DONE} Announce  (---) Pending\n\n"
        "Visual progress tracking at a glance.",
        title="🚀 Pipeline Status",
        border="solid",
        border_color="cyan",
        content_color="white",
        align="left",
        width=70,
    )
    console.newline(2)


def demo_tech_emojis():
    """Technology and development emojis."""
    console.banner("TECHNOLOGY", font="standard", start_color="cyan", end_color="purple")
    console.newline()

    console.frame(
        f"{EMOJI.LAPTOP} Computer - System, machine, host\n"
        f"{EMOJI.ROCKET} Rocket - Launch, deploy, fast\n"
        f"{EMOJI.GEAR} Gear - Settings, configuration\n"
        f"{EMOJI.PACKAGE} Package - Module, library, bundle\n"
        f"{EMOJI.FILE_FOLDER} Folder - Directory, collection\n"
        f"{EMOJI.PAGE_FACING_UP} File - Document, data\n"
        f"{EMOJI.LOCKED} Lock - Secure, encrypted, private\n"
        f"{EMOJI.KEY} Key - Authentication, access\n"
        f"{EMOJI.LINK} Link - Connection, reference\n\n"
        "Tech emojis speak the language\n"
        "Of developers worldwide.",
        title="💻 Tech Icons",
        border="rounded",
        border_gradient_start="cyan",
        border_gradient_end="purple",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()

    # System status example
    console.frame(
        "SYSTEM OVERVIEW:\n\n"
        f"{EMOJI.LAPTOP} Hostname: prod-web-01\n"
        f"{EMOJI.PACKAGE} Services: 12 running\n"
        f"{EMOJI.FILE_FOLDER} Storage: 2.4TB / 4TB\n"
        f"{EMOJI.LOCKED} Security: All checks passed\n"
        f"{EMOJI.LINK} Network: 1Gbps up/down\n\n"
        "Tech emojis make system info scannable.",
        title="🖥️  System Status",
        border="solid",
        border_color="cyan",
        content_color="white",
        align="left",
        width=70,
    )
    console.newline(2)


def demo_nature_emojis():
    """Nature and environment emojis."""
    console.banner("NATURE", font="standard", start_color="green", end_color="blue")
    console.newline()

    console.frame(
        f"{EMOJI.EVERGREEN_TREE} Tree - Growth, branching, stability\n"
        f"{EMOJI.SEEDLING} Seedling - New, starting, potential\n"
        f"{EMOJI.LEAF_FLUTTERING_IN_WIND} Leaf - Natural, organic, green\n"
        f"{EMOJI.FIRE} Fire - Energy, danger, heat\n"
        f"{EMOJI.DROPLET} Water - Flow, liquid, clean\n"
        f"{EMOJI.STAR} Star - Favorite, important, rating\n"
        f"{EMOJI.SPARKLES} Sparkles - Magic, special, new\n"
        f"{EMOJI.RAINBOW} Rainbow - Colorful, complete, joy\n\n"
        "Nature emojis bring organic warmth\n"
        "To digital interfaces.",
        title="🌳 Natural Elements",
        border="rounded",
        border_gradient_start="green",
        border_gradient_end="blue",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()

    # Environment monitoring
    console.frame(
        "ENVIRONMENT METRICS:\n\n"
        f"{EMOJI.EVERGREEN_TREE} Carbon offset: 2.4 tons\n"
        f"{EMOJI.LEAF_FLUTTERING_IN_WIND} Green energy: 85%\n"
        f"{EMOJI.DROPLET} Water usage: -12% YoY\n"
        f"{EMOJI.SEEDLING} New initiatives: 3 started\n"
        f"{EMOJI.STAR} Sustainability score: 4.7/5\n\n"
        "Nature emojis for environmental metrics.",
        title="🌍 Sustainability Dashboard",
        border="solid",
        border_color="green",
        content_color="white",
        align="left",
        width=70,
    )
    console.newline(2)


def demo_symbol_emojis():
    """Symbols and shapes."""
    console.banner("SYMBOLS", font="standard", start_color="yellow", end_color="orange")
    console.newline()

    console.frame(
        f"{EMOJI.BELL} Bell - Notification, alert, reminder\n"
        f"{EMOJI.TROPHY} Trophy - Achievement, success, winner\n"
        f"{EMOJI.BULLSEYE} Target - Goal, objective, aim\n"
        f"{EMOJI.SHIELD} Shield - Protection, security, safe\n"
        f"{EMOJI.CROWN} Crown - Premium, royal, best\n"
        f"{EMOJI.GEM_STONE} Diamond - Valuable, rare, premium\n"
        f"{EMOJI.RED_HEART} Heart - Favorite, like, love\n"
        f"{EMOJI.HIGH_VOLTAGE} Lightning - Fast, powerful, energy\n\n"
        "Symbols convey meaning instantly,\n"
        "Transcending language barriers.",
        title="⚡ Universal Symbols",
        border="rounded",
        border_gradient_start="yellow",
        border_gradient_end="red",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()

    # Achievements example
    console.frame(
        "ACHIEVEMENTS UNLOCKED:\n\n"
        f"{EMOJI.TROPHY} First Deployment - Completed\n"
        f"{EMOJI.CROWN} Zero Downtime Week - Achieved\n"
        f"{EMOJI.GEM_STONE} 99.99% Uptime - Maintained\n"
        f"{EMOJI.BULLSEYE} Performance Goals - Met\n"
        f"{EMOJI.SHIELD} Security Audit - Passed\n\n"
        "Symbols celebrate accomplishments.",
        title="🏆 Achievement Board",
        border="solid",
        border_color="gold",
        content_color="white",
        align="left",
        width=70,
    )
    console.newline(2)


def demo_emoji_combinations():
    """Creative emoji combinations for richer meaning."""
    console.banner("COMBINATIONS", font="standard", start_color="purple", end_color="cyan")
    console.newline()

    combinations = [
        {
            "title": "🚀 Rocket Launch",
            "pattern": f"{EMOJI.ROCKET}{EMOJI.SPARKLES}",
            "meaning": "Exciting deployment or major release",
        },
        {
            "title": "⚠️  Critical Warning",
            "pattern": f"{EMOJI.WARNING}{EMOJI.FIRE}",
            "meaning": "Urgent issue requiring immediate attention",
        },
        {
            "title": "✅ Complete Success",
            "pattern": f"{EMOJI.CHECK_MARK_BUTTON}{EMOJI.TROPHY}",
            "meaning": "Task completed with exceptional results",
        },
        {
            "title": "🔒 Secure Connection",
            "pattern": f"{EMOJI.LOCKED}{EMOJI.CHECK_MARK_BUTTON}",
            "meaning": "Security verified and active",
        },
        {
            "title": "📦 Package Ready",
            "pattern": f"{EMOJI.PACKAGE}{EMOJI.ROCKET}",
            "meaning": "Build complete and ready to deploy",
        },
        {
            "title": "🌟 Featured Item",
            "pattern": f"{EMOJI.STAR}{EMOJI.CROWN}",
            "meaning": "Top-tier or premium feature",
        },
    ]

    for combo in combinations:
        console.frame(
            f"Pattern: {combo['pattern']}\n\n"
            f"Meaning: {combo['meaning']}\n\n"
            "Two emojis together create\n"
            "Richer, more nuanced meaning.",
            title=combo["title"],
            border="rounded",
            border_color="cyan",
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def demo_emoji_best_practices():
    """Guidelines for effective emoji usage."""
    console.banner("BEST PRACTICES", font="standard", start_color="magenta", end_color="cyan")
    console.newline()

    practices = [
        {
            "title": "✅ DO: Use Consistently",
            "text": f"{EMOJI.CHECK_MARK_BUTTON} Stick to one emoji per status type\n"
            f"{EMOJI.CHECK_MARK_BUTTON} Always use {EMOJI.CHECK_MARK_BUTTON} for success\n"
            f"{EMOJI.CHECK_MARK_BUTTON} Always use {EMOJI.CROSS_MARK} for errors\n\n"
            "Consistency builds user familiarity.",
            "color": "green",
        },
        {
            "title": "✅ DO: Consider Context",
            "text": f"{EMOJI.ROCKET} Rocket for deployments (exciting!)\n"
            f"{EMOJI.GEAR} Gear for processing (neutral)\n"
            f"{EMOJI.HOURGLASS_DONE} Hourglass for waiting (patient)\n\n"
            "Match emoji energy to the situation.",
            "color": "cyan",
        },
        {
            "title": "❌ DON'T: Overuse",
            "text": "Too many emojis become visual noise.\n"
            "Use them purposefully, not decoratively.\n\n"
            "One emoji per line is usually enough.",
            "color": "orange",
        },
        {
            "title": "✅ DO: Test Alignment",
            "text": "Emojis have variable width.\n"
            "Always test your layouts!\n\n"
            "StyledConsole handles this automatically.",
            "color": "blue",
        },
        {
            "title": "✅ DO: Provide Text Fallback",
            "text": f"{EMOJI.CHECK_MARK_BUTTON} Build succeeded\n"
            f"{EMOJI.CROSS_MARK} Build failed\n\n"
            "Never rely on emoji alone.\n"
            "Text ensures clarity for all users.",
            "color": "purple",
        },
    ]

    for practice in practices:
        console.frame(
            practice["text"],
            title=practice["title"],
            border="thick",
            border_color=practice["color"],
            content_color="white",
            align="center",
            width=70,
        )
        console.newline()

    console.newline()


def demo_emoji_catalog():
    """Complete catalog of all Tier 1 safe emojis."""
    console.banner("CATALOG", font="banner", start_color="red", end_color="violet")
    console.newline()

    console.text(
        "Complete reference of all Tier 1 safe emojis.\nVerified for cross-platform compatibility.",
        color="cyan",
        italic=True,
    )
    console.newline()

    categories = [
        {
            "name": "Status & Alerts",
            "emojis": [
                (EMOJI.CHECK_MARK_BUTTON, "Check"),
                (EMOJI.CROSS_MARK, "Cross"),
                (EMOJI.WARNING, "Warning"),
                (EMOJI.INFORMATION, "Info"),
                (EMOJI.RED_QUESTION_MARK, "Question"),
            ],
        },
        {
            "name": "Arrows & Navigation",
            "emojis": [
                (EMOJI.ARROW_UP, "Up"),
                (EMOJI.ARROW_DOWN, "Down"),
                (EMOJI.ARROW_LEFT, "Left"),
                (EMOJI.ARROW_RIGHT, "Right"),
                (EMOJI.UP_RIGHT_ARROW, "Up-Right"),
                (EMOJI.COUNTERCLOCKWISE_ARROWS_BUTTON, "Refresh"),
            ],
        },
        {
            "name": "Progress & Time",
            "emojis": [
                (EMOJI.HOURGLASS_DONE, "Hourglass"),
                (EMOJI.ONE_OCLOCK, "Clock"),
                (EMOJI.GEAR, "Gear"),
                (EMOJI.ROCKET, "Rocket"),
                (EMOJI.SPARKLES, "Sparkles"),
            ],
        },
        {
            "name": "Technology",
            "emojis": [
                (EMOJI.LAPTOP, "Computer"),
                (EMOJI.PACKAGE, "Package"),
                (EMOJI.FILE_FOLDER, "Folder"),
                (EMOJI.PAGE_FACING_UP, "File"),
                (EMOJI.LOCKED, "Lock"),
                (EMOJI.KEY, "Key"),
                (EMOJI.LINK, "Link"),
            ],
        },
        {
            "name": "Nature",
            "emojis": [
                (EMOJI.EVERGREEN_TREE, "Tree"),
                (EMOJI.SEEDLING, "Seedling"),
                (EMOJI.LEAF_FLUTTERING_IN_WIND, "Leaf"),
                (EMOJI.FIRE, "Fire"),
                (EMOJI.DROPLET, "Water"),
                (EMOJI.RAINBOW, "Rainbow"),
            ],
        },
        {
            "name": "Symbols",
            "emojis": [
                (EMOJI.BELL, "Bell"),
                (EMOJI.TROPHY, "Trophy"),
                (EMOJI.BULLSEYE, "Target"),
                (EMOJI.SHIELD, "Shield"),
                (EMOJI.CROWN, "Crown"),
                (EMOJI.GEM_STONE, "Diamond"),
                (EMOJI.RED_HEART, "Heart"),
                (EMOJI.HIGH_VOLTAGE, "Lightning"),
                (EMOJI.STAR, "Star"),
            ],
        },
    ]

    for category in categories:
        emoji_list = "\n".join([f"{emoji} {name}" for emoji, name in category["emojis"]])
        console.frame(
            emoji_list,
            title=f"{EMOJI.BOOKS} {category['name']}",
            border="rounded",
            border_color="cyan",
            content_color="white",
            align="left",
            width=50,
        )
        console.newline()

    console.newline()


def demo_creative_showcase():
    """Creative artistic emoji compositions."""
    console.banner("CREATIVE", font="banner", start_color="red", end_color="violet")
    console.newline()

    # Emoji art
    console.frame(
        f"        {EMOJI.STAR}\n"
        f"       {EMOJI.SPARKLES}{EMOJI.SPARKLES}\n"
        f"      {EMOJI.STAR}{EMOJI.SPARKLES}{EMOJI.STAR}\n"
        f"     {EMOJI.SPARKLES}{EMOJI.CROWN}{EMOJI.SPARKLES}\n"
        f"    {EMOJI.STAR}{EMOJI.SPARKLES}{EMOJI.SPARKLES}{EMOJI.STAR}\n"
        f"   {EMOJI.SPARKLES}{EMOJI.SPARKLES}{EMOJI.TROPHY}{EMOJI.SPARKLES}{EMOJI.SPARKLES}\n"
        f"  {EMOJI.STAR}{EMOJI.SPARKLES}{EMOJI.SPARKLES}{EMOJI.SPARKLES}{EMOJI.STAR}\n\n"
        "Achievement pyramid!\n"
        "Emojis as ASCII art.",
        title=f"{EMOJI.ARTIST_PALETTE} Emoji Art",
        border="double",
        border_gradient_start="yellow",
        border_gradient_end="orange",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Progress bar with emojis
    console.frame(
        "Build Progress:\n\n"
        f"{EMOJI.CHECK_MARK_BUTTON}{EMOJI.CHECK_MARK_BUTTON}{EMOJI.CHECK_MARK_BUTTON}{EMOJI.CHECK_MARK_BUTTON}{EMOJI.CHECK_MARK_BUTTON}"
        f"{EMOJI.CHECK_MARK_BUTTON}{EMOJI.CHECK_MARK_BUTTON}{EMOJI.GEAR}{EMOJI.HOURGLASS_DONE}{EMOJI.HOURGLASS_DONE}\n\n"
        "70% Complete\n\n"
        "Emojis as progress indicators!",
        title=f"{EMOJI.BAR_CHART} Visual Progress",
        border="rounded",
        border_gradient_start="lime",
        border_gradient_end="green",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline()

    # Emoji timeline
    console.frame(
        "Deployment Timeline:\n\n"
        f"{EMOJI.SEEDLING} Planning   (Week 1)\n"
        f"     {EMOJI.ARROW_DOWN}\n"
        f"{EMOJI.GEAR} Development (Week 2-3)\n"
        f"     {EMOJI.ARROW_DOWN}\n"
        f"{EMOJI.ROCKET} Launch      (Week 4)\n"
        f"     {EMOJI.ARROW_DOWN}\n"
        f"{EMOJI.TROPHY} Success!    (Week 5)\n\n"
        "Emojis tell stories over time.",
        title=f"{EMOJI.CALENDAR} Timeline",
        border="solid",
        border_color="cyan",
        content_color="white",
        align="center",
        width=60,
    )
    console.newline(2)


def main():
    """Run the complete emoji showcase."""
    console.rule(f"{EMOJI.SPARKLES} EMOJI SHOWCASE GALLERY", color="magenta")
    console.newline()

    console.text(
        "A comprehensive catalog of Tier 1 safe emojis.\n"
        "Learn when, where, and how to use them effectively.\n"
        "Transform your terminal UI with universal visual language.",
        color="cyan",
        italic=True,
    )
    console.newline(2)

    # Category demonstrations
    demo_status_emojis()
    demo_arrow_emojis()
    demo_progress_emojis()
    demo_tech_emojis()
    demo_nature_emojis()
    demo_symbol_emojis()

    # Advanced usage
    demo_emoji_combinations()
    demo_emoji_best_practices()
    demo_emoji_catalog()
    demo_creative_showcase()

    # Finale
    console.rule(f"{EMOJI.SPARKLES}", color="magenta")
    console.newline()
    console.frame(
        f"{EMOJI.TROPHY} EMOJI MASTERY ACHIEVED\n\n"
        "You've explored:\n\n"
        f"{EMOJI.CHECK_MARK_BUTTON} 50+ Tier 1 safe emojis\n"
        f"{EMOJI.CHECK_MARK_BUTTON} 6 thematic categories\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Creative combinations\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Best practices guide\n"
        f"{EMOJI.CHECK_MARK_BUTTON} Real-world applications\n\n"
        "Emojis are the universal language\n"
        "Of modern terminal interfaces.\n\n"
        f"Now go forth and communicate visually! {EMOJI.ROCKET}{EMOJI.SPARKLES}",
        title=f"{EMOJI.CROWN} Gallery Complete",
        border="double",
        border_gradient_start="red",
        border_gradient_end="purple",
        content_color="white",
        align="center",
        width=70,
    )
    console.newline()


if __name__ == "__main__":
    main()
