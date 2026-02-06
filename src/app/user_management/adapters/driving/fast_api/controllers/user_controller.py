from typing import Annotated
from fastapi import APIRouter, Depends
from src.app.user_management.application.services.user_application_service import (
    UserApplicationService,
)
from src.app.user_management.adapters.driving.fast_api.schemas.user_schemas import (
    CreateUserSchema,
)
from src.app.user_management.application.dtos.user_dtos import UserDTO
from src.app.user_management.application.commands.create_user_command import (
    CreateUserCommand,
)
from src.app.user_management.adapters.driving.fast_api.dependencies.user_dependencies import get_user_application_service

user_v1 = APIRouter(prefix="/users")


@user_v1.post(path="/")
async def create_user(
    body: CreateUserSchema,
    service: Annotated[UserApplicationService, Depends(get_user_application_service)]
) -> UserDTO:
    return service.create_user(
        CreateUserCommand(
            user_mobile_number=body.user_mobile_number,
            user_email=body.user_email,
            plain_password=body.plain_password,
        )
    )
