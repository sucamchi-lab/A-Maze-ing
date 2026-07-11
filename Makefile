VENV = venv
PYTHON = $(VENV)/bin/python3
MYPY = $(VENV)/bin/mypy
FLAKE8 = $(VENV)/bin/flake8
PIP = $(VENV)/bin/pip
CONFIG_FILE = config.txt

install:
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py $(CONFIG_FILE)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG_FILE)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf mazegen/__pycache__
	rm -rf dist build *.egg-info
	rm -f maze.txt

lint:
	$(FLAKE8) .
	$(MYPY) .

lint-strict:
	$(FLAKE8) .
	$(MYPY) --strict .

build:
	$(PYTHON) -m build

.PHONY: install run debug clean lint lint-strict build
