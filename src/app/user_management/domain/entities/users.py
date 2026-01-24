from pydantic import BaseModel, Field
from src.app.user_management.domain.value_objects.user_info import (
    UserEmail,
    UserMobileNumber,
    UserId,
    HashedPassword,
)
from src.app.user_management.domain.value_objects.team import TeamId
from src.app.user_management.domain.exceptions import (
    NotTeamManagerError,
    MemberAlreadyInTeamError,
    MemberNotInTeamError,
)


class User(BaseModel):
    id: UserId
    mobile_num: UserMobileNumber
    email_address: UserEmail
    hashed_password: HashedPassword = Field()


class Team(BaseModel):
    id: TeamId
    name: str = Field(min_length=1, max_length=10)
    manager_id: UserId
    members: set[UserId]

    def __check_manager_id__(self, manager_id):
        if not manager_id == self.manager_id:
            raise NotTeamManagerError()

    def add_member(self, manager_id: UserId, new_member_id: UserId):
        self.__check_manager_id__(manager_id)
        if new_member_id in self.members:
            raise MemberAlreadyInTeamError()
        self.members.add(new_member_id)

    def remove_member(self, manager_id: UserId, member_id: UserId):
        self.__check_manager_id__(manager_id)
        if member_id not in self.members:
            raise MemberNotInTeamError()
        try:
            self.members.remove(member_id)
        except KeyError as e:
            raise MemberNotInTeamError()
