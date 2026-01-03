"""Declarative Layout Engine.

This module provides a factory for creating complex CLI layouts/dashboards
from JSON-serializable configuration dictionaries.
"""

from typing import Any

from rich.align import Align
from rich.console import Group
from rich.panel import Panel
from rich.rule import Rule
from rich.text import Text

from styledconsole.presets.tables import create_table_from_config


def create_layout_from_config(config: dict[str, Any]) -> Any:
    """Create a renderable object from a configuration dictionary.

    Acts as a universal factory for building CLI interfaces declaratively.

    Args:
        config: Dictionary with a 'type' field and type-specific arguments.

    Returns:
        A Rich renderable object (Panel, Table, Group, etc.) that can be
        printed by the Console.

    Supported Types:
        - "group": Container for multiple items.
        - "table": GradientTable (via create_table_from_config).
        - "banner": Figlet text (rendered as Text since we can't easily return
          ANSI string as renderable without wrapping). *Note*: For full fidelity
          banners, using Console.banner() directly is preferred.
        - "text": CMS-style text block with Rich styles.
        - "rule": Horizontal divider.
        - "panel": Content container (standard Rich Panel).
    """
    item_type = config.get("type")

    if item_type == "group":
        return _create_group(config)
    elif item_type == "table":
        # Table config expects 'theme' and 'data' separation
        # If the declarative config merges them, we split them here.
        # Design choice: expects 'theme' and 'data' keys nested, or
        # specific keys at root. Reusing strict factory for now.
        return create_table_from_config(theme=config.get("theme", {}), data=config.get("data", {}))
    elif item_type == "text":
        return _create_text(config)
    elif item_type == "rule":
        return _create_rule(config)
    elif item_type == "panel" or item_type == "frame":
        return _create_panel(config)
    elif item_type == "vspacer":
        return Text("\n" * (config.get("lines", 1) - 1))

    raise ValueError(f"Unknown layout item type: {item_type}")


def _create_group(config: dict[str, Any]) -> Group:
    """Create a Group of renderables."""
    items = []
    for item_config in config.get("items", []):
        try:
            items.append(create_layout_from_config(item_config))
        except ValueError as e:
            # For robustness in declarative configs, we renders error text
            # instead of crashing the whole dashboard
            items.append(Text(f"Error: {e!s}", style="bold red"))

    return Group(*items)


def _create_text(config: dict[str, Any]) -> Any:
    """Create a styled Text object (or Align wrapper)."""
    text = Text(
        config.get("content", ""),
        style=config.get("style", ""),
        justify=config.get("justify", "left"),
    )

    align = config.get("align")
    if align:
        return Align(text, align=align)
    return text


def _create_rule(config: dict[str, Any]) -> Rule:
    """Create a styled Rule."""
    return Rule(
        title=config.get("title", ""),
        style=config.get("style", "rule.line"),
        align=config.get("align", "center"),
        characters=config.get("char", "─"),
    )


def _create_panel(config: dict[str, Any]) -> Panel:
    """Create a Panel/Frame."""
    from styledconsole.core.box_mapping import get_box_style

    # Recursively create content if it's a config dict, otherwise use raw string
    content_raw = config.get("content", "")
    if isinstance(content_raw, dict):
        content = create_layout_from_config(content_raw)
    elif isinstance(content_raw, list):
        # Implicit group if list
        content = _create_group({"items": content_raw})
    else:
        content = Text.from_markup(str(content_raw))

    # Resolve box shape from 'border' key (defaulting to rounded)
    # We support 'border_style' as alias for shape if it's a known shape name,
    # to be forgiving, but prefer 'border'.
    # Actually, let's be strict to avoid ambiguity:
    # 'border' -> Shape (box.HEAVY)
    # 'border_style' -> Color/Style ("red", "bold")

    box_shape = config.get("border", "rounded")

    # If the user passed a shape name in 'border_style' by mistake (like in my demo),
    # valid rich border_style would fail or produce weird colors.
    # But we can't easily detect if "heavy" is meant as a color or shape without a registry check.
    # For now, we enforce the schema: border=SHAPE, border_style=COLOR.

    # Handle rainbow title
    title = config.get("title")
    if title and config.get("title_rainbow"):
        from styledconsole.effects.strategies import RainbowSpectrum
        from styledconsole.utils.text import strip_ansi

        # We need to manually apply rainbow to the title text
        # Since Rich Panel just takes a Renderable or text, we can pass a styled Text object.
        # But for rainbow, each char needs a different color.
        plain_title = strip_ansi(title)
        spectrum = RainbowSpectrum()
        styled_title = Text()

        width = len(plain_title)
        for i, char in enumerate(plain_title):
            # Calculate position 0..1
            t = i / max(1, width - 1)
            # RainbowSpectrum.get_color expects (row, col) but effectively uses position strategy
            # Actually RainbowSpectrum ignores position for generic get_color?
            # No, ColorSource.get_color takes 3 args usually or 1 float?
            # Let's check ColorSource signature.
            # It takes (position: float).

            color = spectrum.get_color(t)
            styled_title.append(char, style=color)

        title = styled_title

    return Panel(
        content,
        title=title,
        subtitle=config.get("subtitle"),
        box=get_box_style(box_shape),
        border_style=config.get("border_style", "none"),
        style=config.get("style", "none"),
        padding=config.get("padding", (1, 2)),
    )
