#!/usr/bin/env just --justfile

list:
    just -l

build:
    maturin develop
    pyo3-stubgen python_rust_cache ./
    cat python_rust_cache_extra.pyi >> ./python_rust_cache.pyi


lint:
    cargo clippy

sanity-check:
    maturin develop && python scripts/sanity_check.py

benchmark:
    maturin develop && python scripts/benchmark.py

run-fastapi-demo-dev:
    uvicorn scripts.fastapi_demo:app --reload

run-fastapi-demo-production:
    uvicorn scripts.fastapi_demo:app --workers 4 --host 0.0.0.0 --port 8000

# Run wrk to load test the API (install wrk with brew if needed)
load-test-fastapi-demo:
    wrk -t4 -c40 -d30s http://localhost:8000/get/foo
