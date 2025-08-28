import time

from python_rust_cache import PyCache


def test_set_and_get_string_value():
    # Arrange
    cache = PyCache(10, None)
    key, value = "foo", b"bar"

    # Act
    cache.set(key, value)
    result = cache.get(key)

    # Assert
    assert result == value


def test_get_returns_none_for_missing_key():
    # Arrange
    cache = PyCache(10, None)
    key = "missing"

    # Act
    result = cache.get(key)

    # Assert
    assert result is None


def test_overwrite_value():
    # Arrange
    cache = PyCache(10, None)
    key = "foo"
    first_value = b"bar"
    second_value = b"baz"
    cache.set(key, first_value)

    # Act
    cache.set(key, second_value)
    result = cache.get(key)

    # Assert
    assert result == second_value


def test_cache_respects_capacity():
    # Arrange
    capacity = 1
    cache = PyCache(capacity, None)

    # Act
    cache.set("key1", b"value1")
    cache.set("key2", b"value2")

    # Allow Moka's background maintenance to catch up
    time.sleep(0.05)

    # Assert
    # Cache never exceeds capacity
    # (may contain "key1" or "key2" depending on LFU admission policy)
    # but length must be <= 1
    assert cache.len() <= capacity


def test_ttl_expires_entries(monkeypatch):
    # Arrange
    cache = PyCache(10, 1)  # TTL = 1 second
    cache.set("foo", b"bar")

    # Act
    import time
    time.sleep(1.5)  # wait until TTL expires
    result = cache.get("foo")

    # Assert
    assert result is None
