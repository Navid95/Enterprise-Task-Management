from abc import ABC, abstractmethod
from src.app.user_management.domain.entities.users import User
from src.app.user_management.domain.value_objects.user_info import (
    UserId,
    UserEmail,
    UserMobileNumber,
)
from src.app.user_management.domain.exceptions import UserNotFound, DuplicateUserInformation


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, user_id: UserId) -> User:
        """
        Command Query
        Retrieve a user by its id.
        :raises UserNotFound: if a user is not found by the given id
        :param user_id: the id of the user
        :return: user instance
        """
        ...

    @abstractmethod
    def save(self, user: User):
        """
        Command Query
        Persist a user instance
        Note: The adapter must implement constraint checks for uniqueness
        :raises DuplicateUserInformation: if any user filed is duplicated
        :param user: a user instance
        :return: None
        """
        ...

    @abstractmethod
    def get_by_mobile(self, mobile: UserMobileNumber) -> User:
        """
        Command Query
        Retrieve a user by its mobile number
        :raises UserNotFound: if a user is not found by the given mobile number
        :param mobile: the mobile number of the user
        :return: user instance
        """
        ...

    @abstractmethod
    def get_by_email(self, email: UserEmail) -> User:
        """
        Command Query
        Retrieve a user by its email address
        :raises UserNotFound: if a user is not found by the given email address
        :param email: the email address of the user
        :return: user instance
        """
        ...

    @abstractmethod
    def exists_by_email(self, email: UserEmail) -> bool:
        """
        Check if a user with the given email address exists
        :param email: the email address of the user
        :return: True if a user with the given email address exists
        """

    @abstractmethod
    def exists_by_mobile(self, mobile: UserMobileNumber) -> bool:
        """
        Check if a user with the given mobil3 number exists
        :param mobile: the mobile number of the user
        :return: True if a user with the given mobile number exists
        """

