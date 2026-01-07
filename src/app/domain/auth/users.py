from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class Base(BaseModel):
    id: UUID | None = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)


class User(Base):
    mobile_num: str = Field(min_length=10, max_length=13)
    hashed_password: str = Field()
    roles: list['Role'] = Field()


class Role(Base):
    name: str
    description: str | None = Field(default="")

