from pydantic import BaseModel, ConfigDict


class TokenDTO(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    access_token: str
    token_type: str = "bearer"
