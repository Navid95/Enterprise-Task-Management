from pydantic import BaseModel, ConfigDict


class LoginCommand(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    email: str
    password: str
