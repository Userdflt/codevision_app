"""
Application configuration using Pydantic settings.
"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Code Vision Agent API"
    app_version: str = "0.1.0"
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    api_version: str = Field(default="v1", alias="API_VERSION")

    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")
    workers: int = Field(default=1, alias="WORKERS")

    # Supabase Configuration (Primary Authentication)
    supabase_url: str = Field(alias="SUPABASE_URL")
    supabase_anon_key: str = Field(alias="SUPABASE_ANON_KEY")
    supabase_service_role_key: str = Field(alias="SUPABASE_SERVICE_ROLE_KEY")

    # Database
    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")
    vector_similarity_threshold: float = Field(
        default=0.8, alias="VECTOR_SIMILARITY_THRESHOLD"
    )
    max_vector_results: int = Field(default=10, alias="MAX_VECTOR_RESULTS")

    # LLM Providers
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(default=None, alias="ANTHROPIC_API_KEY")
    default_llm_provider: str = Field(default="openai", alias="DEFAULT_LLM_PROVIDER")
    default_model: str = Field(default="gpt-4-turbo-preview", alias="DEFAULT_MODEL")

    # Agent Configuration
    max_agent_iterations: int = Field(default=5, alias="MAX_AGENT_ITERATIONS")
    agent_timeout_seconds: int = Field(default=30, alias="AGENT_TIMEOUT_SECONDS")
    enable_parallel_agents: bool = Field(default=True, alias="ENABLE_PARALLEL_AGENTS")

    # Session Memory Configuration
    session_expiry_hours: int = Field(default=24, alias="SESSION_EXPIRY_HOURS")
    max_session_messages: int = Field(default=100, alias="MAX_SESSION_MESSAGES")

    # Google Cloud Configuration
    gcp_project_id: Optional[str] = Field(default=None, alias="GCP_PROJECT_ID")
    google_application_credentials: Optional[str] = Field(
        default=None, alias="GOOGLE_APPLICATION_CREDENTIALS"
    )

    # Authentication Configuration
    # Primary: Supabase JWT with ES256/RS256 (configured above)
    # Fallback: Simple JWT for development/testing only
    jwt_secret_key: Optional[str] = Field(default=None, alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, alias="JWT_EXPIRATION_HOURS")
    
    # JWT Cache Configuration
    jwks_cache_ttl_seconds: int = Field(default=3600, alias="JWKS_CACHE_TTL_SECONDS")  # 1 hour
    jwt_validation_timeout_seconds: int = Field(default=10, alias="JWT_VALIDATION_TIMEOUT_SECONDS")

    # Observability
    enable_metrics: bool = Field(default=True, alias="ENABLE_METRICS")
    enable_tracing: bool = Field(default=False, alias="ENABLE_TRACING")
    prometheus_port: int = Field(default=9090, alias="PROMETHEUS_PORT")

    # Pydantic v2 settings are configured via model_config above


# Global settings instance
settings = Settings()