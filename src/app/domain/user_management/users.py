from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from src.app.domain.user_management.value_objects.user_info import UserEmail, UserMobileNumber


class Base(BaseModel):
    id: UUID | None = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)


class User(Base):
    mobile_num: UserMobileNumber
    email_address: UserEmail = Field(default=None)
    hashed_password: str = Field()
    roles: list['Role'] = Field()


class Role(Base):
    name: str
    description: str | None = Field(default="")

