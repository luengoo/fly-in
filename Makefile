VENV = env
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MAP = example_map.txt

all:
	clear
	python3 fly-in.py $(MAP)

install:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) fly-in.py $(MAP)

debug:
	python3 -m pdb fly-in.py $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	python3 -m flake8 . --exclude=env && \
	python3 -m mypy . --exclude=env --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs

.PHONY = all install run debug clean lint