#!/usr/bin/env python3
"""StyledConsole CLI - Preview and render terminal UIs.

Usage:
    styledconsole demo                    # Interactive feature showcase
    styledconsole render <file>           # Render YAML/JSON config
    styledconsole palette [name]          # List or preview palettes
    styledconsole effects [name]          # List or preview effects
    styledconsole icons [search]          # List or search icons
    styledconsole schema                  # Get JSON Schema path for IDE config
"""

import argparse
import sys
from pathlib import Path


def cmd_demo(args: argparse.Namespace) -> int:
    """Show an interactive demo of StyledConsole features."""
    from styledconsole import Console, EffectSpec, icons
    from styledconsole.enums import Border, Effect

    console = Console()

    # Header
    console.banner("StyledConsole", font="small", effect=Effect.RAINBOW)
    console.newline()

    console.text("[bold]Welcome to StyledConsole![/] Here's what you can do:")
    console.newline()

    # 1. Basic frames
    console.rule("[cyan]1. Frames with Effects[/]")
    console.frame(
        f"{icons.ROCKET} Beautiful terminal output",
        title="Basic Frame",
        border=Border.ROUNDED,
        effect=Effect.OCEAN,
    )
    console.newline()

    # 2. Background gradients
    console.rule("[cyan]2. Background Gradients[/]")
    console.frame(
        [
            f"{icons.CHECK_MARK_BUTTON} API Server    Online",
            f"{icons.CHECK_MARK_BUTTON} Database      Online",
            f"{icons.WARNING} Cache         Warming",
        ],
        title="System Status",
        border=Border.HEAVY,
        effect=EffectSpec.gradient("#6366f1", "#8b5cf6", layer="background"),
    )
    console.newline()

    # 3. Multiple effects
    console.rule("[cyan]3. Effect Presets[/]")
    effects_demo = [
        ("success", "Operation completed"),
        ("warning", "Proceed with caution"),
        ("error", "Action failed"),
        ("info", "Here's some info"),
    ]
    for effect_name, message in effects_demo:
        console.frame(message, effect=effect_name, border=Border.ROUNDED, width=35)
    console.newline()

    # 4. Icons
    console.rule("[cyan]4. Smart Icons (ASCII fallback in CI)[/]")
    console.text(f"  {icons.ROCKET} ROCKET          {icons.CHECK_MARK_BUTTON} CHECK_MARK_BUTTON")
    console.text(f"  {icons.SPARKLES} SPARKLES        {icons.WARNING} WARNING")
    console.text(f"  {icons.FIRE} FIRE            {icons.GEAR} GEAR")
    console.text(f"  {icons.PACKAGE} PACKAGE         {icons.GLOBE_WITH_MERIDIANS} GLOBE")
    console.newline()

    # 5. Palettes
    console.rule("[cyan]5. Color Palettes (90 available)[/]")
    palettes = ["ocean_depths", "city_sunset", "forest_green", "cyberpunk_neon"]
    for palette in palettes:
        console.frame(
            f"{icons.ARTIST_PALETTE} {palette}",
            effect=EffectSpec.from_palette(palette),
            border=Border.ROUNDED,
            width=30,
        )
    console.newline()

    # Footer
    console.rule("[cyan]Learn More[/]")
    console.text("  [bold]Documentation:[/] https://github.com/ksokolowski/StyledConsole")
    console.text("  [bold]Examples:[/]      https://github.com/ksokolowski/StyledConsole-Examples")
    console.text("")
    console.text("  [dim]Try:[/] styledconsole palette --list")
    console.text("  [dim]Try:[/] styledconsole effects --list")
    console.text("  [dim]Try:[/] styledconsole icons rocket")
    console.newline()

    return 0


def cmd_render(args: argparse.Namespace) -> int:
    """Render a YAML/JSON config file."""
    from styledconsole import Console

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return 1

    suffix = file_path.suffix.lower()
    content = file_path.read_text()

    try:
        console = Console()

        if suffix in (".yaml", ".yml"):
            try:
                from styledconsole import load_yaml
            except ImportError:
                msg = "Error: PyYAML required. Install with: pip install styledconsole[yaml]"
                print(msg, file=sys.stderr)
                return 1
            ui = load_yaml(content)
            console.render_object(ui)
        elif suffix == ".json":
            import json

            config = json.loads(content)
            console.render_dict(config)
        else:
            msg = f"Error: Unsupported file type: {suffix} (use .yaml, .yml, or .json)"
            print(msg, file=sys.stderr)
            return 1

        return 0

    except Exception as e:
        print(f"Error rendering {file_path}: {e}", file=sys.stderr)
        return 1


def cmd_palette(args: argparse.Namespace) -> int:
    """List or preview color palettes."""
    from styledconsole import Console, EffectSpec, get_palette, list_palettes
    from styledconsole.enums import Border

    console = Console()

    if args.list or args.name is None:
        # List all palettes
        palettes = sorted(list_palettes())
        console.text(f"[bold]Available Palettes ({len(palettes)}):[/]")
        console.newline()

        # Display in columns
        cols = 3
        for i in range(0, len(palettes), cols):
            row = palettes[i : i + cols]
            console.text("  " + "  ".join(f"{p:25}" for p in row))

        console.newline()
        console.text("[dim]Preview a palette:[/] styledconsole palette <name>")
        return 0

    # Preview specific palette
    name = args.name
    try:
        palette_data = get_palette(name)
        if palette_data is None:
            raise KeyError(f"Unknown palette: '{name}'")
        colors = palette_data.get("colors", [])

        console.text(f"[bold]Palette: {name}[/]")
        console.newline()

        # Show palette colors
        color_list = ", ".join(colors[:6]) + ("..." if len(colors) > 6 else "")
        console.text(f"  Colors ({len(colors)}): {color_list}")
        console.newline()

        # Preview frame with this palette
        console.frame(
            [
                f"Palette: {name}",
                f"Colors: {len(colors)}",
                "",
                "This is how it looks!",
            ],
            title=name,
            effect=EffectSpec.from_palette(name),
            border=Border.ROUNDED,
            width=40,
        )
        console.newline()

        # Also show background variant
        console.frame(
            "Background variant",
            title=f"{name} (background)",
            effect=EffectSpec.from_palette(name, layer="background"),
            border=Border.ROUNDED,
            width=40,
        )

        return 0

    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_effects(args: argparse.Namespace) -> int:
    """List or preview effect presets."""
    from styledconsole import EFFECTS, Console
    from styledconsole.enums import Border, Effect

    console = Console()

    if args.list or args.name is None:
        # List all effects by category
        categories = {
            "Gradients": [
                "fire",
                "ocean",
                "sunset",
                "forest",
                "aurora",
                "gold",
                "mint",
                "peach",
                "steel",
                "lavender",
            ],
            "Rainbows": ["rainbow", "rainbow_pastel", "rainbow_neon", "rainbow_muted"],
            "Themed": ["matrix", "cyberpunk", "vaporwave", "dracula", "nord_aurora", "retro"],
            "Semantic": ["success", "warning", "error", "info", "neutral"],
            "Nature": ["beach", "autumn", "spring_blossom", "winter_frost"],
            "Tech": ["terminal_green", "electric_blue", "cyber_magenta"],
        }

        console.text("[bold]Available Effect Presets:[/]")
        console.newline()

        for category, effects in categories.items():
            console.text(f"  [cyan]{category}:[/] {', '.join(effects)}")

        console.newline()
        console.text("[dim]Preview an effect:[/] styledconsole effects <name>")
        return 0

    # Preview specific effect
    name = args.name
    try:
        # Try to get the effect
        effect = getattr(EFFECTS, name, None) or getattr(Effect, name.upper(), None) or name

        console.text(f"[bold]Effect: {name}[/]")
        console.newline()

        # Preview frame with this effect
        console.frame(
            [
                f"Effect: {name}",
                "",
                "This is how it looks!",
                "Beautiful gradients.",
            ],
            title=name,
            effect=effect,
            border=Border.ROUNDED,
            width=40,
        )

        return 0

    except Exception as e:
        print(f"Error: Unknown effect '{name}': {e}", file=sys.stderr)
        return 1


def cmd_icons(args: argparse.Namespace) -> int:
    """List or search available icons."""
    from styledconsole import Console, icons

    console = Console()
    all_icons = icons.list_icons()

    if args.search:
        # Search for icons
        search = args.search.upper()
        matches = [name for name in all_icons if search in name]

        if not matches:
            console.text(f"[yellow]No icons found matching '{args.search}'[/]")
            return 0

        console.text(f"[bold]Icons matching '{args.search}' ({len(matches)}):[/]")
        console.newline()

        for name in sorted(matches)[:20]:
            icon = getattr(icons, name)
            console.text(f"  {icon}  {name}")

        if len(matches) > 20:
            console.text(f"  [dim]... and {len(matches) - 20} more[/]")

        return 0

    # List all icons (grouped by first letter or limited)
    console.text(f"[bold]Available Icons ({len(all_icons)}):[/]")
    console.newline()

    # Show a sample
    sample_icons = [
        "CHECK_MARK_BUTTON",
        "CROSS_MARK",
        "WARNING",
        "ROCKET",
        "SPARKLES",
        "FIRE",
        "GEAR",
        "PACKAGE",
        "GLOBE_WITH_MERIDIANS",
        "HIGH_VOLTAGE",
        "ARTIST_PALETTE",
        "BAR_CHART",
        "BELL",
        "BOOKMARK",
        "BUG",
        "CALENDAR",
        "CLIPBOARD",
        "CLOUD",
        "COFFEE",
        "CONSTRUCTION",
    ]

    for name in sample_icons:
        if name in all_icons:
            icon = getattr(icons, name)
            console.text(f"  {icon}  {name}")

    console.newline()
    console.text(f"[dim]Showing 20 of {len(all_icons)} icons[/]")
    console.text("[dim]Search icons:[/] styledconsole icons <search>")

    return 0


def cmd_schema(args: argparse.Namespace) -> int:
    """Show JSON Schema path for IDE configuration."""
    from styledconsole.schemas import get_schema_path

    schema_path = get_schema_path()

    if args.json:
        import json

        from styledconsole.schemas import get_schema

        print(json.dumps(get_schema(), indent=2))
        return 0

    if args.path:
        print(schema_path)
        return 0

    # Default: show usage info
    from styledconsole import Console

    console = Console()
    console.text("[bold]StyledConsole JSON Schema[/]")
    console.newline()
    console.text(f"  Path: {schema_path}")
    console.newline()
    console.text("[bold]IDE Configuration:[/]")
    console.newline()
    console.text("  [cyan]VS Code (settings.json):[/]")
    console.text('    "yaml.schemas": {')
    console.text(f'      "{schema_path}": ["*.styledconsole.yaml", "*.sc.yaml"]')
    console.text("    }")
    console.newline()
    console.text("  [cyan]YAML file (inline):[/]")
    console.text(f"    # yaml-language-server: $schema={schema_path}")
    console.newline()
    console.text("  [cyan]JSON file (inline):[/]")
    console.text(f'    "$schema": "{schema_path}"')
    console.newline()
    console.text("[dim]Options:[/]")
    console.text("  styledconsole schema --path   Print path only")
    console.text("  styledconsole schema --json   Print schema as JSON")

    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="styledconsole",
        description="StyledConsole CLI - Preview and render beautiful terminal UIs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  styledconsole demo                    Show feature showcase
  styledconsole render config.yaml      Render a config file
  styledconsole palette ocean_depths    Preview a color palette
  styledconsole effects fire            Preview an effect preset
  styledconsole icons rocket            Search for icons
  styledconsole schema                  Get JSON Schema for IDE config

Documentation: https://github.com/ksokolowski/StyledConsole
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # demo command
    demo_parser = subparsers.add_parser("demo", help="Show interactive feature demo")
    demo_parser.set_defaults(func=cmd_demo)

    # render command
    render_parser = subparsers.add_parser("render", help="Render YAML/JSON config file")
    render_parser.add_argument("file", help="Path to YAML or JSON config file")
    render_parser.set_defaults(func=cmd_render)

    # palette command
    palette_parser = subparsers.add_parser("palette", help="List or preview color palettes")
    palette_parser.add_argument("name", nargs="?", help="Palette name to preview")
    palette_parser.add_argument("--list", "-l", action="store_true", help="List all palettes")
    palette_parser.set_defaults(func=cmd_palette)

    # effects command
    effects_parser = subparsers.add_parser("effects", help="List or preview effect presets")
    effects_parser.add_argument("name", nargs="?", help="Effect name to preview")
    effects_parser.add_argument("--list", "-l", action="store_true", help="List all effects")
    effects_parser.set_defaults(func=cmd_effects)

    # icons command
    icons_parser = subparsers.add_parser("icons", help="List or search available icons")
    icons_parser.add_argument("search", nargs="?", help="Search term for icons")
    icons_parser.set_defaults(func=cmd_icons)

    # schema command
    schema_parser = subparsers.add_parser("schema", help="Get JSON Schema for IDE config")
    schema_parser.add_argument("--path", "-p", action="store_true", help="Print path only")
    schema_parser.add_argument("--json", "-j", action="store_true", help="Print schema JSON")
    schema_parser.set_defaults(func=cmd_schema)

    args = parser.parse_args()

    if args.command is None:
        # No command given - show demo
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
