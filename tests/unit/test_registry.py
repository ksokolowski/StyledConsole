"""Tests for the Generic Registry system."""

import pytest

from styledconsole.core.registry import Registry


def test_registry_registration():
    """Test basic registration and retrieval."""
    registry = Registry[str]("test item")
    registry.register("item1", "value1")

    assert registry.get("item1") == "value1"
    assert registry.get("ITEM1") == "value1"  # Case-insensitive
    assert "item1" in registry
    assert "ITEM1" in registry
    assert len(registry) == 1


def test_registry_overwrite():
    """Test overwriting registrations."""
    registry = Registry[str]("test item")
    registry.register("item1", "value1")

    with pytest.raises(KeyError, match="already registered"):
        registry.register("item1", "value2")

    registry.register("item1", "value2", overwrite=True)
    assert registry.get("item1") == "value2"


def test_registry_missing_item():
    """Test error handling for missing items."""
    registry = Registry[str]("test item")
    registry.register("item1", "value1")

    with pytest.raises(KeyError, match="Unknown test item: 'missing'"):
        registry.get("missing")


def test_registry_list_all():
    """Test listing all registered names."""
    registry = Registry[str]("test item")
    registry.register("C", "val")
    registry.register("A", "val")
    registry.register("B", "val")

    assert registry.list_all() == ["a", "b", "c"]


def test_registry_dict_access():
    """Test dictionary-style access."""
    registry = Registry[str]("test item")
    registry.register("item1", "value1")

    assert registry["item1"] == "value1"
    assert registry["ITEM1"] == "value1"


def test_registry_attribute_access():
    """Test attribute-style access."""
    registry = Registry[str]("test item")
    registry.register("item1", "value1")

    assert registry.item1 == "value1"
    assert registry.ITEM1 == "value1"

    with pytest.raises(AttributeError, match="Unknown test item: 'missing'"):
        _ = registry.missing


def test_registry_attribute_access_private():
    """Test that private attributes are not intercepted by __getattr__."""
    registry = Registry[str]("test item")

    with pytest.raises(AttributeError, match="has no attribute '_private'"):
        _ = registry._private
