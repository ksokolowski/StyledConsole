"""Integration tests for Console class.

Tests end-to-end workflows combining multiple Console methods and features.
"""

import io

from styledconsole.console import Console


class TestConsoleBasicWorkflows:
    """Test basic console workflows combining multiple methods."""

    def test_welcome_screen_workflow(self):
        """Test creating a welcome screen with banner, text, and frames."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False, record=True)

        # Welcome banner
        console.banner("WELCOME", font="slant")
        console.newline()

        # Description frame
        console.frame(
            ["Welcome to StyledConsole!", "A modern terminal output library."],
            title="About",
            border="double",
        )
        console.newline()

        # Status text
        console.text("Status: Ready", color="green", bold=True)

        output = buffer.getvalue()

        # Verify all content is present
        assert "WELCOME" in output or "Welcome" in output
        assert "About" in output
        assert "StyledConsole" in output
        assert "Ready" in output

    def test_status_report_workflow(self):
        """Test creating a status report with multiple sections."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        # Header
        console.rule("System Status Report", color="cyan")
        console.newline()

        # Multiple status frames
        console.frame("CPU: 45%", title="Performance")
        console.newline()
        console.frame("Disk: 120GB free", title="Storage")
        console.newline()
        console.frame("Network: Connected", title="Connectivity")

        output = buffer.getvalue()

        assert "System Status Report" in output
        assert "CPU" in output
        assert "Disk" in output
        assert "Network" in output

    def test_error_message_workflow(self):
        """Test creating error messages with banners and frames."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        # Error banner
        console.banner("ERROR", font="slant")
        console.newline()

        # Error details in frame
        console.frame(
            ["Failed to connect to database", "Check your connection settings"],
            title="Details",
            border="heavy",
        )
        console.newline()

        # Suggestion text
        console.text("Suggestion: Verify your credentials", color="yellow")

        output = buffer.getvalue()

        # Banner creates ASCII art, may not have exact word
        assert len(output) > 0
        assert "database" in output
        assert "Suggestion" in output


class TestConsoleRecordingWorkflows:
    """Test Console recording and export workflows."""

    def test_record_and_export_html(self):
        """Test recording output and exporting to HTML."""
        console = Console(record=True, detect_terminal=False)

        # Create content
        console.text("Title", color="blue", bold=True)
        console.frame("Content in a box", title="Frame")
        console.newline()
        console.rule("Section")

        # Export HTML
        html = console.export_html()

        # Verify HTML contains content
        assert isinstance(html, str)
        assert len(html) > 0
        assert "Title" in html
        assert "Content in a box" in html
        assert "Section" in html

    def test_record_and_export_text(self):
        """Test recording output and exporting to plain text."""
        console = Console(record=True, detect_terminal=False)

        # Create styled content
        console.text("Colored text", color="red", bold=True)
        console.frame("Framed content", title="Box", border="solid")

        # Export plain text
        text = console.export_text()

        # Verify text contains content without ANSI codes
        assert isinstance(text, str)
        assert "Colored text" in text
        assert "Framed content" in text
        assert "Box" in text
        assert "\033[" not in text  # No ANSI escape codes

    def test_record_complex_output(self):
        """Test recording complex multi-element output."""
        console = Console(record=True, detect_terminal=False)

        # Complex layout
        console.banner("DEMO", font="slant")
        console.newline()
        console.rule("Section 1", color="blue")
        console.text("First section content", color="white")
        console.newline()
        console.frame(["Line 1", "Line 2", "Line 3"], title="Data", border="double")
        console.newline()
        console.rule("Section 2", color="green")
        console.text("Second section content", color="white")

        # Export HTML (always works with recording)
        html = console.export_html()

        # Verify HTML contains key elements
        assert "Section" in html
        assert "Data" in html
        assert "Line 1" in html


class TestConsoleFrameIntegration:
    """Test frame rendering integration with various options."""

    def test_frames_with_different_borders(self):
        """Test rendering multiple frames with different border styles."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        border_styles = ["solid", "double", "rounded", "heavy", "ascii"]

        for style in border_styles:
            console.frame(f"Border: {style}", title=style.capitalize(), border=style)
            console.newline()

        output = buffer.getvalue()

        for style in border_styles:
            assert style.capitalize() in output

    def test_frames_with_colors_and_gradients(self):
        """Test rendering frames with various color options."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        # Solid color frame
        console.frame(
            "Solid color",
            title="Red Content",
            content_color="red",
            border_color="blue",
        )
        console.newline()

        # Gradient frame
        console.frame(
            ["Line 1", "Line 2", "Line 3"],
            title="Gradient",
            start_color="red",
            end_color="blue",
        )

        output = buffer.getvalue()

        assert "Red Content" in output
        assert "Gradient" in output
        assert "Solid color" in output

    def test_frames_with_alignment(self):
        """Test rendering frames with different alignments."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        for align in ["left", "center", "right"]:
            console.frame(
                f"Aligned {align}",
                title=f"{align.capitalize()} Aligned",
                align=align,
                width=60,
            )
            console.newline()

        output = buffer.getvalue()

        assert "Left Aligned" in output
        assert "Center Aligned" in output
        assert "Right Aligned" in output


class TestConsoleBannerIntegration:
    """Test banner rendering integration with various options."""

    def test_banners_with_different_fonts(self):
        """Test rendering banners with different fonts."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        fonts = ["slant", "standard", "banner"]

        for font in fonts:
            console.banner("HI", font=font)
            console.newline(2)

        output = buffer.getvalue()

        # Should have ASCII art content
        assert len(output) > 0
        lines = output.split("\n")
        assert len(lines) > 10  # Multiple banners with spacing

    def test_banners_with_gradients(self):
        """Test rendering banners with gradient colors."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.banner(
            "OK",
            font="slant",
            start_color="red",
            end_color="blue",
        )
        console.newline()

        console.banner(
            "GO",
            font="slant",
            start_color="lime",
            end_color="blue",
        )

        output = buffer.getvalue()

        # Verify banners were rendered
        assert len(output) > 0

    def test_banners_with_borders(self):
        """Test rendering banners with frame borders."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.banner("TEST", font="slant", border="solid")
        console.newline()

        console.banner("DEMO", font="slant", border="double")

        output = buffer.getvalue()

        # Should have border characters
        assert "┌" in output or "+" in output
        assert len(output) > 0


class TestConsoleTextIntegration:
    """Test text rendering integration with various styles."""

    def test_text_with_multiple_styles(self):
        """Test rendering text with various style combinations."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Normal text")
        console.text("Bold text", bold=True)
        console.text("Italic text", italic=True)
        console.text("Underlined text", underline=True)
        console.text("Dim text", dim=True)
        console.text("Bold and italic", bold=True, italic=True)

        output = buffer.getvalue()

        assert "Normal text" in output
        assert "Bold text" in output
        assert "Italic text" in output
        assert "Underlined text" in output
        assert "Dim text" in output
        assert "Bold and italic" in output

    def test_text_with_colors(self):
        """Test rendering colored text."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        colors = ["red", "green", "blue", "yellow", "cyan", "magenta"]

        for color in colors:
            console.text(f"{color.capitalize()} text", color=color)

        output = buffer.getvalue()

        for color in colors:
            assert f"{color.capitalize()} text" in output

    def test_text_inline_output(self):
        """Test rendering text without newlines."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.text("Part 1", end=" ")
        console.text("Part 2", end=" ")
        console.text("Part 3")

        output = buffer.getvalue()

        assert "Part 1 Part 2 Part 3" in output


class TestConsoleLayoutIntegration:
    """Test Console with layout and spacing."""

    def test_structured_layout_with_rules(self):
        """Test creating structured layouts with rules and spacing."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.rule("Header", color="blue")
        console.newline()
        console.frame("Header content", align="center")
        console.newline(2)

        console.rule("Body", color="green")
        console.newline()
        console.text("Body text content")
        console.newline(2)

        console.rule("Footer", color="red")
        console.newline()
        console.frame("Footer content", align="center")

        output = buffer.getvalue()

        assert "Header" in output
        assert "Body" in output
        assert "Footer" in output
        assert "Header content" in output
        assert "Body text content" in output
        assert "Footer content" in output

    def test_dashboard_layout(self):
        """Test creating a simple dashboard layout."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        # Title
        console.banner("STATUS", font="slant")
        console.newline()

        # Metrics section
        console.rule("Metrics", color="cyan")
        console.frame("CPU: 45%", title="Performance", width=40)
        console.frame("Memory: 2.1GB", title="Resources", width=40)
        console.frame("Uptime: 3 days", title="System", width=40)
        console.newline()

        # Status section
        console.rule("Health", color="green")
        console.text("✓ All systems operational", color="green", bold=True)

        output = buffer.getvalue()

        assert "Metrics" in output
        assert "CPU" in output
        assert "Memory" in output
        assert "Uptime" in output
        assert "Health" in output
        assert "operational" in output


class TestConsoleTerminalDetection:
    """Test Console with terminal detection enabled."""

    def test_console_with_terminal_detection(self):
        """Test Console detects terminal capabilities."""
        console = Console(detect_terminal=True, record=True)

        # Terminal profile should be available
        assert console.terminal_profile is not None
        assert hasattr(console.terminal_profile, "ansi_support")
        assert hasattr(console.terminal_profile, "color_depth")
        assert hasattr(console.terminal_profile, "emoji_safe")

    def test_console_rendering_with_detection(self):
        """Test rendering works with terminal detection enabled."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=True)

        console.frame("Test content", title="Detection Test")
        console.text("Some text", color="blue")

        output = buffer.getvalue()

        assert "Test content" in output
        assert "Detection Test" in output
        assert "Some text" in output


class TestConsoleErrorHandling:
    """Test Console error handling and edge cases."""

    def test_export_without_recording_raises_error(self):
        """Test export methods raise error when recording not enabled."""
        console = Console(record=False, detect_terminal=False)

        console.text("Some content")

        # Should raise RuntimeError
        try:
            console.export_html()
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "Recording mode not enabled" in str(e)

        try:
            console.export_text()
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "Recording mode not enabled" in str(e)

    def test_newline_with_negative_count(self):
        """Test newline raises error with negative count."""
        console = Console(detect_terminal=False)

        try:
            console.newline(-1)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "count must be >= 0" in str(e)

    def test_empty_content_handling(self):
        """Test Console handles empty content gracefully."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        console.frame("")
        console.text("")
        console.banner("")

        output = buffer.getvalue()

        # Should not crash, produces some output
        assert isinstance(output, str)


class TestConsoleComplexWorkflows:
    """Test complex real-world console workflows."""

    def test_test_results_report(self):
        """Test creating a test results report."""
        console = Console(record=True, detect_terminal=False)

        # Header
        console.banner("TESTS", font="slant")
        console.newline()

        # Summary
        console.rule("Summary", color="blue")
        console.frame(
            ["Total: 150 tests", "Passed: 145 ✓", "Failed: 3 ✗", "Skipped: 2 ⊝"],
            title="Results",
            border="double",
        )
        console.newline()

        # Status
        console.text("Status: ", end="")
        console.text("PASSING", color="green", bold=True)
        console.newline()

        # Failed tests
        console.rule("Failed Tests", color="red")
        console.frame(
            ["test_database_connection", "test_api_timeout", "test_cache_invalidation"],
            title="3 Failures",
            border="heavy",
        )

        # Verify export works
        html = console.export_html()

        # Check HTML output contains all elements
        assert "Summary" in html
        assert "Results" in html
        assert "PASSING" in html or "Passing" in html
        assert "Total" in html
        assert "145" in html  # Passed count

    def test_deployment_log(self):
        """Test creating a deployment log output."""
        console = Console(record=True, detect_terminal=False)

        # Title
        console.banner("DEPLOY", font="slant")
        console.newline()

        # Stages
        stages = [
            ("Build", "✓", "green"),
            ("Test", "✓", "green"),
            ("Security Scan", "✓", "green"),
            ("Deploy", "→", "yellow"),
        ]

        for stage, icon, color in stages:
            console.text(f"{icon} {stage}", color=color, bold=True)

        console.newline()

        # Details frame
        console.frame(
            ["Environment: Production", "Version: 2.1.0", "Time: 00:03:45"],
            title="Deployment Info",
            border="solid",
        )

        # Export
        text = console.export_text()

        assert "Build" in text
        assert "Test" in text
        assert "Deploy" in text
        assert "Production" in text
        assert "2.1.0" in text

    def test_configuration_display(self):
        """Test displaying configuration information."""
        buffer = io.StringIO()
        console = Console(file=buffer, detect_terminal=False)

        # Title
        console.rule("Configuration", color="cyan")
        console.newline()

        # Multiple config sections
        sections = [
            ("Database", ["Host: localhost", "Port: 5432", "Name: app_db"]),
            ("API", ["URL: https://api.example.com", "Timeout: 30s"]),
            ("Cache", ["Type: Redis", "TTL: 3600s"]),
        ]

        for title, lines in sections:
            console.frame(lines, title=title, border="solid", width=50)
            console.newline()

        output = buffer.getvalue()

        assert "Configuration" in output
        assert "Database" in output
        assert "API" in output
        assert "Cache" in output
        assert "localhost" in output
        assert "Redis" in output
