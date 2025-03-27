from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from movie.models import Movie
from movie.serializer import MovieSerializer, MovieQueryParamsSerializer
from movie.service import MovieService
from movie.value_objects import MovieQueryParamsVo, MovieVo
from typing import Iterable
from film_noir.settings import logger


class MovieView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        logger.debug(f"{request.query_params=}")
        params_vo: MovieQueryParamsVo = MovieQueryParamsSerializer(
            request.query_params
        ).get_vo()
        logger.debug(f"{params_vo=}")

        movies: Iterable[Movie] = MovieService.get(params_vo)
        return Response(MovieSerializer(movies, many=True).data)
