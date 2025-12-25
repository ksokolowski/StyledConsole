# Feasibility Study: Implementation of Context Object Pattern

**Date:** 2025-12-25
**Target Component:** `styledconsole.core.rendering_engine` & `styledconsole.console`
**Status:** DRAFT

______________________________________________________________________

## 1. Executive Summary

This document analyzes the feasibility of implementing the **Context Object Pattern** within the `styledconsole` library. The primary goal is to resolve the "parameter explosion" issue observed in the core rendering methods, where functions accept 13+ optional arguments for styling.

The analysis confirms that the codebase is a **prime candidate** for this pattern. Implementing a `StyleContext` object will significantly improve maintainability, extensibility, and code readability without sacrificing performance.

## 2. Problem Statement

Current inspection of `src/styledconsole/console.py` and `src/styledconsole/core/rendering_engine.py` reveals a "Long Parameter List" code smell.

**Example Signature (`RenderingEngine.render_frame_to_string`):**

```python
def render_frame_to_string(
    self,
    content: str | list[str],
    *,
    title: str | None = None,
    border: str = "rounded",
    width: int | None = None,
    padding: int = 1,
    align: AlignType = "left",
    content_color: str | None = None,
    border_color: str | None = None,
    title_color: str | None = None,
    start_color: str | None = None,
    end_color: str | None = None,
    border_gradient_start: str | None = None,
    border_gradient_end: str | None = None,
    border_gradient_direction: str = "vertical",
) -> str:
```

**Issues:**

1. **Fragility:** Adding a new style property (e.g., `shadow`, `opacity`) requires updating signatures across the Facade (`Console`), the Engine (`RenderingEngine`), and internal helpers (`_render_custom_frame`).
1. **Readability:** Function calls become verbose and difficult to visually parse.
1. **Validation:** Validation logic (e.g., checking if `start_color` is present when `end_color` is used) is scattered inside the methods or duplicated.

## 3. Proposed Solution: Context Object Pattern

We propose introducing a **Context Object** (likely named `StyleContext` or `RenderOptions`) to encapsulate all styling configuration.

### 3.1. Concept

The `StyleContext` would be a strongly-typed immutable Data Class that holds the state required for rendering a single frame or element.

```python
@dataclass(frozen=True)
class StyleContext:
    # Dimensions & Layout
    width: int | None = None
    padding: int = 1
    align: AlignType = "left"

    # Border Configuration
    border_style: str = "rounded"
    border_color: str | None = None
    border_gradient: Gradient | None = None  # Encapsulates start/end/direction

    # Content Styling
    content_color: str | None = None
    content_gradient: Gradient | None = None

    # Meta
    title: str | None = None
    title_color: str | None = None
```

### 3.2. Architecture Impact

1. **`Console` (Facade):** Continues to accept `kwargs` for backward compatibility and ease of use, but immediately constructs valid `StyleContext` objects.
1. **`RenderingEngine`:** Refactored to accept `StyleContext` objects.
   - `print_frame(content, context: StyleContext)`
1. **`RenderPolicy`:** remains as the *global* environment context, while `StyleContext` becomes the *local* operation context.

## 4. Pros & Cons Analysis

### Pros

- **Cleaner Signatures:** Reduces method arguments from ~15 down to 2-3 (Content, Context, Policy).
- **Centralized Validation:** The Context object's `__post_init__` can enforce rules (e.g., "gradient requires both start and end colors").
- **Reusability:** Users can define a `StyleContext` once and reuse it across multiple calls (Pre-defined Styles).
- **Extensibility:** Adding new features (like shadows or margins) only involves updating the Context object and the final renderer, skipping the intermediate layers.

### Cons

- **Refactoring Effort:** Requires modifying core files (`console.py`, `rendering_engine.py`) and updating many internal calls.
- **API Changes:** While the public Facade can stay compatible, custom extensions using `RenderingEngine` directly would need updates.

## 5. Potential Implementation Plan

### Phase 1: Core Implementation

1. Create `src/styledconsole/core/context.py`.
1. Define `StyleContext` and helper dataclasses (e.g., `Gradient`).
1. Implement builder/factory methods for easy creation.

### Phase 2: Internal Refactoring

1. Refactor `RenderingEngine` to accept `StyleContext`.
1. Create an overload/adapter to support the old signature temporarily (if needed) or just do a hard switch for internal methods.

### Phase 3: Facade Integration

1. Update `Console.frame()` to instantiate `StyleContext`.
1. Update `Console.render_frame()` and `Console.render_frame_group()`.

### Phase 4: Testing & Verification

1. Add unit tests for `StyleContext` validation logic.
1. Verify that existing tests pass (regression testing).

## 6. Recommendation

**PROCEED.** The project has reached a complexity level where the benefits of the Context Object Pattern significantly outweigh the implementation costs. It aligns with the "Refactoring for Extensibility" goal found in the project's roadmap / best practices.
