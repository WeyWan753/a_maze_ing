PYTHON = python3

install:
	$(PYTHON) -m pip install -e ".[dev]"

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

lint:
	$(PYTHON) -m flake8 mazegen a_maze_ing.py
	$(PYTHON) -m mypy mazegen a_maze_ing.py --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 mazegen a_maze_ing.py
	$(PYTHON) -m mypy mazegen a_maze_ing.py --strict

build:
	$(PYTHON) -m build

.PHONY: install run debug clean lint lint-strict build