from fastapi import Request
from src.app.user_management.application.services.user_application_service import (
    UserApplicationService,
)


def get_user_application_service(request: Request) -> UserApplicationService:
    return request.app.container.get_user_application_service()
