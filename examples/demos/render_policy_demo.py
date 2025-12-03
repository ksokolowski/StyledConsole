#!/usr/bin/env python3
"""Demonstration of the RenderPolicy system.

Shows how to use RenderPolicy for environment-aware rendering
and how different policies affect output.
"""

from styledconsole import (
    Console,
    RenderPolicy,
    get_default_policy,
    icons,
    reset_default_policy,
    set_default_policy,
)


def show_policy_info(policy: RenderPolicy, title: str) -> None:
    """Display policy configuration."""
    console = Console()
    console.frame(
        [
            f"unicode: {policy.unicode}",
            f"color: {policy.color}",
            f"emoji: {policy.emoji}",
            f"force_ascii_icons: {policy.force_ascii_icons}",
            "",
            f"border_style_fallback: {policy.border_style_fallback}",
            f"icon_mode: {policy.icon_mode}",
        ],
        title=title,
        border="rounded",
    )


def demo_auto_detection() -> None:
    """Demonstrate automatic environment detection."""
    console = Console()
    console.banner("RenderPolicy", font="small")

    console.frame(
        [
            "RenderPolicy automatically detects your environment",
            "and configures rendering behavior accordingly.",
            "",
            "Environment variables detected:",
            "  • NO_COLOR - Disables color output",
            "  • FORCE_COLOR - Forces color even if not TTY",
            "  • TERM=dumb - Minimal terminal mode",
            "  • CI, GITHUB_ACTIONS, etc. - CI environment",
        ],
        title=f"{icons.GEAR} Auto Detection",
        border="rounded",
    )

    # Show current environment's policy
    policy = RenderPolicy.from_env()
    show_policy_info(policy, f"{icons.INFO} Current Environment Policy")


def demo_factory_methods() -> None:
    """Demonstrate factory methods for common scenarios."""
    console = Console()

    console.frame(
        [
            "RenderPolicy provides factory methods for common scenarios:",
            "",
            "  RenderPolicy.full()       - All features enabled",
            "  RenderPolicy.minimal()    - ASCII only, no colors",
            "  RenderPolicy.ci_friendly() - Colors but no emoji",
            "  RenderPolicy.no_color()   - Respects NO_COLOR standard",
        ],
        title=f"{icons.WRENCH} Factory Methods",
        border="rounded",
    )

    # Show each factory
    policies = [
        (RenderPolicy.full(), "RenderPolicy.full()"),
        (RenderPolicy.minimal(), "RenderPolicy.minimal()"),
        (RenderPolicy.ci_friendly(), "RenderPolicy.ci_friendly()"),
        (RenderPolicy.no_color(), "RenderPolicy.no_color()"),
    ]

    for policy, name in policies:
        show_policy_info(policy, name)


def demo_icon_integration() -> None:
    """Demonstrate policy integration with icons."""
    console = Console()

    console.frame(
        [
            "Policies can control icon rendering mode:",
            "",
            "  policy.apply_to_icons()  - Apply policy to global icons",
            "  policy.icon_mode         - Get effective icon mode",
        ],
        title=f"{icons.STAR} Icon Integration",
        border="rounded",
    )

    # Demonstrate different modes
    print("\nWith emoji-enabled policy:")
    RenderPolicy.full().apply_to_icons()
    print(f"  {icons.CHECK} Success  {icons.CROSS} Error  {icons.WARNING} Warning")

    print("\nWith ASCII-forced policy:")
    RenderPolicy.ci_friendly().apply_to_icons()
    print(f"  {icons.CHECK} Success  {icons.CROSS} Error  {icons.WARNING} Warning")

    # Reset to auto
    from styledconsole.icons import reset_icon_mode

    reset_icon_mode()


def demo_with_override() -> None:
    """Demonstrate policy override."""
    console = Console()

    console.frame(
        [
            "Create modified policies with with_override():",
            "",
            "  base = RenderPolicy.full()",
            "  no_emoji = base.with_override(emoji=False)",
            "",
            "Original policy is unchanged (immutable).",
        ],
        title=f"{icons.REFRESH} Policy Override",
        border="rounded",
    )

    # Demonstrate override
    base = RenderPolicy.full()
    modified = base.with_override(emoji=False, color=False)

    show_policy_info(base, "Original: RenderPolicy.full()")
    show_policy_info(modified, "Modified: with_override(emoji=False, color=False)")


def demo_default_policy() -> None:
    """Demonstrate global default policy."""
    console = Console()

    console.frame(
        [
            "Module-level default policy functions:",
            "",
            "  get_default_policy()    - Get auto-detected policy",
            "  set_default_policy(p)   - Set custom default",
            "  reset_default_policy()  - Re-detect from environment",
        ],
        title=f"{icons.GLOBE_WITH_MERIDIANS} Default Policy",
        border="rounded",
    )

    # Show default policy
    reset_default_policy()
    default = get_default_policy()
    show_policy_info(default, "get_default_policy()")

    # Set custom default
    custom = RenderPolicy.ci_friendly()
    set_default_policy(custom)
    print("\nAfter set_default_policy(RenderPolicy.ci_friendly()):")
    current = get_default_policy()
    show_policy_info(current, "get_default_policy() - now CI-friendly")

    # Reset
    reset_default_policy()


def main() -> None:
    """Run all demos."""
    demo_auto_detection()
    print()
    demo_factory_methods()
    print()
    demo_icon_integration()
    print()
    demo_with_override()
    print()
    demo_default_policy()

    console = Console()
    console.frame(
        [
            f"{icons.CHECK} Auto-detection from environment",
            f"{icons.CHECK} Factory methods for common scenarios",
            f"{icons.CHECK} Icon system integration",
            f"{icons.CHECK} Immutable with override support",
            f"{icons.CHECK} Global default policy management",
        ],
        title=f"{icons.TROPHY} RenderPolicy Features",
        border="double",
        border_color="gold",
    )


if __name__ == "__main__":
    main()
