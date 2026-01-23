from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserEmail(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    email: EmailStr = Field(default=None)


class UserMobileNumber(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    mobile: str = Field(min_length=10, max_length=13)
