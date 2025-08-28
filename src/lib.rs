use std::collections::HashMap;
use std::sync::{Mutex};
use lazy_static::lazy_static;
use pyo3::prelude::*;
use pyo3::types::PyBytes;

lazy_static! {
    static ref CACHE: Mutex<HashMap<String, Vec<u8>>> = Mutex::new({
        let map = HashMap::new();
        map
    });
}

/// Compression
fn compress(bytes: &[u8]) -> Vec<u8> {
    let level = 3;
    zstd::encode_all(bytes, level).unwrap()
}

fn decompress(compressed_data: &[u8]) -> Vec<u8> {
    zstd::decode_all(compressed_data).unwrap()
}

/// Internal Binary Get/Set
fn _get_binary_item(name: &str) -> Option<Vec<u8>> {
    let cache = CACHE.lock().unwrap();
    cache.get(name).cloned()
}

fn _set_binary_item(name: String, item: Vec<u8>) -> PyResult<()> {
    let mut cache = CACHE.lock().map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Mutex error: {}", e)))?;
    cache.insert(name, item);
    Ok(())
}

/// Python API
#[pyfunction]
fn print_cache_size() {
    // Acquire lock and clone the map
    let cache = CACHE.lock().unwrap();
    let cloned_map = cache.clone();

    // Serialize the map to CBOR
    let serialized_map = serde_cbor::to_vec(&cloned_map).expect("Serialization failed");

    let size_in_mb = serialized_map.len() as f64 / (1024.0 * 1024.0);

    println!("+++ Size of the map in bytes: {} bytes", serialized_map.len());
    println!("+++ Size of the map in megabytes: {:.2} MB", size_in_mb);
}

/// Python API no compression
#[pyfunction]
fn get_binary_item(_py: Python, name: String) -> PyResult<Py<PyBytes>> {
    let result = _get_binary_item(&name);
    let buf = result.unwrap_or_else(Vec::new);
    let pybytes_bound = PyBytes::new(_py, &buf);
    Ok(pybytes_bound.unbind())
}

#[pyfunction]
fn set_binary_item(_py: Python, name: String, item: &Bound<'_, PyBytes>) -> PyResult<()> {
    let item_as_bytes = item.as_bytes().to_vec();
    _set_binary_item(name, item_as_bytes)
}

#[pyfunction]
fn get_string_item(_py: Python, name: String) -> PyResult<String> {
    let maybe_bytes_data = _get_binary_item(&name);
    let bytes_data: Vec<u8> = maybe_bytes_data.unwrap_or_else(Vec::new);
    let string_data = String::from_utf8(bytes_data).expect("Invalid UTF-8 sequence");
    Ok(string_data)
}

#[pyfunction]
fn set_string_item(_py: Python, name: String, item: String) -> PyResult<()> {
    _set_binary_item(name, item.as_bytes().to_vec())
}

/// Python API with compression
#[pyfunction]
fn get_binary_item_decompressed(_py: Python, name: String) -> PyResult<Py<PyBytes>> {
    let item = _get_binary_item(&name);
    let buf = item.unwrap_or_else(Vec::new);
    let decompressed_item = decompress(buf.as_slice());
    let pybytes_bound = PyBytes::new(_py, &decompressed_item);
    Ok(pybytes_bound.unbind())
}

#[pyfunction]
fn set_binary_item_compressed(_py: Python, name: String, item: &Bound<'_, PyBytes>) -> PyResult<()> {
    let compressed_item = compress(item.as_bytes());
    _set_binary_item(name, compressed_item)
}

#[pyfunction]
fn get_string_item_decompressed(_py: Python, name: String) -> PyResult<String> {
    let maybe_bytes_data = _get_binary_item(&name);
    let bytes_data: Vec<u8> = maybe_bytes_data.unwrap_or_else(Vec::new);
    let decompressed_item = decompress(bytes_data.as_slice());
    let string_data = String::from_utf8(decompressed_item).expect("Invalid UTF-8 sequence");
    Ok(string_data)
}

#[pyfunction]
fn set_string_item_compressed(_py: Python, name: String, item: String) -> PyResult<()> {
    let compressed_item = compress(item.as_bytes());
    _set_binary_item(name, compressed_item)
}

#[pymodule]
fn python_rust_cache(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Profiling
    m.add_function(wrap_pyfunction!(print_cache_size, m)?)?;
    // Basic
    m.add_function(wrap_pyfunction!(get_string_item, m)?)?;
    m.add_function(wrap_pyfunction!(set_string_item, m)?)?;
    m.add_function(wrap_pyfunction!(get_binary_item, m)?)?;
    m.add_function(wrap_pyfunction!(set_binary_item, m)?)?;
    // Compressed
    m.add_function(wrap_pyfunction!(get_string_item_decompressed, m)?)?;
    m.add_function(wrap_pyfunction!(set_string_item_compressed, m)?)?;
    m.add_function(wrap_pyfunction!(get_binary_item_decompressed, m)?)?;
    m.add_function(wrap_pyfunction!(set_binary_item_compressed, m)?)?;
    Ok(())
}
