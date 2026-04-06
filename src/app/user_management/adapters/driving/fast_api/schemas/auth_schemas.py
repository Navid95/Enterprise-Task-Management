from pydantic import BaseModel, ConfigDict


class LoginSchema(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    email: str
    password: str
