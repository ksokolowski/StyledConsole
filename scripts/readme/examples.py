#!/usr/bin/env python3
"""README example definitions - single source of truth.

Each example contains:
- code: The Python code to display in README
- generator: Function that generates the corresponding image

All images are rendered on a fixed 80x24 terminal to ensure consistent font size.

Usage:
  uv run python scripts/readme/examples.py  # Generate all images
"""

from pathlib import Path

from styledconsole import Console, RenderPolicy, icons
from styledconsole.export import get_image_theme
from styledconsole.icons import set_icon_mode
from styledconsole.utils.text import set_render_target

# Output directory for generated images (docs/images for GitHub compatibility)
OUTPUT_DIR = Path(__file__).parent.parent.parent / "docs" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_EXPORT_POLICY = RenderPolicy.for_image_export()

# Force emoji mode for image generation (not auto-detect from terminal)
set_icon_mode("emoji")

# Set render target to "image" for consistent emoji width calculations
# This must be set BEFORE calling gradient_frame or other functions that use visual_width
set_render_target("image")

# Fixed terminal size for consistent font rendering across all images
TERMINAL_COLS = 80
TERMINAL_ROWS = 24
ImageTheme = get_image_theme()
FIXED_TERMINAL_THEME = ImageTheme(terminal_size=(TERMINAL_COLS, TERMINAL_ROWS))


# =============================================================================
# EXAMPLE DEFINITIONS
# =============================================================================

EXAMPLES = {}


def example(name: str, code: str):
    """Decorator to register an example with its code."""

    def decorator(func):
        EXAMPLES[name] = {
            "code": code.strip(),
            "generator": func,
        }
        return func

    return decorator


# -----------------------------------------------------------------------------
# Quick Start / Basic Frame
# -----------------------------------------------------------------------------


@example(
    "basic_frame",
    """
from styledconsole import Console, icons

console = Console()

console.frame(
    f"{icons.CHECK_MARK_BUTTON} Build successful\\n"
    f"{icons.ROCKET} Deployed to production",
    title=f"{icons.SPARKLES} Status",
    border="rounded",
    border_gradient_start="green",
    border_gradient_end="cyan",
)
""",
)
def generate_basic_frame():
    """Generate basic frame example - rich visual showcase."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    console.frame(
        [
            f"{icons.CHECK_MARK_BUTTON} Build successful",
            f"{icons.PACKAGE} Dependencies installed",
            f"{icons.GEAR} Configuration loaded",
            f"{icons.ROCKET} Deployed to production",
        ],
        title=f"{icons.SPARKLES} Deployment Status",
        border="rounded",
        border_gradient_start="green",
        border_gradient_end="cyan",
    )
    console.export_webp(
        str(OUTPUT_DIR / "basic_frame.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "basic_frame.webp"


# -----------------------------------------------------------------------------
# Gradient Frame
# -----------------------------------------------------------------------------


@example(
    "gradient_frame",
    """
console.frame(
    "Beautiful gradient borders",
    title="Gradients",
    border="rounded",
    border_gradient_start="cyan",
    border_gradient_end="magenta",
)
""",
)
def generate_gradient_frame():
    """Generate gradient border frame example - rainbow showcase."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    console.frame(
        [
            f"{icons.RAINBOW} Rainbow gradients",
            f"{icons.ARTIST_PALETTE} Custom color schemes",
            f"{icons.FIRE} Hot to cool transitions",
            f"{icons.SNOWFLAKE} Smooth interpolation",
        ],
        title=f"{icons.SPARKLES} Gradient Engine",
        border="double",
        border_gradient_start="magenta",
        border_gradient_end="cyan",
    )
    console.export_webp(
        str(OUTPUT_DIR / "gradient_frame.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "gradient_frame.webp"


# -----------------------------------------------------------------------------
# Nested Frames
# -----------------------------------------------------------------------------


@example(
    "nested_frames",
    """
from styledconsole import Console

console = Console()
inner = console.render_frame("Core", border="double", width=20)
console.frame(["Application Shell", inner], border="heavy", width=40)
""",
)
def generate_nested_frames():
    """Generate nested frames example."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    inner = console.render_frame("Core", border="double", width=20)
    console.frame(["Application Shell", inner], border="heavy", width=40)
    console.export_webp(
        str(OUTPUT_DIR / "nested_frames.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "nested_frames.webp"


# -----------------------------------------------------------------------------
# Rainbow Banner
# -----------------------------------------------------------------------------


@example(
    "rainbow_banner",
    """
# Full ROYGBIV rainbow spectrum
console.banner("RAINBOW", font="slant", rainbow=True)

# Two-color gradient
console.banner("HELLO", font="big", start_color="cyan", end_color="magenta")
""",
)
def generate_rainbow_banner():
    """Generate rainbow banner example - shows both rainbow and gradient styles."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    # Full ROYGBIV rainbow spectrum
    console.banner("RAINBOW", font="slant", rainbow=True)
    console.newline()
    # Two-color gradient
    console.banner("HELLO", font="big", start_color="cyan", end_color="magenta")
    console.export_webp(
        str(OUTPUT_DIR / "rainbow_banner.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "rainbow_banner.webp"


# -----------------------------------------------------------------------------
# Border Styles
# -----------------------------------------------------------------------------


@example(
    "border_styles",
    """
# 8 beautiful border styles available
styles = ["solid", "double", "rounded", "heavy", "dots", "minimal", "thick", "ascii"]
for style in styles:
    console.frame(f"{style}", border=style, width=20)
""",
)
def generate_border_styles():
    """Generate border styles grid (2 columns x 4 rows)."""
    from io import StringIO

    from rich.console import Console as RichConsole
    from rich.table import Table

    from styledconsole.export import get_image_exporter

    styles = ["solid", "double", "rounded", "heavy", "dots", "minimal", "thick", "ascii"]

    rich_console = RichConsole(record=True, width=TERMINAL_COLS, force_terminal=True)

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column()
    table.add_column()

    # Create pairs for 2x4 grid
    pairs = list(zip(styles[::2], styles[1::2], strict=True))

    for left_style, right_style in pairs:
        cells = []
        for style in [left_style, right_style]:
            buffer = StringIO()
            temp = Console(file=buffer, detect_terminal=False, width=36, policy=IMAGE_EXPORT_POLICY)
            temp.frame(style, border=style, width=34)
            frame_text = buffer.getvalue().rstrip()
            from rich.text import Text

            cells.append(Text.from_ansi(frame_text))
        table.add_row(*cells)

    rich_console.print(table)

    image_exporter_cls = get_image_exporter()
    exporter = image_exporter_cls(rich_console, theme=FIXED_TERMINAL_THEME)
    img = exporter._render_frame()
    img = exporter._auto_crop(img, margin=20)
    img.save(str(OUTPUT_DIR / "border_styles.webp"), "WEBP", quality=90)
    return "border_styles.webp"


# -----------------------------------------------------------------------------
# Status Messages
# -----------------------------------------------------------------------------


@example(
    "status_messages",
    """
console.text("Build completed successfully!", color="green")
console.text("Warning: deprecated API", color="yellow")
console.text("Error: connection failed", color="red")
""",
)
def generate_status_messages():
    """Generate status messages example - colorful status showcase."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    console.text(f"{icons.CHECK_MARK_BUTTON} All tests passed (427/427)", color="green", bold=True)
    console.text(f"{icons.CHART_INCREASING} Performance improved by 23%", color="bright_green")
    console.text(f"{icons.WARNING} Cache hit ratio below target", color="yellow")
    console.text(
        f"{icons.HOURGLASS_NOT_DONE} Build taking longer than usual", color="bright_yellow"
    )
    console.text(f"{icons.CROSS_MARK} Connection to database failed", color="red", bold=True)
    console.text(f"{icons.INFORMATION} Retrying in 5 seconds...", color="cyan")
    console.export_webp(
        str(OUTPUT_DIR / "status_messages.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "status_messages.webp"


# -----------------------------------------------------------------------------
# Icons Showcase
# -----------------------------------------------------------------------------


@example(
    "icons_showcase",
    """
from styledconsole import icons

print(f"{icons.ROCKET} Deploying...")  # Auto-detects terminal
print(f"{icons.CHECK_MARK_BUTTON} Done!")
""",
)
def generate_icons_showcase():
    """Generate icons showcase example - diverse icon categories."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    console.text(f"{icons.ROCKET} Deploying to production...", color="cyan")
    console.text(f"{icons.PACKAGE} Installing dependencies...", color="blue")
    console.text(f"{icons.GEAR} Configuring environment...", color="magenta")
    console.text(f"{icons.SHIELD} Security scan passed", color="green")
    console.text(f"{icons.SPARKLES} Optimizations applied", color="yellow")
    console.text(f"{icons.CHECK_MARK_BUTTON} All systems go!", color="bright_green", bold=True)
    console.export_webp(
        str(OUTPUT_DIR / "icons_showcase.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "icons_showcase.webp"


# -----------------------------------------------------------------------------
# Color Palette Showcase
# -----------------------------------------------------------------------------


@example(
    "text_styles",
    """
# Rich color support - named colors and RGB
console.text("Red alert!", color="red")
console.text("Green success", color="green")
console.text("Blue info", color="blue")
console.text("Custom RGB", color="#ff6b6b")
""",
)
def generate_text_styles():
    """Generate color palette showcase - color options available."""
    from rich.text import Text

    from styledconsole.effects import gradient_frame

    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)

    # Add empty line to prevent title clipping with auto_crop
    console._rich_console.print()

    # Color palette frame with emojis
    lines = gradient_frame(
        [
            f"{icons.ARTIST_PALETTE} Named: red, green, blue, cyan...",
            f"{icons.RAINBOW} Bright: bright_red, bright_green...",
            f"{icons.PAINTBRUSH} RGB: #ff6b6b, #4ecdc4, #ffe66d",
            f"{icons.FIRE} ANSI: color0-color255",
        ],
        start_color="#ff6b6b",
        end_color="#4ecdc4",
        target="both",
        border="rounded",
        title=f"{icons.SPARKLES} Color Palette",
    )
    for line in lines:
        console._rich_console.print(Text.from_ansi(line))

    console.export_webp(
        str(OUTPUT_DIR / "text_styles.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "text_styles.webp"


# -----------------------------------------------------------------------------
# Gradient Text
# -----------------------------------------------------------------------------


@example(
    "gradient_text",
    """
from styledconsole.effects import gradient_frame

# Apply gradient to multiline text
lines = gradient_frame(
    ["Welcome to StyledConsole!", "Beautiful gradient text", "Across multiple lines"],
    start_color="cyan",
    end_color="magenta",
    target="content",
)
for line in lines:
    print(line)
""",
)
def generate_gradient_text():
    """Generate gradient text showcase - multiline gradient effect."""
    from rich.text import Text

    from styledconsole.effects import gradient_frame

    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)

    # Add empty line to prevent title clipping with auto_crop
    console._rich_console.print()

    # Gradient text in a frame with emojis
    lines = gradient_frame(
        [
            f"{icons.SPARKLES} Welcome to StyledConsole!",
            f"{icons.RAINBOW} Beautiful gradient text",
            f"{icons.ARTIST_PALETTE} Smooth color transitions",
            f"{icons.FIRE} From cyan to magenta",
        ],
        start_color="cyan",
        end_color="magenta",
        target="both",
        border="double",
        title=f"{icons.PAINTBRUSH} Gradient Text",
    )
    for line in lines:
        # Use Text.from_ansi() to properly render pre-colored ANSI strings
        console._rich_console.print(Text.from_ansi(line))

    console.export_webp(
        str(OUTPUT_DIR / "gradient_text.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "gradient_text.webp"


# -----------------------------------------------------------------------------
# Font Styles Showcase
# -----------------------------------------------------------------------------


@example(
    "font_styles",
    """
from styledconsole import Console

console = Console()

# Text styling with bold, italic, underline, strikethrough
console.text("Bold text for emphasis", bold=True)
console.text("Italic text for style", italic=True)
console.text("Underlined for importance", underline=True)
console.text("Strikethrough for removed", strike=True)

# Combined styles with colors
console.text("Bold + Red + Underline", bold=True, color="red", underline=True)
console.text("Italic + Cyan + Strike", italic=True, color="cyan", strike=True)
""",
)
def generate_font_styles():
    """Generate font styles showcase - bold, italic, underline, strike."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)

    # Add empty line for spacing
    console._rich_console.print()

    # Basic styles - apply to entire lines
    console._rich_console.print("[bold]Bold text for emphasis[/bold]")
    console._rich_console.print("[italic]Italic text for style[/italic]")
    console._rich_console.print("[underline]Underlined for importance[/underline]")
    console._rich_console.print("[strike]Strikethrough for removed[/strike]")
    console._rich_console.print("[dim]Dimmed text for secondary info[/dim]")
    console._rich_console.print()

    # Combined styles with colors
    console._rich_console.print("[bold red underline]Bold + Red + Underline[/bold red underline]")
    console._rich_console.print("[italic cyan strike]Italic + Cyan + Strike[/italic cyan strike]")
    console._rich_console.print(
        "[bold italic underline green]All styles combined![/bold italic underline green]"
    )

    console.export_webp(
        str(OUTPUT_DIR / "font_styles.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "font_styles.webp"


# -----------------------------------------------------------------------------
# CI/CD Pipeline Dashboard
# -----------------------------------------------------------------------------


@example(
    "build_report",
    """
from styledconsole import Console, icons

console = Console()
console.banner("BUILD", font="standard", start_color="blue", end_color="purple")

console.frame([
    f"{icons.CHECK_MARK_BUTTON} Lint checks passed",
    f"{icons.CHECK_MARK_BUTTON} Unit tests: 427/427",
    f"{icons.CHECK_MARK_BUTTON} Integration tests: 52/52",
    f"{icons.WARNING} Coverage: 94% (target: 95%)",
    f"{icons.ROCKET} Deploying to staging...",
], title=f"{icons.BAR_CHART} Pipeline Status", border="heavy", border_color="green")
""",
)
def generate_build_report():
    """Generate CI/CD pipeline dashboard example."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    console.banner("BUILD", font="standard", start_color="blue", end_color="purple")
    console.frame(
        [
            f"{icons.CHECK_MARK_BUTTON} Lint checks passed",
            f"{icons.CHECK_MARK_BUTTON} Unit tests: 427/427",
            f"{icons.CHECK_MARK_BUTTON} Integration tests: 52/52",
            f"{icons.WARNING} Coverage: 94% (target: 95%)",
            f"{icons.ROCKET} Deploying to staging...",
        ],
        title=f"{icons.BAR_CHART} Pipeline Status",
        border="heavy",
        border_color="green",
    )
    console.export_webp(
        str(OUTPUT_DIR / "build_report.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "build_report.webp"


# -----------------------------------------------------------------------------
# Error Reporting
# -----------------------------------------------------------------------------


@example(
    "error_report",
    """
console.frame(
    f"{icons.CROSS_MARK} Connection refused\\n\\n"
    f"   Host: database.example.com:5432\\n"
    f"   Error: ETIMEDOUT after 30s\\n"
    f"   Retry: 3/3 attempts failed\\n\\n"
    f"{icons.LIGHT_BULB} Check firewall settings",
    title=f"{icons.WARNING} Database Error",
    border="heavy",
    border_gradient_start="red",
    border_gradient_end="darkred"
)
""",
)
def generate_error_report():
    """Generate error reporting example."""
    console = Console(record=True, width=TERMINAL_COLS, policy=IMAGE_EXPORT_POLICY)
    console.frame(
        f"{icons.CROSS_MARK} Connection refused\n\n"
        f"   Host: database.example.com:5432\n"
        f"   Error: ETIMEDOUT after 30s\n"
        f"   Retry: 3/3 attempts failed\n\n"
        f"{icons.LIGHT_BULB} Check firewall settings",
        title=f"{icons.WARNING} Database Error",
        border="heavy",
        border_gradient_start="red",
        border_gradient_end="darkred",
    )
    console.export_webp(
        str(OUTPUT_DIR / "error_report.webp"), theme=FIXED_TERMINAL_THEME, auto_crop=True
    )
    return "error_report.webp"


# =============================================================================
# ANIMATION GENERATORS
# =============================================================================


def generate_progress_animation():
    """Generate animated parallel progress bars WebP."""
    from rich.console import Console as RichConsole

    from styledconsole.export import get_image_exporter

    frames = []

    # Simulate 3 parallel tasks with different speeds
    bar_width = 50
    num_frames = 40  # 40 frames for smooth animation

    for frame_idx in range(num_frames + 1):
        rich_console = RichConsole(record=True, width=TERMINAL_COLS, force_terminal=True)

        # Calculate progress for each task
        t = frame_idx / num_frames  # 0.0 to 1.0

        # Stagger the tasks slightly for visual interest
        task1_progress = min(100, int(t * 100 * 1.0))
        task2_progress = min(100, int(t * 100 * 0.85))
        task3_progress = min(100, int(t * 100 * 0.7))

        def make_bar(progress, label, color):
            filled = int(bar_width * progress / 100)
            empty = bar_width - filled
            bar = f"{'━' * filled}{'─' * empty}"
            return f"[{color}]{bar}[/{color}] [bold]{progress:3d}%[/bold] {label}"

        rich_console.print("[bold]✨ Multiple Tasks:[/bold]")
        rich_console.print(make_bar(task1_progress, "Fetching data", "green"))
        rich_console.print(make_bar(task2_progress, "Processing", "cyan"))
        rich_console.print(make_bar(task3_progress, "Saving results", "magenta"))

        image_exporter_cls = get_image_exporter()
        exporter = image_exporter_cls(rich_console, theme=FIXED_TERMINAL_THEME)
        frame = exporter._render_frame()
        frames.append(frame)

    # Auto-crop all frames to common bounding box and save
    if frames:
        image_exporter_cls = get_image_exporter()
        exporter = image_exporter_cls(None, theme=FIXED_TERMINAL_THEME)
        frames = exporter._auto_crop_frames(frames, margin=20)
        frames[0].save(
            str(OUTPUT_DIR / "progress_animation.webp"),
            "WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=80,  # 80ms per frame
            loop=0,
            quality=85,
        )
    print(f"  {icons.CHECK_MARK_BUTTON} progress_animation.webp (animated)")
    return "progress_animation.webp"


def generate_gradient_animation():
    """Generate animated gradient demo - the hero animation for README."""
    from io import StringIO

    from rich.console import Console as RichConsole

    from styledconsole import StyleContext
    from styledconsole.core.styles import get_border_style
    from styledconsole.effects.engine import apply_gradient
    from styledconsole.effects.strategies import (
        Both,
        DiagonalPosition,
        OffsetPositionStrategy,
        RainbowSpectrum,
    )
    from styledconsole.export import get_image_exporter

    # Pre-render the base content (no colors)
    frame_width = 40
    buffer = StringIO()
    temp_console = Console(file=buffer, detect_terminal=False, width=frame_width)

    content = [
        "✨ Animated Gradients ✨",
        "",
        "Powered by StyledConsole",
        "Unified Gradient Engine",
        "",
        "Beautiful terminal output",
    ]

    style = StyleContext(
        border_style="double",
        width=frame_width,
        align="center",
        padding=1,
    )
    temp_console.frame(content, title="🚀 StyledConsole", style=style)
    base_lines = [line.rstrip() for line in buffer.getvalue().splitlines()]

    # Setup gradient strategies
    base_pos_strategy = DiagonalPosition()
    color_source = RainbowSpectrum()
    target_filter = Both()

    # Get border chars for detection
    border_style = get_border_style("double")
    border_chars = {
        border_style.top_left,
        border_style.top_right,
        border_style.bottom_left,
        border_style.bottom_right,
        border_style.horizontal,
        border_style.vertical,
        border_style.left_joint,
        border_style.right_joint,
        border_style.top_joint,
        border_style.bottom_joint,
        border_style.cross,
    }

    frames = []

    # Generate frames for one complete color cycle (loopable)
    num_frames = 30
    for i in range(num_frames):
        offset = i * 0.033

        # Create strategy with current offset
        pos_strategy = OffsetPositionStrategy(base_pos_strategy, offset=offset)

        # Apply gradient
        colored_lines = apply_gradient(
            base_lines, pos_strategy, color_source, target_filter, border_chars
        )

        # Convert ANSI-colored lines to Rich Text for proper parsing
        from rich.text import Text

        ansi_text = "\n".join(colored_lines)
        styled_text = Text.from_ansi(ansi_text)

        # Render to image using Rich console with fixed terminal size
        null_file = StringIO()
        rich_console = RichConsole(
            record=True, width=TERMINAL_COLS, force_terminal=True, file=null_file
        )
        rich_console.print(styled_text)

        image_exporter_cls = get_image_exporter()
        exporter = image_exporter_cls(rich_console, theme=FIXED_TERMINAL_THEME)
        frame = exporter._render_frame()
        frames.append(frame)

    # Auto-crop all frames to common bounding box and save
    if frames:
        image_exporter_cls = get_image_exporter()
        exporter = image_exporter_cls(None, theme=FIXED_TERMINAL_THEME)
        frames = exporter._auto_crop_frames(frames, margin=20)
        frames[0].save(
            str(OUTPUT_DIR / "gradient_animation.webp"),
            "WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=66,  # 66ms per frame = ~15 FPS
            loop=0,  # Infinite loop
            quality=80,  # Lower quality for smaller file
        )
    print(f"  {icons.CHECK_MARK_BUTTON} gradient_animation.webp (animated)")
    return "gradient_animation.webp"


# =============================================================================
# API FUNCTIONS
# =============================================================================


def get_example_code(name: str) -> str:
    """Get the code for an example by name."""
    if name not in EXAMPLES:
        raise KeyError(f"Unknown example: {name}")
    return EXAMPLES[name]["code"]


def generate_example_image(name: str) -> str:
    """Generate image for an example, returns filename."""
    if name not in EXAMPLES:
        raise KeyError(f"Unknown example: {name}")
    return EXAMPLES[name]["generator"]()


def generate_all_images():
    """Generate all example images (static and animated)."""
    print("Generating README images...")

    print("\nStatic images:")
    for name in EXAMPLES:
        filename = generate_example_image(name)
        print(f"  {icons.CHECK_MARK_BUTTON} {filename}")

    print("\nAnimated images:")
    generate_progress_animation()
    generate_gradient_animation()

    print(f"\n{icons.CHECK_MARK_BUTTON} All images generated in {OUTPUT_DIR}/")


def list_examples() -> list[str]:
    """List all available example names."""
    return list(EXAMPLES.keys())


if __name__ == "__main__":
    generate_all_images()
