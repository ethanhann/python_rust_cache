from fastapi import FastAPI
from python_rust_cache import (
    set_string_item, get_string_item,
    set_binary_item, get_binary_item,
    get_string_item_decompressed, set_string_item_compressed,
    get_binary_item_decompressed, set_binary_item_compressed,
    print_cache_size,
    __version__,
)

app = FastAPI()


@app.get("/")
def root():
    return {"version": __version__}


@app.get("/set/{key}/{value}")
def set_item(key: str, value: str):
    set_string_item(key, value)
    return {"key": key, "value": value}


@app.get("/get/{key}")
def get_item(key: str):
    return {"key": key, "value": get_string_item(key)}


@app.get("/set_compressed/{key}/{value}")
def set_compressed_item(key: str, value: str):
    set_string_item_compressed(key, value)
    return {"key": key, "value": value}


@app.get("/get_compressed/{key}")
def get_compressed_item(key: str):
    return {"key": key, "value": get_string_item_decompressed(key)}


@app.get("/set_binary/{key}/{value}")
def set_binary_item(key: str, value: str):
    set_binary_item(key, value)
    return {"key": key, "value": value}


@app.get("/get_binary/{key}")
def get_binary_item(key: str):
    return {"key": key, "value": get_binary_item(key)}


@app.get("/set_binary_compressed/{key}/{value}")
def set_binary_compressed_item(key: str, value: str):
    set_binary_item_compressed(key, value)
    return {"key": key, "value": value}


@app.get("/get_binary_compressed/{key}")
def get_binary_compressed_item(key: str):
    return {"key": key, "value": get_binary_item_decompressed(key)}


@app.get("/size")
def get_size():
    return {"size": print_cache_size()}
