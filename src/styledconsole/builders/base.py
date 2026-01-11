"""Base classes and protocols for the builder layer.

This module defines the Builder protocol that all builders implement,
providing a consistent fluent API for constructing ConsoleObjects.

Example:
    >>> from styledconsole.builders import FrameBuilder
    >>>
    >>> frame = (FrameBuilder()
    ...     .content("Hello World")
    ...     .title("Greeting")
    ...     .effect("ocean")
    ...     .build())
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Protocol, TypeVar, runtime_checkable

from typing_extensions import Self

if TYPE_CHECKING:
    from styledconsole.console import Console
    from styledconsole.model import ConsoleObject

T = TypeVar("T", bound="ConsoleObject", covariant=True)


@runtime_checkable
class Builder(Protocol[T]):
    """Protocol for all builders.

    Builders provide a fluent API for constructing ConsoleObjects.
    Each builder:
    - Uses method chaining (returns self)
    - Validates during build()
    - Returns an immutable ConsoleObject

    Example:
        >>> class MyBuilder(Builder[MyObject]):
        ...     def build(self) -> MyObject:
        ...         errors = self.validate()
        ...         if errors:
        ...             raise ValueError(errors)
        ...         return MyObject(...)
        ...
        ...     def validate(self) -> list[str]:
        ...         return []
    """

    def build(self) -> T:
        """Construct the final ConsoleObject.

        Returns:
            Immutable ConsoleObject instance.

        Raises:
            ValueError: If validation fails.
        """
        ...

    def validate(self) -> list[str]:
        """Validate builder state.

        Returns:
            List of validation error messages. Empty if valid.
        """
        ...


class BaseBuilder(Generic[T]):
    """Base class for builders with common functionality.

    Provides shared validation and error handling logic.
    Subclasses should override _validate() and _build().
    """

    _console: Console | None = None

    def _bind_console(self, console: Console) -> Self:
        """Bind this builder to a Console for rendering.

        This is called internally by Console.build_*() methods.

        Args:
            console: Console to bind.

        Returns:
            Self for chaining.
        """
        self._console = console
        return self

    def render(self) -> None:
        """Build and render the object to the bound console.

        This is a convenience method that builds the object and
        renders it in one step.

        Raises:
            RuntimeError: If no console is bound.
            ValueError: If validation fails.
        """
        if self._console is None:
            raise RuntimeError(
                "No console bound. Use console.build_frame() or bind with _bind_console()."
            )
        obj = self.build()
        self._console.render_object(obj)

    def validate(self) -> list[str]:
        """Validate builder state.

        Returns:
            List of validation error messages.
        """
        return self._validate()

    def _validate(self) -> list[str]:
        """Subclass hook for validation logic.

        Override this to add type-specific validation.
        """
        return []

    def build(self) -> T:
        """Build the ConsoleObject.

        Validates state and constructs the object.

        Returns:
            Immutable ConsoleObject instance.

        Raises:
            ValueError: If validation fails.
        """
        errors = self.validate()
        if errors:
            raise ValueError(f"Invalid builder state: {'; '.join(errors)}")
        return self._build()

    def _build(self) -> T:
        """Subclass hook for object construction.

        Override this to implement type-specific building.
        """
        raise NotImplementedError("Subclasses must implement _build()")


def _resolve_effect(effect: str | Any | None) -> str | None:
    """Resolve effect to string preset name.

    Args:
        effect: Effect preset name, EffectSpec, or None.

    Returns:
        Effect name string or None.
    """
    if effect is None:
        return None
    if isinstance(effect, str):
        return effect
    # If it's an EffectSpec, get its name
    if hasattr(effect, "name"):
        name = effect.name
        return str(name) if name is not None else None
    return str(effect)


__all__ = ["BaseBuilder", "Builder", "_resolve_effect"]
