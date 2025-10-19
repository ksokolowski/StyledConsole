# Border Gradients - Feature Proposal

## Current Status: Not Implemented (Proposed for Phase 3)

### What Works Now ✅

**Content Gradients** - Fully supported!
```python
frame_renderer.render(
    ["Line 1", "Line 2", "Line 3"],
    gradient_start="red",
    gradient_end="blue",
    border="rounded"
)
# Each line gets a different color from red → purple → blue
```

**Single Border Color** - Fully supported!
```python
frame_renderer.render(
    ["Content"],
    border_color="cyan",
    border="double"
)
# Entire border is cyan
```

### What Doesn't Work Yet ❌

**Border Gradients** - Not yet implemented
```python
# This would be AMAZING but doesn't exist yet:
frame_renderer.render(
    ["Content"],
    border_gradient_start="red",
    border_gradient_end="blue",
    border="rounded"
)
# Would make border transition from red → blue vertically
```

## Why Border Gradients Are Tricky

1. **Multiple Border Components**:
   - Top border (1 line)
   - Left/Right borders (N lines for N content lines)
   - Bottom border (1 line)

2. **Gradient Direction Options**:
   - **Vertical**: Top→Bottom (most common)
   - **Horizontal**: Left→Right (per line)
   - **Diagonal**: Corner→Corner (complex)

3. **Character-Level Coloring**:
   - Each border character needs individual coloring
   - Box-drawing characters must maintain visual continuity
   - Performance considerations with many ANSI codes

## Proposed Implementation (Phase 3)

### API Design

```python
@dataclass
class Frame:
    # ... existing fields ...
    border_gradient_start: str | None = None
    border_gradient_end: str | None = None
    border_gradient_direction: Literal["vertical", "horizontal"] = "vertical"
```

### Usage Examples

```python
# Example 1: Vertical gradient (fire effect)
frame_renderer.render(
    ["Status: Online", "Requests: 1.2M"],
    title="🔥 Server",
    border="heavy",
    border_gradient_start="yellow",
    border_gradient_end="red",
    border_gradient_direction="vertical"
)
# Top border: yellow
# Side borders: yellow → orange → red (interpolated)
# Bottom border: red

# Example 2: Rainbow border
frame_renderer.render(
    ["🌈 Rainbow Frame"],
    border="double",
    border_gradient_start="red",
    border_gradient_end="violet"
)

# Example 3: Content + Border gradients together!
frame_renderer.render(
    ["Line 1", "Line 2", "Line 3"],
    gradient_start="blue",           # Content: blue → yellow
    gradient_end="yellow",
    border_gradient_start="magenta", # Border: magenta → cyan
    border_gradient_end="cyan",
    border="rounded"
)
# Ultimate visual effect! 🎨
```

### Implementation Approach

```python
def _render_border_with_gradient(
    self,
    border_line: str,
    line_index: int,
    total_lines: int,
    gradient_start: str,
    gradient_end: str
) -> str:
    """Apply gradient to border line based on vertical position."""
    # Calculate gradient position (0.0 to 1.0)
    t = line_index / max(total_lines - 1, 1)

    # Interpolate color
    color = interpolate_color(gradient_start, gradient_end, t)

    # Apply to entire border line
    return self._colorize(border_line, color)
```

### Edge Cases to Handle

1. **Title in top border**: Should title inherit border gradient color at that position?
2. **Single-line frames**: Both borders get same color (no gradient visible)
3. **Very tall frames**: Smooth gradient or stepped?
4. **Horizontal gradients**: Character-by-character coloring (expensive!)
5. **Validation**: Both gradient params required together

## Visual Impact

### Before (Single Color)
```
┌─── Title ───┐   <- All cyan
│  Content    │   <- All cyan
└─────────────┘   <- All cyan
```

### After (Vertical Gradient)
```
┌─── Title ───┐   <- Red
│  Content    │   <- Orange (interpolated)
└─────────────┘   <- Yellow
```

### Ultimate (Content + Border Gradients)
```
┌─── Title ───┐   <- Border: Red
│  Line 1     │   <- Border: Orange, Content: Blue
│  Line 2     │   <- Border: Orange, Content: Cyan
│  Line 3     │   <- Border: Yellow, Content: Green
└─────────────┘   <- Border: Yellow
```

## Complexity Estimate

- **Implementation**: 2-3 days
- **Testing**: 1 day
- **Documentation**: 0.5 day
- **Total**: ~4 days

## Priority

- **Phase 1**: ✅ Complete (Core features)
- **Phase 2**: ✅ Complete (Type safety, public API)
- **Phase 3**: 🔄 In planning
  - Border gradients
  - Horizontal content gradients
  - Diagonal gradients
  - Animation support (future)

## Workarounds Until Implementation

### Option 1: Use High-Contrast Single Colors
```python
# Make borders stand out with bright colors
frame_renderer.render(
    content,
    gradient_start="red",      # Content has gradient ✅
    gradient_end="blue",
    border_color="yellow",     # Border is solid yellow
)
```

### Option 2: Multiple Nested Frames
```python
# Create "fake" gradient by stacking frames
outer = frame_renderer.render(
    inner_content,
    border="solid",
    border_color="red"
)

middle = frame_renderer.render(
    outer,
    border="solid",
    border_color="orange"
)

# Not true gradient but creates layered effect
```

### Option 3: ASCII Art Borders
```python
# Use ASCII art to simulate gradient effect
print("╔════ 🔥 FIRE EFFECT 🔥 ════╗")  # Yellow
print("║  Content goes here        ║")  # Orange
print("╚═══════════════════════════╝")  # Red
# Manual coloring per line
```

## Related Features

Once border gradients are implemented, these become possible:

1. **Animated gradients**: Rotate gradient colors over time
2. **Pulsing borders**: Alternate between two gradients
3. **Rainbow mode**: Automatic rainbow gradient
4. **Theme presets**: Pre-configured gradient combinations
5. **Gradient blending**: Smooth transitions between frames

## User Feedback

Based on user request (October 19, 2025):
> "How about gradient applied not to frame content but gradient applied to frame border itself? :D"

**Response**: Great idea! This would be an excellent Phase 3 feature. Current workaround is using high-contrast single border colors with content gradients, which still looks amazing! 🎨

## Decision: Implement or Defer?

**Recommendation**: Defer to Phase 3

**Reasons**:
1. Content gradients already work great ✅
2. Single border colors provide good visual impact ✅
3. Complex implementation (4 days effort)
4. Need to finalize Phase 2 features first
5. Could gather more user feedback on desired gradient directions

**Alternative**: Quick prototype with vertical-only gradients (2 days) for user testing

---

**Status**: 📝 Documented as future feature
**Created**: October 19, 2025
**Priority**: Medium (Phase 3)
**User Interest**: High! 🎨
