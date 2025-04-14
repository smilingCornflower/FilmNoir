import re
from dataclasses import dataclass

from domain.constants import (PASSWORD_MAX_LENGTH, PASSWORD_MIN_LENGTH,
                              PASSWORD_PATTERN, USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH,
                              USERNAME_PATTERN)

from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


@dataclass(frozen=True)
class Username:
    value: str

    def __post_init__(self) -> None:
        if not (USERNAME_MIN_LENGTH <= len(self.value) <= USERNAME_MAX_LENGTH):
            raise ValueError(
                f"Username must be {USERNAME_MIN_LENGTH}-{USERNAME_MAX_LENGTH} chars."
            )
        if not re.match(USERNAME_PATTERN, self.value):
            raise ValueError("Username contains invalid characters.")


@dataclass(frozen=True)
class RawPassword:
    value: str

    def __post_init__(self) -> None:
        if not (PASSWORD_MIN_LENGTH <= len(self.value) <= PASSWORD_MAX_LENGTH):
            raise ValueError(
                f"Password must be {PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH} chars."
            )
        if not re.match(PASSWORD_PATTERN, self.value):
            raise ValueError(
                "Password must contain at least one digit, one uppercase letter and one lowercase letter."
            )


@dataclass(frozen=True)
class Email:
    value: str
    _validator = EmailValidator()

    def __post_init__(self) -> None:
        try:
            self._validator(self.value)
        except ValidationError as _:
            raise ValueError("Invalid email format.")
