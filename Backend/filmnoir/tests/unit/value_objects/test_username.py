from django.test import TestCase
from domain.value_objects.user import Username
from domain.exceptions.validation import ValidationException


class UsernameTests(TestCase):
    def test_valid_username(self) -> None:
        username = Username("valid_user-123")
        self.assertEqual(username.value, "valid_user-123")

    def test_username_too_short(self) -> None:
        with self.assertRaises(ValidationException):
            Username("ab")

    def test_username_too_long(self) -> None:
        with self.assertRaises(ValidationException):
            Username("a" * 31)

    def test_username_invalid_characters(self) -> None:
        with self.assertRaises(ValidationException):
            Username("bad!name")

    def test_username_not_str(self) -> None:
        with self.assertRaises(TypeError):
            Username(123)  # type: ignore
