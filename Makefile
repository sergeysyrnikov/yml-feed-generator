.PHONY: help test lint format type-check validate clean-pycache deps-sync deps-update run

.DEFAULT_GOAL := help

RUN_CMD := uv run

BLUE := \033[36m
NC := \033[0m

help: ## Show this help message
	@echo 'Usage:'
	@echo '  ${BLUE}make${NC} ${BLUE}<target>${NC}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${BLUE}%-15s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

clean-pycache: ## Remove __pycache__ and *.pyc
	find . -type d -name __pycache__ -not -path '*/.venv/*' -not -path '*/.git/*' -print0 | xargs -0 rm -rf 2>/dev/null || true
	find . -type f -name "*.pyc" -not -path '*/.venv/*' -not -path '*/.git/*' -delete 2>/dev/null || true

test: ## Run tests
	mkdir -p test-reports
	$(RUN_CMD) pytest tests/ --cov=feed_task --cov-report=xml --cov-report=html --cov-report=term --junit-xml=test-reports/junit.xml

format: clean-pycache ## Format code
	$(RUN_CMD) black .
	$(RUN_CMD) ruff check --fix .
	$(RUN_CMD) isort .

lint: ## Run linters
	$(RUN_CMD) flake8
	$(RUN_CMD) black --check .
	$(RUN_CMD) isort --check-only .

type-check: ## Type checking
	$(RUN_CMD) mypy feed_task.py

validate: format lint type-check ## Validate code (format + lint + type-check)

deps-sync: ## Install dependencies from lock file
	uv sync

deps-update: ## Update dependencies
	uv sync -U

run: ## Run Django dev server with YML feed
	$(RUN_CMD) python app.py
