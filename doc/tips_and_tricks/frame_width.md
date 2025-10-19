# Frame Width Best Practices

## The Truncation Issue

When using `Console.frame()` with multi-line content, you may see truncation like:

```
┌─────────────────────────────────────────┐
│ This is a very long line that gets t... │
└─────────────────────────────────────────┘
```

## Why It Happens

1. **Default max_width constraint** - Frames limit width to prevent overflow
2. **Multi-line string parsing** - Using `'''` makes width calculation harder
3. **Auto-sizing behavior** - Without explicit width, frames may be too narrow

## Solutions

### ✅ Solution 1: Use List of Strings (Recommended)

```python
# BAD: Multi-line string may truncate
console.frame('''
Line 1 content
Line 2 with longer content
''', title="Example")

# GOOD: List of strings with explicit width
console.frame([
    "Line 1 content",
    "Line 2 with longer content",
], title="Example", width=50)
```

### ✅ Solution 2: Specify Explicit Width

```python
# Specify width to accommodate your content
console.frame(
    "Your content here",
    title="Title",
    width=60,  # Adjust based on content length
)
```

### ✅ Solution 3: Keep Lines Short

```python
# Break long lines into shorter ones
console.frame([
    "Performance:     ⚡ Fast",
    "Quality:         ⭐⭐⭐⭐⭐",
    "Status:          ✅ Working",
], width=40)
```

## Width Calculation Tips

**Good widths for common content:**

- Short messages: `width=40`
- Medium content: `width=60`
- Wide dashboards: `width=80`
- Full terminal: `width=120` (or omit for auto)

**Calculate needed width:**

```python
# For known content
max_line_length = max(len(line) for line in content_lines)
width = max_line_length + 4  # +4 for padding and borders
```

## Example: UX Validation Display

**Before (truncated):**

```python
console.frame('''✅ ALL 12 EXAMPLES PASSED

Basic Examples:      8/8 ✓
Showcase Examples:   3/3 ✓
Gallery Examples:    1/1 ✓''', title='📊 Test Results')
# Output: "Gallery Exam..."  ❌ TRUNCATED
```

**After (complete):**

```python
console.frame([
    "✅ ALL 12 EXAMPLES PASSED",
    "",
    "Basic Examples:      8/8 ✓",
    "Showcase Examples:   3/3 ✓",
    "Gallery Examples:    1/1 ✓",
], title="📊 Test Results", width=60)
# Output: Full content visible ✅
```

## When to Omit Width

Omit `width` parameter when:
- ✅ Content is short (< 30 chars)
- ✅ You want auto-sizing based on content
- ✅ Using with `max_width` to prevent overflow

## Terminal Width Considerations

```python
from styledconsole import Console

# Get terminal width
console = Console(detect_terminal=True)
term_width = console.terminal_profile.width if console.terminal_profile else 80

# Use 90% of terminal width for frames
frame_width = int(term_width * 0.9)
console.frame(content, width=frame_width)
```

## Summary

**Quick Fix Checklist:**
- [ ] Use list of strings instead of multi-line `'''` strings
- [ ] Add explicit `width` parameter if content is wide
- [ ] Keep individual lines under ~70 characters
- [ ] Test output to verify no truncation (look for `...`)

**See Also:**
- `examples/testing/ux_validation_summary.py` - Working example
- `examples/basic/01_simple_frame.py` - Basic frame usage
- `examples/basic/08_console_api.py` - Various frame examples
