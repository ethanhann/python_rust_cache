use pyo3::prelude::*;
use std::collections::HashMap;
use lazy_static::lazy_static;
use std::sync::{Mutex};

lazy_static! {
    static ref CACHE: Mutex<HashMap<String, Vec<u8>>> = Mutex::new({
        let map = HashMap::new();
        map
    });
}

/*
 * Binary
 */
fn _get_binary_item(name: &str) -> Option<Vec<u8>> {
    let cache = CACHE.lock().unwrap();
    cache.get(name).cloned()
}

fn _set_binary_item(name: String, item: Vec<u8>) -> PyResult<()> {
    let mut cache = CACHE.lock().map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Mutex error: {}", e)))?;
    cache.insert(name, item);
    Ok(())
}

#[pyfunction]
fn get_binary_item(_py: Python, name: String) -> PyResult<Option<Vec<u8>>> {
    Ok(_get_binary_item(&name))
}

#[pyfunction]
fn set_binary_item(_py: Python, name: String, item: Vec<u8>) -> PyResult<()> {
    _set_binary_item(name, item)
}

/*
 * String
 */
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

#[pymodule]
fn crusty(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_string_item, m)?)?;
    m.add_function(wrap_pyfunction!(set_string_item, m)?)?;
    m.add_function(wrap_pyfunction!(get_binary_item, m)?)?;
    m.add_function(wrap_pyfunction!(set_binary_item, m)?)?;
    Ok(())
}
