PYTHON := python
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip

.PHONY: venv init deps-run deps-dev dev install format lint type test coverage build run pre-commit clean

venv:
	$(PYTHON) -m venv $(VENV)

init: venv
	$(PIP) install --upgrade pip setuptools wheel

deps-run: init
	$(PIP) install -e .

deps-dev: init
	$(PIP) install -e ".[dev]"

dev: deps-dev

format:
	$(BIN)/ruff format

lint:
	$(BIN)/ruff check --fix

type:
	$(BIN)/mypy src

test:
	$(BIN)/pytest -q

coverage:
	$(BIN)/pytest --cov=concatenator --cov-report=term-missing --cov-fail-under=80

build:
	$(BIN)/python -m build

install: build
	$(PIP) install dist/*.whl

run:
	$(BIN)/concatenator $(ARGS)

pre-commit: format lint type test

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache dist build *.egg-info
