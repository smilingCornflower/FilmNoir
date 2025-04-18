from domain.services.movie import MovieReadService
from django.http import QueryDict
from application.dto.movie import MovieDto
from application.converters.request_converters.movie import query_params_to_movie_filter
from domain.value_objects.common import Id
from domain.models.movie import Movie
from domain.exceptions.media import MovieNotFound
from application.converters.response_converters.movie import convert_movies_to_dto, convert_movie_to_dto
from domain.value_objects.filter import MovieFilter


class MovieAppService:
    def __init__(self, movie_read_service: MovieReadService):
        self._movie_read_service = movie_read_service

    def get_by_id(self, id_: int) -> MovieDto:
        """:raises MovieNotFound:"""
        movie: Movie = self._movie_read_service.get_by_id(Id(id_))
        movie_dto: MovieDto = convert_movie_to_dto(movie)
        return movie_dto

    def get_all(self, query_params: QueryDict) -> list[MovieDto]:
        """:raises ValidationException:"""
        movie_filter: MovieFilter = query_params_to_movie_filter(query_params)
        movies: list[Movie] = self._movie_read_service.get_all(movie_filter)
        movies_dto: list[MovieDto] = convert_movies_to_dto(movies)
        return movies_dto
