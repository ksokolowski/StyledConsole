#!/usr/bin/env python3
"""
Banner Showcase

A visual demonstration of the best banner rendering capabilities.

v0.4.0: Updated to use Console.banner() instead of BannerRenderer.
"""

from styledconsole import Console

console = Console()

# Application Launch
print()
console.banner(
    "WELCOME",
    font="slant",
    start_color="dodgerblue",
    end_color="purple",
    border="double",
    width=80,
)

print()
console.banner(
    "StyledConsole v0.1",
    font="standard",
    start_color="lightseagreen",
    end_color="coral",
    border="rounded",
)

print()
print()

# Status Messages
print("Status Messages:")
print()

console.banner(
    "SUCCESS",
    font="banner",
    start_color="lime",
    end_color="green",
    border="heavy",
    width=65,
)

print()

console.banner(
    "ERROR",
    font="banner",
    start_color="red",
    end_color="darkred",
    border="heavy",
    width=65,
)

print()

console.banner(
    "WARNING",
    font="banner",
    start_color="orange",
    end_color="orangered",
    border="heavy",
    width=65,
)

print()
print()

# Section Headers
print("Section Headers:")
print()

console.banner(
    "API",
    font="big",
    start_color="cyan",
    end_color="blue",
)

print()

console.banner(
    "DATABASE",
    font="big",
    start_color="green",
    end_color="teal",
)

print()

console.banner(
    "TESTS",
    font="big",
    start_color="yellow",
    end_color="orange",
)

print()
print()

# Feature Showcase
print("Feature Showcase:")
print()

console.banner(
    "ASCII ART",
    font="slant",
    start_color="red",
    end_color="orange",
    border="solid",
    width=70,
    padding=2,
)

print()

console.banner(
    "GRADIENTS",
    font="slant",
    start_color="purple",
    end_color="pink",
    border="solid",
    width=70,
    padding=2,
)

print()

console.banner(
    "BORDERS",
    font="slant",
    start_color="blue",
    end_color="cyan",
    border="solid",
    width=70,
    padding=2,
)

print()
print()

# Final Message
console.banner(
    "ENJOY",
    font="banner",
    start_color="gold",
    end_color="orange",
    border="thick",
    width=60,
)

print()
