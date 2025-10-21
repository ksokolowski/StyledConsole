# ANSI Layout Wrapping Bug

**Priority:** HIGH
**Status:** ✅ **SOLUTION FOUND** - Use Rich's `justify` parameter
**Date Discovered:** 2025-10-20
**Date Analyzed:** 2025-10-21
**Date Solved:** 2025-10-21
**Discovered in:** Rainbow Fat Alignment Showcase Example

---

## ✅ SOLUTION FOUND (2025-10-21)

**Rich's `justify` parameter handles ANSI codes correctly!**

Instead of padding strings in `LayoutComposer`, use Rich's built-in ANSI-aware justification:

```python
# ❌ OLD (Broken with colored frames):
layout = composer.stack([frame], align="right", width=terminal_width)
for line in layout:
    console.print(line)

# ✅ NEW (Works perfectly):
layout = composer.stack([frame], align="left")  # Don't add padding
for line in layout:
    console.print(line, justify="right")  # Let Rich handle alignment
```

**Why this works:**
- Rich's `console.print(text, justify="right")` uses ANSI-aware width calculation
- It outputs positioning codes instead of padding strings with spaces
- Terminal counts positioning codes differently than character padding
- Result: Perfect alignment with no wrapping!

**Implementation options:**
1. **Quick fix:** Document workaround, update examples
2. **Clean solution:** Add `justify_output` parameter to Console methods
3. **Comprehensive:** Refactor `LayoutComposer` to delegate alignment to Rich

**Recommended:** Option 2 - add `justify` parameter to layout-printing methods.

---

## Problem Description

When using `LayoutComposer` with `align="right"` or `align="center"`, frames containing ANSI color codes wrap to the next line even though their **visual width** fits within the terminal width.

### Fundamental Constraint

This is a **mathematical impossibility** with the current string-based architecture:

**Three conflicting requirements:**
1. ✅ **Colored borders** (adds ~20 bytes ANSI codes per line)
2. ✅ **Perfect right-edge alignment** (requires padding to terminal width)
3. ✅ **No wrapping** (requires total string length ≤ terminal width)

**Why they conflict:**
- Frame visual width: 60 chars (what you see)
- ANSI codes overhead: ~20 bytes (invisible)
- Terminal width: 277 chars
- For right-align: padding = 277 - 60 = 217 spaces
- Total string: 217 + 60 + 20 = **297 bytes**
- Terminal wraps at: 277 chars
- **Result: 20 bytes overflow → frame breaks**

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

## Current Workaround (v0.1.0)

**In rainbow_fat_alignment.py:**
```python
max_frame_width = min(60, terminal_width // 2)  # Keep frames narrow
```

This works because:
- Frame width: 60 chars
- ANSI overhead: ~20 bytes
- Total string: 60 + 20 = 80 bytes
- Padding for right-align: 277 - 60 = 217 spaces
- Total output: 217 + 80 = 297 bytes (still wraps!)

**Current workaround still has issues.** Left and center alignment work, but right alignment still wraps.

## Why All Attempted Fixes Failed

### ❌ Attempted Fix #1: Reduce Padding by ANSI Overhead
```python
max_padding = target_width - visual_width - ansi_overhead
```
**Result:** No wrapping ✅, but frames don't align to terminal edge ❌
**Problem:** Frames appear ~20 chars left of where they should be

### ❌ Attempted Fix #2: ANSI Cursor Positioning
```python
cursor_forward = f"\x1b[{padding}C"  # Move cursor without spaces
return cursor_forward + line
```
**Result:** Still wraps ❌
**Problem:** Terminal counts the frame string bytes after cursor position

### ❌ Attempted Fix #3: Rich Text API with Padding
```python
text = Text.from_ansi(line)
text.pad_left(target_width)
```
**Result:** Still wraps ❌
**Problem:** Rich outputs ANSI string + spaces, same total length

## The Real Solution: Architectural Change

### Current Architecture (v0.1.0)
```
LayoutComposer.stack() → list[str]  # Pre-formatted with padding
  ↓
Console.print(str)  # Just outputs the string
```

**Problem:** Once we add padding to create the string, it's too late - the string length already exceeds terminal width.

### Proposed Architecture (M4)

**Option A: Return Structured Data**
```python
@dataclass
class LayoutLine:
    content: str          # The frame line with ANSI
    visual_width: int     # Visual width
    alignment: AlignType  # How to align

LayoutComposer.stack() → list[LayoutLine]
  ↓
Console.print(LayoutLine)  # Uses Rich's justify parameter
```

**Option B: Use Rich Renderables**
```python
LayoutComposer.stack() → Renderables
  ↓
Console.print(Renderable)  # Rich handles alignment internally
```

**Option C: Strip Colors, Let Console Re-apply**
```python
LayoutComposer.stack() → list[tuple[str, style_info]]
  ↓
Console.print()  # Applies colors while printing with Rich
```

## Recommendation

**Implement Option A** (Structured Data) in M4 because:

1. **Separation of Concerns:** Layout calculates positions, Console handles rendering
2. **No Data Loss:** Preserves all information (content, width, alignment, colors)
3. **Rich Integration:** Can use `Text()` objects with `justify` parameter
4. **Backward Compatible:** Can add `stack_legacy()` that returns strings
5. **Future-Proof:** Enables more features (vertical alignment, padding control, etc.)

## Implementation Plan (M4 Milestone)

### Phase 1: Define New Types (0.5 days)
```python
# In types.py
@dataclass
class LayoutLine:
    """A line in a layout with metadata for proper rendering."""
    content: str  # May contain ANSI codes
    visual_width: int
    alignment: AlignType = "left"
```

### Phase 2: Update LayoutComposer (1 day)
- Add `stack_structured()` method that returns `list[LayoutLine]`
- Keep `stack()` for backward compatibility (returns `list[str]`)
- Mark `stack()` as deprecated with migration guide

### Phase 3: Update Console.print() (1 day)
- Add overload for `print(LayoutLine)`
- Use Rich's `Text()` with `justify` parameter for alignment
- Handle ANSI codes transparently

### Phase 4: Testing (0.5 days)
- Test all frame types with all alignments
- Test at various terminal widths (40, 80, 120, 277)
- Test edge cases (frame wider than terminal, etc.)
- Update all 655 existing tests

### Phase 5: Update Examples & Docs (0.5 days)
- Update `rainbow_fat_alignment.py` to remove workarounds
- Update all other examples to use new API
- Document migration path in CHANGELOG
- Update API documentation

**Total Effort:** 3.5 days
**Target:** M4 Milestone

## Testing Checklist (Post-Implementation)

- [ ] Colored frame, left-aligned, terminal width 80
- [ ] Colored frame, center-aligned, terminal width 80
- [ ] Colored frame, right-aligned, terminal width 80
- [ ] Colored frame, center-aligned, terminal width 277
- [ ] Colored frame, right-aligned, terminal width 277
- [ ] Multiple colored frames stacked, all alignments
- [ ] Gradient frames (complex ANSI) with all alignments
- [ ] Very narrow terminal (40 chars)
- [ ] Frame wider than terminal (graceful degradation)
- [ ] Mixed colored and plain frames
- [ ] Grid layouts with colored frames
- [ ] All existing 655 tests pass

## Impact Analysis

**Breaking Changes:**
- None if we keep `stack()` returning strings
- Add `stack_structured()` as new API

**Migration Path:**
```python
# Old (v0.1.0)
layout = composer.stack([frame1, frame2], align="right", width=terminal_width)
for line in layout:
    console.print(line, highlight=False, soft_wrap=False)

# New (v0.2.0 / M4)
layout = composer.stack([frame1, frame2], align="right")  # No width needed
console.print_layout(layout)  # Console handles alignment
```

**Benefits:**
- ✅ Perfect alignment to terminal edge
- ✅ No wrapping with colored frames
- ✅ Cleaner API (Console handles rendering)
- ✅ Better separation of concerns
- ✅ Enables future features (animations, dynamic resize, etc.)

## References

- Original issue: `examples/showcase/rainbow_fat_alignment.py` wrapping
- Related: Terminal detection in `utils/terminal.py`
- Related: Visual width calculations in `utils/text.py`
- Architecture doc: `doc/project/PLAN.md`
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
