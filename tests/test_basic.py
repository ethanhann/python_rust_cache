
def test_import():
    import python_rust_cache
    assert hasattr(python_rust_cache, "__version__")
    assert hasattr(python_rust_cache, "set_string_item")
    assert hasattr(python_rust_cache, "get_string_item")
    assert hasattr(python_rust_cache, "set_binary_item")
    assert hasattr(python_rust_cache, "get_binary_item")
    assert hasattr(python_rust_cache, "print_cache_size")
    assert hasattr(python_rust_cache, "set_string_item_compressed")
    assert hasattr(python_rust_cache, "get_string_item_decompressed")
    assert hasattr(python_rust_cache, "set_binary_item_compressed")
    assert hasattr(python_rust_cache, "get_binary_item_decompressed")
