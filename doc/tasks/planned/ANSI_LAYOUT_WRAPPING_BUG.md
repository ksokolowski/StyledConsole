# ANSI Layout Wrapping Bug

**Priority:** HIGH
**Status:** Discovered
**Date:** 2025-10-20
**Discovered in:** Rainbow Fat Alignment Showcase Example

## Problem Description

When using `LayoutComposer` with `align="right"` or `align="center"`, frames containing ANSI color codes wrap to the next line even though their **visual width** fits within the terminal width.

### Root Cause

The issue occurs because:

1. `LayoutComposer._align_line()` correctly calculates **visual width** using `visual_width()` which strips ANSI codes
2. Padding is added as spaces to reach `target_width` (e.g., 277 characters)
3. The resulting string has:
   - **Visual width:** 277 (correct)
   - **String length:** 296+ (visual width + ANSI escape codes ~20 chars)
4. When Rich's `console.print()` or the terminal receives a 296-character string, it wraps at the terminal width boundary (277), breaking the frame borders

### Reproduction

```python
from styledconsole import Console
from styledconsole.core.frame import FrameRenderer
from styledconsole.core.layout import LayoutComposer

console = Console()
renderer = FrameRenderer()
composer = LayoutComposer()

# Create a colored frame
frame = renderer.render(
    "Test content",
    border="double",
    border_color="cyan",  # Adds ANSI codes
    width=60
)

# Align right to terminal width (e.g., 277)
terminal_width = console._rich_console.width
layout = composer.stack([frame], align="right", width=terminal_width)

# Print - this wraps!
for line in layout:
    console.print(line, highlight=False, soft_wrap=False)
```

### Expected Behavior

Frames should be aligned without wrapping, with ANSI codes transparent to alignment calculations.

### Actual Behavior

- **Left alignment:** Works correctly (ANSI codes at start don't cause issues)
- **Center alignment:** Wraps due to padding on both sides pushing total length over terminal width
- **Right alignment:** Wraps significantly due to large left padding before ANSI-colored content

## Impact

- **Severity:** HIGH - Breaks visual alignment, a core feature
- **Affected Components:**
  - `LayoutComposer.stack()` with `align="center"` or `align="right"`
  - Any colored frames in centered/right-aligned layouts
  - Examples: `rainbow_fat_alignment.py`, potentially others
- **Workaround:** Use narrow frames (≤60 chars) or left-align only

## Technical Analysis

### Current Flow

```
FrameRenderer.render()
  → Returns lines with embedded ANSI codes like:
    "\033[38;2;0;255;255m╔══════╗\033[0m"
    (Length: ~30, Visual: 10)

LayoutComposer._align_line(line, target_width=277, align="right")
  → visual_width(line) = 10
  → padding_needed = 277 - 10 = 267
  → Returns: " " * 267 + line
  → Total length: 267 + 30 = 297 characters

console.print(line, soft_wrap=False)
  → Terminal sees 297-char string
  → Wraps at position 277
  → Frame breaks across lines
```

### Why It Happens

The padding calculation is **visually correct** but doesn't account for ANSI codes making the **string length** exceed terminal width. Terminals and Rich's output handling work with byte/character positions, not visual width.

## Proposed Solutions

### Option 1: Strip ANSI Before Padding (Recommended)

Modify `LayoutComposer._align_line()`:

```python
def _align_line(self, line: str, target_width: int, align: AlignType) -> str:
    """Align a line to target width with specified alignment."""
    from styledconsole.utils.text import strip_ansi

    # Get visual width
    current_width = visual_width(line)

    if current_width >= target_width:
        return line

    padding_needed = target_width - current_width

    if align == "left":
        return line + (" " * padding_needed)
    elif align == "right":
        # Extract ANSI codes to preserve them
        clean_line = strip_ansi(line)
        ansi_codes = self._extract_ansi_codes(line)
        # Pad the clean line, then re-apply ANSI
        return (" " * padding_needed) + self._reapply_ansi(clean_line, ansi_codes)
    else:  # center
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        clean_line = strip_ansi(line)
        ansi_codes = self._extract_ansi_codes(line)
        return (" " * left_pad) + self._reapply_ansi(clean_line, ansi_codes) + (" " * right_pad)
```

**Pros:**
- Fixes the root cause
- Works for all alignment types
- No changes to frame rendering

**Cons:**
- Requires ANSI code extraction/reapplication logic
- More complex implementation

### Option 2: Use Rich's Padding API

Leverage Rich's built-in padding that understands ANSI:

```python
from rich.padding import Padding
from rich.text import Text

def _align_line(self, line: str, target_width: int, align: AlignType) -> str:
    # Convert to Rich Text object
    text = Text.from_ansi(line)

    # Use Rich's padding
    if align == "left":
        padded = Padding(text, (0, target_width - visual_width(line), 0, 0))
    elif align == "right":
        padded = Padding(text, (0, 0, 0, target_width - visual_width(line)))
    else:  # center
        left = (target_width - visual_width(line)) // 2
        right = target_width - visual_width(line) - left
        padded = Padding(text, (0, right, 0, left))

    # Render back to ANSI string
    return padded.render()
```

**Pros:**
- Uses Rich's battle-tested ANSI handling
- Cleaner code

**Cons:**
- Adds dependency on Rich's Padding API
- May have performance implications

### Option 3: Console-Level Fix

Make `console.print()` ANSI-aware for width calculations:

```python
def print(self, *args: Any, **kwargs: Any) -> None:
    # If content has ANSI and would exceed width, strip and re-apply
    for arg in args:
        if isinstance(arg, str) and len(arg) > self._rich_console.width:
            visual = visual_width(arg)
            if visual <= self._rich_console.width:
                # String length exceeds but visual fits - handle specially
                self._print_ansi_safe(arg, **kwargs)
                return
    self._rich_console.print(*args, **kwargs)
```

**Pros:**
- Fixes at output layer
- No changes to layout code

**Cons:**
- Patches symptom, not cause
- May affect other use cases

## Recommendation

**Implement Option 1** (Strip ANSI Before Padding) as it:
- Fixes the root cause in `LayoutComposer`
- Maintains separation of concerns
- Doesn't rely on Rich's internal APIs
- Provides precise control over alignment

## Implementation Plan

1. **Phase 1:** Add ANSI extraction/reapplication utilities to `utils/text.py`
   - `extract_ansi_sequences(text: str) -> list[tuple[int, str]]`
   - `reapply_ansi_sequences(text: str, sequences: list) -> str`

2. **Phase 2:** Update `LayoutComposer._align_line()` to use new utilities

3. **Phase 3:** Add comprehensive tests:
   - Test colored frames with all alignment types
   - Test various terminal widths
   - Test edge cases (very narrow terminals, very wide frames)

4. **Phase 4:** Update examples:
   - Fix `rainbow_fat_alignment.py` to remove workarounds
   - Verify all showcase examples work correctly

5. **Phase 5:** Documentation:
   - Update `LayoutComposer` docstrings
   - Add note about ANSI-safe alignment
   - Update examples README

## Testing Checklist

- [ ] Colored frame, left-aligned, terminal width 80
- [ ] Colored frame, center-aligned, terminal width 80
- [ ] Colored frame, right-aligned, terminal width 80
- [ ] Colored frame, center-aligned, terminal width 277
- [ ] Colored frame, right-aligned, terminal width 277
- [ ] Multiple colored frames stacked, all alignments
- [ ] Gradient frames (complex ANSI) with all alignments
- [ ] Very narrow terminal (40 chars)
- [ ] Very wide terminal (300+ chars)
- [ ] Mixed colored and non-colored frames
- [ ] Banner + frame stacking with alignment

## Related Issues

- Examples affected: `rainbow_fat_alignment.py`, potentially `cicd_dashboard.py`
- May affect any user code using colored frames with center/right alignment

## Timeline

- **Priority:** HIGH
- **Estimated effort:** 2-3 days
- **Target:** M4 (Current sprint)

## Notes

This bug was discovered during the creation of the rainbow fat alignment showcase. Current workarounds (narrow frames, left-align only) are insufficient for production use. This is a foundational issue that affects the core value proposition of the library (beautiful aligned terminal UIs).
