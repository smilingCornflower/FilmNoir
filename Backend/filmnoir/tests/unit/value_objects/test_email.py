from django.test import TestCase
from domain.exceptions.validation import ValidationException
from domain.value_objects.user import Email


class EmailTests(TestCase):
    def test_valid_email(self) -> None:
        email = Email("user@example.com")
        self.assertEqual(email.value, "user@example.com")

    def test_invalid_email_format(self) -> None:
        with self.assertRaises(ValidationException):
            Email("not-an-email")

        with self.assertRaises(ValidationException):
            Email("missing@domain")

        with self.assertRaises(ValidationException):
            Email("missing.at.symbol.com")

    def test_email_not_str(self) -> None:
        with self.assertRaises(TypeError):
            Email(123)  # type: ignore
