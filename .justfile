#!/usr/bin/env just --justfile

list:
    just -l

test:
    PYTHONPATH=. pytest

build:
    maturin develop

clean:
    cargo clean

format:
    cargo fmt

fix:
    cargo clippy --fix

lint:
    cargo clippy -- -W clippy::all
    ruff check .

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
