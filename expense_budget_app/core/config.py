"""
Application Configuration using Pydantic Settings
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator, field_validator


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """
    # Project Info
    PROJECT_NAME: str = "Expense & Budget Management API"
    PROJECT_DESCRIPTION: str = "Track expenses, manage salary, and view budget breakdowns"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database - Primary URL (if set, this takes precedence)
    DATABASE_URL: Optional[str] = None

    # Database - Individual components (used if DATABASE_URL is not set)
    DB_TYPE: str = "sqlite"  # postgresql or sqlite
    DB_DRIVER: str = "aiosqlite"  # asyncpg for PostgreSQL, aiosqlite for SQLite
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""
    DB_NAME: str = "expense_budget_db"

    # Database Options
    DATABASE_ECHO: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_PRE_PING: bool = True
    DB_POOL_RECYCLE: int = 3600

    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-characters-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Security
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100

    # Rate Limiting (future implementation)
    RATE_LIMIT_PER_MINUTE: int = 60

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    def get_database_url(self) -> str:
        """
        Get the database URL. If DATABASE_URL is set, use it.
        Otherwise, construct from individual components.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # Construct DATABASE_URL from components
        if self.DB_TYPE == "sqlite":
            return f"sqlite+{self.DB_DRIVER}:///./{self.DB_NAME}.db"
        elif self.DB_TYPE == "postgresql":
            return f"postgresql+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else:
            raise ValueError(f"Unsupported database type: {self.DB_TYPE}")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Override DATABASE_URL with constructed URL if not explicitly set
if not settings.DATABASE_URL:
    settings.DATABASE_URL = settings.get_database_url()
