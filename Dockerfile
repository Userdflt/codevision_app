# Multi-stage build for FastAPI backend and Next.js frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ ./
RUN npm run build && npm run export

# Python backend stage
FROM python:3.12-slim AS backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.7.0

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy source code
COPY src/ ./src/

# Copy frontend build from previous stage
COPY --from=frontend-builder /app/frontend/out ./static/

# Create non-root user
RUN useradd --create-home --shell /bin/bash agent
RUN chown -R agent:agent /app
USER agent

EXPOSE 8000

CMD ["uvicorn", "agent_project.application.main:app", "--host", "0.0.0.0", "--port", "8000"]