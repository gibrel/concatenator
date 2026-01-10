PYTHON := python
VENV := .venv
BIN := $(VENV)/bin
PIP := $(BIN)/pip

.PHONY: venv init deps dev install format lint type test build run clean

venv:
	$(PYTHON) -m venv $(VENV)

init: venv
	$(PIP) install --upgrade pip setuptools wheel

deps: init
	$(PIP) install -e ".[dev]"

dev: deps

install: deps

format:
	$(BIN)/ruff format

lint:
	$(BIN)/ruff check --fix

type:
	$(BIN)/mypy src

test:
	$(BIN)/pytest

build:
	$(BIN)/python -m build

run:
	$(BIN)/pyminplate

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache dist build *.egg-info
