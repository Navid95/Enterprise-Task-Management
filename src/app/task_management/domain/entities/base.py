from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Base(BaseModel):
    id: UUID | None = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
