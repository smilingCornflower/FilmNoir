from typing import cast

from django.http import QueryDict
from loguru import logger

from domain.exceptions.validation import ValidationException
from domain.value_objects.common import Id, RatingVo, YearVo
from domain.value_objects.filter import MovieFilter


def _query_params_to_movie_filter(query_params: QueryDict) -> MovieFilter:
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


def query_params_to_movie_filter(query_params: QueryDict) -> MovieFilter:
    """:raises ValidationException:"""
    logger.debug(f"query_params = {query_params}")
    try:
        return _query_params_to_movie_filter(query_params)
    except ValueError as e:
        logger.error("Failed to convert query_params to MovieFilter.")
        raise ValidationException("Invalid query parameters format.")
