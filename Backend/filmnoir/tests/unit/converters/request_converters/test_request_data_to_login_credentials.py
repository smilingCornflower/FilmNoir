from django.http import QueryDict
from django.test import TestCase
from domain.exceptions.validation import ValidationException
from domain.value_objects.auth import LoginCredentials
from application.converters.request_converters.auth import request_data_to_login_credentials


class TestRequestDataToLoginCredentials(TestCase):
    def test_valid_credentials(self) -> None:
        query_params = QueryDict("email=valid@example.com&password=ValidPass123")
        result = request_data_to_login_credentials(query_params)

        self.assertIsInstance(result, LoginCredentials)
        self.assertEqual(result.email.value, "valid@example.com")
        self.assertEqual(result.password.value, "ValidPass123")

    def test_missing_fields(self) -> None:
        test_cases = [
            ({"password": "ValidPass123"}, "email"),
            ({"email": "valid@example.com"}, "password"),
            ({}, "both"),
        ]

        for data, missing_field in test_cases:
            with self.subTest(missing_field=missing_field):
                query_params = QueryDict("", mutable=True)
                query_params.update(data)
                with self.assertRaises(ValidationException) as context:
                    request_data_to_login_credentials(query_params)
                self.assertEqual(
                    str(context.exception),
                    "Missing required fields: email, or password."
                )

    def test_invalid_email(self) -> None:
        query_params = QueryDict("email=invalid_email&password=ValidPass123")
        with self.assertRaises(ValidationException):
            request_data_to_login_credentials(query_params)

    def test_invalid_password(self) -> None:
        query_params = QueryDict("email=valid@example.com&password=invalid_password")
        with self.assertRaises(ValidationException):
            request_data_to_login_credentials(query_params)

    def test_empty_fields(self) -> None:
        query_params = QueryDict("email=&password=")
        with self.assertRaises(ValidationException):
            request_data_to_login_credentials(query_params)
