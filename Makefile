.PHONY: help install lint test format clean run dev docker-build docker-run

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	poetry install

lint:  ## Run linting (flake8, mypy)
	poetry run flake8 src/ tests/
	poetry run mypy src/

format:  ## Format code with black and isort
	poetry run black src/ tests/
	poetry run isort src/ tests/

test:  ## Run tests with coverage
	poetry run pytest

clean:  ## Clean build artifacts
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

run:  ## Run the FastAPI server
	poetry run uvicorn agent_project.application.main:app --reload --host 0.0.0.0 --port 8000

dev:  ## Run in development mode with hot reload
	poetry run uvicorn agent_project.application.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

docker-build:  ## Build Docker image
	docker build -t code-vision-app .

docker-run:  ## Run Docker container
	docker run -p 8000:8000 --env-file .env code-vision-app

frontend-dev:  ## Run frontend development server
	cd frontend && npm run dev

frontend-build:  ## Build frontend for production
	cd frontend && npm run build && npm run export