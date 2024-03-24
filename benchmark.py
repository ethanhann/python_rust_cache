# import my_python_module.crusty as rust_lib
import json
import profile
import pickle

from crusty import set_string_item, get_string_item, set_binary_item, get_binary_item


def main():
    """
    Need to evaluate 3 test cases:
    1. set/get of PyString
        Set 3ms / Get 10ms
    2. set/get of python string / rust pickled binary data
        Set 1.384 / Get 0.534
    3. set/get of python pickled binary data / rust Vec<u8>
        Similar to case 2

    Conclusion (so far)... passing bytes through the function boundary is slow.

    :return:
    """
    print("Profiling...")
    with open("./large-file.json", 'r') as file:
        # Load the JSON data from the file
        big_str = file.read()
        # big_json = json.load(file)

    pickled_big_str = pickle.dumps(big_str)

    # This was... Set 3ms / Get 9ms
    print("Set/Get Big String")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(200):
    set_string_item("big_str", big_str)
    get_string_item("big_str")
    """, globals(), locals())
    profiler.print_stats()

    profiler = profile.Profile()
    # This was... Set ? / Get ?
    print("Set/Get Big Python Pickled Binary")
    profiler.runctx("""
for _ in range(10):
    set_binary_item("pickled_big_str", pickled_big_str)
    get_binary_item("pickled_big_str")
    """, globals(), locals())
    profiler.print_stats()


if __name__ == '__main__':
    main()
