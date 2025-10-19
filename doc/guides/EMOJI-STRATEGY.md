# Emoji/Icon Support Strategy

**Project:** StyledConsole
**Version:** MVP v0.1 → v0.3+
**Date:** October 15, 2025

---

## The Problem

Different emoji types have vastly different complexity levels and terminal support:

1. **Encoding complexity:** Single codepoint vs multi-codepoint sequences
2. **Width calculation:** Some emojis render as width=1, some width=2, some unpredictable
3. **Terminal support:** Modern terminals handle basic icons well, but struggle with compound emojis
4. **Alignment issues:** Complex emojis can break frame borders and text alignment

**Impact on StyledConsole:** Since we render frames with precise borders, even 1-character width miscalculation breaks the entire layout.

---

## Solution: Tiered Support

We implement emoji support in **three tiers**, each with increasing complexity:

### Tier 1: Basic Icons (MVP v0.1) ✅

**Target:** Single-codepoint symbols and emojis that are universally supported

**Examples:**
- Status indicators: ✅ ❌ ⚠️ ℹ️
- Common icons: ⭐ 🚀 ❤️ 🎉 💡 🔥 📊 🎯
- Simple emojis: 😀 😎 👍 🏆 ⚡

**Characteristics:**
- Single Unicode codepoint
- Predictable width=2 in terminals
- Supported since Unicode 6.0 (2010+)
- Works in 95%+ of modern terminals

**Implementation:**
- Use `wcwidth` library for width calculation
- Simple grapheme detection with `regex` library
- Conservative fallback to ASCII when detection fails

**Coverage:** ~200 commonly used icons/emojis

**Why MVP:** These cover 95% of test reporting use cases (status, metrics, decorations)

---

### Tier 2: Modified Emojis (v0.2) 🔜

**Target:** Emojis with modifiers (skin tones, gender, presentation selectors)

**Examples:**
- Skin tone modifiers: 👍🏽 👨🏻 👩🏿
- Emoji presentation selector: 🏳️ (flag with U+FE0F)
- Gender modifiers: ♂️ ♀️

**Characteristics:**
- 2-3 Unicode codepoints (base + modifier)
- Width typically 2, but can vary
- Supported in most modern terminals (2015+)
- May render inconsistently on older terminals

**Implementation:**
- Enhanced grapheme cluster detection
- Track modifier sequences as single unit
- Per-terminal testing for width edge cases

**Coverage:** ~2,000 emoji variants

**When:** After v0.1 is stable, based on user feedback requesting skin tone support

---

### Tier 3: ZWJ Sequences (v0.3+) 🔮

**Target:** Complex multi-emoji compounds joined with Zero-Width Joiner (ZWJ)

**Examples:**
- Family: 👨‍👩‍👧‍👦 (man + ZWJ + woman + ZWJ + girl + ZWJ + boy)
- Profession: 👨‍💻 (man + ZWJ + laptop)
- Flag: 🏳️‍🌈 (white flag + ZWJ + rainbow)

**Characteristics:**
- 4+ Unicode codepoints (multiple emojis + ZWJ + optional modifiers)
- Width unpredictable (2-4 characters)
- Highly terminal-dependent rendering
- May break or display as separate emojis on older terminals

**Implementation:**
- Full Unicode segmentation (may require `grapheme` library)
- Per-sequence width measurement
- Terminal capability detection (emoji ZWJ support flag)
- Graceful degradation (show base emoji only)

**Coverage:** ~3,000 ZWJ sequences

**When:** Post-MVP, when terminal support is more mature (2026+)

---

## Technical Details

### Width Calculation Hierarchy

```python
def visual_width(text: str) -> int:
    """
    Tier 1 (v0.1): wcwidth-based calculation
    - Works for single-codepoint emojis
    - Fast and reliable for basic cases
    """
    from wcwidth import wcswidth
    width = wcswidth(strip_ansi(text))
    return width if width >= 0 else len(text)

def visual_width_enhanced(text: str) -> int:
    """
    Tier 2/3 (v0.2+): Grapheme cluster-based
    - Handles modifiers and ZWJ sequences
    - More accurate but slower
    """
    import grapheme
    clusters = list(grapheme.graphemes(text))
    return sum(measure_cluster(c) for c in clusters)
```

### Terminal Capability Detection

| Feature | Detection Method | Fallback |
|---------|-----------------|----------|
| Basic emoji support | UTF-8 locale + color support | ASCII replacements (✅→[OK], ❌→[X]) |
| Skin tone support | Test render + measure | Show base emoji without modifier |
| ZWJ support | Terminal version detection | Show first emoji in sequence |

---

## Migration Path

### v0.1.0 Release (MVP)
- ✅ Tier 1 basic icons fully supported
- ✅ Documentation warns about Tier 2/3 limitations
- ✅ Test suite covers 200+ common icons
- ⚠️ Known issue: Skin tones may have ±1 width errors
- ⚠️ Known issue: ZWJ sequences may break frames

### v0.2.0 Release
- ✅ Tier 2 modified emojis supported
- ✅ Enhanced grapheme detection
- ⚠️ ZWJ sequences still limited

### v0.3.0+ Release
- ✅ Tier 3 ZWJ sequences supported
- ✅ Full Unicode segmentation
- ✅ Complete emoji compatibility matrix

---

## User Documentation

### Quick Start (v0.1)

```python
from styledconsole import Console

console = Console()

# ✅ SAFE: These work reliably in v0.1
console.frame("Build passed ✅", title="Status")
console.frame("3 tests failed ❌", title="Results")
console.frame("Warning: Rate limit ⚠️", title="Alert")

# ⚠️ LIMITED: These may misalign in v0.1
console.frame("Great job 👍🏽", title="Feedback")  # Skin tone
console.frame("Family photo 👨‍👩‍👧‍👦", title="Album")  # ZWJ sequence
```

### Emoji Compatibility Table

| Emoji Type | Example | v0.1 | v0.2 | v0.3+ |
|------------|---------|------|------|-------|
| Basic icons | ✅ ❌ ⚠️ | ✅ | ✅ | ✅ |
| Simple emojis | 🚀 ❤️ 🎉 | ✅ | ✅ | ✅ |
| Skin tones | 👍🏽 👨🏻 | ⚠️ | ✅ | ✅ |
| Gender modifiers | ♂️ ♀️ | ⚠️ | ✅ | ✅ |
| ZWJ sequences | 👨‍💻 🏳️‍🌈 | ❌ | ⚠️ | ✅ |
| Complex families | 👨‍👩‍👧‍👦 | ❌ | ⚠️ | ✅ |

**Legend:**
- ✅ Fully supported, reliable alignment
- ⚠️ Partial support, may have edge cases
- ❌ Not supported, may break frames

---

## Testing Strategy

### Tier 1 Test Coverage (v0.1)

```python
# Basic icon suite (mandatory for MVP)
TIER1_TEST_ICONS = [
    "✅", "❌", "⚠️", "ℹ️",  # Status
    "⭐", "🚀", "❤️", "🎉",  # Common
    "💡", "🔥", "📊", "🎯",  # Misc
    "😀", "😎", "👍", "🏆",  # Simple emojis
]

def test_tier1_alignment():
    for icon in TIER1_TEST_ICONS:
        frame = console.frame(f"Test {icon}", width=20)
        assert_no_overflow(frame)
        assert_border_intact(frame)
```

### Visual Regression Testing

- **Snapshot tests:** All Tier 1 icons with various frame styles
- **Width assertions:** Verify calculated width matches rendered width
- **Border integrity:** Ensure frames don't break with any icon

---

## Rationale

### Why Not Support Everything in v0.1?

1. **Complexity vs Value:** Tier 1 covers 95% of real-world use cases
2. **Terminal fragmentation:** ZWJ support is inconsistent across terminals in 2025
3. **Library dependencies:** Full grapheme support requires heavier dependencies
4. **Testing burden:** Tier 2/3 require extensive cross-terminal testing
5. **User expectations:** Better to have reliable basics than buggy advanced features

### Why This Matters for StyledConsole

Unlike a text editor (which can reflow), StyledConsole renders **fixed-width frames**:

```
┌─────────────────┐
│ Status: ✅      │  ← 1 char width error breaks the border
└─────────────────┘
```

Precision is critical. Starting with well-understood Tier 1 ensures reliability.

---

## Future Considerations

### v0.4+: Per-Terminal Profiles

- Detect terminal capabilities at runtime
- Load emoji support profiles (iTerm2 vs Windows Terminal vs xterm)
- Auto-adjust rendering based on detected support

### v0.5+: User Configuration

```python
console = Console(emoji_tier="tier1")  # Force basic icons only
console = Console(emoji_tier="auto")   # Detect terminal capabilities
console = Console(emoji_tier="tier3")  # Enable all emojis (may break)
```

---

## References

- **Unicode Standard:** https://unicode.org/emoji/
- **wcwidth library:** https://github.com/jquast/wcwidth
- **grapheme library:** https://github.com/alvinlindstam/grapheme
- **Terminal emoji support matrix:** https://github.com/alacritty/alacritty/issues/50

---

**Status:** ✅ Strategy defined and documented
**Next Steps:** Implement Tier 1 in T-002 (Text Width Utilities)
