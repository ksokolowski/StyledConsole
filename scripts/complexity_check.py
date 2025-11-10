#!/usr/bin/env python3
"""
Simple complexity gate using radon.

- Fails if any function/method has cyclomatic complexity worse than grade C (i.e., D-F)
- Fails if any file has Maintainability Index < 40 (pragmatic threshold for existing code)

Configuration via environment variables:
- COMPLEXITY_PATHS: space-separated paths to check (default: "src/styledconsole")
- CC_MIN_GRADE: minimum acceptable grade (default: "C")
- MI_MIN: minimum maintainability index per file (default: 40)

Usage:
  uv run python scripts/complexity_check.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

try:
    from radon.complexity import cc_rank, cc_visit
    from radon.metrics import mi_visit
except Exception:  # pragma: no cover - guard for missing dev dep
    print("[complexity] radon not available; skip (install in dev group)", file=sys.stderr)
    sys.exit(0)


def iter_py_files(base: Path) -> list[Path]:
    return [p for p in base.rglob("*.py") if "/__pycache__/" not in str(p)]


def main() -> int:
    base_paths = os.environ.get("COMPLEXITY_PATHS", "src/styledconsole").split()
    min_grade = os.environ.get("CC_MIN_GRADE", "C").upper()
    mi_min = float(os.environ.get("MI_MIN", "40"))

    allowed_grades = {"A", "B", "C", "D", "E", "F"}
    if min_grade not in allowed_grades:
        allowed_list = sorted(allowed_grades)
        print(f"[complexity] Invalid CC_MIN_GRADE={min_grade}; expected one of {allowed_list}")
        return 2

    fail = False

    # Cyclomatic complexity gate
    for path in base_paths:
        for py in iter_py_files(Path(path)):
            try:
                code = py.read_text(encoding="utf-8")
            except Exception:
                continue
            for block in cc_visit(code):
                grade = cc_rank(block.complexity)
                if grade > min_grade:  # lexicographical (A<B<...)
                    print(
                        f"[CC] {py}:{block.lineno} {block.name} "
                        f"complexity={block.complexity} grade={grade} (min {min_grade})"
                    )
                    fail = True

    # Maintainability index gate
    for path in base_paths:
        for py in iter_py_files(Path(path)):
            try:
                code = py.read_text(encoding="utf-8")
            except Exception:
                continue
            mi = mi_visit(code, multi=True)
            if mi < mi_min:
                print(f"[MI] {py} maintainability_index={mi:.2f} (min {mi_min})")
                fail = True

    if fail:
        print("[complexity] thresholds failed. Tune via CC_MIN_GRADE / MI_MIN or refactor.")
        return 1
    print("[complexity] OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
