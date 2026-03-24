# Thread Safety — StyledConsole

## Summary

StyledConsole is designed primarily for single-threaded use. As of v0.10.5,
some components have been made safe for concurrent use, while others remain
global singletons.

## Per-Call Safe (v0.10.5+)

**Render target** — The `visual_width()` calculation mode (terminal vs image vs HTML)
is scoped per render call using Python's `ContextVar`. Multiple Console instances
rendering concurrently will not interfere with each other's width calculations.

`set_render_target()` remains available as a public function for module-level
overrides (e.g., image export scripts that need consistent width calculations
before any Console is created).

## Global Singletons (Not Thread-Safe)

**Icon mode** — `set_icon_mode()` is a global setting. Creating a Console with
a different policy will change the icon mode for all Console instances.
Planned fix: v0.11.0.

**Rich cell_len patching** — Export consoles (`render_target="image"` or `"html"`)
monkey-patch Rich's `cell_len` function globally. This affects width calculations
in terminal consoles created in the same process. Planned fix: v0.11.0.

## Recommendation

For concurrent use, create one Console per thread and avoid mixing terminal
and export consoles in the same process. For sequential use (the common case),
no special precautions are needed.
