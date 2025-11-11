# VS16 Emoji Terminal Gluing Research & Implementation

**Status:** 📋 Planned
**Priority:** Medium
**Created:** 2025-11-02
**Target:** v1.1.0

______________________________________________________________________

## Problem Statement

Some VS16 (Variation Selector-16) emojis exhibit "gluing" behavior in terminals where the space after the emoji is visually collapsed, making the emoji appear directly attached to following text.

### Observed Behavior

**Gluing emojis (double space needed):**

```
⚙️ Services  → displays as: ⚙️Services (no visible space)
⏱️ Uptime    → displays as: ⏱️Uptime (no visible space)
⏸️ Waiting   → displays as: ⏸️Waiting (no visible space)
```

**Non-gluing emojis (work correctly):**

```
⚠️ Warning   → displays as: ⚠️ Warning (space visible)
ℹ️ Info      → displays as: ℹ️ Info (space visible)
```

### Current Workaround

Manually add double space after gluing emojis:

```python
# Code has double space, terminal displays single space
title="⚙️  Services"  # ⚙️ + VS16 + space + space
```

### Discovery Context

- **Found during:** Dashboard frame alignment fixes (2025-11-02)
- **Root cause:** Terminals render some VS16 emojis as 2-width even though base character is 1-width
- **Impact:** Visual appearance only (width calculations are correct)
- **Affects:** Frame titles, banner text, formatted output with VS16 emojis

______________________________________________________________________

## Research Phase: Systematic Discovery

### Objectives

1. **Identify all gluing VS16 emojis** from our Tier 1 supported set
1. **Test across multiple terminals** to understand terminal-specific behavior
1. **Find the pattern** - what characteristic causes gluing?
1. **Document findings** in emoji guidelines

### Research Script Requirements

Create `examples/testing/test_vs16_gluing.py`:

```python
"""Test VS16 emoji gluing behavior across terminals.

This script systematically tests all VS16 emojis from EMOJI_GUIDELINES.md
to identify which ones exhibit terminal "gluing" behavior (space collapse).
"""

from styledconsole.utils.text import SAFE_EMOJIS

# Extract all VS16 emojis from SAFE_EMOJIS
vs16_emojis = [
    emoji for emoji, info in SAFE_EMOJIS.items()
    if '\ufe0f' in emoji
]

# Test each emoji with single space
print("=" * 80)
print("VS16 EMOJI GLUING TEST")
print("=" * 80)
print()
print("Instructions:")
print("  1. Look at each line below")
print("  2. Note if there's visible space between emoji and 'Test'")
print("  3. Record 'GLUE' if no space visible, 'OK' if space visible")
print()
print("=" * 80)
print()

for emoji in sorted(vs16_emojis):
    info = SAFE_EMOJIS[emoji]
    codepoints = [hex(ord(c)) for c in emoji]

    # Test with single space
    print(f"|{emoji} Test| - {info['category']:15} - {codepoints}")

print()
print("=" * 80)
```

### Testing Matrix

| Terminal         | Version | OS      | Tester | Date | Results File                   |
| ---------------- | ------- | ------- | ------ | ---- | ------------------------------ |
| GNOME Terminal   | ?       | Linux   | ?      | ?    | `results/gnome_terminal.txt`   |
| Kitty            | ?       | Linux   | ?      | ?    | `results/kitty.txt`            |
| Alacritty        | ?       | Linux   | ?      | ?    | `results/alacritty.txt`        |
| iTerm2           | ?       | macOS   | ?      | ?    | `results/iterm2.txt`           |
| Windows Terminal | ?       | Windows | ?      | ?    | `results/windows_terminal.txt` |
| VSCode Terminal  | ?       | All     | ?      | ?    | `results/vscode_terminal.txt`  |

### Expected Outcomes

**Pattern hypothesis:**

- VS16 emojis where `wcwidth(base_char) == 1` but terminal renders as 2-width
- Possibly related to Unicode blocks (e.g., Miscellaneous Symbols U+2600-U+26FF)
- May vary by terminal emulator

**Documentation deliverable:**

- Create `doc/guides/VS16_TERMINAL_GLUING.md`
- Update `doc/guides/EMOJI_RENDERING.md` with gluing section
- Add table of known gluing emojis to `doc/guides/EMOJI_GUIDELINES.md`

______________________________________________________________________

## Implementation Phase: Library Support

### Phase 1: Detection API

Add to `src/styledconsole/utils/text.py`:

```python
# Known VS16 emojis that exhibit gluing behavior in common terminals
VS16_GLUING_EMOJIS = frozenset([
    '\u2699\ufe0f',  # ⚙️ GEAR
    '\u23f1\ufe0f',  # ⏱️ STOPWATCH
    '\u23f8\ufe0f',  # ⏸️ PAUSE BUTTON
    # ... more from research results
])

def needs_spacing_workaround(text: str) -> bool:
    """Check if text contains VS16 emojis that need spacing workaround.

    Some VS16 emojis exhibit "gluing" behavior in terminals where the
    space after the emoji is visually collapsed. This function detects
    if text contains such emojis.

    Args:
        text: Text to check for gluing emojis

    Returns:
        True if text contains gluing VS16 emojis, False otherwise

    Example:
        >>> needs_spacing_workaround("⚙️ Services")
        True
        >>> needs_spacing_workaround("⚠️ Warning")
        False
    """
    return any(emoji in text for emoji in VS16_GLUING_EMOJIS)

def apply_spacing_workaround(text: str) -> str:
    """Apply spacing workaround for VS16 gluing emojis.

    Adds extra space after VS16 emojis that exhibit terminal gluing
    behavior. The extra space compensates for terminal rendering that
    visually collapses the first space.

    Args:
        text: Text containing VS16 emojis

    Returns:
        Text with spacing workaround applied

    Example:
        >>> apply_spacing_workaround("⚙️ Services")
        '⚙️  Services'  # Double space after emoji
        >>> apply_spacing_workaround("⚠️ Warning")
        '⚠️ Warning'  # No change needed
    """
    result = text
    for emoji in VS16_GLUING_EMOJIS:
        if emoji in result:
            # Replace "emoji + space" with "emoji + double space"
            result = result.replace(f"{emoji} ", f"{emoji}  ")
    return result
```

### Phase 2: Optional Auto-Fix in RenderingEngine

Add parameter to `Console.frame()` and `Console.banner()`:

```python
def frame(
    self,
    content: str | list[str],
    *,
    title: str | None = None,
    auto_spacing: bool = True,  # NEW: Auto-apply VS16 spacing workaround
    # ... existing parameters
) -> None:
    """Render a frame.

    Args:
        auto_spacing: If True, automatically apply spacing workaround for
            VS16 emojis that exhibit terminal gluing behavior. Set to False
            if you've already applied the workaround manually or want to
            disable it. Defaults to True.
    """
    # Apply workaround to title if enabled
    if auto_spacing and title and needs_spacing_workaround(title):
        title = apply_spacing_workaround(title)

    # Existing rendering logic...
```

### Phase 3: Terminal-Specific Profiles

Extend `TerminalManager` to detect terminal type:

```python
# In src/styledconsole/core/terminal_manager.py

class TerminalProfile:
    """Terminal capabilities and quirks."""

    vs16_gluing_behavior: bool = True  # NEW: Does this terminal have VS16 gluing?
    # ... existing fields

def detect_terminal_type() -> str:
    """Detect specific terminal emulator.

    Returns:
        Terminal identifier: 'gnome-terminal', 'kitty', 'alacritty',
        'iterm2', 'windows-terminal', 'vscode', 'unknown'
    """
    # Check environment variables
    if 'KITTY_WINDOW_ID' in os.environ:
        return 'kitty'
    elif 'ALACRITTY_SOCKET' in os.environ:
        return 'alacritty'
    # ... more detection logic
```

______________________________________________________________________

## Testing Strategy

### Unit Tests

Add to `tests/unit/test_text_utils.py`:

```python
class TestVS16Gluing:
    """Test VS16 emoji gluing detection and workaround."""

    def test_needs_spacing_workaround_detects_gear(self):
        assert needs_spacing_workaround("⚙️ Services")

    def test_needs_spacing_workaround_ignores_warning(self):
        assert not needs_spacing_workaround("⚠️ Warning")

    def test_apply_spacing_workaround_adds_space(self):
        result = apply_spacing_workaround("⚙️ Services")
        assert result == "⚙️  Services"  # Double space

    def test_apply_spacing_workaround_preserves_non_gluing(self):
        result = apply_spacing_workaround("⚠️ Warning")
        assert result == "⚠️ Warning"  # Unchanged
```

### Integration Tests

Add to `tests/integration/test_vs16_gluing.py`:

```python
def test_frame_auto_applies_spacing_workaround():
    """Frame titles with gluing emojis get automatic spacing."""
    console = Console()
    # Should auto-convert "⚙️ Services" to "⚙️  Services"
    console.frame(["Test"], title="⚙️ Services")
    # Verify output has visible space

def test_frame_respects_auto_spacing_false():
    """Can disable auto-spacing if already applied manually."""
    console = Console()
    console.frame(["Test"], title="⚙️  Services", auto_spacing=False)
    # Should not add third space
```

### Visual Tests

Create `examples/testing/visual_vs16_spacing.py`:

- Display frames with all known gluing emojis
- Compare with/without workaround
- Manual visual verification

______________________________________________________________________

## Documentation Updates

### 1. Update `doc/guides/EMOJI_RENDERING.md`

Add new section after "Variation Selector-16":

````markdown
## Terminal Gluing Behavior (v1.1.0+)

### Problem: Visual Space Collapse

Some VS16 emojis exhibit "gluing" in certain terminals where the space
after the emoji is visually collapsed, even though width calculations
are correct.

**Example:**
```python
title = "⚙️ Services"  # Has space in code
# Terminal displays: ⚙️Services (no visible space!)
````

### Known Gluing Emojis

| Emoji | Unicode     | Name         | Base Width | Rendered Width |
| ----- | ----------- | ------------ | ---------- | -------------- |
| ⚙️    | U+2699+FE0F | GEAR         | 1          | 2              |
| ⏱️    | U+23F1+FE0F | STOPWATCH    | 1          | 2              |
| ⏸️    | U+23F8+FE0F | PAUSE BUTTON | 1          | 2              |

*(See full list in research results)*

### Workaround: Double Space

```python
# Manual workaround (v0.3.0 - v1.0.0)
title = "⚙️  Services"  # Double space compensates

# Automatic workaround (v1.1.0+)
console.frame(["content"], title="⚙️ Services", auto_spacing=True)
# Library auto-applies double space
```

### Why This Happens

**Theory:** Terminals render these VS16 emojis as full 2-width emoji
presentation, even though the base character has `wcwidth=1`. The emoji
rendering "consumes" the following space position, making it invisible.

**Affected emojis:** Primarily narrow base characters (wcwidth=1) from
Miscellaneous Symbols block (U+2600-U+26FF) with VS16 selector.

````

### 2. Update `doc/guides/EMOJI_GUIDELINES.md`

Add after "Variation Selector Issues" section:

```markdown
## VS16 Terminal Gluing (v1.1.0+)

### Gluing Behavior

Some VS16 emojis appear "glued" to following text in terminals:

**Affected Emojis:**
- ⚙️ GEAR (U+2699+FE0F) - appears as ⚙️Services instead of ⚙️ Services
- ⏱️ STOPWATCH (U+23F1+FE0F) - appears as ⏱️Uptime instead of ⏱️ Uptime
- ⏸️ PAUSE (U+23F8+FE0F) - appears as ⏸️Waiting instead of ⏸️ Waiting

**Workaround (Manual - v0.3.0+):**
```python
# Use double space in code
title = "⚙️  Services"  # Terminal displays: ⚙️ Services (single space visible)
````

**Automatic Fix (v1.1.0+):**

```python
# Library auto-detects and fixes
console.frame(["content"], title="⚙️ Services")  # Auto-converts to double space
```

**Disable auto-fix:**

```python
console.frame(["content"], title="⚙️  Services", auto_spacing=False)
```

```

### 3. Create `doc/guides/VS16_TERMINAL_GLUING.md`

Complete technical deep-dive document with:
- Terminal rendering theory
- Width calculation vs visual display
- Research methodology and results
- Terminal-specific behavior matrix
- Workaround implementation details

---

## Success Criteria

### Research Phase Complete When:
- [ ] All Tier 1 VS16 emojis tested in at least 3 terminals
- [ ] Pattern identified and documented
- [ ] Known gluing emojis cataloged in `VS16_GLUING_EMOJIS`
- [ ] Documentation updated with findings

### Implementation Phase Complete When:
- [ ] `needs_spacing_workaround()` function added and tested
- [ ] `apply_spacing_workaround()` function added and tested
- [ ] `auto_spacing` parameter added to `Console.frame()` and `Console.banner()`
- [ ] 10+ unit tests added (95%+ coverage maintained)
- [ ] 3+ integration tests added
- [ ] Visual test example created
- [ ] All existing examples still work (auto_spacing=True by default)

### Documentation Phase Complete When:
- [ ] `EMOJI_RENDERING.md` updated with gluing section
- [ ] `EMOJI_GUIDELINES.md` updated with workaround guide
- [ ] `VS16_TERMINAL_GLUING.md` created with full research
- [ ] CHANGELOG.md updated for v1.1.0
- [ ] Migration guide created (if breaking changes)

---

## Related Issues

- Dashboard alignment fix (2025-11-02) - discovered the issue
- Rich Panel title alignment fix - enabled proper testing
- VS16 width calculation fix (v0.1.0) - related but different issue

---

## Notes

- This is a **terminal rendering quirk**, not a library bug
- Width calculations are correct; visual display is affected
- Workaround is cosmetic (adds space for visual correctness)
- Auto-spacing should be opt-out (default=True) for best UX
- Consider adding `STYLEDCONSOLE_AUTO_SPACING=0` env var for global disable

---

## Estimated Effort

- Research Phase: 4-6 hours (testing across terminals)
- Implementation Phase: 6-8 hours (API + tests)
- Documentation Phase: 2-3 hours
- **Total:** 12-17 hours

---

## Dependencies

- Requires completion of deprecation removal (v1.0.0)
- No external library dependencies needed
- Benefits from existing terminal detection in `TerminalManager`
```
