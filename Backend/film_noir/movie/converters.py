from django.http import QueryDict
from loguru import logger
from rest_framework.exceptions import ParseError

from common.type_aliases import GenreT, YearT
from common.value_objects import ActorVo, DirectorVo
from movie.value_objects import MovieQueryParamsVo


class MovieQueryParamsVoConverter:
    @staticmethod
    def _get_vo_from_query_dict(data: QueryDict) -> MovieQueryParamsVo:
        years: list[YearT] = [int(i) for i in data.getlist("years", [])]
        genres: list[GenreT] = [str(i) for i in data.getlist("genres", [])]
        actors: list[ActorVo] = []

        for i in data.getlist("actors", []):
            name, surname = i.split()
            actors.append(ActorVo(name=name, surname=surname))
        directors: list[DirectorVo] = []
        for i in data.getlist("directors", []):
            name, surname = i.split()
            directors.append(DirectorVo(name=name, surname=surname))

        return MovieQueryParamsVo(
            years=years, genres=genres, actors=actors, directors=directors
        )

    @classmethod
    def get_vo_from_query_dict(cls, data: QueryDict) -> MovieQueryParamsVo:
        try:
            return cls._get_vo_from_query_dict(data)
        except ValueError as e:
            logger.error(e)
            raise ParseError("Incorrect request")
