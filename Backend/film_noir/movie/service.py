from django.db.models import Q

from common.service import BaseContentService
from movie.models import Movie
from movie.value_objects import MovieQueryParamsVo


class MovieService(BaseContentService[Movie, MovieQueryParamsVo]):
    @classmethod
    def get(cls, params: MovieQueryParamsVo) -> list[Movie]:
        query = Q()

        if params.years:
            query |= Q(year__in=params.years)
        if params.genres:
            query |= Q(genres__name__in=params.genres)
        if params.actors:
            for actor in params.actors:
                query |= Q(actors__name=actor.name, actors__surname=actor.surname)

        result = list(Movie.objects.filter(query).distinct())

        return result
