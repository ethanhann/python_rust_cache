# import my_python_module.crusty as rust_lib
import json
import profile
import pickle

from crusty import set_string_item, get_string_item, set_binary_item, get_binary_item, get_string_item_decompressed, \
    set_string_item_compressed, get_binary_item_decompressed, set_binary_item_compressed, print_cache_size


def main():
    """
    Need to evaluate 3 test cases:
    1. set/get of PyString
        Set 3ms / Get 10ms
    2. set/get of python string / rust pickled binary data
        Set 3ms / Get 9ms
    3. set/get of python pickled binary data / rust Vec<u8>
        Set 1.384 / Get 0.534

    Conclusion (so far)... passing bytes through the function boundary is slow.

    :return:
    """
    print("Profiling...")
    with open("../large-file.json", 'r') as file:
        # Load the JSON data from the file
        big_str = file.read()

    # pickled_big_str = pickle.dumps(big_str)
    big_bytes = bytes(big_str, "utf-8")

    # This was... Set 3ms / Get 9ms
    print("Set/Get Big String")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(1):
    set_string_item("big_str", big_str)
    get_string_item("big_str")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()

    # This was... Set ? / Get ?
    print("Set/Get Big Python Binary")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(1):
    set_binary_item("big_bytes", big_bytes)
    get_binary_item("big_bytes")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()

    # This was... Set ? / Get ?
    print("Set/Get Compressed String")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(1):
    set_string_item_compressed("big_str", big_str)
    get_string_item_decompressed("big_str")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()

    # This was... Set ? / Get ?
    print("Set/Get Compressed Python Binary")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(1):
    set_binary_item_compressed("big_bytes", big_bytes)
    get_binary_item_decompressed("big_bytes")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()


if __name__ == '__main__':
    main()
