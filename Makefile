.PHONY: help format lint type-check security test check clean

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

format:  ## Format code with ruff
	uv run ruff format hordekit/ tests/
	uv run ruff check --fix hordekit/ tests/

lint:  ## Lint with ruff (no autofix)
	uv run ruff check hordekit/ tests/

type-check:  ## Run mypy type checking
	uv run mypy hordekit/

security:  ## Run bandit security scan
	uv run bandit -r hordekit/ -c pyproject.toml

test:  ## Run tests
	uv run pytest tests/ -v

check: format lint type-check security test clean  ## Run all checks

clean:  ## Clean up cache files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
