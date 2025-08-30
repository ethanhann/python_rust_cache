import asyncio
import pytest
from python_rust_cache import PyAsyncCache


@pytest.mark.asyncio
async def test_set_and_get_string_value():
    # Arrange
    cache = PyAsyncCache(10, None)
    key, value = "foo", b"bar"

    # Act
    await cache.set(key, value)
    result = await cache.get(key)

    # Assert
    assert result == value


@pytest.mark.asyncio
async def test_get_returns_none_for_missing_key():
    # Arrange
    cache = PyAsyncCache(10, None)
    key = "missing"

    # Act
    result = await cache.get(key)

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_overwrite_value():
    # Arrange
    cache = PyAsyncCache(10, None)
    key = "foo"
    first_value = b"bar"
    second_value = b"baz"
    await cache.set(key, first_value)

    # Act
    await cache.set(key, second_value)
    result = await cache.get(key)

    # Assert
    assert result == second_value


@pytest.mark.asyncio
async def test_cache_respects_capacity():
    # Arrange
    capacity = 1
    cache = PyAsyncCache(capacity, None)

    # Act
    await cache.set("key1", b"value1")
    await cache.set("key2", b"value2")

    # Allow Moka's background maintenance to catch up
    await asyncio.sleep(0.05)

    # Assert
    assert cache.len() <= capacity


@pytest.mark.asyncio
async def test_ttl_expires_entries():
    # Arrange
    cache = PyAsyncCache(10, 1)
    await cache.set("foo", b"bar")

    # Act
    await asyncio.sleep(1.5)  # wait until TTL expires
    result = await cache.get("foo")

    # Assert
    assert result is None
