# StyledConsole Project Status

**Version:** 0.8.0
**Status:** Release Ready
**Last Updated:** November 30, 2025

______________________________________________________________________

## Table of Contents

1. [Current Version](#current-version)
1. [Roadmap](#roadmap)
1. [v0.8.0 Implementation Plan](#v080-implementation-plan)
1. [v0.7.0 Implementation Plan](#v070-implementation-plan)
1. [Active Tasks](#active-tasks)
1. [Known Issues](#known-issues)
1. [Changelog](#changelog)

______________________________________________________________________

## Current Version

### v0.8.0 (November 2025)

**Status:** ✅ Release Ready

| Metric        | Value       |
| ------------- | ----------- |
| Lines of Code | ~5,500      |
| Tests         | 754 passing |
| Coverage      | 84%+        |
| Examples      | 29          |

**Key Features:**

- ✅ Theme System with 10 predefined themes (6 solid + 4 gradient)
- ✅ Gradient themes with auto-applied border, banner, and text gradients
- ✅ Custom themes via `Theme` dataclass with `GradientSpec`
- ✅ `Console(theme=...)` parameter
- ✅ Semantic color resolution (`color="success"`)
- ✅ `console.progress()` context manager
- ✅ `StyledProgress` wrapper with theme integration
- ✅ Presets updated with semantic colors for theme compatibility

______________________________________________________________________

## Roadmap

### Released

| Version | Date     | Theme                     |
| ------- | -------- | ------------------------- |
| v0.1.0  | Oct 2025 | Foundation                |
| v0.3.0  | Nov 2025 | Rich-Native rendering     |
| v0.4.0  | Nov 2025 | Animated Gradients        |
| v0.5.0  | Nov 2025 | Documentation & Structure |
| v0.6.0  | Nov 2025 | text.py Refactoring       |
| v0.7.0  | Nov 2025 | Frame Groups              |
| v0.8.0  | Nov 2025 | Theme System & Gradients  |

### In Progress

| Version | Target  | Theme                  |
| ------- | ------- | ---------------------- |
| v0.9.0  | Q1 2026 | Icon Provider & Policy |

### Planned

| Version | Target  | Theme                                     |
| ------- | ------- | ----------------------------------------- |
| v0.9.0  | Q1 2026 | Icon Provider & Runtime Policy            |
| v0.10.0 | Q1 2026 | Test Automation Presets - Core            |
| v0.11.0 | Q1 2026 | Test Automation Presets - Assertions      |
| v0.12.0 | Q2 2026 | Test Automation Presets - Data & API      |
| v0.13.0 | Q2 2026 | Test Automation Presets - CI/CD           |
| v0.14.0 | Q2 2026 | Test Automation Presets - Robot Framework |
| v1.0.0  | Q3 2026 | API freeze & Production Hardening         |

______________________________________________________________________

## Test Automation Presets Roadmap (v0.10.0 - v0.14.0)

This section outlines the planned presets for test automation and reporting use cases.
All presets will follow the established patterns:

- Accept optional `console` parameter
- Use semantic colors (`success`, `error`, `warning`, `info`)
- Support `render_*` variants for nesting
- Be theme-aware and export-friendly

______________________________________________________________________

### v0.10.0: Test Execution Flow Presets

**Theme:** Core test lifecycle reporting
**Target:** Q1 2026
**Status:** PLANNED

#### Preset 1: `test_start()`

**Purpose:** Announce test beginning with metadata. Provides visual separation between tests
and displays relevant context like tags, suite membership, and test description.

**Use Cases:**

- Test runner integration for visual test start markers
- Debug logging with test context
- Console-based test execution monitoring

**Parameters:**

| Parameter     | Type        | Required | Description                        |
| ------------- | ----------- | -------- | ---------------------------------- |
| `name`        | `str`       | Yes      | Test name/title                    |
| `tags`        | `list[str]` | No       | Test tags/labels                   |
| `suite`       | `str`       | No       | Parent suite name                  |
| `description` | `str`       | No       | Test description or docstring      |
| `test_id`     | `str`       | No       | Unique test identifier             |
| `priority`    | `str`       | No       | Priority level (critical/high/etc) |
| `console`     | `Console`   | No       | Custom Console instance            |

```python
from styledconsole.presets import test_start

test_start(
    name="Login with valid credentials",
    tags=["smoke", "auth", "critical"],
    suite="Authentication Suite",
    description="Verify user can login with valid username and password"
)
```

**Visualization Variant A - Compact (default):**

```text
┏━━━━━━━━━━━━━━━━━━━━━ 🧪 TEST START ━━━━━━━━━━━━━━━━━━━━━━┓
┃ Login with valid credentials                             ┃
┃ 📁 Authentication Suite  🏷️ smoke, auth, critical        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Visualization Variant B - Detailed:**

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 🧪 TEST START                                            ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Login with valid credentials                             ┃
┃──────────────────────────────────────────────────────────┃
┃ 📁 Suite: Authentication Suite                           ┃
┃ 🏷️  Tags:  smoke, auth, critical                         ┃
┃ 📝 Verify user can login with valid username and password┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Visualization Variant C - Minimal (inline):**

```text
▶ 🧪 Login with valid credentials [smoke, auth, critical]
```

______________________________________________________________________

#### Preset 2: `test_end()`

**Purpose:** Show test completion with pass/fail styling. Displays final status with
duration and optional result message. Color-coded based on status for instant recognition.

**Use Cases:**

- Test completion markers in console output
- Duration tracking and slow test identification
- Pass/fail summary with context

**Parameters:**

| Parameter        | Type                                    | Required | Description              |
| ---------------- | --------------------------------------- | -------- | ------------------------ |
| `name`           | `str`                                   | Yes      | Test name/title          |
| `status`         | `Literal["PASS","FAIL","SKIP","ERROR"]` | Yes      | Test result status       |
| `duration`       | `float`                                 | No       | Duration in seconds      |
| `message`        | `str`                                   | No       | Result message or reason |
| `slow_threshold` | `float`                                 | No       | Seconds to mark as slow  |
| `console`        | `Console`                               | No       | Custom Console instance  |

```python
from styledconsole.presets import test_end

# Passed test
test_end(
    name="Login with valid credentials",
    status="PASS",
    duration=2.45,
    message="All assertions passed"
)

# Failed test
test_end(
    name="Login with invalid password",
    status="FAIL",
    duration=1.23,
    message="Expected 'Welcome' but got 'Invalid credentials'"
)
```

**Visualization Variant A - Compact (default):**

```text
✅ PASS  Login with valid credentials                    2.45s
```

```text
❌ FAIL  Login with invalid password                     1.23s
   └─ Expected 'Welcome' but got 'Invalid credentials'
```

**Visualization Variant B - Framed:**

```text
╭─────────────────── ✅ TEST PASSED ────────────────────╮
│ Login with valid credentials                          │
│ ⏱️  Duration: 2.45s                                    │
│ 📝 All assertions passed                              │
╰───────────────────────────────────────────────────────╯
```

```text
╭─────────────────── ❌ TEST FAILED ────────────────────╮
│ Login with invalid password                           │
│ ⏱️  Duration: 1.23s                                    │
│ 💬 Expected 'Welcome' but got 'Invalid credentials'   │
╰───────────────────────────────────────────────────────╯
```

**Visualization Variant C - Status bar:**

```text
┃ ✅ PASS ┃ Login with valid credentials ┃ 2.45s ┃ All assertions passed ┃
```

______________________________________________________________________

#### Preset 3: `suite_header()`

**Purpose:** Suite introduction banner. Creates visual separation and context when
entering a new test suite. Displays suite metadata and expected test count.

**Use Cases:**

- Test suite separation in long test runs
- Suite-level documentation display
- Test count expectations

**Parameters:**

| Parameter     | Type        | Required | Description              |
| ------------- | ----------- | -------- | ------------------------ |
| `name`        | `str`       | Yes      | Suite name               |
| `test_count`  | `int`       | No       | Number of tests in suite |
| `description` | `str`       | No       | Suite description        |
| `tags`        | `list[str]` | No       | Suite-level tags         |
| `path`        | `str`       | No       | File path or location    |
| `console`     | `Console`   | No       | Custom Console instance  |

```python
from styledconsole.presets import suite_header

suite_header(
    name="Authentication Suite",
    test_count=15,
    description="End-to-end authentication tests",
    tags=["regression", "auth"],
    path="tests/auth/test_login.py"
)
```

**Visualization Variant A - Banner (default):**

```text
╔══════════════════════════════════════════════════════════════╗
║                   📁 AUTHENTICATION SUITE                    ║
║                      15 tests | regression, auth             ║
╠══════════════════════════════════════════════════════════════╣
║ End-to-end authentication tests                              ║
║ 📂 tests/auth/test_login.py                                  ║
╚══════════════════════════════════════════════════════════════╝
```

**Visualization Variant B - Minimal:**

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Authentication Suite (15 tests) [regression, auth]
End-to-end authentication tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Visualization Variant C - ASCII art banner:**

```text
    _         _   _                _   _           _   _
   / \  _   _| |_| |__   ___ _ __ | |_(_) ___ __ _| |_(_) ___  _ __
  / _ \| | | | __| '_ \ / _ \ '_ \| __| |/ __/ _` | __| |/ _ \| '_ \
 / ___ \ |_| | |_| | | |  __/ | | | |_| | (_| (_| | |_| | (_) | | | |
/_/   \_\__,_|\__|_| |_|\___|_| |_|\__|_|\___\__,_|\__|_|\___/|_| |_|

                    📊 15 tests | 🏷️ regression, auth
```

______________________________________________________________________

#### Preset 4: `suite_footer()`

**Purpose:** Suite completion summary. Provides aggregated results with pass/fail counts,
duration, and highlights like slowest test or failure summary.

**Use Cases:**

- Suite-level result aggregation
- Performance analysis (slowest tests)
- Quick pass/fail overview

**Parameters:**

| Parameter      | Type               | Required | Description                 |
| -------------- | ------------------ | -------- | --------------------------- |
| `suite_name`   | `str`              | Yes      | Suite name                  |
| `passed`       | `int`              | Yes      | Number of passed tests      |
| `failed`       | `int`              | Yes      | Number of failed tests      |
| `skipped`      | `int`              | No       | Number of skipped tests     |
| `errors`       | `int`              | No       | Number of error tests       |
| `duration`     | `float`            | No       | Total duration in seconds   |
| `slowest_test` | `tuple[str,float]` | No       | (test_name, duration) tuple |
| `failures`     | `list[str]`        | No       | List of failed test names   |
| `console`      | `Console`          | No       | Custom Console instance     |

```python
from styledconsole.presets import suite_footer

suite_footer(
    suite_name="Authentication Suite",
    passed=12,
    failed=2,
    skipped=1,
    duration=45.7,
    slowest_test=("Complex login flow", 8.2),
    failures=["Login with expired token", "Login with revoked user"]
)
```

**Visualization Variant A - Summary box (default):**

```text
┏━━━━━━━━━━━━━━━━━━ 📊 SUITE COMPLETE ━━━━━━━━━━━━━━━━━━━┓
┃ Authentication Suite                                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ✅ Passed: 12    ❌ Failed: 2    ⏭️  Skipped: 1         ┃
┃ ⏱️  Duration: 45.7s                                     ┃
┃ 🐢 Slowest: Complex login flow (8.2s)                  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ❌ Failed tests:                                       ┃
┃    • Login with expired token                          ┃
┃    • Login with revoked user                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Visualization Variant B - Compact inline:**

```text
📊 Authentication Suite: ✅ 12 passed | ❌ 2 failed | ⏭️ 1 skipped | ⏱️ 45.7s
```

**Visualization Variant C - Progress bar style:**

```text
Authentication Suite                                    45.7s
████████████████████████░░░░  80% passed (12/15)
✅ 12 passed  ❌ 2 failed  ⏭️ 1 skipped
```

______________________________________________________________________

#### Preset 5: `step()`

**Purpose:** Numbered test step with status indicator. Tracks individual actions within
a test for debugging and documentation. Supports nesting for sub-steps.

**Use Cases:**

- Step-by-step test execution logging
- Debugging test failures at specific steps
- BDD/Gherkin-style step visualization
- Nested action tracking

**Parameters:**

| Parameter     | Type                                                       | Required | Description              |
| ------------- | ---------------------------------------------------------- | -------- | ------------------------ |
| `number`      | `int`                                                      | Yes      | Step number              |
| `description` | `str`                                                      | Yes      | Step description         |
| `status`      | `Literal["pending","running","passed","failed","skipped"]` | No       | Step status              |
| `details`     | `str`                                                      | No       | Additional details       |
| `duration`    | `float`                                                    | No       | Step duration in seconds |
| `level`       | `int`                                                      | No       | Nesting level (0=root)   |
| `console`     | `Console`                                                  | No       | Custom Console instance  |

```python
from styledconsole.presets import step

step(1, "Navigate to login page", status="passed", duration=0.5)
step(2, "Enter username", status="passed", duration=0.1)
step(3, "Enter password", status="passed", duration=0.1)
step(4, "Click submit button", status="running")
step(5, "Verify dashboard loads", status="pending")
```

**Visualization Variant A - Checklist (default):**

```text
  ✅ 1. Navigate to login page                           0.5s
  ✅ 2. Enter username                                   0.1s
  ✅ 3. Enter password                                   0.1s
  🔄 4. Click submit button                              ...
  ⏳ 5. Verify dashboard loads
```

**Visualization Variant B - Detailed with frame:**

```text
╭─ Step 1 ─────────────────────────────────────────────────╮
│ ✅ Navigate to login page                                │
│    Duration: 0.5s                                        │
│    URL: https://example.com/login                        │
╰──────────────────────────────────────────────────────────╯
```

**Visualization Variant C - BDD/Gherkin style:**

```text
  Given I am on the login page                           ✅
   When I enter valid credentials                        ✅
    And I click the submit button                        🔄
   Then I should see the dashboard                       ⏳
```

**Visualization Variant D - Nested steps:**

```text
  ✅ 1. Login to application
     ├─ ✅ 1.1. Open browser
     ├─ ✅ 1.2. Navigate to URL
     └─ ✅ 1.3. Enter credentials
  🔄 2. Perform search
     ├─ ✅ 2.1. Click search box
     └─ 🔄 2.2. Enter query
```

______________________________________________________________________

### v0.11.0: Assertions & Validation Presets

**Theme:** Test assertions and data validation visualization
**Target:** Q1 2026
**Status:** PLANNED

#### Preset 1: `assertion_result()`

**Purpose:** Side-by-side comparison with diff highlighting. Displays expected vs actual
values with visual emphasis on the difference. Color-coded for pass/fail status.

**Use Cases:**

- Detailed assertion failure reports
- Value comparison debugging
- API response validation display
- Data verification logging

**Parameters:**

| Parameter  | Type      | Required | Description                                 |
| ---------- | --------- | -------- | ------------------------------------------- |
| `label`    | `str`     | Yes      | Description of what's being asserted        |
| `expected` | `Any`     | Yes      | Expected value                              |
| `actual`   | `Any`     | Yes      | Actual value received                       |
| `passed`   | `bool`    | Yes      | Whether assertion passed                    |
| `operator` | `str`     | No       | Comparison operator (equals, contains, etc) |
| `diff`     | `bool`    | No       | Show character-level diff for strings       |
| `console`  | `Console` | No       | Custom Console instance                     |

```python
from styledconsole.presets import assertion_result

# Failed assertion
assertion_result(
    label="Response status code",
    expected=200,
    actual=404,
    passed=False,
    operator="equals"
)

# Passed assertion
assertion_result(
    label="User email format",
    expected="user@example.com",
    actual="user@example.com",
    passed=True
)

# String diff
assertion_result(
    label="Response message",
    expected="Login successful",
    actual="Login failed",
    passed=False,
    diff=True
)
```

**Visualization Variant A - Framed comparison (default):**

```text
╭─────────────────── ❌ ASSERTION FAILED ───────────────────╮
│ Response status code                                      │
├───────────────────────────────────────────────────────────┤
│ Expected: 200                                             │
│ Actual:   404                                             │
│ Operator: equals                                          │
╰───────────────────────────────────────────────────────────╯
```

```text
╭─────────────────── ✅ ASSERTION PASSED ───────────────────╮
│ User email format                                         │
├───────────────────────────────────────────────────────────┤
│ Value: user@example.com                                   │
╰───────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Inline compact:**

```text
❌ Response status code: expected 200, got 404
✅ User email format: user@example.com
```

**Visualization Variant C - Side-by-side with diff:**

```text
╭─────────────────── ❌ ASSERTION FAILED ───────────────────╮
│ Response message                                          │
├─────────────────────┬─────────────────────────────────────┤
│ Expected            │ Actual                              │
├─────────────────────┼─────────────────────────────────────┤
│ Login successful    │ Login failed                        │
│       ^^^^^^^^^^    │       ^^^^^^                        │
╰─────────────────────┴─────────────────────────────────────╯
```

**Visualization Variant D - JSON/object comparison:**

```text
╭───────────────── ❌ ASSERTION FAILED ─────────────────╮
│ API Response Body                                     │
├───────────────────────────────────────────────────────┤
│ Expected:                                             │
│   {                                                   │
│     "status": "ok",                                   │
│     "count": 5                                        │
│   }                                                   │
├───────────────────────────────────────────────────────┤
│ Actual:                                               │
│   {                                                   │
│     "status": "error",   ← DIFFERENT                  │
│     "count": 3           ← DIFFERENT                  │
│   }                                                   │
╰───────────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 2: `validation_table()`

**Purpose:** Table of validation checks with ✅/❌ status. Displays multiple validation
rules in a structured table format with pass/fail indicators.

**Use Cases:**

- Multi-field form validation results
- API response multi-check validation
- Configuration validation reports
- Data quality check summaries

**Parameters:**

| Parameter  | Type                    | Required | Description               |
| ---------- | ----------------------- | -------- | ------------------------- |
| `checks`   | `list[ValidationCheck]` | Yes      | List of validation checks |
| `title`    | `str`                   | No       | Table title               |
| `show_all` | `bool`                  | No       | Show passed checks too    |
| `console`  | `Console`               | No       | Custom Console instance   |

**ValidationCheck TypedDict:**

```python
class ValidationCheck(TypedDict):
    check: str           # Description of the check
    passed: bool         # Whether check passed
    actual: str | None   # Actual value (for failures)
    expected: str | None # Expected value (for failures)
```

```python
from styledconsole.presets import validation_table

validation_table(
    title="API Response Validation",
    checks=[
        {"check": "Status code is 200", "passed": True},
        {"check": "Response time < 500ms", "passed": True, "actual": "234ms"},
        {"check": "Body contains 'success'", "passed": False, "actual": "error", "expected": "success"},
        {"check": "Headers include auth token", "passed": True},
        {"check": "Content-Type is JSON", "passed": True},
    ]
)
```

**Visualization Variant A - Full table (default):**

```text
╭────────────────── 📋 API Response Validation ──────────────────╮
│                                                                │
│  Status  │ Check                      │ Details                │
│ ─────────┼────────────────────────────┼─────────────────────── │
│    ✅    │ Status code is 200         │                        │
│    ✅    │ Response time < 500ms      │ 234ms                  │
│    ❌    │ Body contains 'success'    │ got: error             │
│    ✅    │ Headers include auth token │                        │
│    ✅    │ Content-Type is JSON       │                        │
│ ─────────┴────────────────────────────┴─────────────────────── │
│  Summary: 4/5 passed (80%)                                     │
╰────────────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Checklist style:**

```text
📋 API Response Validation
  ✅ Status code is 200
  ✅ Response time < 500ms (234ms)
  ❌ Body contains 'success' → got: error
  ✅ Headers include auth token
  ✅ Content-Type is JSON

Result: 4/5 passed (80%)
```

**Visualization Variant C - Failures only:**

```text
╭─────────────── ❌ Validation Failures ────────────────╮
│ Body contains 'success'                               │
│   Expected: success                                   │
│   Actual:   error                                     │
╰───────────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 3: `diff_view()`

**Purpose:** Visual diff for string/data comparisons. Shows line-by-line or character-level
differences between expected and actual values with color highlighting.

**Use Cases:**

- JSON/XML response comparison
- Configuration file diff
- Text content verification
- Multi-line string comparison

**Parameters:**

| Parameter  | Type                           | Required | Description                  |
| ---------- | ------------------------------ | -------- | ---------------------------- |
| `expected` | `str`                          | Yes      | Expected content             |
| `actual`   | `str`                          | Yes      | Actual content               |
| `format`   | `Literal["text","json","xml"]` | No       | Content format for parsing   |
| `context`  | `int`                          | No       | Lines of context around diff |
| `title`    | `str`                          | No       | Diff title                   |
| `console`  | `Console`                      | No       | Custom Console instance      |

```python
from styledconsole.presets import diff_view

# JSON diff
diff_view(
    expected='{"status": "ok", "count": 5, "items": [1, 2, 3]}',
    actual='{"status": "error", "count": 3, "items": [1, 2]}',
    format="json",
    title="API Response Diff"
)

# Text diff
diff_view(
    expected="Line 1\nLine 2\nLine 3",
    actual="Line 1\nModified Line 2\nLine 3\nLine 4",
    format="text"
)
```

**Visualization Variant A - Unified diff (default):**

```text
╭─────────────────── 📝 API Response Diff ───────────────────╮
│                                                            │
│ @@ -1,5 +1,5 @@                                            │
│  {                                                         │
│ -  "status": "ok",                                         │
│ +  "status": "error",                                      │
│ -  "count": 5,                                             │
│ +  "count": 3,                                             │
│ -  "items": [1, 2, 3]                                      │
│ +  "items": [1, 2]                                         │
│  }                                                         │
│                                                            │
╰────────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Side-by-side:**

```text
╭─────────────── Expected ───────────────┬─────────────── Actual ─────────────────╮
│ {                                      │ {                                      │
│   "status": "ok",                      │   "status": "error",         ← CHANGED │
│   "count": 5,                          │   "count": 3,                ← CHANGED │
│   "items": [1, 2, 3]                   │   "items": [1, 2]            ← CHANGED │
│ }                                      │ }                                      │
╰────────────────────────────────────────┴────────────────────────────────────────╯
```

**Visualization Variant C - Inline highlights:**

```text
╭─────────────────────── Diff View ───────────────────────╮
│ Line 1: {                                               │
│ Line 2: "status": "[-ok-]{+error+}",                    │
│ Line 3: "count": [-5-]{+3+},                            │
│ Line 4: "items": [1, 2[-,3-]]                           │
│ Line 5: }                                               │
╰─────────────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 4: `assertion_summary()`

**Purpose:** Summary of all assertions in a test. Provides aggregate view of assertion
results with quick access to failure details.

**Use Cases:**

- End-of-test assertion overview
- Multiple soft assertion collection
- Test quality metrics
- Failure triage support

**Parameters:**

| Parameter    | Type                    | Required | Description              |
| ------------ | ----------------------- | -------- | ------------------------ |
| `total`      | `int`                   | Yes      | Total assertion count    |
| `passed`     | `int`                   | Yes      | Passed assertion count   |
| `failed`     | `int`                   | Yes      | Failed assertion count   |
| `assertions` | `list[AssertionDetail]` | No       | Failed assertion details |
| `test_name`  | `str`                   | No       | Test name for context    |
| `console`    | `Console`               | No       | Custom Console instance  |

```python
from styledconsole.presets import assertion_summary

assertion_summary(
    test_name="User Registration Flow",
    total=10,
    passed=8,
    failed=2,
    assertions=[
        {"name": "Email validation", "expected": "valid", "actual": "invalid format", "passed": False},
        {"name": "Password strength", "expected": ">=8 chars", "actual": "6 chars", "passed": False},
    ]
)
```

**Visualization Variant A - Summary box (default):**

```text
╭─────────────── 📊 Assertion Summary ────────────────╮
│ User Registration Flow                              │
├─────────────────────────────────────────────────────┤
│ Total: 10  │  ✅ Passed: 8  │  ❌ Failed: 2         │
│ ████████░░░░░░░░░░░░░░░░░░░░  80% pass rate        │
├─────────────────────────────────────────────────────┤
│ ❌ Failed Assertions:                               │
│   1. Email validation                               │
│      Expected: valid                                │
│      Actual: invalid format                         │
│   2. Password strength                              │
│      Expected: >=8 chars                            │
│      Actual: 6 chars                                │
╰─────────────────────────────────────────────────────╯
```

**Visualization Variant B - Compact:**

```text
📊 Assertions: 8/10 passed (80%) - 2 failures
   ❌ Email validation: expected valid, got invalid format
   ❌ Password strength: expected >=8 chars, got 6 chars
```

**Visualization Variant C - Visual bar:**

```text
╭─────────────────────────────────────────────────────╮
│ User Registration Flow - Assertions                 │
│ ████████████████░░░░  80%  (8 passed / 2 failed)    │
│                                                     │
│ ❌ Email validation ──────────────── invalid format │
│ ❌ Password strength ─────────────── 6 chars        │
╰─────────────────────────────────────────────────────╯
```

______________________________________________________________________

### v0.12.0: Data & API Presets

**Theme:** Data inspection and API response visualization
**Target:** Q2 2026
**Status:** PLANNED

#### Preset 1: `data_snapshot()`

**Purpose:** Pretty-print JSON/dict/list with styled frame. Provides formatted display
of complex data structures for debugging and logging purposes.

**Use Cases:**

- Debugging API responses
- Logging request/response payloads
- Displaying configuration objects
- Snapshot testing visualization

**Parameters:**

| Parameter   | Type                            | Required | Description                  |
| ----------- | ------------------------------- | -------- | ---------------------------- |
| `name`      | `str`                           | Yes      | Snapshot label/title         |
| `data`      | `Any`                           | Yes      | Data to display              |
| `format`    | `Literal["json","yaml","auto"]` | No       | Output format                |
| `max_depth` | `int`                           | No       | Max nesting depth to display |
| `collapsed` | `bool`                          | No       | Show collapsed view          |
| `highlight` | `list[str]`                     | No       | Keys to highlight            |
| `console`   | `Console`                       | No       | Custom Console instance      |

```python
from styledconsole.presets import data_snapshot

# Simple snapshot
data_snapshot(
    name="User Response",
    data={"id": 123, "name": "John", "roles": ["admin", "user"]}
)

# With highlighting
data_snapshot(
    name="API Error",
    data={"status": "error", "code": 500, "message": "Internal error"},
    highlight=["status", "code"]
)

# Nested data
data_snapshot(
    name="Configuration",
    data={
        "database": {"host": "localhost", "port": 5432},
        "cache": {"enabled": True, "ttl": 3600},
        "features": ["auth", "logging", "metrics"]
    },
    max_depth=2
)
```

**Visualization Variant A - Framed JSON (default):**

```text
╭──────────────────── 📦 User Response ─────────────────────╮
│ {                                                         │
│   "id": 123,                                              │
│   "name": "John",                                         │
│   "roles": [                                              │
│     "admin",                                              │
│     "user"                                                │
│   ]                                                       │
│ }                                                         │
╰───────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Highlighted keys:**

```text
╭──────────────────── ⚠️ API Error ──────────────────────╮
│ {                                                      │
│   "status": "error",      ← HIGHLIGHTED                │
│   "code": 500,            ← HIGHLIGHTED                │
│   "message": "Internal error"                          │
│ }                                                      │
╰────────────────────────────────────────────────────────╯
```

**Visualization Variant C - Tree view:**

```text
📦 Configuration
├── database
│   ├── host: "localhost"
│   └── port: 5432
├── cache
│   ├── enabled: true
│   └── ttl: 3600
└── features
    ├── [0]: "auth"
    ├── [1]: "logging"
    └── [2]: "metrics"
```

**Visualization Variant D - Collapsed:**

```text
╭─ 📦 User Response ────────────────────────────────────╮
│ {id: 123, name: "John", roles: [...2 items]}          │
╰───────────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 2: `api_response()`

**Purpose:** HTTP response visualization. Displays complete API response including
status, headers, body, and timing in a structured format.

**Use Cases:**

- API testing result display
- Request/response debugging
- Integration test logging
- API documentation examples

**Parameters:**

| Parameter      | Type            | Required | Description                  |
| -------------- | --------------- | -------- | ---------------------------- |
| `method`       | `str`           | Yes      | HTTP method (GET, POST, etc) |
| `url`          | `str`           | Yes      | Request URL                  |
| `status_code`  | `int`           | Yes      | Response status code         |
| `duration`     | `float`         | No       | Response time in seconds     |
| `headers`      | `dict[str,str]` | No       | Response headers             |
| `body`         | `Any`           | No       | Response body                |
| `size`         | `int`           | No       | Response size in bytes       |
| `show_headers` | `bool`          | No       | Display headers section      |
| `console`      | `Console`       | No       | Custom Console instance      |

```python
from styledconsole.presets import api_response

# Successful response
api_response(
    method="POST",
    url="/api/v1/users",
    status_code=201,
    duration=0.234,
    headers={"Content-Type": "application/json", "X-Request-Id": "abc123"},
    body={"id": 456, "created": True}
)

# Error response
api_response(
    method="GET",
    url="/api/v1/users/999",
    status_code=404,
    duration=0.045,
    body={"error": "User not found"}
)
```

**Visualization Variant A - Full detail (default):**

```text
┏━━━━━━━━━━━━━━━━━━━━━━━ 🌐 API Response ━━━━━━━━━━━━━━━━━━━━━━━┓
┃ POST /api/v1/users                                            ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ✅ 201 Created                              ⏱️ 234ms          ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📋 Headers:                                                   ┃
┃   Content-Type: application/json                              ┃
┃   X-Request-Id: abc123                                        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📦 Body:                                                      ┃
┃   {                                                           ┃
┃     "id": 456,                                                ┃
┃     "created": true                                           ┃
┃   }                                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Visualization Variant B - Compact:**

```text
✅ POST /api/v1/users → 201 Created (234ms)
   Body: {"id": 456, "created": true}
```

**Visualization Variant C - Error emphasis:**

```text
┏━━━━━━━━━━━━━━━━━ ❌ API Error Response ━━━━━━━━━━━━━━━━━┓
┃ GET /api/v1/users/999                                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ❌ 404 Not Found                            ⏱️ 45ms     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📦 Error:                                               ┃
┃   {                                                     ┃
┃     "error": "User not found"                           ┃
┃   }                                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Visualization Variant D - cURL style:**

```text
< HTTP/1.1 201 Created
< Content-Type: application/json
< X-Request-Id: abc123
<
< {"id": 456, "created": true}
<
< ⏱️ 234ms
```

______________________________________________________________________

#### Preset 3: `api_request()`

**Purpose:** HTTP request visualization (before sending). Shows outgoing request
details for debugging and logging.

**Use Cases:**

- Pre-request logging
- Request debugging
- API call documentation
- cURL command generation

**Parameters:**

| Parameter | Type            | Required | Description                  |
| --------- | --------------- | -------- | ---------------------------- |
| `method`  | `str`           | Yes      | HTTP method (GET, POST, etc) |
| `url`     | `str`           | Yes      | Request URL                  |
| `headers` | `dict[str,str]` | No       | Request headers              |
| `body`    | `Any`           | No       | Request body                 |
| `params`  | `dict[str,str]` | No       | Query parameters             |
| `timeout` | `float`         | No       | Request timeout              |
| `console` | `Console`       | No       | Custom Console instance      |

```python
from styledconsole.presets import api_request

api_request(
    method="POST",
    url="https://api.example.com/users",
    headers={
        "Authorization": "Bearer ***",
        "Content-Type": "application/json"
    },
    body={"name": "John", "email": "john@example.com"}
)
```

**Visualization Variant A - Framed (default):**

```text
╭────────────────────── 📤 API Request ──────────────────────╮
│ POST https://api.example.com/users                         │
├────────────────────────────────────────────────────────────┤
│ 📋 Headers:                                                │
│   Authorization: Bearer ***                                │
│   Content-Type: application/json                           │
├────────────────────────────────────────────────────────────┤
│ 📦 Body:                                                   │
│   {                                                        │
│     "name": "John",                                        │
│     "email": "john@example.com"                            │
│   }                                                        │
╰────────────────────────────────────────────────────────────╯
```

**Visualization Variant B - cURL command:**

```text
╭─────────────────── 📤 API Request (cURL) ───────────────────╮
│ curl -X POST 'https://api.example.com/users' \              │
│   -H 'Authorization: Bearer ***' \                          │
│   -H 'Content-Type: application/json' \                     │
│   -d '{"name": "John", "email": "john@example.com"}'        │
╰─────────────────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 4: `db_result()`

**Purpose:** Database query result as styled table. Displays SQL query and results
in a formatted table with row count and execution time.

**Use Cases:**

- Database query logging
- Data verification display
- Query result debugging
- Migration/seeding output

**Parameters:**

| Parameter   | Type          | Required | Description                  |
| ----------- | ------------- | -------- | ---------------------------- |
| `query`     | `str`         | No       | SQL query executed           |
| `columns`   | `list[str]`   | Yes      | Column names                 |
| `rows`      | `list[tuple]` | Yes      | Result rows                  |
| `duration`  | `float`       | No       | Query duration in seconds    |
| `row_count` | `int`         | No       | Total row count (if limited) |
| `title`     | `str`         | No       | Custom title                 |
| `console`   | `Console`     | No       | Custom Console instance      |

```python
from styledconsole.presets import db_result

db_result(
    query="SELECT id, name, email FROM users WHERE active = true LIMIT 3",
    columns=["id", "name", "email"],
    rows=[
        (1, "Alice", "alice@example.com"),
        (2, "Bob", "bob@example.com"),
        (3, "Charlie", "charlie@example.com"),
    ],
    duration=0.045,
    row_count=3
)
```

**Visualization Variant A - Full table (default):**

```text
╭────────────────────── 🗃️ Query Result ──────────────────────╮
│ SELECT id, name, email FROM users WHERE active = true LIMIT 3│
├──────────────────────────────────────────────────────────────┤
│  id  │  name     │  email                                   │
│ ─────┼───────────┼───────────────────────────────────────── │
│  1   │  Alice    │  alice@example.com                       │
│  2   │  Bob      │  bob@example.com                         │
│  3   │  Charlie  │  charlie@example.com                     │
├──────────────────────────────────────────────────────────────┤
│ ⏱️ 45ms  │  📊 3 rows                                        │
╰──────────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Compact:**

```text
🗃️ Query: SELECT id, name, email FROM users...
┌────┬─────────┬───────────────────────┐
│ id │ name    │ email                 │
├────┼─────────┼───────────────────────┤
│ 1  │ Alice   │ alice@example.com     │
│ 2  │ Bob     │ bob@example.com       │
│ 3  │ Charlie │ charlie@example.com   │
└────┴─────────┴───────────────────────┘
3 rows (45ms)
```

**Visualization Variant C - Vertical (single row):**

```text
╭────────── 🗃️ User #1 ──────────╮
│ id:    1                       │
│ name:  Alice                   │
│ email: alice@example.com       │
╰────────────────────────────────╯
```

______________________________________________________________________

#### Preset 5: `timing_breakdown()`

**Purpose:** Bar chart of step durations. Visualizes time spent in each phase
of a test or operation for performance analysis.

**Use Cases:**

- Test step timing analysis
- Performance bottleneck identification
- Execution time breakdown
- SLA compliance checking

**Parameters:**

| Parameter   | Type               | Required | Description                  |
| ----------- | ------------------ | -------- | ---------------------------- |
| `timings`   | `dict[str, float]` | Yes      | Step name → duration mapping |
| `title`     | `str`              | No       | Chart title                  |
| `unit`      | `str`              | No       | Time unit (s, ms)            |
| `threshold` | `float`            | No       | Slow threshold to highlight  |
| `sort`      | `bool`             | No       | Sort by duration             |
| `console`   | `Console`          | No       | Custom Console instance      |

```python
from styledconsole.presets import timing_breakdown

timing_breakdown(
    timings={
        "Setup": 1.2,
        "Login": 2.5,
        "Navigate": 0.8,
        "Submit form": 3.1,
        "Verify": 1.5,
        "Teardown": 0.4,
    },
    title="Test Execution Timing",
    threshold=2.0  # Highlight steps > 2s
)
```

**Visualization Variant A - Horizontal bars (default):**

```text
╭────────────────── ⏱️ Test Execution Timing ──────────────────╮
│                                                              │
│ Setup       ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1.2s   │
│ Login       █████████████░░░░░░░░░░░░░░░░░░░░░░░░░░  2.5s ⚠️│
│ Navigate    █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0.8s   │
│ Submit form ████████████████░░░░░░░░░░░░░░░░░░░░░░░  3.1s ⚠️│
│ Verify      ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  1.5s   │
│ Teardown    ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0.4s   │
│                                                              │
│ Total: 9.5s  │  Slowest: Submit form (3.1s)                  │
╰──────────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Sorted with percentages:**

```text
╭────────────── ⏱️ Timing Breakdown ──────────────╮
│                                                 │
│ Submit form  ████████████████████  3.1s (33%)  │
│ Login        ████████████████░░░░  2.5s (26%)  │
│ Verify       ██████████░░░░░░░░░░  1.5s (16%)  │
│ Setup        ████████░░░░░░░░░░░░  1.2s (13%)  │
│ Navigate     █████░░░░░░░░░░░░░░░  0.8s  (8%)  │
│ Teardown     ███░░░░░░░░░░░░░░░░░  0.4s  (4%)  │
│                                                 │
│ Total: 9.5s                                     │
╰─────────────────────────────────────────────────╯
```

**Visualization Variant C - Inline sparkline:**

```text
⏱️ Timing: Setup(1.2) → Login(2.5⚠️) → Navigate(0.8) → Submit(3.1⚠️) → Verify(1.5) → Teardown(0.4)
   Total: 9.5s | ▁▃▁▅▂▁
```

______________________________________________________________________

#### Preset 6: `performance_comparison()`

**Purpose:** Before/after with % change. Compares performance metrics between
baseline and current values with visual indicators.

**Use Cases:**

- Performance regression detection
- Optimization verification
- A/B testing results
- Benchmark comparisons

**Parameters:**

| Parameter         | Type      | Required | Description                   |
| ----------------- | --------- | -------- | ----------------------------- |
| `metric`          | `str`     | Yes      | Metric name                   |
| `baseline`        | `float`   | Yes      | Baseline/previous value       |
| `current`         | `float`   | Yes      | Current/new value             |
| `unit`            | `str`     | No       | Value unit (ms, s, MB, etc)   |
| `threshold`       | `float`   | No       | Acceptable threshold          |
| `lower_is_better` | `bool`    | No       | Lower values are improvements |
| `console`         | `Console` | No       | Custom Console instance       |

```python
from styledconsole.presets import performance_comparison

# Improvement
performance_comparison(
    metric="Response Time",
    baseline=250,
    current=180,
    unit="ms",
    threshold=200,
    lower_is_better=True
)

# Regression
performance_comparison(
    metric="Memory Usage",
    baseline=512,
    current=768,
    unit="MB",
    lower_is_better=True
)
```

**Visualization Variant A - Comparison box (default):**

```text
╭──────────────── 📊 Performance Comparison ────────────────╮
│ Response Time                                             │
├───────────────────────────────────────────────────────────┤
│ Baseline:  250ms                                          │
│ Current:   180ms                                          │
│ Change:    -70ms (↓ 28%)                                  │
├───────────────────────────────────────────────────────────┤
│ ✅ IMPROVED - Under threshold (200ms)                     │
╰───────────────────────────────────────────────────────────╯
```

```text
╭──────────────── 📊 Performance Comparison ────────────────╮
│ Memory Usage                                              │
├───────────────────────────────────────────────────────────┤
│ Baseline:  512MB                                          │
│ Current:   768MB                                          │
│ Change:    +256MB (↑ 50%)                                 │
├───────────────────────────────────────────────────────────┤
│ ⚠️ REGRESSION - Memory increased significantly            │
╰───────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Inline:**

```text
📊 Response Time: 250ms → 180ms (↓ 28%) ✅ IMPROVED
📊 Memory Usage: 512MB → 768MB (↑ 50%) ⚠️ REGRESSION
```

**Visualization Variant C - Visual scale:**

```text
╭─────────── Response Time ───────────╮
│ Baseline ████████████████████  250ms│
│ Current  ██████████████░░░░░░  180ms│
│          ↓ 28% improvement          │
╰─────────────────────────────────────╯
```

______________________________________________________________________

### v0.13.0: CI/CD & Error Reporting Presets

**Theme:** CI/CD integration and error visualization
**Target:** Q2 2026
**Status:** PLANNED

#### Preset 1: `failure_detail()`

**Purpose:** Rich failure report with comprehensive error information. Displays
test failure with error message, stack trace, screenshots, and relevant logs.

**Use Cases:**

- Detailed failure investigation
- Bug report generation
- CI/CD failure notifications
- Test result archival

**Parameters:**

| Parameter    | Type        | Required | Description                       |
| ------------ | ----------- | -------- | --------------------------------- |
| `test`       | `str`       | Yes      | Test name                         |
| `error`      | `str`       | Yes      | Error message                     |
| `stacktrace` | `str`       | No       | Full stack trace                  |
| `screenshot` | `str`       | No       | Path to screenshot file           |
| `logs`       | `list[str]` | No       | Relevant log lines                |
| `duration`   | `float`     | No       | Test duration                     |
| `context`    | `dict`      | No       | Additional context (browser, etc) |
| `console`    | `Console`   | No       | Custom Console instance           |

```python
from styledconsole.presets import failure_detail

failure_detail(
    test="Login with invalid password",
    error="AssertionError: Expected 'Welcome' but got 'Invalid credentials'",
    stacktrace='''Traceback (most recent call last):
  File "test_login.py", line 45, in test_invalid_password
    assert "Welcome" in page.text
AssertionError: Expected 'Welcome' but got 'Invalid credentials' ''',
    screenshot="/screenshots/login_failure_001.png",
    logs=[
        "[INFO] 10:23:45 - Navigating to login page",
        "[INFO] 10:23:46 - Entering username: testuser",
        "[INFO] 10:23:46 - Entering password: ****",
        "[INFO] 10:23:47 - Clicking submit button",
        "[ERROR] 10:23:48 - Login failed: Invalid credentials"
    ],
    duration=3.2,
    context={"browser": "Chrome 119", "viewport": "1920x1080"}
)
```

**Visualization Variant A - Full detail (default):**

```text
┏━━━━━━━━━━━━━━━━━━━━━━━ ❌ TEST FAILURE ━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Login with invalid password                                   ┃
┃ ⏱️ 3.2s | 🌐 Chrome 119 | 📐 1920x1080                         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 💥 Error:                                                     ┃
┃ AssertionError: Expected 'Welcome' but got 'Invalid           ┃
┃ credentials'                                                  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📜 Stack Trace:                                               ┃
┃   File "test_login.py", line 45, in test_invalid_password     ┃
┃     assert "Welcome" in page.text                             ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📋 Logs:                                                      ┃
┃   [INFO]  10:23:45 - Navigating to login page                 ┃
┃   [INFO]  10:23:46 - Entering username: testuser              ┃
┃   [INFO]  10:23:46 - Entering password: ****                  ┃
┃   [INFO]  10:23:47 - Clicking submit button                   ┃
┃   [ERROR] 10:23:48 - Login failed: Invalid credentials        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 📸 Screenshot: /screenshots/login_failure_001.png             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Visualization Variant B - Compact:**

```text
❌ Login with invalid password (3.2s)
   Error: AssertionError: Expected 'Welcome' but got 'Invalid credentials'
   File: test_login.py:45
   📸 Screenshot saved
```

**Visualization Variant C - Collapsible sections:**

```text
╭─────────────── ❌ TEST FAILURE ───────────────╮
│ Login with invalid password                   │
├───────────────────────────────────────────────┤
│ 💥 Error: AssertionError: Expected 'Welcome'  │
│    but got 'Invalid credentials'              │
├───────────────────────────────────────────────┤
│ ▶ Stack Trace (click to expand)               │
│ ▶ Logs (5 lines)                              │
│ ▶ Screenshot                                  │
╰───────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 2: `retry_status()`

**Purpose:** Retry progress indicator. Shows current retry attempt with wait
time and last error for transient failure handling.

**Use Cases:**

- Flaky test retry visualization
- Network retry progress
- Polling operation status
- Recovery attempt tracking

**Parameters:**

| Parameter      | Type      | Required | Description                 |
| -------------- | --------- | -------- | --------------------------- |
| `attempt`      | `int`     | Yes      | Current attempt number      |
| `max_attempts` | `int`     | Yes      | Maximum retry attempts      |
| `last_error`   | `str`     | No       | Last error message          |
| `wait_time`    | `float`   | No       | Wait time before next retry |
| `operation`    | `str`     | No       | Operation being retried     |
| `console`      | `Console` | No       | Custom Console instance     |

```python
from styledconsole.presets import retry_status

# During retry
retry_status(
    attempt=2,
    max_attempts=3,
    last_error="Connection timeout after 30s",
    wait_time=5,
    operation="Database connection"
)

# Final failure
retry_status(
    attempt=3,
    max_attempts=3,
    last_error="Connection refused",
    operation="Database connection"
)
```

**Visualization Variant A - Progress box (default):**

```text
╭────────────────── 🔄 RETRY 2/3 ──────────────────╮
│ Database connection                              │
├──────────────────────────────────────────────────┤
│ ⚠️ Last error: Connection timeout after 30s      │
│ ⏳ Waiting 5s before next attempt...             │
│                                                  │
│ Progress: ██████████░░░░░  2/3 attempts          │
╰──────────────────────────────────────────────────╯
```

**Visualization Variant B - Inline:**

```text
🔄 Retry 2/3: Database connection - waiting 5s (last: Connection timeout)
```

**Visualization Variant C - Final failure:**

```text
╭────────────────── ❌ RETRY EXHAUSTED ──────────────────╮
│ Database connection                                    │
├────────────────────────────────────────────────────────┤
│ ❌ All 3 attempts failed                               │
│ 💥 Final error: Connection refused                     │
│                                                        │
│ Attempts: ██████████████████  3/3 (all failed)         │
╰────────────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 3: `flaky_test_alert()`

**Purpose:** Flaky test warning with history. Identifies tests with inconsistent
results and provides actionable recommendations.

**Use Cases:**

- Flaky test detection and alerting
- Test stability monitoring
- Quality gate decisions
- Test maintenance prioritization

**Parameters:**

| Parameter        | Type        | Required | Description              |
| ---------------- | ----------- | -------- | ------------------------ |
| `name`           | `str`       | Yes      | Test name                |
| `pass_rate`      | `float`     | Yes      | Pass rate (0.0 to 1.0)   |
| `recent_results` | `list[str]` | No       | Recent PASS/FAIL history |
| `recommendation` | `str`       | No       | Suggested fix            |
| `first_seen`     | `str`       | No       | When flakiness started   |
| `failure_types`  | `list[str]` | No       | Types of failures seen   |
| `console`        | `Console`   | No       | Custom Console instance  |

```python
from styledconsole.presets import flaky_test_alert

flaky_test_alert(
    name="Async notification test",
    pass_rate=0.6,
    recent_results=["PASS", "FAIL", "PASS", "FAIL", "FAIL"],
    recommendation="Consider adding explicit waits or increasing timeout",
    first_seen="2024-01-15",
    failure_types=["TimeoutError", "ElementNotFound"]
)
```

**Visualization Variant A - Alert box (default):**

```text
╭───────────────── ⚠️ FLAKY TEST DETECTED ─────────────────╮
│ Async notification test                                  │
├──────────────────────────────────────────────────────────┤
│ 📊 Pass Rate: 60% (3/5 recent runs)                      │
│ 📈 History: ✅❌✅❌❌                                    │
│ 📅 First seen: 2024-01-15                                │
├──────────────────────────────────────────────────────────┤
│ 💥 Failure types:                                        │
│   • TimeoutError                                         │
│   • ElementNotFound                                      │
├──────────────────────────────────────────────────────────┤
│ 💡 Recommendation:                                       │
│   Consider adding explicit waits or increasing timeout   │
╰──────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Compact:**

```text
⚠️ FLAKY: Async notification test (60% pass rate)
   History: ✅❌✅❌❌ | Failures: TimeoutError, ElementNotFound
   💡 Consider adding explicit waits
```

**Visualization Variant C - Severity-based:**

```text
╭─ 🔴 HIGH FLAKINESS (60%) ─────────────────────────╮
│ Async notification test                           │
│ ░░░░░░████████████  60%                           │
│                                                   │
│ Recent: ✅ ❌ ✅ ❌ ❌                              │
│ Action: Add explicit waits                        │
╰───────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 4: `build_status()`

**Purpose:** CI job summary. Displays build/job status with commit info,
duration, and quick links.

**Use Cases:**

- CI/CD pipeline status display
- Build notification formatting
- Deployment status reporting
- Job completion summaries

**Parameters:**

| Parameter      | Type                                                 | Required | Description             |
| -------------- | ---------------------------------------------------- | -------- | ----------------------- |
| `job`          | `str`                                                | Yes      | Job/build name          |
| `status`       | `Literal["success","failure","running","cancelled"]` | Yes      | Build status            |
| `commit`       | `str`                                                | No       | Commit SHA (short)      |
| `branch`       | `str`                                                | No       | Branch name             |
| `duration`     | `int`                                                | No       | Duration in seconds     |
| `url`          | `str`                                                | No       | Build URL               |
| `triggered_by` | `str`                                                | No       | Who triggered the build |
| `console`      | `Console`                                            | No       | Custom Console instance |

```python
from styledconsole.presets import build_status

# Successful build
build_status(
    job="Unit Tests",
    status="success",
    commit="abc1234",
    branch="main",
    duration=125,
    url="https://ci.example.com/build/123",
    triggered_by="push"
)

# Failed build
build_status(
    job="Integration Tests",
    status="failure",
    commit="def5678",
    branch="feature/login",
    duration=340
)
```

**Visualization Variant A - Status card (default):**

```text
╭────────────────── ✅ BUILD SUCCESS ──────────────────╮
│ Unit Tests                                           │
├──────────────────────────────────────────────────────┤
│ 🔀 Branch:  main                                     │
│ 📝 Commit:  abc1234                                  │
│ ⏱️  Duration: 2m 5s                                   │
│ 🚀 Trigger: push                                     │
├──────────────────────────────────────────────────────┤
│ 🔗 https://ci.example.com/build/123                  │
╰──────────────────────────────────────────────────────╯
```

```text
╭────────────────── ❌ BUILD FAILURE ──────────────────╮
│ Integration Tests                                    │
├──────────────────────────────────────────────────────┤
│ 🔀 Branch:  feature/login                            │
│ 📝 Commit:  def5678                                  │
│ ⏱️  Duration: 5m 40s                                  │
╰──────────────────────────────────────────────────────╯
```

**Visualization Variant B - Inline:**

```text
✅ Unit Tests (main@abc1234) - 2m 5s
❌ Integration Tests (feature/login@def5678) - 5m 40s
🔄 E2E Tests (main@abc1234) - running...
```

**Visualization Variant C - ASCII badge:**

```text
┌─────────────────────────────────────────┐
│  ██████╗  █████╗ ███████╗███████╗       │
│  ██╔══██╗██╔══██╗██╔════╝██╔════╝       │
│  ██████╔╝███████║███████╗███████╗       │
│  ██╔═══╝ ██╔══██║╚════██║╚════██║       │
│  ██║     ██║  ██║███████║███████║       │
│  ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝       │
│                                         │
│  Unit Tests | main | 2m 5s              │
└─────────────────────────────────────────┘
```

______________________________________________________________________

#### Preset 5: `regression_report()`

**Purpose:** Compare against baseline. Shows test result changes between runs
including new failures, fixes, and persistent issues.

**Use Cases:**

- Pre-merge regression checks
- Release readiness assessment
- Baseline comparison reporting
- Quality trend analysis

**Parameters:**

| Parameter       | Type        | Required | Description                   |
| --------------- | ----------- | -------- | ----------------------------- |
| `new_failures`  | `list[str]` | No       | Tests that newly failed       |
| `fixed`         | `list[str]` | No       | Tests that were fixed         |
| `still_failing` | `list[str]` | No       | Persistent failures           |
| `baseline_run`  | `str`       | No       | Baseline build/run identifier |
| `current_run`   | `str`       | No       | Current build/run identifier  |
| `new_tests`     | `list[str]` | No       | Newly added tests             |
| `removed_tests` | `list[str]` | No       | Removed tests                 |
| `console`       | `Console`   | No       | Custom Console instance       |

```python
from styledconsole.presets import regression_report

regression_report(
    baseline_run="Build #122",
    current_run="Build #123",
    new_failures=["Login timeout test", "Payment validation"],
    fixed=["Cart calculation", "Session handling"],
    still_failing=["Legacy API test"],
    new_tests=["New checkout flow"]
)
```

**Visualization Variant A - Full report (default):**

```text
╭─────────────────── 📊 REGRESSION REPORT ───────────────────╮
│ Comparing: Build #122 → Build #123                         │
├────────────────────────────────────────────────────────────┤
│ ❌ NEW FAILURES (2):                                       │
│   • Login timeout test                                     │
│   • Payment validation                                     │
├────────────────────────────────────────────────────────────┤
│ ✅ FIXED (2):                                              │
│   • Cart calculation                                       │
│   • Session handling                                       │
├────────────────────────────────────────────────────────────┤
│ ⚠️ STILL FAILING (1):                                      │
│   • Legacy API test                                        │
├────────────────────────────────────────────────────────────┤
│ 🆕 NEW TESTS (1):                                          │
│   • New checkout flow                                      │
├────────────────────────────────────────────────────────────┤
│ Summary: +2 failures, +2 fixes, 1 persistent               │
│ Status: ❌ REGRESSION DETECTED                             │
╰────────────────────────────────────────────────────────────╯
```

**Visualization Variant B - Compact delta:**

```text
📊 Build #122 → #123: ❌ +2 failures | ✅ +2 fixes | ⚠️ 1 still failing
   New failures: Login timeout test, Payment validation
```

**Visualization Variant C - Visual diff:**

```text
╭────────────── Regression Summary ──────────────╮
│                                                │
│ ❌ +2  ████░░░░░░  New Failures                │
│ ✅ +2  ████░░░░░░  Fixed                       │
│ ⚠️  1  ██░░░░░░░░  Still Failing               │
│ 🆕 +1  ██░░░░░░░░  New Tests                   │
│                                                │
│ Net change: 0 (2 new failures, 2 fixes)        │
╰────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 6: `coverage_delta()`

**Purpose:** Coverage change visualization. Shows coverage differences between
runs with file-level breakdown.

**Use Cases:**

- PR coverage impact assessment
- Coverage trend monitoring
- Quality gate enforcement
- Code review assistance

**Parameters:**

| Parameter       | Type                 | Required | Description                  |
| --------------- | -------------------- | -------- | ---------------------------- |
| `before`        | `float`              | Yes      | Previous coverage percentage |
| `after`         | `float`              | Yes      | Current coverage percentage  |
| `changed_files` | `list[FileCoverage]` | No       | Per-file coverage changes    |
| `threshold`     | `float`              | No       | Minimum acceptable coverage  |
| `new_lines`     | `int`                | No       | New lines added              |
| `covered_new`   | `int`                | No       | Covered new lines            |
| `console`       | `Console`            | No       | Custom Console instance      |

```python
from styledconsole.presets import coverage_delta

coverage_delta(
    before=82.5,
    after=84.1,
    threshold=80,
    changed_files=[
        {"file": "auth.py", "before": 75, "after": 90},
        {"file": "utils.py", "before": 95, "after": 93},
        {"file": "new_feature.py", "before": 0, "after": 85},
    ],
    new_lines=150,
    covered_new=127
)
```

**Visualization Variant A - Coverage card (default):**

```text
╭────────────────── 📊 COVERAGE DELTA ──────────────────╮
│                                                       │
│ Overall: 82.5% → 84.1% (↑ +1.6%)                     │
│ ████████████████░░░░  84.1%  ✅ Above threshold (80%) │
│                                                       │
├───────────────────────────────────────────────────────┤
│ 📁 Changed Files:                                     │
│                                                       │
│ auth.py          75% → 90%   ↑ +15%  ████████████████│
│ utils.py         95% → 93%   ↓  -2%  ████████████████│
│ new_feature.py    0% → 85%   🆕       █████████████░░░│
│                                                       │
├───────────────────────────────────────────────────────┤
│ New Code: 127/150 lines covered (84.7%)               │
╰───────────────────────────────────────────────────────╯
```

**Visualization Variant B - Compact:**

```text
📊 Coverage: 82.5% → 84.1% (↑ +1.6%) ✅
   auth.py ↑ +15% | utils.py ↓ -2% | new_feature.py 🆕 85%
```

**Visualization Variant C - Threshold focus:**

```text
╭────────── Coverage Gate ──────────╮
│                                   │
│  Threshold: 80%                   │
│  Current:   84.1%                 │
│                                   │
│  ████████████████████░░  84.1%   │
│            ↑                      │
│         Threshold                 │
│                                   │
│  ✅ PASSED (+4.1% above minimum)  │
╰───────────────────────────────────╯
```

______________________________________________________________________

#### Preset 7: `artifact_list()`

**Purpose:** Build artifacts with sizes. Displays downloadable artifacts from
a build with type icons and file sizes.

**Use Cases:**

- Build output summary
- Artifact download listing
- Storage usage reporting
- CI/CD result organization

**Parameters:**

| Parameter    | Type             | Required | Description                 |
| ------------ | ---------------- | -------- | --------------------------- |
| `artifacts`  | `list[Artifact]` | Yes      | List of artifacts           |
| `title`      | `str`            | No       | Section title               |
| `total_size` | `str`            | No       | Total size of all artifacts |
| `build_id`   | `str`            | No       | Build identifier            |
| `console`    | `Console`        | No       | Custom Console instance     |

**Artifact TypedDict:**

```python
class Artifact(TypedDict):
    name: str          # File name
    size: str          # Human-readable size
    type: str          # report, archive, coverage, log, screenshot
    url: str | None    # Download URL
```

```python
from styledconsole.presets import artifact_list

artifact_list(
    title="Build #123 Artifacts",
    artifacts=[
        {"name": "test-report.html", "size": "2.4 MB", "type": "report"},
        {"name": "screenshots.zip", "size": "15.2 MB", "type": "archive"},
        {"name": "coverage.xml", "size": "156 KB", "type": "coverage"},
        {"name": "test.log", "size": "1.1 MB", "type": "log"},
        {"name": "failure_001.png", "size": "245 KB", "type": "screenshot"},
    ],
    total_size="19.1 MB"
)
```

**Visualization Variant A - File list (default):**

```text
╭────────────── 📦 Build #123 Artifacts ──────────────╮
│                                                     │
│ 📊 test-report.html              2.4 MB    report  │
│ 📁 screenshots.zip              15.2 MB    archive │
│ 📈 coverage.xml                  156 KB   coverage │
│ 📜 test.log                       1.1 MB       log │
│ 📸 failure_001.png                245 KB screenshot│
│                                                     │
├─────────────────────────────────────────────────────┤
│ Total: 5 files (19.1 MB)                            │
╰─────────────────────────────────────────────────────╯
```

**Visualization Variant B - Compact:**

```text
📦 Artifacts (5 files, 19.1 MB):
   📊 test-report.html (2.4 MB) | 📁 screenshots.zip (15.2 MB)
   📈 coverage.xml (156 KB) | 📜 test.log (1.1 MB) | 📸 failure_001.png (245 KB)
```

**Visualization Variant C - Grouped by type:**

```text
╭─────────────── 📦 Artifacts ───────────────╮
│                                            │
│ 📊 Reports:                                │
│   └─ test-report.html          2.4 MB     │
│                                            │
│ 📈 Coverage:                               │
│   └─ coverage.xml              156 KB     │
│                                            │
│ 📁 Archives:                               │
│   └─ screenshots.zip          15.2 MB     │
│                                            │
│ 📜 Logs:                                   │
│   └─ test.log                  1.1 MB     │
│                                            │
│ 📸 Screenshots:                            │
│   └─ failure_001.png           245 KB     │
│                                            │
╰────────────────────────────────────────────╯
```

````

______________________________________________________________________

### v0.14.0: Robot Framework Presets

**Theme:** Robot Framework specific reporting
**Target:** Q2 2026
**Status:** PLANNED

> **Design Goal:** Provide specialized presets for Robot Framework test automation
> that match RF's unique keyword-driven paradigm, variable scoping, and reporting
> conventions. These presets understand RF-specific concepts like keyword nesting,
> library imports, and tag-based organization.

______________________________________________________________________

#### Preset 1: `rf_keyword_log()`

**Purpose:** Display Robot Framework keyword execution with documentation, arguments,
nesting levels, timing, and status in a format that mirrors RF's native log structure.

**Use Cases:**

- Custom keyword execution logging in RF listeners
- Debugging keyword flow during test development
- Real-time keyword monitoring in CI/CD console output
- Building custom RF log viewers with terminal output

**Parameters:**

| Parameter   | Type           | Default    | Description                            |
| ----------- | -------------- | ---------- | -------------------------------------- |
| `keyword`   | `str`          | (required) | Keyword name                           |
| `args`      | `list[str]`    | `[]`       | Keyword arguments (mask sensitive)     |
| `doc`       | `str \| None`  | `None`     | Keyword documentation string           |
| `level`     | `int`          | `0`        | Nesting level (0=top, 1=child, etc.)   |
| `status`    | `str`          | `"PASS"`   | Status: PASS, FAIL, SKIP, NOT RUN      |
| `duration`  | `float \| None`| `None`     | Execution time in seconds              |
| `msg`       | `str \| None`  | `None`     | Status message (especially for FAIL)   |
| `console`   | `Console`      | `None`     | Optional Console instance              |

**Example:**

```python
from styledconsole.presets import rf_keyword_log

# Top-level keyword with nested calls
rf_keyword_log(
    keyword="Login To Application",
    args=["admin", "***"],
    doc="Logs into the application with given credentials",
    level=0,
    status="PASS",
    duration=1.2
)

# Nested keywords (called automatically by listener)
rf_keyword_log(keyword="Input Text", args=["id=username", "admin"], level=1, status="PASS")
rf_keyword_log(keyword="Input Text", args=["id=password", "***"], level=1, status="PASS")
rf_keyword_log(keyword="Click Button", args=["id=submit"], level=1, status="PASS")

# Failed keyword with message
rf_keyword_log(
    keyword="Wait Until Element Visible",
    args=["id=dashboard"],
    level=1,
    status="FAIL",
    duration=10.0,
    msg="Element not found within timeout"
)
````

**Visualization Variant A (Indented Tree):**

```text
🔧 Login To Application    admin, ***                    ✅ 1.20s
   📝 Logs into the application with given credentials
   ├─ 🔧 Input Text    id=username, admin               ✅ 0.15s
   ├─ 🔧 Input Text    id=password, ***                 ✅ 0.12s
   ├─ 🔧 Click Button  id=submit                        ✅ 0.08s
   └─ ⏳ Wait Until Element Visible    id=dashboard     ❌ 10.0s
         💬 Element not found within timeout
```

**Visualization Variant B (Compact Timeline):**

```text
[00:01.20] ✅ Login To Application (admin, ***)
  [00:00.15] ✅ Input Text
  [00:00.12] ✅ Input Text
  [00:00.08] ✅ Click Button
  [00:10.00] ❌ Wait Until Element Visible
             └─ Element not found within timeout
```

**Visualization Variant C (Framed Keyword Block):**

```text
╭──────────────────────────────────────────────────────╮
│ 🔧 KEYWORD: Login To Application                     │
├──────────────────────────────────────────────────────┤
│ Arguments: admin, ***                                │
│ Doc: Logs into the application with given...         │
│ Duration: 1.20s                                      │
│ Status: ✅ PASS                                      │
├──────────────────────────────────────────────────────┤
│ Nested Keywords:                                     │
│   ✅ Input Text (id=username, admin)                 │
│   ✅ Input Text (id=password, ***)                   │
│   ✅ Click Button (id=submit)                        │
│   ❌ Wait Until Element Visible (id=dashboard)       │
╰──────────────────────────────────────────────────────╯
```

______________________________________________________________________

#### Preset 2: `rf_library_info()`

**Purpose:** Display information about imported Robot Framework libraries including
version, keyword count, scope, initialization parameters, and documentation links.

**Use Cases:**

- Library audit reports showing which versions are in use
- Documentation generation for test project dependencies
- Debugging library import issues in complex projects
- Suite setup logging to track library configurations

**Parameters:**

| Parameter        | Type          | Default    | Description                   |
| ---------------- | ------------- | ---------- | ----------------------------- |
| `name`           | `str`         | (required) | Library name                  |
| `version`        | `str \| None` | `None`     | Library version               |
| `keywords_count` | `int \| None` | `None`     | Number of keywords in library |
| `scope`          | `str`         | `"TEST"`   | Scope: GLOBAL, SUITE, TEST    |
| `doc_url`        | `str \| None` | `None`     | Documentation URL             |
| `init_args`      | `dict`        | `{}`       | Initialization arguments      |
| `source`         | `str \| None` | `None`     | Source file/module path       |
| `console`        | `Console`     | `None`     | Optional Console instance     |

**Example:**

```python
from styledconsole.presets import rf_library_info

# Standard library info
rf_library_info(
    name="SeleniumLibrary",
    version="6.1.0",
    keywords_count=145,
    scope="GLOBAL",
    doc_url="https://robotframework.org/SeleniumLibrary/",
    init_args={"timeout": "10s", "implicit_wait": "0s"}
)

# Custom library
rf_library_info(
    name="CustomKeywords",
    version="1.2.3",
    keywords_count=25,
    scope="SUITE",
    source="/app/libs/custom_keywords.py"
)
```

**Visualization Variant A (Compact Card):**

```text
╭─ 📚 SeleniumLibrary ─────────────────────────────────╮
│ Version: 6.1.0          Scope: GLOBAL                │
│ Keywords: 145           Source: site-packages/...    │
│ Init: timeout=10s, implicit_wait=0s                  │
│ 🔗 https://robotframework.org/SeleniumLibrary/       │
╰──────────────────────────────────────────────────────╯
```

**Visualization Variant B (Inline Badge):**

```text
📚 SeleniumLibrary v6.1.0 [GLOBAL] 145 keywords
   └─ Init: timeout=10s, implicit_wait=0s
```

**Visualization Variant C (Detailed Table):**

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📚 Library Import Details                            ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Name           │ SeleniumLibrary                     ┃
┃ Version        │ 6.1.0                               ┃
┃ Scope          │ GLOBAL                              ┃
┃ Keywords       │ 145                                 ┃
┃ Init Args      │ timeout=10s, implicit_wait=0s       ┃
┃ Documentation  │ robotframework.org/SeleniumLibrary  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

______________________________________________________________________

#### Preset 3: `rf_variable_table()`

**Purpose:** Display Robot Framework variables organized by type (scalar, list, dict)
with their current values, scopes, and sources in a readable table format.

**Use Cases:**

- Variable debugging during test development
- Suite/test setup logging to show resolved variables
- Documentation of variable configurations
- CI/CD logging of environment-specific variables

**Parameters:**

| Parameter    | Type             | Default    | Description                        |
| ------------ | ---------------- | ---------- | ---------------------------------- |
| `variables`  | `dict[str, Any]` | (required) | Variable name → value mapping      |
| `scope`      | `str \| None`    | `None`     | Scope: GLOBAL, SUITE, TEST, LOCAL  |
| `source`     | `str \| None`    | `None`     | Source file (variables file, etc.) |
| `title`      | `str \| None`    | `None`     | Custom title for the table         |
| `show_types` | `bool`           | `True`     | Show variable type prefixes        |
| `mask_keys`  | `list[str]`      | `[]`       | Variable names to mask values      |
| `console`    | `Console`        | `None`     | Optional Console instance          |

**Example:**

```python
from styledconsole.presets import rf_variable_table

# Full variable display
rf_variable_table(
    variables={
        "${BASE_URL}": "https://example.com",
        "${BROWSER}": "chrome",
        "${TIMEOUT}": "10s",
        "${PASSWORD}": "secret123",
        "@{USERS}": ["admin", "user1", "user2"],
        "&{CREDENTIALS}": {"user": "admin", "pass": "secret"},
    },
    scope="SUITE",
    source="variables/env_prod.yaml",
    mask_keys=["${PASSWORD}", "&{CREDENTIALS}"]
)
```

**Visualization Variant A (Categorized Table):**

```text
╭─ 📋 Suite Variables ─────────────────────────────────╮
│ Source: variables/env_prod.yaml                      │
├──────────────────────────────────────────────────────┤
│ 📝 Scalars:                                          │
│   ${BASE_URL}    │ https://example.com               │
│   ${BROWSER}     │ chrome                            │
│   ${TIMEOUT}     │ 10s                               │
│   ${PASSWORD}    │ ********                          │
├──────────────────────────────────────────────────────┤
│ 📋 Lists:                                            │
│   @{USERS}       │ [admin, user1, user2]             │
├──────────────────────────────────────────────────────┤
│ 🔑 Dictionaries:                                     │
│   &{CREDENTIALS} │ {user: admin, pass: ***}          │
╰──────────────────────────────────────────────────────╯
```

**Visualization Variant B (Flat List):**

```text
📋 Variables (SUITE) from variables/env_prod.yaml:
  ${BASE_URL}      = https://example.com
  ${BROWSER}       = chrome
  ${TIMEOUT}       = 10s
  ${PASSWORD}      = ********
  @{USERS}         = [admin, user1, user2]
  &{CREDENTIALS}   = {user: admin, pass: ***}
```

**Visualization Variant C (Scope-Colored):**

```text
┌─────────────────────────────────────────────────────┐
│ Variable Table                          Scope: SUITE│
├─────────────────────────────────────────────────────┤
│ ${BASE_URL}       https://example.com         [str] │
│ ${BROWSER}        chrome                      [str] │
│ ${TIMEOUT}        10s                         [str] │
│ ${PASSWORD}       ********                    [str] │
│ @{USERS}          3 items                    [list] │
│ &{CREDENTIALS}    2 keys                     [dict] │
└─────────────────────────────────────────────────────┘
```

______________________________________________________________________

#### Preset 4: `rf_tag_summary()`

**Purpose:** Display test results aggregated by Robot Framework tags, showing
pass/fail/skip counts, percentages, and optional trends for each tag category.

**Use Cases:**

- CI/CD summary reports organized by test categories
- Quality dashboards showing coverage by feature area
- Sprint reviews showing test status by user story tags
- Smoke/regression test subset reporting

**Parameters:**

| Parameter      | Type                        | Default    | Description                        |
| -------------- | --------------------------- | ---------- | ---------------------------------- |
| `tags`         | `dict[str, dict[str, int]]` | (required) | Tag → {passed, failed, skipped}    |
| `title`        | `str \| None`               | `None`     | Custom title                       |
| `show_percent` | `bool`                      | `True`     | Show percentage for each tag       |
| `sort_by`      | `str`                       | `"name"`   | Sort: name, passed, failed, total  |
| `highlight`    | `list[str]`                 | `[]`       | Tags to highlight (e.g., critical) |
| `console`      | `Console`                   | `None`     | Optional Console instance          |

**Example:**

```python
from styledconsole.presets import rf_tag_summary

rf_tag_summary(
    tags={
        "smoke": {"passed": 10, "failed": 0, "skipped": 0},
        "regression": {"passed": 45, "failed": 3, "skipped": 2},
        "critical": {"passed": 20, "failed": 1, "skipped": 0},
        "api": {"passed": 30, "failed": 2, "skipped": 1},
        "ui": {"passed": 25, "failed": 2, "skipped": 1},
    },
    title="Test Results by Tag",
    highlight=["critical", "smoke"],
    sort_by="failed"
)
```

**Visualization Variant A (Horizontal Bar Chart):**

```text
╭─ 🏷️ Test Results by Tag ────────────────────────────╮
│                                                      │
│ smoke       ██████████████████████████████ 100%  ⭐  │
│             ✅ 10  ❌ 0   ⏭️ 0   Total: 10           │
│                                                      │
│ critical    ████████████████████████████░░  95%  ⭐  │
│             ✅ 20  ❌ 1   ⏭️ 0   Total: 21           │
│                                                      │
│ api         ███████████████████████████░░░  91%     │
│             ✅ 30  ❌ 2   ⏭️ 1   Total: 33           │
│                                                      │
│ ui          ██████████████████████████░░░░  89%     │
│             ✅ 25  ❌ 2   ⏭️ 1   Total: 28           │
│                                                      │
│ regression  ██████████████████████████░░░░  90%     │
│             ✅ 45  ❌ 3   ⏭️ 2   Total: 50           │
│                                                      │
╰──────────────────────────────────────────────────────╯
```

**Visualization Variant B (Compact Table):**

```text
┌──────────────┬────────┬────────┬─────────┬───────┬──────┐
│ Tag          │ Passed │ Failed │ Skipped │ Total │  %   │
├──────────────┼────────┼────────┼─────────┼───────┼──────┤
│ ⭐ smoke     │     10 │      0 │       0 │    10 │ 100% │
│ ⭐ critical  │     20 │      1 │       0 │    21 │  95% │
│ api          │     30 │      2 │       1 │    33 │  91% │
│ ui           │     25 │      2 │       1 │    28 │  89% │
│ regression   │     45 │      3 │       2 │    50 │  90% │
└──────────────┴────────┴────────┴─────────┴───────┴──────┘
```

**Visualization Variant C (Visual Dots):**

```text
🏷️ Tag Summary
─────────────────────────────────────────────────────────
smoke ⭐      ●●●●●●●●●●                          10/10 ✓
critical ⭐   ●●●●●●●●●●●●●●●●●●●●○                20/21
api           ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●○○○    30/33
ui            ●●●●●●●●●●●●●●●●●●●●●●●●●○○○        25/28
regression    ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●○○○○○ 45/50
─────────────────────────────────────────────────────────
Legend: ● Passed  ○ Failed  ◌ Skipped
```

______________________________________________________________________

#### Preset 5: `rf_suite_structure()`

**Purpose:** Display Robot Framework suite hierarchy as a visual tree showing
test counts, statuses, and optional execution times for each suite level.

**Use Cases:**

- Test suite documentation and organization reports
- CI/CD logs showing suite execution structure
- Debugging suite setup/teardown issues
- Navigation aids in large test projects

**Parameters:**

| Parameter       | Type          | Default    | Description                |
| --------------- | ------------- | ---------- | -------------------------- |
| `structure`     | `dict`        | (required) | Nested suite structure     |
| `title`         | `str \| None` | `None`     | Custom title               |
| `show_counts`   | `bool`        | `True`     | Show test counts per suite |
| `show_status`   | `bool`        | `True`     | Show suite status          |
| `show_duration` | `bool`        | `False`    | Show execution duration    |
| `collapse_pass` | `bool`        | `False`    | Collapse passed suites     |
| `console`       | `Console`     | `None`     | Optional Console instance  |

**Structure Format:**

```python
{
    "name": "Suite Name",
    "tests": 5,                    # Optional: test count
    "status": "PASS",              # Optional: PASS, FAIL, SKIP
    "duration": 12.5,              # Optional: seconds
    "children": [...]              # Optional: child suites
}
```

**Example:**

```python
from styledconsole.presets import rf_suite_structure

rf_suite_structure(
    structure={
        "name": "All Tests",
        "status": "FAIL",
        "duration": 125.5,
        "children": [
            {"name": "Auth", "tests": 5, "status": "PASS", "duration": 15.2},
            {"name": "API", "tests": 12, "status": "FAIL", "duration": 45.8, "children": [
                {"name": "Users", "tests": 6, "status": "PASS", "duration": 20.1},
                {"name": "Orders", "tests": 6, "status": "FAIL", "duration": 25.7},
            ]},
            {"name": "UI", "tests": 8, "status": "PASS", "duration": 64.5, "children": [
                {"name": "Login", "tests": 3, "status": "PASS", "duration": 22.0},
                {"name": "Dashboard", "tests": 5, "status": "PASS", "duration": 42.5},
            ]},
        ]
    },
    title="Test Suite Hierarchy",
    show_duration=True
)
```

**Visualization Variant A (Tree with Icons):**

```text
╭─ 🗂️ Test Suite Hierarchy ───────────────────────────╮
│                                                      │
│ 📁 All Tests                          ❌ 125.5s     │
│ ├─ 📂 Auth (5 tests)                  ✅  15.2s     │
│ ├─ 📁 API (12 tests)                  ❌  45.8s     │
│ │  ├─ 📂 Users (6 tests)              ✅  20.1s     │
│ │  └─ 📂 Orders (6 tests)             ❌  25.7s     │
│ └─ 📂 UI (8 tests)                    ✅  64.5s     │
│    ├─ 📂 Login (3 tests)              ✅  22.0s     │
│    └─ 📂 Dashboard (5 tests)          ✅  42.5s     │
│                                                      │
╰──────────────────────────────────────────────────────╯
```

**Visualization Variant B (Indented Text):**

```text
🗂️ Suite Structure
───────────────────────────────────────────────────────
All Tests                                    ❌ 2m 5.5s
  Auth                           5 tests     ✅ 15.2s
  API                           12 tests     ❌ 45.8s
    Users                        6 tests     ✅ 20.1s
    Orders                       6 tests     ❌ 25.7s
  UI                             8 tests     ✅ 1m 4.5s
    Login                        3 tests     ✅ 22.0s
    Dashboard                    5 tests     ✅ 42.5s
───────────────────────────────────────────────────────
Total: 25 tests | Passed: 4/5 suites | Duration: 2m 5.5s
```

**Visualization Variant C (Nested Boxes):**

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 📁 All Tests                             ❌ 125.5s   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ ┌────────────────────────────────────────────────┐  ┃
┃ │ 📂 Auth (5 tests)                    ✅ 15.2s │  ┃
┃ └────────────────────────────────────────────────┘  ┃
┃ ┌────────────────────────────────────────────────┐  ┃
┃ │ 📁 API (12 tests)                    ❌ 45.8s │  ┃
┃ │  ├─ Users (6)                        ✅ 20.1s │  ┃
┃ │  └─ Orders (6)                       ❌ 25.7s │  ┃
┃ └────────────────────────────────────────────────┘  ┃
┃ ┌────────────────────────────────────────────────┐  ┃
┃ │ 📂 UI (8 tests)                      ✅ 64.5s │  ┃
┃ │  ├─ Login (3)                        ✅ 22.0s │  ┃
┃ │  └─ Dashboard (5)                    ✅ 42.5s │  ┃
┃ └────────────────────────────────────────────────┘  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

______________________________________________________________________

#### Preset 6: `rf_test_template()`

**Purpose:** Display data-driven Robot Framework test templates showing the template
keyword and all test data iterations with their individual results.

**Use Cases:**

- Data-driven test result reporting
- Template keyword documentation
- CI/CD logs showing parameterized test outcomes
- Test design reviews showing test data coverage

**Parameters:**

| Parameter       | Type                | Default    | Description                 |
| --------------- | ------------------- | ---------- | --------------------------- |
| `template`      | `str`               | (required) | Template keyword name       |
| `test_cases`    | `list[dict]`        | (required) | List of test case data      |
| `title`         | `str \| None`       | `None`     | Custom title                |
| `arg_names`     | `list[str] \| None` | `None`     | Column names for arguments  |
| `show_index`    | `bool`              | `True`     | Show iteration index        |
| `show_duration` | `bool`              | `False`    | Show duration per iteration |
| `console`       | `Console`           | `None`     | Optional Console instance   |

**Test Case Format:**

```python
{
    "args": ["arg1", "arg2", ...],  # Positional arguments
    "name": "Optional test name",   # Optional: custom name
    "status": "PASS",               # PASS, FAIL, SKIP
    "duration": 1.5,                # Optional: seconds
    "msg": "Error message"          # Optional: failure message
}
```

**Example:**

```python
from styledconsole.presets import rf_test_template

rf_test_template(
    template="Login With Credentials",
    arg_names=["Username", "Password", "Expected"],
    test_cases=[
        {"args": ["valid_user", "valid_pass", "SUCCESS"], "status": "PASS", "duration": 1.2},
        {"args": ["valid_user", "wrong_pass", "INVALID_PASSWORD"], "status": "PASS", "duration": 0.8},
        {"args": ["invalid_user", "any_pass", "USER_NOT_FOUND"], "status": "PASS", "duration": 0.5},
        {"args": ["locked_user", "valid_pass", "ACCOUNT_LOCKED"], "status": "FAIL",
         "msg": "Expected ACCOUNT_LOCKED but got SUCCESS", "duration": 0.9},
        {"args": ["", "any_pass", "EMPTY_USERNAME"], "status": "SKIP",
         "msg": "Skipped: Empty username test disabled"},
    ],
    title="Login Credential Validation Tests",
    show_duration=True
)
```

**Visualization Variant A (Data Table):**

```text
╭─ 📊 Login Credential Validation Tests ──────────────────────────╮
│                                                                  │
│ Template: Login With Credentials                                 │
│                                                                  │
│ ┌────┬──────────────┬──────────────┬──────────────────┬────────┐│
│ │  # │ Username     │ Password     │ Expected         │ Result ││
│ ├────┼──────────────┼──────────────┼──────────────────┼────────┤│
│ │  1 │ valid_user   │ valid_pass   │ SUCCESS          │ ✅ 1.2s││
│ │  2 │ valid_user   │ wrong_pass   │ INVALID_PASSWORD │ ✅ 0.8s││
│ │  3 │ invalid_user │ any_pass     │ USER_NOT_FOUND   │ ✅ 0.5s││
│ │  4 │ locked_user  │ valid_pass   │ ACCOUNT_LOCKED   │ ❌ 0.9s││
│ │  5 │ (empty)      │ any_pass     │ EMPTY_USERNAME   │ ⏭️ --- ││
│ └────┴──────────────┴──────────────┴──────────────────┴────────┘│
│                                                                  │
│ Summary: ✅ 3 passed  ❌ 1 failed  ⏭️ 1 skipped                  │
│                                                                  │
│ ❌ #4: Expected ACCOUNT_LOCKED but got SUCCESS                   │
│ ⏭️ #5: Skipped: Empty username test disabled                     │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯
```

**Visualization Variant B (Compact Iterations):**

```text
📊 Template: Login With Credentials
─────────────────────────────────────────────────────────
  ✅ [1] valid_user, valid_pass → SUCCESS              1.2s
  ✅ [2] valid_user, wrong_pass → INVALID_PASSWORD     0.8s
  ✅ [3] invalid_user, any_pass → USER_NOT_FOUND       0.5s
  ❌ [4] locked_user, valid_pass → ACCOUNT_LOCKED      0.9s
        └─ Expected ACCOUNT_LOCKED but got SUCCESS
  ⏭️ [5] (empty), any_pass → EMPTY_USERNAME            ---
        └─ Skipped: Empty username test disabled
─────────────────────────────────────────────────────────
Results: 3/5 passed (60%)
```

**Visualization Variant C (Card per Iteration):**

```text
╭─ 📊 Login With Credentials ─────────────────────────────────────╮
│                                                                  │
│ ┌─ Iteration 1 ────────────────────────────────────┐  ✅ PASS   │
│ │ Username: valid_user                             │            │
│ │ Password: valid_pass                             │   1.2s     │
│ │ Expected: SUCCESS                                │            │
│ └──────────────────────────────────────────────────┘            │
│                                                                  │
│ ┌─ Iteration 2 ────────────────────────────────────┐  ✅ PASS   │
│ │ Username: valid_user                             │            │
│ │ Password: wrong_pass                             │   0.8s     │
│ │ Expected: INVALID_PASSWORD                       │            │
│ └──────────────────────────────────────────────────┘            │
│                                                                  │
│ ┌─ Iteration 4 ────────────────────────────────────┐  ❌ FAIL   │
│ │ Username: locked_user                            │            │
│ │ Password: valid_pass                             │   0.9s     │
│ │ Expected: ACCOUNT_LOCKED                         │            │
│ │ Error: Expected ACCOUNT_LOCKED but got SUCCESS   │            │
│ └──────────────────────────────────────────────────┘            │
│                                                                  │
╰──────────────────────────────────────────────────────────────────╯
```

______________________________________________________________________

## v0.8.0 Implementation Plan

**Theme:** Theme System, Gradients & Progress Bars
**Status:** ✅ COMPLETED
**Completed:** November 30, 2025

### Feature 1: Theme System ✅ COMPLETED

**Priority:** MEDIUM
**Effort:** 1 day (actual)
**Impact:** Consistent styling, professional appearance

**Implemented API:**

```python
from styledconsole import Console, Theme, THEMES, GradientSpec

# Using predefined theme by name
console = Console(theme="dark")  # or "light", "solarized", etc.

# Using predefined theme constant
console = Console(theme=THEMES.MONOKAI)

# Custom theme
my_theme = Theme(
    primary="hotpink",
    success="lime",
    warning="gold",
    error="crimson",
    info="deepskyblue",
    border="orchid",
    muted="gray",
    secondary="coral",
)
console = Console(theme=my_theme)

# Semantic color resolution
console.text("Success!", color="success")  # Uses theme.success color
```

**Predefined Solid Themes (6):**

| Theme     | Primary   | Success      | Warning       | Error     | Border     |
| --------- | --------- | ------------ | ------------- | --------- | ---------- |
| DARK      | cyan      | lime         | gold          | red       | white      |
| LIGHT     | blue      | green        | orange        | crimson   | darkgray   |
| SOLARIZED | steelblue | olivedrab    | darkgoldenrod | indianred | slategray  |
| MONOKAI   | skyblue   | yellowgreen  | khaki         | deeppink  | whitesmoke |
| NORD      | lightblue | darkseagreen | burlywood     | indianred | lavender   |
| DRACULA   | cyan      | springgreen  | khaki         | tomato    | whitesmoke |

**Deliverables:**

- ✅ `Theme` frozen dataclass in `core/theme.py`
- ✅ `THEMES` namespace with 6 solid themes
- ✅ `Console(theme=...)` parameter (string or Theme)
- ✅ `console.theme` property
- ✅ Semantic color resolution in `console.text()`
- ✅ 34 unit tests in `tests/unit/test_theme.py`
- ✅ Example: `examples/gallery/themes_showcase.py`

______________________________________________________________________

### Feature 2: Gradient Themes ✅ COMPLETED

**Priority:** MEDIUM
**Effort:** 0.5 day (actual)
**Impact:** Eye-catching visuals, rainbow effects

**Implemented API:**

```python
from styledconsole import Console, Theme, GradientSpec, THEMES

# Using predefined gradient theme
console = Console(theme="rainbow")  # or "ocean", "sunset", "neon"
console.banner("HELLO")  # Auto-applies banner gradient
console.frame(["Line 1", "Line 2"])  # Auto-applies border + text gradients

# Custom gradient theme
fire_theme = Theme(
    name="fire",
    primary="orangered",
    border_gradient=GradientSpec("darkred", "gold"),
    banner_gradient=GradientSpec("crimson", "yellow"),
    text_gradient=GradientSpec("orangered", "gold"),
)
console = Console(theme=fire_theme)

# Query gradient themes
solid = THEMES.solid_themes()      # 6 themes without gradients
gradient = THEMES.gradient_themes() # 4 themes with gradients
```

**Predefined Gradient Themes (4):**

| Theme   | Border Gradient | Banner Gradient | Text Gradient          |
| ------- | --------------- | --------------- | ---------------------- |
| RAINBOW | red → magenta   | red → violet    | red → violet           |
| OCEAN   | darkblue → cyan | navy → aqua     | steelblue → aquamarine |
| SUNSET  | crimson → gold  | darkred → gold  | orangered → gold       |
| NEON    | magenta → cyan  | magenta → lime  | hotpink → cyan         |

**Auto-Applied Gradients:**

- `border_gradient`: Applied to frame borders when no explicit gradient
- `banner_gradient`: Applied to banner text when no explicit gradient
- `text_gradient`: Applied to frame content (per-line interpolation)

**Deliverables:**

- ✅ `GradientSpec` frozen dataclass
- ✅ 4 gradient themes (RAINBOW, OCEAN, SUNSET, NEON)
- ✅ `Theme.has_gradients()` method
- ✅ `THEMES.solid_themes()` and `THEMES.gradient_themes()` methods
- ✅ Auto-application in `console.frame()`, `console.banner()`, `console.render_frame()`
- ✅ 10 additional unit tests for gradients

______________________________________________________________________

### Feature 3: Preset Theme Integration ✅ COMPLETED

**Priority:** MEDIUM
**Effort:** 0.5 day (actual)
**Impact:** Presets work seamlessly with themes

**Changes:**

- Updated `status.py` preset to use semantic colors (`success`, `error`, `warning`, `info`)
- Updated `summary.py` preset to use semantic colors
- Updated `dashboard.py` preset to use semantic colors (`primary`, `secondary`)
- Fixed `console.render_frame()` to resolve theme colors

**Usage:**

```python
from styledconsole import Console
from styledconsole.presets.status import status_frame, status_summary

# Presets now use themed console colors
themed_console = Console(theme="dracula")
status_frame("test_example", "PASS", console=themed_console)

# Gradient themes work with presets too
rainbow_console = Console(theme="rainbow")
status_summary(results, console=rainbow_console)
```

______________________________________________________________________

### Feature 4: Progress Bar Wrapper ✅ COMPLETED

**Priority:** LOW → MEDIUM (elevated)
**Effort:** 1 day (actual)
**Impact:** Convenience for long-running operations

**Implemented API:**

```python
from styledconsole import Console

console = Console()

# Simple progress
with console.progress() as progress:
    task = progress.add_task("Processing...", total=100)
    for i in range(100):
        # do work
        progress.update(task, advance=1)

# Multiple tasks
with console.progress() as progress:
    task1 = progress.add_task("Download", total=100)
    task2 = progress.add_task("Process", total=50)
    # ...

# Indeterminate progress (spinner)
with console.progress() as progress:
    task = progress.add_task("Connecting...", total=None)
    # ...

# Theme-aware progress
console = Console(theme="monokai")
with console.progress() as progress:
    # Uses theme colors for styling
    ...
```

**Deliverables:**

- ✅ `StyledProgress` class in `core/progress.py`
- ✅ `console.progress()` context manager
- ✅ Theme color integration
- ✅ Support for multiple tasks, indeterminate progress
- ✅ `transient` option for disappearing progress
- ✅ 18 unit tests in `tests/unit/test_progress.py`
- ✅ Example: `examples/demos/progress_demo.py`

______________________________________________________________________

### Feature 3: Icon Provider (ASCII Fallback) - PLANNED

**Priority:** MEDIUM
**Effort:** 1-2 days (estimated)
**Status:** Not started

See v0.9.0 planning section.

______________________________________________________________________

### Feature 4: Runtime Policy System - PLANNED

**Priority:** MEDIUM
**Effort:** 2-3 days (estimated)
**Status:** Not started

See v0.9.0 planning section.

______________________________________________________________________

## v0.7.0 Implementation Plan

**Theme:** Frame Groups & Context Manager
**Status:** ✅ COMPLETED
**Completed:** November 30, 2025

### Feature 1: Frame Groups (Dictionary API) ✅ COMPLETED

**Priority:** HIGH
**Effort:** 1 day (actual)
**Impact:** Enables dashboard-like layouts without presets

**Implemented API:**

```python
# frame_group() - print grouped frames
console.frame_group(
    [
        {"content": "Status: Online", "title": "System"},
        {"content": "CPU: 45%", "title": "Resources"},
    ],
    title="Dashboard",
    border="double",
    gap=1,
    inherit_style=True,
)

# render_frame_group() - return string for nesting
inner = console.render_frame_group(
    [{"content": "A"}, {"content": "B"}],
    title="Inner",
)
console.frame(inner, title="Outer")
```

**Deliverables:**

- ✅ `frame_group()` method in Console class
- ✅ `render_frame_group()` for nesting support
- ✅ Style inheritance (`inherit_style` parameter)
- ✅ Gap control (`gap` parameter)
- ✅ 27 unit tests in `tests/unit/test_frame_group.py`
- ✅ Updated `examples/demos/nested_frames.py`
- ✅ Documentation in USER_GUIDE.md

**Acceptance Criteria:**

- ✅ Frame group prints as single visual unit
- ✅ Supports title, border, padding on outer group
- ✅ Works with gradient borders
- ✅ Style inheritance option
- ✅ Gap control between inner frames

______________________________________________________________________

### Feature 2: Context Manager (console.group) ✅ COMPLETED

**Priority:** HIGH (accelerated from v0.8.0)
**Effort:** 1 day (actual)
**Impact:** More Pythonic API for complex layouts, preset improvement potential

**Implemented API:**

```python
# Context manager groups multiple frames
with console.group(title="Dashboard", border="heavy") as group:
    console.frame("Status: OK", title="System")
    console.frame("Memory: 4GB", title="Resources")
    # Frames are captured and rendered when exiting context

# Nested groups
with console.group(title="Outer") as outer:
    console.frame("Top section")
    with console.group(title="Inner") as inner:
        console.frame("Nested A")
        console.frame("Nested B")
    console.frame("Bottom section")

# Width alignment for status displays
with console.group(title="Report", align_widths=True):
    console.frame("Success", border_color="green")
    console.frame("Warning message here", border_color="yellow")
    console.frame("Error", border_color="red")
```

**Deliverables:**

- ✅ `FrameGroupContext` class in `core/group.py`
- ✅ `console.group()` context manager method
- ✅ Frame capture via contextvars (thread-safe)
- ✅ Nested group support via stack
- ✅ Width alignment (`align_widths` parameter)
- ✅ Style inheritance (`inherit_style` parameter)
- ✅ Gap control (`gap` parameter)
- ✅ 24 unit tests in `tests/unit/test_group_context.py`
- ✅ Updated `examples/demos/nested_frames.py`
- ✅ Documentation in USER_GUIDE.md

**Acceptance Criteria:**

- ✅ Context manager syntax works as documented
- ✅ Supports arbitrary nesting depth
- ✅ Captured frames rendered on context exit
- ✅ Thread-safe with contextvars
- ✅ Backward compatible (no group = direct print)
- ✅ Width alignment option for uniform display

______________________________________________________________________

## v0.9.0 Future Plans

**Theme:** Environment Adaptation
**Target:** Q1 2026
**Status:** Planned

The following features are planned for v0.9.0:

### Feature 1: Icon Provider (ASCII Fallback)r (ASCII Fallback)

**Priority:** MEDIUM
**Effort:** 1-2 days
**Impact:** Graceful degradation for limited terminals

**Problem:**
Emojis don't render correctly in all terminals (CI/CD, SSH, Windows cmd).

**Proposed API:**

```python
from styledconsole import icons, Console

# Auto-detects terminal capability
console = Console()
console.text(f"{icons.success} Tests passed")  # ✅ or [OK]
console.text(f"{icons.error} Build failed")    # ❌ or [FAIL]

# Force ASCII mode
from styledconsole import set_icon_mode
set_icon_mode("ascii")  # All icons become ASCII
```

**Icon Mapping:**

| Name     | Unicode | ASCII  |
| -------- | ------- | ------ |
| success  | ✅      | [OK]   |
| error    | ❌      | [FAIL] |
| warning  | ⚠️      | [WARN] |
| info     | ℹ️      | [INFO] |
| debug    | 🔍      | [DBG]  |
| critical | 🔥      | [CRIT] |
| rocket   | 🚀      | [>>]   |
| check    | ✓       | [x]    |

**Implementation Steps:**

1. Create `IconProvider` class in `utils/icons.py`
1. Implement auto-detection based on terminal profile
1. Add global `icons` instance with attribute access
1. Add `set_icon_mode(mode)` function
1. Unit tests for both modes
1. Integration with Console (optional `icon_mode` param)

**Acceptance Criteria:**

- [ ] Auto-detects terminal capability
- [ ] Manual override via `set_icon_mode()`
- [ ] 8+ common icons defined
- [ ] Works in CI/CD environments
- [ ] No breaking changes to existing code

______________________________________________________________________

### Feature 3: Runtime Policy System

**Priority:** MEDIUM
**Effort:** 2-3 days
**Impact:** Enterprise-friendly, NO_COLOR compliance

**Problem:**
No central control over rendering decisions based on environment.

**Proposed API:**

```python
from styledconsole import Console, RenderPolicy

# Auto-detect from environment
policy = RenderPolicy.from_env()
console = Console(policy=policy)

# Manual policy
policy = RenderPolicy(
    unicode=True,   # Use Unicode box drawing
    color=False,    # Disable ANSI colors (respects NO_COLOR)
    emoji=False,    # Disable emojis
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

**Implementation Steps:**

1. Create `RenderPolicy` dataclass in `core/policy.py`
1. Implement `from_env()` classmethod with detection logic
1. Add `policy` parameter to Console `__init__`
1. Modify RenderingEngine to respect policy
1. Support NO_COLOR standard (<https://no-color.org/>)
1. Unit tests with mocked environment
1. Documentation for CI/CD integration

**Acceptance Criteria:**

- [ ] Auto-detects NO_COLOR environment variable
- [ ] Detects TERM=dumb for ASCII mode
- [ ] Detects CI environments conservatively
- [ ] Manual override possible
- [ ] Policy affects all rendering operations

______________________________________________________________________

### v0.9.0 Implementation Timeline

```text
Week 1:   Feature 1 (Themes)
Week 2:   Feature 2 (Icons) + Feature 3 (Policy)
Week 3:   Feature 4 (Progress) + Polish
Week 4:   Testing + Documentation + Release
```

### Dependencies

```text
Feature 3 (Policy) → Feature 2 (Icons)   # Policy controls icon mode
Feature 1 (Theme) → Feature 4 (Progress) # Progress uses theme colors
```

______________________________________________________________________

## Active Tasks

### Completed (v0.8.0)

| Task                   | Status  |
| ---------------------- | ------- |
| Theme dataclass        | ✅ Done |
| GradientSpec dataclass | ✅ Done |
| THEMES namespace       | ✅ Done |
| 6 solid themes         | ✅ Done |
| 4 gradient themes      | ✅ Done |
| Console theme param    | ✅ Done |
| Semantic color resolve | ✅ Done |
| Border gradient auto   | ✅ Done |
| Banner gradient auto   | ✅ Done |
| Text gradient auto     | ✅ Done |
| Preset theme support   | ✅ Done |
| StyledProgress class   | ✅ Done |
| console.progress()     | ✅ Done |
| Unit tests (44 new)    | ✅ Done |
| themes_showcase.py     | ✅ Done |
| progress_demo.py       | ✅ Done |

### Future (v0.9.0)

| Task           | Priority |
| -------------- | -------- |
| Icon Provider  | MEDIUM   |
| Runtime Policy | MEDIUM   |

### Future (v1.0.0)

| Task               | Priority |
| ------------------ | -------- |
| Final docs polish  | HIGH     |
| API reference docs | MEDIUM   |
| Performance audit  | LOW      |

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

## Changelog

### Version 0.8.0 (November 2025)

**Added:**

- `Theme` frozen dataclass with 11 semantic colors + 3 gradient specs
- `GradientSpec` frozen dataclass for gradient definitions
- 10 predefined themes: 6 solid + 4 gradient (RAINBOW, OCEAN, SUNSET, NEON)
- `THEMES` namespace with `all()`, `solid_themes()`, `gradient_themes()`, `get()` methods
- `Console(theme=...)` parameter accepting theme name or Theme instance
- Auto-application of border, banner, and text gradients from theme
- `StyledProgress` wrapper class for `rich.progress.Progress`
- `console.progress()` context manager

**Changed:**

- Presets now use semantic color names (`success`, `error`, `warning`, `info`)
- `console.frame()` auto-applies theme gradients when available
- `console.banner()` auto-applies theme banner gradient
- `render_frame()` now resolves theme colors like `frame()`

**Fixed:**

- CSS4 color names now work with Rich (via `normalize_color_for_rich()`)

______________________________________________________________________

### Version 0.7.0 (November 2025)

**Added:**

- `console.frame_group()` for grouped frames with outer container
- `console.render_frame_group()` for nested frame groups
- Full frame nesting support (unlimited depth)
- `gap` parameter for vertical spacing between frames
- `inherit_style` parameter to cascade styles to children

**Changed:**

- Frame rendering now preserves Rich markup in content
- All preset functions updated to use frame nesting API

______________________________________________________________________

### Version 0.5.0 (November 2025)

**Changed:**

- Documentation consolidated into 4 master docs (`docs/USER_GUIDE.md`, `docs/DEVELOPER_GUIDE.md`, `docs/PROJECT_STATUS.md`, `docs/DOCUMENTATION_POLICY.md`)
- Examples reorganized into 4 categories: `gallery/`, `usecases/`, `demos/`, `validation/`
- Gallery examples standardized with EMOJI constants
- Unified example runner with `--all` and `--auto` flags

**Removed:**

- 24 exploratory test files from project root
- Empty `recipes/` folder
- Redundant `test_examples.py`

### Version 0.4.0 (November 2025)

**Added:**

- Unified gradient engine with strategy pattern
- `Animation` class for animated gradients
- `OffsetPositionStrategy` for cycling colors
- Preset functions: `status_frame()`, `test_summary()`, `dashboard()`
- Enhanced HTML export with `page_title`, `theme_css`

**Changed:**

- Gradient functions now use `apply_gradient()` engine
- Cleaner separation of position, color, and target strategies

**Fixed:**

- Consistent color parameter naming across API

### v0.3.0 (November 2025)

**Added:**

- Rich-native frame rendering (uses `rich.Panel`)
- `box_mapping.py` for border → Rich Box mapping
- `RenderingEngine` coordinator class

**Changed:**

- `Console.frame()` now uses Rich Panel internally
- 100% backward compatible with v0.1.0 API

**Fixed:**

- ANSI wrapping bugs eliminated
- Better terminal compatibility

### v0.1.0 (October 2025)

**Initial Release:**

- Core text utilities (emoji-safe width)
- Frame rendering with 8 border styles
- Banner rendering with pyfiglet
- Layout composer (stack, grid, side-by-side)
- Console API (facade pattern)
- 148 CSS4 colors + gradients
- Terminal detection
- HTML/text export

______________________________________________________________________

## Architecture Principles

These principles guide all development:

| Principle              | Description                        |
| ---------------------- | ---------------------------------- |
| Simplicity             | Add complexity only when necessary |
| Test Everything        | Maintain 95%+ coverage             |
| Single Responsibility  | Each module has one purpose        |
| Document Everything    | Type hints + docstrings            |
| Backward Compatibility | Stable public API                  |

______________________________________________________________________

## Contributing

**Feature Requests:**

1. Open a GitHub issue
1. Describe use case
1. We evaluate against principles

**Pull Requests:**

1. Include tests (95%+ coverage)
1. Update documentation
1. Follow code style (ruff)

______________________________________________________________________

## References

- **User Guide:** `docs/USER_GUIDE.md`
- **Developer Guide:** `docs/DEVELOPER_GUIDE.md`
- **CHANGELOG.md:** Root-level changelog
