"""Generic registry system for terminal-agnostic components."""

from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class Registry(Generic[T]):
    """Generic base class for case-insensitive item registries.

    Provides a standard interface for registration and retrieval of items,
    ensuring consistent behavior across different components.
    """

    def __init__(self, item_type_name: str) -> None:
        """Initialize registry.

        Args:
            item_type_name: Readable name of items (e.g., 'border style', 'icon').
                Used in error messages.
        """
        self._items: dict[str, T] = {}
        self._item_type_name = item_type_name

    def register(self, name: str, item: T, overwrite: bool = False) -> None:
        """Register a new item.

        Args:
            name: Case-insensitive name for the item.
            item: The item object to register.
            overwrite: If True, allows overwriting existing registration.

        Raises:
            KeyError: If item name already exists and overwrite is False.
        """
        name_lower = name.lower()
        if not overwrite and name_lower in self._items:
            raise KeyError(
                f"{self._item_type_name.capitalize()} '{name}' is already registered. "
                f"Set overwrite=True to replace it."
            )
        self._items[name_lower] = item

    def get(self, name: str) -> T:
        """Retrieve an item by name.

        Args:
            name: Case-insensitive name of the item.

        Returns:
            The registered item.

        Raises:
            KeyError: If item name is not found.
        """
        name_lower = name.lower()
        if name_lower not in self._items:
            available = ", ".join(sorted(self._items.keys()))
            raise KeyError(
                f"Unknown {self._item_type_name}: {name!r}. Available styles: {available}"
            )
        return self._items[name_lower]

    def list_all(self) -> list[str]:
        """Return sorted list of all registered names."""
        return sorted(self._items.keys())

    def items(self):
        """Return iterator over (name, item) pairs."""
        return self._items.items()

    def keys(self):
        """Return iterator over names."""
        return self._items.keys()

    def values(self):
        """Return iterator over items."""
        return self._items.values()

    def __iter__(self):
        """Iterate over names."""
        return iter(self._items)

    def __contains__(self, name: str) -> bool:
        """Check if an item name exists."""
        return name.lower() in self._items

    def __getitem__(self, name: str) -> T:
        """Allow dict-style access."""
        return self.get(name)

    def __len__(self) -> int:
        """Return number of registered items."""
        return len(self._items)

    def __getattr__(self, name: str) -> T:
        """Allow attribute-style access to items."""
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        try:
            return self.get(name)
        except KeyError as e:
            raise AttributeError(str(e)) from e
