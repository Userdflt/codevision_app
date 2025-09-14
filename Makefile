.PHONY: help install lint test format clean run dev docker-build docker-run

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies using Poetry (fixed encoding issues!)
	@echo "🚀 Installing dependencies with Poetry..."
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && \
	export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8 && \
	poetry install
	@echo "✅ Installation complete! Poetry virtual environment ready!"

install-pip:  ## Install dependencies using pip (backup method)
	@echo "📦 Installing dependencies with pip (backup method)..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating new virtual environment..."; \
		python3.12 -m venv .venv; \
	fi
	@echo "Installing dependencies..."
	@.venv/bin/pip install --upgrade pip
	@.venv/bin/pip install fastapi "uvicorn[standard]" openai-agents openai supabase psycopg2-binary asyncpg pgvector pydantic pydantic-settings "python-jose[cryptography]" python-multipart jinja2 prometheus-client structlog
	@.venv/bin/pip install pytest pytest-asyncio pytest-cov black isort flake8 mypy httpx
	@echo "✅ Installation complete! Virtual environment ready at .venv/"

lint:  ## Run linting (flake8, mypy)
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry run flake8 src/ tests/
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry run mypy src/

format:  ## Format code with black and isort
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry run black src/ tests/
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry run isort src/ tests/

test:  ## Run tests with coverage
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry run pytest

clean:  ## Clean build artifacts and virtual environment
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

clean-full:  ## Clean everything including virtual environment
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ .venv
	poetry cache clear --all pypi 2>/dev/null || true

reset-env:  ## Reset virtual environment completely
	@echo "Resetting virtual environment..."
	rm -rf .venv
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry env remove --all 2>/dev/null || true
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry cache clear --all pypi 2>/dev/null || true
	$(MAKE) install

clear-poetry-cache:  ## Clear all Poetry caches
	@echo "Clearing Poetry caches..."
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry cache clear --all pypi 2>/dev/null || true
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry cache clear --all PyPI 2>/dev/null || true
	rm -rf ~/.cache/pypoetry 2>/dev/null || true
	rm -rf ~/Library/Caches/pypoetry 2>/dev/null || true
	@echo "✅ Poetry caches cleared!"

fix-poetry:  ## Reset Poetry configuration and reinstall
	@echo "🔧 Resetting Poetry configuration..."
	$(MAKE) clear-poetry-cache
	rm -rf .venv
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry env remove --all 2>/dev/null || true
	@echo "Configuring Poetry to use global virtual environments..."
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && \
	export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8 && \
	poetry config virtualenvs.in-project false && \
	poetry config virtualenvs.create true
	@echo "Installing dependencies with Poetry..."
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && \
	export LC_ALL=en_US.UTF-8 && export LANG=en_US.UTF-8 && poetry install --verbose
	@echo "✅ Poetry reset complete!"

run:  ## Run the FastAPI server
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry run uvicorn agent_project.application.main:app --reload --host 0.0.0.0 --port 8000

dev:  ## Run in development mode with hot reload
	@export PATH="/Users/youngwoosong/.local/bin:$PATH" && poetry run uvicorn agent_project.application.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

docker-build:  ## Build Docker image for Cloud Run
	docker build -t code-vision-api .

docker-run:  ## Run Docker container
	docker run -p 8000:8000 --env-file .env code-vision-api

gcp-build:  ## Build and push to Google Artifact Registry
	@echo "Building and pushing to GCP Artifact Registry..."
	@if [ -z "$(PROJECT_ID)" ]; then echo "PROJECT_ID environment variable is required"; exit 1; fi
	gcloud auth configure-docker australia-southeast1-docker.pkg.dev
	docker build -t australia-southeast1-docker.pkg.dev/$(PROJECT_ID)/code-vision/code-vision-api:latest .
	docker push australia-southeast1-docker.pkg.dev/$(PROJECT_ID)/code-vision/code-vision-api:latest

gcp-deploy:  ## Deploy to Cloud Run
	@echo "Deploying to Cloud Run..."
	@if [ -z "$(PROJECT_ID)" ]; then echo "PROJECT_ID environment variable is required"; exit 1; fi
	gcloud run deploy code-vision-api \
		--image australia-southeast1-docker.pkg.dev/$(PROJECT_ID)/code-vision/code-vision-api:latest \
		--region australia-southeast1 \
		--platform managed \
		--allow-unauthenticated \
		--port 8000 \
		--memory 1Gi \
		--cpu 1 \
		--min-instances 0 \
		--max-instances 10

frontend-dev:  ## Run frontend development server
	cd frontend && npm run dev

frontend-build:  ## Build frontend for Firebase Hosting
	cd frontend && npm run build

firebase-deploy:  ## Deploy frontend to Firebase Hosting
	cd frontend && npm run firebase:deploy

firebase-serve:  ## Serve frontend locally using Firebase
	cd frontend && npm run firebase:serve