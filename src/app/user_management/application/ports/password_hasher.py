from abc import ABC, abstractmethod

from src.app.user_management.domain.value_objects.user_info import HashedPassword


class IPasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, plain_password: str) -> HashedPassword: ...

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: HashedPassword) -> bool: ...
