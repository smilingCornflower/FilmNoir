import jwt

from application.ports.mapper import AbstractMapper
from domain.constants import JWT_ALGORITHM
from domain.value_objects.tokens import AccessTokenVo
from typing import Any
from datetime import datetime


def decode_jwt(token: str) -> dict[str, Any]:
    try:
        payload: dict[str, Any] = jwt.decode(
            token, algorithms=[JWT_ALGORITHM], options={"verify_signature": False}
        )
    except jwt.PyJWTError as e:
        raise ValueError(f"Invalid token format {e}")
    if "exp" not in payload:
        raise ValueError(f"Token has no expiration (exp) claim.")

    payload["exp"] = datetime.fromtimestamp(payload["exp"])
    return payload
