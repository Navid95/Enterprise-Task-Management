from sqlalchemy.exc import IntegrityError

from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.exceptions import (
    UserNotFound,
)
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserId,
    UserMobileNumber,
)


class FakeUserRepoInMemory(UserRepository):
    def __init__(self):
        self._users: dict[UserId, User] = dict()

    async def exists_by_email(self, email: UserEmail) -> bool:
        return any([x for x in self._users.values() if x.email_address == email])

    async def exists_by_mobile(self, mobile: UserMobileNumber) -> bool:
        return any([x for x in self._users.values() if x.mobile_num == mobile])

    async def get_by_id(self, user_id: UserId) -> User:
        user = [u for i, u in self._users.items() if i == user_id]
        if len(user) < 1:
            raise UserNotFound(user_id=user_id)
        return user[0]

    async def save(self, user: User):
        if any([x for x in self._users.keys() if x.id == user.id]):
            raise IntegrityError(
                orig=BaseException(),
                statement="duplicate ID",
                hide_parameters=False,
                params={},
            )
        elif await self.exists_by_email(user.email_address):
            raise IntegrityError(
                orig=BaseException(),
                statement="duplicate email",
                hide_parameters=False,
                params={},
            )
        elif await self.exists_by_mobile(user.mobile_num):
            raise IntegrityError(
                orig=BaseException(),
                statement="duplicate mobile",
                hide_parameters=False,
                params={},
            )
        self._users[user.id] = user

    async def get_by_mobile(self, mobile: UserMobileNumber) -> User:
        user = [u for u in self._users.values() if u.mobile_num == mobile]
        if len(user) < 1:
            raise UserNotFound(user_mobile=mobile)
        return user[0]

    async def get_by_email(self, email: UserEmail) -> User:
        user = [u for u in self._users.values() if u.email_address == email]
        if len(user) < 1:
            raise UserNotFound(user_email=email)
        return user[0]
