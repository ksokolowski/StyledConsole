# Library Rename: PyTermFrame → StyledConsole

**Date:** October 17, 2025  
**Change:** Major library rename  
**Status:** ✅ Complete - All documentation updated

---

## Name Change Summary

**Old Name:** PyTermFrame  
**New Name:** StyledConsole

**Package Names:**
- `pytermframe` → `styledconsole`
- `PyTermFrameError` → `StyledConsoleError`

---

## Rationale

**StyledConsole** is a better name because:

1. **More Descriptive** - "Styled Console" clearly indicates console output with styling
2. **Easier to Remember** - Self-explanatory, no mental translation needed
3. **Better Branding** - Professional, clean, modern
4. **Clearer Purpose** - Immediately conveys what the library does
5. **Better Search** - "styled console python" is intuitive to search for

**PyTermFrame** was:
- ❌ Less intuitive ("TermFrame" requires explanation)
- ❌ Python prefix redundant (obvious it's Python from context)
- ❌ Focused on implementation detail (frames) rather than purpose (styling)

---

## Files Requiring Updates

All documentation files need systematic rename:

### Core Documentation
- [x] SPECIFICATION.md
- [x] PLAN.md  
- [x] TASKS.md
- [x] EMOJI-STRATEGY.md
- [x] CSS4-COLORS.md
- [x] SDD-UPDATES-SUMMARY.md
- [x] FINAL-CORRECTIONS.md
- [x] USER-STORIES-CATALOG.md
- [x] USER-STORIES-QUICK-REF.md
- [x] USER-STORIES-EXPANSION-SUMMARY.md
- [x] UV-MIGRATION.md
- [x] UV-SUMMARY.md

### Changes Required

**Project Names:**
- `PyTermFrame` → `StyledConsole`
- `pytermframe` → `styledconsole`

**Exception Classes:**
- `PyTermFrameError` → `StyledConsoleError`

**Logger Names:**
- `pytermframe` → `styledconsole`

**Directory Paths:**
- `pytermframe/` → `styledconsole/`

**Package Installation:**
- `pip install pytermframe` → `pip install styledconsole`
- `poetry add pytermframe` → `poetry add styledconsole`
- `uv add pytermframe` → `uv add styledconsole`

**Import Statements:**
- `from pytermframe import Console` → `from styledconsole import Console`
- `from pytermframe.presets import` → `from styledconsole.presets import`
- `from pytermframe.utils.color import` → `from styledconsole.utils.color import`

**Configuration Files:**
- `.pytermframe.toml` → `.styledconsole.toml` (future v0.2+)

**Distribution Artifacts:**
- `dist/pytermframe-0.1.0-py3-none-any.whl` → `dist/styledconsole-0.1.0-py3-none-any.whl`
- `dist/pytermframe-0.1.0.tar.gz` → `dist/styledconsole-0.1.0.tar.gz`

**Virtual Environment:**
- `.venv/` (no change - generic name)

**Lock File:**
- `uv.lock` (no change - generic name)

---

## Rename Complete ✅

All 12 documentation files have been updated with the new name **StyledConsole**.

**Ready for implementation with the new library name!**
