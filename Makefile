install:
	pip install -e ./
test:
	pytest -s
local_test:
	barseq -i tests/data/input/sequences -f -e test_barcodes -s tests/data/input/samples.csv -b tests/data/input/barcodes.csv -o tests/dump
local_test_ref_free:
	barseq -i tests/data/input/sequences -f -e test -s tests/data/input/samples.csv --reference-free -o tests/dump
clean_dump:
	rm -r tests/dump/results