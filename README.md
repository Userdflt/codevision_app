# Code Vision App - Work in Progress

A Python-powered AI agent system for querying building codes and regulations with clause-specific expertise.

## Architecture

This application consists of:

- **FastAPI + LangGraph Backend**: Orchestration agent with specialist clause agents (B-H)
- **Next.js Frontend**: Static chat UI with Supabase Auth
- **Supabase pgvector**: Vector database for clause embeddings
- **Fly.io Deployment**: Auto-scaling Python API service
- **Netlify Deployment**: Global CDN for frontend

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+
- Poetry
- Docker (optional)

### Installation

```bash
# Install Python dependencies
make install

# Install frontend dependencies
cd frontend && npm install
```

### Development

```bash
# Run backend in development mode
make dev

# Run frontend in development mode (separate terminal)
make frontend-dev
```

### Testing

```bash
# Run all tests with coverage
make test

# Run linting
make lint

# Format code
make format
```

### Production Build

```bash
# Build Docker image
make docker-build

# Run production container
make docker-run
```

## Project Structure

```
├── .github/workflows/     # CI/CD pipeline
├── src/agent_project/     # Python backend
│   ├── application/       # FastAPI routers & DI
│   ├── core/
│   │   ├── agents/        # LangGraph agents (orchestrator + specialists)
│   │   ├── prompts/       # Jinja prompt templates
│   │   ├── tools/         # Shared retrieval & reasoning
│   │   └── utils/         # Utilities (logging, timing)
│   ├── infrastructure/
│   │   ├── vector_db/     # Supabase pgvector client
│   │   ├── llm/           # LLM provider wrappers
│   │   └── auth/          # Supabase JWT validation
│   └── config.py          # Pydantic settings
├── frontend/              # Next.js static export
├── tools/                 # CLI utilities
├── tests/                 # Pytest test suites
└── claude-rules/          # Claude AI assistant rules
```

## Environment Variables

Create a `.env` file with:

```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# LLM Providers
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Application
APP_ENV=development
LOG_LEVEL=INFO
API_VERSION=v1
```

## Deployment

The application auto-deploys on push to `main`:

1. **Backend**: Builds Docker image → pushes to GHCR → deploys to Fly.io
2. **Frontend**: Builds static export → deploys to Netlify
3. **Infrastructure**: Terraform Cloud manages secrets and scaling

## API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics

## Contributing

1. Create a feature branch
2. Make your changes
3. Run tests and linting: `make test lint`
4. Submit a pull request
