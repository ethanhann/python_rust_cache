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


def test_eviction_when_over_capacity():
    # Arrange
    cache = PyCache(1, None)  # capacity 1
    cache.set("key1", b"value1")

    # Act
    cache.set("key2", b"value2")
    result1 = cache.get("key1")
    result2 = cache.get("key2")

    # Assert
    assert result1 is None
    assert result2 == b"value2"


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
