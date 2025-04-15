from typing import cast

from django.http import QueryDict
from loguru import logger as log
from rest_framework import status
from rest_framework.parsers import FormParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from application.exceptions.mapping import MappingException
from application.exceptions.validation import ApplicationValidationException
from application.mappers.form_data_to_user_create import FormDataToUserCreate
from application.service_factories.auth import AuthServiceFactory
from application.service_factories.user import UserServiceFactory
from application.services.auth import AuthAppService
from application.services.user import UserRegistrationService
from domain.exceptions.user import (
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from domain.value_objects.data import UserCreateData
from domain.value_objects.tokens import AccessTokenVo, TokenPairVo, AccessPayload


class LoginView(APIView):
    parser_classes = [FormParser]

    @staticmethod
    def post(request: Request) -> Response:
        auth_service: AuthAppService = AuthServiceFactory.get_auth_service()

        # TODO: KeyError
        email: str | None = request.data.get("email")
        password: str | None = request.data.get("password")
        if not (email and password):
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tokens: TokenPairVo = auth_service.login(email, password)
        try:
            return Response(
                {
                    "access_token": tokens.access.value,
                    "refresh_token": tokens.refresh.value,
                    "expires_at": tokens.access.expires_at.isoformat(),
                },
                status=status.HTTP_200_OK,
            )
        except ApplicationValidationException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegistrationView(APIView):
    parser_classes = [FormParser]

    @staticmethod
    def post(request: Request) -> Response:
        form_data: QueryDict = cast(QueryDict, request.data)
        user_service: UserRegistrationService = (
            UserServiceFactory.get_registration_service()
        )
        try:
            user_create_data: UserCreateData = FormDataToUserCreate.map(form_data)

            log.debug(f"username={user_create_data.username}")
            log.debug(f"email={user_create_data.email}")
            log.debug(f"password={'*' * len(user_create_data.password.value)}")

            user_service.register(user_create_data)

        except (
            MappingException,
            UsernameAlreadyExistsException,
            EmailAlreadyExistsException,
        ) as e:
            log.error(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": "success"}, 200)


class TokenRefreshView(APIView):
    @staticmethod
    def post(request: Request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        auth_service: AuthAppService = AuthServiceFactory.get_auth_service()
        try:
            access_token: AccessTokenVo = auth_service.reissue_access(refresh_token)
        except ApplicationValidationException:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                "access_token": access_token.value,
                "expires_at": access_token.expires_at.isoformat(),
            },
            status=status.HTTP_200_OK,
        )


class TokenVerifyView(APIView):
    @staticmethod
    def post(request: Request):
        auth_service: AuthAppService = AuthServiceFactory.get_auth_service()
        access_token = request.data.get('access_token')
        if not access_token:
            return Response(
                {"error": "Access token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            payload: AccessPayload = auth_service.verify_access_token(access_token)
        except ApplicationValidationException as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({
                "user_id": payload.user_id,
                "email": payload.email,
                "expires_at": datetime.fromtimestamp(payload.exp).isoformat()
            }, status=status.HTTP_200_OK)
