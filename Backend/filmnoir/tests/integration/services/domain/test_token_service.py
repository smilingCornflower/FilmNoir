from datetime import datetime, UTC

import jwt
from django.test import TestCase
from loguru import logger
from typing import cast
from domain.constants import JWT_ALGORITHM, ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME
from domain.models.user import User
from domain.services.token import TokenService
from domain.value_objects.token import AccessTokenVo, RefreshTokenVo, AccessPayload, RefreshPayload
from domain.enums.token import TokenTypeEnum
from domain.exceptions.auth import InvalidTokenException, TokenExpiredException


# noinspection DuplicatedCode
class TokenServiceTestCase(TestCase):
    secret_key: str
    token_service: TokenService
    token_service_with_invalid_key: TokenService
    user: User
    access_token_lifetime: int
    refresh_token_lifetime: int
    invalid_secret: str

    @classmethod
    def setUpTestData(cls) -> None:
        cls.secret_key = "secret_key"
        cls.invalid_secret = "invalid_key"
        cls.access_token_lifetime = ACCESS_TOKEN_LIFETIME
        cls.refresh_token_lifetime = REFRESH_TOKEN_LIFETIME

        cls.token_service = TokenService(
            secret_key=cls.secret_key,
            access_token_lifetime=cls.access_token_lifetime,
            refresh_token_lifetime=cls.refresh_token_lifetime,
        )
        cls.token_service_with_invalid_key = TokenService(
            secret_key=cls.invalid_secret,
            access_token_lifetime=cls.access_token_lifetime,
            refresh_token_lifetime=cls.refresh_token_lifetime,
        )

        cls.user = User.objects.create_user(
            email="test@example.com", username="test_user", password="password"
        )

    def test_generate_access_token(self) -> None:
        access_token: AccessTokenVo = self.token_service.generate_access(user=self.user)

        self.assertIsInstance(access_token, AccessTokenVo)
        self.assertTrue(access_token.value)

        decoded_payload: dict[str, int | str] = jwt.decode(access_token.value, self.secret_key, algorithms=[JWT_ALGORITHM])
        logger.debug(f"decoded access payload = {decoded_payload}")

        self.check_iat(cast(int, decoded_payload["iat"]))
        self.check_exp(cast(int, decoded_payload["exp"]), self.access_token_lifetime)

        self.assertEqual(decoded_payload["sub"], self.user.id)
        self.assertEqual(decoded_payload["email"], self.user.email)
        self.assertEqual(decoded_payload["type"], TokenTypeEnum.ACCESS)

    def test_generate_refresh_token(self) -> None:
        refresh_token: RefreshTokenVo = self.token_service.generate_refresh(user=self.user)

        self.assertIsInstance(refresh_token, RefreshTokenVo)
        self.assertTrue(refresh_token.value)

        decoded_payload = jwt.decode(refresh_token.value, self.secret_key, algorithms=[JWT_ALGORITHM])
        logger.debug(f"decoded refresh payload = {decoded_payload}")

        self.check_iat(cast(int, decoded_payload["iat"]))
        self.check_exp(cast(int, decoded_payload["exp"]), self.refresh_token_lifetime)

        self.assertEqual(decoded_payload["sub"], self.user.id)
        self.assertEqual(decoded_payload["type"], TokenTypeEnum.REFRESH)

    def test_verify_valid_access_token(self) -> None:
        access_token: AccessTokenVo = self.token_service.generate_access(self.user)
        access_payload: AccessPayload = self.token_service.verify_access(access_token)
        self.assertIsInstance(access_payload, AccessPayload)

        self.check_iat(access_payload.iat)
        self.check_exp(access_payload.exp, self.access_token_lifetime)

        self.assertEqual(access_payload.sub, self.user.id)
        self.assertEqual(access_payload.email, self.user.email)
        self.assertEqual(access_payload.type, TokenTypeEnum.ACCESS)

    def test_verify_valid_refresh_token(self) -> None:
        refresh_token: RefreshTokenVo = self.token_service.generate_refresh(self.user)
        refresh_payload: RefreshPayload = self.token_service.verify_refresh(refresh_token)
        self.assertIsInstance(refresh_payload, RefreshPayload)

        self.check_iat(refresh_payload.iat)
        self.check_exp(refresh_payload.exp, self.refresh_token_lifetime)

        self.assertEqual(refresh_payload.sub, self.user.id)
        self.assertEqual(refresh_payload.type, TokenTypeEnum.REFRESH)

    def test_access_token_with_wrong_secret(self) -> None:
        access_token: AccessTokenVo = self.token_service_with_invalid_key.generate_access(self.user)
        with self.assertRaises(InvalidTokenException) as context:
            self.token_service.verify_access(access_token)
        self.assertEqual(str(context.exception), "Invalid access token.")

    def test_refresh_token_with_wrong_secret(self) -> None:
        refresh_token: RefreshTokenVo = self.token_service_with_invalid_key.generate_refresh(self.user)
        with self.assertRaises(InvalidTokenException) as context:
            self.token_service.verify_refresh(refresh_token)
        self.assertEqual(str(context.exception), "Invalid refresh token.")

    def test_expired_access_token(self) -> None:
        iat = int((datetime.now(UTC)).timestamp()) - 100
        exp = iat + 1

        payload = {
            "sub": self.user.id,
            "email": self.user.email,
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.ACCESS,
            }
        expired_token: str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(TokenExpiredException) as context:
            self.token_service.verify_access(AccessTokenVo(value=expired_token))
        self.assertEqual(str(context.exception), "Access token has expired.")

    def test_expired_refresh_token(self) -> None:
        iat = int((datetime.now(UTC)).timestamp()) - 100
        exp = iat + 1

        payload = {
            "sub": self.user.id,
            "email": self.user.email,
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.REFRESH,
            }
        expired_token: str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(TokenExpiredException) as context:
            self.token_service.verify_refresh(RefreshTokenVo(value=expired_token))
        self.assertEqual(str(context.exception), "Refresh token has expired.")

    def test_access_token_with_missing_fields(self) -> None:
        iat = int(datetime.now(UTC).timestamp())
        exp = iat + self.access_token_lifetime

        base_payload = {
            "sub": self.user.id,
            "email": self.user.email,
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.ACCESS,
        }
        for missing_field in base_payload.keys():
            with self.subTest(missing_field=missing_field):

                invalid_payload = {k: v for k, v in base_payload.items() if k != missing_field}
                token_str = jwt.encode(invalid_payload, self.secret_key, algorithm=JWT_ALGORITHM)

                with self.assertRaises(InvalidTokenException) as context:
                    self.token_service.verify_access(AccessTokenVo(value=token_str))
                self.assertEqual(str(context.exception), "Invalid access token.")

    def test_refresh_token_with_missing_fields(self) -> None:
        iat = int(datetime.now(UTC).timestamp())
        exp = iat + self.refresh_token_lifetime

        base_payload = {
            "sub": self.user.id,
            "iat": iat,
            "exp": exp,
            "type": TokenTypeEnum.REFRESH,
        }
        for missing_field in base_payload.keys():
            with self.subTest(missing_field=missing_field):

                invalid_payload = {k: v for k, v in base_payload.items() if k != missing_field}
                token_str = jwt.encode(invalid_payload, self.secret_key, algorithm=JWT_ALGORITHM)

                with self.assertRaises(InvalidTokenException) as context:
                    self.token_service.verify_refresh(RefreshTokenVo(value=token_str))
                self.assertEqual(str(context.exception), "Invalid refresh token.")

    def test_token_with_str_exp(self) -> None:
        """
        Verifies that a token with expired 'exp' (even as string)
        raises TokenExpiredException.
        """
        iat = int(datetime.now(UTC).timestamp()) - 200
        exp = iat + 100

        payload = {
            "sub": self.user.id,
            "iat": str(iat),
            "exp": str(exp),
            "type": TokenTypeEnum.ACCESS,
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(TokenExpiredException):
            self.token_service.verify_refresh(RefreshTokenVo(value=token_str))

    def test_token_with_str_iat(self) -> None:
        """
        Verifies that a token with 'iat' set in the future (even as string)
        raises InvalidTokenException.
        """
        iat = int(datetime.now(UTC).timestamp()) + 100
        exp = iat + self.refresh_token_lifetime + 200

        payload = {
            "sub": self.user.id,
            "iat": str(iat),
            "exp": str(exp),
            "type": TokenTypeEnum.REFRESH,
        }
        token_str = jwt.encode(payload, self.secret_key, algorithm=JWT_ALGORITHM)
        with self.assertRaises(InvalidTokenException):
            self.token_service.verify_refresh(RefreshTokenVo(value=token_str))

    def check_iat(self, iat: int) -> None:
        now: float = datetime.now(UTC).timestamp()
        self.assertLess(abs(now - iat), 3)

    def check_exp(self, exp: int, lifetime: int) -> None:
        now: float = datetime.now(UTC).timestamp()
        self.assertLess(abs(now + lifetime - exp), 3)

