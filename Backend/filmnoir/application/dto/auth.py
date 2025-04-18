from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TokenPairDto:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class AccessTokenDto:
    access_token: str


@dataclass(frozen=True)
class RefreshTokenDto:
    refresh_token: str


@dataclass(frozen=True)
class AccessPayloadDto:
    sub: int
    email: str
    iat: int
    exp: int
    type: str

