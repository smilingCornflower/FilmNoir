from dataclasses import asdict
from datetime import datetime
from typing import cast

from django.http import QueryDict
from loguru import logger, logger as log
from rest_framework import status
from rest_framework.parsers import FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from domain.exceptions.auth import InvalidTokenException
from application.converters.request_converters.auth import request_data_to_user_create
from application.dto.auth import AccessTokenDto
from application.dto.auth import TokenPairDto
from application.exceptions.validation import ApplicationValidationException
from application.service_factories.auth import AuthServiceFactory, RegistrationServiceFactory
from application.services.auth import AuthAppService, RegistrationAppService
from domain.exceptions.auth import InvalidCredentialsException
from domain.exceptions.validation import ValidationException
from domain.value_objects.data import UserCreateData
from domain.value_objects.token import AccessPayload, AccessTokenVo
from domain.exceptions.user import UsernameAlreadyExistsException, EmailAlreadyExistsException
from application.dto.auth import AccessPayloadDto

class LoginView(APIView):
    parser_classes = [FormParser]

    @staticmethod
    def post(request: Request) -> Response:
        form_data: QueryDict = cast(QueryDict, request.data)
        logger.debug(f"request data = {form_data}")

        auth_service: AuthAppService = AuthServiceFactory.get_auth_service()
        try:
            tokens_pair_dto: TokenPairDto = auth_service.login(form_data)
        except (InvalidCredentialsException, ValidationException) as e:
            logger.error(e)
            return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)

        return Response(asdict(tokens_pair_dto), 200)


class RegistrationView(APIView):
    parser_classes = [FormParser]

    @staticmethod
    def post(request: Request) -> Response:
        form_data: QueryDict = cast(QueryDict, request.data)
        registration_service: RegistrationAppService = RegistrationServiceFactory.get_registration_service()
        try:
            registration_service.register(form_data)
        except (ValidationException, UsernameAlreadyExistsException, EmailAlreadyExistsException) as e:
            log.error(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "User has registered successfully."}, status.HTTP_201_CREATED)


class ReissueAccessTokenView(APIView):
    parser_classes = [FormParser]

    @staticmethod
    def post(request: Request) -> Response:
        auth_service: AuthAppService = AuthServiceFactory.get_auth_service()

        try:
            access_token_dto: AccessTokenDto = auth_service.reissue_access(cast(QueryDict, request.data))
        except (ValidationException, InvalidTokenException) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(asdict(access_token_dto), status=status.HTTP_200_OK)


class AccessVerifyView(APIView):
    parser_classes = [FormParser]

    @staticmethod
    def post(request: Request) -> Response:
        auth_service: AuthAppService = AuthServiceFactory.get_auth_service()

        try:
            access_payload_dto: AccessPayloadDto = auth_service.verify_access(cast(QueryDict, request.data))
        except (ValidationException, InvalidTokenException) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(asdict(access_payload_dto), status=status.HTTP_200_OK)
