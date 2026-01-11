"""Builder layer for StyledConsole - fluent API for constructing ConsoleObjects.

This module provides builder classes that implement the builder pattern,
allowing fluent construction of console output objects.

Key Features:
- Method chaining for readable construction
- Validation during build()
- Factory methods for common patterns
- Type-safe with full IDE support

Example:
    >>> from styledconsole.builders import (
    ...     FrameBuilder,
    ...     BannerBuilder,
    ...     TableBuilder,
    ...     LayoutBuilder,
    ... )
    >>>
    >>> # Build a frame
    >>> frame = (FrameBuilder()
    ...     .content("Hello World")
    ...     .title("Greeting")
    ...     .effect("ocean")
    ...     .build())
    >>>
    >>> # Build a banner
    >>> banner = (BannerBuilder()
    ...     .text("WELCOME")
    ...     .font("slant")
    ...     .effect("fire")
    ...     .build())
    >>>
    >>> # Build a table
    >>> table = (TableBuilder()
    ...     .columns("Name", "Status")
    ...     .add_row("API", "Online")
    ...     .add_row("DB", "Online")
    ...     .effect("steel")
    ...     .build())
    >>>
    >>> # Build a layout
    >>> dashboard = (LayoutBuilder()
    ...     .vertical()
    ...     .gap(1)
    ...     .add(banner)
    ...     .add(LayoutBuilder.row(frame, table).build())
    ...     .build())
    >>>
    >>> # Using factory methods
    >>> info_frame = FrameBuilder.info("Task completed", "Status").build()
    >>> warning_frame = FrameBuilder.warning("Low disk space", "Alert").build()
"""

from styledconsole.builders.banner import BannerBuilder
from styledconsole.builders.base import BaseBuilder, Builder
from styledconsole.builders.frame import FrameBuilder
from styledconsole.builders.layout import LayoutBuilder
from styledconsole.builders.table import TableBuilder

__all__ = [
    "BannerBuilder",
    "BaseBuilder",
    "Builder",
    "FrameBuilder",
    "LayoutBuilder",
    "TableBuilder",
]
