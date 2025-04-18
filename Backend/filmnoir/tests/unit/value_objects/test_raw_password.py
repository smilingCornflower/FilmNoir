from django.test import TestCase
from domain.value_objects.user import RawPassword
from domain.exceptions.validation import ValidationException
from domain.constants import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH


class RawPasswordTests(TestCase):
    def test_valid_password(self) -> None:
        password = RawPassword("Valid123")
        self.assertEqual(password.value, "Valid123")

    def test_password_too_short(self) -> None:
        with self.assertRaises(ValidationException):
            RawPassword("a" * (PASSWORD_MIN_LENGTH - 3) + "A1")

    def test_password_too_long(self) -> None:
        with self.assertRaises(ValidationException):
            RawPassword("A1" + "a" * PASSWORD_MAX_LENGTH)

    def test_password_invalid_pattern(self) -> None:
        with self.assertRaises(ValidationException):
            RawPassword("all_lowercase123")

        with self.assertRaises(ValidationException):
            RawPassword("ALL_UPPERCASE123")

        with self.assertRaises(ValidationException):
            RawPassword("NoDigitsHere")

    def test_password_not_str(self) -> None:
        with self.assertRaises(TypeError):
            RawPassword(12345678)  # type: ignore