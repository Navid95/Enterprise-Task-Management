from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.ports.driven.user_repo import UserRepository
from src.app.user_management.domain.value_objects.user_info import UserEmail, UserMobileNumber, UserId
from src.app.user_management.domain.exceptions import UserNotFound, DuplicateUserInformation


class FakeUserRepoInMemory(UserRepository):

    def __init__(self):
        self._users: dict[UserId, User] = dict()

    def exists_by_email(self, email: UserEmail) -> bool:
        return any([x for x in self._users.values() if x.email_address == email])

    def exists_by_mobile(self, mobile: UserMobileNumber) -> bool:
        return any([x for x in self._users.values() if x.mobile_num == mobile])

    def get_by_id(self, user_id: UserId) -> User:
        user = [u for i, u in self._users.items() if i == user_id]
        if len(user) < 1:
            raise UserNotFound(user_id=user_id)
        return user[0]

    def save(self, user: User):
        if any([x for x in self._users.keys() if x.id == user.id]):
            raise DuplicateUserInformation()
        elif self.exists_by_email(user.email_address):
            raise DuplicateUserInformation(user_email=user.email_address)
        elif self.exists_by_mobile(user.mobile_num):
            raise DuplicateUserInformation(user_mobile=user.mobile_num)
        self._users[user.id] = user

    def get_by_mobile(self, mobile: UserMobileNumber) -> User:
        user = [u for u in self._users.values() if u.mobile_num == mobile]
        if len(user) < 1:
            raise UserNotFound(user_mobile=mobile)
        return user[0]

    def get_by_email(self, email: UserEmail) -> User:
        user = [u for u in self._users.values() if u.email_address == email]
        if len(user) < 1:
            raise UserNotFound(user_email=email)
        return user[0]
