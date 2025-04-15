from application.services.auth import AuthAppService
from domain.services.auth import TokenService, AuthService
from config import settings
from infrastructure.repositories.user import DjUserReadRepository
from typing import cast

class AuthServiceFactory:
    @staticmethod
    def get_auth_service() -> AuthAppService:
        token_service = TokenService(secret_key=cast(str, settings.SECRET_KEY))
        auth_service = AuthService(
            token_service=TokenService(secret_key=cast(str, settings.SECRET_KEY)),
            user_repository=DjUserReadRepository(),
        )
        return AuthAppService(token_service=token_service, auth_service=auth_service)