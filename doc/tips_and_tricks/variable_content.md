# Variable-Length Content Guide

## Overview

The StyledConsole library now provides powerful utilities for handling frames with **variable-length content** such as error logs, API responses, user input, and other dynamic text that you can't predict in advance.

## The Problem

When working with frames, you often encounter content whose length you cannot know in advance:

```python
# ❌ PROBLEM: Content length unknown
error_log = get_error_from_system()  # Could be 10 chars or 10,000 chars!
console.frame(error_log, title="Error")  # Might truncate or overflow
```

## The Solution

Use the new wrapping utilities:

```python
from styledconsole import Console, prepare_frame_content, auto_size_content

# ✅ SOLUTION 1: Automatic wrapping
content = prepare_frame_content(error_log, max_width=60)
console.frame(content, title="Error", width=70)

# ✅ SOLUTION 2: Auto-sizing
content, width = auto_size_content(error_log, max_width=80)
console.frame(content, title="Error", width=width + 4)
```

______________________________________________________________________

## Core Functions

### 1. `prepare_frame_content()` - Main Helper

**Purpose:** Prepare any content for framing with intelligent wrapping and truncation.

**Signature:**

```python
prepare_frame_content(
    text: str | list[str],
    *,
    max_width: int = 80,
    max_lines: int | None = None,
    wrap: bool = True,
    break_long_words: bool = True,
    preserve_paragraphs: bool = False,
) -> list[str]
```

**Example:**

```python
from styledconsole import Console, prepare_frame_content

console = Console()

# Long error message
error = (
    "DatabaseConnectionError: Unable to connect to postgresql://prod.example.com:5432/myapp "
    "after 3 retry attempts. Connection timeout exceeded (30s). "
    "Check network connectivity and firewall rules."
)

# Prepare content with wrapping
content = prepare_frame_content(error, max_width=50, max_lines=5)

console.frame(content, title="❌ Error", border="heavy", width=60)
```

**Output:**

```
┏━━━━━━━━━━━━━━━━━━━━ ❌ Error ━━━━━━━━━━━━━━━━━━━━┓
┃ DatabaseConnectionError: Unable to connect to  ┃
┃ postgresql://prod.example.com:5432/myapp       ┃
┃ after 3 retry attempts. Connection timeout     ┃
┃ exceeded (30s). Check network connectivity     ┃
┃ and firewall rules.                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### 2. `auto_size_content()` - Smart Width Detection

**Purpose:** Automatically determine optimal width for content, then wrap if needed.

**Signature:**

```python
auto_size_content(
    text: str | list[str],
    *,
    max_width: int = 100,
    min_width: int = 20,
    max_lines: int | None = None,
) -> tuple[list[str], int]
```

**Example:**

```python
from styledconsole import Console, auto_size_content

console = Console()

# API response (length unknown)
api_response = get_api_response()  # Could be short or long

# Auto-size based on content
content, width = auto_size_content(api_response, max_width=80)

# Use calculated width
console.frame(content, title="📡 Response", width=width + 4)
```

### 3. `wrap_text()` - Basic Text Wrapping

**Purpose:** Wrap a single string to fit within a specific width.

**Signature:**

```python
wrap_text(
    text: str,
    width: int,
    *,
    break_long_words: bool = True,
    break_on_hyphens: bool = True,
    preserve_paragraphs: bool = False,
) -> list[str]
```

**Example:**

```python
from styledconsole import wrap_text

text = "This is a very long line that needs to be wrapped to fit within a frame"
lines = wrap_text(text, width=30)

# Result:
# ['This is a very long line',
#  'that needs to be wrapped to',
#  'fit within a frame']
```

### 4. `truncate_lines()` - Line Count Limiting

**Purpose:** Limit the number of lines with an overflow indicator.

**Signature:**

```python
truncate_lines(
    lines: list[str],
    max_lines: int,
    *,
    truncation_indicator: str = "... ({count} more lines)",
) -> list[str]
```

**Example:**

```python
from styledconsole import Console, truncate_lines

console = Console()

# Long log file (100+ lines)
log_lines = read_log_file()  # Returns many lines

# Show only recent entries
recent = truncate_lines(log_lines, max_lines=10)

console.frame(recent, title="📋 Recent Logs", width=80)
```

**Output:**

```
┌──────────────── 📋 Recent Logs ─────────────────┐
│ [2025-10-19 14:20:01] INFO: App started         │
│ [2025-10-19 14:20:02] INFO: Connected to DB     │
│ ...                                             │
│ [2025-10-19 14:20:10] ERROR: Timeout            │
│ ... (90 more lines)                             │
└─────────────────────────────────────────────────┘
```

### 5. `wrap_multiline()` - Multi-line Wrapping

**Purpose:** Wrap multiple lines while preserving line breaks and indentation.

**Signature:**

```python
wrap_multiline(
    lines: list[str],
    width: int,
    *,
    break_long_words: bool = True,
    preserve_indentation: bool = True,
) -> list[str]
```

**Example:**

```python
from styledconsole import wrap_multiline

code_lines = [
    "def process_data(input_file, output_file, max_retries=3):",
    "    # This is a very long comment that explains what this function does",
    "    with open(input_file) as f:",
]

wrapped = wrap_multiline(code_lines, width=50, preserve_indentation=True)
```

______________________________________________________________________

## Real-World Use Cases

### Use Case 1: Error Logs

```python
from styledconsole import Console, prepare_frame_content

console = Console()

def display_error(exception: Exception):
    """Display any exception in a formatted frame."""
    error_msg = f"{type(exception).__name__}: {str(exception)}"

    # Prepare with wrapping and line limit
    content = prepare_frame_content(
        error_msg,
        max_width=60,
        max_lines=10,
        wrap=True
    )

    console.frame(
        content,
        title="❌ Error",
        border="heavy",
        content_color="red",
        width=70
    )

try:
    open("/path/to/missing/file.txt")
except Exception as e:
    display_error(e)
```

### Use Case 2: Stack Traces

```python
import traceback
from styledconsole import Console, truncate_lines

console = Console()

def display_traceback():
    """Display stack trace with truncation."""
    # Get full traceback
    tb_lines = traceback.format_exc().splitlines()

    # Truncate to reasonable size
    content = truncate_lines(tb_lines, max_lines=15)

    console.frame(
        content,
        title="🐛 Stack Trace",
        border="double",
        width=80
    )
```

### Use Case 3: API Responses

```python
import json
from styledconsole import Console, auto_size_content

console = Console()

def display_api_response(response_data: dict):
    """Display API response with auto-sizing."""
    # Pretty-print JSON
    json_str = json.dumps(response_data, indent=2)

    # Auto-size to content
    content, width = auto_size_content(json_str, max_width=100)

    console.frame(
        content,
        title="📡 API Response",
        border="rounded",
        width=width + 4
    )

response = {"status": "ok", "data": {"items": [1, 2, 3]}}
display_api_response(response)
```

### Use Case 4: User Input

```python
from styledconsole import Console, prepare_frame_content

console = Console()

def display_comment(user: str, text: str):
    """Display user comment with wrapping."""
    # Prepare comment with reasonable limits
    content = prepare_frame_content(
        text,
        max_width=60,
        max_lines=8,
        wrap=True
    )

    console.frame(
        [f"From: {user}", ""] + content,
        title="💬 Comment",
        border="solid",
        width=70
    )

display_comment(
    user="Alice",
    text="This is a very long comment that goes on and on about how great this product is..."
)
```

### Use Case 5: Configuration Display

```python
from styledconsole import Console, wrap_text

console = Console()

def display_config(config: dict):
    """Display configuration with wrapped values."""
    lines = []

    for key, value in config.items():
        # Wrap key-value pairs if needed
        kv = f"{key}: {value}"
        wrapped = wrap_text(kv, width=60)
        lines.extend(wrapped)

    console.frame(
        lines,
        title="⚙️  Configuration",
        border="rounded",
        width=70
    )

config = {
    "database_url": "postgresql://localhost:5432/very_long_database_name_prod",
    "api_key": "sk_live_" + "x" * 50,
    "timeout": "30s",
}

display_config(config)
```

______________________________________________________________________

## Best Practices

### ✅ DO: Use `prepare_frame_content()` for Most Cases

```python
# This handles 90% of use cases
content = prepare_frame_content(text, max_width=60, max_lines=10)
console.frame(content, width=70)
```

### ✅ DO: Use `auto_size_content()` for Adaptive Layouts

```python
# Great for content that varies significantly
content, width = auto_size_content(text, max_width=80)
console.frame(content, width=width + 4)
```

### ✅ DO: Set Reasonable Limits

```python
# Prevent excessive output
content = prepare_frame_content(
    log_data,
    max_width=80,   # Readable width
    max_lines=20,   # Prevent scroll overflow
)
```

### ❌ DON'T: Skip Wrapping for Unknown Content

```python
# BAD: Could overflow or truncate
console.frame(unknown_text, width=50)

# GOOD: Prepare first
content = prepare_frame_content(unknown_text, max_width=40)
console.frame(content, width=50)
```

### ❌ DON'T: Use Excessive Width

```python
# BAD: Too wide for most terminals
content = prepare_frame_content(text, max_width=200)

# GOOD: Stay within reasonable bounds
content = prepare_frame_content(text, max_width=80)
```

______________________________________________________________________

## Parameter Guide

### `max_width`

- **Purpose:** Maximum line width (excluding frame borders/padding)
- **Default:** 80
- **Recommended:** 40-80 for readability
- **Example:**

```python
prepare_frame_content(text, max_width=60)  # 60 chars per line
```

### `max_lines`

- **Purpose:** Maximum number of lines (adds truncation indicator if exceeded)
- **Default:** `None` (no limit)
- **Recommended:** 10-20 for logs, 5-8 for user messages
- **Example:**

```python
prepare_frame_content(log, max_lines=15)  # Show first 15 lines
```

### `wrap`

- **Purpose:** Enable/disable text wrapping
- **Default:** `True`
- **Use `False`:** When content is pre-formatted
- **Example:**

```python
prepare_frame_content(code, wrap=False)  # Don't wrap code
```

### `break_long_words`

- **Purpose:** Break words longer than `max_width`
- **Default:** `True`
- **Use `False`:** To keep words intact (may overflow)
- **Example:**

```python
prepare_frame_content(url, break_long_words=True)  # Break long URLs
```

### `preserve_paragraphs`

- **Purpose:** Keep double newlines as paragraph breaks
- **Default:** `False`
- **Use `True`:** For formatted text with paragraphs
- **Example:**

```python
text = "Paragraph 1.\n\nParagraph 2."
prepare_frame_content(text, preserve_paragraphs=True)
```

______________________________________________________________________

## Advanced Patterns

### Pattern 1: Conditional Truncation

```python
def display_logs(logs: list[str], max_display: int = 10):
    """Show recent logs with conditional truncation."""
    if len(logs) > max_display:
        content = truncate_lines(logs, max_display)
        title = f"📋 Recent Logs ({len(logs)} total)"
    else:
        content = logs
        title = "📋 All Logs"

    console.frame(content, title=title, width=80)
```

### Pattern 2: Smart Width Calculation

```python
from styledconsole.utils.text import visual_width

def smart_frame(text: str):
    """Frame with smart width based on content."""
    lines = text.splitlines()
    max_line = max(visual_width(line) for line in lines)

    if max_line <= 60:
        # Content fits naturally
        content = lines
        width = max_line + 4
    else:
        # Wrap to 60 chars
        content = prepare_frame_content(text, max_width=60)
        width = 70

    console.frame(content, width=width)
```

### Pattern 3: Progressive Truncation

```python
def show_with_fallback(data: list[str]):
    """Show data with progressive truncation."""
    for limit in [50, 20, 10, 5]:
        content = truncate_lines(data, max_lines=limit)
        if len(content) <= limit + 1:  # Fits with indicator
            console.frame(content, title=f"Showing {limit} of {len(data)}")
            break
```

______________________________________________________________________

## Performance Tips

### ✅ Cache Wrapped Content

```python
# If displaying same content multiple times
cached_content = prepare_frame_content(large_text, max_width=60)

for i in range(5):
    console.frame(cached_content, title=f"Display {i}")
```

### ✅ Use Appropriate Limits

```python
# Don't process more than needed
content = prepare_frame_content(
    huge_log,
    max_lines=20,  # Only wrap/process 20 lines
)
```

### ✅ Avoid Redundant Wrapping

```python
# BAD: Double wrapping
wrapped = wrap_text(text, width=60)
content = prepare_frame_content(wrapped, max_width=60)  # Redundant!

# GOOD: Wrap once
content = prepare_frame_content(text, max_width=60)
```

______________________________________________________________________

## Troubleshooting

### Content Still Truncating

**Problem:** Content shows "..." even after using `prepare_frame_content()`

**Solution:** Increase `max_width` or `max_lines`:

```python
# Before
content = prepare_frame_content(text, max_width=40, max_lines=5)

# After
content = prepare_frame_content(text, max_width=60, max_lines=10)
```

### Words Breaking Awkwardly

**Problem:** Words break in the middle

**Solution:** Disable `break_long_words`:

```python
content = prepare_frame_content(text, break_long_words=False)
```

### Indentation Lost

**Problem:** Code or formatted text loses indentation

**Solution:** Use `wrap_multiline()` with `preserve_indentation=True`:

```python
wrapped = wrap_multiline(code_lines, width=60, preserve_indentation=True)
```

### Frame Too Wide/Narrow

**Problem:** Auto-sized frame doesn't fit well

**Solution:** Set explicit bounds with `min_width` and `max_width`:

```python
content, width = auto_size_content(
    text,
    min_width=40,   # Don't go narrower
    max_width=80,   # Don't go wider
)
```

______________________________________________________________________

## Summary

The text wrapping utilities solve the challenge of displaying variable-length content in frames:

**Key Functions:**

- `prepare_frame_content()` - Main helper for most use cases
- `auto_size_content()` - Smart width calculation
- `wrap_text()` - Basic wrapping
- `truncate_lines()` - Line limiting
- `wrap_multiline()` - Multi-line with indentation

**Benefits:**

✅ Handle error logs of any length
✅ Display API responses without manual formatting
✅ Wrap user input dynamically
✅ Truncate long output with indicators
✅ Auto-size frames to content

**See Also:**

- `examples/basic/09_variable_content.py` - 8 real-world examples
- `doc/FRAME_WIDTH_TIPS.md` - Frame width best practices
- API documentation for detailed function references
