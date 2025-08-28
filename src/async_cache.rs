use pyo3::Py;
use std::time::Duration;
use moka::future::{Cache as AsyncCache, CacheBuilder};
use pyo3::{pyclass, pymethods, Bound, PyAny, PyResult, Python};
use pyo3::types::{PyBytes, PyBytesMethods};
use pyo3_async_runtimes::tokio::future_into_py;

#[pyclass]
pub struct PyAsyncCache {
    inner: AsyncCache<String, Vec<u8>>,
}

#[pymethods]
impl PyAsyncCache {
    #[new]
    fn new(capacity: u64, ttl_secs: Option<u64>) -> Self {
        let mut builder = CacheBuilder::new(capacity);
        if let Some(ttl) = ttl_secs {
            builder = builder.time_to_live(Duration::from_secs(ttl));
        }
        Self {
            inner: builder.build(),
        }
    }

    fn get<'a>(&'a self, key: String, py: Python<'a>) -> PyResult<Bound<'a, PyAny>> {
        let inner = self.inner.clone();
        future_into_py(py, async move {
            let v_opt = inner.get(&key).await;
            Python::with_gil(|py| {
                let any: Py<PyAny> = match v_opt {
                    Some(v) => PyBytes::new(py, &v).unbind().into_any(),
                    None => py.None().into_any(),
                };
                Ok(any)
            })
        })
    }

    fn set<'a>(&'a self, key: String, value: &Bound<'a, PyBytes>, py: Python<'a>) -> PyResult<Bound<'a, PyAny>> {
        let inner = self.inner.clone();
        let v = value.as_bytes().to_vec();
        future_into_py(py, async move {
            inner.insert(key, v).await;
            Python::with_gil(|py| Ok(py.None().into_any()))
        })
    }
}
