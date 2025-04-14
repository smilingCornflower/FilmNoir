from django.http import QueryDict

from application.exceptions.mapping import MappingException
from application.ports.mapper import AbstractMapper
from domain.value_objects.data import UserCreateData
from domain.value_objects.user import Email, RawPassword, Username
from loguru import logger as log

class FormDataToUserCreate(AbstractMapper):
    @classmethod
    def _map(cls, form_data: QueryDict) -> UserCreateData:
        """:raises ValueError:"""
        username: str | None = form_data.get("username")
        email: str | None = form_data.get("email")
        password: str | None = form_data.get("password")
        if not (username and email and password):
            log.info("Missing required fields")
            raise ValueError("Missing required fields: username, email, or password.")

        return UserCreateData(
            email=Email(email),
            username=Username(username),
            password=RawPassword(password),
        )

    @classmethod
    def map(cls, form_data: QueryDict) -> UserCreateData:
        """:raises MappingException"""
        try:
            return cls._map(form_data)
        except ValueError as e:
            raise MappingException(str(e))
