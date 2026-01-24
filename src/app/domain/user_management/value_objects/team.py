from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4


class TeamId(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    id: UUID = Field(default_factory=uuid4)
