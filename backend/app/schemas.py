from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator


Priority = Literal["p1", "p2", "p3", "p4"]


class ProductOut(BaseModel):
    id: int
    name: str
    slug: str


class TicketOut(BaseModel):
    id: int
    reference_code: str
    product_id: int
    product_name: str
    title: str
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime
    closed_at: datetime | None


class TicketCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    product_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=160)
    priority: Priority
    message: str = Field(min_length=1, max_length=10000)

    @field_validator("title", "message")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value


class MessageCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    body: str = Field(min_length=1, max_length=10000)

    @field_validator("body")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value


class MessageOut(BaseModel):
    id: int
    ticket_id: int
    author_user_id: int
    author_name: str
    body: str
    created_at: datetime


class EventOut(BaseModel):
    id: int
    ticket_id: int
    actor_user_id: int | None
    actor_name: str | None
    event_type: str
    metadata: dict[str, Any]
    created_at: datetime
