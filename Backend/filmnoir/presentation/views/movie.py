from loguru import logger as log
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.mappers.query_params_to_movie_filter import (
    QueryParamsToMovieFilterMapper,
)
from application.serializers.movie import MovieSerializer
from application.services.movie import MovieReadService
from domain.models.movie import Movie
from domain.value_objects.filter import MovieFilter
from infrastructure.repositories.movie import DjMovieReadRepository


class MovieReadView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        log.info(f"{request.query_params}")

        movie_filter: MovieFilter = QueryParamsToMovieFilterMapper.map(request.query_params)
        log.debug(f"{movie_filter=}")

        movie_service = MovieReadService(DjMovieReadRepository())
        movies: list[Movie] = movie_service.get_all(movie_filter)
        log.debug(f"found {len(movies)} movies")

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
