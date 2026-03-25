from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class TeamId(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    id: UUID = Field(default_factory=uuid4)
