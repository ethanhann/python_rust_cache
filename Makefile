sanity_check:
	maturin develop && python sanity_check.py

benchmark:
	maturin develop && python benchmark.py
