# Gallery Examples Fix - Phase 3 Quality Issues

**Date:** 2025-11-12\
**Status:** 🔴 Blocked - Requires systematic fixing\
**Files Affected:** 5 gallery examples (~3,000 lines)\
**Root Cause:** Created without reviewing codebase/documentation first

______________________________________________________________________

## Problem Summary

All 5 gallery examples (`borders_showcase.py`, `colors_showcase.py`, `gradients_showcase.py`, `emojis_showcase.py`, `banners_showcase.py`) were created with fundamental violations of project standards. They use incorrect APIs, manual frame drawing, and raw emoji usage instead of library functions.

**Impact:** Examples will be copied by users → must show correct API usage. Current state violates "examples as reference quality" principle from DOCUMENTATION_POLICY.md.

______________________________________________________________________

## Violations Found

### 1. Wrong Banner API (ALL 5 FILES)

**Current (WRONG):**

```python
console.banner(
    "Title",
    style="gradient",           # ❌ Parameter doesn't exist
    colors=["red", "blue"]      # ❌ Parameter doesn't exist
)
```

**Correct:**

```python
console.banner(
    "Title",
    start_color="red",          # ✅ Correct parameter
    end_color="blue"            # ✅ Correct parameter
)
```

**Affected lines:**

- `borders_showcase.py`: lines 26, 58, 91, 125, 159, 196, 229, 261
- `colors_showcase.py`: multiple banner calls throughout
- `gradients_showcase.py`: multiple banner calls throughout
- `emojis_showcase.py`: multiple banner calls throughout
- `banners_showcase.py`: nearly every banner call (500+ lines)

**API Reference:**

```python
# From src/styledconsole/console.py
def banner(
    self,
    text: str,
    font: str = "standard",
    start_color: str | tuple[int, int, int] | None = None,
    end_color: str | tuple[int, int, int] | None = None,
    border: str = "solid",
    width: int | None = None,
    align: AlignType = "center",
    padding: int = 1,
) -> None:
```

### 2. Manual Frame Drawing (FORBIDDEN)

**Issue:** Using box-drawing characters in strings instead of `console.frame()`.

**Examples:**

```python
# borders_showcase.py, lines 177-182 (WRONG):
content = """
┏━━━━━━━━━━━━━━━━━━━━━━━━┓
┃   🔒 Protected Zone   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
console.text(content)  # ❌ Manual frame drawing with raw emoji

# Should be (CORRECT):
from styledconsole import EMOJI

content = f"{EMOJI.LOCK} Protected Zone"  # ✅ Use EMOJI constant
console.frame(
    content,
    border="double",
    border_color="yellow"
)  # ✅ Uses library function
```

**Affected locations:**

- `borders_showcase.py`: lines 177-182 (nested frame), lines 299-310 (comparison table)
- `gradients_showcase.py`: lines 465-480 (nested gradient frames)

**Why forbidden:**

- Breaks ANSI handling (wrapping bugs)
- Violates v0.3.0 Rich-native rendering architecture
- Bypasses emoji-safe width calculations from `utils/text.py`

**CRITICAL when fixing:**
When replacing manual frames, emojis MUST be referenced via EMOJI constants:

```python
# WRONG (double violation):
content = "🔒 Protected Zone"  # ❌ Raw emoji in manual frame

# CORRECT:
from styledconsole import EMOJI
content = f"{EMOJI.LOCK} Protected Zone"  # ✅ EMOJI constant
console.frame(content, border="double")    # ✅ Library function
```

### 3. Raw Emoji Usage (MUST USE CONSTANTS)

**Issue:** Using UTF-8 emoji literals instead of EMOJI constants from `src/styledconsole/emojis.py`.

**Examples:**

```python
# WRONG:
title = "🚀 Launch Sequence"         # ❌ Raw UTF-8
content = "Status: ✅ Ready"         # ❌ Raw UTF-8

# CORRECT:
from styledconsole import EMOJI
title = f"{EMOJI.ROCKET} Launch Sequence"      # ✅ Uses constant
content = f"Status: {EMOJI.CHECK} Ready"       # ✅ Uses constant
```

**Raw emojis found in `borders_showcase.py`:**

- Line 99: ⚡ (should be EMOJI.ZAP)
- Line 129: 🎆 (should be EMOJI.FIREWORKS)
- Line 133: 💪 (should be EMOJI.FLEXED_BICEPS)
- Line 147: ⚡ (should be EMOJI.ZAP)
- Line 163: 🛡️ (should be EMOJI.SHIELD)
- Line 167: 🏰 (should be EMOJI.CASTLE)
- Line 180: 🔒 (should be EMOJI.LOCK)
- Line 203: 🌸 (should be EMOJI.BLOSSOM)
- Line 217: 🦋 (should be EMOJI.BUTTERFLY)
- Line 268: ⚡ (should be EMOJI.ZAP)
- Line 306: 💎 (should be EMOJI.GEM_STONE)
- Line 313: 🏛️ (should be EMOJI.CLASSICAL_BUILDING)

**All other gallery files have similar raw emoji usage.**

**Why required:**

- Tier 1 emoji safety (cross-platform compatibility)
- Consistent with project emoji strategy (EMOJI_GUIDELINES.md)
- Examples must demonstrate proper library usage

### 4. Missing Local Content Variables Pattern

**Issue:** Content inlined in function calls instead of using local variables with f-strings.

**Current pattern (INCONSISTENT):**

```python
console.frame("Some content here", title="Title")
console.text("More content")
```

**Should follow usecases pattern (CONSISTENT):**

```python
# From examples/usecases/alerts.py:
title = f"{EMOJI.WARNING} System Alert"
content = f"""
{EMOJI.INFO} Server maintenance scheduled
{EMOJI.CLOCK} Time: 2024-03-15 02:00 UTC
{EMOJI.HOURGLASS} Duration: ~2 hours
"""
console.frame(content, title=title, border="double", border_color="yellow")
```

**Why required:**

- Readability: separates data from presentation
- Maintainability: easy to modify content
- Reference quality: users can copy the pattern
- Follows established convention from Phase 2 examples

______________________________________________________________________

## Correct API Reference

### Console.banner() - VERIFIED 2025-11-12

```python
console.banner(
    text="TITLE",
    font="standard",              # pyfiglet font name
    start_color="red",            # Gradient start (CSS4/hex/RGB)
    end_color="blue",             # Gradient end (CSS4/hex/RGB)
    border="solid",               # Border style name
    width=None,                   # Auto-width if None
    align="center",               # left|center|right
    padding=1                     # Internal padding
)
```

**Parameters that DON'T exist:**

- ❌ `style="gradient"` - WRONG
- ❌ `colors=[...]` - WRONG
- ❌ Any other style variants

### Console.text() - VERIFIED 2025-11-12

```python
console.text(
    text="content",
    color="white",                # CSS4/hex/RGB
    bold=False,                   # Boolean flag
    italic=False,                 # Boolean flag
    underline=False,              # Boolean flag
    dim=False,                    # Boolean flag
    end="\n"                      # Line ending
)
```

**Parameters that DON'T exist:**

- ❌ `style="bold red"` - WRONG (partially fixed by sed)
- ❌ `align="center"` - WRONG (partially fixed by sed)

### Console.frame() - PRIMARY METHOD

```python
console.frame(
    content="text",
    title="Title",
    border="solid",               # solid|rounded|double|thick|dashed|minimal|ascii|heavy
    width=None,                   # Auto-width if None
    padding=1,                    # Internal padding
    align="left",                 # left|center|right (content alignment)
    content_color="white",        # CSS4/hex/RGB
    border_color="blue",          # CSS4/hex/RGB
    title_color="cyan",           # CSS4/hex/RGB
    start_color=None,             # Gradient start (overrides border_color)
    end_color=None                # Gradient end (overrides border_color)
)
```

**Use for ALL boxed content - never draw frames manually.**

______________________________________________________________________

## Systematic Fix Plan

### Phase 1: borders_showcase.py (PRIORITY)

1. **Fix banner calls (8 locations):**

   - Lines 26, 58, 91, 125, 159, 196, 229, 261
   - Replace: `style="gradient", colors=["x", "y"]`
   - With: `start_color="x", end_color="y"`

1. **Remove manual frames AND use EMOJI constants:**

   - Lines 177-182: Replace manual box drawing with `console.frame()`
   - **MUST** convert raw emojis to EMOJI constants when removing manual frames
   - Example: `"🔒 Zone"` → `f"{EMOJI.LOCK} Zone"` → `console.frame(content, ...)`
   - Lines 299-310: Replace with proper frame or table layout
   - **Pattern:** Manual frame removal = mandatory EMOJI constant conversion

1. **Replace raw emojis (12 locations):**

   - Add import: `from styledconsole import EMOJI`
   - Replace all raw emojis with EMOJI constants (see list in section 3)

1. **Add local content variables:**

   - Extract inline strings to variables
   - Use f-strings with EMOJI constants
   - Follow pattern from `examples/usecases/alerts.py`

1. **Test:**

   ```bash
   uv run python examples/gallery/borders_showcase.py
   ```

### Phase 2: colors_showcase.py

- Same 4-step process (banner API, raw emojis, content variables, test)
- Focus: Demonstrate CSS4 color palette properly
- Verify gradient demonstrations use correct API

### Phase 3: gradients_showcase.py

- Fix banner API calls
- **Critical:** Remove manual nested frames (lines 465-480)
- Demonstrate `gradient_frame()`, `diagonal_gradient_frame()`, `rainbow_frame()` from effects.py
- Replace raw emojis with EMOJI constants

### Phase 4: emojis_showcase.py

- **Ironic issue:** Emoji showcase doesn't use EMOJI constants
- Rewrite to properly demonstrate `from styledconsole import EMOJI`
- Show each emoji category (symbols, faces, objects, etc.)
- Use frame() for categorized displays

### Phase 5: banners_showcase.py

- **Most affected:** Nearly every banner call has wrong API
- Replace `style="rainbow"`, `style="gradient"` throughout
- Use start_color/end_color for gradients
- Demonstrate actual pyfiglet font catalog
- Show Banner class usage if needed

______________________________________________________________________

## Testing Checklist

After fixing each file:

- [ ] `uv run python examples/gallery/FILE.py` executes without errors
- [ ] No raw emojis (search: `grep -P "[^\x00-\x7F]" FILE.py` only shows EMOJI assignments)
- [ ] No manual frames (search: `grep "[┌┐└┘─│┏┓┗┛━┃]" FILE.py` returns empty)
- [ ] All banner calls use start_color/end_color (search: `grep "style=" FILE.py` in banner context returns empty)
- [ ] Visual output matches creative intent
- [ ] Code follows usecases pattern (local variables, EMOJI.\*, proper API)

______________________________________________________________________

## Reference Examples (CORRECT PATTERNS)

### Good Example: examples/usecases/alerts.py

```python
from styledconsole import Console, EMOJI

def show_alerts():
    console = Console()

    # ✅ Local content variable with EMOJI constants
    warning_content = f"""
{EMOJI.WARNING} System Alert
{EMOJI.INFO} Server maintenance scheduled
{EMOJI.CLOCK} Time: 2024-03-15 02:00 UTC
"""

    # ✅ Uses console.frame() with proper API
    console.frame(
        warning_content,
        title=f"{EMOJI.WARNING} Warning",
        border="double",
        border_color="yellow"
    )

    # ✅ Banner with correct API
    console.banner(
        "CRITICAL",
        font="banner",
        start_color="red",      # ✅ Not style="gradient"
        end_color="yellow"      # ✅ Not colors=[...]
    )
```

### Reference for Gradients: src/styledconsole/effects.py

```python
from styledconsole.effects import gradient_frame, diagonal_gradient_frame, rainbow_frame

# Horizontal gradient
gradient_frame(
    console,
    "Content",
    title="Title",
    start_color="blue",
    end_color="purple",
    border="rounded"
)

# Diagonal gradient
diagonal_gradient_frame(
    console,
    "Content",
    title="Title",
    colors=["red", "orange", "yellow"],  # ✅ Note: effects.py uses colors, banner() doesn't
    border="double"
)

# Rainbow effect
rainbow_frame(
    console,
    "Content",
    title="Title",
    border="heavy"
)
```

______________________________________________________________________

## Lessons Learned

1. **Always review codebase before implementing:**

   - Read actual API signatures in source code
   - Review existing examples for patterns
   - Check documentation policy first

1. **Examples are reference quality:**

   - Users will copy them verbatim
   - Wrong APIs in examples propagate to user code
   - "Code as documentation" principle applies doubly

1. **Test incrementally:**

   - Run examples during creation, not after
   - Catch API errors immediately
   - Verify output matches intent

1. **Follow established patterns:**

   - Phase 2 usecases established the pattern
   - Don't invent new patterns without reason
   - Consistency > individual creativity

______________________________________________________________________

## Completion Criteria

Gallery examples are **DONE** when:

1. ✅ All 5 files execute without errors
1. ✅ All banner calls use start_color/end_color API
1. ✅ All frames use console.frame(), zero manual drawing
1. ✅ All emojis use EMOJI constants, zero raw UTF-8
1. ✅ All files follow usecases pattern (local variables)
1. ✅ Visual output is creative and showcases features properly
1. ✅ Code is reference quality (users can copy confidently)
1. ✅ Committed with message: "feat(examples): Add 5 gallery showcase examples"

______________________________________________________________________

## Next Session Action Items

1. Start with `borders_showcase.py` (foundational)
1. Apply 4-step fix process systematically
1. Test after each file before moving to next
1. Commit when all 5 pass quality checks
1. Update this document status to ✅ Complete
