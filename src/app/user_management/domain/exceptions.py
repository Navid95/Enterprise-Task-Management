from src.app.core.exceptions import DomainError
from src.app.user_management.domain.value_objects.user_info import (
    UserId,
    UserEmail,
    UserMobileNumber,
)
from src.app.user_management.domain.value_objects.team import TeamId


class BaseUserManagementError(DomainError):
    """
    Base class for all exceptions in the User Management context
    """


class NotTeamManagerError(BaseUserManagementError):
    def __init__(self, manager_id: UserId, team_id: TeamId):
        super().__init__(context={"manager_id": manager_id, "team_id": team_id})


class MemberAlreadyInTeamError(BaseUserManagementError):
    def __init__(self, member_id: UserId, team_id: TeamId):
        super().__init__(context={"member_id": member_id, "team_id": team_id})


class MemberNotInTeamError(BaseUserManagementError):
    def __init__(self, member_id: UserId, team_id: TeamId):
        super().__init__(context={"member_id": member_id, "team_id": team_id})


class UserNotFound(BaseUserManagementError):
    def __init__(
        self,
        user_id: UserId | None = None,
        user_email: UserEmail | None = None,
        user_mobile: UserMobileNumber | None = None,
    ):
        super().__init__(
            context={
                "user_id": user_id,
                "user_email": user_email,
                "user_mobile": user_mobile,
            }
        )


class DuplicateUserInformation(BaseUserManagementError):
    def __init__(
        self,
        user_email: UserEmail | None = None,
        user_mobile: UserMobileNumber | None = None,
    ):
        super().__init__(
            context={
                "user_email": user_email,
                "user_mobile": user_mobile,
            }
        )
