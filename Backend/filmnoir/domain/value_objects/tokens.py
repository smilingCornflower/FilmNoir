# domain/value_objects/tokens.py
from dataclasses import dataclass
from datetime import datetime
from domain.enums.token import TokenTypeEnum
from typing import Any


@dataclass(frozen=True)
class AccessTokenVo:
    value: str
    expires_at: datetime


@dataclass(frozen=True)
class RefreshTokenVo:
    value: str
    expires_at: datetime


@dataclass(frozen=True)
class TokenPairVo:
    access: AccessTokenVo
    refresh: RefreshTokenVo


@dataclass(frozen=True)
class AccessPayload:
    user_id: int
    email: str
    exp: int
    type: str = TokenTypeEnum.ACCESS.value


@dataclass(frozen=True)
class RefreshPayload:
    user_id: int
    exp: int
    type: str = TokenTypeEnum.REFRESH.value
