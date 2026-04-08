import logging

from src.app.container import Container
from src.app.core.settings import settings
from src.app.infrastructure.persistence.db.session import close_engine, init_engine
from src.app.user_management.application.commands.create_user_command import CreateUserCommand
from src.app.user_management.domain.exceptions import DuplicateUserInformation

logger = logging.getLogger(__name__)


async def create_admin():
    init_engine()
    container = Container()
    try:
        await container.user_application_service.create_user(
            container.get_uow(),
            CreateUserCommand(
                user_mobile_number="0000000000000",
                user_email=settings.ADMIN_EMAIL,
                plain_password=settings.ADMIN_PASSWORD,
            ),
        )
    except DuplicateUserInformation:
        logger.info("admin user already exists")
    await close_engine()
