from dataclasses import dataclass

from domain.ports.filter import AbstractFilter
from domain.value_objects.common import Id, RatingVo, YearVo
from domain.value_objects.user import Email, Username


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


@dataclass
class UserFilter(AbstractFilter):
    id_: Id | None = None
    username: Username | None = None
    email: Email | None = None



