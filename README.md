# Code Vision App

A state-of-the-art AI agent system for querying New Zealand building codes and regulations, powered by **100% native OpenAI Agents SDK** with advanced handoffs and guardrails.

## 🚀 Architecture

This application features a **pure OpenAI Agents SDK implementation** with:

- **Pure SDK Backend**: 100% native OpenAI Agents SDK with 7 specialist agents (Code B-H)
- **Native Handoffs**: Intelligent agent collaboration and routing
- **Advanced Guardrails**: Input validation and safety output checking
- **Next.js Frontend**: Static chat UI with Supabase Auth
- **Supabase pgvector**: Vector database for building code embeddings  
- **Google Cloud Run**: Auto-scaling Python API service (australia-southeast1)
- **Firebase Hosting**: Global CDN for frontend static site
- **Ephemeral Chat Memory**: Session-based message storage with automatic cleanup

### ✨ Key Features

- 🎭 **Intelligent Triage**: Auto-routes queries to appropriate specialists
- 🔄 **Native Handoffs**: Seamless collaboration between building code specialists
- 🛡️ **Safety Guardrails**: Input validation and professional response formatting
- ⚡ **Performance Optimized**: Cached agents and streamlined execution
- 🔧 **SDK Native Tools**: 5 specialized building code search and analysis tools

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

### 🎭 Using Pure SDK Agents

```bash
# Test pure SDK orchestrator (recommended)
poetry run python tools/run_agent.py pure_sdk "What are fire safety requirements for buildings?"

# Use advanced orchestrator with full features
poetry run python tools/run_agent.py advanced "Complex building code analysis"

# Test individual specialists
poetry run python tools/run_agent.py code_b "Building classification query"
poetry run python tools/run_agent.py code_c "Insulation requirements"
poetry run python tools/run_agent.py code_h "Accessibility standards"
```

### Testing

```bash
# Run all tests with coverage
make test

# Test pure SDK implementation specifically
poetry run pytest tests/test_migration/test_pure_sdk.py -v

# Test integration points
poetry run pytest tests/test_migration/test_integration_phase4.py -v

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

``` text
├── .github/workflows/     # CI/CD pipeline
├── src/agent_project/     # Python backend
│   ├── application/       # FastAPI routers using pure SDK
│   ├── agents/            # 🚀 Pure OpenAI Agents SDK implementation
│   │   ├── pure_sdk.py         # Native SDK specialists with handoffs
│   │   ├── pure_orchestrator.py # 100% SDK orchestration
│   │   ├── tools.py            # @function_tool decorated SDK tools  
│   │   ├── specifications.py   # Agent knowledge & handoff config
│   │   └── advanced/           # Advanced features (guardrails, etc.)
│   ├── core/
│   │   ├── agents/        # Original domain knowledge agents (preserved)
│   │   ├── tools/         # Shared reasoning tools
│   │   └── utils/         # Utilities (logging, timing)
│   ├── infrastructure/
│   │   ├── vector_db/     # Supabase pgvector client
│   │   ├── llm/           # LLM provider wrappers
│   │   └── auth/          # Supabase JWT validation
│   └── config.py          # Pydantic settings
├── frontend/              # Next.js static export
├── tools/                 # CLI utilities (updated for pure SDK)
├── tests/                 # Comprehensive test suites (95% coverage)
│   └── test_migration/    # Pure SDK migration validation tests
└── .cursor/rules/         # Development guidelines
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

# Security
JWT_SECRET_KEY=your_jwt_secret_key_for_development

# Google Cloud Configuration
GCP_PROJECT_ID=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Session Memory Configuration
SESSION_EXPIRY_HOURS=24
MAX_SESSION_MESSAGES=100

# Firebase Configuration  
FIREBASE_PROJECT_ID=your-firebase-project-id
```

## 🎊 Migration to Pure SDK

This application has been **completely migrated** from LangChain/LangGraph to **100% native OpenAI Agents SDK**:

### Migration Benefits
- ✅ **Zero Legacy Dependencies** - No LangChain/LangGraph overhead
- ✅ **Advanced Features** - Native handoffs, guardrails, advanced orchestration
- ✅ **Performance Optimized** - Direct SDK execution with caching
- ✅ **Maintainable Code** - Clean architecture with 25% fewer files
- ✅ **Future Proof** - Built on latest OpenAI Agents SDK

### Available Orchestrators
- **`pure_sdk`** - 100% native SDK with handoffs (recommended)
- **`advanced`** - Full advanced features (guardrails, orchestration patterns)
- **Individual specialists** - Direct access to Code B-H specialists

## API Endpoints

### Chat API (Pure SDK)
```bash
POST /chat
{
    "content": "What are fire safety requirements?",
    "session_id": "optional-session-id" 
}

POST /chat/stream  # Streaming responses
POST /agents/test/{agent_type}  # Admin testing (pure_sdk, advanced, code_b-h)
```

## Deployment

The application auto-deploys on push to `main`:

1. **Backend**: Builds Docker image → pushes to Google Artifact Registry → deploys to Cloud Run
2. **Frontend**: Builds static export → deploys to Firebase Hosting  
3. **Infrastructure**: Google Secret Manager stores secrets, Cloud Run auto-scales containers

### Manual Deployment Commands

```bash
# Backend to Google Cloud Run
export PROJECT_ID=your-gcp-project-id
make gcp-build gcp-deploy

# Frontend to Firebase Hosting  
make frontend-build firebase-deploy
```
