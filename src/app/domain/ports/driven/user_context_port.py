from abc import ABC, abstractmethod
from src.app.domain.user_management.entities.users import User


class UserContextPort(ABC):

    @abstractmethod
    def current_user(self) -> User | None:
        """
        Retrieves the current user. Each adapter should implement this method based on the logics of the connection type
        it is using.
        :return: A User object
        """
        pass
