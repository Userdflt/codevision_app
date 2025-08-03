# Project Context for Code Vision App

## Project Overview

The Code Vision App is an AI-powered assistant for querying Australian building codes and regulations. It consists of specialist AI agents that can answer clause-specific questions about the National Construction Code (NCC).

## Architecture Context

### System Components
1. **n8n Ingestion Pipeline** (Existing) - Processes documents and creates embeddings
2. **Supabase pgvector** - Vector database storing clause embeddings
3. **FastAPI + LangGraph Backend** - AI agent orchestration and API
4. **Next.js Frontend** - Chat interface with Supabase Auth

### Agent Specializations
- **Orchestrator Agent** - Routes queries to appropriate specialists
- **Code B Agent** - General building requirements, classifications, fire safety
- **Code C Agent** - Energy efficiency, thermal performance, insulation
- **Code D Agent** - Mechanical systems, HVAC, ventilation
- **Code E Agent** - Lighting requirements, natural and artificial lighting
- **Code F Agent** - Plumbing, water supply, drainage systems
- **Code G Agent** - Electrical systems, wiring, safety
- **Code H Agent** - Accessibility, disability access, universal design

## Domain Knowledge

### Building Code Structure
- The NCC is organized into sections (A-H) covering different aspects
- Each section has specific clauses with detailed requirements
- Cross-references between sections are common
- Some requirements vary by building classification (Class 1-10)
- Climate zones affect certain requirements (especially thermal)

### User Types
- **Building Professionals** - Architects, engineers, builders
- **Compliance Officers** - Council workers, building surveyors
- **Students** - Architecture/engineering students
- **DIY Builders** - Home owners planning modifications

### Query Patterns
- Specific clause lookups: "What does clause J1.5 require?"
- Requirement questions: "What's the minimum R-value for Zone 3?"
- Compliance checks: "Does this design meet accessibility requirements?"
- Comparative questions: "What's the difference between Class 1a and 1b?"

## Business Rules

### Response Quality
- Always cite specific clause references when possible
- Explain requirements in practical terms
- Note when professional consultation is recommended
- Highlight safety-critical requirements
- Clarify when requirements vary by jurisdiction

### Query Routing
- Route based on intent classification, not just keywords
- Allow fallback to general agent when uncertain
- Support cross-clause queries that span multiple specialists
- Handle ambiguous queries gracefully

### User Experience
- Provide fast responses (target <3 seconds)
- Show source references for transparency
- Support follow-up questions in context
- Graceful error handling with helpful messages

## Technical Constraints

### Performance
- Target p95 response time ≤ 3 seconds
- Support auto-scaling (0-3 Fly.io instances)
- Maintain >99.5% uptime
- Handle concurrent users efficiently

### Security
- All API endpoints require authentication
- Implement proper CORS policies
- Use HTTPS everywhere
- Validate all inputs
- Rate limit API endpoints

### Cost Management
- Optimize LLM token usage
- Use caching for repeated queries
- Efficient vector search queries
- Minimal data retention for chat sessions

## Integration Points

### External Services
- **Supabase** - Authentication, database, real-time features
- **OpenAI/Anthropic** - Language model providers
- **Fly.io** - Backend hosting and auto-scaling
- **Netlify** - Frontend hosting and CDN
- **n8n** - Document ingestion (external system)

### Data Flow
1. User query → Frontend → FastAPI API
2. Orchestrator → Intent classification
3. Specialist agent → Vector search → LLM generation
4. Response with sources → Frontend → User

## Compliance and Legal

### Data Handling
- User queries may contain project details (potentially sensitive)
- Chat sessions should be ephemeral by default
- No long-term storage of user conversations
- Comply with Australian privacy regulations

### Content Accuracy
- Responses based on official NCC documents
- Include disclaimers about professional advice
- Version control for code updates
- Clear attribution to source documents

## Development Workflow

### CI/CD Pipeline
- GitHub Actions for automated testing
- Dual deployment (backend to Fly.io, frontend to Netlify)
- Environment-specific configurations
- Rollback capabilities

### Monitoring
- Structured logging throughout the system
- Prometheus metrics for performance monitoring
- Health checks for all components
- Error tracking and alerting

### Testing Strategy
- Unit tests for business logic
- Integration tests for API endpoints
- End-to-end tests for critical user flows
- Performance testing for response times