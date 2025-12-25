"""Predefined StyleContext presets for common use cases.

These styles can be passed directly to Console.frame() or used as a base
for custom styles using dataclasses.replace().
"""

from styledconsole.core.context import StyleContext

# Status Styles
SUCCESS_STYLE = StyleContext(
    border_style="rounded",
    border_color="green",
    title="SUCCESS",
    title_color="green",
    padding=1,
)

WARNING_STYLE = StyleContext(
    border_style="rounded",
    border_color="yellow",
    title="WARNING",
    title_color="yellow",
    padding=1,
)

ERROR_STYLE = StyleContext(
    border_style="heavy",
    border_color="red",
    title="ERROR",
    title_color="red",
    padding=1,
)

INFO_STYLE = StyleContext(
    border_style="rounded",
    border_color="blue",
    title="INFO",
    title_color="blue",
    padding=1,
)

# Layout Styles
PANEL_STYLE = StyleContext(
    border_style="solid",
    padding=1,
    margin=1,
)

MINIMAL_STYLE = StyleContext(
    border_style="minimal",
    padding=0,
)
