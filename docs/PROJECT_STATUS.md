# StyledConsole Project Status

**Version:** 0.9.0
**Status:** Released
**Last Updated:** December 3, 2025

______________________________________________________________________

## Quick Summary

| Metric        | Value       |
| ------------- | ----------- |
| Current       | v0.9.0      |
| Lines of Code | ~6,500      |
| Tests         | 797 passing |
| Coverage      | 85%+        |
| Examples      | 31          |

______________________________________________________________________

## Roadmap

### Released

| Version | Date     | Theme                         |
| ------- | -------- | ----------------------------- |
| v0.1.0  | Oct 2025 | Foundation                    |
| v0.3.0  | Nov 2025 | Rich-Native rendering         |
| v0.4.0  | Nov 2025 | Animated Gradients            |
| v0.5.0  | Nov 2025 | Documentation & Structure     |
| v0.6.0  | Nov 2025 | text.py Refactoring           |
| v0.7.0  | Nov 2025 | Frame Groups                  |
| v0.8.0  | Nov 2025 | Theme System & Gradients      |
| v0.9.0  | Dec 2025 | Icon Provider (Colored ASCII) |

### Planned

| Version | Target | Theme | Status |
| v0.10.0 | Q1 2026 | Test Automation Presets - Core | PLANNED |
| v0.11.0 | Q1 2026 | Test Automation Presets - Assertions | PLANNED |
| v0.12.0 | Q2 2026 | Test Automation Presets - Data & API | PLANNED |
| v0.13.0 | Q2 2026 | Test Automation Presets - CI/CD | PLANNED |
| v0.14.0 | Q2 2026 | Test Automation Presets - Robot Framework | PLANNED |
| v1.0.0 | Q3 2026 | API freeze & Production Hardening | PLANNED |

______________________________________________________________________

## v0.9.0: Icon Provider & Runtime Policy

**Released:** December 3, 2025
**Status:** RELEASED

### Feature 1: Icon Provider (Colored ASCII Fallback) ✅ IMPLEMENTED

**Problem:** Emojis don't render correctly in all terminals (CI/CD, SSH, Windows cmd).
However, ANSI colors typically work even when Unicode fails.

**Solution Implemented:**

- 224 emoji→ASCII mappings organized in 16 categories
- ANSI escape codes for colored ASCII (avoids Rich markup conflicts)
- Parentheses-style ASCII: `(OK)`, `(FAIL)`, `(WARN)` (not square brackets)
- Three rendering modes: `auto`, `emoji`, `ascii`
- Module-level singleton `icons` for easy access

**Files Created:**

| File                                   | Purpose                                        |
| -------------------------------------- | ---------------------------------------------- |
| `src/styledconsole/utils/icon_data.py` | 224 emoji→ASCII+color mappings (16 categories) |
| `src/styledconsole/icons.py`           | Icon, IconProvider classes, mode switching     |
| `tests/unit/test_icons.py`             | 43 unit tests (all passing)                    |
| `examples/demos/icon_provider_demo.py` | Interactive demonstration                      |

**API (Implemented):**

```python
from styledconsole import icons, set_icon_mode, get_icon_mode, reset_icon_mode

# Access icons via attribute
print(icons.success)  # ✅ (emoji mode) or (OK) in green (ascii mode)
print(icons.error)    # ❌ (emoji mode) or (FAIL) in red (ascii mode)

# Mode control
set_icon_mode("ascii")   # Force colored ASCII everywhere
set_icon_mode("emoji")   # Force emoji everywhere
set_icon_mode("auto")    # Auto-detect (default)
reset_icon_mode()        # Reset to auto

# Bulk conversion
from styledconsole import convert_emoji_to_ascii
text = "✅ Test passed ❌ Test failed"
ascii_text = convert_emoji_to_ascii(text)  # "(OK) Test passed (FAIL) Test failed"
```

**Icon Categories (224 total):**

| Category  | Count | Examples                          |
| --------- | ----- | --------------------------------- |
| STATUS    | 11    | success, error, warning, info     |
| STARS     | 7     | star, glowing_star, sparkles      |
| DOCUMENT  | 9     | file, folder, clipboard, memo     |
| BOOK      | 12    | book_red, books, notebook         |
| TECH      | 16    | laptop, phone, keyboard, battery  |
| TOOLS     | 13    | wrench, hammer, gear, magnet      |
| ACTIVITY  | 11    | running, trophy, medal, dice      |
| TRANSPORT | 10    | rocket, car, airplane, ship       |
| WEATHER   | 12    | sun, moon, cloud, rain, lightning |
| PLANT     | 9     | seedling, tree, flower, cactus    |
| FOOD      | 12    | apple, pizza, coffee, cake        |
| PEOPLE    | 12    | person, wave, thumbs_up, clap     |
| ARROW     | 15    | right, left, up, down, cycle      |
| SYMBOL    | 17    | check, cross, plus, minus, star   |
| HEART     | 9     | heart_red, heart_blue, hearts     |
| MISC      | 49    | Various UI and semantic icons     |

<details>
<summary><strong>Complete Icon Mapping (click to expand - ARCHIVED)</strong></summary>

> Note: The original planning table is preserved below for reference.
> Actual implementation uses parentheses `(X)` instead of brackets `[X]`
> to avoid Rich markup parser conflicts.

#### Status & Results

| Name       | Unicode | ASCII    | Color    | Hex Code  |
| ---------- | ------- | -------- | -------- | --------- |
| `success`  | ✅      | `[OK]`   | green    | `#00ff00` |
| `error`    | ❌      | `[FAIL]` | red      | `#ff0000` |
| `warning`  | ⚠️      | `[WARN]` | yellow   | `#ffff00` |
| `info`     | ℹ️      | `[INFO]` | cyan     | `#00ffff` |
| `debug`    | 🔍      | `[DBG]`  | gray     | `#808080` |
| `critical` | 🔥      | `[CRIT]` | red bold | `#ff0000` |
| `skip`     | ⏭️      | `[SKIP]` | dim      | `#666666` |
| `pending`  | ⏳      | `[...]`  | yellow   | `#ffff00` |
| `running`  | 🔄      | `[~]`    | cyan     | `#00ffff` |

#### Test Execution

| Name        | Unicode | ASCII | Color  | Hex Code  |
| ----------- | ------- | ----- | ------ | --------- |
| `test`      | 🧪      | `[T]` | purple | `#9370db` |
| `suite`     | 📁      | `[S]` | blue   | `#1e90ff` |
| `step`      | ▶       | `>`   | cyan   | `#00ffff` |
| `keyword`   | 🔧      | `[K]` | gray   | `#808080` |
| `assertion` | ✓       | `[x]` | green  | `#00ff00` |

#### Colored Indicators (Circles → Dots)

| Name     | Unicode | ASCII | Color   | Hex Code  |
| -------- | ------- | ----- | ------- | --------- |
| `red`    | 🔴      | `●`   | red     | `#ff0000` |
| `yellow` | 🟡      | `●`   | yellow  | `#ffff00` |
| `green`  | 🟢      | `●`   | green   | `#00ff00` |
| `blue`   | 🔵      | `●`   | blue    | `#0000ff` |
| `orange` | 🟠      | `●`   | orange  | `#ff8c00` |
| `purple` | 🟣      | `●`   | magenta | `#ff00ff` |

#### Metrics & Data

| Name       | Unicode | ASCII | Color | Hex Code  |
| ---------- | ------- | ----- | ----- | --------- |
| `time`     | ⏱️      | `[t]` | cyan  | `#00ffff` |
| `chart`    | 📊      | `[#]` | blue  | `#1e90ff` |
| `up`       | 📈      | `[^]` | green | `#00ff00` |
| `down`     | 📉      | `[v]` | red   | `#ff0000` |
| `database` | 🗃️      | `[D]` | gray  | `#808080` |
| `api`      | 🌐      | `[@]` | blue  | `#1e90ff` |

#### Actions & Objects

| Name      | Unicode | ASCII | Color  | Hex Code  |
| --------- | ------- | ----- | ------ | --------- |
| `rocket`  | 🚀      | `>>>` | cyan   | `#00ffff` |
| `star`    | ⭐      | `*`   | yellow | `#ffd700` |
| `fire`    | 🔥      | `~`   | red    | `#ff4500` |
| `bulb`    | 💡      | `*`   | yellow | `#ffd700` |
| `gear`    | ⚙️      | `[*]` | gray   | `#808080` |
| `wrench`  | 🔧      | `[T]` | gray   | `#808080` |
| `target`  | 🎯      | `(o)` | red    | `#ff0000` |
| `trophy`  | 🏆      | `[#]` | gold   | `#ffd700` |
| `package` | 📦      | `[P]` | brown  | `#8b4513` |
| `folder`  | 📁      | `[/]` | blue   | `#1e90ff` |
| `file`    | 📄      | `[f]` | white  | `#ffffff` |
| `lock`    | 🔒      | `[L]` | gray   | `#808080` |
| `key`     | 🔑      | `[k]` | gold   | `#ffd700` |
| `link`    | 🔗      | `[-]` | blue   | `#1e90ff` |
| `tag`     | 🏷️      | `[t]` | purple | `#9370db` |

#### Arrows (No Color - Terminal Default)

| Name    | Unicode | ASCII |
| ------- | ------- | ----- |
| `right` | →       | `->`  |
| `left`  | ←       | `<-`  |
| `up`    | ↑       | `^`   |
| `down`  | ↓       | `v`   |

</details>

### Feature 2: Runtime Policy System (PENDING)

**Status:** Not yet implemented

**Problem:** No central control over rendering decisions based on environment.

**Proposed API:**

```python
from styledconsole import Console, RenderPolicy

# Auto-detect from environment
policy = RenderPolicy.from_env()
console = Console(policy=policy)

# Manual policy
policy = RenderPolicy(
    unicode=True,
    color=False,    # Respects NO_COLOR
    emoji=False,
)
console = Console(policy=policy)
```

**Environment Detection:**

| Variable    | Effect                         |
| ----------- | ------------------------------ |
| NO_COLOR    | `color=False`                  |
| TERM=dumb   | `unicode=False`, `emoji=False` |
| CI=true     | `emoji=False` (conservative)   |
| FORCE_COLOR | `color=True` (override)        |

______________________________________________________________________

## Test Automation Presets Roadmap (v0.10.0 - v0.14.0)

All presets follow established patterns:

- Accept optional `console` parameter
- Use semantic colors (`success`, `error`, `warning`, `info`)
- Support `render_*` variants for nesting
- Be theme-aware and export-friendly

### v0.10.0: Test Execution Flow Presets

**Theme:** Core test lifecycle reporting
**Target:** Q1 2026

| Preset           | Purpose                               |
| ---------------- | ------------------------------------- |
| `test_start()`   | Announce test beginning with metadata |
| `test_end()`     | Show test completion with pass/fail   |
| `suite_header()` | Suite introduction banner             |
| `suite_footer()` | Suite completion summary              |
| `step()`         | Numbered test step with status        |

<details>
<summary><strong>Preset Details (click to expand)</strong></summary>

#### `test_start()`

**Parameters:**

| Parameter     | Type        | Required | Description             |
| ------------- | ----------- | -------- | ----------------------- |
| `name`        | `str`       | Yes      | Test name/title         |
| `tags`        | `list[str]` | No       | Test tags/labels        |
| `suite`       | `str`       | No       | Parent suite name       |
| `description` | `str`       | No       | Test description        |
| `test_id`     | `str`       | No       | Unique test identifier  |
| `priority`    | `str`       | No       | Priority level          |
| `console`     | `Console`   | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Compact:
┏━━━━━━━━━━━━━━━━━━━━━ 🧪 TEST START ━━━━━━━━━━━━━━━━━━━━━━┓
┃ Login with valid credentials                             ┃
┃ 📁 Authentication Suite  🏷️ smoke, auth, critical        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Variant B - Minimal:
▶ 🧪 Login with valid credentials [smoke, auth, critical]
```

#### `test_end()`

**Parameters:**

| Parameter        | Type                                    | Required | Description             |
| ---------------- | --------------------------------------- | -------- | ----------------------- |
| `name`           | `str`                                   | Yes      | Test name/title         |
| `status`         | `Literal["PASS","FAIL","SKIP","ERROR"]` | Yes      | Test result status      |
| `duration`       | `float`                                 | No       | Duration in seconds     |
| `message`        | `str`                                   | No       | Result message          |
| `slow_threshold` | `float`                                 | No       | Seconds to mark as slow |
| `console`        | `Console`                               | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Compact:
✅ PASS  Login with valid credentials                    2.45s

❌ FAIL  Login with invalid password                     1.23s
   └─ Expected 'Welcome' but got 'Invalid credentials'

Variant B - Framed:
╭─────────────────── ✅ TEST PASSED ────────────────────╮
│ Login with valid credentials                          │
│ ⏱️  Duration: 2.45s                                   │
╰───────────────────────────────────────────────────────╯
```

#### `suite_header()`

**Parameters:**

| Parameter     | Type        | Required | Description             |
| ------------- | ----------- | -------- | ----------------------- |
| `name`        | `str`       | Yes      | Suite name              |
| `test_count`  | `int`       | No       | Number of tests         |
| `description` | `str`       | No       | Suite description       |
| `tags`        | `list[str]` | No       | Suite-level tags        |
| `path`        | `str`       | No       | File path               |
| `console`     | `Console`   | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Banner:
╔══════════════════════════════════════════════════════════════╗
║                   📁 AUTHENTICATION SUITE                    ║
║                      15 tests | regression, auth             ║
╚══════════════════════════════════════════════════════════════╝

Variant B - Minimal:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Authentication Suite (15 tests) [regression, auth]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### `suite_footer()`

**Parameters:**

| Parameter      | Type               | Required | Description             |
| -------------- | ------------------ | -------- | ----------------------- |
| `suite_name`   | `str`              | Yes      | Suite name              |
| `passed`       | `int`              | Yes      | Passed tests            |
| `failed`       | `int`              | Yes      | Failed tests            |
| `skipped`      | `int`              | No       | Skipped tests           |
| `duration`     | `float`            | No       | Total duration          |
| `slowest_test` | `tuple[str,float]` | No       | Slowest test info       |
| `failures`     | `list[str]`        | No       | Failed test names       |
| `console`      | `Console`          | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Summary box:
┏━━━━━━━━━━━━━━━━━━ 📊 SUITE COMPLETE ━━━━━━━━━━━━━━━━━━━┓
┃ Authentication Suite                                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ✅ Passed: 12    ❌ Failed: 2    ⏭️  Skipped: 1        ┃
┃ ⏱️  Duration: 45.7s                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Variant B - Compact:
📊 Authentication Suite: ✅ 12 passed | ❌ 2 failed | ⏭️ 1 skipped | ⏱️ 45.7s
```

#### `step()`

**Parameters:**

| Parameter     | Type                                                       | Required | Description             |
| ------------- | ---------------------------------------------------------- | -------- | ----------------------- |
| `number`      | `int`                                                      | Yes      | Step number             |
| `description` | `str`                                                      | Yes      | Step description        |
| `status`      | `Literal["pending","running","passed","failed","skipped"]` | No       | Step status             |
| `details`     | `str`                                                      | No       | Additional details      |
| `duration`    | `float`                                                    | No       | Step duration           |
| `level`       | `int`                                                      | No       | Nesting level           |
| `console`     | `Console`                                                  | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Checklist:
  ✅ 1. Navigate to login page                           0.5s
  ✅ 2. Enter username                                   0.1s
  🔄 3. Click submit button                              ...
  ⏳ 4. Verify dashboard loads

Variant B - BDD/Gherkin:
  Given I am on the login page                           ✅
   When I enter valid credentials                        ✅
   Then I should see the dashboard                       ⏳
```

</details>

______________________________________________________________________

### v0.11.0: Assertions & Validation Presets

**Theme:** Test assertions and data validation visualization
**Target:** Q1 2026

| Preset                | Purpose                             |
| --------------------- | ----------------------------------- |
| `assertion_result()`  | Side-by-side comparison with diff   |
| `validation_table()`  | Table of validation checks          |
| `diff_view()`         | Visual diff for string/data         |
| `assertion_summary()` | Summary of all assertions in a test |

<details>
<summary><strong>Preset Details (click to expand)</strong></summary>

#### `assertion_result()`

**Parameters:**

| Parameter  | Type      | Required | Description                          |
| ---------- | --------- | -------- | ------------------------------------ |
| `label`    | `str`     | Yes      | Description of what's being asserted |
| `expected` | `Any`     | Yes      | Expected value                       |
| `actual`   | `Any`     | Yes      | Actual value received                |
| `passed`   | `bool`    | Yes      | Whether assertion passed             |
| `operator` | `str`     | No       | Comparison operator                  |
| `diff`     | `bool`    | No       | Show character-level diff            |
| `console`  | `Console` | No       | Custom Console instance              |

**Visualization Variants:**

```text
Variant A - Framed:
╭─────────────────── ❌ ASSERTION FAILED ───────────────────╮
│ Response status code                                      │
├───────────────────────────────────────────────────────────┤
│ Expected: 200                                             │
│ Actual:   404                                             │
╰───────────────────────────────────────────────────────────╯

Variant B - Inline:
❌ Response status code: expected 200, got 404
```

#### `validation_table()`

**Parameters:**

| Parameter  | Type                    | Required | Description               |
| ---------- | ----------------------- | -------- | ------------------------- |
| `checks`   | `list[ValidationCheck]` | Yes      | List of validation checks |
| `title`    | `str`                   | No       | Table title               |
| `show_all` | `bool`                  | No       | Show passed checks too    |
| `console`  | `Console`               | No       | Custom Console instance   |

**Visualization Variants:**

```text
Variant A - Table:
╭────────────────── 📋 API Response Validation ──────────────────╮
│  Status  │ Check                      │ Details                │
│ ─────────┼────────────────────────────┼─────────────────────── │
│    ✅    │ Status code is 200         │                        │
│    ❌    │ Body contains 'success'    │ got: error             │
│  Summary: 4/5 passed (80%)                                     │
╰────────────────────────────────────────────────────────────────╯

Variant B - Checklist:
📋 API Response Validation
  ✅ Status code is 200
  ❌ Body contains 'success' → got: error
Result: 4/5 passed (80%)
```

#### `diff_view()`

**Parameters:**

| Parameter  | Type                           | Required | Description             |
| ---------- | ------------------------------ | -------- | ----------------------- |
| `expected` | `str`                          | Yes      | Expected content        |
| `actual`   | `str`                          | Yes      | Actual content          |
| `format`   | `Literal["text","json","xml"]` | No       | Content format          |
| `context`  | `int`                          | No       | Lines of context        |
| `title`    | `str`                          | No       | Diff title              |
| `console`  | `Console`                      | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Unified diff:
 {
-  "status": "ok",
+  "status": "error",
 }

Variant B - Side-by-side:
│ Expected            │ Actual                              │
│ "status": "ok"      │ "status": "error"         ← CHANGED │
```

#### `assertion_summary()`

**Parameters:**

| Parameter    | Type                    | Required | Description              |
| ------------ | ----------------------- | -------- | ------------------------ |
| `total`      | `int`                   | Yes      | Total assertion count    |
| `passed`     | `int`                   | Yes      | Passed assertion count   |
| `failed`     | `int`                   | Yes      | Failed assertion count   |
| `assertions` | `list[AssertionDetail]` | No       | Failed assertion details |
| `test_name`  | `str`                   | No       | Test name for context    |
| `console`    | `Console`               | No       | Custom Console instance  |

**Visualization Variants:**

```text
Variant A - Summary box:
╭─────────────── 📊 Assertion Summary ────────────────╮
│ Total: 10  │  ✅ Passed: 8  │  ❌ Failed: 2         │
│ ████████░░░░░░░░░░░░░░░░░░░░  80% pass rate         │
╰─────────────────────────────────────────────────────╯

Variant B - Compact:
📊 Assertions: 8/10 passed (80%) - 2 failures
```

</details>

______________________________________________________________________

### v0.12.0: Data & API Presets

**Theme:** Data inspection and API response visualization
**Target:** Q2 2026

| Preset                     | Purpose                     |
| -------------------------- | --------------------------- |
| `data_snapshot()`          | Pretty-print JSON/dict/list |
| `api_response()`           | HTTP response visualization |
| `api_request()`            | HTTP request visualization  |
| `db_result()`              | Database query result table |
| `timing_breakdown()`       | Bar chart of step durations |
| `performance_comparison()` | Before/after with % change  |

<details>
<summary><strong>Preset Details (click to expand)</strong></summary>

#### `data_snapshot()`

**Parameters:**

| Parameter   | Type                            | Required | Description             |
| ----------- | ------------------------------- | -------- | ----------------------- |
| `name`      | `str`                           | Yes      | Snapshot label          |
| `data`      | `Any`                           | Yes      | Data to display         |
| `format`    | `Literal["json","yaml","auto"]` | No       | Output format           |
| `max_depth` | `int`                           | No       | Max nesting depth       |
| `highlight` | `list[str]`                     | No       | Keys to highlight       |
| `console`   | `Console`                       | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Framed JSON:
╭──────────────────── 📦 User Response ─────────────────────╮
│ {                                                         │
│   "id": 123,                                              │
│   "name": "John"                                          │
│ }                                                         │
╰───────────────────────────────────────────────────────────╯

Variant B - Tree view:
📦 Configuration
├── database
│   ├── host: "localhost"
│   └── port: 5432
└── cache
    └── enabled: true
```

#### `api_response()`

**Parameters:**

| Parameter     | Type            | Required | Description              |
| ------------- | --------------- | -------- | ------------------------ |
| `method`      | `str`           | Yes      | HTTP method              |
| `url`         | `str`           | Yes      | Request URL              |
| `status_code` | `int`           | Yes      | Response status code     |
| `duration`    | `float`         | No       | Response time in seconds |
| `headers`     | `dict[str,str]` | No       | Response headers         |
| `body`        | `Any`           | No       | Response body            |
| `console`     | `Console`       | No       | Custom Console instance  |

**Visualization Variants:**

```text
Variant A - Full detail:
┏━━━━━━━━━━━━━━━━━━ 🌐 API Response ━━━━━━━━━━━━━━━━━━━┓
┃ POST /api/v1/users                                   ┃
┃ ✅ 201 Created                        ⏱️ 234ms       ┃
┃ Body: {"id": 456, "created": true}                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Variant B - Compact:
✅ POST /api/v1/users → 201 Created (234ms)
```

#### `api_request()`

**Parameters:**

| Parameter | Type            | Required | Description             |
| --------- | --------------- | -------- | ----------------------- |
| `method`  | `str`           | Yes      | HTTP method             |
| `url`     | `str`           | Yes      | Request URL             |
| `headers` | `dict[str,str]` | No       | Request headers         |
| `body`    | `Any`           | No       | Request body            |
| `params`  | `dict[str,str]` | No       | Query parameters        |
| `console` | `Console`       | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Framed:
╭────────────────────── 📤 API Request ──────────────────────╮
│ POST https://api.example.com/users                         │
│ Headers: Authorization: Bearer ***                         │
│ Body: {"name": "John"}                                     │
╰────────────────────────────────────────────────────────────╯

Variant B - cURL:
curl -X POST 'https://api.example.com/users' \
  -H 'Authorization: Bearer ***' \
  -d '{"name": "John"}'
```

#### `db_result()`

**Parameters:**

| Parameter   | Type          | Required | Description             |
| ----------- | ------------- | -------- | ----------------------- |
| `query`     | `str`         | No       | SQL query executed      |
| `columns`   | `list[str]`   | Yes      | Column names            |
| `rows`      | `list[tuple]` | Yes      | Result rows             |
| `duration`  | `float`       | No       | Query duration          |
| `row_count` | `int`         | No       | Total row count         |
| `console`   | `Console`     | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Full table:
╭────────────────────── 🗃️ Query Result ──────────────────────╮
│  id  │  name     │  email                                   │
│ ─────┼───────────┼───────────────────────────────────────── │
│  1   │  Alice    │  alice@example.com                       │
│  2   │  Bob      │  bob@example.com                         │
│ ⏱️ 45ms  │  📊 2 rows                                       │
╰─────────────────────────────────────────────────────────────╯

Variant B - Compact:
🗃️ 2 rows (45ms): id, name, email
```

#### `timing_breakdown()`

**Parameters:**

| Parameter   | Type               | Required | Description             |
| ----------- | ------------------ | -------- | ----------------------- |
| `timings`   | `dict[str, float]` | Yes      | Step name → duration    |
| `title`     | `str`              | No       | Chart title             |
| `unit`      | `str`              | No       | Time unit (s, ms)       |
| `threshold` | `float`            | No       | Slow threshold          |
| `console`   | `Console`          | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Horizontal bars:
╭────────────────── ⏱️ Timing Breakdown ─────────────────╮
│ Setup       ████████░░░░░░░░░░░░░░░░░░░░░░░░  1.2s     │
│ Login       █████████████░░░░░░░░░░░░░░░░░░░  2.5s ⚠️  │
│ Submit form ████████████████░░░░░░░░░░░░░░░░  3.1s ⚠️  │
│ Total: 9.5s                                            │
╰────────────────────────────────────────────────────────╯

Variant B - Sparkline:
⏱️ Timing: Setup(1.2) → Login(2.5⚠️) → Submit(3.1⚠️) | Total: 9.5s
```

#### `performance_comparison()`

**Parameters:**

| Parameter         | Type      | Required | Description             |
| ----------------- | --------- | -------- | ----------------------- |
| `metric`          | `str`     | Yes      | Metric name             |
| `baseline`        | `float`   | Yes      | Baseline value          |
| `current`         | `float`   | Yes      | Current value           |
| `unit`            | `str`     | No       | Value unit              |
| `threshold`       | `float`   | No       | Acceptable threshold    |
| `lower_is_better` | `bool`    | No       | Lower values are better |
| `console`         | `Console` | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Comparison box:
╭──────────────── 📊 Performance Comparison ────────────────╮
│ Response Time                                             │
│ Baseline:  250ms  →  Current: 180ms                       │
│ Change:    -70ms (↓ 28%)  ✅ IMPROVED                     │
╰───────────────────────────────────────────────────────────╯

Variant B - Inline:
📊 Response Time: 250ms → 180ms (↓ 28%) ✅ IMPROVED
```

</details>

______________________________________________________________________

### v0.13.0: CI/CD & Error Reporting Presets

**Theme:** CI/CD integration and error visualization
**Target:** Q2 2026

| Preset                | Purpose                          |
| --------------------- | -------------------------------- |
| `failure_detail()`    | Rich failure report with context |
| `retry_status()`      | Retry progress indicator         |
| `flaky_test_alert()`  | Flaky test warning with history  |
| `build_status()`      | CI job summary                   |
| `regression_report()` | Compare against baseline         |
| `coverage_delta()`    | Coverage change visualization    |
| `artifact_list()`     | Build artifacts with sizes       |

<details>
<summary><strong>Preset Details (click to expand)</strong></summary>

#### `failure_detail()`

**Parameters:**

| Parameter    | Type        | Required | Description             |
| ------------ | ----------- | -------- | ----------------------- |
| `test`       | `str`       | Yes      | Test name               |
| `error`      | `str`       | Yes      | Error message           |
| `stacktrace` | `str`       | No       | Full stack trace        |
| `screenshot` | `str`       | No       | Path to screenshot      |
| `logs`       | `list[str]` | No       | Relevant log lines      |
| `duration`   | `float`     | No       | Test duration           |
| `context`    | `dict`      | No       | Additional context      |
| `console`    | `Console`   | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Full detail:
┏━━━━━━━━━━━━━━━━━━━━━━━ ❌ TEST FAILURE ━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Login with invalid password                                   ┃
┃ 💥 Error: AssertionError: Expected 'Welcome'                  ┃
┃ 📜 Stack: test_login.py:45                                    ┃
┃ 📋 Logs: [5 lines]                                            ┃
┃ 📸 Screenshot: /screenshots/failure_001.png                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Variant B - Compact:
❌ Login with invalid password (3.2s)
   Error: AssertionError: Expected 'Welcome'
   File: test_login.py:45
```

#### `retry_status()`

**Parameters:**

| Parameter      | Type      | Required | Description             |
| -------------- | --------- | -------- | ----------------------- |
| `attempt`      | `int`     | Yes      | Current attempt number  |
| `max_attempts` | `int`     | Yes      | Maximum retry attempts  |
| `last_error`   | `str`     | No       | Last error message      |
| `wait_time`    | `float`   | No       | Wait before next retry  |
| `operation`    | `str`     | No       | Operation being retried |
| `console`      | `Console` | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Progress box:
╭────────────────── 🔄 RETRY 2/3 ──────────────────╮
│ Database connection                              │
│ ⚠️ Last error: Connection timeout                │
│ ⏳ Waiting 5s before next attempt...             │
╰──────────────────────────────────────────────────╯

Variant B - Inline:
🔄 Retry 2/3: Database connection - waiting 5s
```

#### `flaky_test_alert()`

**Parameters:**

| Parameter        | Type        | Required | Description              |
| ---------------- | ----------- | -------- | ------------------------ |
| `name`           | `str`       | Yes      | Test name                |
| `pass_rate`      | `float`     | Yes      | Pass rate (0.0 to 1.0)   |
| `recent_results` | `list[str]` | No       | Recent PASS/FAIL history |
| `recommendation` | `str`       | No       | Suggested fix            |
| `first_seen`     | `str`       | No       | When flakiness started   |
| `console`        | `Console`   | No       | Custom Console instance  |

**Visualization Variants:**

```text
Variant A - Alert box:
╭───────────────── ⚠️ FLAKY TEST DETECTED ─────────────────╮
│ Async notification test                                  │
│ 📊 Pass Rate: 60%  📈 History: ✅❌✅❌❌               │
│ 💡 Consider adding explicit waits                        │
╰──────────────────────────────────────────────────────────╯

Variant B - Compact:
⚠️ FLAKY: Async notification test (60% pass rate)
```

#### `build_status()`

**Parameters:**

| Parameter  | Type                                                 | Required | Description             |
| ---------- | ---------------------------------------------------- | -------- | ----------------------- |
| `job`      | `str`                                                | Yes      | Job/build name          |
| `status`   | `Literal["success","failure","running","cancelled"]` | Yes      | Build status            |
| `commit`   | `str`                                                | No       | Commit SHA              |
| `branch`   | `str`                                                | No       | Branch name             |
| `duration` | `int`                                                | No       | Duration in seconds     |
| `url`      | `str`                                                | No       | Build URL               |
| `console`  | `Console`                                            | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Status card:
╭────────────────── ✅ BUILD SUCCESS ──────────────────╮
│ Unit Tests                                           │
│ 🔀 Branch: main  📝 Commit: abc1234  ⏱️ 2m 5s        │
╰──────────────────────────────────────────────────────╯

Variant B - Inline:
✅ Unit Tests (main@abc1234) - 2m 5s
```

#### `regression_report()`

**Parameters:**

| Parameter       | Type        | Required | Description             |
| --------------- | ----------- | -------- | ----------------------- |
| `new_failures`  | `list[str]` | No       | Tests that newly failed |
| `fixed`         | `list[str]` | No       | Tests that were fixed   |
| `still_failing` | `list[str]` | No       | Persistent failures     |
| `baseline_run`  | `str`       | No       | Baseline build ID       |
| `current_run`   | `str`       | No       | Current build ID        |
| `console`       | `Console`   | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Full report:
╭─────────────────── 📊 REGRESSION REPORT ───────────────────╮
│ Comparing: Build #122 → Build #123                     │
│ ❌ NEW FAILURES (2): Login timeout, Payment validation     │
│ ✅ FIXED (2): Cart calculation, Session handling           │
│ ⚠️ STILL FAILING (1): Legacy API test                      │
╰────────────────────────────────────────────────────────────╯

Variant B - Compact:
📊 Build #122 → #123: ❌ +2 failures | ✅ +2 fixes | ⚠️ 1 still failing
```

#### `coverage_delta()`

**Parameters:**

| Parameter       | Type                 | Required | Description             |
| --------------- | -------------------- | -------- | ----------------------- |
| `before`        | `float`              | Yes      | Previous coverage %     |
| `after`         | `float`              | Yes      | Current coverage %      |
| `changed_files` | `list[FileCoverage]` | No       | Per-file coverage       |
| `threshold`     | `float`              | No       | Minimum acceptable %    |
| `console`       | `Console`            | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - Coverage card:
╭────────────────── 📊 COVERAGE DELTA ──────────────────╮
│ Overall: 82.5% → 84.1% (↑ +1.6%)                      │
│ ████████████████░░░░  84.1%  ✅ Above threshold (80%) │
╰───────────────────────────────────────────────────────╯

Variant B - Compact:
📊 Coverage: 82.5% → 84.1% (↑ +1.6%) ✅
```

#### `artifact_list()`

**Parameters:**

| Parameter    | Type             | Required | Description             |
| ------------ | ---------------- | -------- | ----------------------- |
| `artifacts`  | `list[Artifact]` | Yes      | List of artifacts       |
| `title`      | `str`            | No       | Section title           |
| `total_size` | `str`            | No       | Total size              |
| `console`    | `Console`        | No       | Custom Console instance |

**Visualization Variants:**

```text
Variant A - File list:
╭────────────── 📦 Build Artifacts ──────────────╮
│ 📊 test-report.html              2.4 MB        │
│ 📁 screenshots.zip              15.2 MB        │
│ 📈 coverage.xml                  156 KB        │
│ Total: 5 files (19.1 MB)                       │
╰────────────────────────────────────────────────╯

Variant B - Compact:
📦 Artifacts (5 files, 19.1 MB): test-report.html, screenshots.zip...
```

</details>

______________________________________________________________________

### v0.14.0: Robot Framework Presets

**Theme:** Robot Framework specific reporting
**Target:** Q2 2026

| Preset                 | Purpose                        |
| ---------------------- | ------------------------------ |
| `rf_keyword_log()`     | Keyword execution with nesting |
| `rf_library_info()`    | Library import info            |
| `rf_variable_table()`  | Variable scope display         |
| `rf_tag_summary()`     | Pass/fail by tag               |
| `rf_suite_structure()` | Visual suite hierarchy         |
| `rf_test_template()`   | Data-driven test template      |

<details>
<summary><strong>Preset Details (click to expand)</strong></summary>

#### `rf_keyword_log()`

**Parameters:**

| Parameter  | Type            | Default    | Description           |
| ---------- | --------------- | ---------- | --------------------- |
| `keyword`  | `str`           | (required) | Keyword name          |
| `args`     | `list[str]`     | `[]`       | Keyword arguments     |
| `doc`      | `str \| None`   | `None`     | Keyword documentation |
| `level`    | `int`           | `0`        | Nesting level         |
| `status`   | `str`           | `"PASS"`   | PASS, FAIL, SKIP      |
| `duration` | `float \| None` | `None`     | Execution time        |
| `msg`      | `str \| None`   | `None`     | Status message        |
| `console`  | `Console`       | `None`     | Console instance      |

**Visualization Variants:**

```text
Variant A - Indented Tree:
🔧 Login To Application    admin, ***                    ✅ 1.20s
   ├─ 🔧 Input Text    id=username, admin               ✅ 0.15s
   ├─ 🔧 Input Text    id=password, ***                 ✅ 0.12s
   └─ 🔧 Click Button  id=submit                        ✅ 0.08s

Variant B - Compact Timeline:
[00:01.20] ✅ Login To Application (admin, ***)
  [00:00.15] ✅ Input Text
  [00:00.12] ✅ Input Text
```

#### `rf_library_info()`

**Parameters:**

| Parameter        | Type          | Default    | Description         |
| ---------------- | ------------- | ---------- | ------------------- |
| `name`           | `str`         | (required) | Library name        |
| `version`        | `str \| None` | `None`     | Library version     |
| `keywords_count` | `int \| None` | `None`     | Number of keywords  |
| `scope`          | `str`         | `"TEST"`   | GLOBAL, SUITE, TEST |
| `doc_url`        | `str \| None` | `None`     | Documentation URL   |
| `init_args`      | `dict`        | `{}`       | Init arguments      |
| `console`        | `Console`     | `None`     | Console instance    |

**Visualization Variants:**

```text
Variant A - Compact Card:
╭─ 📚 SeleniumLibrary ─────────────────────────────────╮
│ Version: 6.1.0          Scope: GLOBAL                │
│ Keywords: 145           Init: timeout=10s            │
╰──────────────────────────────────────────────────────╯

Variant B - Inline:
📚 SeleniumLibrary v6.1.0 [GLOBAL] 145 keywords
```

#### `rf_variable_table()`

**Parameters:**

| Parameter   | Type             | Default    | Description           |
| ----------- | ---------------- | ---------- | --------------------- |
| `variables` | `dict[str, Any]` | (required) | Variable name → value |
| `scope`     | `str \| None`    | `None`     | GLOBAL, SUITE, TEST   |
| `source`    | `str \| None`    | `None`     | Source file           |
| `mask_keys` | `list[str]`      | `[]`       | Variables to mask     |
| `console`   | `Console`        | `None`     | Console instance      |

**Visualization Variants:**

```text
Variant A - Categorized:
╭─ 📋 Suite Variables ─────────────────────────────────╮
│ 📝 Scalars:                                          │
│   ${BASE_URL}    │ https://example.com               │
│   ${BROWSER}     │ chrome                            │
│ 📋 Lists:                                            │
│   @{USERS}       │ [admin, user1, user2]             │
╰──────────────────────────────────────────────────────╯

Variant B - Flat:
📋 Variables (SUITE):
  ${BASE_URL} = https://example.com
  ${BROWSER}  = chrome
```

#### `rf_tag_summary()`

**Parameters:**

| Parameter      | Type                        | Default    | Description            |
| -------------- | --------------------------- | ---------- | ---------------------- |
| `tags`         | `dict[str, dict[str, int]]` | (required) | Tag → {passed, failed} |
| `title`        | `str \| None`               | `None`     | Custom title           |
| `show_percent` | `bool`                      | `True`     | Show percentage        |
| `highlight`    | `list[str]`                 | `[]`       | Tags to highlight      |
| `console`      | `Console`                   | `None`     | Console instance       |

**Visualization Variants:**

```text
Variant A - Bar Chart:
╭─ 🏷️ Test Results by Tag ────────────────────────────╮
│ smoke       ██████████████████████████████ 100%  ⭐ │
│ critical    ████████████████████████████░░  95%  ⭐ │
│ regression  ██████████████████████████░░░░  90%     │
╰─────────────────────────────────────────────────────╯

Variant B - Table:
│ Tag          │ Passed │ Failed │  %   │
│ ⭐ smoke     │     10 │      0 │ 100% │
│ ⭐ critical  │     20 │      1 │  95% │
```

#### `rf_suite_structure()`

**Parameters:**

| Parameter       | Type          | Default    | Description            |
| --------------- | ------------- | ---------- | ---------------------- |
| `structure`     | `dict`        | (required) | Nested suite structure |
| `title`         | `str \| None` | `None`     | Custom title           |
| `show_counts`   | `bool`        | `True`     | Show test counts       |
| `show_status`   | `bool`        | `True`     | Show suite status      |
| `show_duration` | `bool`        | `False`    | Show execution time    |
| `console`       | `Console`     | `None`     | Console instance       |

**Visualization Variants:**

```text
Variant A - Tree:
╭─ 🗂️ Test Suite Hierarchy ───────────────────────────╮
│ 📁 All Tests                          ❌ 125.5s     │
│ ├─ 📂 Auth (5 tests)                  ✅  15.2s     │
│ ├─ 📁 API (12 tests)                  ❌  45.8s     │
│ │  ├─ 📂 Users (6 tests)              ✅  20.1s     │
│ │  └─ 📂 Orders (6 tests)             ❌  25.7s     │
│ └─ 📂 UI (8 tests)                    ✅  64.5s     │
╰─────────────────────────────────────────────────────╯

Variant B - Indented:
All Tests                                    ❌ 2m 5.5s
  Auth                           5 tests     ✅ 15.2s
  API                           12 tests     ❌ 45.8s
```

#### `rf_test_template()`

**Parameters:**

| Parameter       | Type                | Default    | Description            |
| --------------- | ------------------- | ---------- | ---------------------- |
| `template`      | `str`               | (required) | Template keyword name  |
| `test_cases`    | `list[dict]`        | (required) | List of test case data |
| `arg_names`     | `list[str] \| None` | `None`     | Column names           |
| `show_duration` | `bool`              | `False`    | Show duration          |
| `console`       | `Console`           | `None`     | Console instance       |

**Visualization Variants:**

```text
Variant A - Data Table:
╭─ 📊 Login Credential Tests ─────────────────────────────────╮
│ Template: Login With Credentials                            │
│ ┌────┬──────────────┬──────────────┬────────┐               │
│ │  # │ Username     │ Password     │ Result │               │
│ │  1 │ valid_user   │ valid_pass   │ ✅ 1.2s│               │
│ │  2 │ invalid_user │ any_pass     │ ❌ 0.9s│               │
│ └────┴──────────────┴──────────────┴────────┘               │
│ Summary: ✅ 3 passed  ❌ 1 failed                           │
╰─────────────────────────────────────────────────────────────╯

Variant B - Compact:
📊 Template: Login With Credentials
  ✅ [1] valid_user, valid_pass → SUCCESS              1.2s
  ❌ [2] invalid_user, any_pass → USER_NOT_FOUND       0.9s
```

</details>

______________________________________________________________________

## Known Issues

### Current Limitations

| Area      | Limitation                                |
| --------- | ----------------------------------------- |
| Emojis    | Tier 1 only (no skin tones, no ZWJ)       |
| Terminals | Some emulators have limited emoji support |
| Gradients | Horizontal not yet implemented            |

### Not Planned

Based on lessons learned, we explicitly avoid:

- ❌ Tier 2/3 emoji support (complexity risk)
- ❌ Plugin systems
- ❌ Factory factories
- ❌ Post-rendering alignment hacks

______________________________________________________________________

## Architecture Principles

| Principle              | Description                        |
| ---------------------- | ---------------------------------- |
| Simplicity             | Add complexity only when necessary |
| Test Everything        | Maintain 95%+ coverage             |
| Single Responsibility  | Each module has one purpose        |
| Document Everything    | Type hints + docstrings            |
| Backward Compatibility | Stable public API                  |

______________________________________________________________________

## References

- **User Guide:** `docs/USER_GUIDE.md`
- **Developer Guide:** `docs/DEVELOPER_GUIDE.md`
- **Changelog:** `CHANGELOG.md`
