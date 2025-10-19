# Emoji Guidelines for StyledConsole

## Current Status: v0.1.0

StyledConsole supports emoji rendering with proper width calculation for **simple, single-codepoint emojis**.

## ✅ Supported Emojis (Single Codepoint)

These emojis work perfectly and are recommended:

### Status & Symbols
- ✅ ❌ ⚠️ ℹ️ ⏭️ ⏸️ ⏹️
- 🔴 🟡 🟢 🔵 🟣 🟠
- ⭐ ✨ 💫 🌟

**Note**: Some symbols like ⚠️ and ℹ️ include a variation selector (U+FE0F) but are fully supported by the library's `visual_width()` function. However, **avoid using variation selector emojis in custom character-by-character processing** (like diagonal gradients) as they require special handling.

### Objects & Activities
- 📊 📈 📉 📦 📁 📂 📄 📝
- 🎯 🎨 🎉 🎊 🎁
- 🚀 💻 🖥️ ⌨️ 🖱️ 💾 💿
- 🧪 🔬 🔧 🔨 ⚙️

### People (Simple)
- 👥 👤
- 👍 👎 👋 🙌

### Nature & Food
- 🌈 ☀️ 🌙 ⭐ 💧
- 🍕 🍔 🍟 ☕ 🍺

## ❌ NOT Supported (ZWJ Sequences)

**Zero-Width Joiner (ZWJ) emojis are NOT supported** in the current version due to width calculation complexity:

### Avoid These:
- 👨‍💻 👩‍💻 🧑‍💻 (person + laptop)
- 👨‍🔬 👩‍🔬 (person + science)
- 👨‍🎨 👩‍🎨 (person + art)
- 👨‍🚀 👩‍🚀 (person + rocket)
- 👨‍⚕️ 👩‍⚕️ (person + medical)
- 🏳️‍🌈 (rainbow flag)
- Any emoji with skin tone modifiers + profession
- Family emojis (👨‍👩‍👧‍👦)

### Why Not Supported?

ZWJ emojis are composed of multiple codepoints joined together:
```
👨‍💻 = 👨 (man) + ZWJ + 💻 (laptop) = 3 codepoints but displays as 1 glyph
```

This causes:
1. **Width miscalculation**: Library counts it as 3-4 characters wide but terminal renders it as 2
2. **Border misalignment**: Frame borders don't line up correctly
3. **Content overflow**: Text appears to spill outside frames
4. **Padding issues**: Alignment calculations are off

## ⚠️ Variation Selector Issues

**IMPORTANT:** Some emojis have **variation selectors** (U+FE0F) that add an extra codepoint without visual width. These work with `visual_width()` but can cause issues in character-by-character processing (like diagonal gradients).

### Problematic Emojis (Variation Selectors)

**AVOID these in gradient effects or character-level processing:**

| Emoji | Codepoints | Issue | Safe Alternative |
|-------|-----------|-------|-----------------|
| 🖥️ | U+1F5A5 + U+FE0F | 2 codepoints | � (U+1F5A5 only) |
| ↘️ | U+2198 + U+FE0F | 2 codepoints | ↘ (U+2198 only) |
| ➡️ | U+27A1 + U+FE0F | 2 codepoints | → or ➡ (base) |
| ⬆️ | U+2B06 + U+FE0F | 2 codepoints | ↑ or ⬆ (base) |
| ⬇️ | U+2B07 + U+FE0F | 2 codepoints | ↓ or ⬇ (base) |
| ⬅️ | U+2B05 + U+FE0F | 2 codepoints | ← or ⬅ (base) |

**Safe to use everywhere:**

| Emoji | Codepoint | Visual Width | Use Case |
|-------|----------|--------------|----------|
| ✨ | U+2728 | 2 | Sparkles, highlights |
| 🌈 | U+1F308 | 2 | Rainbow, colors |
| 🎨 | U+1F3A8 | 2 | Art, creativity |
| 🚀 | U+1F680 | 2 | Speed, launch |
| 💻 | U+1F4BB | 2 | Computer, code |
| 📊 | U+1F4CA | 2 | Charts, data |
| 🔥 | U+1F525 | 2 | Fire, trending |
| ⭐ | U+2B50 | 2 | Star, favorite |

**How to check:**
```python
# Check if emoji has variation selector
emoji = "🖥️"
codepoints = [hex(ord(c)) for c in emoji]
print(f"{emoji} - codepoints: {codepoints}")
# Output: 🖥️ - codepoints: ['0x1f5a5', '0xfe0f']  ❌ Has variation selector!

emoji = "✨"
codepoints = [hex(ord(c)) for c in emoji]
print(f"{emoji} - codepoints: {codepoints}")
# Output: ✨ - codepoints: ['0x2728']  ✅ Safe!
```

## 📋 Comprehensive Safe Emoji List

### ✅ SAFE - Tested & Recommended

These emojis are **single codepoint** (or safe multi-codepoint) and work perfectly with all StyledConsole features including gradient effects:

#### Status & Indicators (Width: 1-2)
```
✅ ❌ ⭕ 🔴 🟡 🟢 🔵 🟣 🟠 ⚫ ⚪
✓ ✗ ○ ● ◆ ◇ ■ □ ▪ ▫
⭐ ✨ 💫 🌟 ⚡ 🔥 💥 💢
```

#### Arrows & Direction (Width: 1-2)
```
← → ↑ ↓ ↔ ↕ ↖ ↗ ↘ ↙
⬆ ⬇ ⬅ ➡ ⬈ ⬉ ⬊ ⬋
⇧ ⇨ ⇩ ⇦ ⇄ ⇅
```

#### Tech & Objects (Width: 2)
```
💻 🖥 ⌨ 🖱 🖨 💾 💿 📀
📱 📞 ☎ 📟 📠 📡
🔧 🔨 ⚙ 🛠 ⚡ 🔌 🔋
🧪 🔬 🔭 📡 🎛 🎚
```

#### Nature & Weather (Width: 2)
```
🌈 ☀ 🌙 ⭐ 💧 ☁ ⛅ 🌤
🌱 🌿 🍀 🌸 🌺 🌻 🌼
🔥 💨 💦 ⚡ ❄ 🌊
```

#### Charts & Data (Width: 2)
```
📊 📈 📉 📋 📌 📍 📎
📦 📁 📂 📄 📃 📝 📜
```

#### Symbols & Misc (Width: 1-2)
```
🎯 🎨 🎭 🎪 🎉 🎊 🎁
🏆 🥇 🥈 🥉 🏅 🎖
💎 💰 💵 💴 💶 💷
♠ ♣ ♥ ♦ ♟ ♞ ♝ ♜
```

#### Food & Drink (Width: 2)
```
🍕 🍔 🍟 🌭 🍿 🧂
☕ 🍵 🥤 🍺 🍻 🥂
🍰 🎂 🧁 🍪 🍩 🍫
```

#### People (Simple) (Width: 2)
```
👥 👤 👣
👍 👎 👋 🙌 👏 🤝
💪 🧠 👁 👀 👂 👃
```

### ❌ UNSAFE - Avoid These

**Variation Selector Emojis** (Use base version instead):
```
❌ AVOID: 🖥️ ↘️ ➡️ ⬆️ ⬇️ ⬅️ ☝️ ✌️ ☺️
✅ USE: 🖥 ↘ → ↑ ↓ ← (base versions)
```

**ZWJ Sequences** (Multiple codepoints joined):
```
❌ AVOID: 👨‍💻 👩‍💻 🧑‍💻 👨‍🔬 👩‍🔬 👨‍🎨 👩‍🎨
👨‍🚀 👩‍🚀 👨‍⚕️ 👩‍⚕️ 🏳️‍🌈 👨‍👩‍👧‍👦
```

**Flag Emojis** (Regional indicators):
```
❌ AVOID: 🇺🇸 🇬🇧 🇨🇦 🇯🇵 (any country flags)
```

**Skin Tone Modifiers**:
```
❌ AVOID: 👋🏻 👋🏼 👋🏽 👋🏾 👋🏿
✅ USE: 👋 (default without modifier)
```

## �🔄 Workarounds

Instead of ZWJ emojis, use combinations:

| ❌ Don't Use | ✅ Use Instead | Description |
|-------------|---------------|-------------|
| 👨‍💻 | 💻 or 👥💻 (separate) | Developer |
| 👨‍🔬 | 🧪 or 🔬 | Scientist |
| 👨‍🎨 | 🎨 | Artist |
| 🏳️‍🌈 | 🌈 | Rainbow |
| 🖥️ | 🖥 | Desktop computer |
| ➡️ | → or ➡ | Right arrow |

## Examples

### ✅ Good Example
```python
console.frame(
    ["Status: Online", "Users: 342"],
    title="💻 Server",  # Single emoji
    border="rounded"
)
```

### ❌ Bad Example
```python
console.frame(
    ["Status: Online", "Users: 342"],
    title="👨‍💻 Server",  # ZWJ emoji - causes misalignment!
    border="rounded"
)
```

## Testing Emojis

To test if an emoji is safe:

```python
import unicodedata

emoji = "💻"  # Test your emoji
codepoints = len(emoji)
print(f"Codepoints: {codepoints}")

# Safe if codepoints == 1 or 2 (for flag emojis)
# Unsafe if codepoints > 2 (likely ZWJ)
```

## Future Enhancements

In future versions, we may add:

- [ ] Full ZWJ emoji support with proper width calculation
- [ ] Emoji skin tone modifier support
- [ ] Flag emoji support (regional indicators)
- [ ] Emoji variation selectors handling
- [ ] `validate_emoji()` utility function (tracked in T-010a)
- [ ] Comprehensive safe emoji catalog (tracked in T-010a)

For now, **stick to simple single-codepoint emojis** from the safe list above for best results!

## Reference

See examples:

- `examples/basic/02_emoji_support.py` - Simple emoji examples
- `examples/showcase/advanced_dashboard.py` - Complex dashboard with emojis
- `examples/showcase/digital_poetry.py` - Artistic emoji usage
- `examples/showcase/gradient_effects.py` - Gradient effects with safe emojis

See documentation:

- `doc/VARIATION_SELECTOR_ISSUE.md` - Deep dive into variation selector problems
- `doc/GRADIENT_IMPLEMENTATION.md` - Gradient effects and emoji handling
- `doc/TASKS.md` (T-010a) - Future safe emoji list & validation

---

**Last Updated**: October 19, 2025 (v0.1.0)
- Added comprehensive safe emoji list (100+ tested emojis)
- Added variation selector warnings and alternatives
- Added quick reference for character-by-character processing
- Added workarounds for problematic emojis from gradient implementation
