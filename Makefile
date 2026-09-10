.PHONY: build test eda release-check

build:
	python3 src/run_pipeline.py

test:
	python3 -m unittest discover -s tests -v

eda:
	python3 notebooks/eda.py

release-check: build test
