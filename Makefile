install:
	pip install -e ./
test:
	pytest -s
local_test:
	barseq -i tests/data/input/sequences -f -e test -s tests/data/input/samples.csv --reference-free -o tests/dump