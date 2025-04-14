from domain.models.user import User
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.value_objects.data import UserCreateData
from domain.value_objects.filter import UserFilter
from domain.value_objects.user import Email, Username
from domain.exceptions.user import UsernameAlreadyExistsException, EmailAlreadyExistsException
from loguru import logger as log


class UserRegistrationService:
    def __init__(
            self,
            read_repository: UserReadRepository,
            write_repository: UserWriteRepository,
    ):
        self.read_repository = read_repository
        self.write_repository = write_repository

    def _check_username_already_exists(self, username: Username) -> None:
        """:raises UsernameAlreadyExistsException:"""
        result: list[User] = self.read_repository.get_all(UserFilter(username=username))
        if result:
            raise UsernameAlreadyExistsException(username.value)

    def _check_email_already_exists(self, email: Email) -> None:
        """:raises EmailAlreadyExistsException:"""
        result: list[User] = self.read_repository.get_all(UserFilter(email=email))
        if result:
            raise EmailAlreadyExistsException(email.value)

    def register(self, data: UserCreateData) -> User:
        self._check_username_already_exists(data.username)
        self._check_email_already_exists(data.email)
        return self.write_repository.create(data)

