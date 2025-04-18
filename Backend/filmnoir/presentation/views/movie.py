from dataclasses import asdict

from loguru import logger
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import cast
from django.http import QueryDict
from application.dto.movie import MovieDto
from application.service_factories.movie import MovieServiceFactory
from application.services.movie import MovieAppService


class MovieReadView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        logger.info(f"request data type = {type(request.query_params)}")  # dict
        movie_service: MovieAppService = MovieServiceFactory.get_read_service()
        movies: list[MovieDto] = movie_service.get_all(cast(QueryDict, request.query_params))
        logger.debug(f"found {len(movies)} movies")

        return Response(list(map(asdict, movies)), status=status.HTTP_200_OK)
