from dataclasses import asdict
from datetime import datetime
from typing import Any
from domain.value_objects.common import Id
import jwt
from domain.exceptions.user import UserNotFoundException
from domain.constants import (
    ACCESS_TOKEN_LIFETIME,
    JWT_ALGORITHM,
    REFRESH_TOKEN_LIFETIME,
)
from domain.enums.token import TokenTypeEnum
from domain.exceptions.auth import (
    InvalidAccessTokenException,
    InvalidRefreshTokenException,
    InvalidCredentialsException,
)
from domain.models.user import User
from domain.repositories.user import UserReadRepository
from domain.value_objects.tokens import (
    AccessPayload,
    AccessTokenVo,
    RefreshPayload,
    RefreshTokenVo,
    TokenPairVo,
)
from domain.value_objects.auth import LoginCredentials
from loguru import logger


class TokenService:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.access_token_lifetime = ACCESS_TOKEN_LIFETIME
        self.refresh_token_lifetime = REFRESH_TOKEN_LIFETIME

    def generate_access_token(self, user: User) -> AccessTokenVo:
        expires_at: datetime = datetime.now() + self.access_token_lifetime
        payload = AccessPayload(
            user_id=user.id,
            email=user.email,
            exp=int(expires_at.timestamp()),
        )
        logger.debug(f"{payload=}")
        token: str = jwt.encode(
            asdict(payload), self.secret_key, algorithm=JWT_ALGORITHM
        )
        return AccessTokenVo(value=token, expires_at=expires_at)

    def generate_refresh_token(self, user: User) -> RefreshTokenVo:
        expires_at: datetime = datetime.now() + self.refresh_token_lifetime
        payload = RefreshPayload(
            user_id=user.id,
            exp=int(expires_at.timestamp()),
        )
        logger.debug(f"{payload=}")

        token: str = jwt.encode(
            asdict(payload), self.secret_key, algorithm=JWT_ALGORITHM
        )
        return RefreshTokenVo(value=token, expires_at=expires_at)

    def create_token_pair(self, user: User) -> TokenPairVo:
        return TokenPairVo(
            access=self.generate_access_token(user=user),
            refresh=self.generate_refresh_token(user=user),
        )

    def verify_access(self, token: AccessTokenVo) -> AccessPayload:
        """:raises InvalidAccessTokenException:"""
        try:
            payload: dict[str, Any] = jwt.decode(
                token.value, self.secret_key, algorithms=[JWT_ALGORITHM]
            )
        except jwt.PyJWTError as e:
            raise InvalidAccessTokenException(f"Invalid access token: {str(e)}")

        if payload.get("type") != TokenTypeEnum.ACCESS:
            raise InvalidAccessTokenException("Not an access token.")

        return AccessPayload(
            user_id=payload["user_id"],
            email=payload["email"],
            exp=payload["exp"],
        )

    def verify_refresh(self, token: RefreshTokenVo) -> RefreshPayload:
        """:raises InvalidRefreshTokenException:"""
        try:
            payload: dict[str, Any] = jwt.decode(
                token.value, self.secret_key, algorithms=[JWT_ALGORITHM]
            )
        except jwt.PyJWTError as e:
            raise InvalidRefreshTokenException(f"Invalid refresh token: {str(e)}")

        if payload.get("type") != TokenTypeEnum.REFRESH:
            raise InvalidRefreshTokenException("Not a refresh token.")

        return RefreshPayload(
            user_id=payload["user_id"],
            exp=payload["exp"],
        )


class AuthService:
    def __init__(
        self, token_service: TokenService, user_repository: UserReadRepository
    ):
        self._token_service = token_service
        self._user_repository = user_repository

    def login(self, credentials: LoginCredentials) -> TokenPairVo:
        user = self._authenticate_user(credentials)
        return self._token_service.create_token_pair(user=user)

    def reissue_access(self, refresh_token: RefreshTokenVo) -> AccessTokenVo:
        payload: RefreshPayload = self._token_service.verify_refresh(refresh_token)
        user: User = self._user_repository.get_by_id(Id(payload.user_id))
        return self._token_service.generate_access_token(user=user)

    def refresh_tokens(self, refresh_token: RefreshTokenVo) -> TokenPairVo:
        payload: RefreshPayload = self._token_service.verify_refresh(refresh_token)
        user: User = self._user_repository.get_by_id(Id(payload.user_id))
        return self._token_service.create_token_pair(user=user)

    def _authenticate_user(self, credentials: LoginCredentials) -> User:
        """:raises InvalidCredentialsException:"""
        try:
            user: User = self._user_repository.get_by_email(credentials.email)
        except UserNotFoundException:
            raise InvalidCredentialsException("Invalid user or password.")

        if not user.check_password(credentials.password.value):
            raise InvalidCredentialsException("Invalid user or password.")
        return user
