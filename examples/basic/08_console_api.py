"""Console API Examples - Main entry point for StyledConsole.

This example demonstrates the Console class, which is the primary interface
for using StyledConsole. It wraps all rendering functionality in a convenient
high-level API.
"""

from styledconsole import Console

print("=" * 80)
print("CONSOLE API EXAMPLES")
print("=" * 80)
print()

# ============================================================================
# Example 1: Basic Console Initialization
# ============================================================================
print("Example 1: Basic Console Initialization")
print("-" * 80)

# Simple initialization
console = Console()

# With recording for HTML export
console_rec = Console(record=True)

# With terminal detection disabled
console_no_detect = Console(detect_terminal=False)

# With custom width
console_wide = Console(width=120)

print("✓ Console initialized with various configurations")
print()

# ============================================================================
# Example 2: Frame Rendering
# ============================================================================
print("Example 2: Frame Rendering")
print("-" * 80)

console.frame("Hello, World!", title="Greeting", border="solid")
print()

console.frame(
    ["Multiple lines", "in a frame", "with different borders"], title="Multi-line", border="double"
)
print()

console.frame(
    "Colored frame content",
    title="Colors",
    border="rounded",
    content_color="lime",
    border_color="cyan",
)
print()

# ============================================================================
# Example 3: Banner Rendering
# ============================================================================
print("Example 3: Banner Rendering")
print("-" * 80)

console.banner("SUCCESS", font="slant")
print()

console.banner(
    "DEMO",
    font="banner",
    start_color="red",
    end_color="blue",
)
print()

console.banner(
    "FRAMED",
    font="slant",
    border="double",
    start_color="green",
    end_color="blue",
)
print()

# ============================================================================
# Example 4: Styled Text
# ============================================================================
print("Example 4: Styled Text")
print("-" * 80)

console.text("Normal text")
console.text("Bold text", bold=True)
console.text("Italic text", italic=True)
console.text("Underlined text", underline=True)
console.text("Dim text", dim=True)
print()

console.text("Red text", color="red", bold=True)
console.text("Green text", color="green", bold=True)
console.text("Blue text", color="blue", bold=True)
console.text("Yellow text", color="yellow", bold=True)
print()

console.text("Combined: ", end="")
console.text("bold", bold=True, end=" ")
console.text("and", end=" ")
console.text("italic", italic=True, end=" ")
console.text("and", end=" ")
console.text("colored", color="cyan", end="")
console.text("!")
print()

# ============================================================================
# Example 5: Rules (Horizontal Dividers)
# ============================================================================
print("Example 5: Rules (Horizontal Dividers)")
print("-" * 80)

console.rule()
console.newline()

console.rule("Section Title", color="blue")
console.newline()

console.rule("Left Aligned", color="green", align="left")
console.newline()

console.rule("Right Aligned", color="red", align="right")
print()

# ============================================================================
# Example 6: Spacing with Newlines
# ============================================================================
print("Example 6: Spacing with Newlines")
print("-" * 80)

console.text("Line 1")
console.newline()
console.text("Line 2 (1 blank line above)")
console.newline(3)
console.text("Line 3 (3 blank lines above)")
print()

# ============================================================================
# Example 7: Complete Workflow - Welcome Screen
# ============================================================================
print("Example 7: Complete Workflow - Welcome Screen")
print("-" * 80)

console.banner("WELCOME", font="slant")
console.newline()

console.rule("About", color="cyan")
console.frame(
    [
        "StyledConsole - Modern terminal output library",
        "",
        "Features:",
        "  • Beautiful frames and borders",
        "  • ASCII art banners",
        "  • Color gradients",
        "  • Emoji support",
        "  • HTML export",
    ],
    title="Description",
    border="double",
    width=60,
)
console.newline()

console.rule("Status", color="green")
console.text("✓ Ready to use", color="green", bold=True)
print()

# ============================================================================
# Example 8: Status Report
# ============================================================================
print("Example 8: Status Report")
print("-" * 80)

console.rule("System Status", color="blue")
console.newline()

console.frame("CPU: 45%", title="Performance", border="solid", width=30)
console.frame("Memory: 2.1GB / 8GB", title="Resources", border="solid", width=30)
console.frame("Disk: 120GB free", title="Storage", border="solid", width=30)
console.newline()

console.text("Status: ", end="")
console.text("Operational", color="green", bold=True)
print()

# ============================================================================
# Example 9: Error Display
# ============================================================================
print("Example 9: Error Display")
print("-" * 80)

console.banner("ERROR", font="slant")
console.newline()

console.frame(
    [
        "Connection Failed",
        "",
        "Unable to connect to database server.",
        "Please check your configuration.",
    ],
    title="Error Details",
    border="heavy",
    content_color="red",
)
console.newline()

console.text("Suggestion: ", bold=True, end="")
console.text("Verify your database credentials and network connection.", color="yellow")
print()

# ============================================================================
# Example 10: Recording and HTML Export
# ============================================================================
print("Example 10: Recording and HTML Export")
print("-" * 80)

# Create console with recording enabled
rec_console = Console(record=True, detect_terminal=False)

# Generate content
rec_console.banner("REPORT", font="slant")
rec_console.newline()
rec_console.rule("Summary", color="blue")
rec_console.frame(
    ["Item 1: Complete", "Item 2: Complete", "Item 3: Pending"],
    title="Status",
    border="double",
)
rec_console.newline()
rec_console.text("Overall: ", end="")
rec_console.text("In Progress", color="yellow", bold=True)

# Export to HTML
html_output = rec_console.export_html(inline_styles=True)

print(f"✓ Generated HTML export: {len(html_output)} characters")
print(f"  First 100 chars: {html_output[:100]}...")
print()

# ============================================================================
# Example 11: Configuration Display
# ============================================================================
print("Example 11: Configuration Display")
print("-" * 80)

console.rule("Application Configuration", color="cyan")
console.newline()

configs = [
    ("Database", ["Host: localhost", "Port: 5432", "User: admin"]),
    ("Cache", ["Type: Redis", "Host: localhost:6379", "TTL: 3600s"]),
    ("API", ["URL: https://api.example.com", "Timeout: 30s", "Retries: 3"]),
]

for title, settings in configs:
    console.frame(settings, title=title, border="solid", width=50)
    console.newline()

# ============================================================================
# Example 12: Test Results Display
# ============================================================================
print("Example 12: Test Results Display")
print("-" * 80)

console.banner("TESTS", font="slant")
console.newline()

console.rule("Results", color="green")
console.frame(
    [
        "Total: 150 tests",
        "Passed: 145 ✓",
        "Failed: 3 ✗",
        "Skipped: 2 ⊝",
        "",
        "Coverage: 97.5%",
        "Duration: 3.2s",
    ],
    title="Test Summary",
    border="double",
    start_color="lime",
    end_color="darkgreen",
)
console.newline()

console.text("Status: ", bold=True, end="")
console.text("PASSING", color="green", bold=True)
print()

# ============================================================================
# Example 13: Terminal Detection
# ============================================================================
print("Example 13: Terminal Detection")
print("-" * 80)

detected_console = Console(detect_terminal=True)

if detected_console.terminal_profile:
    profile = detected_console.terminal_profile

    console.frame(
        [
            f"ANSI Support: {'Yes' if profile.ansi_support else 'No'}",
            f"Color Depth: {profile.color_depth} colors",
            f"Emoji Safe: {'Yes' if profile.emoji_safe else 'No'}",
            f"Width: {profile.width} columns",
            f"Height: {profile.height} lines",
            f"Terminal: {profile.term or 'Unknown'}",
        ],
        title="Terminal Capabilities",
        border="rounded",
    )
else:
    console.text("Terminal detection disabled", color="yellow")

print()

# ============================================================================
# Example 14: Dashboard Layout
# ============================================================================
print("Example 14: Dashboard Layout")
print("-" * 80)

console.banner("STATUS", font="slant")
console.newline()

console.rule("Metrics", color="blue")
console.newline()

# Row 1
console.frame("⚡ 3.2ms", title="Response Time", border="solid", width=25)
console.frame("🔄 1,234", title="Requests/min", border="solid", width=25)
console.frame("💾 45%", title="CPU Usage", border="solid", width=25)
console.newline()

# Row 2
console.frame("🌐 Online", title="Service", border="solid", width=25, content_color="green")
console.frame("✓ Healthy", title="Database", border="solid", width=25, content_color="green")
console.frame("⚠️ Warning", title="Disk", border="solid", width=25, content_color="yellow")
console.newline()

console.rule("Health", color="green")
console.text("✓ All systems operational", color="green", bold=True)
print()

# ============================================================================
# Example 15: Direct Rich Console Access
# ============================================================================
print("Example 15: Direct Rich Console Access")
print("-" * 80)

# For advanced use cases, access Rich console directly
console.print("[bold blue]Rich markup:[/bold blue] [red]colored[/red] [green]text[/green]")
console.print("[italic yellow]This uses Rich's markup syntax directly[/italic yellow]")
print()

print("=" * 80)
print("All Console API examples completed!")
print("=" * 80)
