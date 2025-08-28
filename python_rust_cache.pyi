# flake8: noqa: PYI021
def get_binary_item(name):
    """Python API no compression"""

def get_binary_item_decompressed(name):
    """Python API with compression"""

def get_string_item(name):
    ...

def get_string_item_decompressed(name):
    ...

def print_cache_size():
    """Python API"""

def set_binary_item(name, item):
    ...

def set_binary_item_compressed(name, item):
    ...

def set_string_item(name, item):
    ...

def set_string_item_compressed(name, item):
    ...
# Variable Annotations
__version__: str
