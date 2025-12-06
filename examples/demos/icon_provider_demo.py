#!/usr/bin/env python3
"""Demo: Icon Provider with Emoji/ASCII Fallback.

This example demonstrates the Icon Provider system that automatically
switches between Unicode emojis and colored ASCII based on terminal
capabilities.

Features shown:
- Automatic terminal detection
- Manual mode switching (emoji/ascii/auto)
- Colored ASCII fallbacks
- Various icon categories
"""

from styledconsole import Console, get_icon_mode, icons, set_icon_mode

console = Console()


def demo_auto_mode() -> None:
    """Show icons in auto-detection mode."""
    console.frame(
        f"""In 'auto' mode, icons automatically render as:
• Emoji if terminal supports it
• Colored ASCII if emoji is unsafe

Current mode: {get_icon_mode()}
Terminal emoji safe: detected automatically""",
        title=f"{icons.GEAR} Auto Mode",
        border="rounded",
    )

    console.text("")
    console.text("Status icons:")
    console.text(f"  {icons.CHECK_MARK_BUTTON} Success    {icons.CROSS_MARK} Error")
    console.text(f"  {icons.WARNING} Warning    {icons.INFORMATION} Info")
    console.text("")


def demo_emoji_mode() -> None:
    """Force emoji mode."""
    set_icon_mode("emoji")
    console.frame(
        f"""Mode: {get_icon_mode()}
Icons always render as Unicode emojis.

{icons.ROCKET} Rocket  {icons.STAR} Star  {icons.FIRE} Fire
{icons.TROPHY} Trophy  {icons.BULLSEYE} Target  {icons.LIGHT_BULB} Idea""",
        title=f"{icons.SPARKLES} Emoji Mode",
        border="rounded",
        border_color="cyan",
    )
    console.text("")


def demo_ascii_mode() -> None:
    """Force ASCII mode with colors."""
    set_icon_mode("ascii")
    console.frame(
        f"""Mode: {get_icon_mode()}
Icons render as colored ASCII symbols.

Status:
  {icons.CHECK_MARK_BUTTON} Success (green)
  {icons.CROSS_MARK} Error (red)
  {icons.WARNING} Warning (yellow)
  {icons.INFORMATION} Info (cyan)

Objects:
  {icons.ROCKET} Rocket  {icons.STAR} Star  {icons.FILE_FOLDER} Folder
  {icons.GEAR} Gear    {icons.LOCKED} Lock  {icons.KEY} Key""",
        title="[*] ASCII Mode",  # Manual ASCII since we're in ASCII mode
        border="rounded",
        border_color="yellow",
    )
    console.text("")


def demo_colored_indicators() -> None:
    """Show colored circle indicators."""
    set_icon_mode("ascii")
    console.text("Colored indicators (ASCII mode):")
    console.text(
        f"  {icons.RED_CIRCLE} Critical  "
        f"{icons.YELLOW_CIRCLE} Warning  "
        f"{icons.GREEN_CIRCLE} OK  "
        f"{icons.BLUE_CIRCLE} Info"
    )
    console.text("")


def demo_test_output() -> None:
    """Simulate test output in both modes."""
    # Emoji mode
    set_icon_mode("emoji")
    console.text("Test Results (emoji mode):")
    console.text(f"  {icons.CHECK_MARK_BUTTON} test_login_success")
    console.text(f"  {icons.CHECK_MARK_BUTTON} test_logout")
    console.text(f"  {icons.CROSS_MARK} test_payment_timeout")
    console.text(f"  {icons.WARNING} test_slow_query (2.5s)")
    console.text("")

    # ASCII mode
    set_icon_mode("ascii")
    console.text("Test Results (ASCII mode):")
    console.text(f"  {icons.CHECK_MARK_BUTTON} test_login_success")
    console.text(f"  {icons.CHECK_MARK_BUTTON} test_logout")
    console.text(f"  {icons.CROSS_MARK} test_payment_timeout")
    console.text(f"  {icons.WARNING} test_slow_query (2.5s)")
    console.text("")


def demo_categories() -> None:
    """Show icons from different categories."""
    set_icon_mode("emoji")
    console.frame(
        f"""Transport: {icons.ROCKET} {icons.AIRPLANE} {icons.AUTOMOBILE} {icons.LOCOMOTIVE}
Weather:   {icons.SUN} {icons.CLOUD} {icons.SNOWFLAKE} {icons.HIGH_VOLTAGE}
Nature:    {icons.EVERGREEN_TREE} {icons.SEEDLING} {icons.CHERRY_BLOSSOM} {icons.FIRE}
Tech:      {icons.LAPTOP} {icons.FLOPPY_DISK} {icons.GLOBE_WITH_MERIDIANS} {icons.GEAR}
Activity:  {icons.BULLSEYE} {icons.TROPHY} {icons.PARTY_POPPER} {icons.WRAPPED_GIFT}""",
        title=f"{icons.ARTIST_PALETTE} Icon Categories",
        border="double",
    )
    console.text("")


def main() -> None:
    """Run all demos."""
    console.banner("Icon Provider", font="small", start_color="cyan", end_color="blue")
    console.text("")

    demo_auto_mode()
    demo_emoji_mode()
    demo_ascii_mode()
    demo_colored_indicators()
    demo_test_output()
    demo_categories()

    # Reset to auto
    set_icon_mode("auto")
    console.text(f"Reset to: {get_icon_mode()} mode")
    console.text(f"Total icons available: {len(icons)}")


if __name__ == "__main__":
    main()
