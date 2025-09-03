"""
Configuration settings for the AI-Enhanced Autonomous Content Pipeline.
Handles environment variables, API keys, and application settings.
"""

import os
from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="AI-Enhanced Autonomous Content Pipeline", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    
    # Database (Supabase)
    supabase_url: str = Field(default="https://test-project.supabase.co", env="SUPABASE_URL")
    supabase_key: str = Field(default="test-anon-key", env="SUPABASE_KEY")
    supabase_service_role_key: Optional[str] = Field(default="test-service-role-key", env="SUPABASE_SERVICE_ROLE_KEY")
    
    # AI Services
    openrouter_api_key: str = Field(default="test-openrouter-key", env="OPENROUTER_API_KEY")
    langsmith_api_key: str = Field(default="test-langsmith-key", env="LANGSMITH_API_KEY")
    langsmith_project: str = Field(default="phoenix-content-pipeline", env="LANGSMITH_PROJECT")
    
    # Default AI Models
    default_content_model: str = Field(default="openai/gpt-4", env="DEFAULT_CONTENT_MODEL")
    default_research_model: str = Field(default="openai/gpt-3.5-turbo", env="DEFAULT_RESEARCH_MODEL")
    
    # API Configuration
    api_timeout: int = Field(default=30, env="API_TIMEOUT")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    
    # Content Generation
    max_content_length: int = Field(default=2000, env="MAX_CONTENT_LENGTH")
    default_temperature: float = Field(default=0.7, env="DEFAULT_TEMPERATURE")
    
    # Security
    secret_key: str = Field(default="test-secret-key-for-development", env="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    allowed_origins: list = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="ALLOWED_ORIGINS"
    )
    
    @validator('allowed_origins', pre=True)
    def parse_allowed_origins(cls, v):
        """Parse comma-separated origins string."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    @validator('supabase_url')
    def validate_supabase_url(cls, v):
        """Validate Supabase URL format."""
        if not v.startswith('https://'):
            raise ValueError('Supabase URL must start with https://')
        return v
    
    @validator('default_temperature')
    def validate_temperature(cls, v):
        """Validate temperature is within valid range."""
        if not 0.0 <= v <= 2.0:
            raise ValueError('Temperature must be between 0.0 and 2.0')
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings
