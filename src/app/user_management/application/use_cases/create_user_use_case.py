from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import (
    UserId,
    UserEmail,
    UserMobileNumber,
    HashedPassword,
)
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
        existing_mobile = self._user_repo.get_by_mobile(user_mobile_number)
        if existing_mobile:
            raise Exception()
        existing_email = self._user_repo.get_by_email(user_email)
        if existing_email:
            raise Exception()
        user = User(
            id=UserId(),
            mobile_num=user_mobile_number,
            email_address=user_email,
            hashed_password=hashed_password,
        )

        self._user_repo.save(user)

        return user
