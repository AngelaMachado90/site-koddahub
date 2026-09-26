from dataclasses import dataclass
from fastapi import Depends, HTTPException
from .config import Settings, get_settings


@dataclass(frozen=True)
class Identity:
    organization_id: int
    user_id: int


def get_current_identity(settings: Settings = Depends(get_settings)) -> Identity:
    if not settings.dev_identity_enabled or settings.environment not in {"development", "hml"}:
        raise HTTPException(status_code=503, detail="Authentication is not configured")
    return Identity(settings.dev_organization_id, settings.dev_user_id)
