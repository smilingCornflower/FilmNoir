from dataclasses import dataclass

from domain.ports.data import AbstractCreateData, AbstractUpdateData
from domain.value_objects.user import Username, Email, RawPassword
from domain.value_objects.common import Id

@dataclass
class UserCreateData(AbstractCreateData):
    username: Username
    email: Email
    password: RawPassword


@dataclass
class UserUpdateData(AbstractUpdateData):
    id_: Id
    username: Username | None = None
    email: Email | None = None
    password: RawPassword | None = None
