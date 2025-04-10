from dataclasses import dataclass

from domain.ports.filter import AbstractFilter
from domain.value_objects.common import Id, YearVo, RatingVo


@dataclass
class MovieFilter(AbstractFilter):
    id_: Id | None = None
    years: list[YearVo] | None = None
    min_year: YearVo | None = None
    max_year: YearVo | None = None

    min_rating: RatingVo | None = None
    max_rating: RatingVo | None = None

    genre_ids: list[Id] | None = None
    actor_ids: list[Id] | None = None
    director_ids: list[Id] | None = None

