# Console API Improvement Ideas

**Date:** November 12, 2025
**Context:** Identified during gallery examples development

## 1. Nested Frames / Frame Grouping

### Current Limitation

Users cannot easily create true nested frames (frames within frames) using Console API alone. The workaround requires:

- Using Rich Panel directly
- Accessing `console._rich_console` (internal API)
- Complex string capturing logic

### Use Case

System monitoring dashboards, multi-level information hierarchy, visual grouping of related frames.

### Example from borders_showcase.py

```python
# Current: Multiple independent frames (logical grouping, not visual nesting)
console.frame(cpu_content, title="CPU Status", border="rounded", border_color="green", width=35)
console.frame(memory_content, title="Memory Status", border="rounded", border_color="yellow", width=35)
console.frame(network_content, title="Network Status", border="rounded", border_color="cyan", width=35)
```

### Proposed API

```python
# Option A: Context manager
with console.group(title="System Dashboard", border="heavy", border_color="blue"):
    console.frame(cpu_content, title="CPU Status", border="rounded", border_color="green")
    console.frame(memory_content, title="Memory Status", border="rounded", border_color="yellow")
    console.frame(network_content, title="Network Status", border="rounded", border_color="cyan")

# Option B: Explicit nesting
dashboard = console.create_group(title="System Dashboard", border="heavy")
dashboard.frame(cpu_content, title="CPU Status", border="rounded")
dashboard.frame(memory_content, title="Memory Status", border="rounded")
console.print(dashboard)

# Option C: Container parameter
console.frame(
    [
        ("CPU Status", cpu_content, {"border": "rounded", "border_color": "green"}),
        ("Memory Status", memory_content, {"border": "rounded", "border_color": "yellow"}),
        ("Network Status", network_content, {"border": "rounded", "border_color": "cyan"}),
    ],
    container_title="System Dashboard",
    container_border="heavy",
    container_color="blue"
)
```

### Implementation Notes

- Should leverage Rich's Panel and Group internally
- Maintain emoji-safe width calculations
- Support gradient borders on both container and nested frames
- Consider padding/spacing between nested elements

### Priority

Medium - Nice-to-have for advanced use cases, not blocking basic functionality

______________________________________________________________________

## 2. Color & Gradient API Consistency

### Current Situation

Introduce an explicit concept of a **preprocessed content block** that can be reused when constructing frames or other layouts.
Design this helper to be **Rich-native under the hood**, so StyledConsole does not reimplement styling or wrapping logic:

- `Console.banner(...)` (in `console.py`)

  - Solid color via `color="cyan"`.
  - Gradient via `start_color` / `end_color` parameters (documented in v0.3.0).
  - Legacy examples still use `style="gradient"` and `colors=["red", "blue"]`, and `style="rainbow"`.

- `Console.frame(...)`

  - Solid border/content color via `border_color` / `content_color` (type `ColorType` = `str | tuple[int, int, int]`).
  - Some examples overload `border_color` with tuples of **color names** to imply gradients, e.g.:
    - `border_color=("red", "blue")` (two-stop gradient intent).
    - `border_color=("coral", "tomato", "orangered", "darkorange", "orange")` (multi-stop gradient intent).

- Gradient effects in `styledconsole/effects.py`:

  - `gradient_frame(...)` and `diagonal_gradient_frame(...)` use `start_color` / `end_color`.
  - `rainbow_frame(...)` implements a rainbow gradient using an internal palette.

### Problems

- **Inconsistent naming and semantics**

  - Banners already use `start_color` / `end_color`, but some examples still rely on `style` + `colors`.
  - Frames overload `border_color` to mean both a solid color and an implicit gradient spec when a tuple of names is passed.

- **Type mismatch between docs and examples**

  - `ColorType` is documented as `str | tuple[int, int, int]` (name or RGB), but examples use `tuple[str, ...]` for gradients.
  - Users cannot reliably infer from type hints how to express gradients.

- **Unclear canonical way to create gradients**

  - There are dedicated helpers (`gradient_frame`, `diagonal_gradient_frame`, `rainbow_frame`) using `start_color` / `end_color`.
  - At the same time, examples show gradients by overloading `border_color` with tuples of names.
  - For banners, legacy `style="gradient"` / `style="rainbow"` still appear in older code.

1. **Standardize gradient parameter naming**

   - For any API that supports a 2-stop gradient, use:

     - `start_color: ColorType | None`
     - `end_color: ColorType | None`

   - Behavior:

     - If both are `None`: render as solid color via `color` / `border_color`.
     - If `start_color` is set and `end_color` is `None`: treat as error or fall back to solid; decision to be documented.
     - If both are set: render a gradient between `start_color` and `end_color`.

   - This already matches:

     - `Console.banner(...)` (current v0.3.0 API and docstring).
     - `gradient_frame(...)` and `diagonal_gradient_frame(...)` in `effects.py`.

1. **Keep "simple vs advanced" separation clear**

   - Core API (`Console`):
     - Solid colors: `color`, `border_color`, `content_color` using `ColorType`.
     - Optional 2-stop gradients where it makes sense (`start_color`, `end_color`), with simple rules.
   - Effects API (`styledconsole.effects`):
     - Advanced or opinionated gradients (diagonal, rainbow, multi-stop).
     - Example usage should prefer `gradient_frame` / `diagonal_gradient_frame` / `rainbow_frame` for complex cases.

1. **Deprecate overloading `border_color` with tuples of names in examples**

   - Replace example usages like:

     ```python
     console.frame(
             "...",
             border="thick",
             border_color=("coral", "tomato", "orangered", "darkorange", "orange"),
     )
     ```

   - With one of:

     ```python
     # Option A: Use gradient helpers
     gradient_frame(
             "...",
             start_color="coral",
             end_color="orange",
             border="thick",
             align="center",
             width=70,
     )

     # Option B: Once supported, use explicit frame gradient parameters
     console.frame(
             "...",
             border="thick",
             start_color="coral",
             end_color="orange",
             width=70,
     )
     ```

   - This removes the need to special-case `tuple[str, ...]` in `border_color` and keeps `ColorType` honest.

1. **Explicitly de-emphasize `style`/`colors` on banners**

   - In v0.3.x examples and docs, avoid:

     ```python
     console.banner("Title", font="banner", style="gradient", colors=["red", "blue"])
     console.banner("RAINBOW", font="banner", style="rainbow")
     ```

   - Prefer the new API:

     ```python
     # Solid banner
     console.banner("SUCCESS", font="slant", color="green")

     # Gradient banner
     console.banner("DEPLOY", font="banner", start_color="cyan", end_color="purple")
     ```

   - If backward-compat `style`/`colors` handling remains in code, treat it as legacy and clearly mark it as such in docstrings.

### Potential v0.3.x Implementation Steps

- Audit all examples (especially `examples/gallery/colors_showcase.py` and `examples/gallery/gradients_showcase.py`) to:

  - Replace `style="gradient"`/`style="rainbow"` with `start_color` / `end_color` where appropriate.
  - Replace tuple-of-names `border_color` usage with gradient helpers.

- Optionally extend `Console.frame(...)` signature to accept `start_color` / `end_color` for border gradients, implemented via `RenderingEngine` and `box_mapping`.

### v1.0+ Cleanup Ideas

- Consider formally deprecating `style`/`colors` on `banner()` in the public API and removing them in v1.0.
- Consider narrowing `ColorType` back to `str | tuple[int, int, int]` and documenting that gradients are always expressed via `start_color` / `end_color` (or dedicated helpers), never via overloading `border_color`.

### Unified Color & Effect Feature Matrix (Draft)

To keep the API coherent, we can treat "coloring" as applying a **color scheme** to a specific visual region (content, border, title, banner text) with a small set of modes.

#### Visual elements vs. color modes

| Element          | Region         | Solid color parameters | Gradient parameters                  | Rainbow / special        | Notes                                                  |
| ---------------- | -------------- | ---------------------- | ------------------------------------ | ------------------------ | ------------------------------------------------------ |
| `Console.text`   | text           | `color`                | –                                    | –                        | Focused on simple styling; no gradients.               |
| `Console.frame`  | content        | `content_color`        | `start_color` / `end_color` (future) | via `effects.gradient_*` | Gradients via helpers; core may later accept them.     |
| `Console.frame`  | border         | `border_color`         | via helpers only                     | via `effects.*`          | Avoid overloading `border_color` with tuples of names. |
| `Console.frame`  | title          | `title_color`          | –                                    | –                        | Title gradients considered out of scope for now.       |
| `Console.banner` | banner text    | `color`                | `start_color` / `end_color`          | via helper (future)      | Rainbow banner as helper built on same machinery.      |
| Effects helpers  | content/border | `color` (fallback)     | `start_color` / `end_color`, palette | built-in palette         | Opinionated, advanced patterns over the same types.    |

Unifying rules behind this matrix:

- **Solid colors** always use: `color`, `content_color`, `border_color`, `title_color` depending on region.
- **2-stop gradients** always use `start_color` / `end_color` where supported, never `border_color=("red", "blue")`.
- **Rainbow** is treated as a special gradient case implemented in `effects` using a predefined palette, not a separate ad‑hoc parameter type.
- **Text-only renderables** (`Console.text`) intentionally stay simple: solid color + style flags, no gradients.

This matrix should guide future signature changes: new parameters should fit into these categories instead of inventing one-off names.

______________________________________________________________________

### Unified Parameter Matrix (Draft)

For design-time work, it is also helpful to see **which knobs are intended to apply to which top-level APIs**. This matrix is not user-facing documentation but a planning tool to keep signatures coherent.

| Parameter / Knob   | Console.text | Console.frame  | Console.banner | gradient_frame | diagonal_gradient_frame | rainbow_frame  | Notes                                                |
| ------------------ | :----------: | :------------: | :------------: | :------------: | :---------------------: | :------------: | ---------------------------------------------------- |
| `text` / `content` | ✅ (`text`)  | ✅ (`content`) |  ✅ (`text`)   | ✅ (`content`) |     ✅ (`content`)      | ✅ (`content`) | Naming differs (`text` vs `content`), same role.     |
| `title`            |      –       |       ✅       |   – / future   |       ✅       |           ✅            |       ✅       | Only where frames/titles exist.                      |
| `border`           |      –       |       ✅       |    future?     |       ✅       |           ✅            |       ✅       | Uses named border styles.                            |
| `width`            |      –       |       ✅       |       ✅       |       ✅       |           ✅            |       ✅       | Optional; interacts with `align`.                    |
| `padding`          |      –       |       ✅       |       ✅       |       ✅       |           ✅            |       ✅       | Inner padding for framed content.                    |
| `align`            |      –       |       ✅       |       ✅       |       ✅       |           ✅            |       ✅       | Alignment of content inside the element.             |
| `color`            |      ✅      |       –        |   ✅ (text)    |    fallback    |        fallback         |    fallback    | Solid text color when there is a single region.      |
| `content_color`    |      –       |       ✅       |       –        |       ✅       |           ✅            |       ✅       | Solid color for frame content.                       |
| `border_color`     |      –       |       ✅       |    future?     |       ✅       |           ✅            |       ✅       | Solid color for borders. No tuple-of-names overload. |
| `title_color`      |      –       |       ✅       |       –        |       ✅       |           ✅            |       ✅       | Solid color for title text.                          |
| `start_color`      |      –       |     future     |       ✅       |       ✅       |           ✅            |       –        | 2-stop gradient start.                               |
| `end_color`        |      –       |     future     |       ✅       |       ✅       |           ✅            |       –        | 2-stop gradient end.                                 |
| `bold`             |      ✅      |  via content   |    via text    |  via content   |       via content       |  via content   | Applied through Rich `Text` styling.                 |
| `italic`           |      ✅      |  via content   |    via text    |  via content   |       via content       |  via content   | Same as above.                                       |
| `underline`        |      ✅      |  via content   |    via text    |  via content   |       via content       |  via content   | Same as above.                                       |
| `dim`              |      ✅      |  via content   |    via text    |  via content   |       via content       |  via content   | Same as above.                                       |

Legend:

- `✅` – parameter is part of the intended/actual signature.
- `future` – planned API improvement (see sections above).
- `fallback` / `via content` – used indirectly by building a styled Rich `Text` for the content that is then framed or processed by effects.

This matrix should remain small and high-level; it is meant to prevent ad‑hoc parameters from creeping into new methods and to validate that new features (e.g. banner borders, frame gradients) reuse existing knobs where possible.

______________________________________________________________________

## 3. Alignment & Layout Semantics

### Current Situation

- `Console.frame(...)` accepts `align: AlignType` to control how multi-line content is aligned **inside** the frame (left/center/right), with width determined by `width` (if provided) or content.
- `Console.banner(...)` also accepts `align: AlignType`, but in practice alignment interacts with both the generated ASCII art and the outer frame/padding.
- `Console.text(...)` deliberately does **not** take an `align` argument; alignment is expected to be handled by the surrounding layout (frames, terminal, or Rich layout constructs).

### Problems

- From a user perspective it's not obvious **where** alignment should be applied:
  - Should `align` mean "align the content within the frame width" or "align the whole frame within the terminal width"?
  - Banners have two layers (ASCII art + optional frame), and current docs/examples don't clearly state which layer `align` applies to.
- Examples sometimes rely on implicit terminal alignment (e.g., trusting the terminal to be wide enough) without documenting behavior when the terminal is narrow or when `width` is not set.

### Proposed Direction

- Clearly document that:
  - `Console.frame(..., align=...)` controls **content alignment inside the frame box**.
  - `Console.banner(..., align=...)` controls **ASCII-art text alignment inside the banner area**, with any surrounding frame following the same alignment.
  - `Console.text(...)` intentionally has no `align` parameter; alignment should be achieved by wrapping text in `frame()` or using higher-level layout constructs.
- Prefer examples that specify `width` when alignment matters, so behavior is deterministic across terminals.
- For v1.0, consider adding a higher-level layout helper (e.g. `console.columns(...)` or `console.grid(...)`) if repeated alignment patterns emerge; document as a potential follow-up to the nested frame/grouping API.

### Potential v0.3.x Steps

- Update gallery examples to:
  - Use `align="center"` with explicit `width` for banners and key frames that are meant to be centered.
  - Avoid relying on terminal width for "centered" output in examples.
- Add brief notes to docstrings for `frame` and `banner` clarifying what `align` controls.

______________________________________________________________________

## 4. Banner/Frame/Text Naming Consistency

### Current Situation

- `Console.frame(...)` uses `content_color`, `border_color`, and `title_color` for solid colors, plus optional `start_color` / `end_color` for gradients (by design).
- `Console.banner(...)` uses `color` for solid text color and `start_color` / `end_color` for gradients.
- `Console.text(...)` uses `color` for the main text color along with style flags (`bold`, `italic`, `underline`, `dim`).

### Problems

- The difference between `color` vs `content_color` is not always obvious from examples alone.
- Users may expect `banner(..., border_color=...)` or `text(..., border_color=...)` even though banners and plain text do not expose borders directly.
- Some legacy examples mix old parameters (`style`, `colors`) with newer ones, making it harder to see the intended naming scheme.

### Proposed Direction

- Establish and document the following naming rules:
  - `color`: the primary text color for content that is **not** inside a frame, or for banner ASCII art.
  - `content_color`: the color of text **inside a frame**.
  - `border_color`: the color of the frame border.
  - `title_color`: the color of the frame title.
  - `start_color` / `end_color`: exclusively for 2-stop gradients (as described in section 2).
- Keep `Console.text(...)` focused on text styling (`color` + style flags) and avoid adding border-related options there.
- Keep `Console.banner(...)` scoped to text and optional surrounding frame; if border options are extended in the future, reuse `border_color` and `title_color` naming from `frame`.

#### Text Style Knobs (Bold/Italic/Underline/Dim)

- `Console.text(...)` is the canonical place where text style knobs are exposed today: `bold`, `italic`, `underline`, `dim`, plus `color`.
- These knobs are intended to be **reused for other text regions** in the future (frame content, frame titles, banner text) by introducing region-aware style parameters such as:
  - `content_style` or `content_bold` / `content_italic` / ...
  - `title_style` or `title_bold` / `title_italic` / ...
- Internally, all of these should map to Rich `Text` styling in a consistent way, so that titles, content, and banner text can share the same styling capabilities without duplicating logic.

### Potential v0.3.x Steps

- Audit docstrings and examples to:
  - Use `content_color`/`border_color`/`title_color` consistently when frames are involved.
  - Use plain `color` only for non-framed content and banner text.
- Add a short "Color naming convention" section to the user-facing docs that summarizes these rules in one place.

______________________________________________________________________

## 5. Emoji Usage & Examples

### Current Situation

- The core library already provides emoji-safe utilities (`visual_width`, `pad_to_width`, `truncate_to_width`) and a curated `EMOJI` mapping.
- Some examples (especially older gallery files) still use raw emoji literals instead of `EMOJI[...]` constants.
- Emoji categories (status, faces, objects, etc.) are not consistently represented across examples.

### Problems

- Using raw emoji literals in examples makes it harder to change or curate the emoji set in one place.
- It also hides the existence of the `EMOJI` mapping from users who read examples as their primary documentation.
- Some terminals have limited emoji support; examples do not currently make it obvious that emojis are optional and that the core rendering remains stable without them.

### Proposed Direction

- In examples, prefer `from styledconsole import EMOJI` and use named constants, e.g. `EMOJI["rocket"]`, `EMOJI["warning"]`.
- Ensure each emoji-heavy example has a clear theme (e.g. "status indicators", "weather", "transport"), so users can see how emojis map to semantics, not just decoration.
- Briefly mention in user docs that emojis are optional and that StyledConsole falls back gracefully in environments with limited emoji support.

### Potential v0.3.x Steps

- Refactor `emojis_showcase.py` and related gallery examples to:
  - Replace raw literals with `EMOJI[...]` usage.
  - Group emojis by category and label them in comments or section titles.
- Add a short note in the emoji guide linking examples to the formal emoji policy.

______________________________________________________________________

## 6. Error Handling & Validation Expectations

### Current Situation

- The current API performs basic validation (e.g. for border names, colors) but some behaviors are implicit:
  - Passing only `start_color` without `end_color` may silently behave like a solid color or partial gradient, depending on the path.
  - Unknown color names rely on `parse_color` error behavior, which may not be obvious from the top-level API.
  - Invalid border names or font names typically fall back to defaults, but this isn't prominently documented.

### Problems

- For library users, it's not always clear **when** they should expect a hard error vs. a graceful fallback.
- Inconsistent error behavior across `frame`, `banner`, `text`, and effects makes debugging harder.

### Proposed Direction

- Define and document a small set of error-handling principles:
  - Invalid configuration that the library can safely recover from (e.g. unknown color name) should log/debug-note internally and fall back to a sensible default.
  - Ambiguous gradient configuration (e.g. `start_color` provided without `end_color`) should either:
    - Be treated as solid color with a documented rule, **or**
    - Raise a clear `ValueError` with guidance.
  - Unknown border or font names should fall back to a documented default and, if feasible, emit a warning in debug mode.
- Apply these rules consistently across `Console.frame`, `Console.banner`, `Console.text`, and the gradient helpers in `effects.py`.

### Potential v0.3.x Steps

- Audit validation paths in `console.py`, `effects.py`, and `utils/color.py` to:
  - Make ambiguous cases explicit (choose fallback vs. error and document).
  - Ensure error messages are actionable (mention parameter names and expected types).
- Add a short "Error handling" section to user docs describing these principles with 1–2 concrete examples.

______________________________________________________________________

## 7. Large Text Blocks & Preprocessed Content

### Current Situation

- `Console.frame(...)` currently accepts `content` as a string (or list of strings) and relies on Rich + internal utilities (`wrap.py`, `text.py`) to handle wrapping and emoji-safe width calculations.
- For many real-world use cases (logs, long descriptions, multi-paragraph text), users want to:
  - Provide a large text block (potentially with emojis and ANSI styling).
  - Have it automatically wrapped and formatted to a sensible width.
  - Then render it inside a frame whose width is derived from the wrapped content, not guessed up front.
- While this is possible today by manually calling `wrap_text` and using `visual_width` helpers, the workflow is not obvious or streamlined from the top-level `Console` API.

### Use Cases

- Rendering multi-paragraph help text or documentation snippets with emojis and bullet lists.
- Displaying sections of logs or error reports in a frame with an automatically chosen width.
- Building dashboards where certain panels show longer descriptions, but the user doesn't want to hardcode widths.

### Proposed Direction

- Introduce an explicit concept of a **preprocessed content block** that can be reused when constructing frames or other layouts.

- Possible API shapes (illustrative):

  ```python
  # Option A: Helper on Console
  content = console.prepare_content(
      text=raw_text,
      max_width=80,  # optional hint; None = auto-detect reasonable width
      preserve_paragraphs=True,
  )

  console.frame(content, title="Details")

  # Option B: Standalone utility function
  from styledconsole.utils import prepare_content_block

  content = prepare_content_block(raw_text, max_width=80)
  console.frame(content, title="Details")
  ```

- Internally, such a helper would:

  - Use existing emoji-aware utilities (`split_graphemes`, `visual_width`, `wrap_text`) to produce a wrapped representation.
  - Optionally compute a suggested `width` (e.g., min(max line width + padding, some upper bound)).
  - Return a structure that `Console.frame` can accept directly (e.g., list of lines or a small data object) without re-wrapping.

### Architectural Fit

- This feature fits well within the existing layering:
  - **Utilities** (`utils/text.py`, `utils/wrap.py`) remain the place where low-level wrapping and width logic lives.
  - A new helper (either in `console.py` or `utils/terminal.py`) would orchestrate these utilities into a higher-level "prepared content" concept.
  - `RenderingEngine.print_frame(...)` continues to work with strings / lists of strings; it does not need to know *how* they were prepared.
- This keeps Rich as the rendering backend while giving users a more ergonomic way to handle large, emoji-rich text blocks.

### Potential v0.3.x Steps

- Design a small, focused API (method or function) for preparing content blocks, with:
  - Clear inputs (raw text, optional max width, flags for paragraph handling).
  - A return type that integrates cleanly with `Console.frame`.
- Add 1–2 gallery examples demonstrating:
  - Rendering a multi-paragraph help panel.
  - Showing a log excerpt in an auto-sized frame.
- Document how this helper relates to existing utilities, so advanced users can still drop down to the lower-level API when needed.

______________________________________________________________________

## Future Ideas

Add more improvement ideas here as they're identified during development.
