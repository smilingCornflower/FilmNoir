from typing import cast

from django.http import QueryDict

from domain.value_objects.common import Id, YearVo, RatingVo
from domain.value_objects.filter import MovieFilter
from rest_framework.exceptions import ParseError
from loguru import logger as log
from application.ports.mapper import AbstractMapper
from application.exceptions.mapping import MappingException


class QueryParamsToMovieFilterMapper(AbstractMapper):
    @classmethod
    def map(cls, query_params: QueryDict) -> MovieFilter:
        """:raises ParseError"""
        try:
            return cls._map(query_params)
        except ValueError as e:
            log.error(f"Failed to parse query_params: {e}")
            raise MappingException("Failed to parse URL or query parameters")

    @classmethod
    def _map(cls, query_params: QueryDict) -> MovieFilter:
        """:raises ValueError:"""
        result = MovieFilter()
        if query_params.get("id"):
            result.id_ = Id(int(cast(str, query_params.get("id"))))

        if query_params.getlist("years"):
            result.years = [YearVo(int(i)) for i in query_params.getlist("years")]

        if query_params.get("min_year"):
            result.min_year = YearVo(int(cast(str, query_params.get("min_year"))))
        if query_params.get("max_year"):
            result.max_year = YearVo(int(cast(str, query_params.get("max_year"))))

        if query_params.get("min_rating"):
            result.min_rating = RatingVo(
                float(cast(str, query_params.get("min_rating")))
            )
        if query_params.get("max_rating"):
            result.max_rating = RatingVo(
                float(cast(str, query_params.get("max_rating")))
            )

        if query_params.getlist("genre_ids"):
            result.genre_ids = [Id(int(i)) for i in query_params.getlist("genre_ids")]
        if query_params.getlist("actor_ids"):
            result.actor_ids = [Id(int(i)) for i in query_params.getlist("actor_ids")]
        if query_params.getlist("director_ids"):
            result.director_ids = [
                Id(int(i)) for i in query_params.getlist("director_ids")
            ]

        return result
