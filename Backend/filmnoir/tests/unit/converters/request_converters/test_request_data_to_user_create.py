from django.http import QueryDict
from django.test import TestCase
from domain.exceptions.validation import ValidationException
from domain.value_objects.user import Username, RawPassword, Email
from application.converters.request_converters.auth import request_data_to_user_create
from domain.value_objects.data import UserCreateData


class TestRequestDataToUserCreateData(TestCase):
    def test_valid_data(self) -> None:
        query_params = QueryDict(
            "username=valid_user&email=valid@example.com&password=ValidPass123"
        )
        result = request_data_to_user_create(query_params)

        self.assertIsInstance(result, UserCreateData)
        self.assertEqual(result.username.value, "valid_user")
        self.assertEqual(result.email.value, "valid@example.com")
        self.assertEqual(result.password.value, "ValidPass123")

    def test_missing_fields(self) -> None:
        test_cases = [
            ({"email": "test@test.com", "password": "Pass123"}, "username"),
            ({"username": "user", "password": "Pass123"}, "email"),
            ({"username": "user", "email": "test@test.com"}, "password"),
        ]

        for data, missing_field in test_cases:
            with self.subTest(missing_field=missing_field):
                query_params = QueryDict("", mutable=True)
                query_params.update(data)

                with self.assertRaises(ValidationException) as context:
                    request_data_to_user_create(query_params)
                self.assertEqual(str(context.exception), "Missing required fields: username, email, or password.")

    def test_empty_strings(self) -> None:
        query_params = QueryDict("username=&email=&password=")
        with self.assertRaises(ValidationException):
            request_data_to_user_create(query_params)

    def test_invalid_email(self) -> None:
        query_params = QueryDict("username=valid&email=invalid&password=ValidPass123")
        with self.assertRaises(ValidationException):
            request_data_to_user_create(query_params)

    def test_invalid_username(self) -> None:
        query_params = QueryDict(
            "username=invalid!name&email=valid@example.com&password=ValidPass123"
        )
        with self.assertRaises(ValidationException):
            request_data_to_user_create(query_params)

    def test_invalid_password(self) -> None:
        query_params = QueryDict(
            "username=valid&email=valid@example.com&password=invalid"
        )
        with self.assertRaises(ValidationException):
            request_data_to_user_create(query_params)
