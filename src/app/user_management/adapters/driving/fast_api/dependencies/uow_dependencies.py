from fastapi import Request
from src.app.user_management.domain.ports.driven.unit_of_work import UnitOfWork


def get_uow(request: Request) -> UnitOfWork:
    return request.app.container.get_uow()
