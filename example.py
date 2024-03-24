# import my_python_module.crusty as rust_lib
import json
import pickle

from crusty import set_string_item, get_string_item, set_binary_item, get_binary_item, get_string_item_decompressed, \
    set_string_item_compressed, get_binary_item_decompressed, set_binary_item_compressed, print_cache_size


def main():
    """
    Need to evaluate 3 test cases:
    1. set/get of PyString
    2. set/get of python pickled binary data
    3. set/get of rust pickled binary data
    ... and maybe some other cases involving JSON serialization.
    :return:
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
    pickled_big_str = pickle.dumps(json_str)

    print("String Get/Set...")
    key = "foo1"
    set_string_item(key, json_str)
    result = get_string_item(key)
    print(result)

    print("Bytes Get/Set...")
    key = "foo2"
    set_binary_item(key, pickled_big_str)
    result = get_binary_item(key)
    print(result)

    print("Compressed String Get/Set...")
    key = "foo3"
    set_string_item_compressed(key, json_str)
    result = get_string_item_decompressed(key)
    print(result)

    print("Compressed Bytes Get/Set...")
    key = "foo4"
    set_binary_item_compressed(key, pickled_big_str)
    result = get_binary_item_decompressed(key)
    print(result)


if __name__ == '__main__':
    main()
