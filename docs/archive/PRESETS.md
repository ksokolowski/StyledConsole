# 🧩 StyledConsole Presets Guide

StyledConsole includes a collection of **presets**—pre-built, high-level components designed for common CLI patterns. These presets save you time by encapsulating complex layout and styling logic into simple function calls.

## Available Presets

| Preset           | Function         | Description                                                      |
| :--------------- | :--------------- | :--------------------------------------------------------------- |
| **Status Frame** | `status_frame()` | Displays a status update (Pass/Fail/Skip) with a timestamp.      |
| **Test Summary** | `test_summary()` | Shows a comprehensive summary of test execution results.         |
| **Dashboard**    | `dashboard()`    | Creates a grid-based dashboard layout for monitoring or metrics. |

______________________________________________________________________

## 🚦 Status Frame

The `status_frame` preset is perfect for displaying the result of a single operation, such as a test case, a build step, or a service check.

### Usage

```python
from styledconsole.presets import status_frame

# Simple success
status_frame("Database Connection", "PASS", duration=0.05)

# Failure with error message
status_frame(
    "API Integration",
    "FAIL",
    duration=1.2,
    message="ConnectionRefusedError: Connection refused"
)
```

### Parameters

- `name` (str): The name of the task or operation.
- `status` (str): The status code (e.g., "PASS", "FAIL", "SKIP", "ERROR", "WARN").
- `duration` (float, optional): Duration of the operation in seconds.
- `message` (str, optional): Additional details or error message.
- `console` (Console, optional): The console instance to use.

______________________________________________________________________

## 📊 Test Summary

The `test_summary` preset generates a beautiful summary report for a collection of test results or operation outcomes. It calculates statistics automatically.

### Usage

```python
from styledconsole.presets import test_summary

results = [
    {"name": "test_auth", "status": "PASS", "duration": 0.12},
    {"name": "test_db", "status": "PASS", "duration": 0.45},
    {"name": "test_api", "status": "FAIL", "duration": 1.05, "message": "500 Internal Server Error"},
]

test_summary(results, total_duration=1.62)
```

### Parameters

- `results` (list[TestResult]): A list of result dictionaries. Each dict should have:
  - `name` (str): Name of the test.
  - `status` (str): Status ("PASS", "FAIL", etc.).
  - `duration` (float): Duration in seconds.
  - `message` (str, optional): Error message or details.
- `total_duration` (float, optional): Total execution time.
- `console` (Console, optional): The console instance to use.

______________________________________________________________________

## 🚀 Dashboard

The `dashboard` preset allows you to create multi-panel layouts quickly. It uses a grid system to arrange "widgets" (content panels) automatically.

### Usage

```python
from styledconsole.presets import dashboard, DashboardWidget
from styledconsole import EMOJI

widgets = [
    {
        "title": f"{EMOJI.CHART_INCREASING} CPU Load",
        "content": "45% Usage\n8 Cores Active",
    },
    {
        "title": f"{EMOJI.MEMORY} Memory",
        "content": "2.4GB / 8GB Used",
    },
    {
        "title": f"{EMOJI.GLOBE_WITH_MERIDIANS} Network",
        "content": "In: 1.2 MB/s\nOut: 0.4 MB/s",
    },
    {
        "title": f"{EMOJI.WARNING} Alerts",
        "content": "No active alerts",
    },
]

dashboard("System Monitor", widgets, columns=2)
```

### Parameters

- `title` (str): The main title of the dashboard.
- `widgets` (list[DashboardWidget]): A list of widget configurations. Each widget is a dict with:
  - `title` (str): Widget title.
  - `content` (str | Any): Widget content (text or renderable).
  - `width` (int, optional): Fixed width.
  - `ratio` (int, optional): Flex ratio (default 1).
- `columns` (int): Number of columns in the grid (default: 2).
- `console` (Console, optional): The console instance to use.
