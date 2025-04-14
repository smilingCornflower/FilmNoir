from domain.models.user import User
from domain.repositories.user import UserReadRepository, UserWriteRepository
from domain.value_objects.common import Id
from domain.value_objects.data import UserCreateData, UserUpdateData
from domain.value_objects.filter import UserFilter
from domain.exceptions.user import UserNotFoundException
from domain.value_objects.user import Email, Username


class DjUserReadRepository(UserReadRepository):
    def get_by_id(self, id_: Id) -> User:
        """:raises UserNotFoundException:"""
        user: User | None = User.objects.filter(id=id_.value).first()
        if user is None:
            raise UserNotFoundException(f"An user with id = {id_.value} not found.")
        return user

    def get_all(self, filter_: UserFilter) -> list[User]:
        if filter_.id_:
            return list(User.objects.filter(id=filter_.id_.value))
        if filter_.email:
            return list(User.objects.filter(email=filter_.email.value))
        if filter_.username:
            return list(User.objects.filter(username=filter_.username.value))
        return list(User.objects.all())

    def get_by_email(self, email: Email) -> User:
        """:raises UserNotFoundException:"""
        user: User | None = User.objects.filter(email=email.value).first()
        if user is None:
            raise UserNotFoundException(F"An user with email = {email.value} not found.")
        return user

    def get_by_username(self, username: Username) -> User:
        """:raises UserNotFoundException:"""
        user: User | None = User.objects.filter(username=username.value).first()
        if user is None:
            raise UserNotFoundException(F"An user with username = {username.value} not found.")
        return user


class DjUserWriteRepository(UserWriteRepository):
    def create(self, data: UserCreateData) -> User:
        return User.objects.create_user(
            email=data.email.value,
            username=data.username.value,
            password=data.password.value,
        )

    def update(self, data: UserUpdateData) -> User:
        """:raises UserNotFoundException:"""
        try:
            user: User = User.objects.get(id=data.id_.value)
        except User.DoesNotExist:
            raise UserNotFoundException(f"An user with id = {data.id_.value} is not found.")

        if data.email:
            user.email = data.email.value
        if data.username:
            user.username = data.username.value
        if data.password:
            user.set_password(data.password.value)
        user.save()
        return user

    def delete(self, id_: Id) -> None:
        """:raises UserNotFoundException:"""
        try:
            User.objects.get(id=id_.value).delete()
        except User.DoesNotExist:
            raise UserNotFoundException(f"An user with id = {id_.value} is not found.")

