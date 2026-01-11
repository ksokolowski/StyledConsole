"""FrameBuilder for constructing Frame objects with a fluent API.

Example:
    >>> from styledconsole.builders import FrameBuilder
    >>>
    >>> # Simple frame
    >>> frame = (FrameBuilder()
    ...     .content("Hello World")
    ...     .title("Greeting")
    ...     .border("rounded")
    ...     .effect("ocean")
    ...     .build())
    >>>
    >>> # Using factory methods
    >>> info = FrameBuilder.info("Operation completed", "Status").build()
    >>> warning = FrameBuilder.warning("Disk space low", "Alert").build()
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from styledconsole.builders.base import BaseBuilder, _resolve_effect
from styledconsole.model import Frame, Style, Text

if TYPE_CHECKING:
    from styledconsole.model import ConsoleObject


class FrameBuilder(BaseBuilder[Frame]):
    """Fluent builder for Frame objects.

    Provides a chainable API for constructing frames with content,
    titles, borders, effects, and styling.

    Example:
        >>> frame = (FrameBuilder()
        ...     .content("Hello")
        ...     .title("Greeting")
        ...     .border("rounded")
        ...     .effect("ocean")
        ...     .width(40)
        ...     .build())
    """

    def __init__(self) -> None:
        """Initialize builder with default values."""
        self._content: ConsoleObject | None = None
        self._title: str | None = None
        self._subtitle: str | None = None
        self._border: str = "solid"
        self._effect: str | None = None
        self._width: int | None = None
        self._padding: int = 1
        self._align: Literal["left", "center", "right"] = "left"
        self._style: Style | None = None

    def content(self, content: str | ConsoleObject | list[str]) -> FrameBuilder:
        """Set frame content.

        Args:
            content: Text string, list of lines, or ConsoleObject.

        Returns:
            Self for chaining.
        """
        if isinstance(content, str):
            self._content = Text(content=content)
        elif isinstance(content, list):
            self._content = Text(content="\n".join(content))
        else:
            self._content = content
        return self

    def title(self, title: str) -> FrameBuilder:
        """Set frame title.

        Args:
            title: Title text displayed in the border.

        Returns:
            Self for chaining.
        """
        self._title = title
        return self

    def subtitle(self, subtitle: str) -> FrameBuilder:
        """Set frame subtitle.

        Args:
            subtitle: Subtitle text displayed below the title.

        Returns:
            Self for chaining.
        """
        self._subtitle = subtitle
        return self

    def border(self, border: str) -> FrameBuilder:
        """Set border style.

        Args:
            border: Border style name (e.g., "solid", "rounded", "heavy", "double").

        Returns:
            Self for chaining.
        """
        self._border = border
        return self

    def effect(self, effect: str | None) -> FrameBuilder:
        """Set visual effect.

        Args:
            effect: Effect preset name (e.g., "ocean", "fire", "rainbow")
                or None for no effect.

        Returns:
            Self for chaining.
        """
        self._effect = _resolve_effect(effect)
        return self

    def width(self, width: int) -> FrameBuilder:
        """Set explicit frame width.

        Args:
            width: Width in characters. Must be at least 3.

        Returns:
            Self for chaining.
        """
        self._width = width
        return self

    def padding(self, padding: int) -> FrameBuilder:
        """Set internal padding.

        Args:
            padding: Padding spaces around content.

        Returns:
            Self for chaining.
        """
        self._padding = padding
        return self

    def align(self, align: Literal["left", "center", "right"]) -> FrameBuilder:
        """Set content alignment.

        Args:
            align: Alignment within frame.

        Returns:
            Self for chaining.
        """
        self._align = align
        return self

    def style(
        self,
        color: str | None = None,
        background: str | None = None,
        bold: bool = False,
        italic: bool = False,
        underline: bool = False,
        dim: bool = False,
    ) -> FrameBuilder:
        """Set text style.

        Args:
            color: Text color.
            background: Background color.
            bold: Bold text.
            italic: Italic text.
            underline: Underlined text.
            dim: Dimmed text.

        Returns:
            Self for chaining.
        """
        self._style = Style(
            color=color,
            background=background,
            bold=bold,
            italic=italic,
            underline=underline,
            dim=dim,
        )
        return self

    def _validate(self) -> list[str]:
        """Validate builder state."""
        errors = []
        if self._content is None:
            errors.append("Frame content is required")
        if self._width is not None and self._width < 3:
            errors.append("Frame width must be at least 3")
        if self._padding < 0:
            errors.append("Padding cannot be negative")
        return errors

    def _build(self) -> Frame:
        """Build the Frame object."""
        return Frame(
            content=self._content,
            title=self._title,
            subtitle=self._subtitle,
            border=self._border,
            effect=self._effect,
            width=self._width,
            padding=self._padding,
            align=self._align,
            style=self._style,
        )

    # Factory methods for common patterns

    @classmethod
    def info(cls, content: str, title: str = "Info") -> FrameBuilder:
        """Create a pre-configured info frame.

        Args:
            content: Frame content.
            title: Frame title. Defaults to "Info".

        Returns:
            Configured FrameBuilder.
        """
        return cls().content(content).title(title).effect("ocean").border("rounded")

    @classmethod
    def success(cls, content: str, title: str = "Success") -> FrameBuilder:
        """Create a pre-configured success frame.

        Args:
            content: Frame content.
            title: Frame title. Defaults to "Success".

        Returns:
            Configured FrameBuilder.
        """
        return cls().content(content).title(title).effect("forest").border("rounded")

    @classmethod
    def warning(cls, content: str, title: str = "Warning") -> FrameBuilder:
        """Create a pre-configured warning frame.

        Args:
            content: Frame content.
            title: Frame title. Defaults to "Warning".

        Returns:
            Configured FrameBuilder.
        """
        return cls().content(content).title(title).effect("fire").border("heavy")

    @classmethod
    def error(cls, content: str, title: str = "Error") -> FrameBuilder:
        """Create a pre-configured error frame.

        Args:
            content: Frame content.
            title: Frame title. Defaults to "Error".

        Returns:
            Configured FrameBuilder.
        """
        return cls().content(content).title(title).effect("fire").border("double")


__all__ = ["FrameBuilder"]
