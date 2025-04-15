from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import Client, TestCase
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.response import Response
from loguru import logger
from domain.constants import USERNAME_MAX_LENGTH, USERNAME_MIN_LENGTH, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
from django.core.validators import EmailValidator
from domain.exceptions.user import UsernameAlreadyExistsException, EmailAlreadyExistsException

User = get_user_model()


class TestRegisterEndpoint(TestCase):
    def send_request(self):
        response: Response = self.client.post(
            path=self.register_url,
            data=urlencode(self.valid_data),
            content_type=self.content_type,
        )
        return response

    @classmethod
    def setUpTestData(cls):
        cls.register_url = "/api/auth/register/"
        cls.client = Client()
        cls.valid_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "ValidPass123",
        }
        cls.content_type = "application/x-www-form-urlencoded"

    def test_successful_register(self):
        response: Response = self.send_request()
        user: User | None = User.objects.filter(username="test_user").first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertTrue(check_password(self.valid_data["password"], user.password))

    def test_missed_username_field(self):
        self.valid_data.pop("username")
        response = self.send_request()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missed_email_field(self):
        self.valid_data.pop("email")
        response = self.send_request()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missed_password_field(self):
        self.valid_data.pop("password")
        response = self.send_request()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_content_types(self):
        wrong_content_types = [
            "application/json",
            "multipart/form-data",
            "text/plain",
        ]
        for content_type in wrong_content_types:
            self.content_type = content_type
            response = self.send_request()
            self.assertEqual(
                response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
            )

    def test_incorrect_username(self):
        wrong_usernames = [
            "a" * (USERNAME_MIN_LENGTH - 1),
            "a" * (USERNAME_MAX_LENGTH + 1),
            "!wrong_name",
            "?wrong_name",
            "неправильный_никнейм",
        ]
        for username in wrong_usernames:
            self.valid_data["username"] = username
            response = self.send_request()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_emails(self):
        wrong_emails = [
            "user@",
            "username.example.com",
            "user name@example.com",
            "user@example",
            "user()@example.com",
        ]
        for email in wrong_emails:
            self.valid_data["email"] = email
            response = self.send_request()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_incorrect_passwords(self):
        wrong_passwords = [
            "a" * (PASSWORD_MIN_LENGTH - 3) + "A1",
            "a" * PASSWORD_MAX_LENGTH + "A1",
            "only_lowercases_123",
            "ONLY_UPPERCASES_123",
            "WithoutDigits",
        ]
        for password in wrong_passwords:
            self.valid_data["password"] = password
            response = self.send_request()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_already_exists(self):
        User.objects.create_user(
            username=self.valid_data["username"],
            email=self.valid_data["email"],
            password=self.valid_data["password"],
        )
        self.valid_data["email"] = "another_email@example.com"
        response = self.send_request()

        self.assertEqual(response.status_code, 400)

    def test_email_already_exists(self):
        User.objects.create_user(
            username=self.valid_data["username"],
            email=self.valid_data["email"],
            password=self.valid_data["password"],
        )
        self.valid_data["username"] = "another_username"
        response = self.send_request()

        self.assertEqual(response.status_code, 400)