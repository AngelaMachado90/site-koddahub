from dataclasses import dataclass
from functools import lru_cache
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    environment: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_password_file: Path
    cors_origins: tuple[str, ...]
    dev_identity_enabled: bool
    dev_organization_id: int
    dev_user_id: int


@lru_cache
def get_settings() -> Settings:
    environment = os.getenv("SUPPORT_ENVIRONMENT", "development")
    dev_enabled = os.getenv("SUPPORT_DEV_IDENTITY_ENABLED", "false").lower() == "true"
    if environment == "production" and dev_enabled:
        raise RuntimeError("Development identity cannot be enabled in production")
    origins = tuple(
        value.strip()
        for value in os.getenv("SUPPORT_CORS_ORIGINS", "http://127.0.0.1:8000").split(",")
        if value.strip()
    )
    if not origins or "*" in origins:
        raise RuntimeError("CORS origins must be explicit")
    return Settings(
        environment=environment,
        db_host=os.getenv("SUPPORT_DB_HOST", "db"),
        db_port=int(os.getenv("SUPPORT_DB_PORT", "5432")),
        db_name=os.getenv("SUPPORT_DB_NAME", "koddahub_support"),
        db_user=os.getenv("SUPPORT_DB_USER", "koddahub_support_app"),
        db_password_file=Path(os.getenv("SUPPORT_DB_PASSWORD_FILE", "/run/secrets/postgres_app_password")),
        cors_origins=origins,
        dev_identity_enabled=dev_enabled,
        dev_organization_id=int(os.getenv("SUPPORT_DEV_ORGANIZATION_ID", "1")),
        dev_user_id=int(os.getenv("SUPPORT_DEV_USER_ID", "1")),
    )
