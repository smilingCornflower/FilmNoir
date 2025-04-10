from typing import cast

from django.http import QueryDict

from domain.value_objects.common import Id, YearVo, RatingVo
from domain.value_objects.filter import MovieFilter


class QueryParamsToMovieFilterMapper:
    @classmethod
    def map(cls, query_params: QueryDict) -> MovieFilter:
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
            result.min_rating = RatingVo(float(cast(str, query_params.get("min_rating"))))
        if query_params.get("max_rating"):
            result.max_rating = RatingVo(float(cast(str, query_params.get("max_rating"))))

        if query_params.getlist("genre_ids"):
            result.genre_ids = [Id(int(i)) for i in query_params.getlist("genre_ids")]
        if query_params.getlist("actor_ids"):
            result.actor_ids = [Id(int(i)) for i in query_params.getlist("actor_ids")]
        if query_params.getlist("director_ids"):
            result.director_ids = [Id(int(i)) for i in query_params.getlist("director_ids")]

        return result
