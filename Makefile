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