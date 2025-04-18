from django.http import QueryDict
from loguru import logger

from application.converters.request_converters.auth import (
    request_data_to_login_credentials,
    request_data_to_user_create,
)
from domain.value_objects.token import AccessPayload
from application.converters.response_converters.auth import token_pair_to_dto, access_token_to_dto, access_payload_to_dto
from application.dto.auth import TokenPairDto, AccessTokenDto, AccessPayloadDto
from domain.models.user import User
from domain.services.auth import AuthService, RegistrationService
from domain.services.token import TokenService
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.data import UserCreateData
from domain.value_objects.token import TokenPairVo, AccessTokenVo, RefreshTokenVo
from application.converters.request_converters.auth import request_data_to_refresh_token, request_data_to_access_token


class AuthAppService:
    def __init__(
        self,
        auth_service: AuthService,
        token_service: TokenService,
    ):
        self._auth_service = auth_service
        self._token_service = token_service

    def login(self, credentials_raw: QueryDict) -> TokenPairDto:
        """
        :raises InvalidCredentialsException:
        :raises ValidationException:
        """
        credentials: LoginCredentials = request_data_to_login_credentials(credentials_raw)
        logger.info(f"Credentials parsed successfully")

        token_pair: TokenPairVo = self._auth_service.login(credentials)
        token_pair_dto: TokenPairDto = token_pair_to_dto(token_pair)
        return token_pair_dto

    def reissue_access(self, request_data: QueryDict) -> AccessTokenDto:
        """
        :raises ValidationException:
        :raises InvalidTokenException:
        """
        refresh_token: RefreshTokenVo = request_data_to_refresh_token(request_data)
        access_token: AccessTokenVo = self._auth_service.reissue_access(refresh_token)
        logger.debug("Access token issued successfully.")

        access_token_dto: AccessTokenDto = access_token_to_dto(access_token=access_token)
        return access_token_dto

    def verify_access(self, request_data: QueryDict) -> AccessPayloadDto:
        """
        :raises ValidationException:
        :raises InvalidTokenException:
        """
        access_token: AccessTokenVo = request_data_to_access_token(request_data)
        access_payload: AccessPayload = self._token_service.verify_access(access_token)
        logger.debug("Access token verified successfully.")

        access_payload_dto: AccessPayloadDto = access_payload_to_dto(access_payload)
        return access_payload_dto


class RegistrationAppService:
    def __init__(self, registration_service: RegistrationService):
        self._registration_service = registration_service

    def register(self, request_data: QueryDict) -> User:
        """
        :raises ValidationException:
        :raises UsernameAlreadyExistsException:
        :raises EmailAlreadyExistsException:
        """
        user_data: UserCreateData = request_data_to_user_create(data=request_data)
        user: User = self._registration_service.register(data=user_data)

        return user
