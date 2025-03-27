from typing import Self
from dataclasses import dataclass

from common.value_objects import (
    GenreVo,
    ActorVo,
    DirectorVo,
    PosterVo,
    VideoVo,
)
from common.type_aliases import IdT, TitleT, DescriptionT, YearT, RatingT, GenreT


@dataclass(frozen=True)
class MovieVo:
    id: IdT
    title: TitleT
    description: DescriptionT
    year: YearT
    rating: RatingT
    genres: list[GenreVo]
    actors: list[ActorVo]
    director: DirectorVo
    poster: PosterVo
    video: VideoVo | None


@dataclass(frozen=True)
class MovieQueryParamsVo:
    years: list[YearT]
    genres: list[GenreT]
    actors: list[ActorVo]
    directors: list[DirectorVo]
