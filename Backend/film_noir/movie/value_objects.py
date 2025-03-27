from dataclasses import dataclass

from common.type_aliases import DescriptionT, GenreT, IdT, RatingT, TitleT, YearT
from common.value_objects import ActorVo, DirectorVo, GenreVo, PosterVo, VideoVo


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
