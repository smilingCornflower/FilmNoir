from django.db.models import Q

from movie.models import Movie
from movie.value_objects import MovieVo, MovieQueryParamsVo
from movie.serializer import MovieSerializer
from typing import Iterable


class MovieService:
    @staticmethod
    def get(params: MovieQueryParamsVo) -> Iterable[Movie]:
        query: Q[Movie] = Q()

        if params.years:
            query |= Q(year__in=params.years)
        if params.genres:
            query |= Q(genres__name__in=params.genres)
        if params.actors:
            for actor in params.actors:
                query |= Q(actors__name=actor.name, actors__surname=actor.surname)

        result = Movie.objects.filter(query).distinct()
        return result
