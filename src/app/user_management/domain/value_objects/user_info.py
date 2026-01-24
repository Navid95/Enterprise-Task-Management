from pydantic import BaseModel, Field, EmailStr, ConfigDict
from uuid import UUID, uuid4


class UserId(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    id: UUID = Field(default_factory=uuid4)


class UserEmail(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    email: EmailStr = Field(default=None)


class UserMobileNumber(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    mobile: str = Field(min_length=10, max_length=13)


class HashedPassword(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    hashed_password: str = Field()
