#!/usr/bin/env just --justfile

release:
  cargo build --release    

lint:
  cargo clippy

bin:
  cargo run --bin bin -- arg1

sanity-check:
	maturin develop && python scripts/sanity_check.py

benchmark:
	maturin develop && python scripts/benchmark.py
