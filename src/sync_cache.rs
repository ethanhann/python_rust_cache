use moka::sync::Cache;
use pyo3::prelude::*;
use std::time::Duration;
use pyo3::types::PyBytes;

#[pyclass]
pub struct PyCache {
    inner: Cache<String, Vec<u8>>,
}

#[pymethods]
impl PyCache {
    #[new]
    fn new(capacity: u64, ttl_secs: Option<u64>) -> Self {
        let mut builder = Cache::builder().max_capacity(capacity);
        if let Some(ttl) = ttl_secs {
            builder = builder.time_to_live(Duration::from_secs(ttl));
        }
        Self {
            inner: builder.build(),
        }
    }

    fn get(&self, key: String, py: Python<'_>) -> Option<Py<PyBytes>> {
        self.inner
            .get(&key)
            .map(|bytes| PyBytes::new(py, &bytes).unbind())
    }

    fn set(&self, key: String, value: &Bound<'_, PyBytes>) {
        self.inner.insert(key, value.as_bytes().to_vec());
    }
}
