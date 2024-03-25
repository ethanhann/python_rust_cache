import json
import sys

from crusty import set_string_item, get_string_item, set_binary_item, get_binary_item, get_string_item_decompressed, \
    set_string_item_compressed, get_binary_item_decompressed, set_binary_item_compressed, print_cache_size


def print_size(val):
    size_in_bytes = sys.getsizeof(val)
    print(f"+++ Size in {size_in_bytes} bytes")


def main():
    """

    """
    data = {
        "Alice": {
            "age": 30,
            "city": "New York",
            "email": "alice@example.com"
        },
        "Bob": {
            "age": 25,
            "city": "Los Angeles",
            "email": "bob@example.com"
        },
        "Charlie": {
            "age": 35,
            "city": "Chicago",
            "email": "charlie@example.com"
        }
    }
    json_str = json.dumps(data)
    # pickled_big_str = pickle.dumps(json_str)
    big_bytes = bytes(json_str, "utf-8")
    key = "foo1"

    # Original Data
    print("\njson_str: ")
    print(json_str)
    print("\npickled_big_str: ")
    print(big_bytes)

    print("\nString Get/Set...")
    set_string_item(key, json_str)
    result = get_string_item(key)
    print_size(json_str)
    print_size(result)
    print_cache_size()
    print(result)

    print("\nBytes Get/Set...")
    set_binary_item(key, big_bytes)
    result = get_binary_item(key)
    print_size(big_bytes)
    print_size(result)
    print_cache_size()
    print(result)

    print("\nCompressed String Get/Set...")
    set_string_item_compressed(key, json_str)
    result = get_string_item_decompressed(key)
    print_size(result)
    print_cache_size()
    print(result)

    print("\nCompressed Bytes Get/Set...")
    set_binary_item_compressed(key, big_bytes)
    result = get_binary_item_decompressed(key)
    print_size(result)
    print_cache_size()
    print(result)


if __name__ == "__main__":
    main()
