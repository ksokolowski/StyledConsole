#!/usr/bin/env python3
"""
Banner Showcase

A visual demonstration of the best banner rendering capabilities.
"""

from styledconsole import BannerRenderer

renderer = BannerRenderer()

# Application Launch
print()
for line in renderer.render(
    "WELCOME",
    font="slant",
    gradient_start="dodgerblue",
    gradient_end="purple",
    border="double",
    width=80,
):
    print(line)

print()
for line in renderer.render(
    "StyledConsole v0.1",
    font="standard",
    gradient_start="lightseagreen",
    gradient_end="coral",
    border="rounded",
):
    print(line)

print()
print()

# Status Messages
print("Status Messages:")
print()

for line in renderer.render(
    "SUCCESS",
    font="banner",
    gradient_start="lime",
    gradient_end="green",
    border="heavy",
    width=65,
):
    print(line)

print()

for line in renderer.render(
    "ERROR",
    font="banner",
    gradient_start="red",
    gradient_end="darkred",
    border="heavy",
    width=65,
):
    print(line)

print()

for line in renderer.render(
    "WARNING",
    font="banner",
    gradient_start="orange",
    gradient_end="orangered",
    border="heavy",
    width=65,
):
    print(line)

print()
print()

# Section Headers
print("Section Headers:")
print()

for line in renderer.render(
    "API",
    font="big",
    gradient_start="cyan",
    gradient_end="blue",
):
    print(line)

print()

for line in renderer.render(
    "DATABASE",
    font="big",
    gradient_start="green",
    gradient_end="teal",
):
    print(line)

print()

for line in renderer.render(
    "TESTS",
    font="big",
    gradient_start="yellow",
    gradient_end="orange",
):
    print(line)

print()
print()

# Feature Showcase
print("Feature Showcase:")
print()

for line in renderer.render(
    "ASCII ART",
    font="slant",
    gradient_start="red",
    gradient_end="orange",
    border="solid",
    width=70,
    padding=2,
):
    print(line)

print()

for line in renderer.render(
    "GRADIENTS",
    font="slant",
    gradient_start="purple",
    gradient_end="pink",
    border="solid",
    width=70,
    padding=2,
):
    print(line)

print()

for line in renderer.render(
    "BORDERS",
    font="slant",
    gradient_start="blue",
    gradient_end="cyan",
    border="solid",
    width=70,
    padding=2,
):
    print(line)

print()
print()

# Final Message
for line in renderer.render(
    "ENJOY",
    font="banner",
    gradient_start="gold",
    gradient_end="orange",
    border="thick",
    width=60,
):
    print(line)

print()
