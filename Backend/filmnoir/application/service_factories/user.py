from application.services.user import UserRegistrationService
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository


class UserServiceFactory:
    @staticmethod
    def get_registration_service() -> UserRegistrationService:
        return UserRegistrationService(
            read_repository=DjUserReadRepository(),
            write_repository=DjUserWriteRepository(),
        )

