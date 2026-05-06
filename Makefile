.PHONY: install test lint format typecheck run-baseline run-multi clean

install:
	pip install -e "[dev,llm]"

test:
	.venv/bin/python -m pytest

lint:
	.venv/bin/ruff check src tests

format:
	.venv/bin/ruff format src tests

typecheck:
	.venv/bin/python -m mypy src

run-baseline:
	python -m multi_agent_research_lab.cli baseline --query "Research GraphRAG state-of-the-art"

run-multi:
	python -m multi_agent_research_lab.cli multi-agent --query "Research GraphRAG state-of-the-art"

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache dist build *.egg-info
