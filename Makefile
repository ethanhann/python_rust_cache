sanity_check:
	maturin develop && python scripts/sanity_check.py

benchmark:
	maturin develop && python scripts/benchmark.py
