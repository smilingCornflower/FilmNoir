from django.http import QueryDict
from django.test import TestCase

from application.mappers.form_data_to_user_create import FormDataToUserCreate
from domain.value_objects.data import UserCreateData
from domain.value_objects.user import Email, RawPassword, Username


class TestFormDataToUserCreate(TestCase):
    def test_successful_case(self):
        username, email, password = "smile-kun", "smile@example.com", "Password1234"
        form_data = QueryDict(f"username={username}&email={email}&password={password}")
        result: UserCreateData = FormDataToUserCreate.map(form_data)
        expected = UserCreateData(
            username=Username(username),
            email=Email(email),
            password=RawPassword(password),
        )
        self.assertEqual(result, expected)


