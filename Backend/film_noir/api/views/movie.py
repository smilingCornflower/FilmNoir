from loguru import logger
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.converters import MovieQueryParamsVoConverter
from movie.models import Movie
from movie.serializer import MovieSerializer
from movie.service import MovieService
from movie.value_objects import MovieQueryParamsVo

from api.schemas.movie import movie_get_schema


class MovieView(APIView):
    @staticmethod
    @movie_get_schema
    def get(request: Request) -> Response:
        logger.debug(f"request query parameters = {request.query_params}")
        params_vo: MovieQueryParamsVo = (
            MovieQueryParamsVoConverter.get_vo_from_query_dict(request.query_params)
        )
        logger.debug(f"converted parameters value object = {params_vo}")
        movies: list[Movie] = MovieService.get(params_vo)

        logger.info(f"{len(movies)} items found")
        return Response(MovieSerializer(movies, many=True).data)
