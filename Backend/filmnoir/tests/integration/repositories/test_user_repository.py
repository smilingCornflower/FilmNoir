from django.test import TestCase
from typing import cast
from domain.exceptions.user import UserNotFoundException
from domain.models.user import User
from domain.value_objects.common import Id
from domain.value_objects.data import UserCreateData, UserUpdateData
from domain.value_objects.user import Email, RawPassword, Username
from infrastructure.repositories.user import DjUserReadRepository, DjUserWriteRepository
from django.contrib.auth.hashers import check_password
from domain.value_objects.filter import UserFilter
from loguru import logger as log


class TestDjUserReadRepository(TestCase):
    read_repo: DjUserReadRepository
    user1: User
    user2: User

    @classmethod
    def setUpTestData(cls) -> None:
        cls.read_repo = DjUserReadRepository()

        cls.user1 = User.objects.create_user(
            email="user1@example.com", username="user1", password="password1"
        )
        cls.user2 = User.objects.create_user(
            email="user2@example.com", username="user2", password="password2"
        )

    def test_get_by_id_existing_user(self) -> None:
        result: User = self.read_repo.get_by_id(Id(self.user1.id))
        self.assertEqual(result, self.user1)

    def test_get_by_id_non_existing_user(self) -> None:
        with self.assertRaises(UserNotFoundException):
            self.read_repo.get_by_id(Id(-1))

    def test_get_all_without_filter(self) -> None:
        result: list[User] = self.read_repo.get_all(UserFilter())
        self.assertEqual(result, [self.user1, self.user2])

    def test_get_all_with_id_filter(self) -> None:
        result: list[User] = self.read_repo.get_all(UserFilter(id_=Id(self.user1.id)))
        self.assertEqual(result, [self.user1])

    def test_get_all_with_email_filter(self) -> None:
        result: list[User] = self.read_repo.get_all(
            UserFilter(email=Email(self.user1.email))
        )
        self.assertEqual(result, [self.user1])

    def test_get_all_with_username_filter(self) -> None:
        result: list[User] = self.read_repo.get_all(
            UserFilter(username=Username(self.user1.username))
        )
        self.assertEqual(result, [self.user1])

    def test_get_by_email_existing_user(self) -> None:
        result = self.read_repo.get_by_email(Email(self.user2.email))
        self.assertEqual(result, self.user2)

    def test_get_by_email_non_existing_user(self) -> None:
        with self.assertRaises(UserNotFoundException):
            self.read_repo.get_by_email(Email("non_existing@example.com"))

    def test_get_by_username_existing_user(self) -> None:
        result = self.read_repo.get_by_username(Username(self.user2.username))
        self.assertEqual(result, self.user2)

    def test_get_by_username_non_existing_user(self) -> None:
        with self.assertRaises(UserNotFoundException):
            self.read_repo.get_by_username(Username("non_existing"))


class TestDjUserWriteRepository(TestCase):
    read_repo: DjUserReadRepository
    write_repo: DjUserWriteRepository
    user1: User

    @classmethod
    def setUpTestData(cls) -> None:
        cls.read_repo = DjUserReadRepository()
        cls.write_repo = DjUserWriteRepository()

        cls.user1 = User.objects.create_user(
            email="user1@example.com", username="user1", password="password1"
        )

    def test_create_user(self) -> None:
        data = UserCreateData(
            email=Email("new_user@example.com"),
            username=Username("new_user"),
            password=RawPassword("Password1234"),
        )
        user: User = self.write_repo.create(data)
        all_users: list[User] = self.read_repo.get_all(UserFilter())
        self.assertEqual(len(all_users), 2)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, data.email.value)
        self.assertEqual(user.username, data.username.value)
        self.assertTrue(check_password(data.password.value, user.password))

    def test_update_user_all_fields(self) -> None:
        data = UserUpdateData(
            id_=Id(self.user1.id),
            email=Email("another_email@example.com"),
            username=Username("another_username"),
            password=RawPassword("AnotherPassword1234"),
        )
        result: User = self.write_repo.update(data)
        user: User = self.read_repo.get_by_id(data.id_)

        self.assertTrue(result.id == user.id == data.id_.value)
        self.assertTrue(result.email == user.email == cast(Email, data.email).value)
        self.assertTrue(result.username == user.username == cast(Username, data.username).value)
        self.assertEqual(result.password, user.password)
        self.assertTrue(check_password(cast(RawPassword, data.password).value, result.password))

    def test_update_email_field(self) -> None:
        data = UserUpdateData(
            id_=Id(self.user1.id), email=Email("another_email@example.com")
        )
        result: User = self.write_repo.update(data)
        user: User = self.read_repo.get_by_id(data.id_)

        self.assertEqual(result.id, user.id)
        self.assertEqual(result.email, user.email)

    def test_update_username_field(self) -> None:
        data = UserUpdateData(
            id_=Id(self.user1.id), username=Username("another_username")
        )
        result: User = self.write_repo.update(data)
        user: User = self.read_repo.get_by_id(data.id_)

        self.assertEqual(result.id, user.id)
        self.assertEqual(result.username, user.username)

    def test_update_password_field(self) -> None:
        data = UserUpdateData(
            id_=Id(self.user1.id), password=RawPassword("NewPassword1234")
        )
        result: User = self.write_repo.update(data)
        user: User = self.read_repo.get_by_id(data.id_)

        self.assertEqual(result.id, user.id)
        self.assertTrue(check_password(cast(RawPassword, data.password).value, user.password))

    def test_update_non_existing_user(self) -> None:
        data = UserUpdateData(id_=Id(-1), username=Username("non_existing"))
        with self.assertRaises(UserNotFoundException):
            self.write_repo.update(data)

    def test_delete_existing_user(self) -> None:
        user_id = Id(self.user1.id)
        self.write_repo.delete(user_id)

        with self.assertRaises(UserNotFoundException):
            self.read_repo.get_by_id(user_id)

    def test_delete_non_existing_user(self) -> None:
        with self.assertRaises(UserNotFoundException):
            self.write_repo.delete(Id(-1))
