#!/usr/bin/env python3
"""
Variable-Length Content Examples

Demonstrates how to handle frames with dynamic, variable-length content
such as error logs, user input, API responses, and other unpredictable text.
"""

from styledconsole import (
    Console,
    auto_size_content,
    prepare_frame_content,
    truncate_lines,
    wrap_text,
)

console = Console()

print("=" * 80)
print("VARIABLE-LENGTH CONTENT EXAMPLES")
print("=" * 80)
print()

# =============================================================================
# Example 1: Error Logs with Auto-Wrapping
# =============================================================================
print("Example 1: Error Logs with Auto-Wrapping")
print("-" * 80)

error_message = (
    "FileNotFoundError: [Errno 2] No such file or directory: "
    "'/var/log/application/very/deeply/nested/directory/structure/logfile.txt'"
)

# Prepare content with automatic wrapping
content = prepare_frame_content(error_message, max_width=60)

console.frame(content, title="❌ Error", border="heavy", content_color="red", width=70)
print()

# =============================================================================
# Example 2: Long Stack Trace with Line Truncation
# =============================================================================
print("Example 2: Long Stack Trace with Line Truncation")
print("-" * 80)

stack_trace = [
    "Traceback (most recent call last):",
    '  File "app.py", line 42, in main',
    "    result = process_data(input_file)",
    '  File "processor.py", line 123, in process_data',
    "    data = read_file(filename)",
    '  File "io_utils.py", line 89, in read_file',
    '    with open(filename, "r") as f:',
    "FileNotFoundError: No such file or directory",
    "",
    "Additional context:",
    "- Input file: /path/to/missing/file.txt",
    "- Working directory: /home/user/project",
    "- Python version: 3.13.3",
    "- OS: Linux 6.5.0",
    "- Memory usage: 245MB",
    "- CPU usage: 12%",
]

# Truncate to first 10 lines with indicator
truncated_trace = truncate_lines(stack_trace, max_lines=10)

console.frame(truncated_trace, title="🐛 Stack Trace (Truncated)", border="double", width=70)
print()

# =============================================================================
# Example 3: API Response with Auto-Sizing
# =============================================================================
print("Example 3: API Response with Auto-Sizing")
print("-" * 80)

api_response = """{
  "status": "error",
  "code": 404,
  "message": "Resource not found",
  "details": "The requested endpoint '/api/v2/users/12345/profile' does not exist",
  "timestamp": "2025-10-19T14:23:15Z",
  "request_id": "req_abc123def456"
}"""

# Auto-size determines optimal width based on content
lines, width = auto_size_content(api_response, max_width=80, min_width=40)

console.frame(lines, title="📡 API Response", border="rounded", width=width + 4)
print()

# =============================================================================
# Example 4: User Input with Unknown Length
# =============================================================================
print("Example 4: User Input with Unknown Length")
print("-" * 80)


def display_user_comment(comment: str):
    """Display a user comment in a frame, handling any length."""
    # Prepare content with wrapping and reasonable limits
    content = prepare_frame_content(comment, max_width=50, max_lines=8, wrap=True)

    console.frame(content, title="💬 User Comment", border="solid", width=60)


# Short comment
display_user_comment("Great product!")
print()

# Long comment
long_comment = (
    "This is an absolutely fantastic product that has completely transformed "
    "how I work. The attention to detail is incredible, and the customer support "
    "team is always responsive and helpful. I would highly recommend this to "
    "anyone looking for a reliable solution. Five stars!"
)
display_user_comment(long_comment)
print()

# =============================================================================
# Example 5: Configuration Display with Variable Fields
# =============================================================================
print("Example 5: Configuration Display with Variable Fields")
print("-" * 80)

config_data = {
    "database": "postgresql://localhost:5432/myapp_production_db",
    "cache_url": "redis://localhost:6379/0",
    "secret_key": "********************************",
    "api_endpoint": "https://api.example.com/v2/production/",
    "max_connections": 100,
    "timeout": "30s",
}

# Build content dynamically
config_lines = []
for key, value in config_data.items():
    line = f"{key}: {value}"
    # Wrap individual lines if needed
    wrapped = wrap_text(line, width=50)
    config_lines.extend(wrapped)

console.frame(config_lines, title="⚙️  Configuration", border="rounded", width=60)
print()

# =============================================================================
# Example 6: Real-Time Log Monitor (Simulated)
# =============================================================================
print("Example 6: Real-Time Log Monitor with Overflow Handling")
print("-" * 80)

log_entries = [
    "[2025-10-19 14:20:01] INFO: Application started",
    "[2025-10-19 14:20:02] INFO: Connected to database",
    "[2025-10-19 14:20:03] DEBUG: Loading configuration from /etc/app/config.yml",
    "[2025-10-19 14:20:04] INFO: Starting HTTP server on port 8080",
    "[2025-10-19 14:20:05] INFO: Server ready to accept connections",
    "[2025-10-19 14:20:10] INFO: Received request GET /api/users",
    "[2025-10-19 14:20:11] DEBUG: Query executed in 12ms",
    "[2025-10-19 14:20:12] INFO: Response sent: 200 OK",
    "[2025-10-19 14:20:15] WARNING: High memory usage detected: 85%",
    "[2025-10-19 14:20:20] INFO: Received request POST /api/data",
    "[2025-10-19 14:20:21] ERROR: Database connection timeout",
    "[2025-10-19 14:20:22] ERROR: Failed to process request",
]


def display_recent_logs(logs: list[str], max_display: int = 6):
    """Display recent log entries with overflow indicator."""
    # Show only the most recent entries
    if len(logs) > max_display:
        recent = logs[-max_display:]
        omitted = len(logs) - max_display
        content = [f"... ({omitted} earlier entries)"] + recent
    else:
        content = logs

    console.frame(content, title="📋 Recent Logs", border="heavy", width=80)


display_recent_logs(log_entries, max_display=6)
print()

# =============================================================================
# Example 7: Exception Message with Context
# =============================================================================
print("Example 7: Exception Message with Full Context")
print("-" * 80)


def display_exception(exc_type: str, message: str, context: dict):
    """Display exception with context in a properly formatted frame."""
    # Build content
    lines = [f"{exc_type}: {message}", ""]

    if context:
        lines.append("Context:")
        for key, value in context.items():
            # Wrap key-value pairs
            kv_line = f"  • {key}: {value}"
            wrapped = wrap_text(kv_line, width=60, break_long_words=True)
            lines.extend(wrapped)

    # Auto-size the frame
    prepared, width = auto_size_content(lines, max_width=70)

    console.frame(
        prepared,
        title="⚠️  Exception Details",
        border="heavy",
        content_color="yellow",
        width=width + 4,
    )


display_exception(
    exc_type="DatabaseConnectionError",
    message="Unable to establish connection to database server",
    context={
        "host": "db.production.example.com",
        "port": 5432,
        "database": "myapp_prod",
        "timeout": "30s",
        "retry_attempts": 3,
        "last_error": "Connection refused",
    },
)
print()

# =============================================================================
# Example 8: Dynamic Content Length Comparison
# =============================================================================
print("Example 8: Handling Different Content Lengths Consistently")
print("-" * 80)

test_messages = [
    "OK",
    "Connection established successfully",
    "The operation completed successfully after retrying 3 times due to network issues",
]

for msg in test_messages:
    # Use auto_size_content for consistent handling
    content, width = auto_size_content(msg, max_width=60, min_width=30)
    console.frame(content, title="✅ Status", border="solid", width=width + 4)
    print()

# =============================================================================
# Summary
# =============================================================================
print("=" * 80)
print("KEY TAKEAWAYS:")
print("=" * 80)
print()
print("✅ Use prepare_frame_content() for automatic wrapping and truncation")
print("✅ Use auto_size_content() to find optimal width for variable content")
print("✅ Use truncate_lines() to limit output with indicators")
print("✅ Use wrap_text() for manual control over text wrapping")
print("✅ Combine these utilities for robust dynamic content handling")
print()
print("=" * 80)
