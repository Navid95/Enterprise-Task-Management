from typing import Annotated

from fastapi import APIRouter, Depends

from src.app.user_management.adapters.driving.fast_api.dependencies.auth_dependencies import (
    get_authentication_service,
)
from src.app.user_management.adapters.driving.fast_api.dependencies.uow_dependencies import get_uow
from src.app.user_management.adapters.driving.fast_api.schemas.auth_schemas import LoginSchema
from src.app.user_management.application.commands.login_command import LoginCommand
from src.app.user_management.application.services.authentication_service import (
    AuthenticationService,
)
from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork

auth_v1 = APIRouter(prefix="/auth")


@auth_v1.post(path="/login")
async def login(
    body: LoginSchema,
    service: Annotated[AuthenticationService, Depends(get_authentication_service)],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    command = LoginCommand(email=body.email, password=body.password)

    return await service.login(login_command=command, uow=uow)
