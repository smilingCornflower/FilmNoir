from django.test import TestCase
from django.http import QueryDict
from application.converters.request_converters.auth import request_data_to_access_token
from domain.value_objects.token import AccessTokenVo
from domain.exceptions.validation import ValidationException


class TestRequestDataToAccessToken(TestCase):
    def test_valid_token(self) -> None:
        query_params = QueryDict("access_token=valid.access.token")
        result = request_data_to_access_token(query_params)

        self.assertIsInstance(result, AccessTokenVo)
        self.assertEqual(result.value, "valid.access.token")

    def test_missing_token(self) -> None:
        query_params = QueryDict()
        with self.assertRaises(ValidationException) as context:
            request_data_to_access_token(query_params)

        self.assertEqual(
            str(context.exception), "Missing required field: access_token."
        )

    def test_empy_token(self) -> None:
        query_params = QueryDict("access_token=")

        with self.assertRaises(ValidationException):
            request_data_to_access_token(query_params)