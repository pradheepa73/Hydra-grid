.PHONY: help run test clean demo

help:
	@echo "HYDRA-GRID shortcuts"
	@echo "  make run     - Run full pipeline"
	@echo "  make test    - Run tests"
	@echo "  make clean   - Remove cache"
	@echo "  make demo    - Run attack simulator"

run:
	python scripts/run_full_pipeline.py

test:
	python -m pytest tests/ -v

clean:
	Remove-Item -Recurse -Force -ErrorAction SilentlyContinue __pycache__, .pytest_cache

demo:
	python scripts/attack_simulator.py
