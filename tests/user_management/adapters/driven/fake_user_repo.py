from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import UserEmail, UserMobileNumber, UserId


class FakeUserRepoInMemory(UserRepository):
    def __init__(self):
        self._users: dict[UserId, User] = dict()

    def get_by_id(self, user_id: UserId) -> User | None:
        user = [u for i, u in self._users.items() if i == user_id]
        if len(user) < 1:
            return None
        return user[0]

    def save(self, user: User):
        self._users[user.id] = user

    def get_by_mobile(self, mobile: UserMobileNumber) -> User | None:
        user = [u for u in self._users.values() if u.mobile_num == mobile]
        if len(user) < 1:
            return None
        return user[0]

    def get_by_email(self, email: UserEmail) -> User | None:
        user = [u for u in self._users.values() if u.email_address == email]
        if len(user) < 1:
            return None
        return user[0]
