from django.test import TestCase
from django.http import QueryDict
from application.converters.request_converters.auth import request_data_to_refresh_token
from domain.value_objects.token import RefreshTokenVo
from domain.exceptions.validation import ValidationException


class TestRequestDataToRefreshToken(TestCase):
    def test_valid_token(self) -> None:
        query_params = QueryDict("refresh_token=valid.refresh.token")
        result = request_data_to_refresh_token(query_params)

        self.assertIsInstance(result, RefreshTokenVo)
        self.assertEqual(result.value, "valid.refresh.token")

    def test_missing_token(self) -> None:
        query_params = QueryDict()
        with self.assertRaises(ValidationException) as context:
            request_data_to_refresh_token(query_params)

        self.assertEqual(
            str(context.exception), "Missing required field: refresh_token."
        )

    def test_empy_token(self) -> None:
        query_params = QueryDict("refresh_token=")

        with self.assertRaises(ValidationException):
            request_data_to_refresh_token(query_params)