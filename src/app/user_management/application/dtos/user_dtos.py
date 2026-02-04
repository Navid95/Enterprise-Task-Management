from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from src.app.user_management.domain.entities.users import User


class UserDTO(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    id: UUID | None = Field(default=None)
    mobile_num: str | None = Field(default=None)
    email_address: str | None = Field(default=None)

    @staticmethod
    def from_entity(user: User) -> 'UserDTO':
        return UserDTO(
            id=user.id.id,
            mobile_num=user.mobile_num.mobile,
            email_address=user.email_address.email,
        )
