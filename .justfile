#!/usr/bin/env just --justfile

release:
  cargo build --release    

lint:
  cargo clippy

sanity-check:
	maturin develop && python scripts/sanity_check.py

benchmark:
	maturin develop && python scripts/benchmark.py
