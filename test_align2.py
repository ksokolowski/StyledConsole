#!/usr/bin/env python3
"""Test center alignment."""

from rich.align import Align
from rich.console import Console as RichConsole
from rich.panel import Panel
from rich.text import Text

content = (
    "╔══════════════════════════════════════════════════════════╗\n"
    "║           🌈 NESTED GRADIENT ARCHITECTURE                ║\n"
    "╚══════════════════════════════════════════════════════════╝"
)

rc = RichConsole()

print("Test 1: Text with no_wrap, no Align wrapper:")
text_obj1 = Text(content, no_wrap=True, overflow="ignore")
panel1 = Panel(text_obj1, title="No Align", width=80)
rc.print(panel1)

print("\n\nTest 2: Text with no_wrap, WITH Align.center wrapper:")
text_obj2 = Text(content, no_wrap=True, overflow="ignore")
aligned = Align.center(text_obj2)
panel2 = Panel(aligned, title="With Align.center", width=80)
rc.print(panel2)

print("\n\nTest 3: Check what Align.center returns:")
text_obj3 = Text("Hello World", no_wrap=True)
aligned3 = Align.center(text_obj3)
print(f"Type: {type(aligned3)}")
print(f"Has no_wrap attr: {hasattr(aligned3, 'no_wrap')}")
