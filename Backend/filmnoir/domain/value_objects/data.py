from dataclasses import dataclass

from domain.ports.data import AbstractCreateData, AbstractUpdateData
from domain.value_objects.common import Id
from domain.value_objects.user import Email, RawPassword, Username


@dataclass(frozen=True)
class UserCreateData(AbstractCreateData):
    username: Username
    email: Email
    password: RawPassword


@dataclass(frozen=True)
class UserUpdateData(AbstractUpdateData):
    id_: Id
    username: Username | None = None
    email: Email | None = None
    password: RawPassword | None = None
