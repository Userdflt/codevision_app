# Coding Rules for Code Vision App

## General Principles

1. **Follow the DDD (Domain-Driven Design) structure** as outlined in the PRD
2. **Maintain separation of concerns** between application, core, and infrastructure layers
3. **Use type hints consistently** in all Python code
4. **Write comprehensive tests** for all new features
5. **Follow the repository's existing patterns** and conventions

## Python Backend Rules

### Code Organization
- Use the established folder structure: `application/`, `core/`, `infrastructure/`
- Keep agents in their respective folders under `core/agents/`
- Separate concerns: routers, business logic, external services
- Use dependency injection where appropriate

### Naming Conventions
- Use snake_case for Python variables, functions, and modules
- Use PascalCase for classes
- Use UPPER_CASE for constants
- Use descriptive names that explain the purpose

### Error Handling
- Always use structured logging with `structlog`
- Catch specific exceptions, not generic `Exception`
- Provide meaningful error messages to users
- Log errors with appropriate context
- Use appropriate HTTP status codes in FastAPI responses

### LangGraph Agent Rules
- Inherit from `BaseAgent` for all specialist agents
- Use proper state management with Pydantic models
- Implement proper error handling in agent graphs
- Add comprehensive logging for debugging
- Keep agent logic focused on their specific domain

### Testing Requirements
- Write unit tests for all business logic
- Write integration tests for API endpoints
- Mock external dependencies (LLM providers, database)
- Use pytest fixtures for common test data
- Aim for >80% code coverage

## Frontend Rules

### TypeScript
- Use strict TypeScript configuration
- Define proper interfaces for all data structures
- Avoid `any` types - use proper typing
- Use meaningful component and prop names

### React Components
- Use functional components with hooks
- Keep components small and focused
- Use proper prop typing with interfaces
- Implement proper error boundaries
- Follow accessibility guidelines

### Styling
- Use Tailwind CSS classes consistently
- Follow the design system color palette
- Ensure responsive design for mobile
- Use semantic HTML elements

## Database Rules

### Vector Database
- Use proper indexing for vector operations
- Implement proper similarity thresholds
- Cache frequent queries when appropriate
- Monitor query performance

### Session Management
- Implement proper session cleanup
- Use appropriate data retention policies
- Secure sensitive session data
- Implement proper user isolation

## Security Rules

### Authentication
- Always validate JWT tokens
- Use proper CORS configuration
- Implement rate limiting
- Validate all user inputs
- Use HTTPS in production

### Data Handling
- Never log sensitive user data
- Implement proper data sanitization
- Use environment variables for secrets
- Follow least privilege principle

## Performance Rules

### Backend
- Use async/await for I/O operations
- Implement proper connection pooling
- Cache expensive operations
- Monitor response times

### Frontend
- Optimize bundle sizes
- Use proper image optimization
- Implement code splitting
- Minimize unnecessary re-renders

## Documentation Rules

- Document all public APIs
- Include type hints and docstrings
- Update README files when adding features
- Document configuration changes
- Maintain architecture decision records

## Git Rules

- Use conventional commit messages
- Create feature branches for new work
- Write descriptive pull request descriptions
- Include tests in all PRs
- Update documentation with code changes