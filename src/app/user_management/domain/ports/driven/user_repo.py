from abc import ABC, abstractmethod
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import UserId, UserEmail, UserMobileNumber


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: UserId) -> User | None:
        ...

    @abstractmethod
    def save(self, user: User):
        ...

    @abstractmethod
    def get_by_mobile(self, mobile: UserMobileNumber) -> User | None:
        ...

    @abstractmethod
    def get_by_email(self, email: UserEmail) -> User | None:
        ...
