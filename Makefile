.PHONY: help format lint type-check test clean

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

format:  ## Format code with black, isort and autoflake
	uv run autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive hordekit/ tests/
	uv run black hordekit/ tests/
	uv run isort hordekit/ tests/

lint:  ## Run flake8 linting
	uv run flake8 hordekit/ tests/

type-check:  ## Run mypy type checking
	uv run mypy hordekit/

test:  ## Run tests
	uv run pytest tests/ -v

check: format lint type-check test  ## Run all checks

clean:  ## Clean up cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete 