from abc import ABC, abstractmethod

from domain.exceptions.user import UserNotFoundException
from domain.models.user import User
from domain.value_objects.user import Email, Username
from domain.ports.repository import AbstractReadRepository, AbstractWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.data import UserCreateData, UserUpdateData
from domain.value_objects.filter import UserFilter


class UserReadRepository(AbstractReadRepository[User, UserFilter], ABC):
    @abstractmethod
    def get_by_id(self, id_: Id) -> User:
        """:raises UserNotFoundException:"""
        pass

    @abstractmethod
    def get_all(self, filter_: UserFilter) -> list[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> User:
        """:raises UserNotFoundException:"""
        pass

    @abstractmethod
    def get_by_username(self, username: Username) -> User:
        """:raises UserNotFoundException:"""
        pass


class UserWriteRepository(AbstractWriteRepository[User, UserCreateData, UserUpdateData], ABC):
    @abstractmethod
    def create(self, data: UserCreateData) -> User:
        pass

    @abstractmethod
    def update(self, data: UserUpdateData) -> User:
        """:raises UserNotFoundException:"""
        pass

    @abstractmethod
    def delete(self, id_: Id) -> None:
        """:raises UserNotFoundException:"""
        pass
