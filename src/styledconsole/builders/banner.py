"""BannerBuilder for constructing Banner objects with a fluent API.

Example:
    >>> from styledconsole.builders import BannerBuilder
    >>>
    >>> # Simple banner
    >>> banner = (BannerBuilder()
    ...     .text("HELLO")
    ...     .font("slant")
    ...     .effect("fire")
    ...     .build())
    >>>
    >>> # Using factory method
    >>> title = BannerBuilder.title("MY APP").build()
"""

from __future__ import annotations

from styledconsole.builders.base import BaseBuilder, _resolve_effect
from styledconsole.model import Banner, Style


class BannerBuilder(BaseBuilder[Banner]):
    """Fluent builder for Banner objects.

    Provides a chainable API for constructing ASCII art banners
    with fonts, effects, and styling.

    Example:
        >>> banner = (BannerBuilder()
        ...     .text("WELCOME")
        ...     .font("banner")
        ...     .effect("ocean")
        ...     .build())
    """

    def __init__(self) -> None:
        """Initialize builder with default values."""
        self._text: str = ""
        self._font: str = "standard"
        self._effect: str | None = None
        self._style: Style | None = None

    def text(self, text: str) -> BannerBuilder:
        """Set banner text.

        Args:
            text: Text to render as ASCII art.

        Returns:
            Self for chaining.
        """
        self._text = text
        return self

    def font(self, font: str) -> BannerBuilder:
        """Set pyfiglet font.

        Args:
            font: Font name (e.g., "standard", "slant", "banner", "big").

        Returns:
            Self for chaining.
        """
        self._font = font
        return self

    def effect(self, effect: str | None) -> BannerBuilder:
        """Set visual effect.

        Args:
            effect: Effect preset name (e.g., "fire", "ocean", "rainbow")
                or None for no effect.

        Returns:
            Self for chaining.
        """
        self._effect = _resolve_effect(effect)
        return self

    def style(
        self,
        color: str | None = None,
        background: str | None = None,
        bold: bool = False,
    ) -> BannerBuilder:
        """Set text style.

        Args:
            color: Text color.
            background: Background color.
            bold: Bold text.

        Returns:
            Self for chaining.
        """
        self._style = Style(color=color, background=background, bold=bold)
        return self

    def _validate(self) -> list[str]:
        """Validate builder state."""
        errors = []
        if not self._text:
            errors.append("Banner text is required")
        return errors

    def _build(self) -> Banner:
        """Build the Banner object."""
        return Banner(
            text=self._text,
            font=self._font,
            effect=self._effect,
            style=self._style,
        )

    # Factory methods

    @classmethod
    def title(cls, text: str, effect: str = "ocean") -> BannerBuilder:
        """Create a title banner.

        Args:
            text: Title text.
            effect: Effect preset. Defaults to "ocean".

        Returns:
            Configured BannerBuilder.
        """
        return cls().text(text).effect(effect)

    @classmethod
    def header(cls, text: str) -> BannerBuilder:
        """Create a header banner with fire effect.

        Args:
            text: Header text.

        Returns:
            Configured BannerBuilder.
        """
        return cls().text(text).font("slant").effect("fire")


__all__ = ["BannerBuilder"]
