from src.app.user_management.application.services.user_application_service import UserApplicationService
from src.app.user_management.application.use_cases.create_user_use_case import CreateUserUseCase
from tests.user_management.adapters.driven.fake_user_repo import FakeUserRepoInMemory


class Container:
    def __init__(self):
        self.user_repo = FakeUserRepoInMemory()
        self.create_user_uc = CreateUserUseCase(self.user_repo)
        self.user_application_service = UserApplicationService(self.create_user_uc)

    def get_user_application_service(self, uow=None, use_case=None):
        return self.user_application_service

    def get_user_repo(self, session):
        ...
    def get_session(self):
        ...
    def get_use_case(self, user_repo):
        ...