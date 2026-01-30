from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import (
    UserId,
    UserEmail,
    UserMobileNumber,
    HashedPassword,
)
from src.app.user_management.domain.exceptions import UserNotFound, DuplicateUserInformation
from src.app.user_management.domain.ports.driven.user_repo import UserRepository


class CreateUserUseCase:

    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    def execute(
        self,
        user_mobile_number: UserMobileNumber,
        user_email: UserEmail,
        hashed_password: HashedPassword,
    ) -> User:
        if self._user_repo.exists_by_mobile(user_mobile_number):
            raise DuplicateUserInformation(user_mobile=user_mobile_number)
        if self._user_repo.exists_by_email(user_email):
            raise DuplicateUserInformation(user_email=user_email)

        user = User(
            id=UserId(),
            mobile_num=user_mobile_number,
            email_address=user_email,
            hashed_password=hashed_password,
        )

        self._user_repo.save(user)
        return user
