from django.http import QueryDict
from loguru import logger

from domain.exceptions.validation import ValidationException
from domain.value_objects.auth import LoginCredentials
from domain.value_objects.data import UserCreateData
from domain.value_objects.token import RefreshTokenVo, AccessTokenVo
from domain.value_objects.user import Email, RawPassword, Username


def request_data_to_login_credentials(data: QueryDict) -> LoginCredentials:
    """
    Convert request data to LoginCredentials.

    :raises ValidationException: If required fields missing or Email / RawPassword validation fails.
    """
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if not (email and password):
        logger.error("Missing required fields.")
        raise ValidationException("Missing required fields: email, or password.")

    return LoginCredentials(email=Email(email), password=RawPassword(password))


def request_data_to_user_create(data: QueryDict) -> UserCreateData:
    """
    Convert request data to UserCreateData.

    :raises ValidationException: If required fields missing or Email / Username / RawPassword validation fails.
    """
    username: str | None = data.get("username")
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    logger.debug(f"username = {username}")
    logger.debug(f"email = {email}")
    logger.debug(f"Is password provided = {bool(password)}")

    if not (username and email and password):
        logger.error("Missing required fields.")
        raise ValidationException("Missing required fields: username, email, or password.")

    return UserCreateData(
        email=Email(value=email),
        username=Username(value=username),
        password=RawPassword(value=password),
    )


def request_data_to_refresh_token(data: QueryDict) -> RefreshTokenVo:
    """:raises ValidationException: If missing 'refresh_token' field."""
    token: str | None = data.get("refresh_token")
    if not token:
        logger.error("Missing refresh_token field.")
        raise ValidationException("Missing required field: refresh_token.")
    return RefreshTokenVo(value=token)


def request_data_to_access_token(data: QueryDict) -> AccessTokenVo:
    """:raises ValidationException: If missing 'access_token' field."""
    token: str | None = data.get("access_token")
    if not token:
        logger.error("Missing access_token field.")
        raise ValidationException("Missing required field: access_token.")
    return AccessTokenVo(value=token)


