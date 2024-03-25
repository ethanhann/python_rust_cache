import profile

from crusty import set_string_item, get_string_item, set_binary_item, get_binary_item, get_string_item_decompressed, \
    set_string_item_compressed, get_binary_item_decompressed, set_binary_item_compressed, print_cache_size


def main():
    print("Profiling...")
    with open("./large-file.json", 'r') as file:
        big_str = file.read()

    big_bytes = bytes(big_str, "utf-8")
    iterations = 10

    # This was... Set 3ms / Get 9ms
    print("Set/Get Big String")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(iterations):
    set_string_item("big_str", big_str)
    get_string_item("big_str")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()

    # This was... Set ? / Get ?
    print("Set/Get Big Python Binary")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(iterations):
    set_binary_item("big_bytes", big_bytes)
    get_binary_item("big_bytes")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()

    # This was... Set ? / Get ?
    print("Set/Get Compressed String")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(iterations):
    set_string_item_compressed("big_str", big_str)
    get_string_item_decompressed("big_str")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()

    # This was... Set ? / Get ?
    print("Set/Get Compressed Python Binary")
    profiler = profile.Profile()
    profiler.runctx("""
for _ in range(iterations):
    set_binary_item_compressed("big_bytes", big_bytes)
    get_binary_item_decompressed("big_bytes")
    print_cache_size()
    """, globals(), locals())
    profiler.print_stats()


if __name__ == '__main__':
    main()
