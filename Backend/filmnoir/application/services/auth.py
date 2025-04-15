from datetime import datetime
from typing import Any

from application.exceptions.validation import ApplicationValidationException
from domain.services.auth import AuthService, TokenService
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.tokens import AccessTokenVo, RefreshTokenVo, TokenPairVo, AccessPayload
from domain.value_objects.user import Email, RawPassword
from infrastructure.utils.decode_jwt import decode_jwt


class AuthAppService:
    def __init__(self, token_service: TokenService, auth_service: AuthService):
        self._token_service = token_service
        self._auth_service = auth_service

    def login(self, email_str: str, password_str: str) -> TokenPairVo:
        try:
            email = Email(email_str)
            password = RawPassword(password_str)
        except ValueError as e:
            raise ApplicationValidationException(str(e))

        credentials = LoginCredentials(email=email, password=password)
        return self._auth_service.login(credentials)

    def reissue_access(self, refresh_token: str) -> AccessTokenVo:
        try:
            decoded: dict[str, Any] = decode_jwt(refresh_token)
            exp: datetime = decoded["exp"]
        except ValueError as e:
            raise ApplicationValidationException(str(e))

        refresh_token_vo = RefreshTokenVo(value=refresh_token, expires_at=exp)
        return self._auth_service.reissue_access(refresh_token_vo)

    def refresh_tokens(self, refresh_token: str) -> TokenPairVo:
        try:
            decoded: dict[str, Any] = decode_jwt(refresh_token)
            exp: datetime = decoded["exp"]
        except ValueError as e:
            raise ApplicationValidationException(str(e))

        refresh_token_vo = RefreshTokenVo(value=refresh_token, expires_at=exp)
        return self._auth_service.refresh_tokens(refresh_token_vo)

    def verify_access_token(self, access_token: str) -> AccessPayload:
        try:
            decoded: dict[str, Any] = decode_jwt(access_token)
            exp: datetime = decoded["exp"]
        except (ValueError, KeyError) as e:
            raise ApplicationValidationException(str(e))
        access_token_vo = AccessTokenVo(value=access_token, expires_at=exp)
        return self._token_service.verify_access(access_token_vo)
