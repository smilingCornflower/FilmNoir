from typing import cast

from django.http import QueryDict
from rest_framework.parsers import FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from application.mappers.form_data_to_user_create import FormDataToUserCreate
from application.service_factories.user import UserServiceFactory
from application.services.user import UserRegistrationService
from domain.value_objects.data import UserCreateData
from application.exceptions.mapping import MappingException
from domain.exceptions.user import UsernameAlreadyExistsException, EmailAlreadyExistsException
from loguru import logger as log


class RegistrationView(APIView):
    parser_classes = [FormParser]

    @staticmethod
    def post(request: Request) -> Response:
        form_data: QueryDict = cast(QueryDict, request.data)
        user_service: UserRegistrationService = UserServiceFactory.get_registration_service()
        try:
            user_create_data: UserCreateData = FormDataToUserCreate.map(form_data)

            log.debug(f"username={user_create_data.username}")
            log.debug(f"email={user_create_data.email}")
            log.debug(f"password={'*' * len(user_create_data.password.value)}")

            user_service.register(user_create_data)

        except (MappingException, UsernameAlreadyExistsException, EmailAlreadyExistsException) as e:
            log.error(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": "success"}, 200)
