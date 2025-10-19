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
    start_color="dodgerblue",
    end_color="purple",
    border="double",
    width=80,
):
    print(line)

print()
for line in renderer.render(
    "StyledConsole v0.1",
    font="standard",
    start_color="lightseagreen",
    end_color="coral",
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
    start_color="lime",
    end_color="green",
    border="heavy",
    width=65,
):
    print(line)

print()

for line in renderer.render(
    "ERROR",
    font="banner",
    start_color="red",
    end_color="darkred",
    border="heavy",
    width=65,
):
    print(line)

print()

for line in renderer.render(
    "WARNING",
    font="banner",
    start_color="orange",
    end_color="orangered",
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
    start_color="cyan",
    end_color="blue",
):
    print(line)

print()

for line in renderer.render(
    "DATABASE",
    font="big",
    start_color="green",
    end_color="teal",
):
    print(line)

print()

for line in renderer.render(
    "TESTS",
    font="big",
    start_color="yellow",
    end_color="orange",
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
    start_color="red",
    end_color="orange",
    border="solid",
    width=70,
    padding=2,
):
    print(line)

print()

for line in renderer.render(
    "GRADIENTS",
    font="slant",
    start_color="purple",
    end_color="pink",
    border="solid",
    width=70,
    padding=2,
):
    print(line)

print()

for line in renderer.render(
    "BORDERS",
    font="slant",
    start_color="blue",
    end_color="cyan",
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
    start_color="gold",
    end_color="orange",
    border="thick",
    width=60,
):
    print(line)

print()
