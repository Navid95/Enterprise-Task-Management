from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from src.app.user_management.infrastructure.persistence.base import BaseModel
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import (
    UserId,
    UserEmail,
    UserMobileNumber,
    HashedPassword,
)


class UserModel(BaseModel):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("mobile_num", name="uq_mobile_num"),
        UniqueConstraint("email_address", name="uq_email_address"),
    )
    mobile_num: Mapped[str]
    email_address: Mapped[str]
    hashed_password: Mapped[str]

    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return UserModel(
            id=user.id.id,
            mobile_num=user.mobile_num.mobile,
            email_address=user.email_address.email,
            hashed_password=user.hashed_password.hashed_password,
        )

    def to_entity(self) -> User:
        return User(
            id=UserId(id=self.id),
            mobile_num=UserMobileNumber(mobile=self.mobile_num),
            email_address=UserEmail(email=self.email_address),
            hashed_password=HashedPassword(hashed_password=self.hashed_password),
        )
