use pyo3::prelude::*;
use std::collections::HashMap;
use lazy_static::lazy_static;
use std::sync::{Mutex};

lazy_static! {
    static ref CACHE: Mutex<HashMap<String, String>> = Mutex::new({
        let mut map = HashMap::new();
        map
    });
}

fn _get_item(name: &str) -> String {
    let cache = CACHE.lock().unwrap();
    cache.get(name).cloned().unwrap_or_else(|| String::from("Item not found"))
}

#[pyfunction]
fn get_item(_py: Python, name: String) -> PyResult<String> {
    Ok(_get_item(&name))
}

fn _set_item(name: String, item: String) -> PyResult<()> {
    let mut cache = CACHE.lock().map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Mutex error: {}", e)))?;
    cache.insert(name, item);
    Ok(())
}

#[pyfunction]
fn set_item(_py: Python, name: String, item: String) -> PyResult<()> {
    _set_item(name, item)
}

#[pymodule]
fn crusty(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_item, m)?)?;
    m.add_function(wrap_pyfunction!(set_item, m)?)?;
    Ok(())
}
