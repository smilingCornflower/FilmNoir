from typing import cast

from application.services.auth import AuthAppService, RegistrationAppService
from config import settings
from domain.services.auth import AuthService, RegistrationService
from domain.services.token import TokenService
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository


class AuthServiceFactory:
    @staticmethod
    def get_auth_service() -> AuthAppService:
        auth_service = AuthService(
            token_service=TokenService(secret_key=cast(str, settings.SECRET_KEY)),
            user_read_repository=DjUserReadRepository(),
        )
        return AuthAppService(
            token_service=TokenService(secret_key=cast(str, settings.SECRET_KEY)),
            auth_service=auth_service,
        )


class RegistrationServiceFactory:
    @staticmethod
    def get_registration_service() -> RegistrationAppService:
        return RegistrationAppService(
            registration_service=RegistrationService(
                read_repository=DjUserReadRepository(),
                write_repository=DjUserWriteRepository(),
            )
        )
