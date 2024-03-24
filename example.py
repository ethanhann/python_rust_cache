# import my_python_module.crusty as rust_lib
import json
import pickle

from crusty import set_string_item, get_string_item, set_binary_item, get_binary_item


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
    print("String Get/Set...")
    json_str = json.dumps(data)
    set_string_item("foo", json_str)
    result = get_string_item("foo")
    print(result)

    print("Bytes Get/Set...")
    pickled_big_str = pickle.dumps(json_str)
    set_binary_item("bytes", pickled_big_str)
    result = get_binary_item("bytes")
    print(result)


if __name__ == '__main__':
    main()
