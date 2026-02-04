from pydantic import BaseModel, ConfigDict


class CreateUserCommand(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    user_mobile_number: str
    user_email: str
    plain_password: str
